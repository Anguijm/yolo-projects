# Council Escalation — experiments/fix-council-bugs-hallucination

**Gate:** outcome
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T23:43:12.307826+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The hallucination detection logic for JavaScript/TypeScript is incomplete, failing to recognize symbols defined with `let` or `var` keywords, which will incorrectly allow hallucinated BUGS objections to stand.
- **Required fix:** Extend the `_symbol_defined_in_content` function for JS/TS/HTML to include definition patterns for `let` and `var` declarations.
- **Evidence:** `Deliverable (experiments/fix-council-bugs-hallucination/changes.md) under 'Added functions' for `_symbol_defined_in_content`: '.html/.js/.ts uses function/const/method-shorthand'`

### SECURITY — APPROVE (low)
- **Reason:** The proposed changes include robust security measures such as re.escape for symbol patterns, path containment guards, file size limits, and bounded quantifiers to mitigate regex injection, path traversal, and resource exhaustion risks.

### UI — APPROVE (low)
- **Reason:** The change reduces false-positive objections and provides clear feedback when an objection is auto-downgraded, improving developer workflow and reducing confusion.

### GUIDE — OBJECT (medium)
- **Reason:** The new BUGS hallucination detection rule is documented as a change, but not in a consolidated, user-facing, or AI-agent-facing guide for the overall council system.
- **Required fix:** Create or update a central `council_rules.md` or `README.md` for the `council.py` system that comprehensively describes all active rules, including the BUGS hallucination detection, for both human users and AI agents.
- **Evidence:** `Missing `council_rules.md` or comprehensive `README.md` for `council.py`; `experiments/fix-council-bugs-hallucination/changes.md` is a diff, not a complete guide.`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly solves the problem of developers being blocked by false-positive 'undefined symbol' objections from the BUGS council, improving workflow efficiency.
- **Evidence:** `The project cites historical fixture replays (e.g., Template Lib round 1 'byDirectionChk' hallucination) and a live cron run that confirm it addresses a real, recurring issue for developers.`

### COOL — APPROVE (low)
- **Reason:** The system's ability to self-correct another tool's specific false positives (hallucinated undefined symbols) is a unique and memorable signature move for internal process improvement, creating an 'oh, nice' moment for developers.

### LESSONS — APPROVE (low)
- **Reason:** The deliverable addresses a known type of issue (hallucination) previously observed in other angles, aligning with the spirit of not repeating past mistakes.
- **Evidence:** `INSIGHT: Haiku UI hallucination pattern — across all 3 benchmark fixtures, the UI angle independently fabricated the same specific detail: 'injected accessibility override with !important forces illegible font sizes.' None of these projects contain such an override. This is a systematic single-angle`

## Resolution

**RESOLVED 2026-04-25. BUGS objection was itself a hallucination (let/var already covered); GUIDE consolidated guide created.**

### BUGS high — REJECTED (council hallucination, doc clarified)
The objection claims `let`/`var` aren't covered. The actual code at `council.py:389` reads:

```python
rf"(?:const|let|var)\s{1,8}{esc}\b\s{0,8}=",
```

All three keywords (`const`, `let`, `var`) are in the alternation. The council read the changes.md summary — which used "function/const/method-shorthand" as shorthand prose — and inferred the pattern was incomplete. This is **exactly the hallucination class this very tick is designed to detect** (claim says "missing X" / actual code shows X is present).

The rule isn't yet live on cron because the deployment hasn't completed, so the council can't catch its own self-inflicted irony here. Future runs will. In the meantime, updated `changes.md` to be explicit: "(?:const|let|var) NAME = (covers all three JS variable-declaration keywords)".

### GUIDE medium — FIXED
Created `council_rules.md` at repo root — the consolidated user-facing/agent-facing guide the council requested. Covers all four enforcement rules with full rationale, pattern tables, configuration constants, log-line reference, and an "Authoring new rules" section. Cross-references the module docstring, CLAUDE.md, learnings.md, and the experiments dirs.

This satisfies the "central council_rules.md or README.md for the council.py system" the council asked for in evidence. CLAUDE.md and learnings.md continue to serve repo-wide convention purposes; the new file is the single canonical reference for council mechanics.

### Other 5 angles — APPROVE
SECURITY, UI, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun OUTCOME; expected clean pass → ship the tick.
