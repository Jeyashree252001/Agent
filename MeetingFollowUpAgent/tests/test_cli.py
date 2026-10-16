import json
import pytest
from unittest.mock import patch
from src.cli import CLI
from src.models import ActionItem, MeetingSummary, DecisionItem

@pytest.fixture
def sample_action():
    return ActionItem(
        description="Write unit tests",
        supporting_text="Bob will write unit tests by Friday",
        owner="Bob",
        deadline="Friday",
        is_confirmed=True
    )

def test_cli_display_summary(capsys):
    cli = CLI()
    summary = MeetingSummary(
        topics=["Architecture"],
        decisions=[DecisionItem(description="Use Microservices", supporting_text="Decided on microservices", is_confirmed=True)],
        actions=[ActionItem(description="Draft diagram", supporting_text="Alice will draft", is_confirmed=False)],
        open_questions=["What is the SLA?"],
        risks_and_concerns=["Tight deadline"],
        missing_or_unclear_information=["Database credentials"],
        summary="Architecture review summary"
    )
    cli.display_summary(summary)
    captured = capsys.readouterr().out
    assert "MEETING SUMMARY" in captured
    assert "Architecture" in captured
    assert "Use Microservices" in captured
    assert "What is the SLA?" in captured
    assert "Tight deadline" in captured

def test_review_actions_approve(sample_action):
    cli = CLI()
    with patch("builtins.input", return_value="a"):
        approved = cli.review_actions([sample_action])
    assert len(approved) == 1
    assert approved[0]["description"] == "Write unit tests"
    assert approved[0]["owner"] == "Bob"

def test_review_actions_reject(sample_action):
    cli = CLI()
    with patch("builtins.input", return_value="r"):
        approved = cli.review_actions([sample_action])
    assert len(approved) == 0

def test_review_actions_modify(sample_action):
    cli = CLI()
    # Mock inputs: 'm' for choice, then new description, new owner, new deadline
    inputs = iter(["m", "Updated description", "Charlie", "Monday"])
    with patch("builtins.input", side_effect=lambda _: next(inputs)):
        approved = cli.review_actions([sample_action])
    assert len(approved) == 1
    assert approved[0]["description"] == "Updated description"
    assert approved[0]["owner"] == "Charlie"
    assert approved[0]["deadline"] == "Monday"
    assert approved[0]["is_confirmed"] is True

def test_save_actions(tmp_path, monkeypatch, sample_action):
    cli = CLI()
    output_file = tmp_path / "approved_actions.json"
    monkeypatch.setattr("src.cli.Config.OUTPUT_FILE", str(output_file))
    monkeypatch.setattr("src.cli.Config.DATA_DIR", str(tmp_path))

    actions_to_save = [sample_action.model_dump()]
    cli.save_actions(actions_to_save)

    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["description"] == "Write unit tests"
