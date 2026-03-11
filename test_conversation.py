#!/usr/bin/env python3
"""Test wieloetapowej konwersacji z kontekstem i wiedzą LTM"""

import requests
import json
import time

API_BASE = "http://localhost:8080"
TOKEN = "0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def chat(messages, user_id="test-conversation"):
    """Wyślij wiadomość do assistant endpoint"""
    resp = requests.post(
        f"{API_BASE}/api/chat/assistant",
        headers=headers,
        json={
            "messages": messages,
            "use_memory": True,
            "use_research": False,
            "save_to_memory": True,
            "user_id": user_id
        }
    )
    if resp.status_code == 200:
        data = resp.json()
        return data.get("answer", "")
    else:
        return f"ERROR {resp.status_code}: {resp.text}"

def print_exchange(turn, user_msg, ai_msg):
    """Wydrukuj wymianę"""
    print(f"\n{'='*80}")
    print(f"🔄 TURA {turn}")
    print(f"{'='*80}")
    print(f"👤 USER: {user_msg}")
    print(f"🤖 AI:   {ai_msg[:300]}{'...' if len(ai_msg) > 300 else ''}")
    print(f"📊 Długość odpowiedzi: {len(ai_msg)} znaków")

# ============================================================================
print("🧪 TEST KONWERSACJI Z KONTEKSTEM I WIEDZĄ LTM")
print("="*80)

# Conversation 1: MODA - wieloetapowa z kontekstem
print("\n\n📋 SCENARIUSZ 1: MODA (kontekst przez 4 tury)")
print("-"*80)

messages = []
user_id = "test-fashion-" + str(int(time.time()))

# Turn 1: Zapytanie o haute couture
msg = "Co wiesz o haute couture?"
messages.append({"role": "user", "content": msg})
response = chat(messages, user_id)
messages.append({"role": "assistant", "content": response})
print_exchange(1, msg, response)
time.sleep(1)

# Turn 2: Kontynuacja - pytanie o konkretny dom mody (test kontekstu)
msg = "A Chanel? Jest w tej kategorii?"
messages.append({"role": "user", "content": msg})
response = chat(messages, user_id)
messages.append({"role": "assistant", "content": response})
print_exchange(2, msg, response)
time.sleep(1)

# Turn 3: Kontrast - streetwear
msg = "A co z streetwear? To też luksus?"
messages.append({"role": "user", "content": msg})
response = chat(messages, user_id)
messages.append({"role": "assistant", "content": response})
print_exchange(3, msg, response)
time.sleep(1)

# Turn 4: Kreatywne połączenie - test czy pamięta oba
msg = "Która opcja jest droższa i dlaczego?"
messages.append({"role": "user", "content": msg})
response = chat(messages, user_id)
messages.append({"role": "assistant", "content": response})
print_exchange(4, msg, response)

# ============================================================================
# Conversation 2: PODRÓŻE + PSYCHOLOGIA - kreatywne połączenie
print("\n\n📋 SCENARIUSZ 2: PODRÓŻE + PSYCHOLOGIA (kreatywne połączenie)")
print("-"*80)

messages2 = []
user_id2 = "test-travel-psych-" + str(int(time.time()))

# Turn 1: Tokio
msg = "Planuję wyjazd do Tokio. Co powinienem zobaczyć?"
messages2.append({"role": "user", "content": msg})
response = chat(messages2, user_id2)
messages2.append({"role": "assistant", "content": response})
print_exchange(1, msg, response)
time.sleep(1)

# Turn 2: Pytanie o konkret (test kontekstu)
msg = "Co to jest to Harajuku?"
messages2.append({"role": "user", "content": msg})
response = chat(messages2, user_id2)
messages2.append({"role": "assistant", "content": response})
print_exchange(2, msg, response)
time.sleep(1)

# Turn 3: Psychologia - flow state w podróży
msg = "Czy podczas zwiedzania mogę doświadczyć flow state?"
messages2.append({"role": "user", "content": msg})
response = chat(messages2, user_id2)
messages2.append({"role": "assistant", "content": response})
print_exchange(3, msg, response)
time.sleep(1)

