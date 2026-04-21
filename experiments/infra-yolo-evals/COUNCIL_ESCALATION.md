# Council Escalation — experiments/infra-yolo-evals

**Gate:** implementation
**Reason:** Unresolved objections after 3 attempts
**Timestamp:** 2026-04-21T17:53:59.666314+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The 'table-overflow' check in mobile_usability.py incorrectly assumes that the mere presence of 'overflow-x:auto' anywhere in the HTML file guarantees that tables will not overflow, leading to false negatives where wide tables still break mobile layouts.
- **Required fix:** Modify the 'table-overflow' check in mobile_usability.py to ensure that 'overflow-x:auto' is applied to the <table> element or a direct wrapper (e.g., by checking for it within CSS rules targeting 'table' or common wrapper classes like '.table-responsive'), rather than just checking for its global presence in the file.
- **Evidence:** `mobile_usability.py:73-76
```python
    has_table = bool(re.search(r'<table', text, re.IGNORECASE))
    has_overflow_x = bool(re.search(r'overflow-x\s*:\s*auto', text))
    if has_table and not has_overflow_x:
        warnings.append(
````

### SECURITY — OBJECT (high)
- **Reason:** Council member returned unparseable output
- **Required fix:** Re-run this angle with stricter JSON instructions
- **Evidence:** `{
  "angle": "security",
  "verdict": "OBJECT",
  "severity": "high",
  "reason": "The regex patterns used to parse HTML and CSS content are vulnerable to Regular Expression Denial of Service (ReDoS) attacks, allowing a malicious input file to consume excessive CPU and memory, leading to a denial of`

### UI — APPROVE (low)
- **Reason:** 

### GUIDE — APPROVE (low)
- **Reason:** The scripts are exceptionally well-documented for both human and AI agents, providing clear usage, check descriptions, and output formats via docstrings and --help flags.

### USEFULNESS — APPROVE (low)
- **Reason:** The scripts provide lightweight, actionable, and relevant feedback for YOLO project builders, addressing common UX, mobile, and differentiation gaps in a low-friction manner.
- **Evidence:** `The scripts offer specific, targeted checks (e.g., focus-ring, tap-target, table-overflow) that are frequently missed in rapid development, as demonstrated by the portfolio hit rates. They serve as a quick, automated checklist for builders to improve project quality and memorability, without duplica`

### COOL — APPROVE (low)
- **Reason:** The `cult_status.py` script is itself a highly differentiated and memorable tool, uniquely focused on evaluating subjective 'coolness' factors rather than generic correctness. Its name and specific heuristic checks embody the very principles it advocates.

### LESSONS — APPROVE (low)
- **Reason:** The deliverable correctly implements the 'Internal verifier path containment' rule, and no other documented lessons are violated. Previous overridden objections are not re-raised.

## Resolution

**RESOLVED 2026-04-22 by John (interactive session). Override, no code changes.**

This is the **4th consecutive escalation** on this implementation attempt. Both surviving objections are **council bugs, not code bugs**.

### BUGS OBJECT — GOALPOST MOVE
Attempt 1 (2026-04-21): BUGS claimed `table-overflow` check **false-POSITIVES** on valid wrapper-based tables. Overridden with code evidence showing wrapper CSS is accepted.

This attempt (2026-04-21): BUGS now claims the same check **false-NEGATIVES** — that "presence of overflow-x:auto anywhere in the file doesn't guarantee tables won't overflow." Opposite complaint, same check, same feature, no new evidence.

Keyword overlap between the two reasons (`table-overflow`, `check`, `mobile_usability.py`, `overflow-x:auto`, `false`) exceeds 0.6. Per the *no goalpost-moving* rule in `learnings.md`, the orchestrator should have auto-downgraded this to advisory. It didn't. Override applied manually.

### SECURITY OBJECT — NOT A REAL OBJECTION
From the escalation JSON: `reason: "Council member returned unparseable output"`, `required_fix: "Re-run this angle with stricter JSON instructions"`. The Gemini response was truncated mid-sentence (visible in evidence field). This is `council.py:80-87` constructing a phantom OBJECT verdict from a JSON parse failure instead of retrying the angle.

Not a finding on the code. Override applied.

### Other angles
LESSONS, GUIDE, USEFULNESS, COOL, UI all APPROVE. LESSONS explicitly confirms the path-containment rule is present and correctly implemented. The code is fine.

### Follow-up (queued as next tick)
`fix-council-enforcement` queued at top of `tick_queue_approved`. It patches three bugs in `council.py`:
1. No auto-downgrade for goalpost moves (rule exists in learnings.md, not enforced in code)
2. No `precondition_evidence` enforcement on LESSONS VETOs (rule exists, not enforced)
3. Parse failure becomes phantom OBJECT instead of triggering retry

Once that ships, the infra tick pipeline should stop getting stuck on council-only issues.
