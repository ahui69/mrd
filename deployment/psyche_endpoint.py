#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
psyche_endpoint.py - Psychika AI (Big Five + Mood)
System symulacji stanu psychicznego AI który wpływa na odpowiedzi
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os

router = APIRouter(prefix="/api/psyche")

# Auth
AUTH_TOKEN = os.getenv("AUTH_TOKEN") or os.getenv("AUTH") or "changeme"
def _auth(req: Request):
    tok = (req.headers.get("Authorization","") or "").replace("Bearer ","").strip()
    if not tok or tok != AUTH_TOKEN:
        raise HTTPException(401, "unauthorized")

# --- Modele ---
class PsycheUpdate(BaseModel):
    mood: Optional[float] = None            # 0.0 - 1.0 (0=very negative, 1=very positive)
    energy: Optional[float] = None          # 0.0 - 1.0 (0=exhausted, 1=energized)
    focus: Optional[float] = None           # 0.0 - 1.0 (0=scattered, 1=focused)
    openness: Optional[float] = None        # Big Five: Openness to experience
    directness: Optional[float] = None      # Jak bezpośredni w komunikacji
    agreeableness: Optional[float] = None   # Big Five: Agreeableness
    conscientiousness: Optional[float] = None  # Big Five: Conscientiousness
    neuroticism: Optional[float] = None     # Big Five: Neuroticism
    style: Optional[str] = None             # Styl komunikacji (np. "rzeczowy", "emocjonalny")

class ObserveText(BaseModel):
    text: str
    user: str = "default"

class Episode(BaseModel):
    user: str = "default"
    kind: str = "event"                     # msg|event|feedback|learning
    valence: float                          # -1.0 (negative) to 1.0 (positive)
    intensity: float                        # 0.0 (weak) to 1.0 (strong)
    tags: str = ""
    note: str = ""

# --- Endpoints ---

