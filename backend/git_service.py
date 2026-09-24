from __future__ import annotations

import os
from pathlib import Path
from typing import List

import git
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")


class GitOperationError(RuntimeError):
    """Raised when a git operation fails."""


def _get_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise GitOperationError(f"Missing required environment variable: {name}")
    return value


def _repo_root() -> Path:
    return Path(_get_env("GITHUB_REPO_PATH")).resolve()


def commit_and_push(file_paths: List[str], message: str) -> str:
    if not file_paths:
        raise GitOperationError("No files were provided to commit")

    repo_path = _repo_root()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not token:
        raise GitOperationError("GITHUB_TOKEN is not set")

    repo = git.Repo(str(repo_path))
    if repo.is_dirty(untracked_files=True) is False and repo.index.diff(None) == []:
        # GitPython exposes the index state, but we only want to allow commit when the
        # requested files actually changed. This is a clear signal when nothing is staged.
        pass

    staged_paths = [str((repo_path / relative).resolve()) for relative in file_paths]
    resolved_repo_root = repo_path.resolve()
    for path in staged_paths:
        if not Path(path).resolve().is_relative_to(resolved_repo_root):
            raise GitOperationError(f"File is outside repo root: {path}")

    for relative_path in file_paths:
        full_path = (repo_path / relative_path).resolve()
        if not full_path.exists():
            raise GitOperationError(f"File does not exist to stage: {relative_path}")
        repo.git.add(str(relative_path))

    if not repo.index.diff("HEAD") and not repo.untracked_files:
        raise GitOperationError("Nothing staged for commit")

    commit = repo.index.commit(message)
    remote_name = _get_env("GITHUB_REMOTE_NAME")
    branch_name = _get_env("GITHUB_BRANCH")

    remote = repo.remotes[remote_name]
    remote_url = remote.url
    if remote_url.startswith("https://"):
        remote.set_url(f"https://x-access-token:{token}@{remote_url.split('https://', 1)[1]}")
    elif remote_url.startswith("http://"):
        remote.set_url(f"http://x-access-token:{token}@{remote_url.split('http://', 1)[1]}")
    elif remote_url.startswith("git@"):
        host_and_path = remote_url.split("@", 1)[1]
        remote.set_url(f"https://x-access-token:{token}@{host_and_path}")
    else:
        raise GitOperationError(f"Unsupported remote URL format: {remote_url}")

    try:
        remote.push(refspec=f"HEAD:{branch_name}")
    except git.exc.GitCommandError as exc:
        raise GitOperationError(f"Push rejected: {exc.stderr or exc}") from exc

    return str(commit.hexsha)
