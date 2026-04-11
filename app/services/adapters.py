from __future__ import annotations

import json
import os
from typing import Dict, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen


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


def call_open_source_llm(prompt: str, model: str, temperature: float) -> Optional[str]:
    """
    Attempts a local open-source LLM call via Ollama-compatible endpoint.
    Returns None when unavailable so callers can fall back safely.
    """
    base_url = os.getenv("OPEN_SOURCE_LLM_URL", "http://127.0.0.1:11434")
    endpoint = f"{base_url.rstrip('/')}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    req = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(req, timeout=8) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            output = body.get("response")
            if isinstance(output, str) and output.strip():
                return output.strip()
    except (URLError, TimeoutError, json.JSONDecodeError):
        return None

    return None
