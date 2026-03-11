# 🧪 JAK URUCHOMIĆ TESTY

## Quick Start

```bash
# Zainstaluj dev dependencies
pip install -r requirements-dev.txt

# Uruchom wszystkie testy
pytest

# Uruchom z coverage
pytest --cov=monolit --cov-report=html

# Uruchom tylko API tests
pytest tests/test_api.py -v

# Uruchom tylko memory tests
pytest tests/test_memory.py -v
```

## Co testujemy?

### API Endpoints (`test_api.py`)
- ✅ Health check
- ✅ LTM search (basic, empty query, add fact)
- ✅ Chat (basic, validation)
- ✅ Auth (unauthorized, invalid token)
- ✅ Cache stats
- ✅ Frontend serving

### Memory Functions (`test_memory.py`)
- ✅ LTM search returns list
- ✅ Results have scores
- ✅ Limit parameter works
- ✅ Tokenization exists

## Pre-commit Hooks

```bash
# Zainstaluj
pip install pre-commit
pre-commit install

# Uruchom manualnie
pre-commit run --all-files

# Auto format przed commitem
git commit -m "..."
# → black, ruff, mypy uruchomią się automatycznie!
```

## Code Quality

```bash
# Format code
black monolit.py

# Lint
ruff check monolit.py

# Type check
mypy monolit.py --ignore-missing-imports
```

## Continuous Integration

Dodaj do `.github/workflows/test.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov
```

