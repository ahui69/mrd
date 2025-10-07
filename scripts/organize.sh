#!/bin/bash
# ORGANIZACJA STRUKTURY PROJEKTU (MINIMALNE ZMIANY)

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  📁 ORGANIZACJA PROJEKTU - CZYTELNA STRUKTURA              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# OPCJA PROSTA: Tylko uporządkowanie docs/scripts/knowledge
# Kod (*.py, *.html) pozostaje w rootcie - ZERO zmian w imports!

echo "📁 Tworzę foldery..."
mkdir -p docs
mkdir -p scripts
mkdir -p knowledge/generators
mkdir -p out/{images,writing,dev}
mkdir -p data/uploads
mkdir -p tmp
mkdir -p logs

echo ""
echo "📚 DOCS (dokumentacja)..."
mv README.md docs/ 2>/dev/null || true
mv FINAL_COMPLETE.md docs/ 2>/dev/null || true
mv REAL_VS_FAKE.md docs/ 2>/dev/null || true
mv CO_TERAZ_DZIALA.md docs/ 2>/dev/null || true
mv JAK_DZIALA_WIEDZA.md docs/ 2>/dev/null || true
mv FILES_TO_DEPLOY.txt docs/ 2>/dev/null || true
mv STRUKTURA_FOLDEROW.md docs/ 2>/dev/null || true

# Skopiuj README z powrotem do roota (dla GitHub)
cp docs/README.md README.md 2>/dev/null || cat > README.md << 'EOF'
# Mordzix AI

AI Assistant with 5200+ facts, auto-learning, and production-ready deployment.

See `docs/` for full documentation.

## Quick Start

```bash
bash start.sh
```

Visit: http://localhost:8080/

## Documentation

- `docs/README.md` - Full guide
- `docs/FINAL_COMPLETE.md` - Complete documentation
- `docs/REAL_VS_FAKE.md` - What works online
- `docs/JAK_DZIALA_WIEDZA.md` - How knowledge system works
EOF

echo "   ✅ Docs przeniesione do docs/"

echo ""
echo "🧪 SCRIPTS (utility)..."
mv start.sh scripts/ 2>/dev/null || true
mv download_list.sh scripts/ 2>/dev/null || true
mv organize.sh scripts/ 2>/dev/null || true

# Symlink w rootcie dla wygody
ln -sf scripts/start.sh start.sh 2>/dev/null || true

echo "   ✅ Scripts przeniesione do scripts/"

echo ""
echo "📚 KNOWLEDGE (fakty + generatory)..."
mv facts_complete.json knowledge/ 2>/dev/null || true
mv facts_5000.json knowledge/ 2>/dev/null || true
mv generate_5000_facts.py knowledge/generators/ 2>/dev/null || true
mv generate_more_facts.py knowledge/generators/ 2>/dev/null || true

# Stwórz README w knowledge/
cat > knowledge/README.md << 'EOF'
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
EOF

echo "   ✅ Knowledge przeniesione do knowledge/"

echo ""
echo "🚀 DEPLOYMENT (pozostaje jak jest)..."
echo "   ✅ deployment/ - bez zmian"

echo ""
echo "📊 DATA / OUT (gitignore)..."
echo "   ✅ data/ - bazy danych"
echo "   ✅ out/ - outputy"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ORGANIZACJA ZAKOŃCZONA!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 NOWA STRUKTURA:"
echo ""
echo "/workspace/"
echo "├── 📚 docs/                    # Dokumentacja"
echo "├── 🧪 scripts/                 # Utility (start.sh, etc)"
echo "├── 📚 knowledge/               # Fakty + generatory"
echo "├── 🚀 deployment/              # Deploy ready"
echo "├── 📊 data/                    # Bazy (gitignore)"
echo "├── 📤 out/                     # Outputs (gitignore)"
echo "└── 🔧 ROOT                     # Kod Python + HTML"
echo "    ├── monolit.py"
echo "    ├── *_endpoint.py"
echo "    ├── middleware.py"
echo "    ├── frontend.html"
echo "    ├── paint.html"
echo "    ├── .env, .gitignore"
echo "    └── start.sh -> scripts/start.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ KOD POZOSTAŁ W ROOTCIE - ZERO ZMIAN W IMPORTS!"
echo "✅ DOKUMENTACJA / SCRIPTS / KNOWLEDGE - UPORZĄDKOWANE"
echo ""
echo "🚀 URUCHOM:"
echo "   bash start.sh"
echo ""
echo "lub:"
echo "   bash scripts/start.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
