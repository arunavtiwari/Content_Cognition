# Content Cognition

Content Cognition is an AI application that generates and optimizes content ideas/scripts based on:
- user goals (virality, leads, authority, etc.)
- content format (reels, blogs, ads)
- platform constraints
- Meta Tribe V2-style cognitive signals (`attention_spike`, `emotion_intensity`, `novelty_signal`)
- optional mirofish optimization pass (implemented as pluggable adapter behavior)

## What is implemented

- FastAPI backend with endpoints:
  - `POST /generate-ideas`
  - `POST /optimize-script`
  - `POST /ab-variants`
  - `GET /health`
- Built-in skill routing for copywriting/marketing skills.
- Weighted ranking model:
  - `ViralityScore`
  - `ConversionScore`
  - `RetentionScore`
  - `BrandFitScore`
  - `NoveltyScore`
- Browser UI at `/` for generating ideas and optimizing scripts.
- Automated API tests with `pytest`.


## How the system comes up with content ideas

When you call `POST /generate-ideas`, idea creation follows this pipeline:

1. **Parse your brief**: niche, audience, desired outcome, content type, platform, and brand voice.
2. **Normalize brain/cognitive features**: Meta Tribe inputs are clamped to safe ranges using defaults when missing.
3. **Map outcome to scoring weights**: e.g., lead-gen increases conversion weight; virality goals increase virality/retention weights.
4. **Route writing/marketing skills**: select relevant skills (hook writing, CTA optimization, thought leadership, SEO, etc.) based on goal + format + platform.
5. **Generate candidate angles**: build idea titles/hooks/scripts from a structured angle library (myth-busting, quick wins, before/after, challenge format, etc.).
6. **Score each idea** using:
   - `ViralityScore`
   - `ConversionScore`
   - `RetentionScore`
   - `BrandFitScore`
   - `NoveltyScore`
7. **Rank and return top ideas** by weighted total score, including rationale and A/B hook + CTA variants.

This gives you ideas aligned to the result you want (reach, leads, authority, etc.) instead of generic brainstorming.


## Open-source LLM idea generation (Ollama)

The generator can use a local open-source model (instead of template-only generation) when `use_open_source_llm=true`.

1. Start Ollama locally (default URL expected by app: `http://127.0.0.1:11434`).
2. Pull a model, for example:

```bash
ollama pull llama3.1
```

3. Call `/generate-ideas` with:
- `"use_open_source_llm": true`
- `"llm_model": "llama3.1"`
- optional: set `OPEN_SOURCE_LLM_URL` env var if your Ollama host is different.

If the model endpoint is unavailable, the app automatically falls back to built-in template generation.

## Project structure

```txt
app/
  main.py
  models.py
  static/index.html
  services/
    generator.py
    goal_mapper.py
    optimizer.py
    scoring.py
    skill_router.py
tests/test_api.py
requirements.txt
```

## Run locally

### 1) Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Start API + UI

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Quick start script

```bash
./scripts/run_local.sh
```

Open:
- UI: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`

### 3) Run tests

```bash
pytest -q
```

`tests/test_api.py` is skipped automatically if FastAPI is not installed in the current environment.

## Example API usage

### Generate ideas

```bash
curl -X POST http://localhost:8000/generate-ideas \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "Fitness coaching",
    "audience": "Busy professionals 25-40",
    "desired_outcome": "Book consultation calls",
    "content_type": "reels",
    "platform": "instagram",
    "brand_voice": "Evidence-based motivational",
    "constraints": [],
    "meta_tribe_features": {
      "attention_spike": 0.8,
      "emotion_intensity": 0.7,
      "novelty_signal": 0.6
    },
    "idea_count": 5,
    "use_open_source_llm": true,
    "llm_model": "llama3.1"
  }'
```

### Optimize script

```bash
curl -X POST http://localhost:8000/optimize-script \
  -H "Content-Type: application/json" \
  -d '{
    "script": "Hook: If you sit 8+ hours, your metabolism drops faster than you think.",
    "desired_outcome": "Book consultation calls",
    "brand_voice": "Evidence-based motivational",
    "platform": "instagram",
    "mirofish_enabled": true
  }'
```

## Notes for production hardening

- Replace simulated Meta Tribe V2 feature ingestion with your real schema and connector.
- Replace the simulated mirofish optimization with direct GitHub integration logic.
- Add auth, rate limiting, persistence, analytics, and observability.


## Troubleshooting

- If `pip install -r requirements.txt` fails with proxy/network errors, configure your Python package index/proxy first, then retry.
- If `uvicorn` is not found, run `python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` inside the activated venv.
