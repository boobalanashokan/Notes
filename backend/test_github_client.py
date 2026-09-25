from github_client import GitHubRepoClient


class FakeBlob:
    def __init__(self, sha):
        self.sha = sha


class FakeTree:
    def __init__(self, sha):
        self.sha = sha


class FakeCommit:
    def __init__(self, sha):
        self.sha = sha
        self.commit = type("CommitMeta", (), {"tree": FakeTree("base-tree")})()


class FakeRef:
    def __init__(self):
        self.object = type("Object", (), {"sha": "abc123"})()

    def edit(self, sha):
        self.edited_sha = sha


class FakeRepo:
    def __init__(self):
        self.ref = FakeRef()

    def get_git_ref(self, _branch):
        return self.ref

    def get_commit(self, _sha):
        return FakeCommit("current-commit")

    def create_git_blob(self, content, encoding):
        return FakeBlob(f"blob-{encoding}-{len(content)}")

    def create_git_tree(self, items, base_tree=None):
        assert isinstance(items, list)
        assert all(item["path"] for item in items)
        return FakeTree("new-tree")

    def create_git_commit(self, message, tree, parents):
        assert message
        assert tree is not None
        assert len(parents) == 1
        return FakeCommit("new-commit")


def test_put_multiple_files_returns_commit_sha_only(monkeypatch):
    client = GitHubRepoClient.__new__(GitHubRepoClient)
    client.branch = "main"
    client._repo = FakeRepo()

    result = client.put_multiple_files(
        [
            {"path": "Notes/mlops/linux/filesystem-shell.md", "content": "# Notes\n", "is_binary": False},
            {"path": "roadmap.json", "content": '{"tracks": []}\n', "is_binary": False},
        ],
        "Add typed notes",
    )

    assert result == {"commit_sha": "new-commit"}
    assert isinstance(result, dict)
    assert set(result.keys()) == {"commit_sha"}
