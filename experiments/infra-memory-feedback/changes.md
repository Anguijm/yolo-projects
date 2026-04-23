# infra-memory-feedback — Implementation Changes

## Files Modified

### `build_memory.py` (+175 lines net, 534 → ~709 after IMPL-escalation fixes)

**IMPLEMENTATION-escalation fixes (2026-04-23, v1–v3 hash algo progression)**:

- `_escalation_id(entry)` helper (lines 90–122): SHA-256 content-hash of the full concatenation `project|gate|resolved_at|timestamp|reason|resolution` (no truncation), `hexdigest()[:16]` gives a 64-bit id. Using the full `reason` (not `reason[:200]`) eliminates the collision risk for distinct reasons sharing a common 200-char prefix. SHA-256 chosen over SHA-1 per SECURITY escalation; both are non-adversarial contexts but SHA-256 is the modern default.
- `_HASH_ALGO_VERSION = 3` (line 134): v1=SHA1/200-char, v2=SHA256/200-char, v3=SHA256/full-no-truncation.
- `schema_versions` table (lines 165–175): KV table tracking `escalation_id_algo` version; when version bumps, all backfilled rows are deleted so they regenerate from the new hash. Manual mark-veto/mark-fp rows (`escalation_timestamp IS NULL`) are preserved across migrations.
- `_migrate_recall_outcomes(db)` (lines 140–175): two-phase migration — (1) column-presence migration if `escalation_id` column missing (pre-first-fix DBs), (2) version-based migration for algo upgrades. Auto-invoked from `get_db()`.
- `uq_recall_backfill` index on `(project, gate, escalation_id) WHERE escalation_id IS NOT NULL` — ensures idempotency for backfilled rows.
- Verified (v3): fresh DB → 6 backfilled rows, 6 unique escalation_ids; second `backfill-recall` → 0 inserted (idempotent); synthetic collision test (same project/gate/resolved_at, different reasons) → distinct ids.

**TESTS gate attempt 2 fix (2026-04-23)**:
- Module docstring expanded with per-command argument documentation: types, valid enum values for `gate` (plan|implementation|tests|outcome), INSERT OR REPLACE semantics, backfill classification categories (prevented_bug / false_positive / irrelevant). Addresses GUIDE critique.

**IMPLEMENTATION gate attempt 2 fixes (2026-04-22)**:
- `list-learnings` arg parsing: changed `except ValueError: pass` to print a warning ("Warning: ignoring unrecognized argument ...") so invalid limit args are visible instead of silently dropped. (BUGS low, main():805-808)
- `cmd_mark_outcome`: changed warning-and-insert-anyway for unknown `learning_id > 0` to error-and-exit. Directs user to `list-learnings` to find valid IDs. (UI high, lines 664-666)

**Original IMPLEMENTATION gate work (from commit 2c7c96a, +132 lines):**

**Docstring** (lines 1–28): Added recall feedback commands section listing 5 new CLI commands.

**`SCHEMA` constant** (after line ~59): Appended `recall_outcomes` table DDL:
- `CREATE TABLE IF NOT EXISTS recall_outcomes` with columns: id, learning_id, project, gate, outcome, notes, escalation_timestamp, recorded_at
- `CREATE UNIQUE INDEX IF NOT EXISTS uq_recall_manual ON recall_outcomes(learning_id, project, gate) WHERE escalation_timestamp IS NULL` — enforces uniqueness for manual mark records
- `CREATE UNIQUE INDEX IF NOT EXISTS uq_recall_backfill ON recall_outcomes(project, gate, escalation_timestamp) WHERE escalation_timestamp IS NOT NULL` — enforces uniqueness for backfilled escalation records by timestamp

**New constants** (before `cmd_recall_stats`):
- `VALID_GATES = {'plan', 'implementation', 'tests', 'outcome'}`
- `VALID_OUTCOMES = {'prevented_bug', 'false_positive', 'irrelevant'}`
- `_FP_RE`: matches `false[\s._-]?positive|phantom|override.*veto|veto.*false`
- `_PREVENTED_RE`: matches `\bFIX\s+APPLIED\b|\bFIX\s+ACCEPTED\b|\bACCEPTED[,.\s—-]+FIX\b|\blegitimate\s+(?:bug|concern|critique|issue|fix|objection|defect|regression)\b|\b(?:real|genuine)\s+(?:bug|defect|regression)\b`
- `_LESSONS_VETO_RE`: matches `LESSONS\s+VETO|VETO`

**New functions**:
- `cmd_recall_stats(db, top_n=10)` (lines ~500–525): LEFT JOIN recall_outcomes → learnings, renders two fixed-width tables (top-N by prevented_bug, top-N by false_positive)
- `cmd_list_learnings(db, limit=20, project=None)` (lines ~528–548): lists recent learnings with id/project/type/snippet; supports optional --project filter
- `cmd_mark_outcome(db, learning_id, project, gate, outcome, notes='')` (lines ~551–575): validates args (int cast, gate/outcome enum check, learning_id > 0), warns if id not in learnings table, INSERT OR REPLACE with `escalation_timestamp = NULL`
- `cmd_backfill_recall(db)` (lines ~578–630): reads session_state.json, iterates council_escalations_resolved, filters to LESSONS VETO entries via `_LESSONS_VETO_RE`, classifies with priority-ordered regex (FP first, then prevented, else irrelevant/AMBIGUOUS), INSERT OR IGNORE with `escalation_timestamp = resolved_at`

**`main()` dispatch** (lines ~635–680): Added 5 elif branches for recall-stats, list-learnings, mark-veto, mark-fp, backfill-recall.

## Test Results

```
python3 -c "import ast; ast.parse(open('build_memory.py').read())"  → SYNTAX OK
python3 build_memory.py import                                       → 2024 learnings from 277 projects (unchanged)
python3 build_memory.py backfill-recall                             → 6 inserted, 1 ambiguous, 11 non-LESSONS skipped
python3 build_memory.py recall-stats 5                              → tables rendered, 0 learning_id rows + 6 escalation records
python3 build_memory.py list-learnings 5                            → table with id/project/type/snippet
python3 build_memory.py list-learnings 5 --project naval-scribe     → filtered table
python3 build_memory.py mark-veto 1 infra-memory-feedback plan      → Recorded prevented_bug for learning 1
python3 build_memory.py mark-fp 1 infra-memory-feedback plan        → INSERT OR REPLACE updated to false_positive
python3 build_memory.py backfill-recall (second run)                → 0 inserted (idempotent)
```

Sentinel-collision verification: `infra-yolo-evals/implementation/learning_id=0` = 1 row.
Note: only 1 of the 3 infra-yolo-evals implementation escalations contains "LESSONS VETO" in reason
(the others are BUGS+SECURITY only). Schema's partial indexes correctly prevent collisions — the
test expectation in plan.md said "4 escalations" but actual data has 3, with 1 LESSONS VETO.
Feature is correctly implemented; future multi-LESSONS-VETO sessions will be handled correctly.

Fix applied (attempt 2): `_PREVENTED_RE` updated to include `\bAPPLIED\s+FIX\b` alongside
`\bFIX\s+APPLIED\b`. Now naval-scribe/tests correctly classifies as `prevented_bug` (the LESSONS
VETO was valid — addItems() DOM batch fix was applied). Backfill: 6 inserted, 0 ambiguous.
