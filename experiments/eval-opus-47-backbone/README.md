# eval-opus-47-backbone

Benchmark Opus 4.7 vs Haiku 4.5 as the `council.py` backbone model.

## What it does

Runs the council `implementation` gate on 3 canonical YOLO utility fixtures
(`url-dissect`, `cron-explain`, `uuid-inspector`) using each model and records:
- Per-angle verdicts (APPROVE / OBJECT)
- Gate latency (seconds)
- Token counts (input + output)
- Estimated cost at current pricing

## Quick start

```bash
# Discover all flags
python3 experiments/eval-opus-47-backbone/benchmark.py --help

# Full 3-fixture run (~$0.35) — timestamped output file
ANTHROPIC_API_KEY=sk-... python3 experiments/eval-opus-47-backbone/benchmark.py

# Single-fixture test (~$0.05)
ANTHROPIC_API_KEY=sk-... python3 experiments/eval-opus-47-backbone/benchmark.py --fixtures 1

# Explicit output path
ANTHROPIC_API_KEY=sk-... python3 experiments/eval-opus-47-backbone/benchmark.py --output my_results.json

# Dry run (no API calls)
python3 experiments/eval-opus-47-backbone/benchmark.py --dry-run
```

## Updating the cost model

When Anthropic publishes new pricing, edit the four constants near the top of `benchmark.py`:

```python
_HAIKU_IN_DEFAULT  = 0.80   # $/MTok input
_HAIKU_OUT_DEFAULT = 4.00   # $/MTok output
_OPUS_IN_DEFAULT   = 15.00  # $/MTok input
_OPUS_OUT_DEFAULT  = 75.00  # $/MTok output
```

Or override per-run without editing the file:

```bash
HAIKU_COST_IN=1.00 HAIKU_COST_OUT=5.00 OPUS_COST_IN=20.00 OPUS_COST_OUT=100.00 \
  ANTHROPIC_API_KEY=sk-... python3 experiments/eval-opus-47-backbone/benchmark.py
```

The effective values are captured in every `benchmark_results_*.json` under `cost_model_used`.

## Adding fixtures

Add entries to `FIXTURES` in `benchmark.py`:

```python
FIXTURES = [
    ("url-dissect",    REPO_ROOT / "url-dissect"    / "index.html"),
    ("cron-explain",   REPO_ROOT / "cron-explain"   / "index.html"),
    ("uuid-inspector", REPO_ROOT / "uuid-inspector" / "index.html"),
    ("my-new-tool",    REPO_ROOT / "my-new-tool"    / "index.html"),  # add here
]
```

Then run with `--fixtures 4` (or higher).

## Interpreting results

| Metric | What it means |
|---|---|
| `approve` count | How many of 7 council angles approved the implementation |
| `gate_latency_s` | Wall time for all 7 parallel angle calls |
| `cost_usd` | Estimated API cost for that fixture × model run |
| `input_tokens` / `output_tokens` | Token counts across all 7 angle calls |

**Signal level:** N=3 fixtures is directional, not statistically conclusive.
- Clear winner (e.g., Opus consistently higher approve count): justified swap
- Mixed results: inconclusive — try `--fixtures 5+` (add more fixtures first)
- Similar results, large cost delta: keep Haiku (cost dominates)

See `results.md` for the actual conclusions from the first benchmark run.

## Isolation guarantee

`benchmark.py` patches `council._BACKEND`, `council._ANTHROPIC_CLIENT`, and
`council.CLAUDE_MODEL` for each run and restores them unconditionally in a
`finally` block — even if `run_gate` raises. No council.py source files are
modified. No `council_*.json` files are written to fixture directories.
