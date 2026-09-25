from fastapi.testclient import TestClient

from main import app


def test_topic_note_endpoint_returns_existing_markdown(monkeypatch):
    class FakeTopic:
        name = "Filesystem & shell"
        subtopics = ["pwd / ls / cd"]

    def fake_get_file(path: str):
        assert path == "Notes/mlops/linux/filesystem-shell.md"
        return "# Filesystem & shell\n\nStatus: Done\n", "sha-123"

    monkeypatch.setattr("main.read_existing_markdown", lambda *args, **kwargs: "# Filesystem & shell\n\nStatus: Done\n")
    monkeypatch.setattr("main.get_topic", lambda *args, **kwargs: FakeTopic())

    client = TestClient(app)
    response = client.get("/tracks/mlops/areas/linux/topics/filesystem-shell/note")

    assert response.status_code == 200
    payload = response.json()
    assert payload["file_exists"] is True
    assert "# Filesystem & shell" in payload["content"]
    assert payload["target_path"] == "Notes/mlops/linux/filesystem-shell.md"
