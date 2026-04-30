# Lessons — claude-headless

## Cycle 1 (DRY_RUN + simulated `claude` binary)
**Tried:** Replaced `claude` on PATH with a shell stub to simulate four
real-world response shapes: malformed JSON, is_error=true, success,
chain mid-failure.

**Learned:**
- DRY_RUN works: prints the planned command without executing it.
- All four real-execution paths behave correctly:
  - Malformed JSON → exit=1 with informative error to stderr.
  - is_error=true → exit=1, prints model's result for diagnosis.
  - Success → exit=0, prints turns + chars metadata + result.
  - Chain mid-failure → stops at the failing step, returns exit=1.
- The chain script correctly halts on first failure rather than
  pressing on with bad context.

**Gaps:**
- No retry path on transient failures (rate-limit, network blip). Real
  use will hit these; the current chain just fails.
- No timeout per step. A model that loops indefinitely with `--max-turns
  6` should be bounded by Claude itself but a wallclock backup matters.
- The chain passes the prior step's *full output* into the next step's
  prompt context. For long outputs this hits the prompt-length limit.
  No truncation logic.
- temp files (`/tmp/yolo_chain_<step>.txt`) are removed via trap, but
  if the script is killed with SIGKILL, they leak. Minor.

**Change for cycle 2:**
- Add a retry loop in yolo_step.sh: on exit 1 with a known transient
  error pattern (e.g., "rate limit"), wait + retry up to 3 times.
- Add a `--max-context-bytes` flag on chain_steps.sh; truncate prior
  output beyond the limit and log the truncation.
- Add a per-step timeout via `timeout` command.

## Cycle 2 (retry on transient + max-context truncation)
**Tried:** Stub claude returns 'rate limit' twice then succeeds. Stub claude emits 10KB output, chain runs with MAX_CONTEXT_BYTES=512.
**Learned:** Retry path works: 2s exp-backoff, attempt 2/4 succeeds. Truncation cuts 10KB prior output to 512B + truncation note.
**Change for cycle 3:** Add per-step timeout via `timeout` command. Also: capture how many retries each step needed in a `runs.jsonl`-style log so we can see which steps are flaky over time.

## Cycle 3 (operational space exhausted)
**Tried:** Same DRY_RUN as cycle 1.
**Learned:** No new lesson — operational space exhausted without a real `claude` CLI. All remaining behavior depends on real CLI semantics that the stub can't simulate (timeout interactions, multi-turn conversations, file edits inside Claude Code's tools).
**Change for cycle 4:** Skip — defer to real-cli validation which requires environment changes outside the experiment's scope.

## Cycle 4 (operational space exhausted)
**Learned:** Same DRY_RUN behavior. No new lesson available without real CLI.

## Cycle 5 (final smoke)
**Result:** DRY_RUN works; real CLI not available in sandbox. Verdict: **defer** validation until tested in a real Claude Code environment with live API.
