# Council Escalation — experiments/infra-memory-feedback

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-22T01:12:30.620742+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The unique constraint `(learning_id, project, gate)` for the `recall_outcomes` table will cause silent data loss during `cmd_backfill_recall` when multiple distinct escalation records from `session_state.json` are classified with the sentinel `learning_id=0` for the same `(project, gate)` combination, as only the first such record will be stored and subsequent distinct records will be ignored.
- **Required fix:** 1. Add a new column, `escalation_timestamp TEXT`, to the `recall_outcomes` table (assuming `resolved_at` or similar timestamp is available in `session_state.json` escalation entries). 2. Modify the `SCHEMA` to define two partial unique indexes: `UNIQUE (learning_id, project, gate) WHERE escalation_timestamp IS NULL` (for manual markings/linked learnings) and `UNIQUE (project, gate, escalation_timestamp) WHERE learning_id IS 0` (for backfilled escalation records). 3. Adjust `cmd_mark_outcome` to set `escalation_timestamp = NULL` and use `INSERT OR REPLACE` targeting the first partial index. 4. Adjust `cmd_backfill_recall` to set `learning_id = 0` and populate `escalation_timestamp` from the `session_state.json` entry, then use `INSERT OR IGNORE` targeting the second partial index.
- **Evidence:** `## Approach
1. **Schema extension** — append `recall_outcomes` table definition to `SCHEMA` constant in `build_memory.py`. `CREATE TABLE IF NOT EXISTS` is non-destructive on existing DBs. Add unique constraint `(learning_id, project, gate)` for idempotent backfill.
...
4. **`cmd_backfill_recall(db)``

### SECURITY — OBJECT (medium)
- **Reason:** The `notes` field in `cmd_mark_outcome` accepts arbitrary user input without explicit sanitization or encoding, creating a latent data integrity and injection vulnerability if the stored data is later consumed by a web UI or other system with a trust boundary.
- **Required fix:** Implement sanitization or encoding for the `notes` field before storing it in the `recall_outcomes` table, or explicitly document the assumption that `notes` content is trusted and future consumers must handle it safely.
- **Evidence:** `Approach, step 3: `cmd_mark_outcome(db, learning_id, project, gate, outcome, notes)` and Security section: lack of explicit validation/sanitization for `notes`.`

### UI — APPROVE (low)
- **Reason:** The plan effectively addresses previous UI feedback by adding a clear discovery workflow for learning IDs, and all CLI outputs are well-structured and actionable.

### GUIDE — APPROVE (low)
- **Reason:** The plan explicitly addresses discoverability by adding `list-learnings` and providing a clear discovery workflow in the documentation.
- **Evidence:** `plan.md: 'cmd_list_learnings(db, limit=20, project=None) — added per UI critique on PLAN escalation. mark-veto/mark-fp both require a numeric learning_id but the plan originally provided no discovery path.'; plan.md: 'Discovery workflow'`

### USEFULNESS — APPROVE (low)
- **Reason:** This project provides a crucial feedback loop for the 'learnings' corpus, enabling evidence-based refinement and preventing degradation of the automated review system.
- **Evidence:** `Without a mechanism to distinguish 'prevented bugs' from 'false positives', the value of the learnings would diminish over time, leading to user frustration and reduced trust in the council system. This project directly addresses that need for continuous improvement.`

### COOL — APPROVE (low)
- **Reason:** The system provides a unique, data-driven feedback loop for evidence-based pruning of the internal learnings corpus, which is a signature move for self-improving knowledge systems.

### LESSONS — APPROVE (low)
- **Reason:** The plan demonstrates adherence to prior council feedback by incorporating specific changes (tightened regex, new CLI command) based on previous critiques, aligning with the principle of not repeating past mistakes.
- **Evidence:** `infra-memory-feedback PLAN escalation resolved 2026-04-22. Both BUGS+UI critiques ACCEPTED with code-level plan.md edits (tightened prevented_bug regex, added list-learnings CLI). First productive post-fix-council-enforcement escalation — council gave substantive feedback and we improved the plan.`

## Resolution

Human decision required. Resume the build after updating session_state.json.
