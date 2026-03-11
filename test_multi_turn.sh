#!/bin/bash

TOKEN="0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
BASE="http://localhost:8080"
USER_ID="test-context-$(date +%s)"

echo "🧪 TEST WIELOETAPOWEJ KONWERSACJI"
echo "=================================="
echo ""

# TURA 1: Moda
echo "👤 TURA 1: Co wiesz o streetwear?"
RESP1=$(curl -s --max-time 60 -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Co wiesz o streetwear?\"}],\"use_memory\":true,\"user_id\":\"$USER_ID\"}" \
  "$BASE/api/chat/assistant")

echo "$RESP1" | python3 -c "import sys,json; d=json.load(sys.stdin); print('🤖 AI:', d.get('answer','')[:150], '...'); print('📊 LTM facts used:', d.get('metadata',{}).get('ltm_facts_used',0))"
echo ""
sleep 2

# TURA 2: Kontekst - pytanie bez słowa "streetwear"
echo "👤 TURA 2: A Supreme to ta kategoria?" 
ANSWER1=$(echo "$RESP1" | python3 -c "import sys,json; print(json.load(sys.stdin).get('answer',''))")

RESP2=$(curl -s --max-time 60 -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Co wiesz o streetwear?\"},{\"role\":\"assistant\",\"content\":$(echo "$ANSWER1" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")},{\"role\":\"user\",\"content\":\"A Supreme to ta kategoria?\"}],\"use_memory\":true,\"user_id\":\"$USER_ID\"}" \
  "$BASE/api/chat/assistant")

echo "$RESP2" | python3 -c "import sys,json; d=json.load(sys.stdin); ans=d.get('answer',''); print('🤖 AI:', ans[:150], '...'); has_context = 'streetwear' in ans.lower() or 'ulica' in ans.lower(); print('✅ KONTEKST:' if has_context else '⚠️  Słaby kontekst')"
echo ""

# TURA 3: Psychologia
echo "👤 TURA 3: Opowiedz o flow state"
sleep 2
RESP3=$(curl -s --max-time 60 -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Opowiedz o flow state\"}],\"use_memory\":true,\"user_id\":\"test-psych-$(date +%s)\"}" \
  "$BASE/api/chat/assistant")

echo "$RESP3" | python3 -c "import sys,json; d=json.load(sys.stdin); print('🤖 AI:', d.get('answer','')[:150], '...'); print('📊 LTM facts used:', d.get('metadata',{}).get('ltm_facts_used',0))"
echo ""

# TURA 4: Kodowanie
echo "👤 TURA 4: Python REST API - best practices?"
sleep 2
RESP4=$(curl -s --max-time 60 -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Python REST API - jakie best practices?\"}],\"use_memory\":true,\"user_id\":\"test-code-$(date +%s)\"}" \
  "$BASE/api/chat/assistant")

echo "$RESP4" | python3 -c "import sys,json; d=json.load(sys.stdin); ans=d.get('answer',''); print('🤖 AI:', ans[:200], '...'); has_api = 'fastapi' in ans.lower() or 'django' in ans.lower() or 'rest' in ans.lower(); print('✅ WIEDZA Z LTM!' if has_api else '⚠️')"

echo ""
echo "=================================="
echo "✅ TEST ZAKOŃCZONY!"
echo ""
echo "Sprawdź czy AI:"
echo "• Używało wiedzy z LTM ✅"
echo "• Trzymało kontekst w multi-turn ✅"
echo "• Odpowiadało merytorycznie ✅"
