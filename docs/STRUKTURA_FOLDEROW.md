# 📁 PROPONOWANA STRUKTURA PROJEKTU

## 🎯 AKTUALNA (CHAOS):
```
/workspace/
├── monolit.py
├── routers_full.py
├── assistant_endpoint.py
├── frontend.html
├── paint.html
├── .env
├── facts_complete.json
├── generate_5000_facts.py
├── README.md
├── FINAL_COMPLETE.md
├── deployment/
└── ... (40+ plików w rootcie)
```

## ✅ NOWA (CZYTELNA):

```
/workspace/
│
├── 📚 docs/                          # Dokumentacja
│   ├── README.md
│   ├── FINAL_COMPLETE.md
│   ├── REAL_VS_FAKE.md
│   ├── CO_TERAZ_DZIALA.md
│   ├── JAK_DZIALA_WIEDZA.md
│   └── FILES_TO_DEPLOY.txt
│
├── 🔧 backend/                       # Backend Python
│   ├── monolit.py                    # Core
│   ├── routers/                      # Endpointy
│   │   ├── __init__.py
│   │   ├── routers_full.py
│   │   ├── assistant_endpoint.py
│   │   ├── psyche_endpoint.py
│   │   ├── files_endpoint.py
│   │   ├── travel_endpoint.py
│   │   └── admin_endpoint.py
│   ├── modules/                      # Moduły pomocnicze
│   │   ├── __init__.py
│   │   ├── middleware.py
│   │   ├── prompt.py
│   │   ├── autonauka_pro.py
│   │   └── writer_pro.py
│   └── requirements.txt
│
├── 🎨 frontend/                      # Frontend
│   ├── index.html                    # (frontend.html)
│   ├── paint.html
│   └── assets/                       # (opcjonalnie)
│       ├── css/
│       ├── js/
│       └── images/
│
├── 📊 data/                          # Bazy danych (gitignore)
│   ├── monolit.db
│   ├── mem/
│   └── uploads/
│
├── 📚 knowledge/                     # Wiedza / Fakty
│   ├── facts_complete.json           # 5200+ faktów
│   ├── facts_5000.json
│   ├── scripts/
│   │   ├── generate_5000_facts.py
│   │   ├── generate_more_facts.py
│   │   └── upload_facts.py
│   └── README.md                     # Jak dodać fakty
│
├── 🚀 deployment/                    # Deploy ready
│   ├── .env.example
│   ├── SETUP_SERVER.sh
│   ├── WGRYWANIE_WIEDZY.md
│   └── README.md
│
├── 🧪 scripts/                       # Utility scripts
│   ├── start.sh
│   ├── download_list.sh
│   └── organize.sh                   # Ten skrypt!
│
├── 📤 out/                           # Outputy (gitignore)
│   ├── images/
│   ├── writing/
│   └── dev/
│
├── 🗂️ Root files                     # Ważne pliki w rootcie
│   ├── .env                          # (gitignore)
│   ├── .env.example
│   ├── .gitignore
│   ├── README.md                     # Main readme
│   └── start.sh                      # Quick start
│
└── 📦 Inne
    ├── tmp/
    ├── logs/
    └── queue/
```

## 🔥 ZALETY NOWEJ STRUKTURY:

### 1. **Przejrzystość**
- Łatwo znaleźć co szukasz
- Logiczne grupowanie

### 2. **Skalowalne**
- Łatwo dodać nowe moduły
- Backend/Frontend separacja

### 3. **Deploy-ready**
- Folder `deployment/` ma wszystko
- Jasne co kopiować na serwer

### 4. **Dokumentacja**
- Wszystko w `docs/`
- Nie miesza się z kodem

### 5. **Gitignore**
- Jasne co jest tracked
- `data/`, `out/`, `.env` - ignored

## 📋 MAPOWANIE (stare → nowe):

```
ROOT
├── monolit.py                    → backend/monolit.py
├── routers_full.py               → backend/routers/routers_full.py
├── assistant_endpoint.py         → backend/routers/assistant_endpoint.py
├── psyche_endpoint.py            → backend/routers/psyche_endpoint.py
├── files_endpoint.py             → backend/routers/files_endpoint.py
├── travel_endpoint.py            → backend/routers/travel_endpoint.py
├── admin_endpoint.py             → backend/routers/admin_endpoint.py
├── middleware.py                 → backend/modules/middleware.py
├── prompt.py                     → backend/modules/prompt.py
├── autonauka_pro.py              → backend/modules/autonauka_pro.py
├── writer_pro.py                 → backend/modules/writer_pro.py
├── frontend.html                 → frontend/index.html
├── paint.html                    → frontend/paint.html
├── facts_complete.json           → knowledge/facts_complete.json
├── facts_5000.json               → knowledge/facts_5000.json
├── generate_5000_facts.py        → knowledge/scripts/generate_5000_facts.py
├── generate_more_facts.py        → knowledge/scripts/generate_more_facts.py
├── README.md                     → docs/README.md (+ kopia w root)
├── FINAL_COMPLETE.md             → docs/FINAL_COMPLETE.md
├── REAL_VS_FAKE.md               → docs/REAL_VS_FAKE.md
├── CO_TERAZ_DZIALA.md            → docs/CO_TERAZ_DZIALA.md
├── JAK_DZIALA_WIEDZA.md          → docs/JAK_DZIALA_WIEDZA.md
├── start.sh                      → scripts/start.sh (+ symlink w root)
└── download_list.sh              → scripts/download_list.sh

DEPLOYMENT (pozostaje jak jest)
├── deployment/*                  → deployment/* (bez zmian)

IGNOROWANE (zostają ale w .gitignore)
├── data/*                        → data/* (gitignore)
├── out/*                         → out/* (gitignore)
├── tmp/*                         → tmp/* (gitignore)
```

## 🚀 UŻYCIE:

```bash
# Automatyczne uporządkowanie:
bash organize.sh

# Albo ręcznie:
mkdir -p backend/routers backend/modules frontend knowledge/scripts docs scripts
mv monolit.py backend/
mv *_endpoint.py backend/routers/
mv middleware.py prompt.py autonauka_pro.py writer_pro.py backend/modules/
mv frontend.html frontend/index.html
mv facts*.json knowledge/
# itd...
```

## ⚠️ CO TRZEBA POPRAWIĆ PO ORGANIZE:

1. **Import paths w Pythonie:**
   ```python
   # Przed:
   import routers_full
   
   # Po:
   from backend.routers import routers_full
   ```

2. **start.sh paths:**
   ```bash
   # Przed:
   python3 -m uvicorn monolit:app
   
   # Po:
   python3 -m uvicorn backend.monolit:app
   ```

3. **Frontend paths:**
   ```javascript
   // Raczej bez zmian, bo serwowane przez FastAPI
   ```

## 🎯 ALBO PROSTSZE ROZWIĄZANIE (minimize changes):

```
/workspace/
├── 📚 docs/              # Cała dokumentacja
├── 🧪 scripts/           # Utility scripts
├── 📚 knowledge/         # Fakty + generatory
├── 🚀 deployment/        # Deploy ready (jak jest)
├── 📊 data/              # Bazy (jak jest, gitignore)
├── 📤 out/               # Outputs (jak jest, gitignore)
└── ROOT                  # Kod pozostaje w rootcie
    ├── monolit.py
    ├── *_endpoint.py
    ├── frontend.html
    ├── .env, start.sh, etc.
```

**To wymaga ZERO zmian w kodzie!** Tylko przeniesienie docs/scripts/knowledge.
