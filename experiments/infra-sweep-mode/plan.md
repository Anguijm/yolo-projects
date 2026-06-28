# Plan — infra-sweep-mode

## Goal
Ship `sweep_runner.py`: a dependency-free producer that reads a sweep spec, enumerates a parameter grid (cartesian product), and enqueues N parameterized tick specs into `tick_tock.tick_queue_approved` so the existing YOLO loop drains them one-per-tick through the normal 4 council gates.

## Scope
**In scope** (exactly the three declared `deliverable_paths`):
- `sweep_runner.py` — the enumerator/enqueuer (~230 LOC incl. embedded minimal YAML-subset parser + selftest).
- `experiments/infra-sweep-mode/sweep_spec_example.yaml` — a realistic worked example.
- `experiments/infra-sweep-mode/README.md` — usage + design rationale.

**Explicitly NOT in scope:**
- No execution of ticks. `sweep_runner.py` does NOT invoke `council.py`, does NOT run builds, does NOT call any LLM. It only writes queue entries; the existing loop runs them. (Answers PLAN council_focus — see Approach.)
- No changes to `tick_tock.yml`, `council.py`, `update_session_state.py`, or any other pipeline file.
- No new third-party dependency. PyYAML is NOT installed in CI; the runner must work without it.
- No `infra-sweep-mode/` directory at repo root (infra ticks live only under `experiments/`).

## Approach
**Integration point (PLAN council_focus: tick-queue injection vs invoking council.py directly).**
Decision: **tick-queue injection.** The YOLO loop already drains `tick_queue_approved` one item per cron slot, running each through all 4 gates with the per-tick commit/push discipline defined in `CLAUDE.md`. If `sweep_runner` invoked `council.py` itself it would have to re-implement the entire gate sequence, context injection, pre-filter, and commit protocol that lives in the workflow + orchestrator — duplicating the hottest path and bypassing per-tick isolation. Keeping `sweep_runner` a pure *producer* (enumerate grid → append valid queue entries) means: (a) each generated tick gets the full, unmodified council treatment for free; (b) the runner is trivially testable with a dry-run (no API, no side effects); (c) a sweep is just "N normal ticks", so nothing downstream needs to know sweeps exist.

**Spec format & parsing (no PyYAML).**
The spec is YAML for human authorability, but PyYAML is absent in CI. Strategy: `import yaml` if available (preferred), else fall back to an embedded `_mini_yaml_load` that handles exactly the documented subset — top-level scalars, one level of nested mapping, block sequences (`- item`), and inline flow lists (`[a, b, c]`). The subset is small, closed, and covered by `--selftest`. JSON is a strict subset of YAML, so a `.json` spec also parses via the same path when PyYAML is present; the mini-parser additionally accepts JSON-style inline lists.

**Spec schema:**
```yaml
sweep_id: <stable id for this sweep>
base_tick:
  name: <base name>
  type: infrastructure | yolo | experiment
  idea: <one-liner>
  rationale: <why>
  council_focus: <focus text>
  plan_summary: <summary; "{param}" placeholders substituted per combo>
  deliverable_paths: [<path with optional {param} placeholders>, ...]
param_grid:
  <param_a>: [v1, v2, ...]
  <param_b>: [v1, v2, ...]
max_runs: 10        # hard cap on generated entries (safety)
budget_cap: 5.0     # USD; recorded per entry + sweep-level guard
```

**Enumeration.** Cartesian product of `param_grid` values (sorted key order for determinism). Each combo produces one queue entry derived from `base_tick`:
- `name` = `<base_tick.name>--<k1>_<v1>__<k2>_<v2>` (filesystem/queue-safe slug).
- `plan_summary` / `deliverable_paths` strings get `{param}` placeholders substituted from the combo.
- Each param appended as `param_<k>=<v>` to `plan_summary` (per `plan_summary` spec).
- Added fields: `sweep_id`, `sweep_run` (1-based index), `sweep_total`, `budget_cap`, `queued_date` (passed in via `--date`, since `Date.now()` is unavailable in the harness; CLI default uses real `datetime` when run normally).

