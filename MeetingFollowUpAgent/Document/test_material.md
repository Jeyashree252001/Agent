# Test Material

## Synthetic Input Data
The synthetic data is located in the `data/` directory.

## Test Cases

### 1. `test_case_1_clear.txt`
- **Rationale**: Establishes the baseline. Can the agent extract well-structured, explicit information accurately?
- **Expected Behavior**: Extracts 3 confirmed actions, 2 confirmed decisions, maps owners and deadlines correctly.

### 2. `test_case_2_ambiguous.txt` (From Assignment)
- **Rationale**: Tests the agent's ability to handle missing owners, distinguish between proposed and confirmed items, and identify open questions without hallucinating answers.
- **Expected Behavior**: "Prepare example data" is extracted as an action with `null` owner. "External users access" is extracted as an open question.

### 3. `test_case_3_contradictory.txt`
- **Rationale**: Tests how the agent handles conflicting statements within the same meeting.
- **Expected Behavior**: The database migration ownership and timeline, as well as the cloud provider decision, should be flagged in `missing_or_unclear_information` or `risks_and_concerns`. Actions might be flagged as proposed/unconfirmed due to the dispute.

### 4. `test_case_4_short.txt`
- **Rationale**: Tests edge cases where no actions or decisions are present.
- **Expected Behavior**: The agent should return empty lists for actions and decisions and not invent any filler content.

### 5. Automated Unit Tests (`tests/test_models.py`)
- **Rationale**: Validates the structural integrity of the application independently of the LLM.
- **Expected Behavior**: `pytest` passes, confirming that Pydantic models correctly initialize, enforce types, and apply default values (like `None` for unassigned owners).

## Test-Running Instructions
To run manual tests against the agent:
```bash
python -m src.main data/test_case_1_clear.txt
python -m src.main data/test_case_2_ambiguous.txt
```
To run automated unit tests:
```bash
python -m pytest tests/
```
