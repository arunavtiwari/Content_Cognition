from __future__ import annotations

from typing import Dict

from app.services.adapters import mirofish_optimize


def optimize_script(script: str, desired_outcome: str, brand_voice: str, platform: str, mirofish_enabled: bool) -> Dict[str, str | Dict[str, str]]:
    outcome_line = f"Outcome Target: {desired_outcome}"
    platform_line = f"Platform Adaptation: {platform}"
    voice_line = f"Voice Check: {brand_voice}"

    mirofish_context: Dict[str, str] = {
        "mirofish_version": "disabled",
        "recommended_change": "N/A",
        "confidence": "0.00",
        "mode": "disabled",
        "script": script,
    }
    if mirofish_enabled:
        mirofish_context = mirofish_optimize(
            script=script,
            desired_outcome=desired_outcome,
            platform=platform,
        )

    optimized = (
        f"{script}\n\n"
        "--- Optimization Additions ---\n"
        "- Add a stronger first 2-second hook.\n"
        "- Increase specificity with one proof point.\n"
        "- End with a single explicit CTA.\n"
        f"- {outcome_line}.\n"
        f"- {platform_line}.\n"
        f"- {voice_line}.\n"
        f"- Mirofish recommendation: {mirofish_context['recommended_change']}\n"
        f"- Mirofish confidence: {mirofish_context['confidence']}\n"
    )

    return {
        "optimized_script": optimized,
        "report": {
            "hook": "Strengthened opening for improved watch retention.",
            "clarity": "Reduced ambiguity and improved actionability.",
            "cta": "Added outcome-focused CTA.",
            "mirofish": f"mode={mirofish_context['mode']}; version={mirofish_context['mirofish_version']}",
        },
    }


def generate_ab_variants(hook: str, cta: str, desired_outcome: str) -> list[dict[str, str]]:
    return [
        {
            "hook": f"Stop scrolling: one shift can improve your {desired_outcome.lower()} this week.",
            "cta": f"Reply 'START' to get a plug-and-play version. ({cta})",
            "hypothesis": "Direct urgency framing should increase early retention.",
        },
        {
            "hook": f"Most creators fail at {desired_outcome.lower()} because they skip this first step.",
            "cta": f"Comment 'CHECKLIST' to get the framework. ({cta})",
            "hypothesis": "Problem-framing hook should improve conversion intent.",
        },
        {
            "hook": hook,
            "cta": f"Save this and DM 'MAP' for a custom plan. ({cta})",
            "hypothesis": "Save + DM dual CTA should improve post-engagement and leads.",
        },
    ]
