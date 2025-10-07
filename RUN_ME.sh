#!/bin/bash

echo "🚀 URUCHAMIANIE AI ASSISTANT MONOLIT"
echo "===================================="
echo ""

cd /workspace

echo "1️⃣  Sprawdzam zależności..."
pip install -q -r requirements.txt 2>&1 | tail -3

echo "2️⃣  Uruchamiam serwer..."
python3 monolit.py -p 8000 2>&1 | grep -E "Started|Application|OK|WARN" &

sleep 8

echo "3️⃣  Testowanie..."
HEALTH=$(curl -s http://localhost:8000/api/health)
if echo "$HEALTH" | grep -q '"ok":true'; then
    echo "   ✅ Backend działa!"
else
    echo "   ❌ Backend nie odpowiada"
    exit 1
fi

FRONTEND=$(curl -s http://localhost:8000/ | head -1)
if echo "$FRONTEND" | grep -q "<!DOCTYPE"; then
    echo "   ✅ Frontend działa!"
else
    echo "   ❌ Frontend nie ładuje się"
fi

echo ""
echo "🎉 GOTOWE!"
echo ""
echo "📱 Otwórz w przeglądarce:"
echo "   http://localhost:8000/"
echo ""
echo "📚 Dokumentacja API:"
echo "   http://localhost:8000/docs"
echo ""
echo "🧠 Stan psychiki AI:"
echo "   curl http://localhost:8000/api/psyche/state \\"
echo "     -H 'Authorization: Bearer 0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5'"
echo ""
echo "Press Ctrl+C to stop server"
wait
