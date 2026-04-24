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

**RESOLVED 2026-04-25. All three concerns fixed at source.**

### BUGS critical — FIXED
Added explicit `\b` after every `{esc}` in `_symbol_defined_in_content`. Existing patterns implicitly formed word boundaries through their syntax requirements (e.g. `\s*=`, `\s*[:(]`), but explicit boundaries are defense-in-depth and remove any ambiguity. Now every JS/TS and Python pattern asserts the symbol ends on a word-boundary before whatever syntactic context follows.

### SECURITY high — FIXED
Replaced unbounded `*` quantifiers with bounded `{0,N}` ranges:
- `\s*` → `\s{0,8}` (whitespace between tokens) or `[ \t]{0,80}` (line indent)
- `\s+` → `\s{1,8}` (required whitespace)
- `[^)]*` → `[^)]{0,500}` (paren contents)

Combined with the existing 2 MB file-size cap, these bounds make worst-case backtracking O(N) in input length. Real source code never has 80 leading spaces or a 500-char single-line method signature; the bounds are well above any legitimate case.

### GUIDE high — FIXED
Two new doc surfaces:
1. `learnings.md` "Council enforcement rules are now LIVE in code" section — added bullet 4 documenting the BUGS hallucination rule with detection layers, symbol-extraction nuance ("symbols before each claim keyword, not after"), and the LST/Template-Lib history that motivated it.
2. `CLAUDE.md` — added a new "Council enforcement rules (auto-downgrade behavior)" section listing all four rules so AI agents working in this repo discover them as part of the standard repo conventions.

Both surfaces are agent-discoverable: `CLAUDE.md` is auto-loaded into Claude Code sessions, and `learnings.md` is referenced from there + scanned in standard council prompts.

### Other 4 angles — APPROVE
UI, USEFULNESS, COOL, LESSONS all clean.

34 enforcement tests pass (17 prior + 17 new = `TestSymbolDefinedInContent` + `TestBugsHallucination` + fixture replays).

Cron may rerun IMPLEMENTATION; expected clean pass.
