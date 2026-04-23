# eval-opus-47-backbone — Infrastructure Tick Plan

## Goal
Benchmark Opus 4.7 vs Haiku 4.5 as the council.py backbone on 3 canonical deliverables and produce a data-grounded swap recommendation.

## Scope

**In scope:**
- `experiments/eval-opus-47-backbone/benchmark.py` — runner script (~120 LOC)
- `experiments/eval-opus-47-backbone/results.md` — results table + hand-written conclusions
- `experiments/eval-opus-47-backbone/README.md` — usage guide

**Out of scope:**
- Modifying `council.py` source — benchmark monkey-patches the in-process module; no file edits
- Gemini backend — benchmark forces Claude-only for apples-to-apples comparison; GEMINI_API_KEY is ignored
- Flagship tock files (markdown-deck, naval-scribe) — too large for affordable benchmarking; 3 utility ticks give equivalent structural signal at a fraction of the cost
- Automated results writing — results.md is written during TESTS gate after benchmark.py produces benchmark_results.json

**Signal question (N=3 vs N=5):**
N=3 × 2 models × 7 angles = 42 angle evaluations per run. This is sufficient to detect clear directional differences (e.g., consistent APPROVE/OBJECT shift) but insufficient for statistical significance. The benchmark is explicitly labelled as "directional signal, not statistically conclusive." If results are mixed (some fixtures favour one model, some the other), the recommendation is "inconclusive — expand N." N=5+ is a follow-on run using `--fixtures 5` once additional fixture paths are added.

## Approach

**Isolation guarantee:** Both model runs receive identical context — same gate, same project, same `context_path` file on disk. `council.run_gate()` is called directly (not via subprocess), so no shell env or file system state can drift between the haiku and opus invocations. The only variable between runs is `council.CLAUDE_MODEL`.

**Subtasks (in order):**

1. **Setup** — create `experiments/eval-opus-47-backbone/` directory; write `plan.md` (this file).

2. **benchmark.py** — implement the runner:
   - Import `council` as a module; patch `council._BACKEND`, `council._ANTHROPIC_CLIENT`, `council.CLAUDE_MODEL` for each run
   - Restoration guarantee: `run_one` saves original values of all three module attributes before patching, then unconditionally restores them in a `finally` block — `TokenTracker.__exit__` also runs in `finally`. This guarantees isolation even if `run_gate` raises an exception mid-run.
   - `TokenTracker` context manager wraps `client.messages.create` to intercept `response.usage.input_tokens` / `.output_tokens` per API call without modifying council.py
   - `run_one(fixture, model_key, client)` — runs `council.run_gate("implementation", ...)` and collects verdicts, gate latency, total tokens, estimated cost
   - `main()` — CLI with `--fixtures N` (default 3), `--dry-run`, and `--output PATH`; default output filename is timestamped (`benchmark_results_YYYYMMDDTHHMMSS.json`) so successive runs never overwrite prior results; `--output` allows an explicit path (useful for scripting)
   - Cost model: Haiku $0.80/$4.00 per MTok in/out; Opus $15.00/$75.00 per MTok in/out

3. **Fixtures** — 3 canonical YOLO utility ticks:
   - `url-dissect` (URL Dissector & Analyzer, ~956 lines)
   - `cron-explain` (Cron expression explainer, ~945 lines)
   - `uuid-inspector` (UUID inspector, ~972 lines)
   All three exist on disk; sizes are comparable, keeping token costs consistent across models.

4. **README.md** — how to run, interpret results, add fixtures, understand confidence level.

5. **Pre-filter** — `python3 -c "ast.parse(...)"` on benchmark.py; `--dry-run` smoke test; then `--fixtures 1` live run to confirm end-to-end path works. No council_*.json files in url-dissect/ are written (benchmark calls `run_gate`, not `main`, so `write_gate_result` is never invoked).

6. **results.md** — written after the TESTS gate live run. Contains per-angle verdict table, latency delta, cost delta, and a concrete recommendation (swap / keep / inconclusive).

## File Layout

| File | Action | Notes |
|---|---|---|
| `experiments/eval-opus-47-backbone/plan.md` | CREATE | This file |
| `experiments/eval-opus-47-backbone/benchmark.py` | CREATE | ~120 LOC runner |
| `experiments/eval-opus-47-backbone/benchmark_results.json` | AUTO-WRITTEN | Output of benchmark.py |
| `experiments/eval-opus-47-backbone/results.md` | CREATE | Human-written conclusions from benchmark_results.json |
| `experiments/eval-opus-47-backbone/README.md` | CREATE | Usage guide |

