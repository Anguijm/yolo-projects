# Handoff — claude-code-hacks

**Verdict (after 5 cycles):** adopt

**One-line:** Five live slash commands at .claude/commands/ for repeated YOLO loop operations.

## What this is
Project-scoped Claude Code commands at `.claude/commands/`:
- `/plan` — produce a structured plan.md matching the council PLAN gate.
- `/review` — review the pending diff against main using council rubric.
- `/test-gen` — generate pytest cases for a target file/function.
- `/status-deep` — extended `status` (tick queue + escalations + outcomes).
- `/escalation-resolve` — walk through clearing COUNCIL_ESCALATION.md.

## Why an agent might want to adopt this
- You're tired of re-prompting the same operations every session.
- You want the YOLO loop's high-frequency operations on one keystroke.
- You want a consistent contract (Usage: + numbered steps + failure paths)
  that other agents can extend.

## Production-ready bits
- All 5 commands have explicit `Usage:` lines after cycle 4.
- All 5 commands include numbered execution steps and failure-path notes.
- All 5 are under 250 words (well under the 500-word budget).
- Adding a new command is just dropping a new `.md` file.

## What still needs work
- The lint script lives in cycle test outputs; should be promoted to a
  permanent `.github/workflows/` step or a `verify_commands.py` next to
  `verify_build.py`.

## How to run
Just type `/<command-name>` in any Claude Code session in this repo.

## Files
- `.claude/commands/{plan,review,test-gen,status-deep,escalation-resolve}.md`
- `experiments/claude-code-hacks/INDEX.md` — one-line description per command

## Verdict: adopt. Already live.
