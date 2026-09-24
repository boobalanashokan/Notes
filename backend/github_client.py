from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any, Iterable

from dotenv import load_dotenv
from github import Github
from github.GithubException import GithubException

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


class GitHubRepoClient:
    def __init__(self, token: str | None = None, repo_name: str | None = None):
        self.token = (token or _require_env("GITHUB_TOKEN")).strip()
        repo_value = (repo_name or os.getenv("GITHUB_REPO", "")).strip()
        if not repo_value or "/" not in repo_value:
            raise ValueError("GITHUB_REPO must be set to 'owner/repo-name'")
        self.repo_name = repo_value
        self._github = Github(self.token)
        self._repo = self._github.get_repo(self.repo_name)
        self.branch = self._repo.default_branch

    @property
    def repo(self):
        return self._repo

    def get_file(self, path: str) -> tuple[str | None, str | None]:
        try:
            item = self._repo.get_contents(path)
        except GithubException as exc:
            if exc.status == 404:
                return None, None
            raise

        if isinstance(item, list):
            return None, None

        content = item.content or ""
        payload = base64.b64decode(content.encode("utf-8")) if content else b""
        return payload.decode("utf-8"), item.sha

    def get_binary_file(self, path: str) -> tuple[bytes | None, str | None]:
        try:
            item = self._repo.get_contents(path)
        except GithubException as exc:
            if exc.status == 404:
                return None, None
            raise

        if isinstance(item, list):
            return None, None

        content = item.content or ""
        payload = base64.b64decode(content.encode("utf-8")) if content else b""
        return payload, item.sha

    def put_file(self, path: str, content: str | bytes, message: str, sha: str | None = None) -> dict[str, Any]:
        if sha is None:
            try:
                self._repo.get_contents(path)
            except GithubException as exc:
                if exc.status == 404:
                    return self._repo.create_file(path, message, content, branch=self.branch)
                raise
            raise ValueError(f"sha is required when updating '{path}'")

        return self._repo.update_file(path, message, content, sha=sha, branch=self.branch)

    def put_multiple_files(self, files: list[dict[str, Any]], message: str) -> dict[str, Any]:
        if not files:
            raise ValueError("No files provided for commit")

        ref = self._repo.get_git_ref(f"heads/{self.branch}")
        current_commit = self._repo.get_commit(ref.object.sha)
        tree_items: list[dict[str, str]] = []

        for file_item in files:
            path = str(file_item["path"]).strip("/")
            content = file_item["content"]
            is_binary = bool(file_item.get("is_binary", False))

            if isinstance(content, str):
                text = content
                blob_content = text
                if is_binary:
                    blob_content = base64.b64encode(content.encode("utf-8")).decode("ascii")
                    blob_encoding = "base64"
                else:
                    blob_encoding = "utf-8"
            else:
                payload = content if isinstance(content, bytes) else bytes(content)
                blob_content = base64.b64encode(payload).decode("ascii") if is_binary else payload.decode("utf-8")
                blob_encoding = "base64" if is_binary else "utf-8"

            blob = self._repo.create_git_blob(blob_content, blob_encoding)
            tree_items.append({
                "path": path,
                "mode": "100644",
                "type": "blob",
                "sha": blob.sha,
            })

        new_tree = self._repo.create_git_tree(tree_items, base_tree=current_commit.tree)
        new_commit = self._repo.create_git_commit(message, new_tree, [current_commit])
        ref.edit(sha=new_commit.sha)
        return {"commit_sha": new_commit.sha}

    def list_directory(self, path: str) -> list[str]:
        normalized = path.strip("/")
        try:
            entries = self._repo.get_contents(normalized) if normalized else self._repo.get_contents("")
        except GithubException as exc:
            if exc.status == 404:
                return []
            raise

        if not isinstance(entries, list):
            return []
        return [entry.name for entry in entries]
