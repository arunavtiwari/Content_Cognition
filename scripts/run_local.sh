#!/usr/bin/env bash
set -euo pipefail

if ! python3 -c "import fastapi,uvicorn" >/dev/null 2>&1; then
  echo "[ERROR] Missing dependencies: fastapi/uvicorn are not installed."
  echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

exec python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
