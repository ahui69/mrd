# 📚 Knowledge Base

## Files

- `facts_complete.json` - 5200+ facts in 8 categories
- `facts_5000.json` - Backup

## Generators

- `generators/generate_5000_facts.py` - Generate facts
- `generators/generate_more_facts.py` - Extend knowledge

## How to load

```bash
python3 << 'PYEOF'
import sqlite3, json, hashlib, time
with open('knowledge/facts_complete.json') as f:
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
print(f'✅ {len(facts)} facts loaded')
PYEOF
```
