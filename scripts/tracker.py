#!/usr/bin/env python3
"""Generate progress views from roadmap.json and explicit study-note signals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "roadmap.json"
README = ROOT / "README.md"
TRACKER = ROOT / "TRACKER.md"
TODAY = ROOT / "TODAY.md"
PROJECT_TASKS = ROOT / "PROJECT_TASKS.md"
SKILLS = ROOT / "SKILLS.md"
GENERATED_FILES = (README, TRACKER, TODAY, PROJECT_TASKS, SKILLS)
IGNORED_NOTE_NAMES = {path.name for path in GENERATED_FILES} | {"PROGRESS.md"}
START_MARKER = "<!-- INDEX:START -->"
END_MARKER = "<!-- INDEX:END -->"
QUICK_START = "<!-- QUICK-DASHBOARD:START -->"
QUICK_END = "<!-- QUICK-DASHBOARD:END -->"
TRACKERS_START = "<!-- TRACKERS:START -->"
TRACKERS_END = "<!-- TRACKERS:END -->"
DETAIL_START = "<!-- DETAILED-DASHBOARD:START -->"
DETAIL_END = "<!-- DETAILED-DASHBOARD:END -->"
STATUS_DONE_RE = re.compile(r"(?im)^\s*(?:[-*]\s*)?(?:status|state|progress)\s*[:\-]\s*(?:done|complete|completed|finished)\s*$")
CHECKED_TOPIC_RE = re.compile(r"(?im)^\s*[-*]?\s*\[x\]\s+(?P<text>.+?)\s*$")
HEADING_RE = re.compile(r"(?im)^\s*#{1,6}\s+(?P<text>.+?)\s*$")
CHECKBOX_RE = re.compile(r"(?im)^\s*[-*]\s*\[(?P<mark>[ xX])\]\s+(?P<text>.+?)\s*$")


def load_roadmap() -> list[dict]:
    try:
        data = json.loads(ROADMAP.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"Could not load {ROADMAP.name}: {error}") from error
    ids = [row.get("id") for row in data] if isinstance(data, list) else []
    if not data or any(not row.get("id") or not row.get("topic") for row in data) or len(ids) != len(set(ids)):
        raise SystemExit(f"{ROADMAP.name} must contain a non-empty list with unique IDs and topics")
    return data


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*_]", "", value).strip().lower())


def section_for_topic(text: str, row: dict, roadmap: list[dict]) -> str | None:
    headings = list(HEADING_RE.finditer(text))
    unique = sum(normalize(item["topic"]) == normalize(row["topic"]) for item in roadmap) == 1
    for index, heading in enumerate(headings):
        heading_text = normalize(heading.group("text"))
        if normalize(row["topic"]) in heading_text and (normalize(row["area"]) in heading_text or unique):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            return text[heading.start():end]
    return None


def section_is_done(section: str, row: dict) -> bool:
    if STATUS_DONE_RE.search(section):
        return True
    if any(normalize(row["topic"]) in normalize(match.group("text")) for match in CHECKED_TOPIC_RE.finditer(section)):
        return True
    checked = [normalize(match.group("text")) for match in CHECKBOX_RE.finditer(section) if match.group("mark").lower() == "x"]
    return bool(row.get("subtopics")) and all(any(normalize(item) in value for value in checked) for item in row["subtopics"])


def scan_notes(roadmap: list[dict]) -> dict[str, bool]:
    texts = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or ".github" in path.parts or "scripts" in path.parts or path.name in IGNORED_NOTE_NAMES:
            continue
        try:
            texts.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            pass
    return {
        row["id"]: any((section := section_for_topic(text, row, roadmap)) and section_is_done(section, row) for text in texts)
        for row in roadmap
    }


def progress(roadmap: list[dict]):
    total = len(roadmap)
    completed = sum(row["done"] for row in roadmap)
    return total, completed, total - completed, completed / total if total else 0, next((row for row in roadmap if not row["done"]), None)


def table(rows: list[list[str]]) -> str:
    widths = [max(len(row[index]) for row in rows) for index in range(len(rows[0]))]
    output = ["| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(rows[0])) + " |"]
    output.append("| " + " | ".join("-" * max(3, width) for width in widths) + " |")
    output.extend("| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |" for row in rows[1:])
    return "\n".join(output)


def write_tracker(roadmap: list[dict]) -> None:
    lines = ["# MLOps Career Tracker", "", "> **Generated from:** `roadmap.json` and explicit completion signals in study notes.", "> Update your notes; the views are regenerated automatically.", "", "## Completion Signals", "", "Use `Status: Done` in a topic section, check its topic heading, or check every listed subtopic.", "A note existing by itself never marks work complete.", "", "---", "", "## Complete Roadmap", ""]
    for row in roadmap:
        lines += [f"### {row['id']} - Week {row['week']} - {row['area']} - {row['topic']}", "", f"- **Type:** {row['type']}", f"- **Done?:** [{'x' if row['done'] else ' '} ]".replace(" ]", "]"), f"- **Depends On:** {row.get('depends_on') or 'None'}", f"- **Learning / Outcome:** {row['learning_outcome']}", "- **Subtopics to Learn:", *[f"  - {item}" for item in row["subtopics"]], f"- **Project Task:** {row['project_task']}", ""]
    TRACKER.write_text("\n".join(lines), encoding="utf-8")


def update_readme(roadmap: list[dict]) -> None:
    total, completed, remaining, pct, next_row = progress(roadmap)
    focus = f"**Area:** {next_row['area']}\n\n**Topic:** {next_row['topic']}\n\n**Project Task:** {next_row['project_task']}" if next_row else "All roadmap units are complete."
    quick = "\n".join([QUICK_START, "<!-- Generated by scripts/tracker.py. -->", "", "## Quick Dashboard", "", f"**{completed}/{total} complete ({pct:.0%})**", f"`{'#' * round(pct * 20)}{'-' * (20 - round(pct * 20))}`", f"Next: {next_row['topic'] if next_row else 'All complete'}", QUICK_END])
    trackers = "\n".join([TRACKERS_START, "## Trackers & Notes", "", "- [Complete roadmap](TRACKER.md)", "- [Today's focus](TODAY.md)", "- [Project tasks](PROJECT_TASKS.md)", "- [Skills progress](SKILLS.md)", "", "The Index below contains every Markdown study note and generated tracker file.", TRACKERS_END])
    area_rows = [["Area", "Units", "Done", "Progress"]]
    for area in dict.fromkeys(row["area"] for row in roadmap):
        area_items = [row for row in roadmap if row["area"] == area]
        area_done = sum(row["done"] for row in area_items)
        area_rows.append([area, str(len(area_items)), str(area_done), f"{area_done / len(area_items):.0%}"])
    detailed = "\n".join([DETAIL_START, "## Detailed Dashboard", "", f"- **Total units:** {total}", f"- **Completed:** {completed}", f"- **Remaining:** {remaining}", f"- **Completion:** {pct:.0%}", f"- **Current week:** {next_row['week'] if next_row else 'Complete'}", "", "### Current Focus", "", focus, "", "### Progress by Area", "", table(area_rows), "", "> Progress is detected from explicit completion signals in your notes.", DETAIL_END])
    existing = README.read_text(encoding="utf-8", errors="ignore") if README.exists() else ""
    rules = existing[existing.find("## Rules"):] if "## Rules" in existing else "## Rules\n\n- Mark a unit complete only when you can explain the subtopics and reproduce the task.\n- Do not mark work complete merely because GPT produced code.\n"
    text = "# MLOps Career Tracker\n\n" + quick + "\n\n" + f"{START_MARKER}\n## Index\n\n{END_MARKER}" + "\n\n" + trackers + "\n\n" + detailed + "\n\n" + rules.strip() + "\n"
    README.write_text(text, encoding="utf-8")


def update_derived_views(roadmap: list[dict]) -> None:
    rows = [row for row in roadmap if not row["done"]][:12]
    TODAY.write_text("# Today\n\n> Automatically generated from the first incomplete roadmap units.\n\n" + "\n".join(f"- [ ] **{row['id']} - {row['area']} - {row['topic']}** - {row['project_task']}" for row in rows) + ("\n" if rows else "All roadmap units are complete.\n"), encoding="utf-8")
    task_rows = [["ID", "Week", "Area", "Topic", "Project Task", "Depends On", "Done?"]]
    task_rows += [[row["id"], str(row["week"]), row["area"], row["topic"], row["project_task"], row.get("depends_on") or "-", "x" if row["done"] else ""] for row in roadmap if row["type"].lower() == "build"]
    PROJECT_TASKS.write_text("# Project Tasks\n\n> Automatically generated from `roadmap.json`.\n\n" + table(task_rows) + "\n", encoding="utf-8")
    skill_rows = [["Area", "Units", "Done", "Progress"]]
    for area in dict.fromkeys(row["area"] for row in roadmap):
        area_rows = [row for row in roadmap if row["area"] == area]
        done = sum(row["done"] for row in area_rows)
        skill_rows.append([area, str(len(area_rows)), str(done), f"{done / len(area_rows):.0%}"])
    SKILLS.write_text("# Skills Progress\n\n> Automatically generated from `roadmap.json`.\n\n" + table(skill_rows) + "\n", encoding="utf-8")


def update_index() -> None:
    def display(path: Path) -> str:
        return (path.stem if path.suffix.lower() == ".md" else path.name).replace("_", " ").replace("-", " ").strip().title()

    def walk(directory: Path, level: int = 0) -> list[str]:
        lines = []
        for item in sorted(directory.iterdir(), key=lambda path: (path.is_file(), path.name.lower())):
            if item.name.startswith(".") or item.resolve() == README.resolve() or item.name.lower() == "scripts":
                continue
            if item.is_dir():
                lines += [f"{'#' * min(level + 2, 6)} {display(item)}", "", *walk(item, level + 1)]
            elif item.suffix.lower() == ".md":
                lines.append(f"{'  ' * level}- [{display(item)}]({item.relative_to(ROOT).as_posix()})")
        return lines

    readme = README.read_text(encoding="utf-8")
    index = f"{START_MARKER}\n## Index\n\n" + "\n".join(walk(ROOT)) + f"\n{END_MARKER}"
    readme = readme.split(START_MARKER)[0] + index + readme.split(END_MARKER, 1)[1] if START_MARKER in readme and END_MARKER in readme else readme.rstrip() + "\n\n" + index + "\n"
    README.write_text(readme, encoding="utf-8")


def generate() -> tuple[int, int]:
    roadmap = load_roadmap()
    note_state = scan_notes(roadmap)
    for row in roadmap:
        row["done"] = note_state[row["id"]]
    write_tracker(roadmap)
    update_readme(roadmap)
    update_derived_views(roadmap)
    update_index()
    total, completed, *_ = progress(roadmap)
    return total, completed


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate tracker views from study notes")
    parser.add_argument("--check", action="store_true", help="fail when generated files are stale")
    args = parser.parse_args()
    before = {path: path.read_bytes() if path.exists() else None for path in GENERATED_FILES}
    total, completed = generate()
    changed = [path for path in GENERATED_FILES if before[path] != path.read_bytes()]
    if args.check and changed:
        print("Generated files are stale: " + ", ".join(path.name for path in changed), file=sys.stderr)
        sys.exit(1)
    print(f"Tracker updated: {completed}/{total} complete ({completed / total:.0%}).")


if __name__ == "__main__":
    main()
