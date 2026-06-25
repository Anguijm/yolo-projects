# Plan — model-eval-backbone

## Goal
Build a runnable harness that replays N historical YOLO build specs through two
Claude models (current generation backbone vs. a candidate model) and produces a
data-grounded promote / keep / mixed recommendation for the tick/tock generation backbone.

## Scope
**In scope**
- `experiments/model-eval-backbone/benchmark.py` — the replay harness (~150–200 lines).
- `experiments/model-eval-backbone/README.md` — how to run, how to add specs, what "pass" means.
- `experiments/model-eval-backbone/results.md` — per-spec table + summary stats + a real recommendation grounded in a live 5-spec run.
- A timestamped `benchmark_results_<TS>.json` raw record (written by the run).

**Explicitly NOT in scope**
- Replaying the **council reviewer** model. That is a *different* axis and is
  already covered by `experiments/eval-opus-47-backbone/` (it swaps `council.CLAUDE_MODEL`
  and runs gates on fixtures). This experiment swaps the **generation** model — the
  one that *produces* the artifact from a build spec — and never touches council backend state.
- "Council retry count per gate" as a metric. The adoption rationale floated it, but
  `plan_summary` narrowed the pass signal to "re-run test_project.py against the generated
  artifact". Running 4×7 council gates per (spec×model) would 56× the token cost for marginal
  signal. Pass/fail uses test_project's static checks (see Test Strategy). Council-retry replay
  is logged in README as a documented future extension.
- Changing the live tick/tock backbone. This produces a *recommendation*; promotion is a
  separate human decision.
- Any new framework dependency. Uses the already-present `anthropic` SDK only.

## Approach
Subtasks, in dependency order:

1. **Spec set (no deps).** Pin a default list of 5 historical single-file YOLO tools that
   (a) have a recorded goal in `.harness/yolo_log.json` and (b) still have a `<project>/index.html`
   on disk to anchor "what good looked like". Chosen for diversity of build skill:
   - `cron-explain` (expression parser + plain-English)
   - `url-dissect` (parse + encoding audit)
   - `uuid-inspector` (binary/timestamp decode)
   - `svg-fields` (DOM templating from markers)
   - `semver-range` (range logic + PASS/FAIL evaluation)
   A `--from-log N` flag instead auto-selects the N most recent logged builds whose project dir
   has an `index.html`, so the set stays maintainable as the portfolio grows.

2. **Two-model config (deps: none).** `--backbone` (default `claude-sonnet-4-6`) and
   `--candidate` (default `claude-opus-4-8`), both reachable via the one `ANTHROPIC_API_KEY`.
   Framing: is the more expensive candidate worth promoting over the current backbone for
   single-shot artifact generation? Model ids are CLI-overridable so the harness outlives any
   single model generation.

