# pydantic-agents-production-optimisation

A research scaffold for tightening one council angle's parse-and-validate
path using Pydantic models, adopted from the Pydantic-AI production-optimization
talk.

**Status:** scaffold — schema + parser + replay-based A/B protocol. The
actual rollout into `.harness/scripts/council.py` is a follow-on tick once
the comparison run confirms the path is worth the dependency.

## The argument we're testing

The Pydantic-AI talk's claim: bounded retries + Pydantic-validated outputs
+ per-call cost ceilings turn flaky LLM calls into reliable production
primitives. Our council pipeline is exactly that domain — each angle
(`bugs`, `lessons`, `security`, etc.) emits a JSON Verdict that the runner
parses, and parse failures already fall through to "phantom OBJECT" via
the parse-failure-retry rule in `.harness/scripts/council_rules.md`.

The hypothesis: replacing the ad-hoc parse path with a Pydantic-validated
one produces **clearer errors**, **fewer phantom OBJECTs**, and a
**reusable contract** that anyone authoring a new persona can lean on.

## Scope

In scope for this scaffold:
- `verdict_schema.py` — Pydantic models for the per-angle Verdict
  (verdict, severity, reason, required_fix, evidence), matching the
  exact field set in `.harness/scripts/council_rules.md`.
- `parse_with_pydantic.py` — drop-in replacement for the parse path:
  takes raw model output, attempts JSON parse, then Pydantic validation,
  returns either a typed `Verdict` or a structured `ParseError` with
  diagnosable failure reason.
- `comparison_protocol.md` — the A/B test recipe. Replay raw council
  outputs from existing logs through both parsers (old and new), tally
  parse-success rates, and surface cases where the new parser would
  have caught issues the old one let through.

Out of scope:
- Touching `.harness/scripts/council.py` (the integration is a follow-on
  tick — we want the comparison data first).
- The Pydantic-AI agent framework itself. We adopt only the
  schema-validation pattern; not the agent runtime, not the tool model.
- Refactoring all 7 angles. This scaffold validates one schema; rollout
  is per-angle in follow-on ticks.

## Why one angle is enough

The council's Verdict schema is **uniform across angles** — every angle
emits the same JSON shape (`verdict`, `severity`, `reason`, etc.). A
schema that works for one works for all. The reason this scaffold scopes
to one angle is the **A/B test**, not the schema: rerunning every angle
against historical logs is overkill when one angle gives a clear
signal of whether the validation path catches real failures.

We choose `bugs` because it's the angle most prone to hallucination
(see the BUGS hallucination auto-downgrade rule in `council_rules.md`),
so its raw outputs are most likely to contain malformed or surprising
JSON.

## Files in this directory

- `README.md` — this file
- `verdict_schema.py` — Pydantic Verdict + ParseError models
- `parse_with_pydantic.py` — parse-and-validate function
- `comparison_protocol.md` — A/B test recipe for replay-based comparison

## Running the demo

```bash
cd experiments/pydantic-agents-production-optimisation
python3 -m pip install --quiet pydantic
python3 parse_with_pydantic.py --demo
```

The `--demo` flag runs 6 canned inputs (3 good, 3 broken in different
ways) through `parse_verdict()` and prints the result classification —
demonstrating that the validation path returns structured errors
instead of swallowing failures.

## Follow-on ticks this enables

1. **Execute the A/B comparison** (`comparison_protocol.md`) on 50
   historical raw outputs from `.harness/yolo_log.json` and report
   parse-success rate delta.
2. **Wire `parse_with_pydantic.parse_verdict` into council.py** for
   the `bugs` angle only, behind a `COUNCIL_USE_PYDANTIC=1` env flag.
   Run one week shadow-mode (call both parsers, compare outputs in log).
3. **Promote to all 7 angles** if shadow mode shows ≥95% agreement
   and clearer error messages on disagreements.
