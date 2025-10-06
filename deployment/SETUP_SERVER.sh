#!/bin/bash
# SETUP NA SERWERZE PRODUKCYJNYM

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 SETUP MORDZIX AI - PRODUCTION SERVER                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Wybierz katalog (domyślnie /var/www/mordzix)
APP_DIR="${1:-/var/www/mordzix}"

echo "📁 Katalog aplikacji: $APP_DIR"
echo ""

# 1. Utwórz strukturę katalogów
echo "1️⃣  Tworzę katalogi..."
mkdir -p "$APP_DIR"/{data,out/images,out/writing,out/dev,queue,prompts,data/uploads,data/mem}
echo "   ✅ Utworzono strukturę katalogów"

# 2. Skopiuj pliki (zakładam że są w bieżącym katalogu)
echo ""
echo "2️⃣  Kopiuję pliki aplikacji..."
cp *.py "$APP_DIR/" 2>/dev/null
cp *.html "$APP_DIR/" 2>/dev/null
cp .env.production "$APP_DIR/.env" 2>/dev/null || cp .env "$APP_DIR/.env"
cp start.sh "$APP_DIR/"
cp requirements.txt "$APP_DIR/"
echo "   ✅ Skopiowano pliki"

# 3. Zaktualizuj ścieżki w .env
echo ""
echo "3️⃣  Aktualizuję ścieżki w .env..."
cd "$APP_DIR"
sed -i "s|/var/www/mordzix|$APP_DIR|g" .env
sed -i "s|C:/Users/48501/Desktop/mrd69|$APP_DIR|g" .env
echo "   ✅ Zaktualizowano ścieżki"

# 4. Instaluj dependencies
echo ""
echo "4️⃣  Instaluję zależności Python..."
pip3 install -r requirements.txt
echo "   ✅ Zainstalowano dependencies"

# 5. Wgraj fakty (jeśli są)
if [ -f "facts_complete.json" ]; then
    echo ""
    echo "5️⃣  Wgrywam 5200+ faktów do bazy..."
    python3 << 'PYEOF'
import sqlite3, json, hashlib, time
try:
    with open('facts_complete.json') as f:
        facts = json.load(f)
    conn = sqlite3.connect('data/monolit.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS ltm 
                   (id TEXT PRIMARY KEY, text TEXT, tags TEXT, 
                    source TEXT, conf REAL, created_at INTEGER)''')
    for fact in facts:
        fact_id = hashlib.sha256(fact['text'].encode()).hexdigest()[:16]
        tags_str = ','.join(fact['tags']) if isinstance(fact['tags'], list) else fact['tags']
        cur.execute('INSERT OR IGNORE INTO ltm VALUES (?,?,?,?,?,?)', 
                   (fact_id, fact['text'], tags_str, 
                    fact.get('source','batch'), fact.get('conf',0.75), 
                    int(time.time())))
    conn.commit()
    print(f'   ✅ Wgrano {len(facts)} faktów do bazy')
except Exception as e:
    print(f'   ⚠️  Błąd wgrywania faktów: {e}')
PYEOF
else
    echo "   ⚠️  Brak facts_complete.json - pominięto"
fi

# 6. Uprawnienia
echo ""
echo "6️⃣  Ustawiam uprawnienia..."
chmod +x start.sh
chmod 755 "$APP_DIR"
chmod -R 755 "$APP_DIR/data"
chmod -R 755 "$APP_DIR/out"
chmod -R 755 "$APP_DIR/queue"
echo "   ✅ Uprawnienia ustawione"

# 7. Informacje
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SETUP ZAKOŃCZONY!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 URUCHOMIENIE:"
echo "   cd $APP_DIR"
echo "   bash start.sh"
echo ""
echo "🌐 ADRES:"
echo "   http://$(hostname -I | awk '{print $1}'):8080/"
echo ""
echo "📊 SPRAWDŹ STATUS:"
echo "   curl http://localhost:8080/api/health"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