3. **Robust clarification metric (deps: 2).** Each generation prompt instructs the model to
   reply with **strict JSON**: `{"clarifying_questions": [...], "html": "<full document or null>"}`.
   `clarification_count = len(clarifying_questions)`. This makes "clarification request count"
   deterministically measurable (the council's IMPLEMENTATION concern) instead of scraping prose
   for question marks. A model that asks zero questions and emits HTML scores 0; one that punts
   with questions and `html: null` scores N and is marked `incomplete`.

4. **Run + metrics (deps: 1,2,3).** For each (spec × model): one `messages.create` call,
   capped `max_tokens`. Capture: `clarification_count`, `output_tokens`, `input_tokens`,
   `wall_s`, `completed` (parseable JSON with non-null html), `cost_usd`, and `passed`
   (test_project static checks on the generated html). Module-level token/cost helpers reused
   in spirit from `eval-opus-47-backbone/benchmark.py`.

5. **Pass/fail (deps: 4).** Write generated html to a temp dir under the experiment folder,
   import `test_project` and call its static checkers directly (`extract_js`, `check_syntax`,
   `check_id_consistency`, `check_event_listeners`) — no Playwright/browser dependency, fully
   deterministic in cron. `passed = syntax OK and no missing ids and no missing listeners`.

6. **Aggregate + emit (deps: 4,5).** JSON raw record + a markdown summary block printed to
   stdout. `results.md` is hand-authored from the live run with mean clarification count,
   pass-rate delta, mean output tokens, cost delta, and a promote/keep/mixed verdict.

## File Layout
- `experiments/model-eval-backbone/benchmark.py` — NEW (~150–200 lines).
- `experiments/model-eval-backbone/README.md` — NEW (~70 lines).
- `experiments/model-eval-backbone/results.md` — NEW (~60 lines), written after the live run.
- `experiments/model-eval-backbone/benchmark_results_<TS>.json` — NEW, run output.
- `experiments/model-eval-backbone/changes.md` — NEW, implementation-gate context.
- No files outside `experiments/model-eval-backbone/` are touched. No root `<name>/` dir created.

## Function Map
`experiments/model-eval-backbone/benchmark.py`:
- `_env_float(name, default) -> float` — validated non-negative float env override (cost model).
- `_load_cost_model() -> dict` — per-model $/MTok table with env overrides.
- `_cost(model_id, in_tok, out_tok, costs) -> float` — dollar cost of one call.
- `_pricing_key(model_id) -> str` — map a model id to its cost bucket (sonnet/opus/haiku/default).
- `load_specs(from_log_n) -> list[dict]` — build the replay spec set (pinned default or `--from-log`).
- `build_prompt(spec) -> str` — generation instruction with the strict-JSON envelope contract. The
  untrusted spec goal text is embedded inside an explicitly-delimited `<build_spec>…</build_spec>`
  block (with any literal `<build_spec`/`</build_spec>` occurrences in the goal neutralized) and the
  system framing states that the delimited content is a task description to *fulfil*, never
  instructions to the assistant — prompt-injection containment (SECURITY high objection, attempt 1).
- `parse_envelope(text) -> dict` — tolerant parse of the model's JSON reply (fenced/bare). **Coerces
  `clarifying_questions` to a list (default `[]`) before any `len()`** so a non-list value (string,
  dict, null) can never miscompute `clarification_count` — the ACCEPTED BUGS override from the prior
  escalation. Always returns `{"clarifying_questions": list, "html": str|None}`.
- `load_specs(from_log_n)` reads `.harness/yolo_log.json` only when `--from-log` is given; it catches
  `FileNotFoundError` and `json.JSONDecodeError`, prints a clear stderr message, and exits non-zero
  rather than crashing with a traceback (BUGS medium objection, attempt 1).
- `_safe_slug(raw) -> str` — sanitize a spec slug to `[A-Za-z0-9._-]` only (strip `/`, `..`, leading dots) before any path use; reject empty result. Prevents path traversal from untrusted `yolo_log.json`/CLI-derived slugs.
- `static_pass(html, slug) -> dict` — write html to a temp dir built from `_safe_slug(slug)` only, run test_project static checks, return {passed, detail}.
- `run_one(spec, model_id, client, costs, max_tokens) -> dict` — one (spec×model) record.
- `summarize(results) -> dict` — per-model aggregates + verdict heuristic.
- `main() -> int` — argparse (`--from-log`, `--limit`, `--backbone`, `--candidate`, `--max-tokens`, `--dry-run`, `--output`), orchestration, JSON write, stdout summary.

## Security
- Trust boundary: model output is **untrusted**. Generated html is written only to a temp dir
  *inside* the experiment folder and is **never** opened in a browser or executed — only parsed
  by static checkers (AST/regex). No `eval`, no network fetch of generated content.
- **Prompt injection (SECURITY high, attempt 1):** the build-spec goal text is sourced from
  `.harness/yolo_log.json` / CLI and is therefore untrusted input flowing *into* the prompt.
  `build_prompt` contains it inside an explicit `<build_spec>…</build_spec>` delimiter, neutralizes
  any literal delimiter tokens in the goal so the boundary can't be forged, and the surrounding
  instruction states the delimited block is a task to fulfil, not commands to obey. Residual risk is
  low (the corpus is our own historical build log, not third-party input) and the blast radius is a
  single low-quality benchmark run — never code execution or data exfiltration, since output is only
  statically parsed. Documented as a known limitation in the README rather than claimed airtight.
- **Slug sanitization (path traversal):** spec slugs come from `yolo_log.json` / `--from-log` /
  CLI and are therefore untrusted. `_safe_slug` whitelists `[A-Za-z0-9._-]`, strips any `/` and
  `..` sequences and leading dots, and rejects an empty result before the slug is used to build a
  temp dir path. The temp root is a fixed `_gen/` dir inside the experiment folder; the final path
  is additionally `.resolve()`-checked to stay within that root (defense in depth).
- Output path is validated to stay within repo root (reuse of the prior benchmark's guard) to
  prevent path-traversal via `--output`.
- API key read from env only; never logged. The generated artifacts are throwaway and the temp
  dir is cleaned at the end of each run.
- No secrets written to `results.md` or the JSON record (only token counts, costs, verdicts).

## UI
CLI tool. States:
- **Normal:** progress line per run (`run i/N: slug × model`), then a summary table to stdout.
- **Dry-run:** prints planned (spec×model) matrix and the output path, makes zero API calls, exits 0.
- **Error — no key:** clear stderr message + exit 1.
- **Error — bad envelope:** that run is recorded `completed=false` with the raw text truncated; the
  run continues (one flaky generation must not abort the whole benchmark).
- `--help` lists every flag (GUIDE objected to a missing `--help` on the prior benchmark — included here).

## Guide
- README opens with one-line purpose, a "What it measures" list, quick-start commands (dry-run,
  single spec via `--limit 1`, full run, custom model pair), the explicit **definition of "pass"**,
  how to add a spec, and the cost-model edit point.
- `--help` epilog mirrors the module docstring.

## Edge Cases
- Model returns prose, not JSON → `parse_envelope` returns `{clarifying_questions: [], html: None}`, run marked `completed=false`.
- Model returns `html: null` with questions → `completed=false`, `clarification_count>0` (a "punt").
- Generated html missing `<script>` → `static_pass` returns passed=false with reason (mirrors test_project).
- `--limit` larger than spec set → clamped to set size; `--limit 0` or negative → clamped to 1.
- A fixture's project dir was deleted → spec still replays (artifact-on-disk is only documentation, not required at runtime); README notes this.
- `.harness/yolo_log.json` missing or malformed (only read under `--from-log`) → `load_specs` catches `FileNotFoundError`/`json.JSONDecodeError`, prints a clear stderr message, exits non-zero. The pinned default spec set needs no file read, so the default path never crashes on a bad log.
- Build-spec goal text contains injection-style content or a forged `</build_spec>` delimiter → `build_prompt` neutralizes literal delimiter tokens and the model is framed to treat the block as a task spec; worst case is one degraded run, not execution.
- One model id invalid / API error on one call → that run recorded with `error` field, others proceed.
- Temp dir collision across specs → per-(`_safe_slug(slug)`,model) subdir under a fixed `_gen/` root, removed in a `finally`.
- Malicious/odd slug from `yolo_log.json` (e.g. `../../etc`) → `_safe_slug` reduces it to a safe token or rejects it; no path escapes `_gen/`.

## Test Strategy
1. **Static:** `python3 -c "import ast; ast.parse(open('experiments/model-eval-backbone/benchmark.py').read())"`.
2. **Dry-run:** `python3 benchmark.py --dry-run` prints the 5×2 matrix, zero API calls, exit 0.
3. **End-to-end smoke (council TESTS focus):** `python3 benchmark.py --limit 1` runs ONE spec ×
   both models, verifying both runs complete with comparable records (same keys, real token counts).
4. **Full run for results.md (OUTCOME focus):** all 5 specs × 2 models, real metrics, written to
   `results.md` with a promote/keep/mixed verdict grounded in the numbers.
5. **Pass/fail self-check:** `static_pass` is validated against a known-good on-disk fixture
   (e.g. `cron-explain/index.html` must score passed=true) during the smoke run.
