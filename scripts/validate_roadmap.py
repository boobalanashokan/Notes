#!/usr/bin/env python3
"""Validate and remap legacy flat roadmap dependency IDs into the nested v2 structure."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

ROOT = Path(__file__).resolve().parents[1]
OLD_ROADMAP_PATH = ROOT / "roadmap.json"
NEW_ROADMAP_PATH = ROOT / "roadmap.v2.json"
OUTPUT_PATH = ROOT / "roadmap.v3.json"


def normalize_value(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().lower()


def flatten_dependencies(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        values = value
    else:
        values = [value]

    result: List[str] = []
    for item in values:
        if item is None:
            continue
        item_str = str(item).strip()
        if item_str:
            result.append(item_str)
    return result


def build_old_flat_mapping(flat_roadmap: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
    mapping: Dict[str, Dict[str, str]] = {}
    for item in flat_roadmap:
        item_id = str(item.get("id", "")).strip()
        if not item_id:
            continue
        mapping[item_id] = {
            "area": normalize_value(item.get("area", "")),
            "topic": normalize_value(item.get("topic", "")),
        }
    return mapping


def build_new_topic_lookup(nested_roadmap: Dict[str, Any]) -> tuple[Dict[str, str], Set[str]]:
    lookup: Dict[str, str] = {}
    all_topic_ids: Set[str] = set()

    for track in nested_roadmap.get("tracks", []):
        for area in track.get("areas", []):
            area_name = normalize_value(area.get("name", ""))
            for topic in area.get("topics", []):
                topic_id = str(topic.get("id", "")).strip()
                topic_name = normalize_value(topic.get("name", ""))
                if not topic_id:
                    continue
                all_topic_ids.add(topic_id)
                lookup[f"{area_name}|{topic_name}"] = topic_id
    return lookup, all_topic_ids


def remap_depends_on(raw_depends: List[str], old_flat_mapping: Dict[str, Dict[str, str]], new_lookup: Dict[str, str]) -> tuple[List[str], List[str], List[str]]:
    remapped: List[str] = []
    warnings: List[str] = []
    broken: List[str] = []

    for dep in raw_depends:
        dep_str = str(dep).strip()
        if not dep_str:
            continue

        if dep_str in old_flat_mapping:
            item_info = old_flat_mapping[dep_str]
            area_key = item_info["area"]
            topic_key = item_info["topic"]
            matched_id = new_lookup.get(f"{area_key}|{topic_key}")
            if matched_id:
                remapped.append(matched_id)
                continue

        if dep_str in new_lookup.values():
            remapped.append(dep_str)
            continue

        placeholder = f"UNMAPPED:{dep_str}"
        remapped.append(placeholder)
        warnings.append(dep_str)

    for dep in remapped:
        if dep.startswith("UNMAPPED:"):
            broken.append(dep)
            continue
        if dep not in new_lookup.values():
            broken.append(dep)

    return remapped, warnings, broken


def main() -> None:
    with OLD_ROADMAP_PATH.open("r", encoding="utf-8") as infile:
        old_roadmap = json.load(infile)

    with NEW_ROADMAP_PATH.open("r", encoding="utf-8") as infile:
        new_roadmap = json.load(infile)

    old_flat_mapping = build_old_flat_mapping(old_roadmap)
    new_lookup, all_topic_ids = build_new_topic_lookup(new_roadmap)

    total_processed = 0
    total_remapped = 0
    warnings: List[Dict[str, str]] = []
    topic_issues: List[Dict[str, Any]] = []

    for track in new_roadmap.get("tracks", []):
        for area in track.get("areas", []):
            area_name = str(area.get("name", "")).strip()
            for topic in area.get("topics", []):
                topic_name = str(topic.get("name", "")).strip()
                raw_depends = flatten_dependencies(topic.get("depends_on", []))
                total_processed += len(raw_depends)

                remapped, unmapped_ids, broken_ids = remap_depends_on(raw_depends, old_flat_mapping, new_lookup)
                topic["depends_on"] = remapped
                total_remapped += sum(1 for dep in remapped if dep not in {f"UNMAPPED:{d}" for d in unmapped_ids} and dep in all_topic_ids)

                if unmapped_ids or broken_ids:
                    topic_issues.append(
                        {
                            "area": area_name,
                            "topic": topic_name,
                            "raw_depends": raw_depends,
                            "resolved_depends": remapped,
                            "unmapped": unmapped_ids,
                            "broken": broken_ids,
                        }
                    )

                    for dep in unmapped_ids:
                        warnings.append({
                            "area": area_name,
                            "topic": topic_name,
                            "unmapped_id": dep,
                        })

                    for dep in broken_ids:
                        warnings.append({
                            "area": area_name,
                            "topic": topic_name,
                            "unmapped_id": dep,
                        })

    with OUTPUT_PATH.open("w", encoding="utf-8") as outfile:
        json.dump(new_roadmap, outfile, indent=2)
        outfile.write("\n")

    print(f"Total depends_on references processed: {total_processed}")
    print(f"Successfully remapped: {total_remapped}")
    if warnings:
        print("Warnings / unmapped ids:")
        for warning in warnings:
            print(f"  - {warning['area']} / {warning['topic']}: {warning['unmapped_id']}")
    else:
        print("Warnings / unmapped ids: none")

    if topic_issues:
        print("\nTopics with unmapped or broken depends_on entries:")
        for issue in topic_issues:
            print(f"  - {issue['area']} / {issue['topic']}")
            print(f"      raw: {issue['raw_depends']}")
            print(f"      resolved: {issue['resolved_depends']}")
            if issue['unmapped']:
                print(f"      unmapped: {issue['unmapped']}")
            if issue['broken']:
                print(f"      broken: {issue['broken']}")
    else:
        print("\nTopics with unmapped or broken depends_on entries: none")

    print(f"\nOutput file: {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
