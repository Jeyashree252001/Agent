# Design Reflection

### What needed to be learned?
Understanding how to force a large language model to strictly adhere to a schema while simultaneously preventing it from hallucinating missing data. Using Pydantic with Gemini's `response_schema` feature was crucial for ensuring robust data extraction.

### What was the most difficult design decision?
Balancing the complexity of the agent. The assignment suggested tools like "Date validator" and "Person validator". I decided to keep the architecture streamlined by enforcing strict LLM instructions and pushing the validation to the human-in-the-loop (HITL) review stage. Building complex multi-agent validation loops might be over-engineering for a prototype where a human must review it anyway.

### What assumptions were made?
- The user is running this in a terminal environment capable of interactive input.
- The user has a Google Gemini API key.
- The input meeting notes are not so large that they exceed the context window of the LLM (which is quite large for modern models anyway).

### What is most likely to fail?
The agent might still occasionally misclassify a "proposed decision" as a "confirmed decision" if the language in the notes is highly ambiguous. Furthermore, relative dates (like "next week") are extracted as strings rather than normalized timestamps, which could break downstream calendar integrations.

### How was behaviour verified?
By running the agent against specific synthetic test cases designed to trigger edge cases (ambiguity, contradictions, emptiness) and observing the CLI output. Automated tests were also written to verify the data models.

### What should change before production?
1. **Security**: Implement robust handling of PII and confidential data (potentially using a self-hosted LLM).
2. **UI/UX**: Replace the CLI with a web application or integrate directly into tools like Slack, Teams, or Notion.
3. **Integration**: Add concrete "Tools" (like an API call to Microsoft Graph or Google Workspace) to resolve relative dates and validate employee names against a real directory.

### When should a human be involved?
A human should *always* be involved before an action is saved, assigned to someone else, or committed to a system of record. The current design enforces this by requiring explicit approval (or modification) for every extracted action item.

### Would a non-agent solution have been sufficient?
No. Traditional NLP or regex-based extraction completely fails on unstructured, conversational meeting notes. Differentiating between "John proposed we do X" and "We agreed John will do X" requires the semantic understanding that only an LLM/agentic solution provides.