# Turn 4: Kreatywne połączenie wiedzy
msg = "Jakie miejsce w Tokio byłoby najlepsze do tego?"
messages2.append({"role": "user", "content": msg})
response = chat(messages2, user_id2)
messages2.append({"role": "assistant", "content": response})
print_exchange(4, msg, response)

# ============================================================================
# Conversation 3: KODOWANIE - kontekst techniczny
print("\n\n📋 SCENARIUSZ 3: KODOWANIE (wieloetapowy tech talk)")
print("-"*80)

messages3 = []
user_id3 = "test-coding-" + str(int(time.time()))

# Turn 1: Python frameworks
msg = "Chcę zbudować REST API. Jakie frameworki Pythona polecasz?"
messages3.append({"role": "user", "content": msg})
response = chat(messages3, user_id3)
messages3.append({"role": "assistant", "content": response})
print_exchange(1, msg, response)
time.sleep(1)

# Turn 2: Docker (test czy pamięta że mówimy o API)
msg = "Jak to potem zdockeryzować?"
messages3.append({"role": "user", "content": msg})
response = chat(messages3, user_id3)
messages3.append({"role": "assistant", "content": response})
print_exchange(2, msg, response)
time.sleep(1)

# Turn 3: Git workflow
msg = "A jaki git workflow byś użył do tego projektu?"
messages3.append({"role": "user", "content": msg})
response = chat(messages3, user_id3)
messages3.append({"role": "assistant", "content": response})
print_exchange(3, msg, response)
time.sleep(1)

# Turn 4: Clean code
msg = "Daj mi 3 najważniejsze zasady clean code dla tego"
messages3.append({"role": "user", "content": msg})
response = chat(messages3, user_id3)
messages3.append({"role": "assistant", "content": response})
print_exchange(4, msg, response)

# ============================================================================
# Conversation 4: MIX WSZYSTKIEGO - super kreatywny test
print("\n\n📋 SCENARIUSZ 4: KREATYWNY MIX (wszystkie dziedziny)")
print("-"*80)

messages4 = []
user_id4 = "test-creative-" + str(int(time.time()))

# Turn 1: Start - geografia
msg = "Jaka jest najwyższa góra świata?"
messages4.append({"role": "user", "content": msg})
response = chat(messages4, user_id4)
messages4.append({"role": "assistant", "content": response})
print_exchange(1, msg, response)
time.sleep(1)

# Turn 2: Psychologia + geografia
msg = "Czy wspinaczka na nią to przykład flow state?"
messages4.append({"role": "user", "content": msg})
response = chat(messages4, user_id4)
messages4.append({"role": "assistant", "content": response})
print_exchange(2, msg, response)
time.sleep(1)

# Turn 3: + podróże
msg = "A gdybym chciał tam pojechać, co powinienem wiedzieć o Nepalu?"
messages4.append({"role": "user", "content": msg})
response = chat(messages4, user_id4)
messages4.append({"role": "assistant", "content": response})
print_exchange(3, msg, response)
time.sleep(1)

# Turn 4: + kodowanie (absurdalne ale test kreatywności)
msg = "Gdybym robił apkę do planowania takiej wyprawy, jakiej stack byś użył?"
messages4.append({"role": "user", "content": msg})
response = chat(messages4, user_id4)
messages4.append({"role": "assistant", "content": response})
print_exchange(4, msg, response)
time.sleep(1)

# Turn 5: Callback do początku (test długiego kontekstu)
msg = "A wracając do tej góry - ile ma metrów?"
messages4.append({"role": "user", "content": msg})
response = chat(messages4, user_id4)
messages4.append({"role": "assistant", "content": response})
print_exchange(5, msg, response)

# ============================================================================
print("\n\n" + "="*80)
print("✅ TEST ZAKOŃCZONY!")
print("="*80)
print("""
📊 PRZETESTOWANO:
✅ 4 scenariusze konwersacji
✅ 17 tur w sumie
✅ Kontekst przez wiele wymian
✅ Wiedza z LTM (moda, podróże, psychologia, kodowanie, geografia)
✅ Kreatywne połączenia różnych dziedzin
✅ Callback do wcześniejszych części rozmowy

🎯 Sprawdź czy AI:
- Pamiętało kontekst w każdej turze
- Używało wiedzy z LTM
- Łączyło kreatywnie różne tematy
- Odpowiadało spójnie przez długą rozmowę
""")
