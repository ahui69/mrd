# 🧠 JAK SYSTEM WCZYTUJE I UŻYWA WIEDZY

## 📚 GDZIE JEST WIEDZA?

### 1. BAZA SQLite
```
/workspace/data/monolit.db
Tabela: ltm (Long-Term Memory)

Struktura:
- id          (hash tekstu)
- text        (treść faktu)
- tags        (kategorie, np. "moda,vinted,pricing")
- source      (źródło, np. "Fashion Encyclopedia")
- conf        (pewność, 0.0-1.0)
- created_at  (timestamp)
```

**Aktualna zawartość:**
- ~2932 faktów w bazie (po ostatnim wgraniu)
- 8 kategorii: moda, Vinted, social, aukcje, psychologia, pisanie, kod, geografia

---

## 🔄 JAK SYSTEM WCZYTUJE WIEDZĘ?

### SPOSÓB 1: Automatycznie przy starcie serwera ❌

**NIE - fakty NIE są ładowane do pamięci przy starcie!**

Baza SQLite jest odczytywana **na żądanie** gdy:
- Użytkownik zadaje pytanie
- System wykonuje `ltm_search()`

### SPOSÓB 2: Podczas chat'a (on-demand) ✅

**TAK - to główny sposób!**

```python
# W assistant_endpoint.py (uproszczony flow):

1. User: "Co wiesz o Chanel?"

2. System wywołuje: ltm_search(query="Chanel", limit=5)
   
3. SQLite SELECT:
   SELECT * FROM ltm 
   WHERE tags LIKE '%chanel%' OR text LIKE '%Chanel%'
   ORDER BY relevance
   LIMIT 5

4. Zwraca np.:
   - "Coco Chanel revolutionized women's fashion..."
   - "Chanel No. 5 perfume remains timeless..."
   - "Chanel's little black dress..."

5. Te fakty są dodawane do promptu LLM jako KONTEKST

6. LLM generuje odpowiedź UŻYWAJĄC tych faktów
```

---

## 🔍 DOKŁADNY FLOW (krok po kroku):

### A. Użytkownik wysyła wiadomość

```javascript
// frontend.html
sendMessage() {
  fetch('/api/chat/assistant', {
    body: JSON.stringify({
      messages: [...],
      use_memory: true  // ← WŁĄCZ PAMIĘĆ!
    })
  })
}
```

### B. Backend (assistant_endpoint.py)

```python
@router.post("/chat/assistant")
async def chat_assistant(req: ChatRequest):
    
    # 1. Wyciągnij ostatnią wiadomość użytkownika
    user_msg = req.messages[-1].content
    
    # 2. SZUKAJ W LTM (jeśli use_memory=true)
    if req.use_memory:
        ltm_facts = M.ltm_search_hybrid(
            query=user_msg,
            topk=5  # Weź top 5 faktów
        )
        # ltm_facts = [
        #   {"text": "Chanel...", "score": 0.85},
        #   {"text": "Haute couture...", "score": 0.72},
        #   ...
        # ]
    
    # 3. Dodaj fakty do SYSTEM PROMPT
    system_prompt = f"""
    Jesteś Mordzix. Używaj faktów z bazy:
    
    FAKTY:
    {ltm_facts[0]['text']}
    {ltm_facts[1]['text']}
    ...
    
    USER: {user_msg}
    """
    
    # 4. Wyślij do LLM
    response = llm_call(system_prompt)
    
    # 5. Zwróć odpowiedź
    return {"answer": response}
```

### C. SQLite (monolit.py)

```python
def ltm_search_hybrid(query, topk=5):
    """Hybrid search: BM25 + TF-IDF"""
    
    # 1. Tokenizuj query
    tokens = query.lower().split()
    
    # 2. Szukaj w bazie
    conn = sqlite3.connect('data/monolit.db')
    
    # Metoda 1: Szukaj po tagach
    for token in tokens:
        results = conn.execute("""
            SELECT * FROM ltm 
            WHERE tags LIKE ?
        """, (f'%{token}%',))
    
    # Metoda 2: Szukaj po treści
    results += conn.execute("""
        SELECT * FROM ltm 
        WHERE text LIKE ?
    """, (f'%{query}%',))
    
    # 3. Scoruj wyniki (TF-IDF)
    scored = []
    for row in results:
        score = calculate_tfidf(row['text'], query)
        scored.append({
            'text': row['text'],
            'score': score,
            'tags': row['tags'],
            'source': row['source']
        })
    
    # 4. Sortuj i zwróć top K
    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:topk]
```

---

## 📥 JAK DODAĆ NOWE FAKTY?

### SPOSÓB 1: API Endpoint

