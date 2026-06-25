# model-eval-backbone

A generation-side backbone benchmark. It replays historical YOLO build specs
through two Claude models — a **current backbone** and a **candidate** — and
emits comparable per-run metrics so a human can decide whether to promote the
candidate into the tick/tock *generation* backbone.

This swaps the model that **produces** the artifact from a build spec. It does
**not** replay the council reviewer model — that is a separate axis already
covered by [`../eval-opus-47-backbone/`](../eval-opus-47-backbone/). This
benchmark never touches council state and never executes generated HTML.

## What it measures

Per `(spec × model)` run:

- **clarification_count** — number of clarifying questions the model asked,
  measured deterministically from a strict-JSON reply envelope (not by scraping
  prose for question marks).
- **completed** — model returned a non-null HTML document (vs. punting with
  questions and `html: null`).
- **passed** — the generated HTML passes `test_project.py`'s *static* checks
  (JS syntax via `node -c`, `getElementById` ids all exist, `addEventListener`
  targets all exist). No browser, no execution.
- **input_tokens / output_tokens / cost_usd / wall_s**.

Aggregated per model: pass rate, complete rate, mean clarifications, mean output
tokens, total cost, mean wall time.

## Quick start

```bash
# See the planned matrix; zero API calls.
python3 experiments/model-eval-backbone/benchmark.py --dry-run

# One spec × both models — end-to-end smoke.
python3 experiments/model-eval-backbone/benchmark.py --limit 1

# Full pinned 5-spec run.
python3 experiments/model-eval-backbone/benchmark.py

# Custom model pair.
python3 experiments/model-eval-backbone/benchmark.py \
    --backbone claude-sonnet-4-6 --candidate claude-opus-4-8

# Auto-select the 5 most recent logged builds that still have an index.html.
python3 experiments/model-eval-backbone/benchmark.py --from-log 5
```

Requires `ANTHROPIC_API_KEY` in the environment for live runs (`--dry-run` does
not). Output is written incrementally to a timestamped
`benchmark_results_<TS>.json` so a partial run is recoverable.

## What "pass" means

`passed = (JS syntax OK) and (no missing getElementById ids) and (no missing
addEventListener targets)`.

These are the deterministic static checks from the repo's `test_project.py`,
called directly on the generated HTML written to a sandboxed temp dir. We do not
run Playwright/browser tests here — they are non-deterministic in cron and a
weak signal across model variation. A model that asks clarifying questions and
returns `html: null` is `completed=false` and `passed=false` (a "punt").

## Adding a spec

Edit `DEFAULT_SPECS` in `benchmark.py`: each entry is `{"slug": "<project>",
"goal": "<original build idea>"}`. Pick a slug whose `<slug>/index.html` still
exists on disk (it anchors "what good looked like", though the run does not
require it). Alternatively use `--from-log N` to auto-select recent builds from
`.harness/yolo_log.json`.

## Cost model

Defaults live in `_PRICING_DEFAULTS` in `benchmark.py` ($/MTok). Override per run
via env vars without editing code:

| Bucket | In | Out |
|---|---|---|
| sonnet | `SONNET_COST_IN` | `SONNET_COST_OUT` |
| opus | `OPUS_COST_IN` | `OPUS_COST_OUT` |
| haiku | `HAIKU_COST_IN` | `HAIKU_COST_OUT` |

A model id is mapped to a bucket by substring (`opus`/`sonnet`/`haiku`), falling
back to `default`.

## Security / trust boundary

- Model output is **untrusted**: generated HTML is written only to a temp dir
  inside this folder (`_gen/`, removed after each run) and is **never** opened in
  a browser or executed — only statically parsed.
- **Prompt injection (known limitation):** the build-spec goal text comes from
  `.harness/yolo_log.json` / CLI and flows into the prompt. `build_prompt` wraps
  it in an explicit `<build_spec>…</build_spec>` delimiter, neutralizes forged
  delimiter tokens, and frames the block as a task to fulfil, not instructions to
  obey. The corpus is our own build log, so the residual risk is low and the
  blast radius of a successful injection is a single degraded benchmark run — not
  code execution or data exfiltration. This is containment, not an airtight
  guarantee.
- Slugs are sanitized (`_safe_slug`, whitelist `[A-Za-z0-9._-]`, `..`/leading-dot
  stripped) and the temp path is `.resolve()`-checked to stay under `_gen/`.

## Future extensions (documented, not built)

- **Council-retry replay** — running the full 4×7 council gates per `(spec ×
  model)` to measure retry count per gate. Deferred: it ~56×'s token cost for a
  marginal signal beyond the static pass/fail used here.
- Larger spec sets (`--from-log 10+`) once a 5-spec signal justifies the spend.