No files outside `experiments/eval-opus-47-backbone/` are created or modified.

## Function Map

**`experiments/eval-opus-47-backbone/benchmark.py`:**

| Function | Role |
|---|---|
| `TokenTracker.__init__(client)` | Store original `messages.create`; init `records` list |
| `TokenTracker.__enter__()` | Install wrapped `messages.create` that logs usage + latency per call |
| `TokenTracker.__exit__(*_)` | Restore original `messages.create` (called in `finally` — guaranteed) |
| `TokenTracker.total_input` (property) | Sum input_tokens across all captured calls |
| `TokenTracker.total_output` (property) | Sum output_tokens across all captured calls |
| `run_one(fixture, model_key, client) → dict` | Save original council module state; patch; run gate in `try`; restore in `finally` |
| `main()` | CLI entrypoint; determine timestamped output path; iterate fixtures × models, save incrementally |

## Security

- `ANTHROPIC_API_KEY` read from env; not logged, not written to disk
- All output files written within `experiments/eval-opus-47-backbone/` (REPO_ROOT-relative); path validated with `os.path.realpath` per learnings.md standing rule (Internal verifier path containment, learnings.md:30)
- `TokenTracker` wraps then unconditionally restores the original method — no permanent mutation to the live council module
- No subprocess execution; no shell injection surface
- `benchmark_results.json` contains verdicts and token counts only — no secrets

## UI

Command-line tool. Per-run progress to stdout: `fixture × model | latency | approve count | tokens | cost`. Final: "DONE — N runs saved to benchmark_results.json."

## Guide

```bash
# Full 3-fixture run (~$0.35 total) — output: benchmark_results_YYYYMMDDTHHMMSS.json
ANTHROPIC_API_KEY=... python3 experiments/eval-opus-47-backbone/benchmark.py

# Quick single-fixture test (~$0.05)
ANTHROPIC_API_KEY=... python3 experiments/eval-opus-47-backbone/benchmark.py --fixtures 1

# Explicit output path
ANTHROPIC_API_KEY=... python3 experiments/eval-opus-47-backbone/benchmark.py --output my_results.json

# Dry run (no API calls)
python3 experiments/eval-opus-47-backbone/benchmark.py --dry-run
```

## Edge Cases

| Condition | Behaviour |
|---|---|
| `GEMINI_API_KEY` set | Warn; force Claude backend regardless |
| `ANTHROPIC_API_KEY` missing | Print error, exit 1 |
| API error mid-run | `council.run_gate` returns OBJECT verdicts with `reason="API error: ..."`; benchmark records and continues; `finally` block always restores council state |
| Exception in `run_gate` | `try/finally` in `run_one` guarantees module state restoration before exception propagates |
| Parse failure on one angle | `parse_failed=True` verdict counted as OBJECT in results |
| Default output filename | Timestamped `benchmark_results_YYYYMMDDTHHMMSS.json` — each run gets a unique file, no silent overwrite |
| `--output PATH` provided | Writes to that exact path; user takes responsibility for overwrite |
| N=3 produces mixed/inconclusive results | results.md notes this and recommends `--fixtures 5` follow-on |

## Test Strategy

1. **Syntax check:** `python3 -c "import ast; ast.parse(open('experiments/eval-opus-47-backbone/benchmark.py').read())"` → exit 0
2. **Dry-run:** `python3 experiments/eval-opus-47-backbone/benchmark.py --dry-run` → prints 6 planned runs (3 fixtures × 2 models), exits 0
3. **Live single-fixture:** `ANTHROPIC_API_KEY=... python3 experiments/eval-opus-47-backbone/benchmark.py --fixtures 1 --output experiments/eval-opus-47-backbone/test_results.json` → output file contains exactly 2 records (haiku + opus on url-dissect), each with keys: `fixture, model, model_id, gate_latency_s, approve, object, input_tokens, output_tokens, cost_usd, verdicts`
4. **No side-effects:** Verify `url-dissect/council_implementation.json` is NOT created or modified after the live run
5. **Restoration guarantee:** Verify `council.CLAUDE_MODEL` equals `"claude-haiku-4-5-20251001"` after `run_one` completes (confirm `finally` restored state)
6. **Full run:** `ANTHROPIC_API_KEY=... python3 experiments/eval-opus-47-backbone/benchmark.py` → 6 records in timestamped output file; results.md written with concrete recommendation
