# Council Escalation — experiments/adopt-stack-audit

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T00:47:43.385346+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The plan relies on hardcoded line numbers for extracting dependencies and model names, making the audit immediately incorrect and stale if source files change.
- **Required fix:** Adopt a robust parsing method (e.g., YAML parser for workflows, AST parser for Python code) to identify dependencies by content and structure, rather than fragile line numbers.
- **Evidence:** `Approach: Step 1 cites 'line 37 of tick_tock.yml, line 59 of daily_research.yml' and 'tick_tock.yml line 40'. Step 2 cites 'council.py:90-91'. Test Strategy also relies on 'exact file and line'.`

### SECURITY — APPROVE (low)
- **Reason:** The plan is for a documentation-only artifact, creating no new executable code or storing secrets, thus introducing no new attack surface.

### UI — APPROVE (low)
- **Reason:** The deliverable is a static documentation artifact (markdown file), so there is no user interface to evaluate for UX concerns.

### GUIDE — APPROVE (low)
- **Reason:** The plan is exceptionally well-documented, providing clear steps, scope, methodology, and even edge cases for both human and AI agents to follow without external help.

### USEFULNESS — APPROVE (low)
- **Reason:** This project creates a valuable, consolidated reference for managing technical debt and future architectural decisions related to external dependencies.
- **Evidence:** `A dependency audit with risk assessment (deprecation, coupling) is a standard and necessary tool for project maintainers and architects, providing insights beyond simple package lists.`

### COOL — APPROVE ()
- **Reason:** The plan outlines a unique, human-augmented dependency audit methodology that goes beyond automated scanning, providing deep architectural insights like coupling depth and deprecation horizons for a broad scope of dependencies, including a 'zero-dep celebration'.

### LESSONS — APPROVE (low)
- **Reason:** The plan is for a documentation-only artifact and does not introduce any code, UI, or architectural changes that would violate documented lessons.

## Resolution

**RESOLVED 2026-04-25. BUGS critical accepted — all line numbers replaced with grep-by-content patterns.**

### BUGS critical — FIXED
The objection is correct: hardcoded line numbers rot the moment a workflow file or `council.py` is reorganized, making the audit immediately stale. Replaced every line-number citation with a grep pattern that locates the dependency by content. The plan now defines exact grep commands for each step:

- Step 1: `grep -nE "pip install" .github/workflows/*.yml` (and equivalents for npm, `uses:`, `node-version`, `python-version`)
- Step 2: `grep -nE "^(MODEL_NAME|CLAUDE_MODEL)\s*=" council.py`
- Step 3: targeted greps for each API service's SDK construction site and the matching workflow secret usage
- Edge cases: `requests` unused-status check uses `grep -rn "^import requests\|^from requests" --include="*.py" .`
- Test Strategy: each row cites a grep pattern, not a line number; **the audit document is invalid if any cited grep returns zero matches** — that is the test signal.

This makes the audit re-derivable with one command per row even after files have shifted, which is the central anti-rot property the BUGS objection demanded.

### Other 6 angles — APPROVE
SECURITY, UI, GUIDE, USEFULNESS, COOL, LESSONS all clean. GUIDE explicitly approved as "exceptionally well-documented."

Cron may rerun PLAN; expected clean pass → IMPLEMENTATION (write `STACK_AUDIT.md`).
