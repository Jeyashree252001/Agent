import json
import pytest
from unittest.mock import patch, MagicMock
from src.main import main
from src.models import MeetingSummary, ActionItem, DecisionItem

def test_workflow_end_to_end(tmp_path, monkeypatch):
    # Setup test meeting notes file
    notes_file = tmp_path / "notes.txt"
    notes_file.write_text("Alice will prepare the presentation by Friday.", encoding="utf-8")

    # Output file
    output_file = tmp_path / "approved_actions.json"
    monkeypatch.setattr("src.cli.Config.OUTPUT_FILE", str(output_file))
    monkeypatch.setattr("src.cli.Config.DATA_DIR", str(tmp_path))

    # Mocked LLM summary output
    mock_summary = MeetingSummary(
        topics=["Project Kickoff"],
        decisions=[DecisionItem(description="Kickoff project", supporting_text="Agreed to kickoff", is_confirmed=True)],
        actions=[ActionItem(description="Prepare presentation", supporting_text="Alice will prepare", owner="Alice", deadline="Friday", is_confirmed=True)],
        open_questions=[],
        risks_and_concerns=[],
        missing_or_unclear_information=[],
        summary="Kickoff summary"
    )

    # Patch sys.argv, agent process_notes, and CLI input ('a' for approve)
    with patch("sys.argv", ["main.py", str(notes_file)]), \
         patch("src.main.MeetingAgent.process_notes", return_value=mock_summary), \
         patch("builtins.input", return_value="a"):
        main()

    # Verify output JSON was created and saved
    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["owner"] == "Alice"
    assert data[0]["description"] == "Prepare presentation"
