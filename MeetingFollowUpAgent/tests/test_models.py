import pytest
from pydantic import ValidationError
from src.models import MeetingSummary, ActionItem, DecisionItem

def test_meeting_summary_model():
    # Test valid creation
    summary = MeetingSummary(
        topics=["Test Topic"],
        decisions=[DecisionItem(description="Test Decision", supporting_text="Text", is_confirmed=True)],
        actions=[ActionItem(description="Test Action", supporting_text="Text", owner="Alice", deadline="Tomorrow", is_confirmed=True)],
        open_questions=["What is next?"],
        risks_and_concerns=[],
        missing_or_unclear_information=[],
        summary="A brief summary"
    )
    assert len(summary.topics) == 1
    assert summary.topics[0] == "Test Topic"
    assert summary.decisions[0].is_confirmed is True
    assert summary.actions[0].owner == "Alice"

def test_action_item_model_defaults():
    action = ActionItem(description="Task", supporting_text="Do task", is_confirmed=False)
    assert action.owner is None
    assert action.deadline is None
    assert action.is_confirmed is False

def test_meeting_summary_defaults():
    # Only required fields provided: topics and summary
    summary = MeetingSummary(topics=["Single Topic"], summary="Quick Summary")
    assert summary.decisions == []
    assert summary.actions == []
    assert summary.open_questions == []
    assert summary.risks_and_concerns == []
    assert summary.missing_or_unclear_information == []

def test_action_item_missing_required_fields():
    # Missing supporting_text and is_confirmed
    with pytest.raises(ValidationError) as exc_info:
        ActionItem(description="Task without supporting text or confirmation")
    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "supporting_text" in missing_fields
    assert "is_confirmed" in missing_fields

def test_decision_item_missing_required_fields():
    # Missing is_confirmed and supporting_text
    with pytest.raises(ValidationError) as exc_info:
        DecisionItem(description="Adopt PostgreSQL")
    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "supporting_text" in missing_fields
    assert "is_confirmed" in missing_fields

def test_meeting_summary_missing_required_fields():
    # Missing summary and topics
    with pytest.raises(ValidationError) as exc_info:
        MeetingSummary()
    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "summary" in missing_fields
    assert "topics" in missing_fields

def test_model_invalid_types():
    # Invalid description type (list instead of string)
    with pytest.raises(ValidationError):
        ActionItem(
            description=["Should", "be", "a", "string"],  # type: ignore
            supporting_text="Excerpt",
            is_confirmed=True
        )

    # Invalid boolean type
    with pytest.raises(ValidationError):
        ActionItem(
            description="Fix login bug",
            supporting_text="Excerpt",
            is_confirmed="not_a_valid_boolean"  # type: ignore
        )

    # Invalid actions list type (passing string instead of list of ActionItem)
    with pytest.raises(ValidationError):
        MeetingSummary(
            topics=["Topic"],
            actions="invalid_actions_list",  # type: ignore
            summary="Summary"
        )

