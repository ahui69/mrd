#!/bin/bash
set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          🚀 MORDZIX AI SYSTEM - STARTUP SCRIPT              ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# 1. ENVIRONMENT
# ============================================================================
echo "📋 [1/5] Wczytuję zmienne środowiskowe..."

if [ -f "/workspace/.env" ]; then
    export $(cat /workspace/.env | grep -v '^#' | xargs)
    echo "✅ .env załadowany"
else
    echo "⚠️  Brak .env - używam defaultów"
fi

# Set defaults jeśli nie ma w .env
export AUTH_TOKEN="${AUTH_TOKEN:-0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5}"
export LLM_API_KEY="${LLM_API_KEY:-w52XW0XN6zoV9hdY8OONhLu6tvnFaXbZ}"
export LLM_MODEL="${LLM_MODEL:-zai-org/GLM-4.6}"
export PORT="8080"
export HOST="${HOST:-0.0.0.0}"

echo "   AUTH_TOKEN: ${AUTH_TOKEN:0:20}..."
echo "   LLM_MODEL: $LLM_MODEL"
echo "   PORT: $PORT"
echo ""

# ============================================================================
# 2. DEPENDENCIES
# ============================================================================
echo "📦 [2/5] Instaluję zależności..."

if [ -f "/workspace/requirements.txt" ]; then
    pip install -q -r /workspace/requirements.txt
    echo "✅ Requirements zainstalowane"
else
    echo "⚠️  Brak requirements.txt - instaluję podstawowe..."
    pip install -q fastapi uvicorn httpx bs4 readability-lxml requests psutil
fi

# Dodatkowe jeśli brakują
pip install -q requests 2>/dev/null || true

echo ""

# ============================================================================
# 3. KILL OLD PROCESSES
# ============================================================================
echo "🔫 [3/5] Zabijam stare procesy..."

# Kill ALL related processes
pkill -9 -f uvicorn 2>/dev/null && echo "   ✅ Killed uvicorn" || true
pkill -9 -f monolit 2>/dev/null && echo "   ✅ Killed monolit" || true
pkill -9 python3 2>/dev/null && echo "   ✅ Killed python3" || true
sleep 2

echo "   ✅ Wszystko wyczyszczone"

echo "   ✅ Procesy wyczyszczone"
echo ""

# ============================================================================
# 4. DATABASE CHECK
# ============================================================================
echo "🗄️  [4/5] Sprawdzam bazę danych..."

DB_DIR="/workspace/mrd69"
DB_FILE="$DB_DIR/mem.db"

if [ ! -d "$DB_DIR" ]; then
    echo "   📁 Tworzę katalog bazy: $DB_DIR"
    mkdir -p "$DB_DIR"
fi

if [ -f "$DB_FILE" ]; then
    DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
    echo "   ✅ Baza istnieje: $DB_FILE ($DB_SIZE)"
else
    echo "   ℹ️  Baza zostanie utworzona przy pierwszym uruchomieniu"
fi

echo ""

# ============================================================================
# 5. START SERVER
# ============================================================================
echo "🚀 [5/5] Startuję serwer..."
echo ""

cd /workspace

# Cleanup old logs
rm -f /tmp/server.log /tmp/monolit.log 2>/dev/null

# Start with nohup
nohup python3 -m uvicorn monolit:app \
    --host $HOST \
    --port $PORT \
    --reload \
    --log-level info \
    > /tmp/monolit.log 2>&1 &

SERVER_PID=$!

echo "   Process ID: $SERVER_PID"
echo "   Czekam 5s na startup..."
sleep 5

# Health check
if curl -s --max-time 3 http://localhost:$PORT/api/health > /dev/null 2>&1; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║                  ✅ SERWER DZIAŁA!                          ║"
    echo "║                                                              ║"
    echo "║   🌐 URLs:                                                   ║"
    echo "║   • Chat:      http://localhost:$PORT/                      ║"
    echo "║   • Paint:     http://localhost:$PORT/paint                 ║"
    echo "║   • API Docs:  http://localhost:$PORT/docs                  ║"
    echo "║                                                              ║"
    echo "║   📊 Status:                                                 ║"
    echo "║   • PID:       $SERVER_PID                                  ║"
    echo "║   • Logs:      tail -f /tmp/monolit.log                     ║"
    echo "║   • Stop:      kill $SERVER_PID                             ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Show some logs
    echo "📋 Ostatnie logi:"
    echo "─────────────────────────────────────────────────────────────"
    tail -15 /tmp/monolit.log | grep -v "INFO:     127.0.0.1"
    echo ""
    
    # Quick stats
    echo "📊 Quick stats:"
    HEALTH=$(curl -s http://localhost:$PORT/api/health)
    echo "   Health: $HEALTH"
    
else
    echo ""
    echo "❌ SERWER NIE ODPOWIADA!"
    echo ""
    echo "Sprawdź logi:"
    echo "  tail -50 /tmp/monolit.log"
    echo ""
    echo "Debug:"
    echo "  ps aux | grep uvicorn"
    echo "  lsof -i :$PORT"
    exit 1
fi

echo "✅ Gotowe! Serwer działa w tle."
echo "   Aby zatrzymać: kill $SERVER_PID"
echo ""
