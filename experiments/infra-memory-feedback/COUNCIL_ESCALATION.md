# Council Escalation — experiments/infra-memory-feedback

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-22T21:42:48.550651+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The `_escalation_id` helper truncates the `reason` field to 200 characters before hashing, which can lead to identical `escalation_id`s for distinct escalation reasons, causing `INSERT OR IGNORE` to silently drop unique historical records.
- **Required fix:** The `_escalation_id` helper must use the full `reason` field (or a sufficiently large prefix, e.g., 1024 characters or more, to prevent practical collisions) when computing the content hash to ensure uniqueness for all distinct escalation records.
- **Evidence:** `New `_escalation_id(entry)` helper: SHA1 content-hash of `project|gate|resolved_at|timestamp|reason[:200]`, truncated to 16 hex chars.`

### SECURITY — APPROVE (low)
- **Reason:** Previous SHA1 concern is explicitly stated as resolved by upgrade to SHA256 in the active override; all SQL queries use parameterized statements preventing injection; input validation and sanitization are adequate for a CLI tool.

### UI — APPROVE (low)
- **Reason:** The changes improve user feedback and guidance, particularly for invalid inputs, and provide clear CLI commands for new functionality.

### GUIDE — APPROVE (low)
- **Reason:** The updated docstring, explicit command listing, actionable error messages, and comprehensive test examples provide excellent discoverability for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** This project provides a critical feedback loop for measuring the impact and accuracy of the 'learnings' system, enabling its continuous improvement.
- **Evidence:** `The `recall-stats` command provides actionable metrics (top prevented bugs, top false positives) that are essential for an analyst or developer to understand and refine the 'learnings' system. The `mark-outcome` commands provide a way for human feedback, and `backfill-recall` automates initial class`

### COOL — APPROVE (low)
- **Reason:** The tool's unique angle is its self-reflection and automated classification of its own past 'learnings' as 'prevented_bug' or 'false_positive', creating a meta-feedback loop for the system itself.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or anti-patterns were violated. Relevant lessons regarding destructive actions and modularity were appropriately applied.

## Resolution

Human decision required. Resume the build after updating session_state.json.
