# deterministic-script-verification

A research scaffold for catching silent-output-regression bugs in YOLO's
council and cron scripts, motivated by the May 2026 card-generator
silent-truncation incident.

**Status:** scaffold — protocol + working `verify.py` + one fixture. Wiring
into CI is a follow-on tick.

## The incident this was born from

`scripts/process_experiments.py` quietly produced **0 cards from 25
transcript-rich videos** for several daily cron runs. Root cause:
`max_tokens=4000` on the Anthropic call truncated the JSON output mid-stream;
the broad `except Exception as e: print(...)` swallowed the resulting
`json.JSONDecodeError`; the cron logged "Added 0 experiment cards" and
moved on. No alert fired because, from the workflow's perspective, the
script succeeded.

The PR that fixed the symptom (#8) bumped `max_tokens` to 16000 and added
branched exception handling that prints the truncated doc. That fix is
necessary but not sufficient — it catches **that** failure mode loudly, not
the next analogous one.

This experiment proposes the next layer: **golden-fixture verification.**
Pin the *shape* (not the content) of each script's output. When the shape
drifts — too few items, missing required keys, type mismatch — the verifier
fails the run loudly before bad output reaches the artifact.

## Scope

In scope for this scaffold:
- `verify.py` — a reusable verifier that takes a generator command + an
  input fixture + an expected-shape spec, runs the generator with the
  fixture as input, and asserts the output conforms.
- One worked example: `process_experiments.py` with a 5-video fixture
  scan and an expected-shape spec for the resulting JSON array of cards.
- `proposed_ci_check.yml` — a draft GitHub Actions job (not wired) showing
  how a follow-on tick would integrate verify.py into CI: stub-LLM check
  on every PR, real-LLM smoke test gated to manual dispatch.

Out of scope:
- Stubbing the Anthropic SDK (the worked example uses a `--stub` mode in
  `process_experiments.py` that doesn't exist yet — flagged as a follow-on)
- Wiring verify.py to CI (`proposed_ci_check.yml` is for review, not merge)
- Coverage for `fetch_youtube_rss.py` and `council.py` (next ticks)

## What the verifier checks

Three classes of assertion, applied to the parsed JSON output of the script:

1. **Top-level shape** — must be a JSON array (not object, not string).
2. **Count band** — `min_items` ≤ `len(output)` ≤ `max_items`. For
   process_experiments with 5 videos, expect 0–10 cards (1–2 per video,
   up to all-skipped if titles are commentary).
3. **Per-item required keys** — every item must contain the keys listed
   in `required_keys` with the type matching `key_types`. Missing or
   wrong-typed keys fail loud.

NOT checked:
- The literal text content of generated cards (LLM output is non-deterministic
  and we don't want to break on prose changes).
- Whether cards are "good" (that's the verdict step, downstream).

## Why this approach (over property-based testing)

Property-based fuzzing of LLM-driven scripts is a research project. Golden
fixtures are 30 lines of glue and catch the specific failure mode we just
hit. We can graduate to property-based later if shape-checks miss something.

## Follow-on ticks this enables

1. **Stub-LLM mode** in `process_experiments.py` — small refactor: accept
   `--stub` flag, when set, replace the `client.messages.create(...)` call
   with a fixture-driven response loader. Unblocks verify.py running in CI
   without spending API budget.
2. **Wire verify.py to CI** — copy `proposed_ci_check.yml` into
   `.github/workflows/`, run on every PR touching `scripts/`.
3. **Pin `fetch_youtube_rss.py`** — same pattern, but the verifier needs
   network-stubbing (mock the YouTube RSS feed). Slightly more setup.
4. **Pin `council.py` per-angle Verdict shape** — overlaps with the
   `pydantic-agents-production-optimisation` tick; coordinate.

## How to run the worked example

Today (manual):

```bash
cd experiments/deterministic-script-verification
python3 verify.py
```

It will print PASS/FAIL plus a diff of any deviations. The current
implementation runs against a **synthetic LLM response file** (since
`process_experiments.py` doesn't have a stub mode yet); this proves the
verifier itself works. The real-LLM path is what follow-on tick #1 enables.

## Files in this directory

- `README.md` — this file
- `verify.py` — the verifier
- `fixtures/process_experiments_input.json` — 5-video frozen input
- `fixtures/process_experiments_expected_shape.json` — expected-shape spec
- `fixtures/synthetic_llm_response.json` — known-good LLM output used to
  exercise verify.py without API spend
- `proposed_ci_check.yml` — draft GitHub Actions workflow
