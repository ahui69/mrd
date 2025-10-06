#!/bin/bash
# LISTA PLIKÓW DO ŚCIĄGNIĘCIA NA SERWER

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  📦 TWORZĘ PACZKĘ DO DEPLOYMENT                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Utwórz katalog deployment
mkdir -p /workspace/deployment
cd /workspace

echo "📁 Kopiuję pliki..."

# CORE
cp monolit.py deployment/
cp requirements.txt deployment/ 2>/dev/null || echo "requirements.txt" > deployment/requirements.txt
cp .env deployment/
cp start.sh deployment/

# ROUTERS
cp routers_full.py deployment/
cp assistant_endpoint.py deployment/
cp psyche_endpoint.py deployment/
cp files_endpoint.py deployment/
cp travel_endpoint.py deployment/
cp admin_endpoint.py deployment/

# MODULES
cp middleware.py deployment/
cp prompt.py deployment/
cp autonauka_pro.py deployment/
cp writer_pro.py deployment/

# FRONTEND
cp frontend.html deployment/
cp paint.html deployment/

# DATA
cp facts_complete.json deployment/ 2>/dev/null

# DOCS
cp README.md deployment/ 2>/dev/null
cp FINAL_COMPLETE.md deployment/ 2>/dev/null

echo ""
echo "✅ Pliki skopiowane do: /workspace/deployment/"
echo ""
echo "📊 LISTA:"
ls -lh deployment/ | tail -n +2 | awk '{printf "   %-30s %s\n", $9, $5}'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 NA SERWERZE ZRÓB:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Zainstaluj dependencies:"
echo "   pip3 install -r requirements.txt"
echo ""
echo "2. Utwórz katalog data:"
echo "   mkdir -p data"
echo ""
echo "3. (Opcjonalnie) Wgraj fakty:"
echo "   python3 << 'EOF'"
echo "   import sqlite3, json, hashlib, time"
echo "   with open('facts_complete.json') as f: facts = json.load(f)"
echo "   conn = sqlite3.connect('data/monolit.db')"
echo "   cur = conn.cursor()"
echo "   cur.execute('CREATE TABLE IF NOT EXISTS ltm (id TEXT PRIMARY KEY, text TEXT, tags TEXT, source TEXT, conf REAL, created_at INTEGER)')"
echo "   for fact in facts:"
echo "       fact_id = hashlib.sha256(fact['text'].encode()).hexdigest()[:16]"
echo "       tags_str = ','.join(fact['tags']) if isinstance(fact['tags'], list) else fact['tags']"
echo "       cur.execute('INSERT OR IGNORE INTO ltm VALUES (?,?,?,?,?,?)', (fact_id, fact['text'], tags_str, fact.get('source','batch'), fact.get('conf',0.75), int(time.time())))"
echo "   conn.commit()"
echo "   print('✅ Wgrano', len(facts), 'faktów')"
echo "   EOF"
echo ""
echo "4. Uruchom:"
echo "   bash start.sh"
echo ""
echo "5. Otwórz:"
echo "   http://TWOJ_SERWER_IP:8080/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
