import re
import spacy
import pytest
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from backend.app.parse_resume import parse_resume_text

@pytest.fixture(autouse=True)
def disable_spacy_warnings(monkeypatch):
    # suppress any lazy‐loading warnings from spaCy
    monkeypatch.setattr("spacy.load", lambda *args, **kwargs: spacy.blank("en"))

def test_parse_basic_fields():
    text = """
    John A. Doe
    Email: john.doe@example.com
    Phone: (123) 456-7890

    Worked as a Software Engineer at OpenAI.
    Key skills: Python, SQL, Docker.
    """

    result = parse_resume_text(text)

    # emails
    assert result["emails"] == ["john.doe@example.com"]

    # phones (might normalize differently)
    assert re.sub(r"\D", "", result["phones"][0]) == "1234567890"

    # names & organizations
    assert "John A. Doe" in result["names"]
    assert "OpenAI" in result["organizations"]

    # skills heuristic should pick up proper nouns
    skills = " ".join(result["skills"])
    assert "Python" in skills
    assert "Docker" in skills

def test_parse_no_contacts_or_orgs():
    text = "Just some random text without emails or phones."
    result = parse_resume_text(text)
    assert result["emails"] == []
    assert result["phones"] == []
    assert result["names"] == []
    assert result["organizations"] == []
