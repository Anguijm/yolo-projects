# Council Escalation — experiments/infra-guardrails

**Gate:** outcome
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-21T11:57:53.121895+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The `ROW_RE` regex for parsing constraint rows is too strict, causing rows with genuinely empty fields (e.g., `| C1 | Rule | Pass | |`) to be entirely skipped, which leads to misleading 'Missing constraint' errors instead of specific 'empty field' warnings.
- **Required fix:** Modify `ROW_RE` in `check_constraints.py` to `re.compile(r"^\s*\|\s*(C\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|", re.MULTILINE)` to allow empty fields to be matched, relying on the subsequent `if not all(fields)` check to correctly identify and report them.
- **Evidence:** `check_constraints.py:ROW_RE and check_constraints.py:L46`

### SECURITY — APPROVE (low)
- **Reason:** SECURITY OBJECT OVERRIDDEN — sys.argv[1] retained. This is a dev-time verifier with no production trust boundary, as per mandatory override. No other exploitable surfaces identified.

### UI — APPROVE (low)
- **Reason:** The CLI tool provides clear usage instructions, robust error checking with actionable messages, and good overall feedback for a technical user. Documentation is thorough.

### GUIDE — APPROVE (low)
- **Reason:** Comprehensive documentation in README and docstring ensures discoverability for both human users and AI agents.
- **Evidence:** `experiments/infra-guardrails/README.md, check_constraints.py docstring`

### USEFULNESS — APPROVE (low)
- **Reason:** This tool provides essential structural integrity checks for a critical internal document (program.md), ensuring consistency for both human and automated processing.
- **Evidence:** `Ensures machine-readable consistency of core system rules, preventing errors in downstream automated processes or human misinterpretation; comparable to linter or schema validation for configuration files.`

### COOL — APPROVE (low)
- **Reason:** COOL OBJECT OVERRIDDEN: internal infrastructure tooling is explicitly exempt from the signature-move bar; this markdown verifier provides high utility for guarding `program.md` integrity.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or anti-patterns from _hot.md or learnings.md are violated by the deliverable. Robust error handling and clear documentation of regex patterns align with past 'KEEP' and 'IMPROVE' insights.

## Resolution

**RESOLVED 2026-04-21 ~12:20 UTC by John (interactive session, via auto-wake).**

### BUGS OBJECT — ACCEPTED (fix applied)
`ROW_RE` changed from `([^|]+)` to `([^|]*)` in all three field capture groups (Rule/Pass/Fail). A row like `| C1 | Rule | Pass | |` now matches the regex; the existing `if not all(fields)` check catches the empty field and reports `Row C1: one or more empty fields` instead of silently dropping C1 from `found_ids` (which previously produced the misleading `Missing constraint: C1` error). Verified with three synthetic fixtures: empty-Fail-field on C1 caught, all-empty-row on C5 caught, and the clean 10-row fixture still passes. The real `program.md` still PASSes.

`changes.md` and `README.md` regex documentation both updated to the new `([^|]*)` pattern with an inline note explaining the empty-field-diagnosis rationale.

All other angles (SECURITY/UI/GUIDE/USEFULNESS/COOL/LESSONS) approved on attempt 2 — nothing else to address.

Cron should now rerun OUTCOME and pass cleanly, then pop infra-guardrails from `tick_queue_approved` and advance to the next tick (`infra-yolo-evals`).
