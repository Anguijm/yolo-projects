# Council Escalation — experiments/fix-council-bugs-hallucination

**Gate:** outcome
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T23:35:07.032574+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** 

### SECURITY — APPROVE (low)
- **Reason:** Existing security mitigations (regex escaping, path traversal guard, file size limit, bounded quantifiers) adequately cover potential attack surfaces introduced by text processing and file I/O.

### UI — APPROVE (low)
- **Reason:** The change improves the user experience by reducing false-positive BUGS objections and provides clear feedback when an objection is auto-downgraded.

### GUIDE — OBJECT (medium)
- **Reason:** The new auto-downgrade behavior for hallucinated symbol claims is not easily discoverable by a first-time user without consulting internal documentation or source code.
- **Required fix:** Update the `council.py` module docstring or add a user-facing `README.md` to clearly explain the new auto-downgrade behavior, including what triggers it and what the outcome is.
- **Evidence:** `Documentation for new behavior is in CLAUDE.md and changes.md, which are not primary user-facing documentation for a command-line tool.`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly addresses a real problem of false positive BUGS objections, improving the accuracy and reliability of the automated council system.
- **Evidence:** `Historical fixture replays confirm instances of hallucinated symbol claims, demonstrating a recurring need to prevent unnecessary build blocks.`

### COOL — APPROVE (low)
- **Reason:** The system's ability to self-correct and auto-downgrade its own hallucinated objections is a unique and memorable signature move.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons are violated; the deliverable addresses a recurring 'hallucination' insight.

## Resolution

Human decision required. Resume the build after updating session_state.json.
