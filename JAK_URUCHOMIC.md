# 🚀 JAK URUCHOMIĆ MORDZIX AI - INSTRUKCJA KROK PO KROKU

## ⚡ OPCJA 1: AUTOMATYCZNIE (POLECAM!) 

### 1 KOMENDA I GOTOWE:

```bash
bash scripts/start.sh
```

**To zrobi WSZYSTKO:**
- ✅ Wczyta .env (albo użyje defaultów)
- ✅ Zainstaluje dependencies (pip install)
- ✅ Zabije stare procesy Pythona
- ✅ Utworzy foldery (data/, out/, logs/)
- ✅ Uruchomi serwer na http://localhost:8080
- ✅ Sprawdzi czy działa (health check)

**Czekasz 5-10 sekund i GOTOWE!** ✅

---

## 🔧 OPCJA 2: MANUALNIE (KROK PO KROKU)

Jeśli wolisz mieć kontrolę nad każdym krokiem:

### KROK 1: Wczytaj zmienne środowiskowe

```bash
# Jeśli masz .env
export $(cat .env | grep -v '^#' | xargs)

# Lub ustaw manualnie minimum:
export AUTH_TOKEN="0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
export LLM_API_KEY="w52XW0XN6zoV9hdY8OONhLu6tvnFaXbZ"
export LLM_MODEL="zai-org/GLM-4.6"
export PORT="8080"
export HOST="0.0.0.0"
```

**Co to robi?**
- Ustawia token autoryzacji
- Ustawia klucz do LLM (DeepInfra)
- Wybiera model AI
- Ustawia port (8080)

---

### KROK 2: Zainstaluj zależności

```bash
pip install -r requirements.txt
```

**Instaluje:**
- FastAPI (web framework)
- Uvicorn (ASGI server)
- httpx, requests (HTTP client)
- beautifulsoup4 (web scraping)
- psutil (process management)
- i inne...

**Czas: ~30 sekund**

---

### KROK 3: Zabij stare procesy (jeśli były)

```bash
pkill -9 -f uvicorn 2>/dev/null || true
pkill -9 -f monolit 2>/dev/null || true
pkill -9 python3 2>/dev/null || true
sleep 2
```

**Co to robi?**
- Zabija wszystkie stare procesy Pythona
- Zwalnia port 8080
- Czeka 2s żeby się wszystko posprzątało

**Możesz pominąć jeśli uruchamiasz pierwszy raz!**

---

### KROK 4: Utwórz foldery (jeśli nie ma)

```bash
mkdir -p data out/images out/writing logs
```

**Tworzy:**
- `data/` - baza SQLite (monolit.db)
- `out/images/` - wygenerowane obrazy
- `out/writing/` - wygenerowane teksty
- `logs/` - logi systemowe

**Foldery utworzą się automatycznie, ale możesz to zrobić wcześniej!**

---

### KROK 5: Uruchom serwer

```bash
# Przejdź do katalogu projektu
cd /workspace

# Uruchom w tle
nohup python3 -m uvicorn monolit:app \
    --host 0.0.0.0 \
    --port 8080 \
    --reload \
    --log-level info \
    > /tmp/monolit.log 2>&1 &
```

**Co się dzieje?**
- `uvicorn monolit:app` - uruchamia FastAPI app z monolit.py
- `--host 0.0.0.0` - słucha na wszystkich interfejsach
- `--port 8080` - port 8080
- `--reload` - auto-reload przy zmianach (dev mode)
- `nohup ... &` - działa w tle
- Logi idą do `/tmp/monolit.log`

**Zapisz PID:**
```bash
echo $! > /tmp/monolit.pid
```

---

### KROK 6: Sprawdź czy działa

```bash
# Czekaj 5s na startup
sleep 5

# Health check
curl http://localhost:8080/api/health
```

**Powinno zwrócić:**
```json
{"status":"ok","message":"Mordzix AI is running","timestamp":1234567890}
```

**Jeśli działa - GOTOWE!** ✅

---

## 📊 CO SIĘ DZIEJE POD MASKĄ?

### 1. **Startup serwera:**
```
🚀 Starting Mordzix AI...
✅ LTM: Wczytano 5200+ faktów do RAM
✅ Startup complete!
INFO: Uvicorn running on http://0.0.0.0:8080
```

### 2. **Wczytywanie faktów do RAM:**
- Otwiera `data/monolit.db`
- Czyta tabelę `ltm` (wszystkie fakty)
- Ładuje do `LTM_FACTS_CACHE` (lista w pamięci)
- Pre-tokenizuje każdy fakt
- **Trwa ~1-2 sekundy**

### 3. **Uruchamia endpointy:**
- `/` - frontend (chat)
- `/paint` - paint editor
- `/api/*` - wszystkie API
- `/docs` - Swagger UI

---

## 🌐 DOSTĘP DO SYSTEMU

