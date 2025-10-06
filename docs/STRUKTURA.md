# 📁 STRUKTURA PROJEKTU

## ✅ Aktualna organizacja (po uporządkowaniu)

```
/workspace/
│
├── 📚 docs/                        Dokumentacja
│   ├── README.md                   Główny przewodnik
│   ├── FINAL_COMPLETE.md           Pełna dokumentacja systemu
│   ├── REAL_VS_FAKE.md             Co działa a co placeholder
│   ├── JAK_DZIALA_WIEDZA.md        System wiedzy
│   ├── CO_TERAZ_DZIALA.md          Status funkcji
│   ├── FILES_TO_DEPLOY.txt         Lista plików do deploy
│   └── STRUKTURA.md                Ten plik
│
├── 🧪 scripts/                     Utility scripts
│   ├── start.sh                    Uruchamianie serwera
│   ├── download_list.sh            Lista do pobrania
│   └── organize.sh                 Organizacja projektu
│
├── 📚 knowledge/                   Baza wiedzy
│   ├── facts_complete.json         5200+ faktów
│   ├── facts_5000.json             Backup
│   ├── README.md                   Jak wgrać fakty
│   └── generators/                 Generatory faktów
│       ├── generate_5000_facts.py
│       └── generate_more_facts.py
│
├── 🚀 deployment/                  Gotowe do deploy
│   ├── .env.example                Template API keys
│   ├── SETUP_SERVER.sh             Auto-setup
│   ├── WGRYWANIE_WIEDZY.md         Instrukcja
│   └── [wszystkie pliki projektu]
│
├── 📊 data/                        Bazy danych (gitignore)
│   ├── monolit.db                  Główna baza (SQLite)
│   ├── uploads/                    Przesłane pliki
│   └── mem/                        Pamięć
│
├── 📤 out/                         Outputy (gitignore)
│   ├── images/                     Wygenerowane obrazy
│   ├── writing/                    Teksty
│   └── dev/                        Dev outputs
│
├── 📝 logs/                        Logi (gitignore)
│
└── 🔧 ROOT                         Kod źródłowy
    │
    ├── Backend (Python)
    │   ├── monolit.py              Core backend
    │   ├── routers_full.py         Główne endpointy
    │   ├── assistant_endpoint.py   Chat endpoint
    │   ├── psyche_endpoint.py      AI psyche
    │   ├── files_endpoint.py       Upload/download
    │   ├── travel_endpoint.py      Mapy/podróże
    │   ├── admin_endpoint.py       Admin panel
    │   ├── middleware.py           Cache/rate limiting
    │   ├── prompt.py               System prompt
    │   ├── autonauka_pro.py        Research/learning
    │   ├── writer_pro.py           Content generation
    │   └── requirements.txt        Dependencies
    │
    ├── Frontend (HTML/JS)
    │   ├── frontend.html           Główny UI
    │   └── paint.html              Paint editor
    │
    └── Config
        ├── .env                    API keys (gitignore!)
        ├── .env.example            Template
        ├── .gitignore              Git ignore rules
        ├── README.md               Quick start
        └── start.sh                Symlink → scripts/
```

## 🎯 Dlaczego tak?

### ✅ Kod w rootcie
- **Zero zmian w imports** - wszystko działa bez modyfikacji
- **Proste uruchomienie** - `python -m uvicorn monolit:app`
- **Standardowe dla FastAPI**

### ✅ Docs oddzielone
- Nie miesza się z kodem
- Łatwo znaleźć dokumentację
- README w rootcie dla GitHub

### ✅ Knowledge wydzielone
- Fakty + generatory w jednym miejscu
- Jasne co jest wiedzą a co kodem
- Łatwo aktualizować

### ✅ Deployment gotowy
- Jeden folder z wszystkim
- Skopiuj i uruchom
- Instrukcje w środku

### ✅ Gitignore jasny
- `.env` - NIE w repo
- `data/`, `out/`, `logs/` - NIE w repo
- Fakty, kod, docs - TAK w repo

## 🚀 Jak używać

### Lokalnie
```bash
bash start.sh
# lub
bash scripts/start.sh
```

### Deploy
```bash
# Skopiuj cały folder deployment/
scp -r deployment/ user@server:/var/www/mordzix/
ssh user@server
cd /var/www/mordzix
bash SETUP_SERVER.sh
```

### Dodawanie wiedzy
```bash
cd knowledge/
# Edytuj generators/generate_5000_facts.py
python3 generators/generate_5000_facts.py
# Wgraj do bazy według instrukcji w README.md
```

## 📖 Dokumentacja

Wszystko w `docs/`:
- Start → `docs/README.md`
- Pełna → `docs/FINAL_COMPLETE.md`
- Online → `docs/REAL_VS_FAKE.md`
- Wiedza → `docs/JAK_DZIALA_WIEDZA.md`

---

**Gotowe! Struktura czytelna i logiczna! 🔥**