@router.get("/state")
async def get_psyche_state(_=Depends(_auth)):
    """
    📊 Pobierz aktualny stan psychiczny AI
    
    Zwraca wszystkie parametry psychiki (Big Five + mood + energy + focus)
    """
    try:
        import monolit as M
        if not hasattr(M, 'psy_get'):
            raise HTTPException(500, "Psyche module not available")
        
        state = M.psy_get()
        tune = M.psy_tune()
        
        return {
            "ok": True,
            "state": state,
            "llm_tuning": tune,
            "interpretation": {
                "mood_level": "positive" if state['mood'] > 0.5 else "neutral" if state['mood'] > 0 else "negative",
                "energy_level": "high" if state['energy'] > 0.7 else "medium" if state['energy'] > 0.4 else "low",
                "personality_type": _get_personality_type(state)
            }
        }
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@router.post("/state")
async def update_psyche_state(body: PsycheUpdate, _=Depends(_auth)):
    """
    🎛️ Zaktualizuj stan psychiczny AI
    
    Pozwala ręcznie ustawić parametry psychiki.
    Użyj wartości 0.0-1.0 dla każdego parametru.
    """
    try:
        import monolit as M
        if not hasattr(M, 'psy_set'):
            raise HTTPException(500, "Psyche module not available")
        
        updates = {}
        for field in ['mood', 'energy', 'focus', 'openness', 'directness', 
                      'agreeableness', 'conscientiousness', 'neuroticism', 'style']:
            value = getattr(body, field, None)
            if value is not None:
                updates[field] = value
        
        new_state = M.psy_set(**updates)
        
        return {
            "ok": True,
            "state": new_state,
            "updated_fields": list(updates.keys())
        }
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@router.post("/observe")
async def observe_text(body: ObserveText, _=Depends(_auth)):
    """
    👁️ Obserwuj tekst i wpłyń na stan psychiczny
    
    Analizuje tekst pod kątem sentymentu (pozytywne/negatywne słowa)
    i automatycznie modyfikuje stan psychiczny AI.
    
    Pozytywne słowa: super, świetnie, dzięki, dobrze, spoko...
    Negatywne: kurwa, błąd, fatalnie, źle...
    """
    try:
        import monolit as M
        if not hasattr(M, 'psy_observe_text'):
            raise HTTPException(500, "Psyche module not available")
        
        state_before = M.psy_get()
        M.psy_observe_text(body.user, body.text)
        state_after = M.psy_get()
        
        mood_change = state_after['mood'] - state_before['mood']
        
        return {
            "ok": True,
            "text_analyzed": body.text,
            "mood_change": round(mood_change, 3),
            "sentiment": "positive" if mood_change > 0 else "negative" if mood_change < 0 else "neutral",
            "state_before": {k: round(v, 3) if isinstance(v, float) else v for k, v in state_before.items()},
            "state_after": {k: round(v, 3) if isinstance(v, float) else v for k, v in state_after.items()}
        }
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@router.post("/episode")
async def add_episode(body: Episode, _=Depends(_auth)):
    """
    📝 Dodaj epizod psychiczny (event/feedback/learning)
    
    Epizod to znaczące wydarzenie które wpływa na stan psychiczny.
    
    Parametry:
    - valence: -1.0 (bardzo negatywne) do 1.0 (bardzo pozytywne)
    - intensity: 0.0 (słabe) do 1.0 (bardzo silne)
    - kind: typ wydarzenia (msg, event, feedback, learning)
    """
    try:
        import monolit as M
        if not hasattr(M, 'psy_episode_add'):
            raise HTTPException(500, "Psyche module not available")
        
        episode_id = M.psy_episode_add(
            user=body.user,
            kind=body.kind,
            valence=body.valence,
            intensity=body.intensity,
            tags=body.tags,
            note=body.note
        )
        
        new_state = M.psy_get()
        
        return {
            "ok": True,
            "episode_id": episode_id,
            "new_state": new_state
        }
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@router.get("/reflect")
async def psyche_reflect(_=Depends(_auth)):
    """
    🤔 Refleksja psychiczna
    
    Analizuje ostatnie 100 epizodów i zwraca statystyki:
    - Dominant mood (przeważający nastrój)
    - Average valence (średnia walencja)
    - Emotional volatility (zmienność emocjonalna)
    """
    try:
        import monolit as M
        if not hasattr(M, 'psy_reflect'):
            raise HTTPException(500, "Psyche module not available")
        
        reflection = M.psy_reflect()
        
        return {
            "ok": True,
            "reflection": reflection
        }
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@router.get("/tune")
async def get_llm_tuning(_=Depends(_auth)):
    """
    🎛️ Pobierz parametry LLM dostosowane do psychiki
    
    Zwraca temperature i tone dla LLM bazując na aktualnym stanie psychicznym.
    
    Np.:
    - Wysoka openness -> wyższa temperature (więcej kreatywności)
    - Niska energy -> niższa temperature (bardziej przewidywalnie)
    - Wysoka directness -> tone "konkretny"
    """
    try:
        import monolit as M
        if not hasattr(M, 'psy_tune'):
            raise HTTPException(500, "Psyche module not available")
        
        tuning = M.psy_tune()
        state = M.psy_get()
        
        return {
            "ok": True,
            "tuning": tuning,
            "explanation": {
                "temperature": f"Bazuje na: openness({state['openness']:.2f}), directness({state['directness']:.2f}), focus({state['focus']:.2f})",
                "tone": f"Bazuje na: energy({state['energy']:.2f}), directness({state['directness']:.2f})"
            }
        }
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@router.post("/reset")
async def reset_psyche(_=Depends(_auth)):
    """
    🔄 Zresetuj stan psychiczny do wartości domyślnych
    """
    try:
        import monolit as M
        if not hasattr(M, 'psy_set'):
            raise HTTPException(500, "Psyche module not available")
        
        # Domyślne wartości
        default_state = M.psy_set(
            mood=0.0,
            energy=0.6,
            focus=0.6,
            openness=0.55,
            directness=0.62,
            agreeableness=0.55,
            conscientiousness=0.63,
            neuroticism=0.44,
            style="rzeczowy"
        )
        
        return {
            "ok": True,
            "message": "Psyche reset to defaults",
            "state": default_state
        }
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

# --- Helper functions ---

def _get_personality_type(state: Dict[str, Any]) -> str:
    """Określ typ osobowości na podstawie Big Five"""
    o = state.get('openness', 0.5)
    c = state.get('conscientiousness', 0.5)
    e = state.get('energy', 0.5)  # jako proxy dla Extraversion
    a = state.get('agreeableness', 0.5)
    n = state.get('neuroticism', 0.5)
    
    traits = []
    if o > 0.6: traits.append("kreatywny")
    if c > 0.6: traits.append("zorganizowany")
    if e > 0.6: traits.append("energiczny")
    if a > 0.6: traits.append("przyjazny")
    if n < 0.4: traits.append("stabilny emocjonalnie")
    
    if not traits:
        traits.append("zrównoważony")
    
    return ", ".join(traits)
