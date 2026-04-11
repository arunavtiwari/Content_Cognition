from __future__ import annotations

from typing import Dict


DEFAULT_WEIGHTS = {
    "virality": 0.25,
    "conversion": 0.25,
    "retention": 0.2,
    "brand_fit": 0.2,
    "novelty": 0.1,
}


def map_goal_to_weights(goal: str) -> Dict[str, float]:
    goal_lower = goal.lower()
    if any(word in goal_lower for word in ["viral", "reach", "share", "views"]):
        return {
            "virality": 0.4,
            "conversion": 0.15,
            "retention": 0.25,
            "brand_fit": 0.1,
            "novelty": 0.1,
        }
    if any(word in goal_lower for word in ["sales", "lead", "dm", "book", "conversion"]):
        return {
            "virality": 0.15,
            "conversion": 0.45,
            "retention": 0.2,
            "brand_fit": 0.15,
            "novelty": 0.05,
        }
    if any(word in goal_lower for word in ["trust", "authority", "education"]):
        return {
            "virality": 0.1,
            "conversion": 0.2,
            "retention": 0.25,
            "brand_fit": 0.35,
            "novelty": 0.1,
        }
    return DEFAULT_WEIGHTS
