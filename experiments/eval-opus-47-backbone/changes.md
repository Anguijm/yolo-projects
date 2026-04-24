# eval-opus-47-backbone — Implementation Changes

## Files created

### `experiments/eval-opus-47-backbone/benchmark.py` (~250 LOC)
- `_load_cost_model()`: reads `HAIKU_COST_IN/OUT` and `OPUS_COST_IN/OUT` env vars, logs any overrides, returns dict of $/MTok for haiku + opus
- `_cost(model_key, input_tokens, output_tokens, costs) → float`: applies cost table to token counts
- `TokenTracker.__init__/___enter__/__exit__`: wraps `client.messages.create` to record `latency_s`, `input_tokens`, `output_tokens` per call; `__exit__` unconditionally restores original method
- `TokenTracker.total_input/total_output` (properties): sum over all captured records
- `run_one(fixture_name, context_path, model_key, client, costs) → dict`: saves `council._BACKEND`, `council._ANTHROPIC_CLIENT`, `council.CLAUDE_MODEL`; patches all three; calls `council.run_gate("implementation", ...)`; restores all three in `finally`; returns verdict + token + cost record
- `main()`: argparse CLI with `--fixtures N` (default 3), `--dry-run`, `--output PATH`; output defaults to timestamped path in experiment dir; validates output path is within REPO_ROOT; saves results incrementally per run

Key design decisions:
- `council.CLAUDE_MODEL` patched per run, not globally — no side-effects between runs or after completion
- `TokenTracker` wraps at the client level (not module level) — cannot bleed across runs
- Incremental JSON write after each run — partial results recoverable if interrupted
- No `council_*.json` files written to fixture directories — `run_gate` is called with `write_gate_result=False` (or the benchmark does not trigger the write path)

### `experiments/eval-opus-47-backbone/README.md` (~90 lines)
- Usage guide: `--help`, `--fixtures 1`, `--output`, dry-run, cost-override examples
- Cost-model update instructions: single-line edit in `benchmark.py`
- Fixture-addition guide: add entries to `FIXTURES` list, increase `--fixtures N`
- Results interpretation: approve count, latency, cost, signal-level caveat (N=3 = directional)
- Isolation guarantee description

## Files not modified
- `council.py` — not edited; `benchmark.py` monkey-patches in-process only
- Any fixture project directory (`url-dissect/`, `cron-explain/`, `uuid-inspector/`) — no files created or modified in fixture dirs

## Path containment
- `out_path.relative_to(REPO_ROOT)` guard at line 203 — rejects paths outside repo
- `REPO_ROOT = Path(__file__).resolve().parent.parent.parent` — computed from benchmark.py location
