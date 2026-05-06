# YOLO loop call-site migration audit

This is the list of places in the loop that currently shell out, write
files, or read files directly. Each one would need to be rewritten to go
through `SandboxAdapter` before a remote cloud adapter is viable.

## Direct shell-outs

- `update_dashboard.py` — runs `git log` for recent commits.
- `verify_build.py` — runs `pytest` and `playwright test` against project
  directories.
- `council.py` — runs `git diff` to compute the change-set passed to gates.

## Direct file I/O

- Every `experiments/<name>/<deliverable>` write today goes to local disk.
  These would become `adapter.write(path, contents)` calls.
- `session_state.json` and `experiments.json` reads/writes happen across
  multiple modules; would need to be funnelled through a single
  `state_store` module that takes an adapter.

## Hard cases

- **Git history.** Cloud sandboxes are ephemeral; git operations need a
  remote (origin) reachable from the sandbox. Practically: every cloud run
  starts with `git clone` and ends with `git push`, with a stash in between
  for any uncommitted progress.
- **Long-running workers.** `bg_task_runner.py` (openai-bg-runner) and any
  daemon model don't fit the ephemeral-sandbox shape. They stay local or
  move to a dedicated long-lived deployment.
- **Phase 4 cron.** Already runs in GitHub Actions, which *is* an ephemeral
  cloud environment. Only the *interactive* tick/tock portion needs the
  rewrite; phase 4 ingestion is essentially already migrated.

## Dependency graph

```
session_state.json reads/writes
    ↓
council.py  ←  verify_build.py  ←  update_dashboard.py
    ↓
shell-outs (git, pytest, playwright)
    ↓
[adapter boundary — what we're inserting]
    ↓
LocalSandbox (today)  |  E2BSandbox / ModalSandbox (future)
```

The adapter boundary sits below council/verify/update — those modules don't
need to know whether they're running locally or remotely.

## Smallest-cut migration order

1. Introduce `state_store` module (single read/write surface for
   session_state.json + experiments.json).
2. Route shell-outs in `verify_build.py` through the adapter.
3. Route shell-outs in `council.py` through the adapter.
4. Add a real `E2BSandbox` adapter (probably the simplest of the three
   providers to wire up).
5. Run a single tick end-to-end through the new adapter on E2B.

Steps 1–3 are pure refactors that don't change behavior. Step 5 is the
moment of truth.
