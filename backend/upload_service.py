from __future__ import annotations

import os
from datetime import date
from pathlib import Path
from typing import List

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _next_available_path(dest_dir: Path, filename: str) -> Path:
    if not dest_dir.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)

    stem = Path(filename).stem
    suffix = Path(filename).suffix.lower()
    candidate = dest_dir / filename
    counter = 2
    while candidate.exists():
        candidate = dest_dir / f"{stem}-{counter}{suffix}"
        counter += 1
    return candidate


def save_upload(track_id: str, filename: str, content: bytes) -> str:
    if not filename:
        raise ValueError("Filename is required")

    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {filename}")

    repo_root = _repo_root()
    day = date.today().strftime("%Y-%m-%d")
    target_dir = repo_root / "Inbox" / track_id / day
    target_dir.mkdir(parents=True, exist_ok=True)

    final_path = _next_available_path(target_dir, filename)
    final_path.write_bytes(content)
    return str(final_path.relative_to(repo_root)).replace("\\", "/")
