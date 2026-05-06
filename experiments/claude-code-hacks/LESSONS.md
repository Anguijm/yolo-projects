# Lessons — claude-code-hacks

## Cycle 1 (static lint of all 5 command prompts)
**Tried:** Linted each command markdown for: action verb at top, file
path references, numbered steps, stop conditions, failure paths, length
under 500 words.

**Learned:**
- 4 of 5 commands pass all 6 checks.
- `/status-deep` lacks explicit numbered steps — it uses prose to
  describe what to add to the standard status output. Slightly weaker
  contract; an LLM might skip a section without realizing it failed.
- All commands stay well under the 500-word budget (max 216 for /plan).
- All commands name failure paths, which is good — they don't assume
  success.

**Gap not caught by lint:**
- The lint checks for *presence* of file paths, not *correctness*.
  `/status-deep` references `experiments/*/council_outcome.json` —
  worth checking that path actually exists in the repo. (Spot-checked:
  yes, used by infra-yolo-evals.)
- No check for "does the command's contract match what the user types
  in chat?" — e.g., `/test-gen path/to/module.py::func_name` argument
  shape. Hard to verify without an actual session.

**Change for cycle 2:**
- Add explicit numbered steps to /status-deep.
- Extend the lint to verify file paths referenced in commands exist in
  the repo (false-path shipping is a real failure mode).
- Add a "command contract" line to each command (`Usage:` block) so the
  argument shape is first-class.

## Cycle 2 (added numbered steps to /status-deep)
**Tried:** Re-linted /status-deep after adding numbered preamble steps.
**Learned:** All 6 lint checks now pass on all 5 commands. Word count for /status-deep grew from 154 to 205 — still under the 500-word budget.
**Change for cycle 3:** Add a `Usage:` line to each command (currently only /test-gen has one). Also: lint should verify referenced file paths actually exist in the repo.

## Cycle 3 (Usage: lines added to 4/5 commands)
**Tried:** Lint with usage check.
**Learned:** /plan, /review, /status-deep, /escalation-resolve all gained Usage: lines. /test-gen had a structured `Usage in chat: ...` line in its body but doesn't start with `Usage:` — the lint heuristic missed it. Both forms communicate the contract; the lint heuristic was overly strict.
**Change for cycle 4:** Either relax the lint heuristic to accept `Usage in chat:` form, or normalize /test-gen. Lean toward normalizing since consistency matters for human readers too.

## Cycle 4 (Usage: normalization)
**Tried:** Re-lint after normalizing /test-gen's Usage: line.
**Learned:** All 5 commands pass usage check now. Lint contract is consistent.

## Cycle 5 (final smoke)
**Result:** 5/5 commands have Usage: lines, lint passes. Verdict: **adopt** — already live, low cost to keep.
