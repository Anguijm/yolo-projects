# Lessons — eval-harness

## Cycle 1 (baseline + bad agent + flaky agent + rubric sanity)
**Tried:** Stub agent (baseline 0.875), always-wrong agent (0.125),
flaky-with-exceptions agent (errors handled, 0.125), all rubric types
exercised with right/wrong inputs.

**Learned:**
- Each of the four deterministic rubric types (keyword, regex, exact,
  length) returns 1.0 on the correct case and 0.0 on the incorrect
  case — clean discrimination.
- **Flaky agent handling works correctly**: when the agent raises, the
  task records `error` and gets score=0; the harness keeps going.
  Errors don't take down the whole run.
- **Bad agent's score (0.125) is suspicious.** "idk" actually matched
  one rubric — `length-1` (which only checks 1 ≤ len ≤ 30, and "idk"
  is 3 chars). That's the rubric being too lax, not the agent being
  good. Length-only rubrics are nearly always trivially satisfied.
- The aggregate stat doesn't differentiate between "wrong answer" and
  "agent crashed". Both contribute 0; the difference matters for
  diagnosis.

**Change for cycle 2:**
- Add separate aggregate fields: `score_failed` (rubric mismatch) vs
  `agent_failed` (exception). Currently both are lumped into "1 - passed".
- Document the `length` rubric more explicitly — it's almost never
  meaningful as a sole rubric; it's an *additional* check on top of
  another rubric. Maybe rename to `length_check` and make it
  composable rather than primary.
- The LLM-judge rubric still falls back to keyword matching when no
  API key exists. Add a clearer warning to the report when fallback
  was used so a stub-driven score isn't mistaken for real LLM
  judgment.

## Cycle 2 (score_failed vs agent_failed split + degraded_mode)
**Tried:** Flaky agent (raises every 3rd call) + always-wrong responses.
**Learned:** Aggregate now shows score_failed=5, agent_failed=2 — clean separation. degraded_mode=True since LLM-judge rubric is in the suite but no key. Reports now self-document their stub-vs-real status.
**Change for cycle 3:** Add a stable-seed mode for the stub agent so reruns are bit-identical (currently the order of failures depends on call counter). Useful for snapshot tests of the eval harness itself.

## Cycle 3 (re-run, observe baseline)
**Tried:** Standard run on the 8 starter tasks + aggregate inspection.
**Learned:** 7/8 passed (the unanswerable Mars population task fails — by design). degraded_mode flag correctly fires due to the LLM-judge rubric without a real key. score_failed=1 / agent_failed=0 — clean attribution.
**Change for cycle 4:** Operational space exhausted on the deterministic rubrics. LLM-judge rubric needs a real key to validate.

## Cycle 4 (cross-experiment scoring of self-evolving-agent)
**Tried:** Score the seed and evolved prompts from self-evolving-agent's history.
**Learned:** Harness cleanly substitutes its agent function for an arbitrary system_prompt closure. Same harness, two prompts, two scores. **Differential scoring works** — a key building block for benchmarking prompt changes.

## Cycle 5 (final smoke)
**Result:** 7/8 pass on starter suite, score_failed=1, agent_failed=0, degraded=True. Verdict: **adopt** — use as the regression test for any prompt or model change; foundation for self-evolving-agent.
