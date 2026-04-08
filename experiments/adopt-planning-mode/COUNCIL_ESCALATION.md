# Council Escalation — experiments/adopt-planning-mode

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-08T22:29:30.631890+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The change is limited to a prompt instruction for an AI agent, and the generated output is explicitly stated to be for human review only, with no automated parsing or execution, thus eliminating systemic correctness risks.
- **Evidence:** `Security section: 'It is NOT parsed or executed programmatically — no automated system consumes the file paths or function names listed in it.'`

### SECURITY — OBJECT (medium)
- **Reason:** The plan explicitly states that no sanitization or validation is needed for the AI's output (`plan.md`) because it is only read by humans. This creates a trust boundary violation, as the AI's output is an untrusted input that could contain malicious or misleading content (e.g., XSS payloads, dangerous file paths) which, even if not programmatically executed today, could be misinterpreted by humans or exploited if future systems parse the output.
- **Required fix:** Modify `.github/workflows/tick_tock_prompt.md` to instruct the AI to sanitize file paths and function names in the generated plan, ensuring they adhere to a safe character set and do not contain executable code or dangerous path traversals.
- **Evidence:** `Security section of `experiments/adopt-planning-mode/plan.md`: 'No sanitization or validation is needed for the plan artifact itself because it is read by humans, not executed by scripts.'`

### UI — APPROVE (low)
- **Reason:** The proposed changes improve the clarity, structure, and reviewability of the AI-generated plan document, which directly benefits the human reviewer's experience.

### GUIDE — APPROVE (low)
- **Reason:** The proposed changes to the prompt significantly enhance the discoverability and self-documentation of the planning process for both AI agents and human reviewers by providing explicit, structured instructions and a clear output format.

### USEFULNESS — APPROVE (low)
- **Reason:** This project significantly improves the utility and verifiability of AI-generated plans for human reviewers, addressing a clear need for structured information before code is written.
- **Evidence:** `The explicit requirement for a 'Function Map' and detailed file/function targets in the plan directly solves the problem of vague or incomplete AI plans, making human review more efficient and robust, similar to how a well-structured architectural design document aids human engineers.`

### COOL — APPROVE (low)
- **Reason:** This introduces a signature planning structure for AI agents, making their pre-code output uniquely verifiable and actionable for human review.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

Human decision required. Resume the build after updating session_state.json.
