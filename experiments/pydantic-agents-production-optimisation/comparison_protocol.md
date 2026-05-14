# A/B comparison protocol — Pydantic-validated vs. ad-hoc parse path

## Goal

Decide whether to roll `parse_with_pydantic.parse_verdict` into
`.harness/scripts/council.py` for the `bugs` angle by comparing parse
success rates and error-message clarity against the current path,
**without spending API budget** on a fresh council run.

## Setup

Inputs are **historical raw Verdict outputs** captured by `council.py`
during cron runs. They live in `.harness/yolo_log.json` (one entry
per build) under the `council_raw_responses` key per angle.

If `council.py` doesn't currently persist raw responses, the prerequisite
follow-on tick is: add a `--debug-log-raw` flag that writes raw model
output to `.harness/raw_council_responses/{angle}/{timestamp}.txt`. That
ticket is small (~10 LOC) but blocking for this comparison.

For now, the protocol works against a hand-curated sample: 20 raw outputs
the user dumps from a recent cron log into `samples/` (gitignored).

## Procedure

1. **Collect 20 raw `bugs` outputs.** Mix of clean APPROVE, clean OBJECT,
   and at least 3 known-malformed (the ones that produced phantom OBJECTs
   in the past). Save under `samples/bugs/{001..020}.txt`.

2. **Run both parsers over each sample.**

   ```python
   # comparison_run.py — write as a follow-on; the skeleton is:
   from parse_with_pydantic import parse_verdict, Verdict, ParseError
   # importable shim around council.py's current parse function:
   from council_legacy_shim import legacy_parse  # to be written

   results = []
   for path in sorted(Path("samples/bugs").glob("*.txt")):
       raw = path.read_text()
       pydantic_result = parse_verdict(raw)
       legacy_result = legacy_parse(raw)
       results.append({
           "sample": path.name,
           "pydantic_ok": isinstance(pydantic_result, Verdict),
           "pydantic_detail": (
               pydantic_result.model_dump() if isinstance(pydantic_result, Verdict)
               else pydantic_result.model_dump()
           ),
           "legacy_ok": legacy_result is not None,
           "legacy_detail": legacy_result,
       })
   Path("comparison_results.json").write_text(json.dumps(results, indent=2))
   ```

3. **Tally these four counts** from `comparison_results.json`:

   | Pydantic | Legacy  | Meaning                                |
   |----------|---------|----------------------------------------|
   | OK       | OK      | Both parse cleanly — no signal         |
   | OK       | FAIL    | Pydantic recovered something Legacy lost (rare; flag for inspection) |
   | FAIL     | OK      | Legacy was lenient; check whether the "ok" was actually a phantom |
   | FAIL     | FAIL    | Both fail — but Pydantic explains why |

   The interesting cells are (FAIL, OK) and (OK, FAIL). Manually inspect
   each.

4. **Score error message quality** on the (FAIL, FAIL) and (FAIL, OK)
   rows: would the Pydantic `ParseError.detail` field have been more
   actionable in a cron log than the legacy path's silent phantom-OBJECT
   fallback? Score 1–3 per case; aim for average ≥2.5.

5. **Decide.** Go-criteria for the wire-it-up follow-on:
   - Pydantic parses ≥ 95% of clean inputs cleanly.
   - Pydantic error messages average ≥2.5 / 3 on the failure cases.
   - No (OK, FAIL) cases where Pydantic accepted something the legacy
     path correctly rejected.

## What this protocol deliberately does not measure

- **Council verdict quality.** Whether the Pydantic path changes the
  final tick_tock verdict is downstream of parsing — it's a separate
  question. We're testing parser robustness, not council judgement.
- **Latency.** Pydantic validation is microseconds; not worth measuring
  against API call time.
- **API cost.** Identical (zero net change — we're not adding LLM calls).

## Why offline replay is enough

The interesting question is "does the new parser disagree with the old
one on inputs we've already seen, in ways that matter?" That's
answerable from logs. A live A/B would only add noise (model variance,
network jitter) without changing the answer.
