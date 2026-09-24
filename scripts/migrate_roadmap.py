#!/usr/bin/env python3
"""Migrate the legacy flat roadmap into a multi-track JSON structure."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "roadmap.json"
OUTPUT_PATH = ROOT / "roadmap.v2.json"


def slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def normalize_depends_on(raw_value: Any, id_map: Dict[str, str]) -> List[str]:
    if raw_value in (None, "", []):
        return []

    if isinstance(raw_value, list):
        values = raw_value
    else:
        values = [raw_value]

    result: List[str] = []
    for item in values:
        if item is None:
            continue
        tokens = str(item).split(",") if "," in str(item) else [str(item)]
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if token in id_map:
                result.append(id_map[token])
            else:
                result.append(slugify(token))
    return list(dict.fromkeys(result))


def build_roadmap(rows: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    ordered_areas: Dict[str, Dict[str, Any]] = {}
    topic_id_map: Dict[str, str] = {}

    for item in rows:
        area_name = str(item.get("area", "")).strip()
        if not area_name:
            continue

        area_key = slugify(area_name)
        area = ordered_areas.setdefault(
            area_key,
            {"id": area_key, "name": area_name, "topics": []},
        )

        topic_name = str(item.get("topic", "")).strip()
        base_topic_id = slugify(topic_name)
        topic_id = base_topic_id
        counter = 2
        while topic_id in topic_id_map.values():
            topic_id = f"{base_topic_id}-{counter}"
            counter += 1

        topic_id_map[str(item.get("id", ""))] = topic_id

        topic = {
            "id": topic_id,
            "name": topic_name,
            "week": int(item.get("week", 0) or 0),
            "type": str(item.get("type", "")),
            "subtopics": item.get("subtopics", []) or [],
            "learning_outcome": str(item.get("learning_outcome", "")),
            "project_task": str(item.get("project_task", "")),
            "depends_on": [],
            "done": bool(item.get("done", False)),
        }
        area["topics"].append(topic)

    for item in rows:
        area_name = str(item.get("area", "")).strip()
        if not area_name:
            continue

        area_key = slugify(area_name)
        area = ordered_areas[area_key]
        topic_name = str(item.get("topic", "")).strip()
        topic_id = None
        for topic in area["topics"]:
            if topic["name"] == topic_name:
                topic_id = topic["id"]
                break
        if topic_id is None:
            continue

        topic = next(topic for topic in area["topics"] if topic["id"] == topic_id)
        topic["depends_on"] = normalize_depends_on(item.get("depends_on", []), topic_id_map)

    track = {
        "id": "mlops",
        "name": "MLOps",
        "areas": list(ordered_areas.values()),
    }

    return {"tracks": [track]}


def main() -> None:
    with INPUT_PATH.open("r", encoding="utf-8") as infile:
        rows = json.load(infile)

    roadmap = build_roadmap(rows)
    with OUTPUT_PATH.open("w", encoding="utf-8") as outfile:
        json.dump(roadmap, outfile, indent=2)
        outfile.write("\n")

    tracks = roadmap.get("tracks", [])
    areas = sum(len(track.get("areas", [])) for track in tracks)
    topics = sum(len(area.get("topics", [])) for track in tracks for area in track.get("areas", []))
    subtopics = sum(len(topic.get("subtopics", [])) for track in tracks for area in track.get("areas", []) for topic in area.get("topics", []))

    print(f"Tracks: {len(tracks)}")
    print(f"Areas: {areas}")
    print(f"Topics: {topics}")
    print(f"Total subtopics migrated: {subtopics}")
    print(f"Output: {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
