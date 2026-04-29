# claude-code-hacks

Source: Phase 4 experiment `nh-2026-04-27-claude-code-hacks` (NateHerk,
2026-04-27).

## Hypothesis
A versioned `CLAUDE.md` plus a curated slash-command library for common YOLO
loop operations (`/plan`, `/review`, `/test-gen`, `/status-deep`) keeps
sessions on rails with less prompt re-engineering.

## What this delivers
A starter set of project-scoped slash commands at `.claude/commands/`. Each
file is a markdown prompt that Claude Code reads when the user types
`/<filename>` in a session. The CLAUDE.md at repo root already documents the
`status` convention; these commands extend that pattern to other recurring
operations.

The repo's existing CLAUDE.md is already well-structured (it's the source of
truth for the `status` shape). This experiment focuses on the slash-command
half of the hypothesis.

## Commands added
- `/plan` — produce a structured plan.md for the current task using the
  council PLAN gate's required structure.
- `/review` — review the pending diff (HEAD vs main) against the council
  rubric without running the full council.
- `/test-gen` — generate pytest cases for a target file or function.
- `/status-deep` — extended `status` that also reports tick queue contents,
  recent escalations, and recent council outcomes.
- `/escalation-resolve` — interactive helper for clearing
  `COUNCIL_ESCALATION.md` once a veto has been addressed.

## Why these five
They're the operations the YOLO loop actually repeats often enough that
re-prompting is friction. `/plan` is invoked at the top of every tick.
`/review` is invoked before commit. `/test-gen` is invoked once per build.
`/status-deep` is the every-session orientation step. `/escalation-resolve`
matches the most painful interrupt path in the loop.

## Files
- `.claude/commands/plan.md`
- `.claude/commands/review.md`
- `.claude/commands/test-gen.md`
- `.claude/commands/status-deep.md`
- `.claude/commands/escalation-resolve.md`
- `experiments/claude-code-hacks/INDEX.md` — pointer back to the commands
  with a one-line description of each.

## Validation
Type `/plan` (or any of the other four) in a Claude Code session in this
repo. The command file is loaded as the prompt. No code is required — the
deliverable is the prompts themselves.
