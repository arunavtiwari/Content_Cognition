from __future__ import annotations

from typing import Dict


DEFAULT_META_TRIBE_FEATURES: Dict[str, float] = {
    "attention_spike": 0.5,
    "emotion_intensity": 0.5,
    "novelty_signal": 0.5,
}


def normalize_meta_tribe_features(features: Dict[str, float] | None) -> Dict[str, float]:
    normalized = dict(DEFAULT_META_TRIBE_FEATURES)
    if not features:
        return normalized

    for key, value in features.items():
        clamped = max(0.0, min(1.0, float(value)))
        normalized[key] = clamped
    return normalized


def mirofish_optimize(script: str, desired_outcome: str, platform: str) -> Dict[str, str]:
    """
    Local adapter stub for future mirofish GitHub integration.
    Returns deterministic optimization metadata so higher layers can be tested.
    """
    return {
        "mirofish_version": "local-stub-v1",
        "recommended_change": f"Emphasize one measurable promise for {desired_outcome} on {platform}.",
        "confidence": "0.71",
        "mode": "simulated",
        "script": script,
    }
