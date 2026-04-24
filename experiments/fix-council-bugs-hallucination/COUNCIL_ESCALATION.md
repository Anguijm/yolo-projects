# Council Escalation — experiments/fix-council-bugs-hallucination

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T23:02:21.847828+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The `_symbol_defined_in_content` function lacks word boundaries (`\b`) after the escaped symbol in patterns for JS/TS method shorthand and Python definition/assignment, leading to false positives where a symbol is a substring of another, incorrectly downgrading valid BUGS objections.
- **Required fix:** Add `\b` after `esc` in the regex patterns for JS/TS method shorthand (`{esc}\b`), Python `def/class` (`{esc}\b`), and Python assignment (`{esc}\b`) within `_symbol_defined_in_content` to ensure exact symbol matching.
- **Evidence:** `council.py: line 55 (method shorthand pattern), line 60 (Python def/class pattern), line 63 (Python assignment pattern)`

### SECURITY — OBJECT (high)
- **Reason:** The regular expressions in `_symbol_defined_in_content` contain unbounded quantifiers (`*`) on potentially large, user-controlled file content, creating a Regular Expression Denial of Service (ReDoS) vulnerability.
- **Required fix:** Refine the regex patterns in `_symbol_defined_in_content` to prevent excessive backtracking, for example, by using more specific quantifiers or by limiting the length of matched sequences where appropriate, especially for `\s*` and `[^)]*`.
- **Evidence:** `council.py:70:            rf"(?m)^\s*(?:async\s+)?(?:static\s+)?{esc}\s*\([^)]*\)\s*\{"`

### UI — APPROVE (low)
- **Reason:** The change improves the developer's experience by reducing unnecessary blocks due to hallucinated BUGS objections, and provides clear feedback when auto-downgrading.

### GUIDE — OBJECT (high)
- **Reason:** The automatic downgrade mechanism for BUGS OBJECTs is not sufficiently documented for a first-time AI agent or human user to anticipate its behavior.
- **Required fix:** A user-facing document (e.g., a 'Council Rules' or 'Enforcement Guide' for agents) should explicitly describe this auto-downgrade rule, including the conditions that trigger it and the resulting output format, and this document should be discoverable by an AI agent.
- **Evidence:** `Missing user-facing documentation / AI agent guide for the auto-downgrade rule; `changes.md` is an internal document, not a user-facing guide.`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly addresses a known source of false positives in the BUGS council, preventing incorrect build blocks and saving developer time.
- **Evidence:** `Historical fixture replays (e.g., Template Lib round 1) demonstrate past occurrences of this problem, confirming a real, recurring need.`

### COOL — APPROVE (low)
- **Reason:** The system's ability to self-correct its own 'hallucinated' objections is a unique and highly memorable signature move.

### LESSONS — APPROVE (low)
- **Reason:** The project addresses a known hallucination pattern, aligning with the 'Haiku UI hallucination pattern' insight, and does not violate any documented lessons or anti-patterns.
- **Evidence:** `INSIGHT: Haiku UI hallucination pattern — across all 3 benchmark fixtures, the UI angle independently fabricated the same specific detail: 'injected accessibility override with !important forces illegible font sizes.' None of these projects contain such an override. This is a systematic single-angle`

## Resolution

Human decision required. Resume the build after updating session_state.json.
