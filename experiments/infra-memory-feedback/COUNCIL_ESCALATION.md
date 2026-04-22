# Council Escalation — experiments/infra-memory-feedback

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-22T10:15:23.221959+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The `uq_recall_backfill` unique index, combined with `learning_id=0` for all backfilled records, can cause silent data loss if multiple distinct escalation events from `session_state.json` happen to share the same `project`, `gate`, and `resolved_at` timestamp.
- **Required fix:** Modify the `uq_recall_backfill` index to include a truly unique identifier for each backfilled escalation event (e.g., an `escalation_id` from `session_state.json` if available, or a hash of the full escalation details), or remove the unique constraint on `(project, gate, escalation_timestamp)` for backfilled records to allow all distinct events to be recorded.
- **Evidence:** `CREATE UNIQUE INDEX IF NOT EXISTS uq_recall_backfill ON recall_outcomes(project, gate, escalation_timestamp) WHERE escalation_timestamp IS NOT NULL;

In `cmd_backfill_recall`, `db.execute("""INSERT OR IGNORE INTO recall_outcomes ... VALUES (0, ?, ?, ?, '', ?) """, (project, gate, outcome, timestamp)`

### SECURITY — OBJECT (high)
- **Reason:** The `cmd_backfill_recall` function reads `session_state.json`, which is described as containing `council_escalations_resolved`. If this file contains sensitive information (e.g., details of vulnerabilities, confidential project names), processing and storing even derived metadata (project, gate, outcome, timestamp) into an unencrypted SQLite database could lead to data exposure if the database has broader access than the source file.
- **Required fix:** Implement explicit redaction or sanitization of sensitive data within `session_state.json` before processing, or ensure the SQLite database has equivalent or stronger access controls and encryption as the source file. Alternatively, confirm that `session_state.json` is guaranteed not to contain any sensitive data that would be exposed by this process.
- **Evidence:** `build_memory.py:580 (reads session_state.json), build_memory.py:619 (inserts derived data into recall_outcomes)`

### UI — APPROVE (low)
- **Reason:** The new CLI commands provide clear instructions, good validation feedback, and helpful discovery mechanisms for learning IDs, ensuring a smooth user experience for managing recall outcomes.

### GUIDE — APPROVE (low)
- **Reason:** The CLI tool provides a comprehensive docstring as a usage guide, clear command names, explicit error messages, and examples for all new features.

### USEFULNESS — APPROVE (low)
- **Reason:** This project establishes a critical feedback loop, allowing the system to learn which 'learnings' are genuinely useful in preventing issues (prevented_bug) versus those that are false positives or irrelevant. This is fundamental for improving the system's real-world utility and turning it into a reliable tool.
- **Evidence:** `Any predictive or recommendation system requires a feedback mechanism to validate its output and drive continuous improvement. The `mark-veto`/`mark-fp` commands provide this explicit feedback, `backfill-recall` leverages historical data to bootstrap, and `recall-stats` offers essential monitoring f`

### COOL — APPROVE (low)
- **Reason:** The automated backfilling of 'LESSONS VETO' escalations and the 'recall-stats' command quantifying prevented bugs vs. false positives provide a unique, evaluative feedback loop for learnings, moving beyond simple collection.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The `cmd_mark_outcome` function uses `INSERT OR REPLACE` to record manual outcomes without explicitly warning the user *before* overwriting an existing manual record, violating the 'WILL CHANGE / WILL CLEAR / WILL KEEP pattern for destructive actions' lesson.
- **Required fix:** Implement a pre-action confirmation prompt in `cmd_mark_outcome` if a manual record for the given `(learning_id, project, gate)` already exists, asking the user to confirm the overwrite.
- **Evidence:** `[INSIGHT — WILL CHANGE / WILL CLEAR / WILL KEEP pattern for destructive actions]: When a feature overwrites or clears existing user data (body text, field sets), the preview drawer must explicitly list every affected field in three named sections. This is both a UX requirement (informed consent) and`

## Resolution

Human decision required. Resume the build after updating session_state.json.
