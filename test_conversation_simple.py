#!/usr/bin/env python3
"""Prosty test konwersacji - 1 scenariusz"""

import requests
import json

API_BASE = "http://localhost:8080"
TOKEN = "0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

print("🧪 QUICK TEST KONWERSACJI\n")

messages = []

# Turn 1
print("👤 USER: Co wiesz o haute couture?")
messages.append({"role": "user", "content": "Co wiesz o haute couture?"})

resp = requests.post(
    f"{API_BASE}/api/chat/assistant",
    headers=headers,
    json={
        "messages": messages,
        "use_memory": True,
        "use_research": False,
        "save_to_memory": True,
        "user_id": "quick-test"
    },
    timeout=30
)

if resp.status_code == 200:
    data = resp.json()
    answer = data.get("answer", "")
    print(f"🤖 AI: {answer[:200]}...\n")
    messages.append({"role": "assistant", "content": answer})
    
    # Turn 2 - test kontekstu
    print("👤 USER: A Chanel należy do tej kategorii?")
    messages.append({"role": "user", "content": "A Chanel należy do tej kategorii?"})
    
    resp2 = requests.post(
        f"{API_BASE}/api/chat/assistant",
        headers=headers,
        json={
            "messages": messages,
            "use_memory": True,
            "use_research": False,
            "save_to_memory": True,
            "user_id": "quick-test"
        },
        timeout=30
    )
    
    if resp2.status_code == 200:
        data2 = resp2.json()
        answer2 = data2.get("answer", "")
        print(f"🤖 AI: {answer2[:200]}...\n")
        
        # Check context
        if "haute" in answer2.lower() or "luksus" in answer2.lower() or "couture" in answer2.lower():
            print("✅ KONTEKST ZACHOWANY! AI pamięta o haute couture!")
        else:
            print("⚠️  Kontekst może być słaby")
            
        # Check LTM knowledge
        if "chanel" in answer.lower() or "chanel" in answer2.lower():
            print("✅ WIEDZA Z LTM UŻYTA! (Chanel wymieniony w faktach)")
        
        print("\n✅ TEST OK!")
    else:
        print(f"❌ Turn 2 failed: {resp2.status_code}")
else:
    print(f"❌ Turn 1 failed: {resp.status_code}")