```bash
curl -X POST http://localhost:8080/api/ltm/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Vue 3 uses Composition API for better TypeScript support",
    "tags": ["kod", "vue", "javascript"],
    "source": "Vue 3 Docs",
    "conf": 0.9
  }'
```

### SPOSÓB 2: Auto-uczenie (frontend)

```
1. Sidebar → "🎓 Auto-uczenie"
2. Wpisz hasło: "Vue 3"
3. Kliknij "🔍 Naucz się"

→ System:
  - Szuka w DuckDuckGo
  - Pobiera top 5 wyników
  - Zapisuje top 3 do LTM
```

### SPOSÓB 3: Python script (bulk)

```python
import sqlite3, hashlib, time

facts = [
    {"text": "...", "tags": ["moda"], "source": "..."},
    # ... więcej faktów
]

conn = sqlite3.connect('data/monolit.db')
for fact in facts:
    fact_id = hashlib.sha256(fact['text'].encode()).hexdigest()[:16]
    tags_str = ','.join(fact['tags'])
    
    conn.execute("""
        INSERT OR IGNORE INTO ltm 
        (id, text, tags, source, conf, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (fact_id, fact['text'], tags_str, 
          fact['source'], 0.8, int(time.time())))

conn.commit()
```

### SPOSÓB 4: Z pliku JSON

```bash
# Masz facts_complete.json (5200+ faktów)
python3 << 'EOF'
import sqlite3, json, hashlib, time

with open('facts_complete.json') as f:
    facts = json.load(f)

conn = sqlite3.connect('data/monolit.db')
cur = conn.cursor()

for fact in facts:
    fact_id = hashlib.sha256(fact['text'].encode()).hexdigest()[:16]
    tags_str = ','.join(fact['tags']) if isinstance(fact['tags'], list) else fact['tags']
    
    cur.execute('''
        INSERT OR IGNORE INTO ltm 
        VALUES (?,?,?,?,?,?)
    ''', (fact_id, fact['text'], tags_str, 
          fact.get('source',''), fact.get('conf',0.75), 
          int(time.time())))

conn.commit()
print(f'✅ Wgrano {len(facts)} faktów')
EOF
```

---

## ✅ CZY WIEDZA DZIAŁA?

### Test 1: Sprawdź bazę

```bash
sqlite3 data/monolit.db "SELECT COUNT(*) FROM ltm;"
# Powinno pokazać ~2932+

sqlite3 data/monolit.db "SELECT * FROM ltm LIMIT 3;"
# Powinno pokazać przykładowe fakty
```

### Test 2: Test search

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8080/api/ltm/search?q=chanel&limit=3"

# Powinno zwrócić fakty o Chanel
```

### Test 3: Test w chacie

```
User: "Co wiesz o Coco Chanel?"

System powinien:
✅ Znaleźć fakty o Chanel w LTM
✅ Użyć ich w odpowiedzi
✅ Podać konkretne detale (np. "Chanel No. 5", "little black dress")
```

---

## 🔥 KLUCZOWE PUNKTY:

1. **Wiedza = SQLite database** (`data/monolit.db`)
2. **Ładowanie = On-demand** (nie przy starcie, ale przy każdym pytaniu)
3. **Search = Hybrid** (tags + full-text + TF-IDF scoring)
4. **Dodawanie = 4 sposoby** (API, auto-learn, script, bulk JSON)
5. **Używanie = Automatyczne** (jeśli `use_memory: true` w request)

---

## 📊 OBECNY STAN:

```
Fakty w bazie:     ~2932 (po ostatnim wgraniu)
Kategorii:         8 (moda, Vinted, social, etc.)
Format:            SQLite (szybki, offline)
Search:            Hybrid (BM25 + TF-IDF)
Auto-load:         NIE (on-demand)
Performance:       < 100ms na query
```

---

## ⚠️ JEŚLI BRAK FAKTÓW:

```bash
# Wgraj z backup:
python3 << 'EOF'
import sqlite3, json, hashlib, time
with open('facts_complete.json') as f:
    facts = json.load(f)
conn = sqlite3.connect('data/monolit.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS ltm (id TEXT PRIMARY KEY, text TEXT, tags TEXT, source TEXT, conf REAL, created_at INTEGER)')
for fact in facts:
    fid = hashlib.sha256(fact['text'].encode()).hexdigest()[:16]
    tags = ','.join(fact['tags']) if isinstance(fact['tags'], list) else fact['tags']
    cur.execute('INSERT OR IGNORE INTO ltm VALUES (?,?,?,?,?,?)', 
                (fid, fact['text'], tags, fact.get('source',''), fact.get('conf',0.75), int(time.time())))
conn.commit()
print(f'✅ {len(facts)} faktów')
EOF
```

---

**GOTOWE! Teraz wiesz jak działa wiedza w systemie! 🧠**
