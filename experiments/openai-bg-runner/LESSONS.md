# Lessons — openai-bg-runner

## Cycle 1 (baseline + perturbations)
**Tried:** 3-task drain, thread continuity (enqueue with explicit
thread_id), simulated crash (injected pending → in_progress half-state).

**Learned:**
- Baseline drain works. Each task gets its own auto-generated thread id;
  passing an explicit thread id at enqueue time is preserved through to
  drain.
- **Crash recovery is broken.** The drain command only picks up tasks
  whose current state is `pending`. A task that crashed mid-execution
  (`in_progress` but no terminal state) is silently skipped on the next
  drain. The injected `task_crash01` stayed `in_progress` forever.
- The status display shows the right counts but doesn't surface that an
  `in_progress` task is stale — there's no "stuck for N seconds"
  indicator.

**Change for cycle 2:**
- Drain should also pick up `in_progress` tasks whose last state-change
  is older than a threshold (default 60s). Treat them as "previously
  failed; retry once".
- Status should age-flag stuck `in_progress` tasks.
- Add a `reset` subcommand that explicitly converts stuck `in_progress`
  back to `pending`.

## Cycle 2 (stuck recovery)
**Tried:** Injected a stuck `in_progress` task with last-state-change >60s old, ran drain.
**Learned:** Stuck task is detected (status flags STUCK(119s)), auto-recovered to pending, drained successfully, ends in done. Recovery is logged ("recovering 1 stuck task(s)").
**Change for cycle 3:** Add a max-recovery-attempts counter so a task that crashes the worker repeatedly doesn't infinite-loop. After N recoveries → state=failed_repeatedly with a poison-pill marker.

## Cycle 3 (reset subcommand)
**Tried:** Manual `reset` of an in_progress task; verified status returns it to pending and drain picks it up.
**Learned:** reset works as documented. Counts go from {pending: 2, in_progress: 1} → {pending: 3} → {done: 3} after drain.
**Change for cycle 4:** Operational space largely exhausted. The remaining open question is rate-limit handling under real OpenAI API load — not testable without a key.

## Cycle 4 (smoke)
**Tried:** Standard enqueue + drain.
**Learned:** No regressions from cycles 1-3 changes. Operational space exhausted.

## Cycle 5 (final smoke)
**Result:** drain succeeds, thread continuity preserved. Verdict: **iterate** — needs real OpenAI key to validate Responses API thread persistence.
