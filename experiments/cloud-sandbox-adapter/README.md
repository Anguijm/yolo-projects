# cloud-sandbox-adapter

Source: Phase 4 experiment `mlops-2026-04-27-agents-software-dev-cloud`
(MLOps, 2026-04-27).

## Hypothesis
Running each YOLO loop iteration inside an ephemeral cloud sandbox (Modal,
E2B, Daytona) gives clean state, network isolation, and elastic compute per
run. The cost is rewriting environment setup, file I/O, and git operations
around remote ephemeral instances.

## What this delivers
The smallest abstraction that makes the rewrite tractable: a
`SandboxAdapter` interface plus two implementations.

- `LocalSandbox` — current behavior, runs commands in the local working
  directory. Useful baseline + matches today's loop.
- `DryRunSandbox` — records what would be sent to a remote provider
  without executing anything. The output of a dry run is the migration
  audit: every command and every file write the loop would issue.

A real `E2BSandbox` / `ModalSandbox` adapter would slot in by implementing
the same three methods. The rest of the loop never changes.

## Why this shape
The interface is intentionally tiny — `create() / exec(cmd) / write(path,
contents) / read(path) / teardown()`. Anything more ambitious (file syncing,
incremental snapshots, port forwarding) is a follow-on tick. This experiment
is to validate that the loop's existing shell-out call sites can be
mechanically rewritten to go through the adapter.

## Usage

```
python3 sandbox_adapter.py demo            # runs the demo against LocalSandbox
python3 sandbox_adapter.py demo --dry-run  # records the trace via DryRunSandbox
```

## Files
- `sandbox_adapter.py` — interface + two adapters + demo (~140 LOC).
- `MIGRATION.md` — list of call sites in the YOLO loop that need rewriting
  before a remote adapter is viable, plus a dependency graph.
