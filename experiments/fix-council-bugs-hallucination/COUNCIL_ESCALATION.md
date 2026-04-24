# Council Escalation — experiments/fix-council-bugs-hallucination

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T22:47:41.679212+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The JavaScript/TypeScript definition pattern `"{symbol}\\s*\\("` in `_symbol_defined_in_content` incorrectly identifies function calls as definitions, leading to false positives where legitimate BUGS objections about truly undefined functions will be auto-downgraded.
- **Required fix:** Remove or significantly refine the `rf"{esc}\\s*\\("` pattern in `_symbol_defined_in_content` for `.js` and `.ts` files to prevent misidentifying function calls as definitions, or explicitly state that method shorthand definitions are out of scope for regex detection.
- **Evidence:** ````python
    if ext in (".html", ".js", ".ts"):
        patterns = [
            rf"function\\s+{esc}\\b",
            rf"(?:const|let|var)\\s+{esc}\\s*=",
            rf"{esc}\\s*\\(",           # call-site is NOT a def, but method shorthand is
        ]
````

### SECURITY — APPROVE (low)
- **Reason:** The plan correctly handles path containment and regex injection, and file operations are read-only, limiting direct attack surfaces.

### UI — APPROVE (low)
- **Reason:** This plan describes an internal enforcement mechanism for the council system and has no direct impact on user-facing UI or user experience.

### GUIDE — APPROVE (low)
- **Reason:** The plan includes clear logging, updates to `changes.md`, and `learnings.md` to ensure discoverability of the new enforcement rule for both human users and AI agents.
- **Evidence:** `changes.md, learnings.md, UI section in plan.md`

### USEFULNESS — APPROVE (low)
- **Reason:** This project directly addresses a documented, costly problem of AI hallucination, improving the reliability and trustworthiness of a critical internal tool for developers.
- **Evidence:** `The plan cites specific, recurring instances of hallucinated 'undefined symbol' objections on projects like Letter Status Tracker and Template Letter Library, leading to wasted developer time and manual overrides. This directly solves that problem.`

### COOL — APPROVE (low)
- **Reason:** The system's ability to detect and auto-downgrade specific AI hallucinations about undefined symbols is a unique, meta-AI signature move, demonstrating depth beyond a generic linter.

### LESSONS — APPROVE (low)
- **Reason:** The plan directly addresses and prevents a documented recurring failure mode (BUGS hallucination loop), aligning with the LESSONS mandate to not repeat past mistakes.
- **Evidence:** `Goal: Add a council.py enforcement rule that auto-downgrades BUGS OBJECT verdicts whose cited evidence doesn't match actual file contents. Closes off the hallucination-loop pattern observed on Letter Status Tracker (rounds 7-9) and Template Letter Library (rounds 1-3) where cron kept objecting with `

## Resolution

**RESOLVED 2026-04-25. BUGS critical accepted; pattern refined.**

### BUGS critical — ACCEPTED
The objection is correct: `{esc}\s*\(` matches every call site, not just method-shorthand definitions. That would cause false-positive auto-downgrades on legitimate "undefined function" objections whenever the function is called (but not defined) in a cited file.

Fix: replaced the third JS/TS pattern with a line-anchored method-shorthand matcher that requires `{` after the closing paren:

```python
rf"(?m)^\s*(?:async\s+)?(?:static\s+)?{esc}\s*\([^)]*\)\s*\{{",
```

This matches method shorthand (`foo() { ... }`, `async bar() { ... }`, `static baz() { ... }`) but excludes call sites (`foo();`, `obj.foo()`, `foo().bar`) because none of those end with `{` directly after the closing paren. Methods inside class/object bodies remain detected since they live at the start of their indented line.

`function foo()` declarations are still caught by the first pattern (`function\s+{esc}\b`); the third pattern's role is strictly the method-shorthand-without-`function` form.

### Other 6 angles — APPROVE
SECURITY, UI, GUIDE, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun PLAN; expected clean pass.
