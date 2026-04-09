from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import (
    ABVariantsRequest,
    ABVariantsResponse,
    ABVariant,
    GenerateIdeasRequest,
    GenerateIdeasResponse,
    OptimizeScriptRequest,
    OptimizeScriptResponse,
)
from app.services.adapters import normalize_meta_tribe_features
from app.services.generator import generate_ideas
from app.services.goal_mapper import map_goal_to_weights
from app.services.optimizer import generate_ab_variants, optimize_script
from app.services.skill_router import route_skills

app = FastAPI(title="Content Cognition API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def ui() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate-ideas", response_model=GenerateIdeasResponse)
def generate_ideas_endpoint(payload: GenerateIdeasRequest) -> GenerateIdeasResponse:
    weights = map_goal_to_weights(payload.desired_outcome)
    selected_skills = route_skills(
        desired_outcome=payload.desired_outcome,
        content_type=payload.content_type,
        platform=payload.platform,
    )

    normalized_features = normalize_meta_tribe_features(payload.meta_tribe_features)

    ideas = generate_ideas(
        niche=payload.niche,
        audience=payload.audience,
        desired_outcome=payload.desired_outcome,
        content_type=payload.content_type,
        platform=payload.platform,
        brand_voice=payload.brand_voice,
        weights=weights,
        selected_skills=selected_skills,
        meta_features=normalized_features,
        idea_count=payload.idea_count,
        use_open_source_llm=payload.use_open_source_llm,
        llm_model=payload.llm_model,
        llm_temperature=payload.llm_temperature,
    )

    return GenerateIdeasResponse(
        objective_profile=weights,
        selected_skills=selected_skills,
        ideas=ideas,
    )


@app.post("/optimize-script", response_model=OptimizeScriptResponse)
def optimize_script_endpoint(payload: OptimizeScriptRequest) -> OptimizeScriptResponse:
    result = optimize_script(
        script=payload.script,
        desired_outcome=payload.desired_outcome,
        brand_voice=payload.brand_voice,
        platform=payload.platform,
        mirofish_enabled=payload.mirofish_enabled,
    )
    return OptimizeScriptResponse(
        original_script=payload.script,
        optimized_script=result["optimized_script"],
        report=result["report"],
    )


@app.post("/ab-variants", response_model=ABVariantsResponse)
def ab_variants_endpoint(payload: ABVariantsRequest) -> ABVariantsResponse:
    variants = generate_ab_variants(
        hook=payload.hook,
        cta=payload.cta,
        desired_outcome=payload.desired_outcome,
    )
    return ABVariantsResponse(
        title=payload.title,
        variants=[ABVariant(**item) for item in variants],
    )
