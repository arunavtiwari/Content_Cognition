from __future__ import annotations

from typing import Dict, List

from app.models import IdeaVariant, ScriptIdea
from app.services.adapters import call_open_source_llm
from app.services.scoring import score_idea, total_score

ANGLE_LIBRARY = [
    "myth-busting",
    "step-by-step framework",
    "before-after transformation",
    "common mistakes",
    "data-backed insight",
    "challenge format",
    "story-driven revelation",
    "quick wins",
    "controversial take",
    "tool stack breakdown",
]


def _build_script(hook: str, audience: str, outcome: str) -> str:
    return (
        f"{hook}\n\n"
        f"1) Call out {audience} and the hidden problem.\n"
        "2) Deliver one surprising insight backed by practical logic.\n"
        "3) Show a simple framework the viewer can apply immediately.\n"
        f"4) Tie the framework to the outcome: {outcome}."
    )


def _build_llm_prompt(niche: str, audience: str, desired_outcome: str, content_type: str, platform: str, brand_voice: str, angle: str) -> str:
    return (
        "You are an expert content strategist. "
        f"Generate one {content_type} idea for {platform}. "
        f"Niche: {niche}. Audience: {audience}. Goal: {desired_outcome}. "
        f"Voice: {brand_voice}. Angle: {angle}. "
        "Return in plain text with three labeled lines: HOOK:, SCRIPT:, CTA:."
    )


def _extract_or_fallback(label: str, text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.strip().lower().startswith(f"{label.lower()}:"):
            value = line.split(":", 1)[1].strip()
            if value:
                return value
    return fallback


def generate_ideas(
    niche: str,
    audience: str,
    desired_outcome: str,
    content_type: str,
    platform: str,
    brand_voice: str,
    weights: Dict[str, float],
    selected_skills: List[str],
    meta_features: Dict[str, float],
    idea_count: int,
    use_open_source_llm: bool = False,
    llm_model: str = "llama3.1",
    llm_temperature: float = 0.4,
) -> List[ScriptIdea]:
    ideas: list[ScriptIdea] = []
    outcome_boost = 10 if any(word in desired_outcome.lower() for word in ["viral", "sales", "lead"]) else 5

    for i in range(idea_count):
        angle = ANGLE_LIBRARY[i % len(ANGLE_LIBRARY)]
        title = f"{content_type.title()} Idea #{i + 1}: {angle.title()} for {niche}"
        hook = f"{audience}: this {angle} approach can accelerate your {desired_outcome.lower()} in 30 days."
        cta = "Comment 'PLAN' for the exact template and next steps."
        script = _build_script(hook, audience, desired_outcome)

        if use_open_source_llm:
            llm_prompt = _build_llm_prompt(
                niche=niche,
                audience=audience,
                desired_outcome=desired_outcome,
                content_type=content_type,
                platform=platform,
                brand_voice=brand_voice,
                angle=angle,
            )
            llm_response = call_open_source_llm(
                prompt=llm_prompt,
                model=llm_model,
                temperature=llm_temperature,
            )
            if llm_response:
                hook = _extract_or_fallback("HOOK", llm_response, hook)
                llm_script = _extract_or_fallback("SCRIPT", llm_response, script)
                cta = _extract_or_fallback("CTA", llm_response, cta)
                script = llm_script

        caption = f"{platform.title()} strategy for {niche} | voice: {brand_voice}"

        scores = score_idea(base=50 + i, meta_features=meta_features, outcome_boost=outcome_boost)
        total = total_score(scores, weights)

        ab = IdeaVariant(
            hook=f"Most people in {niche} miss this {angle} trigger that changes results fast.",
            cta="DM 'GROWTH' and I will send a personalized outline.",
        )

        rationale = (
            f"Uses {angle} with skills {', '.join(selected_skills[:4])}; aligned to {desired_outcome} on {platform}."
        )

        ideas.append(
            ScriptIdea(
                title=title,
                hook=hook,
                script=script,
                cta=cta,
                caption=caption,
                virality_score=scores["virality"],
                conversion_score=scores["conversion"],
                retention_score=scores["retention"],
                brand_fit_score=scores["brand_fit"],
                novelty_score=scores["novelty"],
                total_score=total,
                skills_used=selected_skills,
                rationale=rationale,
                ab_variant=ab,
            )
        )

    return sorted(ideas, key=lambda x: x.total_score, reverse=True)
