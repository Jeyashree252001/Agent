# Architecture Description

## Overview
The system follows a simple pipeline architecture with a Human-in-the-Loop (HITL) step at the end.

## Components
1. **User Interaction (CLI)**: 
   - Takes a file path as input.
   - Displays the parsed Meeting Summary to the user.
   - Prompts the user to review each extracted Action Item.
2. **Agent Module (`agent.py`)**: 
   - Responsible for communicating with the LLM via `pydantic-ai`. 
   - Defines a single PydanticAI Agent with `result_type=MeetingSummary`.
   - Injects 4 simple tools (`validate_person`, `validate_date`, `search_fictional_project_info`, `get_current_date`) to help the agent validate context before forming the final structured JSON.
3. **Model (LLM)**: 
   - Google Gemini (e.g., `gemini-3.8-flash`). It is provided with strict system instructions to not invent owners/deadlines and to attach supporting text.
4. **Data Models (`models.py`)**: 
   - Defines `MeetingSummary`, `ActionItem`, and `DecisionItem` using Pydantic.
5. **Stored Outputs**: 
   - Approved actions are saved to `data/approved_actions.json`.

## Human Approval Points
The critical approval point happens after the AI has processed the text but *before* anything is saved.
- The user is presented with each action one by one.
- The user sees: The description, proposed owner, proposed deadline, and the *exact supporting text* from the notes.
- The user can input:
  - `a`: Approve the action as-is.
  - `r`: Reject the action (it is discarded).
  - `m`: Modify the action (change description, owner, or deadline) and approve the modified version.

## Diagram
```text
[Meeting Notes (Text/MD)] 
       |
       v
[PydanticAI Agent] <---> [Tools: validate_person, validate_date, search_info, get_date]
       |
       v
[Pydantic Models (MeetingSummary)]
       |
       v
[CLI Display Summary]
       |
       v
[CLI Review Actions Loop (Human Approval Point)]
       |--- Reject ---> (Discarded)
       |--- Approve / Modify ---> [Save to approved_actions.json]
```
