# Council Escalation — experiments/fix-council-bugs-hallucination

**Gate:** outcome
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T23:35:07.032574+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** 

### SECURITY — APPROVE (low)
- **Reason:** Existing security mitigations (regex escaping, path traversal guard, file size limit, bounded quantifiers) adequately cover potential attack surfaces introduced by text processing and file I/O.

### UI — APPROVE (low)
- **Reason:** The change improves the user experience by reducing false-positive BUGS objections and provides clear feedback when an objection is auto-downgraded.

### GUIDE — OBJECT (medium)
- **Reason:** The new auto-downgrade behavior for hallucinated symbol claims is not easily discoverable by a first-time user without consulting internal documentation or source code.
- **Required fix:** Update the `council.py` module docstring or add a user-facing `README.md` to clearly explain the new auto-downgrade behavior, including what triggers it and what the outcome is.
- **Evidence:** `Documentation for new behavior is in CLAUDE.md and changes.md, which are not primary user-facing documentation for a command-line tool.`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly addresses a real problem of false positive BUGS objections, improving the accuracy and reliability of the automated council system.
- **Evidence:** `Historical fixture replays confirm instances of hallucinated symbol claims, demonstrating a recurring need to prevent unnecessary build blocks.`

### COOL — APPROVE (low)
- **Reason:** The system's ability to self-correct and auto-downgrade its own hallucinated objections is a unique and memorable signature move.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons are violated; the deliverable addresses a recurring 'hallucination' insight.

## Resolution

**RESOLVED 2026-04-25. GUIDE medium fixed at source — module docstring expanded.**

### GUIDE medium — FIXED
The council's point is fair: `CLAUDE.md` and `changes.md` aren't the primary doc surface for a CLI tool — `council.py --help` and the module docstring are. Expanded the module docstring at the top of `council.py` to enumerate all four auto-downgrade enforcement rules with one-paragraph descriptions each, plus a pointer to learnings.md and the experiments dirs for full rationale. The docstring is now the single canonical reference for council behavior, discoverable via:
- `head council.py` (developers reading the source)
- `python3 -c "import council; help(council)"` (REPL/IDE introspection)
- IDE hover tooltips via `__doc__`
- AI-agent file reads (the docstring is in the first 30 lines)

This complements (rather than replaces) the CLAUDE.md and learnings.md docs — those remain the canonical surfaces for repo-wide conventions.

### Other 6 angles — APPROVE
BUGS, SECURITY, UI, USEFULNESS, COOL, LESSONS all clean. SECURITY explicitly noted bounded quantifiers + 2MB size cap + path containment as adequate. BUGS APPROVE (low) — no goalpost issues this round.

Cron may rerun OUTCOME; expected clean pass → ship the tick.
