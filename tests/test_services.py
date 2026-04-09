from app.services.adapters import normalize_meta_tribe_features
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
