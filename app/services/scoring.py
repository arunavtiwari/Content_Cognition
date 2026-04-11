from __future__ import annotations

from typing import Dict


def bounded(score: float) -> float:
    return max(0.0, min(100.0, round(score, 2)))


def score_idea(base: float, meta_features: Dict[str, float], outcome_boost: float) -> Dict[str, float]:
    attention = meta_features.get("attention_spike", 0.5) * 20
    emotion = meta_features.get("emotion_intensity", 0.5) * 20
    novelty_signal = meta_features.get("novelty_signal", 0.5) * 20

    virality = bounded(base + attention + novelty_signal + outcome_boost)
    conversion = bounded(base + emotion + (outcome_boost * 0.9))
    retention = bounded(base + attention + (emotion * 0.7))
    brand_fit = bounded(base + 15)
    novelty = bounded(base + novelty_signal + 8)

    return {
        "virality": virality,
        "conversion": conversion,
        "retention": retention,
        "brand_fit": brand_fit,
        "novelty": novelty,
    }


def total_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    total = (
        scores["virality"] * weights["virality"]
        + scores["conversion"] * weights["conversion"]
        + scores["retention"] * weights["retention"]
        + scores["brand_fit"] * weights["brand_fit"]
        + scores["novelty"] * weights["novelty"]
    )
    return bounded(total)
