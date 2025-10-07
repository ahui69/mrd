#!/usr/bin/env bash
set -euo pipefail

# Load env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Install system deps if needed (Ubuntu minimal)
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install -r requirements.txt >/dev/null 2>&1 || true
python3 -m pip install python-multipart >/dev/null 2>&1 || true

# Run app
exec python3 -m uvicorn monolit:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}" --reload
