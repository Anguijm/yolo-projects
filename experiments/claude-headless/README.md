# claude-headless

Source: Phase 4 experiment `nh-2026-04-27-claude-code-headless-automation`
(NateHerk, 2026-04-27).

## Hypothesis
Invoking Claude Code via `claude -p "<prompt>" --output-format json`
(headless mode) inside YOLO loop shell scripts lets us chain plan →
implement → test → commit steps without an interactive UI.

## What this delivers
Two reference shell scripts that demonstrate the pattern.

- `yolo_step.sh` — runs a single headless Claude Code invocation, parses the
  JSON response, and prints a one-line summary with exit code reflecting
  success.
- `chain_steps.sh` — chains four steps (plan → implement → test → commit)
  by piping each step's output into the next step's prompt context. Stops
  on first failure.

Both scripts are dry-run safe: they print the command they'd run when
`DRY_RUN=1` is set, so you can review the chain without spending tokens.

## Usage

```
# single step
./yolo_step.sh "List the files in this directory"

# full chain (dry-run first)
DRY_RUN=1 ./chain_steps.sh add-readme "Write a one-paragraph README.md for this repo"

# real run
./chain_steps.sh add-readme "Write a one-paragraph README.md for this repo"
```

## Files
- `yolo_step.sh` — single-step wrapper.
- `chain_steps.sh` — multi-step pipeline.

## Notes
The scripts assume `claude` is on PATH. They use `--output-format json` so
downstream parsing is reliable. They use `--max-turns` to bound the agent
loop (default 6 turns per step).

The chain uses temp files (`/tmp/yolo_chain_<step>.txt`) to pass the prior
step's stdout into the next step's prompt context. Cleaned up on success.
