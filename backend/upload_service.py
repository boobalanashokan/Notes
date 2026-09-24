from __future__ import annotations

from datetime import date
from pathlib import Path

from github_client import GitHubRepoClient

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def _next_available_path(target_dir: str, filename: str, existing_names: list[str]) -> str:
    stem = Path(filename).stem
    suffix = Path(filename).suffix.lower()
    candidate = filename
    counter = 2
    while candidate in existing_names:
        candidate = f"{stem}-{counter}{suffix}"
        counter += 1
    return f"{target_dir}/{candidate}"


def save_upload(track_id: str, filename: str, content: bytes, client: GitHubRepoClient | None = None) -> str:
    if not filename:
        raise ValueError("Filename is required")

    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {filename}")

    client = client or GitHubRepoClient()
    day = date.today().strftime("%Y-%m-%d")
    target_dir = f"Inbox/{track_id}/{day}"
    existing_names = client.list_directory(target_dir)
    return _next_available_path(target_dir, filename, existing_names)
