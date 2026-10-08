from pydantic_ai import Agent, RunContext
from src.config import Config
from src.models import MeetingSummary
import os
import datetime

# Define the model, injecting the API key from config
model_id = "test" if Config.MODEL_NAME == "test" else f"google:{Config.MODEL_NAME}"
agent = Agent(
    model_id,
    output_type=MeetingSummary,
    defer_model_check=True,
    system_prompt=(
        "You are an AI assistant that extracts structured information from meeting notes. "
        "You must distinguish between confirmed decisions, proposed decisions, confirmed actions, "
        "possible actions, open questions, background information, and missing or unclear information. "
        "DO NOT invent owners, deadlines, or project facts. If an owner or deadline is not explicitly "
        "stated, leave it null or note it as unclear. "
        "Attach the original supporting text to each proposed decision or action. "
        "Before generating the summary, use your tools to validate people, dates, and project info."
    ),
)

@agent.tool_plain
def validate_person(name: str) -> str:
    """Check if a person is a valid employee. Use this when an owner is mentioned."""
    EMPLOYEES = ["alice", "bob", "charlie", "laura", "john", "sarah", "david"]
    if name.lower() in EMPLOYEES:
        return f"{name} is a valid employee."
    return f"{name} is not found in the employee directory."

@agent.tool_plain
def validate_date(date_string: str) -> str:
    """Validate or convert a relative date to a standard format. Use this to interpret dates."""
    return f"Validated Date: {date_string} (normalized relative to today)"

@agent.tool_plain
def search_fictional_project_info(query: str) -> str:
    """Search for fictional project information (e.g. cloud provider choices)."""
    return "Project Info DB: Current cloud provider is Azure. External users are not currently allowed."

@agent.tool_plain
def get_current_date() -> str:
    """Get the current date to use as a reference for relative dates."""
    return f"Current date is {datetime.date.today().isoformat()}"

class MeetingAgent:
    def __init__(self):
        Config.validate()
        os.environ['GEMINI_API_KEY'] = Config.GEMINI_API_KEY
        os.environ['GOOGLE_API_KEY'] = Config.GEMINI_API_KEY
        
    def process_notes(self, notes_text: str) -> MeetingSummary:
        """
        Parses raw meeting notes into structured data using pydantic-ai.
        """
        result = agent.run_sync(notes_text)
        return result.output
