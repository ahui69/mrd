# 📚 KOMPLETNA LISTA WSZYSTKICH API ENDPOINTÓW

## 🤖 CHAT & ASSISTANT

### `/api/chat/*` - All-in-one Assistant
- `POST /api/chat/assistant` - Główny endpoint chatu (STM+LTM+Research+Semantic)
- `GET /api/chat/history` - Historia rozmów
- `POST /api/chat/feedback` - User feedback
- `POST /api/chat/assistant/stream` - Streaming response (SSE)

### `/api/llm/*` - Direct LLM
- `POST /api/llm/chat` - Prosty chat z LLM

---

## 💾 PAMIĘĆ (MEMORY)

### `/api/memory/*` - STM (Short-term Memory)
- `POST /api/memory/add` - Dodaj wiadomość
- `GET /api/memory/context?limit=20` - Pobierz kontekst

### `/api/ltm/*` - LTM (Long-term Memory)  
- `POST /api/ltm/add` - Dodaj fakt
- `GET /api/ltm/search?q=query&limit=10` - Szukaj faktów
- `POST /api/ltm/delete` - Usuń fakt
- `POST /api/ltm/reindex` - Rebuild indeksów

---

## 🧠 PSYCHIKA AI

### `/api/psyche/*` - Stan psychiczny
- `GET /api/psyche/state` - Pobierz stan (mood, energy, Big Five)
- `POST /api/psyche/state` - Zaktualizuj stan
- `POST /api/psyche/observe` - Obserwuj tekst (sentiment)
- `POST /api/psyche/episode` - Dodaj epizod psychiczny
- `GET /api/psyche/reflect` - Refleksja (statystyki)
- `GET /api/psyche/tune` - Parametry LLM z psychiki
- `POST /api/psyche/reset` - Reset do domyślnych

---

## 🔍 RESEARCH & AUTONAUKA

### `/api/research/*` - Web Research
- `GET /api/research/sources?q=query&topk=8&deep=false` - Web research z źródłami

### `/api/search/*` - Search with AI
- `GET /api/search/answer?q=query&deep=false` - Odpowiedź z cytowaniem źródeł

### `/api/news/*` - News
- `GET /api/news/duck?q=query&limit=10` - DuckDuckGo news

---

## 📝 WRITER PRO

### `/api/write/*` - Generowanie tekstów
- `POST /api/write/creative` - Tworzenie treści
- `POST /api/write/rewrite` - Przepisywanie
- `POST /api/write/seo` - Artykuły SEO
- `POST /api/write/social` - Posty social media
- `POST /api/write/batch` - Batch generation

---

## 📁 PLIKI (FILES)

### `/api/files/*` - Upload, Download, Analyze
- `POST /api/files/upload` - Upload (multipart/form-data)
- `POST /api/files/upload/base64` - Upload (base64)
- `GET /api/files/list` - Lista plików
- `GET /api/files/download/{file_id}` - Download
- `POST /api/files/analyze` - Analiza pliku (OCR, parsing)
- `DELETE /api/files/{file_id}` - Usuń plik
- `GET /api/files/stats` - Statystyki
- `POST /api/files/batch/analyze` - Batch analiza

**Obsługiwane formaty:**
- 📄 PDF (text extraction)
- 🖼️ Images: JPG, PNG, GIF, WEBP (OCR + analysis)
- 📦 ZIP (list contents)
- 📝 Text: TXT, MD, PY, JS, JSON, YAML, HTML, CSS
- 🎥 Video: MP4, AVI, MOV, MKV (metadata)
- 🎵 Audio: MP3, WAV, OGG

---

## 🗺️ TRAVEL & MAPS

### `/api/travel/*` - Podróże i mapy
- `GET /api/travel/search?city=Kraków&what=attractions` - Szukaj w mieście
  - `what`: attractions | hotels | restaurants
- `GET /api/travel/geocode?city=Warszawa` - Geocoding (współrzędne)
- `GET /api/travel/attractions/{city}` - Atrakcje
- `GET /api/travel/hotels/{city}` - Hotele
- `GET /api/travel/restaurants/{city}` - Restauracje
- `GET /api/travel/trip-plan?city=Gdańsk&days=3&interests=culture,food` - AI trip planner

**Źródła danych:**
- OpenTripMap API
- SERPAPI Google Maps
- Overpass API (OpenStreetMap)

---

## 🎯 SEMANTIC ANALYSIS

### `/api/semantic/*` - Analiza semantyczna
- `POST /api/semantic/analyze` - Analiza tekstu
  - Sentiment analysis
  - Intent detection
  - Entity extraction
  - Topic detection
  - Keyword extraction
- `POST /api/semantic/analyze_conversation` - Analiza rozmowy
- `POST /api/semantic/enhance_response` - Ulepszenie odpowiedzi

---

## ⚽ SPORTS (Mock)

### `/api/sports/*` - Wyniki sportowe
- `GET /api/sports/scores?league=nba` - Scores (mock - ready for ESPN API)

---

## 🛠️ SYSTEM

### `/api/system/*` - System & Admin
- `GET /api/system/stats` - Statystyki (CPU, RAM, DB, Psyche)
- `POST /api/system/optimize` - Optymalizuj bazę danych
- `POST /api/system/backup` - Backup danych

### `/api/health` - Health check
- `GET /api/health` - Status serwera (bez auth)

---

## 🌐 FRONTEND

### Główna aplikacja
- `GET /` - Frontend HTML
- `GET /app` - Frontend (alias)
- `GET /chat` - Frontend (alias)

### Dokumentacja
- `GET /docs` - Swagger UI (interaktywna dokumentacja)
- `GET /redoc` - ReDoc (czytelna dokumentacja)
- `GET /openapi.json` - OpenAPI schema

---

## 🔑 AUTENTYKACJA

**Wszystkie endpointy (oprócz `/api/health`, `/`, `/docs`) wymagają:**

```
Authorization: Bearer 0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5
```

---

## 📊 PODSUMOWANIE

### Liczba endpointów: **55+**

### Kategorie:
- 🤖 Chat & AI: 5
- 💾 Memory: 6
- 🧠 Psyche: 7
- 🔍 Research: 4
- 📝 Writer: 5
- 📁 Files: 8
- 🗺️ Travel: 6
- 🎯 Semantic: 3
- ⚽ Sports: 1
- 🛠️ System: 4
- 🌐 Frontend: 6

### Funkcje unikalne:
- ✅ Psychika AI z Big Five
- ✅ Auto STM→LTM rotacja
- ✅ Hybrid search (BM25 + semantic)
- ✅ File parsing (PDF, OCR, video)
- ✅ Travel planning z AI
- ✅ Semantic enhancement
- ✅ Real-time voice input (frontend)
- ✅ Conversation persistence

**PRODUCTION READY!** 🚀
