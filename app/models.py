from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class GenerateIdeasRequest(BaseModel):
    niche: str = Field(..., description="Market/niche")
    audience: str
    desired_outcome: str
    content_type: str = Field(..., description="reels, blogs, ads, etc")
    platform: str = Field(..., description="instagram, tiktok, youtube, linkedin, blog")
    brand_voice: str
    constraints: List[str] = Field(default_factory=list)
    meta_tribe_features: Dict[str, float] = Field(default_factory=dict)
    campaign_history: Optional[Dict[str, float]] = None
    idea_count: int = Field(default=10, ge=1, le=25)
    use_open_source_llm: bool = False
    llm_model: str = "llama3.1"
    llm_temperature: float = Field(default=0.4, ge=0.0, le=1.5)


class IdeaVariant(BaseModel):
    hook: str
    cta: str


class ScriptIdea(BaseModel):
    title: str
    hook: str
    script: str
    cta: str
    caption: str
    virality_score: float
    conversion_score: float
    retention_score: float
    brand_fit_score: float
    novelty_score: float
    total_score: float
    skills_used: List[str]
    rationale: str
    ab_variant: IdeaVariant


class GenerateIdeasResponse(BaseModel):
    objective_profile: Dict[str, float]
    selected_skills: List[str]
    ideas: List[ScriptIdea]


class OptimizeScriptRequest(BaseModel):
    script: str
    desired_outcome: str
    brand_voice: str
    platform: str
    mirofish_enabled: bool = True


class OptimizeScriptResponse(BaseModel):
    original_script: str
    optimized_script: str
    report: Dict[str, str]


class ABVariantsRequest(BaseModel):
    title: str
    hook: str
    cta: str
    desired_outcome: str
    platform: str


class ABVariant(BaseModel):
    hook: str
    cta: str
    hypothesis: str


class ABVariantsResponse(BaseModel):
    title: str
    variants: List[ABVariant]
