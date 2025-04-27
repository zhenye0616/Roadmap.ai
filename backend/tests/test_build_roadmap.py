import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
import pytest
from app.roadmap_agnt import build_roadmap


class DummyPages:
    def __init__(self):
        self.created = []
    def create(self, **kwargs):
        self.created.append(kwargs)


@pytest.fixture(autouse=True)
def dummy_notion(monkeypatch):
    from notion_client import Client
    dummy = DummyPages()
    # Patch Client so build_roadmap(Client(...).pages.create) uses our dummy
    monkeypatch.setattr("app.notion_client.Client", lambda **kw: type("X",(),{"pages": dummy})())
    os.environ["NOTION_ROADMAPS_DB_ID"] = "test-db-id"
    return dummy


def test_build_roadmap_creates_one_page_per_entry(dummy_notion):
    fake_map = {
        "roadmap": [
            {"skill": "Kubernetes", "steps": ["Intro","Hands-on"]},
            {"skill": "Terraform",  "steps": ["Setup","Deploy"]},
        ]
    }

    build_roadmap(fake_map)

    # Expect two calls to pages.create
    assert len(dummy_notion.created) == 2
    # Verify the DB id and a property
    first = dummy_notion.created[0]
    assert first["parent"]["database_id"] == "test-db-id"
    assert first["properties"]["Skill"]["select"]["name"] == "Kubernetes"
