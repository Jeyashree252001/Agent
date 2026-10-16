import pytest
import datetime
from unittest.mock import MagicMock, patch
from src.agent import (
    validate_person,
    validate_date,
    search_fictional_project_info,
    get_current_date,
    MeetingAgent
)
from src.models import MeetingSummary, ActionItem, DecisionItem

def test_validate_person_valid():
    # Valid employees
    assert "is a valid employee" in validate_person("Alice")
    assert "is a valid employee" in validate_person("bob")
    assert "is a valid employee" in validate_person("CHARLIE")

def test_validate_person_invalid():
    # Unknown employee
    assert "not found in the employee directory" in validate_person("Zara")
    assert "not found in the employee directory" in validate_person("UnknownPerson")

def test_validate_date():
    result = validate_date("next Friday")
    assert "Validated Date: next Friday" in result

def test_search_fictional_project_info():
    result = search_fictional_project_info("cloud")
    assert "Azure" in result
    assert "External users are not currently allowed" in result

def test_get_current_date():
    today_str = datetime.date.today().isoformat()
    assert today_str in get_current_date()

def test_meeting_agent_process_notes_mocked():
    # Test agent integration with mocked LLM output
    mock_summary = MeetingSummary(
        topics=["Sprint Planning"],
        decisions=[DecisionItem(description="Use FastAPI", supporting_text="Agreed to use FastAPI", is_confirmed=True)],
        actions=[ActionItem(description="Setup repo", supporting_text="Alice will setup repo", owner="Alice", deadline="Tomorrow", is_confirmed=True)],
        open_questions=[],
        risks_and_concerns=[],
        missing_or_unclear_information=[],
        summary="Sprint planning summary"
    )

    with patch("src.agent.Config.validate"), \
         patch("src.agent.agent.run_sync") as mock_run_sync:
        mock_run_sync.return_value = MagicMock(output=mock_summary)
        
        meeting_agent = MeetingAgent()
        result = meeting_agent.process_notes("Mock notes")
        
        assert result.summary == "Sprint planning summary"
        assert len(result.actions) == 1
        assert result.actions[0].owner == "Alice"
        mock_run_sync.assert_called_once_with("Mock notes")
