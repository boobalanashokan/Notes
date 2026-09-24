from __future__ import annotations

from pathlib import Path
from typing import List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent


def markdown_path(track_id: str, area_id: str, topic_id: str) -> str:
    return f"Notes/{track_id.lower()}/{area_id.lower()}/{topic_id.lower()}.md"


def render_markdown_section(
    source_files: List[str],
    subtopics: List[str],
    status: str,
    note_text: str,
    mapped_at: str,
) -> str:
    source_lines = "\n".join(f"- [{Path(source).name}]({source})" for source in source_files) if source_files else "- None"
    checked = status == "Done"
    subtopic_lines = "\n".join(
        f"- [{'x' if checked else ' '}] {subtopic}" for subtopic in subtopics
    ) if subtopics else "- None"
    note_body = note_text.strip()
    return (
        "---\n"
        "## Mapping\n"
        f"**Mapped at:** {mapped_at}\n\n"
        "**Source files:**\n"
        f"{source_lines}\n\n"
        "**Subtopics covered:**\n"
        f"{subtopic_lines}\n\n"
        f"**Status:** {status}\n\n"
        f"{note_body}"
    ).rstrip() + "\n"


def build_full_markdown(topic_name: str, sections: List[str]) -> str:
    cleaned = [section.strip() for section in sections if section and section.strip()]
    if not cleaned:
        return f"# {topic_name}\n"
    return "# " + topic_name + "\n\n" + "\n\n".join(cleaned) + "\n"


def read_existing_markdown(track_id: str, area_id: str, topic_id: str) -> Optional[str]:
    file_path = ROOT_DIR / markdown_path(track_id, area_id, topic_id)
    if not file_path.exists():
        return None
    return file_path.read_text(encoding="utf-8")
