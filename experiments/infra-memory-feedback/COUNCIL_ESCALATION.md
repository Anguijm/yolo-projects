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

**RESOLVED 2026-04-23 by John (interactive session). BUGS fixed at source, SECURITY overridden per precedent.**

### BUGS OBJECT (critical) — FIXED AT SOURCE
Legitimate. The `|` delimiter in `_escalation_id` could produce identical hashes for distinct escalations if any field contained a literal `|` — a real collision risk for `reason`/`resolution` text that might reference pipes.

**Fix applied** (build_memory.py):
- Replaced `"|".join([...])` with `json.dumps([...], ensure_ascii=False, separators=(",",":"))` — JSON escapes quotes inside strings, so no field content can ever be confused with a field boundary. Collision-proof encoding.
- Promoted `import json` to module level (was previously inline in `cmd_backfill_recall`).
- Bumped `_HASH_ALGO_VERSION` 3 → 4 with the new history comment. Migration auto-invalidates v3 backfilled rows on next connection open; next `backfill-recall` repopulates with v4 hashes.

**Verified:**
- Fresh DB + `backfill-recall` → 6 rows, 6 unique v4 escalation_ids
- Second `backfill-recall` → 0 inserted (idempotent)
- `schema_versions.escalation_id_algo = 4`
- Pipe-in-field test: two entries that would have produced identical hashes under the `|` encoding now produce distinct hashes (verified with a synthetic case)

### SECURITY OBJECT (medium) — OVERRIDDEN
ReDoS concern on `_FP_RE` and `_PREVENTED_RE` `.*` patterns.

**Override rationale**: ReDoS requires both a vulnerable pattern AND attacker-controlled unbounded input. Neither applies:
1. `reason` and `resolution` come from `session_state.json`, written only by cron and the repo operator — no external input surface
2. Real inputs are bounded (typically <1KB, always <100KB)
3. Matching happens once during `backfill-recall`, not in a request loop

Per the `adopt-planning-mode` precedent (`learnings.md:26`): producer-side hardening not required absent a concrete downstream consumer with a separate trust boundary. Same rationale used for the SHA1 → SHA256 upgrade, the `sys.argv` path concerns on infra-yolo-evals, and SECURITY concerns on earlier infra-memory-feedback gates.

### Other 5 angles — all APPROVE
UI, GUIDE, USEFULNESS, COOL, LESSONS all clean. No false-positive vetos this round.

Cron may rerun TESTS gate; expected clean pass → OUTCOME → ship. Advances to `eval-opus-47-backbone` after completion.
