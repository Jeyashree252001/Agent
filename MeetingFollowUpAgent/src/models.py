from typing import List, Optional
from pydantic import BaseModel, Field

class BaseItem(BaseModel):
    description: str = Field(description="Description of the item")
    supporting_text: str = Field(description="Exact excerpt from the meeting notes supporting this item")

class ActionItem(BaseItem):
    owner: Optional[str] = Field(default=None, description="Assigned owner, if explicitly mentioned")
    deadline: Optional[str] = Field(default=None, description="Deadline, if explicitly mentioned")
    is_confirmed: bool = Field(description="True if confirmed, False if proposed/possible")

class DecisionItem(BaseItem):
    is_confirmed: bool = Field(description="True if agreed upon, False if only proposed")

class MeetingSummary(BaseModel):
    topics: List[str] = Field(description="Main topics discussed")
    decisions: List[DecisionItem] = Field(default_factory=list, description="Decisions made or proposed")
    actions: List[ActionItem] = Field(default_factory=list, description="Actions assigned or proposed")
    open_questions: List[str] = Field(default_factory=list, description="Unresolved questions")
    risks_and_concerns: List[str] = Field(default_factory=list, description="Risks or concerns raised")
    missing_or_unclear_information: List[str] = Field(default_factory=list, description="Information that is uncertain or requires clarification")
    summary: str = Field(description="A brief, readable summary of the meeting")
