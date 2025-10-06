#!/usr/bin/env bash
set -euo pipefail

# Optional env (safe defaults, without hardcoded secrets)
export BASE="${BASE:-http://127.0.0.1:8000}"
export AUTH_TOKEN="${AUTH_TOKEN:-changeme}"
export AUTH="Authorization: Bearer $AUTH_TOKEN"
# Respect existing keys; do not hardcode sensitive defaults
export FIRECRAWL_KEY="${FIRECRAWL_KEY:-}"
export SERPAPI_KEY="${SERPAPI_KEY:-}"
export LLM_API_KEY="${LLM_API_KEY:-}"

cd /workspace
nohup gunicorn -w 4 -b 0.0.0.0:8000 monolit:app --timeout 120 --reload > monolit.log 2>&1 &
echo "monolit up. tail -n 50 /workspace/monolit.log"
