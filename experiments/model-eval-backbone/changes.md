# Changes — model-eval-backbone (implementation gate)

All changes are confined to `experiments/model-eval-backbone/`. No root `<name>/`
dir, no edits outside the experiment folder.

## Files created

### `benchmark.py` (~430 lines)
Generation-side backbone benchmark. Replays N build specs through two Claude
models and writes comparable per-run metrics + a summary.

- `_env_float / _load_cost_model / _pricing_key / _cost` — $/MTok cost model with
  env overrides; substring model→bucket mapping (opus/sonnet/haiku/default);
  rejects negative/non-numeric costs at the env boundary.
- `load_specs(from_log_n)` — pinned 5-spec default (no file read) OR `--from-log N`
  reading `.harness/yolo_log.json`. **Catches `FileNotFoundError` and
  `json.JSONDecodeError`** and exits non-zero with a clear message (BUGS medium,
  plan attempt 1). Uses the `idea` field as the goal.
- `build_prompt(spec)` — strict-JSON envelope contract. **Wraps the untrusted goal
  in `<build_spec>…</build_spec>`, neutralizes forged delimiter tokens, frames the
  block as data-to-fulfil not instructions** (SECURITY high, plan attempt 1).
  Caps goal at 2000 chars.
- `parse_envelope(text)` — tolerant parse (bare / ```json fenced / first {...}).
  **Coerces `clarifying_questions` to a list (default []) before any `len()`** so a
  string/dict/int/null can never miscompute `clarification_count` — the accepted
  BUGS override from the prior escalation. Always returns
  `{"clarifying_questions": list, "html": str|None}`.
- `_safe_slug(raw)` — whitelist `[A-Za-z0-9._-]`, strip `..`/leading dots, reject
  empty. Path-traversal containment for untrusted slugs.
- `static_pass(html, slug)` — writes html to a sandboxed `_gen/<safe_slug>/` dir
  (`.resolve()`-checked under `_gen/`), runs `test_project` static checks
  (`extract_js`, `check_syntax`, `check_id_consistency`, `check_event_listeners`).
  Never executes html. Returns `{passed, detail}`.
- `run_one(spec, model_id, client, costs, max_tokens)` — one (spec×model) record;
  per-run try/except so a flaky call records `error` and the loop proceeds.
- `summarize(results)` — per-model pass rate, complete rate, mean clarifications,
  mean output tokens, total cost, mean wall time.
- `main()` — argparse (`--backbone`, `--candidate`, `--from-log`, `--limit`,
  `--max-tokens`, `--dry-run`, `--output`), orchestration, incremental JSON write,
  `_gen/` cleanup in a `finally`, stdout summary. Returns int exit code.

### `README.md`
Purpose, what-it-measures, quick-start, definition of "pass", how to add a spec,
cost model table, security/trust-boundary note, documented future extensions.

### `results.md`
Written after the live smoke + run (TESTS/OUTCOME gates).

## Verification already run
- `ast.parse` on benchmark.py → OK.
- `--dry-run` → prints 5×2 matrix, zero API calls, exit 0.
- `parse_envelope` unit cases (list/string/empty/null/int/dict/missing/fenced/prose)
  → all `len()` calls correct, never raises.
- `static_pass(cron-explain/index.html)` → `{passed: True}` (known-good self-check).
- `_safe_slug` on `../../etc`, `..`, `a/b/c`, `..\..\x` → all reduced to safe tokens.