**Subtasks & sequencing:**
1. `_mini_yaml_load` + `load_spec` (prefer PyYAML, fall back). (no deps)
2. `validate_spec` — required keys, types, `max_runs`/`budget_cap` sane, non-empty grid. (depends 1)
3. `enumerate_grid` — cartesian product, deterministic order. (depends 2)
4. `build_entries` — placeholder substitution + slug + field stamping; enforce `max_runs`. (depends 3)
5. `enqueue` — atomic read-modify-write of `session_state.json` (temp file + `os.replace`); idempotent on `sweep_id` (skip combos already queued). (depends 4)
6. `main`/argparse: `--spec`, `--dry-run`, `--state`, `--date`, `--selftest`. (depends all)

## File Layout
- `sweep_runner.py` — NEW, ~230 LOC, repo root (declared deliverable).
- `experiments/infra-sweep-mode/sweep_spec_example.yaml` — NEW.
- `experiments/infra-sweep-mode/README.md` — NEW.

## Function Map
`sweep_runner.py`:
- `_mini_yaml_load(text: str) -> dict` — minimal YAML-subset parser (fallback).
- `load_spec(path) -> dict` — prefer PyYAML, else `_mini_yaml_load`.
- `validate_spec(spec) -> list[str]` — return list of error strings (empty = valid).
- `enumerate_grid(param_grid) -> list[dict]` — cartesian product of params.
- `_slug(s) -> str` — queue/fs-safe slug.
- `_subst(value, combo) -> value` — `{param}` substitution in str / list-of-str.
- `build_entries(spec, date) -> list[dict]` — produce queue entries (capped at max_runs).
- `enqueue(entries, state_path, sweep_id) -> dict` — atomic, idempotent merge into tick_queue_approved.
- `selftest() -> int` — parse+enumerate+build against the bundled example; assert invariants.
- `main() -> int` — argparse + dispatch.

## Security
- **No network, no LLM, no shell-out.** Pure local file read/write.
- **Path containment:** the only file written is `--state` (default `.harness/session_state.json`); generated `deliverable_paths` are data fields (not opened/written by sweep_runner) — they are consumed later by the loop, which already has its own containment. Spec is read-only.
- **Atomic write** (temp + `os.replace`) prevents a crash mid-write from corrupting `session_state.json` (IMPLEMENTATION council_focus: robust to partial failure).
- **DoS / runaway guard:** `max_runs` hard-caps generated entries (default+enforced ≤ a documented ceiling); a grid exceeding the cap is truncated with a logged warning, never silently.
- Trust boundary: the spec is authored by the repo owner / a prior tick; not attacker-controlled. Still, `validate_spec` rejects malformed/oversized input before any write.

## UI
CLI tool. States:
- **dry-run** (default-safe to run): prints grid size, each generated entry name + substituted deliverable_paths; writes nothing; exit 0.
- **enqueue**: prints "enqueued N (skipped M already-present)"; exit 0.
- **validation error**: prints each error to stderr, exit 2; writes nothing.
- **selftest**: prints PASS/FAIL per assertion, exit 0/1.

## Guide
Help text documents the spec schema, the `{param}` placeholder convention, the `max_runs`/`budget_cap` safety fields, and that `--dry-run` is the safe default for inspection. README mirrors this with the worked example.

## Edge Cases
- Empty `param_grid` → validation error (a sweep with no params is just a normal tick; use the queue directly).
- Grid size > `max_runs` → truncate to `max_runs`, log dropped count (no silent cap).
- `max_runs` > ceiling (50) → clamp + warn.
- Re-running the same sweep → idempotent: combos already present (matched by generated `name`) are skipped, not duplicated.
- Missing `session_state.json` or missing `tick_tock.tick_queue_approved` → error, exit 2 (never create a fresh state file).
- Placeholder referencing a param not in the grid → validation error.
- PyYAML absent → fall back to mini-parser (the CI reality); example file uses only the supported subset.

## Test Strategy
- `python3 sweep_runner.py --selftest` — parses `sweep_spec_example.yaml`, enumerates the grid, builds entries; asserts: grid size = product of value-list lengths, entry count = min(grid, max_runs), names unique, placeholders fully substituted (no residual `{`), required queue fields present, max_runs/budget_cap honored. Must pass in pre-filter (no PyYAML).
- `python3 sweep_runner.py --spec experiments/infra-sweep-mode/sweep_spec_example.yaml --dry-run` — shows the would-enqueue set, writes nothing.
- `python3 -c "import ast; ast.parse(open('sweep_runner.py').read())"` — syntax.
- Idempotency: dry-run twice against a temp state with one combo pre-present → reports the skip.
- No regression: `python3 test_project.py <a-known-good-project>` still passes (sweep_runner touches no pipeline file).
