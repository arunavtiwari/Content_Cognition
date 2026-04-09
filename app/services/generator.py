from __future__ import annotations

from typing import Dict, List

from app.models import IdeaVariant, ScriptIdea
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


def _build_script(title: str, hook: str, audience: str, outcome: str) -> str:
    return (
        f"{hook}\n\n"
        f"1) Call out {audience} and the hidden problem.\n"
        "2) Deliver one surprising insight backed by practical logic.\n"
        "3) Show a simple framework the viewer can apply immediately.\n"
        f"4) Tie the framework to the outcome: {outcome}."
    )


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
) -> List[ScriptIdea]:
    ideas: list[ScriptIdea] = []
    outcome_boost = 10 if any(word in desired_outcome.lower() for word in ["viral", "sales", "lead"]) else 5

    for i in range(idea_count):
        angle = ANGLE_LIBRARY[i % len(ANGLE_LIBRARY)]
        title = f"{content_type.title()} Idea #{i + 1}: {angle.title()} for {niche}"
        hook = f"{audience}: this {angle} approach can accelerate your {desired_outcome.lower()} in 30 days."
        cta = "Comment 'PLAN' for the exact template and next steps."
        caption = f"{platform.title()} strategy for {niche} | voice: {brand_voice}"

        scores = score_idea(base=50 + i, meta_features=meta_features, outcome_boost=outcome_boost)
        total = total_score(scores, weights)

        script = _build_script(title, hook, audience, desired_outcome)
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
