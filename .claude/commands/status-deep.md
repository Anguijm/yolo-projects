---
scope: project
---
Usage: `/status-deep` (no args)

Run the standard `status` report (see CLAUDE.md for the canonical shape) and
then append three additional sections sourced from disk at response time.

Steps:

1. Run the standard `status` and emit it verbatim.
2. After the standard `## Session` block, append the three sections below in order.
3. Apply the live-reads-only rule from CLAUDE.md (no caching, no recall).
4. If a source file is missing, render the section's value as `unknown` rather than `0` or empty.

The three sections to append:

### Tick queue (full)
Read `.harness/session_state.json` -> `tick_tock.tick_queue_approved`. For each
entry, print:

```
- [<name>] <type>  source=<source_experiment>
  idea: <one-line idea field>
```

Cap at 10 entries; elide the rest with `… +N more`.

### Recent escalations (last 5 resolved)
Read `.harness/session_state.json` -> `council_escalations_resolved`. Sort by
resolution timestamp descending, take the top 5. For each:

```
- <project> · <gate> · <date>  →  <resolution_summary first 80 chars>
```

If the list is empty say "(no resolved escalations recorded)".

### Recent council outcomes (last 5)
Walk `experiments/*/council_outcome.json` and pick the 5 newest by file
mtime. For each:

```
- <experiment> · <verdict> · <date>
```

All three sections obey the live-reads-only rule. If a source file is
missing, render the section with `unknown` rather than zeros.
