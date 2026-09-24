from types import SimpleNamespace

from ai_service import generate_track_guidance


def test_generate_track_guidance_returns_fallback_when_gemini_fails(monkeypatch):
    track = SimpleNamespace(
        name="MLOps",
        areas=[
            SimpleNamespace(
                name="Linux",
                topics=[
                    SimpleNamespace(name="Shell basics", week=1, done=False),
                    SimpleNamespace(name="Networking", week=2, done=True),
                ],
            )
        ],
    )
    stats = {
        "percent_complete": 50,
        "completed_topics": 1,
        "remaining_topics": 1,
        "areas": [
            {"area_name": "Linux", "completed_topics": 1, "total_topics": 2, "percent_complete": 50.0}
        ],
    }

    def boom(_prompt):
        raise RuntimeError("Gemini API is temporarily unavailable")

    monkeypatch.setattr("ai_service._call_gemini", boom)

    result = generate_track_guidance(track, stats)

    assert result["summary"]
    assert isinstance(result["focus_areas"], list)
    assert isinstance(result["next_actions"], list)
    assert result["focus_areas"]
    assert result["next_actions"]
