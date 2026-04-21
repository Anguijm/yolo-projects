# Council Escalation — experiments/fix-council-enforcement

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-21T20:41:36.938770+00:00

## Angle positions

### BUGS — OBJECT (low)
- **Reason:** The parse-failure retry logic relies on a hardcoded error message string, which could break if the internal message for unparseable output changes in `Verdict.from_raw`.
- **Required fix:** Modify `Verdict.from_raw` to return a specific error flag or type for parse failures, and update `call_angle` to check this flag/type instead of a string comparison.
- **Evidence:** `council.py:84 (line `if verdict.reason == "Council member returned unparseable output" and not _retry:`)`

### SECURITY — APPROVE (low)
- **Reason:** The plan implements defensive measures and explicitly addresses potential path traversal by mandating `proj_dir.resolve().is_relative_to(REPO_ROOT)`, introducing no new attack surfaces or data exposure risks.

### UI — APPROVE (low)
- **Reason:** The plan concerns internal orchestrator logic and has no user-facing UI components, thus presenting no UI/UX concerns.

### GUIDE — APPROVE (low)
- **Reason:** The plan explicitly addresses discoverability for both human operators (via logs, updated learnings.md) and AI agents (via retry instructions, updated learnings.md), and self-documents verdicts.

### USEFULNESS — APPROVE (critical)
- **Reason:** This project directly addresses critical operational friction by fixing recurring false-positive escalations, saving significant human decision cycles and improving system reliability.
- **Evidence:** `The plan cites 'four consecutive council escalations' in two days, each costing 'one human decision cycle,' demonstrating a clear and frequent need for these fixes.`

### COOL — APPROVE (low)
- **Reason:** This project is an internal infrastructure bug fix for `council.py` and is explicitly exempt from the COOL angle's differentiation and memorability requirements per standing override.

### LESSONS — APPROVE (low)
- **Reason:** The plan directly addresses and implements documented lessons regarding council enforcement, precondition evidence, and goalpost moving, rather than violating them.

## Resolution

**RESOLVED 2026-04-22 by John (interactive session). BUGS critique accepted and addressed.**

This is the **6th attempt** at fix-council-enforcement PLAN gate. Notable improvement: **6 of 7 angles approved this round**, including LESSONS (no more false-positive VETOs) and COOL (explicitly exempt per standing override). The council's own behavior is trending correctly — just one low-severity issue remaining.

### BUGS OBJECT — ACCEPTED, FIX APPLIED
Legitimate code-quality critique: "parse-failure retry logic relies on a hardcoded error message string, which could break if the internal message for unparseable output changes in `Verdict.from_raw`."

**Fix**: Added `parse_failed: bool = False` field to `Verdict` dataclass. `Verdict.from_raw` sets it to `True` on `JSONDecodeError`. `call_angle` now checks `verdict.parse_failed` (the flag) instead of `verdict.reason == PARSE_FAILURE_MARKER` (brittle string match). Test `test_parse_failed_flag_set_by_from_raw` added to the suite. 17/17 tests pass.

Shipping as part of the same tick that fix-council-enforcement delivers (one commit). See `changes.md` for the detailed change log.
