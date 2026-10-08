# Meeting Follow-up Agent

## Selected Assignment and Problem Definition
Assignment: Project Meeting Follow-up Agent.
The goal is to convert inconsistent meeting notes into a structured, reviewable follow-up package. 
Meetings produce decisions, actions, and questions, but notes are often messy. A language model might invent details if not constrained. This agent parses the notes into a structured format (JSON), distinguishes between confirmed and proposed items, extracts exact supporting text to prevent hallucination, and provides a CLI for human review and approval.

## Solution and Technology Choices
- **AI Integration**: `pydantic-ai` is used to define a unified AI agent. It seamlessly integrates structured output and custom tools (like `validate_person`, `validate_date`) without boilerplate. Gemini Flash is used via the Google Generative Language API.
- **Structured Data**: `pydantic` is used to enforce a strict JSON schema for the AI output (`MeetingSummary` model).
- **Human-in-the-Loop**: A simple Command Line Interface (CLI) is used to display the parsed summary and iterate through the actions. The user can Approve (a), Reject (r), or Modify (m) each action.
- **Storage**: Approved actions are appended to `data/approved_actions.json`.

## Setup and Execution Instructions
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up the environment variable `GEMINI_API_KEY` (e.g. in a `.env` file in the root folder):
   ```env
   GEMINI_API_KEY="your-api-key-here"
   ```
3. Run the application:
   ```bash
   python -m src.main data/test_case_2_ambiguous.txt
   ```
4. Run tests:
   ```bash
   python -m pytest tests/
   ```