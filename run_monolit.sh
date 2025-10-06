#!/usr/bin/env bash
set -euo pipefail

# env (gdyby bashrc nie zadziałał)
export BASE="${BASE:-http://127.0.0.1:8000}"
export AUTH_TOKEN="${AUTH_TOKEN:-ssjjMijaja6969}"
export AUTH="Authorization: Bearer $AUTH_TOKEN"
export FIRECRAWL_KEY="${FIRECRAWL_KEY:-fc-ec025f3a447c46878bee6926b49c17d3}"
export SERPAPI_KEY="${SERPAPI_KEY:-a5cb3592980e0ff9042a0be2d3f7df276b8db9391325295d71020d46a6089f50}"

cd /workspace/mrd69
nohup gunicorn -w 4 -b 0.0.0.0:8000 monolit:app --timeout 120 --reload > monolit.log 2>&1 &
echo "monolit up. tail -n 50 /workspace/mrd69/monolit.log"
