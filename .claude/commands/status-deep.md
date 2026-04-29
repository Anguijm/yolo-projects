Run the standard `status` report (see CLAUDE.md for the canonical shape) and
then append three additional sections sourced from disk at response time.

After the standard `## Session` block, add:

### Tick queue (full)
Read `session_state.json` -> `tick_tock.tick_queue_approved`. For each
entry, print:

```
- [<name>] <type>  source=<source_experiment>
  idea: <one-line idea field>
```

Cap at 10 entries; elide the rest with `… +N more`.

### Recent escalations (last 5 resolved)
Read `session_state.json` -> `council_escalations_resolved`. Sort by
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
