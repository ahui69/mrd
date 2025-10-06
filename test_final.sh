#!/bin/bash
echo "🧪 FINALNE TESTY CAŁOŚCI"
echo "========================"
echo ""

TOKEN="0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
BASE="http://localhost:8080"

echo "1️⃣ Health check..."
curl -s "$BASE/api/health" | python3 -m json.tool || echo "❌ Health FAIL"
echo ""

echo "2️⃣ Frontend..."
curl -s "$BASE/" | head -5 | grep -q "html" && echo "✅ Frontend OK" || echo "❌ Frontend FAIL"
echo ""

echo "3️⃣ Paint Editor..."
curl -s "$BASE/paint" | head -5 | grep -q "Paint Pro" && echo "✅ Paint OK" || echo "❌ Paint FAIL"
echo ""

echo "4️⃣ Cache stats..."
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/api/admin/cache/stats" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Cache OK: {d['caches']['llm']['size']} items\")" || echo "❌ Cache FAIL"
echo ""

echo "5️⃣ LTM - dodaj fakt..."
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"text":"Test finalny","tags":["test-final"],"source":"test"}' \
  "$BASE/api/ltm/add" | grep -q "ok" && echo "✅ LTM Add OK" || echo "❌ LTM Add FAIL"
echo ""

echo "6️⃣ LTM - wyszukiwanie (moda)..."
RESULT=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/api/ltm/search?q=moda&limit=1")
echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Znaleziono: {len(d.get('items',[]))} wyników\")" 2>/dev/null || echo "Response: $RESULT"
echo ""

echo "7️⃣ LTM - wyszukiwanie (python)..."
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/api/ltm/search?q=python&limit=1" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Python facts: {len(d.get('items',[]))}\")" 2>/dev/null || echo "❌ Search FAIL"
echo ""

echo "8️⃣ Psyche state..."
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/api/psyche/state" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Psyche: mood={d.get('mood',{}).get('valence','?')}\")" 2>/dev/null || echo "❌ Psyche FAIL"
echo ""

echo "✅ TESTY ZAKOŃCZONE!"
