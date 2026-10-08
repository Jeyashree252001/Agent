# Working Demonstration

## 1. Successful Interaction
**Input**: `data/test_case_1_clear.txt`
**Flow**: The agent accurately extracts the topics (Q3 Sales Report, New Marketing Campaign), confirmed decisions, and the three distinct actions.
**Interaction**: The user sees all three actions clearly mapped to Alice, Bob, and Charlie with their respective deadlines. The user presses `a` for all three, and they are saved to `approved_actions.json`.

## 2. Ambiguous or Incomplete Interaction
**Input**: `data/test_case_2_ambiguous.txt` (The assignment's example scenario)
**Flow**: The agent identifies:
- Testing the reporting view as a proposed decision/action.
- Preparing example project data as an action with *no owner* (Unassigned).
- External user access as an open question.
**Interaction**: When reviewing the action "Prepare example project data", the user sees Owner: Unassigned. The user presses `m` to modify, enters "Laura" as the owner, and presses enter. The modified action is approved.

## 3. Failure Scenario
**Input**: Running the script without `GEMINI_API_KEY` set.
**Flow**: The application immediately raises a `ValueError` during initialization, preventing any malformed requests from being sent to the API. 
Another failure scenario is providing a non-existent file path:
**Flow**: `python -m src.main invalid_file.txt`. The application gracefully catches the `FileNotFoundError` and outputs: `Error: File 'invalid_file.txt' not found.` before exiting.

## Agent Decision Flow and Possible Improvements
**Flow**: 
1. System reads raw text.
2. Agent injects system instructions ("do not hallucinate, extract supporting text") and requests JSON conforming to the schema.
3. LLM returns JSON. Pydantic validates it.
4. CLI iterates over the items.

**Improvements**:
- **Date Normalization**: A future improvement would be adding a "Date Validator" tool or sub-agent that converts relative dates ("next month") into ISO-8601 dates based on the meeting date.
- **RAG for Role Validation**: Implement a check against a team database to ensure assigned owners are actual team members.
