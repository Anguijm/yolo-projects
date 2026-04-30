Usage: `/plan` (no args; operates on the current task in context)

Produce a structured `plan.md` for the current task at
`experiments/<task-name>/plan.md`. The file MUST have these sections in this
order, matching the council PLAN gate's expected structure:

1. `## Goal` — one sentence, what we're shipping.
2. `## Scope` — bullet list of in-scope and out-of-scope items. Be explicit
   about what this tick does NOT do.
3. `## Approach` — narrative of how the change works. 2–4 paragraphs.
4. `## File Layout` — every file the tick will create or modify, with a
   line-range estimate for modifications.
5. `## Function Map` — every function added or modified, with file path.
6. `## Security` — threat model, CSP notes, trust boundaries. Even if "no
   security implications" — say that explicitly and explain why.
7. `## UI` — interaction design (skip for pure infrastructure ticks; say
   "not applicable: infrastructure" rather than omitting).
8. `## Guide` — user-facing copy / labels (same caveat as UI).
9. `## Edge Cases` — error states, empty states, race conditions.
10. `## Test Strategy` — how the build will be verified. Concrete commands
    where possible.

Before writing, read `CLAUDE.md` in the repo root and any existing files in
`experiments/<task-name>/` so the plan is consistent with prior decisions.

Do not write any code. Plan only. End by stating the plan is ready for
council review.
