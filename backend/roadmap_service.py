from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from models import Area, Roadmap, Track

ROOT_DIR = Path(__file__).resolve().parent.parent
ROADMAP_PATH = ROOT_DIR / "roadmap.json"


def load_roadmap() -> Roadmap:
    with ROADMAP_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return Roadmap.model_validate(data)


def get_track(track_id: str) -> Track | None:
    roadmap = load_roadmap()
    for track in roadmap.tracks:
        if track.id == track_id:
            return track
    return None


def compute_track_stats(track: Track) -> Dict[str, Any]:
    total_topics = 0
    completed_topics = 0
    area_breakdown: List[Dict[str, Any]] = []

    for area in track.areas:
        area_total = len(area.topics)
        area_completed = sum(1 for topic in area.topics if topic.done)
        total_topics += area_total
        completed_topics += area_completed
        area_breakdown.append(
            {
                "area_name": area.name,
                "total_topics": area_total,
                "completed_topics": area_completed,
                "percent_complete": round((area_completed / area_total) * 100, 2) if area_total else 0.0,
            }
        )

    percent_complete = round((completed_topics / total_topics) * 100, 2) if total_topics else 0.0
    return {
        "track_id": track.id,
        "track_name": track.name,
        "total_topics": total_topics,
        "completed_topics": completed_topics,
        "remaining_topics": total_topics - completed_topics,
        "percent_complete": percent_complete,
        "areas": area_breakdown,
    }
