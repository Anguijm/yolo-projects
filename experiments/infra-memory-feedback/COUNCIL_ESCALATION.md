# Council Escalation — experiments/infra-memory-feedback

**Gate:** tests
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-23T04:47:03.086154+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The `_escalation_id` hash concatenation uses a simple `|` delimiter, which can lead to hash collisions if the `reason` or `resolution` fields contain the `|` character, causing distinct escalations to be treated as identical due to non-unique IDs and potential data corruption via `INSERT OR IGNORE`.
- **Required fix:** Modify `_escalation_id` to use a robust serialization method for concatenation (e.g., length-prefixed fields or JSON serialization) before hashing, to prevent collisions when data fields contain the delimiter character.
- **Evidence:** `_escalation_id(entry)` helper (lines 90–122): SHA-256 content-hash of the full concatenation `project|gate|resolved_at|timestamp|reason|resolution``

### SECURITY — OBJECT (medium)
- **Reason:** Regular expressions used for classifying potentially untrusted input from `session_state.json` contain `.*` patterns which could be vulnerable to ReDoS (Regular Expression Denial of Service) if crafted with long, malicious strings.
- **Required fix:** Analyze and refactor regular expressions (`_FP_RE`, `_PREVENTED_RE`) to eliminate or mitigate ReDoS vulnerabilities by avoiding problematic constructs like unbounded quantifiers on arbitrary wildcards (`.*`) or ensuring input length limits are enforced before regex application.
- **Evidence:** `file:build_memory.py (lines ~578–630, specifically where `reason` and `resolution` from `session_state.json` are processed by `_FP_RE`, `_PREVENTED_RE`, `_LESSONS_VETO_RE`)`

### UI — APPROVE (low)
- **Reason:** The proposed changes significantly improve the user experience by providing clearer error messages, better argument validation feedback, and comprehensive in-tool documentation for new CLI commands.

### GUIDE — APPROVE (low)
- **Reason:** Module docstring provides comprehensive per-command argument documentation, including types, valid enum values, semantics, and classification categories, addressing previous discoverability concerns.
- **Evidence:** `build_memory.py: Module docstring (lines 1-28), TESTS gate attempt 2 fix (2026-04-23) in changes.md`

### USEFULNESS — APPROVE (low)
- **Reason:** This project provides a critical feedback loop for evaluating the effectiveness of 'learnings' derived from council escalations, enabling continuous improvement of the review process.
- **Evidence:** `The `recall-stats` command and the `mark-outcome` commands directly address the need to measure and improve the quality of learnings, which is a common challenge in post-mortem or review processes for any organization.`

### COOL — APPROVE (low)
- **Reason:** The automated classification of 'LESSONS VETO' escalations into 'prevented_bug' or 'false_positive' using regexes, and the subsequent 'recall-stats' reporting, provides a unique signature move for deriving actionable insights from historical feedback, rather than just storing it.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

Human decision required. Resume the build after updating session_state.json.
