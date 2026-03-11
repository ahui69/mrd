#!/bin/bash
# Test assistant endpoint

echo "🤖 TEST ASSISTANT ENDPOINT"
echo "=========================="

# Test 1: Proste pytanie bez research
echo ""
echo "TEST 1: Proste pytanie (bez research)"
curl -s -X POST http://127.0.0.1:8000/api/chat/assistant \
  -H "Authorization: Bearer changeme" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Cześć! Jak się masz?"}
    ],
    "use_research": false,
    "save_to_memory": true
  }' | python3 -m json.tool

echo ""
echo "=========================="
echo ""

# Test 2: Pytanie wymagające research
echo "TEST 2: Pytanie z research"
curl -s -X POST http://127.0.0.1:8000/api/chat/assistant \
  -H "Authorization: Bearer changeme" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Co nowego w AI w 2025?"}
    ],
    "use_research": true,
    "research_depth": "quick",
    "save_to_memory": true
  }' | python3 -m json.tool

echo ""
echo "=========================="
echo ""

# Test 3: Sprawdź historię
echo "TEST 3: Historia rozmów"
curl -s -X GET "http://127.0.0.1:8000/api/chat/history?limit=10" \
  -H "Authorization: Bearer changeme" | python3 -m json.tool

echo ""
echo "=========================="
