# 📚 JAK WGRAĆ WIEDZĘ DO SYSTEMU

## 🎯 SZYBKI START (na serwerze):

```bash
# 1. Upewnij się że masz facts_complete.json
ls -lh facts_complete.json

# 2. Utwórz katalog data
mkdir -p data

# 3. Wgraj fakty do SQLite
python3 << 'EOF'
import sqlite3, json, hashlib, time

with open('facts_complete.json') as f:
    facts = json.load(f)

conn = sqlite3.connect('data/monolit.db')
cur = conn.cursor()

# Utwórz tabelę
cur.execute('''
    CREATE TABLE IF NOT EXISTS ltm (
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        tags TEXT,
        source TEXT,
        conf REAL DEFAULT 0.7,
        created_at INTEGER
    )
''')

# Wgraj fakty
for fact in facts:
    fact_id = hashlib.sha256(fact['text'].encode()).hexdigest()[:16]
    tags_str = ','.join(fact['tags']) if isinstance(fact['tags'], list) else fact['tags']
    
    cur.execute('''
        INSERT OR IGNORE INTO ltm 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        fact_id,
        fact['text'],
        tags_str,
        fact.get('source', ''),
        fact.get('conf', 0.75),
        int(time.time())
    ))

conn.commit()
print(f'✅ Wgrano {len(facts)} faktów!')
EOF

# 4. Sprawdź
python3 -c "import sqlite3; conn=sqlite3.connect('data/monolit.db'); print(f'Faktów w bazie: {conn.execute(\"SELECT COUNT(*) FROM ltm\").fetchone()[0]}'); conn.close()"
```

## ✅ GOTOWE!

Teraz system automatycznie użyje tych faktów podczas chatowania.