Po uruchomieniu możesz otworzyć:

### 1. **Chat UI** (główny interfejs)
```
http://localhost:8080/
```

### 2. **Paint Editor**
```
http://localhost:8080/paint
```

### 3. **API Docs** (Swagger)
```
http://localhost:8080/docs
```

### 4. **Health Check**
```
http://localhost:8080/api/health
```

---

## 🛠️ PRZYDATNE KOMENDY

### Sprawdź czy serwer działa:
```bash
ps aux | grep uvicorn
```

### Zobacz logi:
```bash
tail -f /tmp/monolit.log
```

### Sprawdź port:
```bash
lsof -i :8080
# Lub
netstat -tuln | grep 8080
```

### Zatrzymaj serwer:
```bash
# Znajdź PID
ps aux | grep uvicorn

# Zabij process
kill <PID>

# Lub zabij wszystko:
pkill -9 -f uvicorn
```

### Restart serwera:
```bash
pkill -9 python3
bash scripts/start.sh
```

---

## 🧪 TESTOWANIE

### Test 1: Health check
```bash
curl http://localhost:8080/api/health
```

### Test 2: LTM search
```bash
curl -H "Authorization: Bearer 0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5" \
  "http://localhost:8080/api/ltm/search?q=chanel&limit=3"
```

### Test 3: Chat
```bash
curl -X POST http://localhost:8080/api/chat/assistant \
  -H "Authorization: Bearer 0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Cześć!"}],
    "user_id": "test123"
  }'
```

---

## ❗ TROUBLESHOOTING

### Problem: "Port 8080 already in use"
```bash
# Zabij proces na porcie 8080
lsof -ti:8080 | xargs kill -9

# Lub zabij wszystkie Pythony
pkill -9 python3
```

### Problem: "Module not found"
```bash
# Reinstaluj dependencies
pip install -r requirements.txt --upgrade
```

### Problem: "Cannot connect to database"
```bash
# Utwórz folder data
mkdir -p data

# Sprawdź czy monolit.db istnieje
ls -lh data/monolit.db
```

### Problem: "LTM cache empty"
```bash
# Sprawdź czy masz fakty
ls -lh knowledge/facts_complete.json

# Wgraj fakty do bazy
python3 << 'EOF'
import sqlite3, json, hashlib, time
with open('knowledge/facts_complete.json') as f:
    facts = json.load(f)
conn = sqlite3.connect('data/monolit.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS ltm 
               (id TEXT PRIMARY KEY, text TEXT, tags TEXT, 
                source TEXT, conf REAL, created_at INTEGER)''')
for fact in facts:
    fid = hashlib.sha256(fact['text'].encode()).hexdigest()[:16]
    tags = ','.join(fact['tags']) if isinstance(fact['tags'], list) else fact['tags']
    cur.execute('INSERT OR IGNORE INTO ltm VALUES (?,?,?,?,?,?)', 
                (fid, fact['text'], tags, fact.get('source',''), 
                 fact.get('conf',0.75), int(time.time())))
conn.commit()
print(f'✅ Wgrano {len(facts)} faktów')
EOF
```

### Problem: Serwer nie odpowiada
```bash
# Zobacz logi
tail -50 /tmp/monolit.log

# Sprawdź procesy
ps aux | grep python

# Restart
bash scripts/start.sh
```

---

## 📋 CHECKLIST URUCHOMIENIA

- [ ] Python 3.8+ zainstalowany (`python3 --version`)
- [ ] pip działa (`pip --version`)
- [ ] Jesteś w folderze projektu (`/workspace`)
- [ ] .env istnieje (albo użyjesz defaultów)
- [ ] Port 8080 wolny
- [ ] Uruchomiłeś: `bash scripts/start.sh`
- [ ] Sprawdziłeś: `curl http://localhost:8080/api/health`
- [ ] Otwierasz: http://localhost:8080

---

## 🎯 SZYBKI START (COPY-PASTE)

```bash
# Przejdź do projektu
cd /workspace

# Uruchom
bash scripts/start.sh

# Czekaj 5-10s i otwórz:
# http://localhost:8080
```

**TO WSZYSTKO!** ✅

---

## 📊 CO DZIAŁA PO STARCIE?

✅ **Frontend** - http://localhost:8080  
✅ **Paint Editor** - http://localhost:8080/paint  
✅ **Chat API** - /api/chat/assistant  
✅ **LTM (5200+ faktów)** - /api/ltm/search  
✅ **Research** - /api/research/sources  
✅ **Psyche** - /api/psyche/state  
✅ **Files** - /api/files/upload  
✅ **Travel** - /api/travel/*  
✅ **Streaming SSE** - włączony  
✅ **Cache** - w pamięci  
✅ **Rate limiting** - aktywny  

---

**SYSTEM GOTOWY! LECI! 🚀🔥**
