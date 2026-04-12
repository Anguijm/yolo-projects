# Council Escalation — experiments/adopt-planning-mode

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-12T05:32:50.910088+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The refined planning instructions, especially the explicit 'N/A' guidance for the Function Map, significantly improve the clarity and completeness of the plan artifact, reducing ambiguity and the risk of downstream implementation errors or parsing failures for various project types.

### SECURITY — APPROVE (low)
- **Reason:** The changes introduce a mandatory '## Security' section in the planning phase, requiring explicit consideration of threat models, CSP notes, and trust boundaries, which is a significant improvement for proactive security identification.

### UI — APPROVE (low)
- **Reason:** The updated planning instructions provide significantly clearer guidance, explicitly requiring UI and Guide sections, which ensures user experience considerations are addressed early in the development process.

### GUIDE — OBJECT (high)
- **Reason:** The instruction 'Use structured planning mode' does not explain how an AI agent should invoke or engage this 'mode', leaving it unclear how to act on the directive.
- **Required fix:** Clarify what 'structured planning mode' means for an AI agent; if it's a specific tool/API call, provide the command; if it's a descriptive label for the output format, rephrase the instruction to reflect that (e.g., 'Generate your plan in a structured format, adhering to the following sections').
- **Evidence:** `.github/workflows/tick_tock_prompt.md:lines ~74-100 and ~157 (specifically the phrase 'Use **structured planning mode**')`

### USEFULNESS — APPROVE (low)
- **Reason:** Structured planning significantly improves the utility and reviewability of AI-generated plans, addressing critical gaps in completeness and consistency.
- **Evidence:** `The explicit requirement for sections like 'Function Map', 'Security', 'UI', and 'Edge Cases' ensures that plans cover essential aspects often overlooked, making them more useful for human reviewers and reducing downstream issues.`

### COOL — APPROVE (low)
- **Reason:** The explicit 'Function Map' and granular enumeration of files/functions, along with detailed subtasks and dependencies, creates a unique, highly structured planning artifact from the AI, serving as a signature move for the internal development process.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

**RESOLVED 2026-04-10 by John (interactive session).**

GUIDE objection ACCEPTED. Rephrased "Use structured planning mode" to "Write your plan to ... using the following structured format." Applied the implementation directly to tick_tock_prompt.md (both main PLAN gate and infrastructure PLAN gate). Council should proceed to TESTS gate.
