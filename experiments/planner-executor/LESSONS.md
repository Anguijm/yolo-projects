# Lessons — planner-executor

## Cycle 1 (baseline + validator + retry path)
**Tried:** Baseline pipeline (3-step plan executed cleanly), all 6
validator failure modes + 1 happy path, planner JSON-retry path with
mocked Claude returning garbage on first call.

**Learned:**
- All 7 validator cases pass: every malformed shape is rejected with a
  specific reason, valid shape passes.
- The planner retry works: when Claude returns non-JSON, the second
  call uses a stricter prompt and the validator accepts the (mocked)
  response.
- **The retry prompt is a single static string** ("Return ONLY valid
  JSON. Your previous response was not JSON.") — it doesn't include
  the bad output for diagnosis. A real planner would benefit from
  seeing what it produced last time.
- **No retry on validation failure**, only on JSON parse failure. If
  the planner returns valid JSON with the wrong shape (missing `files`
  on a step), the retry prompt at line 119 attempts a corrected plan
  — wait, actually it does (line 119: "Your previous plan was invalid:
  {reason}. Return a corrected plan as JSON."). Confirmed by reading
  the source: validation failures DO get a retry. Misread initially.
- The executor calls Codex once per step, but doesn't pass *prior step
  outputs* into subsequent steps. If step-2 needs the diff from step-1,
  the current pipeline doesn't provide it.

**Change for cycle 2:**
- Include the bad output in the retry prompt: "Your previous output
  was: <verbatim>. It failed because: <reason>. Return a corrected
  plan."
- After each executor step, accumulate its diff into a "context" field
  passed into subsequent steps. Steps that depend on each other need
  the prior diff to be coherent.
- Add a `--max-retries` CLI arg so the validator strictness can be
  tightened or loosened from the command line.

## Cycle 2 (retry includes prior raw + step accumulation)
**Tried:** Forced JSON parse failure; verified step-2 receives step-1's diff.
**Learned:** Retry prompt now includes the bad raw output (helpful for the planner to self-correct). Executor accumulates prior diffs and passes them into subsequent steps' user prompts. Step independence is no longer assumed.
**Change for cycle 3:** Add an option to verify the success_criterion of each step against the diff (e.g., does the diff actually add a /healthcheck handler, or just gesture at it?). Today the criterion is a string; making it programmatic is the next step.

## Cycle 3 (3-step accumulation verified)
**Tried:** Mocked codex; ran a 3-step plan; inspected each user prompt.
**Learned:** Call 1 has no PRIOR STEP DIFFS section (correct — first step). Calls 2 and 3 both include the section and contain prior diffs. Accumulation works as designed.
**Change for cycle 4:** Operational space exhausted at the orchestration layer. Programmatic success-criterion verification (proposed in cycle 2) is a real feature not a measurement — defer.

## Cycle 4 (smoke)
**Tried:** Standard run.
**Learned:** No regressions. Operational space exhausted at the orchestration layer.

## Cycle 5 (final smoke)
**Result:** 3-step plan validated and executed; retry path includes raw output; step accumulation works. Verdict: **iterate** — orchestration sound; plan-quality validation needs real model.
