# infra-sweep-mode — parameterized experiment sweeps for the tick queue

`sweep_runner.py` (repo root) turns one *base tick* + a *parameter grid* into N
parameterized ticks enqueued onto `tick_tock.tick_queue_approved`. The existing
YOLO loop then drains them one-per-tick through the normal 4 council gates.

Adopted from Phase 4 experiment `nb-2026-04-19-karpathy-700-experiments`
(NateBJones, 2026-04-19): our loop already does one-experiment-per-tick; a sweep
mode parameterizes a single spec across N variants (same build, different
model; same lens, different threshold) so a grid is authored once, not N times.

## Design: a pure producer (not a runner)

`sweep_runner` **only enumerates and enqueues**. It does *not* invoke
`council.py`, run builds, call any LLM, or shell out.

> **Why tick-queue injection rather than calling `council.py` directly?**
> The loop already drains the approved queue one item per cron slot, running
> each through all 4 gates with per-tick commit/push isolation (see
> `CLAUDE.md`). If `sweep_runner` ran the gates itself it would duplicate that
> orchestration and bypass per-tick isolation. As a pure producer, each
> generated tick gets the full, unmodified council treatment for free, the
> runner is trivially testable with `--dry-run` (no API, no side effects), and
> nothing downstream needs to know sweeps exist — a sweep is just "N normal
> ticks."

## Usage

```bash
# Inspect the grid and the entries it WOULD enqueue — writes nothing (safe default):
python3 sweep_runner.py --spec experiments/infra-sweep-mode/sweep_spec_example.yaml --dry-run

# Actually enqueue (atomic + idempotent):
python3 sweep_runner.py --spec experiments/infra-sweep-mode/sweep_spec_example.yaml

# Built-in tests against the bundled example (used in pre-filter; needs no PyYAML):
python3 sweep_runner.py --selftest
```

Run it while the hourly cron is paused (it writes `session_state.json`, same as
`update_session_state.py`); re-enable the cron afterward.

## Spec schema

```yaml
sweep_id: <stable id for this sweep>     # used for idempotency + entry tagging
base_tick:
  name: <base name>                      # final names: <name>--<k>_<v>__<k>_<v>
  type: infrastructure | yolo | experiment
  idea: <one-liner>                      # {param} placeholders allowed
  rationale: <why>
  council_focus: <focus text>            # {param} placeholders allowed
  plan_summary: <summary>                # {param} placeholders allowed
  deliverable_paths:                     # {param} placeholders allowed
    - <repo-relative path with optional {param}>
param_grid:
  <param_a>: [v1, v2, ...]               # non-empty list
  <param_b>: [v1, v2, ...]
max_runs: 10                             # hard cap on generated entries (clamped to 50)
budget_cap: 5.0                          # total-sweep USD budget (enforced, see below)
est_cost_per_run: 0.5                    # optional; USD/run used to convert budget -> run count
```

The number of entries generated is `min(grid_size, max_runs, floor(budget_cap /
est_cost_per_run))`. `budget_cap` therefore has real teeth: with the defaults a
$5 budget at $0.50/run caps the sweep at 10 runs regardless of grid size. When
the budget is the binding constraint the dropped-combo `WARNING` names it.

`{param}` placeholders in `idea` / `rationale` / `council_focus` /
`plan_summary` / `deliverable_paths` are substituted per grid combination
(cartesian product of all `param_grid` value lists, deterministic key order).
Each entry also gets `param_<k>=<v>` appended to its `plan_summary`, plus
`sweep_id`, `sweep_run`, `sweep_total`, `sweep_params`, `budget_cap`,
`queued_date`.

### Dependency-free YAML

PyYAML is **not** installed in CI. `sweep_runner` prefers PyYAML when present,
else falls back to an embedded minimal parser supporting exactly the subset
above (top-level scalars, one level of nested mapping, block sequences `- item`,
inline flow lists `[a, b]`). The example spec uses only this subset.

## Safety (the guards council asked for)

- **Atomic write** — `session_state.json` is written to a temp file and
  `os.replace`d in, so a crash mid-write never corrupts state (BUGS gate).
- **Idempotent** — re-running the same sweep skips combos already queued
  (matched by generated `name`); no duplicates.
- **Input validation** — param values are restricted to a benign charset
  (`alnum . _ / + - space`) and `deliverable_paths` are rejected if they contain
  `..`, are absolute, or carry shell/markup metacharacters — both before *and*
  after `{param}` substitution, so a hostile value can't smuggle traversal or
  injection into a downstream tick (SECURITY gate).
- **Prompt-injection guard** — static text fields (`name`, `idea`, `rationale`,
  `council_focus`, `plan_summary`) are scanned for the most common
  prompt-injection phrasings (e.g. "ignore all previous instructions") and
  rejected before they can reach a downstream LLM tick (defense-in-depth, not a
  complete defense — specs are owner-authored).
- **Quote-aware spec parsing** — the fallback parser strips `#` comments only
  outside quoted strings, so values like `"channel #3"` survive intact.
- **No silent caps** — a grid larger than `max_runs` is truncated with a logged
  `WARNING`; `max_runs` above 50 is clamped with a warning.
- **Refuses to fabricate state** — errors out if `session_state.json` or
  `tick_tock.tick_queue_approved` is missing rather than creating a fresh one.

## Promoting a real sweep

`eval-opus-47-backbone` (the example) can be promoted to sweep mode in its own
plan: author a spec like `sweep_spec_example.yaml`, `--dry-run` to inspect, then
enqueue. Three near-identical evaluation ticks become one authored grid.
