import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_generate_ideas() -> None:
    payload = {
        'niche': 'Fitness coaching',
        'audience': 'Busy professionals',
        'desired_outcome': 'Get more leads',
        'content_type': 'reels',
        'platform': 'instagram',
        'brand_voice': 'Motivational',
        'constraints': [],
        'meta_tribe_features': {
            'attention_spike': 0.8,
            'emotion_intensity': 0.7,
            'novelty_signal': 0.6,
        },
        'idea_count': 3,
    }
    response = client.post('/generate-ideas', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert len(body['ideas']) == 3
    assert 'selected_skills' in body


def test_optimize_script() -> None:
    payload = {
        'script': 'Original script text.',
        'desired_outcome': 'Book calls',
        'brand_voice': 'Professional',
        'platform': 'instagram',
        'mirofish_enabled': True,
    }
    response = client.post('/optimize-script', json=payload)
    assert response.status_code == 200
    assert 'Optimization Additions' in response.json()['optimized_script']
