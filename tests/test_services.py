import pytest

pydantic = pytest.importorskip("pydantic")

from app.services.adapters import normalize_meta_tribe_features
from app.services.generator import generate_ideas
from app.services.goal_mapper import map_goal_to_weights
from app.services.optimizer import optimize_script
from app.services.skill_router import route_skills


def test_normalize_meta_tribe_features_clamps_values() -> None:
    features = normalize_meta_tribe_features({"attention_spike": 2, "emotion_intensity": -1})
    assert features["attention_spike"] == 1.0
    assert features["emotion_intensity"] == 0.0
    assert "novelty_signal" in features


def test_goal_mapper_for_conversion() -> None:
    weights = map_goal_to_weights("book more leads")
    assert weights["conversion"] > weights["virality"]


def test_skill_router_for_reels_lead_gen() -> None:
    skills = route_skills("get leads", "reels", "instagram")
    assert "hook_writing" in skills
    assert "cta_optimization" in skills


def test_optimizer_includes_mirofish_recommendation() -> None:
    result = optimize_script(
        script="A short script",
        desired_outcome="book calls",
        brand_voice="confident",
        platform="instagram",
        mirofish_enabled=True,
    )
    assert "Mirofish recommendation" in result["optimized_script"]
    assert "mode=simulated" in result["report"]["mirofish"]


def test_generate_ideas_uses_open_source_llm_when_available(monkeypatch) -> None:
    def fake_llm(prompt: str, model: str, temperature: float):
        return "HOOK: LLM Hook\nSCRIPT: LLM Script\nCTA: LLM CTA"

    monkeypatch.setattr("app.services.generator.call_open_source_llm", fake_llm)

    ideas = generate_ideas(
        niche="Fitness",
        audience="Busy professionals",
        desired_outcome="Get leads",
        content_type="reels",
        platform="instagram",
        brand_voice="Motivational",
        weights={"virality": 0.2, "conversion": 0.4, "retention": 0.2, "brand_fit": 0.1, "novelty": 0.1},
        selected_skills=["hook_writing"],
        meta_features={"attention_spike": 0.8, "emotion_intensity": 0.7, "novelty_signal": 0.6},
        idea_count=1,
        use_open_source_llm=True,
        llm_model="llama3.1",
        llm_temperature=0.4,
    )

    assert ideas[0].hook == "LLM Hook"
    assert ideas[0].script == "LLM Script"
    assert ideas[0].cta == "LLM CTA"
