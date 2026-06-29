---
scope: project
---
Usage: `/review` (no args; reviews the current branch's diff against main)

Review the pending diff against `main` using the council rubric without
invoking the full council pipeline.

Run, in order:

1. `git fetch origin main` (don't assume main is current).
2. `git diff origin/main...HEAD` — capture the change set.
3. `git log origin/main..HEAD --oneline` — capture the commit history.

Then evaluate against these angles. For each, return APPROVE / OBJECT plus a
one-line reason. If OBJECT, cite the offending file and line.

- **PLAN consistency** — does the diff match the deliverable_paths /
  Function Map in `experiments/<task>/plan.md`?
- **BUGS** — read each modified function. Are there clear logic errors,
  off-by-ones, undefined references, or unhandled exceptions on real paths?
- **SECURITY** — any new external input parsed without sanitization? Any
  `subprocess` shell=True with user input? Any new auth or trust boundary?
- **TESTS** — is there at least one test case per modified function, or is
  there a documented reason there isn't?
- **LESSONS** — does the diff repeat a mistake recorded in `.harness/learnings.md`?
  (cite `file:line` from .harness/learnings.md if so).

End with a one-paragraph summary: ship / iterate / block, with the single
biggest concern named.
