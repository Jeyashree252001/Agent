import pytest
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
