# Council Escalation — experiments/infra-memory-feedback

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-22T20:43:36.362915+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** All identified correctness risks from previous gates have been addressed, and new features are implemented with robust data integrity, migration, and error handling.

### SECURITY — OBJECT (medium)
- **Reason:** The `_escalation_id` function uses SHA1, which is cryptographically broken for collision resistance, potentially allowing an attacker to craft `session_state.json` entries that collide and lead to data loss via `INSERT OR IGNORE`.
- **Required fix:** Replace SHA1 with a cryptographically strong hash function (e.g., SHA256) for `_escalation_id` to ensure unique content-based identifiers even with hostile input.
- **Evidence:** `build_memory.py:120: return hashlib.sha1(key.encode('utf-8')).hexdigest()[:16]`

### UI — APPROVE (low)
- **Reason:** The CLI commands provide clear usage instructions, actionable error messages, and good feedback for various states, including empty and invalid inputs.

### GUIDE — APPROVE (low)
- **Reason:** The tool's docstring clearly outlines all commands and their usage, and error messages provide actionable guidance.

### USEFULNESS — APPROVE (low)
- **Reason:** This feature provides a critical feedback loop, allowing the system to evaluate the real-world impact and accuracy of its collected learnings, transforming a data store into a self-improving tool.
- **Evidence:** `The 'recall-stats' command provides actionable metrics for council members, and 'backfill-recall' automates the initial classification from real historical data, directly addressing the need to validate the utility of 'learnings'.`

### COOL — APPROVE (low)
- **Reason:** The recall feedback loop, especially `recall-stats` and automated backfill, provides a unique meta-learning capability to evaluate the effectiveness of past learnings, distinguishing signal from noise.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or anti-patterns were violated by the proposed changes or the implementation.

## Resolution

Human decision required. Resume the build after updating session_state.json.
