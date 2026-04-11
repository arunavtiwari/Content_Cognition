from app.services.adapters import normalize_meta_tribe_features


def test_smoke_normalize_defaults() -> None:
    features = normalize_meta_tribe_features(None)
    assert features['attention_spike'] == 0.5
    assert features['emotion_intensity'] == 0.5
    assert features['novelty_signal'] == 0.5
