import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_compare(monkeypatch):
    # Stub out the OpenAI call
    def fake_create(*args, **kwargs):
        class Choice:
            message = type("M", (), {"content": "- Acquire Docker\n- Study AWS"})
        return type("R", (), {"choices": [Choice()]})
    monkeypatch.setattr("app.llm.openai.ChatCompletion.create", fake_create)

    payload = {
        "resume": {"skills": ["Python"]},
        "jd": {"text": "Need Python and Docker expertise."}
    }
    r = client.post("/compare", json=payload)
    assert r.status_code == 200
    assert "Acquire Docker" in r.json()["roadmap"]
