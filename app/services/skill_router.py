from __future__ import annotations

from typing import List


def route_skills(desired_outcome: str, content_type: str, platform: str) -> List[str]:
    outcome = desired_outcome.lower()
    content = content_type.lower()
    platform = platform.lower()

    skills: list[str] = ["audience_research", "clarity_editing"]

    if "reel" in content or platform in {"instagram", "tiktok", "youtube"}:
        skills.extend(["hook_writing", "retention_scripting", "pattern_interrupts"])
    if "blog" in content or platform == "blog":
        skills.extend(["seo_content_structuring", "long_form_storytelling"])
    if any(x in outcome for x in ["lead", "sales", "book", "conversion", "dm"]):
        skills.extend(["objection_handling", "cta_optimization", "offer_framing"])
    if any(x in outcome for x in ["viral", "reach", "share", "views"]):
        skills.extend(["trend_reframing", "virality_mechanics"])
    if any(x in outcome for x in ["authority", "trust", "education"]):
        skills.extend(["thought_leadership", "evidence_based_framing"])

    return sorted(set(skills))
