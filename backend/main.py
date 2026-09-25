from __future__ import annotations

import json
import mimetypes
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from ai_service import generate_track_guidance
from github_client import GitHubRepoClient
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
VALID_ID_RE = re.compile(r"^[a-z0-9-]+$")

app = FastAPI(title="Study Tracker API")

allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_raw.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_repo_client() -> GitHubRepoClient:
    return GitHubRepoClient()


def _validated_topic_or_404(track_id: str, area_id: str, topic_id: str):
    topic = get_topic(track_id, area_id, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found in track '{track_id}' / area '{area_id}'")
    return topic


def _validate_source_files(source_files: list[str]) -> None:
    client = _get_repo_client()
    for source_file in source_files:
        if not isinstance(source_file, str):
            raise HTTPException(status_code=400, detail=f"Invalid source_file entry: {source_file!r}")
        normalized = source_file.strip("/")
        if not normalized.startswith("Inbox/"):
            raise HTTPException(status_code=400, detail=f"Source file not found under Inbox/: {source_file}")
        if client.get_file(normalized)[0] is None:
            raise HTTPException(status_code=400, detail=f"Source file not found under Inbox/: {source_file}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tracks", response_model=list[dict[str, str]])
def list_tracks() -> list[dict[str, str]]:
    roadmap = load_roadmap()
    return [{"id": track.id, "name": track.name} for track in roadmap.tracks]


@app.post("/tracks")
def create_track(payload: dict[str, Any] = Body(...)) -> dict:
    try:
        track = Track.model_validate(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc

    roadmap = load_roadmap()
    if any(existing.id == track.id for existing in roadmap.tracks):
        raise HTTPException(status_code=400, detail=f"Track id '{track.id}' already exists")

    invalid_ids: list[str] = []
    if not VALID_ID_RE.fullmatch(track.id):
        invalid_ids.append(f"track:{track.id}")

    for area in track.areas:
        if not VALID_ID_RE.fullmatch(area.id):
            invalid_ids.append(f"area:{area.id}")
        for topic in area.topics:
            if not VALID_ID_RE.fullmatch(topic.id):
                invalid_ids.append(f"topic:{topic.id}")

    if invalid_ids:
        raise HTTPException(status_code=400, detail={"invalid_ids": invalid_ids})

    all_topic_ids = {topic.id for area in track.areas for topic in area.topics}
    invalid_depends_on: list[str] = []
    for area in track.areas:
        for topic in area.topics:
            for dependency in topic.depends_on:
                if dependency not in all_topic_ids:
                    invalid_depends_on.append(dependency)
    if invalid_depends_on:
        raise HTTPException(status_code=400, detail={"invalid_depends_on": sorted(set(invalid_depends_on))})

    for area in track.areas:
        for topic in area.topics:
            topic.done = False

    saved_files = ["roadmap.json"]
    try:
        roadmap.tracks.append(track)
        updated_content = json.dumps(roadmap.model_dump(mode="json"), indent=2) + "\n"
        commit_result = _get_repo_client().put_multiple_files(
            [{"path": "roadmap.json", "content": updated_content, "is_binary": False}],
            f"Add new track: {track.name}",
        )
        return {"saved_files": saved_files, "commit_sha": commit_result["commit_sha"]}
    except Exception as exc:  # pragma: no cover - runtime path for unexpected failures
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "saved_files": saved_files},
        )


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


@app.get("/tracks/{track_id}/ai/coaching")
def get_track_ai_coaching(track_id: str) -> dict:
    track = get_track(track_id)
    if track is None:
        raise HTTPException(status_code=404, detail=f"Track '{track_id}' not found")

    stats = compute_track_stats(track)
    try:
        return generate_track_guidance(track, stats)
    except Exception:
        return {
            "summary": f"Your progress is still moving forward. Keep the next study session focused and consistent.",
            "focus_areas": [
                "Review the latest completed topic.",
                "Finish the next unfinished topic.",
                "Stay consistent with a small daily learning block.",
            ],
            "next_actions": [
                "Open the next item in your current track.",
                "Review the previous notes before starting the next lesson.",
                "Set a 20-minute study block and complete one focused task.",
            ],
        }


@app.get("/tracks/{track_id}/areas/{area_id}/topics/{topic_id}/note")
def get_topic_note(track_id: str, area_id: str, topic_id: str) -> dict:
    topic = _validated_topic_or_404(track_id, area_id, topic_id)
    file_path = markdown_path(track_id, area_id, topic_id)
    content = read_existing_markdown(track_id, area_id, topic_id)
    source_files = []
    if content:
        source_files = re.findall(r"^\- \[[^\]]+\]\(([^)]+)\)", content, flags=re.MULTILINE)
    return {
        "topic_name": topic.name,
        "target_path": file_path,
        "file_exists": content is not None,
        "content": content or "",
        "source_files": source_files,
    }


@app.get("/files")
def get_repo_file(path: str) -> Response:
    if not path:
        raise HTTPException(status_code=400, detail="A repo path is required")

    normalized = path.strip("/")
    if not normalized or not normalized.startswith(("Inbox/", "Notes/")):
        raise HTTPException(status_code=400, detail="Only Notes/ and Inbox/ files can be viewed inline")

    client = _get_repo_client()
    payload, _ = client.get_binary_file(normalized)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"File not found: {normalized}")

    media_type = mimetypes.guess_type(normalized)[0] or "application/octet-stream"
    filename = Path(normalized).name
    return Response(
        payload,
        media_type=media_type,
        headers={"Content-Disposition": f'inline; filename="{filename}"'},
    )


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
    saved_files.extend(source_files)
    commit_files: list[dict[str, Any]] = [{"path": target_path, "content": final_content, "is_binary": False}]

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
        roadmap_json = json.dumps(roadmap.model_dump(mode="json"), indent=2) + "\n"
        commit_files.append({"path": "roadmap.json", "content": roadmap_json, "is_binary": False})
        saved_files.append("roadmap.json")

    try:
        commit_result = _get_repo_client().put_multiple_files(commit_files, f"Add notes for {track_id}/{area_id}/{topic_id}")
        return {"saved_files": saved_files, "commit_sha": commit_result["commit_sha"]}
    except Exception as exc:  # pragma: no cover - runtime path for unexpected failures
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "saved_files": saved_files},
        )


@app.post("/tracks/{track_id}/upload")
async def upload_files(track_id: str, files: list[UploadFile] = File(...)) -> dict:
    if not files:
        raise HTTPException(status_code=400, detail="At least one file is required")

    allowed = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
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
    commit_files: list[dict[str, Any]] = []
    seen_batch_names: set[str] = set()
    try:
        for filename, content in validated:
            rel_path = save_upload(
                track_id,
                filename,
                content,
                _get_repo_client(),
                reserved_names=list(seen_batch_names),
            )
            saved_files.append(rel_path)
            commit_files.append({"path": rel_path, "content": content, "is_binary": True})
            seen_batch_names.add(Path(rel_path).name)

        commit_result = _get_repo_client().put_multiple_files(
            commit_files,
            f"Add {len(saved_files)} file(s) to Inbox/{track_id}",
        )
        return {"saved_files": saved_files, "commit_sha": commit_result["commit_sha"]}
    except Exception as exc:  # pragma: no cover - runtime path for push failure logging
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "saved_files": saved_files},
        )
