#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
travel_endpoint.py - Travel & Maps endpoints
Wykorzystuje funkcje travel_search() z monolit.py
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os

router = APIRouter(prefix="/api/travel")

# Auth
AUTH_TOKEN = os.getenv("AUTH_TOKEN") or os.getenv("AUTH") or "changeme"
def _auth(req: Request):
    tok = (req.headers.get("Authorization","") or "").replace("Bearer ","").strip()
    if not tok or tok != AUTH_TOKEN:
        raise HTTPException(401, "unauthorized")

# ===== ENDPOINTS =====

@router.get("/search")
async def search_travel(
    city: str,
    what: str = "attractions",  # attractions|hotels|restaurants
    _=Depends(_auth)
):
    """
    🗺️ Wyszukaj miejsca w mieście
    
    Parametry:
    - city: nazwa miasta (np. "Warszawa", "Kraków")
    - what: co szukamy
      - "attractions" - atrakcje turystyczne
      - "hotels" - hotele
      - "restaurants" - restauracje i kawiarnie
    
    Źródła:
    - OpenTripMap API (geocoding)
    - SERPAPI Google Maps (hotele, atrakcje)
    - Overpass API / OpenStreetMap (restauracje)
    
    Przykład:
    ```
    GET /api/travel/search?city=Kraków&what=restaurants
    ```
    """
    try:
        import monolit as M
        if not hasattr(M, 'travel_search'):
            raise HTTPException(500, "travel_search() not available")
        
        result = M.travel_search(city, what)
        
        if not result.get("ok"):
            raise HTTPException(400, result.get("error", "Search failed"))
        
        return result
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@router.get("/geocode")
async def geocode_city(city: str, _=Depends(_auth)):
    """
    📍 Pobierz współrzędne geograficzne miasta
    
    Używa OpenTripMap API do geocodingu
    
    Przykład:
    ```
    GET /api/travel/geocode?city=Gdańsk
    ```
    
    Zwraca:
    ```json
    {
        "ok": true,
        "city": "Gdańsk",
        "coordinates": {
            "lat": 54.352,
            "lon": 18.646
        }
    }
    ```
    """
    try:
        import monolit as M
        if not hasattr(M, 'otm_geoname'):
            raise HTTPException(500, "otm_geoname() not available")
        
        coords = M.otm_geoname(city)
        
        if not coords:
            return {
                "ok": False,
                "error": "City not found or OpenTripMap API key missing"
            }
        
        lon, lat = coords
        
        return {
            "ok": True,
            "city": city,
            "coordinates": {
                "lat": lat,
                "lon": lon
            }
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@router.get("/attractions/{city}")
async def get_attractions(city: str, limit: int = 20, _=Depends(_auth)):
    """🏛️ Szybki dostęp do atrakcji"""
    try:
        import monolit as M
        result = M.travel_search(city, "attractions")
        items = result.get("items", [])[:limit]
        return {
            "ok": True,
            "city": city,
            "attractions": items,
            "count": len(items)
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/hotels/{city}")
async def get_hotels(city: str, limit: int = 20, _=Depends(_auth)):
    """🏨 Szybki dostęp do hoteli"""
    try:
        import monolit as M
        result = M.travel_search(city, "hotels")
        items = result.get("items", [])[:limit]
        return {
            "ok": True,
            "city": city,
            "hotels": items,
            "count": len(items)
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/restaurants/{city}")
async def get_restaurants(city: str, limit: int = 20, _=Depends(_auth)):
    """🍽️ Szybki dostęp do restauracji"""
    try:
        import monolit as M
        result = M.travel_search(city, "restaurants")
        items = result.get("items", [])[:limit]
        return {
            "ok": True,
            "city": city,
            "restaurants": items,
            "count": len(items)
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/trip-plan")
async def plan_trip(
    city: str,
    days: int = 3,
    interests: str = "culture,food",  # culture,food,nature,nightlife,shopping
    _=Depends(_auth)
):
    """
    🗓️ Zaplanuj wycieczkę (AI-powered)
    
    Generuje plan wycieczki bazując na:
    - Długość pobytu (dni)
    - Zainteresowania
    - Dostępne atrakcje
    
    Przykład:
    ```
    GET /api/travel/trip-plan?city=Kraków&days=2&interests=culture,food
    ```
    """
    try:
        import monolit as M
        
        # Pobierz atrakcje
        attractions_result = M.travel_search(city, "attractions")
        restaurants_result = M.travel_search(city, "restaurants")
        
        attractions = attractions_result.get("items", [])[:10]
        restaurants = restaurants_result.get("items", [])[:10]
        
        # Przygotuj kontekst dla LLM
        context = f"""
Miasto: {city}
Dni: {days}
Zainteresowania: {interests}

Dostępne atrakcje:
{chr(10).join([f"- {a.get('title', 'Unknown')}" for a in attractions[:8]])}

Dostępne restauracje:
{chr(10).join([f"- {r.get('name', 'Unknown')}" for r in restaurants[:8]])}
"""
        
        # Wywołaj LLM
        if hasattr(M, 'call_llm'):
            plan = M.call_llm([{
                "role": "system",
                "content": "Jesteś ekspertem od planowania podróży. Stwórz szczegółowy plan wycieczki."
            }, {
                "role": "user",
                "content": f"Zaplanuj {days}-dniową wycieczkę do {city}. Zainteresowania: {interests}\n\n{context}\n\nStwórz plan dzień po dniu z konkretnymi miejscami do odwiedzenia."
            }])
        else:
            plan = f"Plan wycieczki do {city} na {days} dni (wymaga LLM)"
        
        return {
            "ok": True,
            "city": city,
            "days": days,
            "interests": interests.split(','),
            "plan": plan,
            "suggested_places": {
                "attractions": attractions[:5],
                "restaurants": restaurants[:5]
            }
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")
