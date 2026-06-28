# Changes — infra-sweep-mode

Pure-producer sweep runner. No pipeline file touched; only the three declared
`deliverable_paths` created.

## Files created
- `sweep_runner.py` (~330 LOC) — repo root.
  - `_mini_yaml_load` / `_in_quote` / `_split_flow` — embedded YAML-subset parser (PyYAML absent in CI).
  - `load_spec` — prefer PyYAML, else mini-parser.
  - `validate_spec` — required keys; type enum; non-empty grid; **param-value charset guard**; **deliverable_path traversal/absolute/metachar guard**; placeholder-references-known-param check; max_runs/budget_cap sanity.
  - `enumerate_grid` — deterministic cartesian product (sorted keys).
  - `_slug` / `_subst` — safe name slug + `{param}` substitution (str + list).
  - `build_entries` — entry construction; **re-validates substituted paths**; enforces `max_runs` + ceiling clamp with warnings; stamps sweep metadata.
  - `enqueue` — **atomic** (temp + `os.replace`) **idempotent** (skip names already queued) merge into `tick_tock.tick_queue_approved`; refuses to create missing state.
  - `selftest` / `main` — CLI: `--spec --state --dry-run --date --selftest`.
- `experiments/infra-sweep-mode/sweep_spec_example.yaml` — worked example (eval-opus-47-backbone × 3 deliverables), YAML-subset-only.
- `experiments/infra-sweep-mode/README.md` — usage, schema, design rationale, safety guards.

## Council objections addressed (advisory — council never blocks the drain)
PLAN gate:
- **BUGS (read-modify-write corruption):** atomic temp+`os.replace`; idempotent re-run; intended to run cron-paused (documented), same constraint as `update_session_state.py`.
- **BUGS (budget_cap had no teeth):** added `effective_cap` — entries = `min(grid, max_runs, floor(budget_cap/est_cost_per_run))`; the binding constraint is named in the dropped-combo WARNING. New optional `est_cost_per_run` field (default $0.50).
- **SECURITY (`{param}` injection / parser surface):** param values restricted to a benign charset; `deliverable_paths` rejected on `..`/absolute/metachars both before and after substitution; mini-parser is a closed subset covered by `--selftest`.

IMPLEMENTATION + TESTS gates:
- **BUGS (unlocked read-modify-write → lost update vs cron):** `enqueue` now takes an exclusive `fcntl.flock` advisory lock across the whole read-modify-write (graceful no-op where fcntl/OSError; atomic `os.replace` still prevents corruption regardless). Lock file `<state>.lock`. Verified the lock is acquired and the file appears.
- **SECURITY (regex injection guard is incomplete):** acknowledged and documented as defense-in-depth, NOT a complete defense — specs are owner-authored (trust boundary). Advisory; logged.
- **BUGS (`#` in string values corrupted by mini-parser):** replaced naive `split('#')` with quote-aware `_strip_comment` (a `#` opens a comment only at line start / after whitespace and never inside quotes). Verified `"channel #3"` survives.
- **SECURITY (static LLM-facing text unvalidated):** `validate_spec` now scans `name`/`idea`/`rationale`/`council_focus`/`plan_summary` against `INJECTION_RE` (common injection phrasings) and rejects matches; verified no false positive on benign "context".
- **COOL (undifferentiated):** advisory/subjective lens for an infra queue-injection utility; logged, not chased — the signature move IS being a pure producer that needs no new runtime path.

## Verification (pre-build, all green)
- `ast.parse` OK; `--selftest` 7/7 PASS; `--dry-run` correct; idempotency verified (3 added → 0 added/3 skipped, JSON stays valid); validation rejects traversal + shell metachars (exit 2); cartesian product (2×3=6) + max_runs truncation warning verified.

## Not touched
`tick_tock.yml`, `council.py`, `update_session_state.py`, any project dir. No repo-root `infra-sweep-mode/` directory.
