# Handoff — claude-headless

**Verdict (after 5 cycles):** defer

**One-line:** Shell wrappers for non-interactive Claude Code, for chaining or scheduling.

## What this is
Two shell scripts that drive `claude -p "<prompt>" --output-format json`:
- `yolo_step.sh` — runs one prompt; parses JSON; surfaces success/error/turns;
  retries on transient errors with exponential backoff.
- `chain_steps.sh` — pipes plan → implement → test → commit, stopping on first
  failure. Supports MAX_CONTEXT_BYTES truncation of prior step output.

Both have `DRY_RUN=1` mode that prints the planned command without executing.

## Why an agent might want to adopt this
- You want to run YOLO loop steps from cron or CI.
- You want a chain of agent steps without an interactive UI.
- You want the failure mode to be "stop", not "press on with bad context".

## Production-ready bits
- DRY_RUN prints the exact command that would run.
- Retry with exp backoff (2s, 4s, 8s) on rate-limit / transient patterns.
- Configurable max context truncation between steps with logging.
- Validated against simulated `claude` stubs for: malformed JSON, is_error=true,
  success path, mid-chain failure, rate-limit retry.

## What still needs work
- Per-step timeout via `timeout` command not added yet.
- Retry counters not surfaced into a runs.jsonl-style log.
- **Crucially**: not validated against the real `claude` CLI in this sandbox
  (CLI not installed). All verification was against simulated stubs.

## How to run
```
DRY_RUN=1 ./yolo_step.sh "List files in this directory"
./chain_steps.sh add-readme "Write a README for this repo"
```

## Files
- `yolo_step.sh`, `chain_steps.sh`

## Verdict: defer. Re-validate in a real Claude Code environment with the live API.
