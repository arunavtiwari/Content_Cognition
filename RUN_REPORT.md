# Run Report

Date: 2026-04-09 (UTC)

## Commands executed in this environment

1. `python3 -m pip install --index-url https://pypi.org/simple fastapi uvicorn pydantic`
   - Result: failed because this environment blocks package download via proxy (403 Tunnel Forbidden).

2. `pytest -q`
   - Result: passes with dependency-aware skipping (`1 passed, 2 skipped`).

## Why the web app could not be started here

The FastAPI runtime dependencies (`fastapi`, `uvicorn`, `pydantic`) are not available in this sandbox and cannot be installed due network/proxy policy.

## To run locally on your machine

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/run_local.sh
```

Open:
- http://localhost:8000/
- http://localhost:8000/docs
