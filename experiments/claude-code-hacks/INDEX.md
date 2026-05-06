# Slash command index

Project-scoped commands at `.claude/commands/`. Each is a markdown prompt
that Claude Code loads when the user types `/<filename>` in a session.

| Command | Purpose |
|---|---|
| `/plan` | Produce structured `plan.md` for the current task using the council PLAN gate's required sections. |
| `/review` | Review pending diff against `main` with the council rubric (no full pipeline run). |
| `/test-gen` | Generate pytest cases for a target file or function and run them. |
| `/status-deep` | Standard `status` plus tick queue, recent escalations, and recent council outcomes. |
| `/escalation-resolve` | Walk through clearing an active `COUNCIL_ESCALATION.md`. |

To add another command: drop a new `.md` file in `.claude/commands/`. The
filename (sans extension) becomes the slash name. Keep prompts concrete:
state file paths, expected outputs, and stop conditions.
