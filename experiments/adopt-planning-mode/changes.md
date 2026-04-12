# Changes: adopt-planning-mode

## File modified
`.github/workflows/tick_tock_prompt.md`

## Change 1 — Main PLAN gate (lines ~74-88, now ~74-100)

**Before:**
```
Write your plan to `<project>/plan.md` (vertical outline: goal, scope, approach, file layout, test strategy).
```

**After:**
```
Use **structured planning mode** to write `<project>/plan.md`. The plan must enumerate each file that will be touched and each function that will be added/modified before any code is written. Decompose the work into named subtasks, note dependencies and sequencing between subtasks, and make the breakdown specific enough that a reviewer can verify completeness without running the code.

**Required sections (all must be present for council review):**
- `## Goal` — one-liner objective
- `## Scope` — what's in scope and explicitly what is NOT
- `## Approach` — narrative; subtasks with sequencing/dependencies noted
- `## File Layout` — every file touched, with approximate line range if modifying existing
- `## Function Map` — every function added or modified, grouped by file path; write "N/A — no functions added/modified" for markup-only or config-only changes (required for all builds)
- `## Security` — threat model, CSP notes, trust boundaries
- `## UI` — interaction design, empty/loading/error states
- `## Guide` — user-facing copy, labels, placeholder text
- `## Edge Cases` — boundary conditions, error states, empty states
- `## Test Strategy` — how the build will be verified
```

## Change 2 — Infrastructure PLAN gate (lines ~145, now ~157)

**Before:**
```
- **PLAN gate**: write `experiments/<name>/plan.md` (detailed plan), then run `python3 council.py ...`.
```

**After:**
```
- **PLAN gate**: use **structured planning mode** to write `experiments/<name>/plan.md`. The plan must enumerate each file that will be touched and each function that will be added/modified before any code is written. Required sections: Goal, Scope, Approach (with subtasks and sequencing), File Layout, Function Map, Security, UI, Guide, Edge Cases, Test Strategy. Then run `python3 council.py ...`.
```

## Snapshot comparison (before vs after)

| Aspect | Before | After |
|---|---|---|
| Planning instruction | "vertical outline: goal, scope, approach, file layout, test strategy" | "structured planning mode" — imperative directive |
| File enumeration | Implicit in "file layout" | Explicit: "enumerate each file that will be touched" |
| Function enumeration | Not required | Explicit: "each function that will be added/modified" — `## Function Map` section |
| Subtask decomposition | Not mentioned | "decompose into named subtasks, note dependencies and sequencing" |
| Required sections | 5 informal labels | 10 named sections with descriptions, council-reviewable |
| Infrastructure gate | "detailed plan" | Same structured planning mode, same 10 sections |
