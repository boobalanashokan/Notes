from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from git_service import GitOperationError, commit_and_push
from models import Track
from notes_service import (
    build_full_markdown,
    markdown_path,
    read_existing_markdown,
    render_markdown_section,
)
from roadmap_service import compute_track_stats, get_topic, get_track, load_roadmap
from upload_service import save_upload

ROOT_DIR = Path(__file__).resolve().parent.parent
ROADMAP_PATH = ROOT_DIR / "roadmap.json"

app = FastAPI(title="Study Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|.*\.app\.github\.dev)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _validated_topic_or_404(track_id: str, area_id: str, topic_id: str):
    topic = get_topic(track_id, area_id, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found in track '{track_id}' / area '{area_id}'")
    return topic


def _validate_source_files(source_files: list[str]) -> None:
    inbox_root = (ROOT_DIR / "Inbox").resolve()
    for source_file in source_files:
        if not isinstance(source_file, str):
            raise HTTPException(status_code=400, detail=f"Invalid source_file entry: {source_file!r}")
        candidate = (ROOT_DIR / source_file).resolve()
        if not candidate.exists() or not candidate.is_relative_to(inbox_root):
            raise HTTPException(status_code=400, detail=f"Source file not found under Inbox/: {source_file}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tracks", response_model=list[dict[str, str]])
def list_tracks() -> list[dict[str, str]]:
    roadmap = load_roadmap()
    return [{"id": track.id, "name": track.name} for track in roadmap.tracks]


@app.get("/tracks/{track_id}", response_model=Track)
def get_single_track(track_id: str) -> Track:
    track = get_track(track_id)
    if track is None:
        raise HTTPException(status_code=404, detail=f"Track '{track_id}' not found")
    return track


@app.get("/tracks/{track_id}/stats")
def get_track_stats(track_id: str) -> dict:
    track = get_track(track_id)
    if track is None:
        raise HTTPException(status_code=404, detail=f"Track '{track_id}' not found")
    return compute_track_stats(track)


@app.get("/tracks/{track_id}/areas/{area_id}/topics/{topic_id}/mapping-options")
def get_mapping_options(track_id: str, area_id: str, topic_id: str) -> dict:
    topic = _validated_topic_or_404(track_id, area_id, topic_id)
    return {"topic_name": topic.name, "valid_subtopics": list(topic.subtopics)}


@app.post("/tracks/{track_id}/areas/{area_id}/topics/{topic_id}/preview")
async def preview_note_mapping(
    track_id: str,
    area_id: str,
    topic_id: str,
    payload: dict[str, Any] = Body(...),
) -> dict:
    topic = _validated_topic_or_404(track_id, area_id, topic_id)

    status = payload.get("status")
    if status not in {"Learning", "Done", "Review"}:
        raise HTTPException(status_code=400, detail="status must be one of: Learning, Done, Review")

    source_files = payload.get("source_files") or []
    if not isinstance(source_files, list):
        raise HTTPException(status_code=400, detail="source_files must be a list")
    _validate_source_files(source_files)

    requested_subtopics = payload.get("subtopics") or []
    if not isinstance(requested_subtopics, list):
        raise HTTPException(status_code=400, detail="subtopics must be a list")
    valid_lookup = {item.strip().lower(): item.strip() for item in topic.subtopics}
    invalid_subtopics: list[str] = []
    normalized_subtopics: list[str] = []
    for item in requested_subtopics:
        if not isinstance(item, str):
            invalid_subtopics.append(str(item))
            continue
        key = item.strip().lower()
        if key not in valid_lookup:
            invalid_subtopics.append(item)
        else:
            normalized_subtopics.append(valid_lookup[key])
    if invalid_subtopics:
        raise HTTPException(status_code=400, detail={"invalid_subtopics": invalid_subtopics})

    note_text = str(payload.get("note_text", ""))
    mapped_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    target_path = markdown_path(track_id, area_id, topic_id)
    existing_content = read_existing_markdown(track_id, area_id, topic_id)
    new_section_preview = render_markdown_section(source_files, normalized_subtopics, status, note_text, mapped_at)

    final_append = (
        (existing_content + "\n\n" + new_section_preview).strip() + "\n"
        if existing_content
        else build_full_markdown(topic.name, [new_section_preview])
    )
    final_overwrite = build_full_markdown(topic.name, [new_section_preview])

    return {
        "topic_name": topic.name,
        "target_path": target_path,
        "file_exists": existing_content is not None,
        "existing_content": existing_content,
        "new_section_preview": new_section_preview,
        "would_append_result": final_append,
        "would_overwrite_result": final_overwrite,
    }


@app.post("/tracks/{track_id}/areas/{area_id}/topics/{topic_id}/approve")
async def approve_note_mapping(
    track_id: str,
    area_id: str,
    topic_id: str,
    payload: dict[str, Any] = Body(...),
) -> dict:
    topic = _validated_topic_or_404(track_id, area_id, topic_id)

    status = payload.get("status")
    if status not in {"Learning", "Done", "Review"}:
        raise HTTPException(status_code=400, detail="status must be one of: Learning, Done, Review")

    source_files = payload.get("source_files") or []
    if not isinstance(source_files, list):
        raise HTTPException(status_code=400, detail="source_files must be a list")
    _validate_source_files(source_files)

    requested_subtopics = payload.get("subtopics") or []
    if not isinstance(requested_subtopics, list):
        raise HTTPException(status_code=400, detail="subtopics must be a list")
    valid_lookup = {item.strip().lower(): item.strip() for item in topic.subtopics}
    invalid_subtopics: list[str] = []
    normalized_subtopics: list[str] = []
    for item in requested_subtopics:
        if not isinstance(item, str):
            invalid_subtopics.append(str(item))
            continue
        key = item.strip().lower()
        if key not in valid_lookup:
            invalid_subtopics.append(item)
        else:
            normalized_subtopics.append(valid_lookup[key])
    if invalid_subtopics:
        raise HTTPException(status_code=400, detail={"invalid_subtopics": invalid_subtopics})

    existing_content = read_existing_markdown(track_id, area_id, topic_id)
    mode = payload.get("mode")
    if existing_content is not None and mode not in {"append", "overwrite"}:
        raise HTTPException(status_code=400, detail="mode is required when the target markdown file already exists")

    target_path = markdown_path(track_id, area_id, topic_id)
    target_file = ROOT_DIR / target_path
    target_file.parent.mkdir(parents=True, exist_ok=True)

    mapped_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    new_section = render_markdown_section(source_files, normalized_subtopics, status, str(payload.get("note_text", "")), mapped_at)

    if existing_content is None:
        final_content = build_full_markdown(topic.name, [new_section])
    elif mode == "append":
        final_content = existing_content + "\n\n" + new_section
    elif mode == "overwrite":
        final_content = build_full_markdown(topic.name, [new_section])
    else:
        final_content = build_full_markdown(topic.name, [new_section])

    saved_files: list[str] = [target_path]
    # keep consistent with the Git commit semantics: source files are included as part of the saved payload
    saved_files.extend(source_files)
    if status == "Done":
        roadmap = load_roadmap()
        for track in roadmap.tracks:
            if track.id != track_id:
                continue
            for area in track.areas:
                if area.id != area_id:
                    continue
                for item in area.topics:
                    if item.id == topic_id:
                        item.done = True
                        break
        with ROADMAP_PATH.open("w", encoding="utf-8") as file:
            json.dump(roadmap.model_dump(mode="json"), file, indent=2)
            file.write("\n")
        saved_files.append("roadmap.json")

    target_file.write_text(final_content, encoding="utf-8")

    try:
        commit_sha = commit_and_push(saved_files, f"Add notes for {track_id}/{area_id}/{topic_id}")
        return {"saved_files": saved_files, "commit_sha": commit_sha}
    except GitOperationError as exc:
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "saved_files": saved_files},
        )
    except Exception as exc:  # pragma: no cover - runtime path for unexpected failures
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}") from exc


@app.post("/tracks/{track_id}/upload")
async def upload_files(track_id: str, files: list[UploadFile] = File(...)) -> dict:
    if not files:
        raise HTTPException(status_code=400, detail="At least one file is required")

    allowed = {".pdf", ".png", ".jpg", ".jpeg"}
    validated: list[tuple[str, bytes]] = []
    for file in files:
        suffix = "." + (file.filename or "").split(".")[-1].lower() if "." in (file.filename or "") else ""
        if suffix not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' has invalid extension. Allowed: {sorted(allowed)}",
            )
        validated.append((file.filename, await file.read()))

    saved_files: list[str] = []
    try:
        for filename, content in validated:
            rel_path = save_upload(track_id, filename, content)
            saved_files.append(rel_path)

        commit_sha = commit_and_push(saved_files, f"Add {len(saved_files)} file(s) to Inbox/{track_id}")
        return {"saved_files": saved_files, "commit_sha": commit_sha}
    except GitOperationError as exc:
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "saved_files": saved_files},
        )
    except Exception as exc:  # pragma: no cover - runtime path for push failure logging
        raise HTTPException(
            status_code=500,
            detail=f"Upload saved locally, but git commit/push failed: {exc}",
        ) from exc
