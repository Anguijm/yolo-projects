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

**RESOLVED 2026-04-23 by John (autonomous wake cycle). SHA1 → SHA256 at source.**

### SECURITY OBJECT (medium) — FIXED AT SOURCE
Legitimate enough concern to address rather than override, even though the realistic attack model is weak (no adversarial input surface — `session_state.json` is written only by cron and the repo operator; an attacker with write access could just write what they want directly, no collision needed).

**Fix applied** (build_memory.py):
- `_escalation_id` now uses `hashlib.sha256` instead of `hashlib.sha1`. Same 16-hex-char prefix (64-bit id space, ample for <10^6 escalations).
- New `_HASH_ALGO_VERSION = 2` constant (v1=SHA1, v2=SHA256) tracked in a new `schema_versions` key-value table.
- `_migrate_recall_outcomes` upgraded: on algorithm version change, deletes backfilled rows (they regenerate on next `backfill-recall`) and updates the version record. Manual rows preserved.
- Docstring updated to explain the non-adversarial use case and the SHA256 upgrade rationale.

**Verified migration path** (v1 → v2):
- Seeded a synthetic v1 row with a SHA1-style hash, forced `escalation_id_algo = 1` in `schema_versions`
- Opened fresh DB connection → migration detected version mismatch → deleted the v1 row → set version to 2
- Next `backfill-recall` repopulated with SHA256 hashes cleanly

**Verified idempotency** (v2 only):
- Fresh DB + `backfill-recall` → 6 rows, 6 unique SHA256-based escalation_ids
- Second `backfill-recall` → 0 inserted (no duplicates)

### Other 6 angles — all APPROVE
BUGS, UI, GUIDE, USEFULNESS, COOL, LESSONS all approved with no objections. BUGS specifically noted "All identified correctness risks from previous gates have been addressed" — the escalation_id content hash fix from the earlier round held up cleanly.

Cron may rerun IMPLEMENTATION; expected clean pass. After IMPL → TESTS → OUTCOME, the tick ships and cron advances to `eval-opus-47-backbone` at queue position [1].
