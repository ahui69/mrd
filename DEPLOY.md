# 🚀 JAK ZROBIĆ DEPLOYMENT NA SERWER

## 📦 QUICK DEPLOY (3 kroki)

### 1. Sklonuj repo na serwer

```bash
git clone https://github.com/ahui69/mrd
cd mrd
```

### 2. Setup środowisko

```bash
# Skopiuj template
cp .env.example .env

# Edytuj .env i dodaj swoje API keys
nano .env
# Lub vim .env
# Lub vi .env

# Ustaw przynajmniej:
AUTH_TOKEN=twoj_token_tutaj
LLM_API_KEY=twoj_deepinfra_key
```

### 3. Uruchom

```bash
bash scripts/start.sh
```

**Gotowe!** System działa na `http://TWOJ_IP:8080`

---

## 📁 CO TRZEBA NA SERWERZE?

### System requirements:
- Python 3.8+
- pip3
- SQLite3 (wbudowane w Python)
- 100MB RAM (dla aplikacji)
- 10MB RAM (dla 5000 faktów LTM)
- Port 8080 otwarty

### Python packages (auto-install):
```bash
pip3 install -r requirements.txt
```

Zawiera:
- fastapi
- uvicorn
- httpx
- beautifulsoup4
- i inne...

---

## 🗂️ STRUKTURA NA SERWERZE:

```bash
/var/www/mordzix/              # Lub inna lokalizacja
├── monolit.py                 # Backend core
├── *_endpoint.py              # Routers
├── middleware.py              # Cache/rate limiting
├── frontend.html              # UI
├── paint.html                 # Paint editor
├── .env                       # API keys (skopiuj z .env.example!)
├── requirements.txt           # Dependencies
├── scripts/start.sh           # Uruchamianie
├── knowledge/                 # Fakty
│   └── facts_complete.json    # 5200+ faktów
└── data/                      # Utworzy się auto
    └── monolit.db             # SQLite (auto)
```

---

## 🔧 SETUP KROK PO KROKU:

### Na SWOIM komputerze:
```bash
git clone https://github.com/ahui69/mrd
cd mrd
```

### Na SERWERZE (przez SSH):
```bash
ssh user@twoj-serwer.com

# Zainstaluj Python jeśli nie ma
sudo apt update
sudo apt install python3 python3-pip -y

# Sklonuj repo
git clone https://github.com/ahui69/mrd
cd mrd

# Setup .env
cp .env.example .env
nano .env
# Dodaj API keys: AUTH_TOKEN, LLM_API_KEY, etc.

# Instaluj dependencies
pip3 install -r requirements.txt

# Utwórz katalogi
mkdir -p data out/images out/writing logs

# Wgraj fakty do bazy (opcjonalnie)
python3 << 'EOF'
import sqlite3, json, hashlib, time
with open('knowledge/facts_complete.json') as f:
    facts = json.load(f)
conn = sqlite3.connect('data/monolit.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS ltm (id TEXT PRIMARY KEY, text TEXT, tags TEXT, source TEXT, conf REAL, created_at INTEGER)')
for fact in facts:
    fid = hashlib.sha256(fact['text'].encode()).hexdigest()[:16]
    tags = ','.join(fact['tags']) if isinstance(fact['tags'], list) else fact['tags']
    cur.execute('INSERT OR IGNORE INTO ltm VALUES (?,?,?,?,?,?)', 
                (fid, fact['text'], tags, fact.get('source',''), fact.get('conf',0.75), int(time.time())))
conn.commit()
print(f'✅ Wgrano {len(facts)} faktów')
EOF

# Uruchom
bash scripts/start.sh

# Sprawdź czy działa
curl http://localhost:8080/api/health
```

---

## 🌐 PUBLICZNY DOSTĘP:

### Nginx jako reverse proxy:

```nginx
server {
    listen 80;
    server_name twoja-domena.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Systemd service (auto-restart):

```bash
sudo nano /etc/systemd/system/mordzix.service
```

```ini
[Unit]
Description=Mordzix AI
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/mordzix
ExecStart=/usr/bin/python3 -m uvicorn monolit:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable mordzix
sudo systemctl start mordzix
sudo systemctl status mordzix
```

---

## 🔒 SECURITY:

1. **Zmień AUTH_TOKEN** w .env na długi random string
2. **Firewall** - otwórz tylko port 80/443 (Nginx)
3. **HTTPS** - użyj Let's Encrypt certbot
4. **Rate limiting** - już wbudowany w system!

---

## 🧪 TESTOWANIE:

```bash
# Health check
curl http://localhost:8080/api/health

# LTM search
curl -H "Authorization: Bearer TWOJ_TOKEN" \
  "http://localhost:8080/api/ltm/search?q=chanel&limit=3"

# Chat test
curl -X POST http://localhost:8080/api/chat/assistant \
  -H "Authorization: Bearer TWOJ_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hi"}],"user_id":"test"}'
```

---

## ⚡ PERFORMANCE TIPS:

1. **RAM cache** - już włączony! Fakty w RAM przy starcie
2. **Gunicorn workers** - dla większego ruchu:
   ```bash
   pip3 install gunicorn
   gunicorn monolit:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
   ```
3. **Redis** - dla distributed cache (opcjonalnie)

---

## 🆘 TROUBLESHOOTING:

**Port zajęty?**
```bash
pkill -9 python3
bash scripts/start.sh
```

**Brak faktów?**
```bash
# Wgraj z knowledge/facts_complete.json
# (patrz kod powyżej)
```

**Błędy imports?**
```bash
pip3 install -r requirements.txt --upgrade
```

---

## 📊 CHECKLIST DEPLOYMENT:

- [ ] Python 3.8+ zainstalowany
- [ ] Repo sklonowany
- [ ] .env utworzony i wypełniony (AUTH_TOKEN, LLM_API_KEY minimum)
- [ ] Dependencies zainstalowane (pip3 install -r requirements.txt)
- [ ] Katalogi utworzone (data/, out/, logs/)
- [ ] Fakty wgrane do bazy (opcjonalnie)
- [ ] Port 8080 otwarty
- [ ] Serwer uruchomiony (bash scripts/start.sh)
- [ ] Health check OK (curl /api/health)

---

**GOTOWE! Deploy w 3 krokach! 🔥**
