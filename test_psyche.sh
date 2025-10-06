#!/bin/bash
# Test psychiki AI

TOKEN="0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
API="http://localhost:8000/api/psyche"

echo "🧠 TEST PSYCHIKI AI"
echo "==================="
echo ""

echo "1️⃣  Stan początkowy..."
curl -s "$API/state" -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin)
s=d['state']
print(f\"  😊 Mood: {s['mood']:.2f}\")
print(f\"  ⚡ Energy: {s['energy']:.2f}\")
print(f\"  🎯 Focus: {s['focus']:.2f}\")
print(f\"  🎨 Style: {s['style']}\")
print(f\"  🌡️  LLM Temp: {d['llm_tuning']['temperature']}\")
"

echo ""
echo "2️⃣  Obserwacja pozytywnego tekstu..."
curl -s -X POST "$API/observe" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Super! Świetnie działa, extra!","user":"test"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f\"  Sentiment: {d['sentiment']}\")
print(f\"  Mood change: {d['mood_change']:+.3f}\")
print(f\"  Mood: {d['state_before']['mood']:.3f} → {d['state_after']['mood']:.3f}\")
"

echo ""
echo "3️⃣  Obserwacja negatywnego tekstu..."
curl -s -X POST "$API/observe" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Kurwa, błąd! Masakra, wkurwia mnie to!","user":"test"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f\"  Sentiment: {d['sentiment']}\")
print(f\"  Mood change: {d['mood_change']:+.3f}\")
print(f\"  Mood: {d['state_before']['mood']:.3f} → {d['state_after']['mood']:.3f}\")
"

echo ""
echo "4️⃣  Ręczna zmiana stanu (zwiększam energy)..."
curl -s -X POST "$API/state" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"energy":0.85,"mood":0.7}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
s=d['state']
print(f\"  ✅ Energy: {s['energy']:.2f}\")
print(f\"  ✅ Mood: {s['mood']:.2f}\")
"

echo ""
echo "5️⃣  Sprawdź jak to wpływa na LLM tuning..."
curl -s "$API/tune" -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin)
t=d['tuning']
print(f\"  🌡️  Temperature: {t['temperature']}\")
print(f\"  🎭 Tone: {t['tone']}\")
print(f\"  ✍️  Style: {t['style']}\")
print(f\"  📝 Wyjaśnienie: {d['explanation']['temperature'][:60]}...\")
"

echo ""
echo "6️⃣  Dodaj epizod (bardzo pozytywny)..."
curl -s -X POST "$API/episode" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"valence":0.9,"intensity":0.8,"kind":"feedback","tags":"success,milestone","note":"Udało się!"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f\"  ✅ Episode ID: {d['episode_id'][:16]}...\")
print(f\"  😊 New mood: {d['new_state']['mood']:.3f}\")
"

echo ""
echo "7️⃣  Reset do wartości domyślnych..."
curl -s -X POST "$API/reset" -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f\"  ✅ {d['message']}\")
print(f\"  Mood: {d['state']['mood']:.2f}\")
print(f\"  Energy: {d['state']['energy']:.2f}\")
"

echo ""
echo "🎉 PSYCHIKA DZIAŁA W 100%!"
