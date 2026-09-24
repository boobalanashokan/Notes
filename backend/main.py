from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from git_service import commit_and_push
from models import Track
from roadmap_service import compute_track_stats, get_track, load_roadmap
from upload_service import save_upload

app = FastAPI(title="Study Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    except Exception as exc:  # pragma: no cover - runtime path for push failure logging
        raise HTTPException(
            status_code=500,
            detail=f"Upload saved locally, but git commit/push failed: {exc}",
        ) from exc
