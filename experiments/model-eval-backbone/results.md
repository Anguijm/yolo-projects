# Backbone model-swap benchmark — results

**Run:** 2026-06-25 · 5 historical YOLO build specs × 2 models = 10 generations.
**Backbone (control):** `claude-sonnet-4-6` · **Candidate:** `claude-opus-4-8`.
**Cap:** `--max-tokens 20000` (raised from the default 8000 after the smoke run
showed an 8000-token cap truncates a full single-file HTML tool inside a JSON
envelope — see *Methodology notes* below).
**Raw data:** `benchmark_results.json` (per-run records + summary; regenerate with
`python3 benchmark.py --max-tokens 20000`).

## Summary

| Metric | `claude-sonnet-4-6` (backbone) | `claude-opus-4-8` (candidate) |
|---|---|---|
| Pass rate (static checks)   | 0.60 (3/5) | **1.00 (5/5)** |
| Complete rate (valid envelope) | 0.80 (4/5) | **1.00 (5/5)** |
| Mean clarifications         | 0.0 | 0.0 |
| Mean output tokens          | 13 166 | **9 150** |
| Mean wall time              | 153.6 s | **82.6 s** |
| Total cost (5 builds)       | **$0.99** | $3.46 |
| Cost per build              | **$0.20** | $0.69 |

## Per-build detail

| Spec | sonnet-4-6 | opus-4-8 |
|---|---|---|
| cron-explain   | ✅ pass (10 874 tok) | ✅ pass (10 276 tok) |
| url-dissect    | ❌ **broken JS** — fails syntax check (13 818 tok) | ✅ pass (9 881 tok) |
| uuid-inspector | ❌ **truncated** — hit 20 k cap, empty envelope (20 000 tok) | ✅ pass (9 781 tok) |
| svg-fields     | ✅ pass (10 208 tok) | ✅ pass (6 688 tok) |
| semver-range   | ✅ pass (10 932 tok) | ✅ pass (9 126 tok) |

"pass" = generated HTML completes a valid envelope **and** clears the same static
gauntlet `test_project.py` runs (`extract_js` → `check_syntax` →
`check_id_consistency` → `check_event_listeners`). Generated HTML is never
executed — static analysis only. Neither model asked a clarifying question on any
spec (the replayed `idea` strings were detailed enough to one-shot).

## Recommendation: **PROMOTE `claude-opus-4-8` as the generation backbone**

On this set, opus-4-8 is strictly dominant on every quality axis and loses only on
raw price:

- **Reliability.** opus completed and passed 5/5; sonnet shipped 2 defective
  builds out of 5 — one truncated mid-generation (uuid-inspector exceeded the
  20 k cap) and one that emitted syntactically broken JS (url-dissect). In the
  autonomous pipeline a defective build is not free: it burns a cron cycle, can
  trigger council IMPLEMENTATION-gate retries, and in the worst case escalates to
  a human. The $0.49/build premium buys 100 % completion.
- **Conciseness.** opus produced *fewer* output tokens (9.2 k vs 13.2 k mean)
  while passing more checks — it is not trading verbosity for quality.
- **Latency.** opus was ~1.9× faster wall-clock (82.6 s vs 153.6 s mean), partly
  because sonnet's verbose generations ran longer and one ran to the token cap.
- **Cost.** sonnet is ~3.5× cheaper ($0.20 vs $0.69/build). This is the only
  axis favoring the incumbent, and in absolute terms the delta is sub-dollar per
  build.

A **hybrid** policy (sonnet for trivial/short tools, opus for anything
non-trivial) is a defensible fallback, but it adds model-routing logic and a
misclassification risk for a per-build saving of cents. Given the small absolute
cost, the simpler "opus-4-8 for all generation" is recommended; revisit only if
build volume grows enough that the 3.5× token-cost multiplier becomes material.

## Methodology notes & caveats

- **N is small and directional, not definitive.** 5 specs, one trial per
  (spec × model) cell, no retries. Treat the pass-rate gap as a signal to act on,
  not a statistically tight estimate. A re-run with ≥10 specs and 3 trials/cell
  would firm up the pass-rate confidence interval.
- **Token cap matters — the default is now 20000.** The smoke run (`--limit 1`)
  at the original 8000-token default returned `completed=False` for both models
  because a full single-file HTML tool plus JSON-escaping overhead exceeds 8000
  output tokens (the historical originals are 6 k–11 k tokens of HTML *before*
  escaping). A default that silently truncates real tools is a footgun, so
  `benchmark.py`'s `--max-tokens` default was changed to **20000**; a small cap
  (e.g. `--max-tokens 8000`) is now an explicit opt-in for cheap smoke-tests only.
  All numbers in this report were produced at the 20000 cap. Even at 20 k,
  sonnet's uuid-inspector generation truncated — a genuine verbosity signal, but
  it means sonnet's complete-rate could be cap-sensitive; opus never approached
  the cap.
- **Generation-side only.** This measures one-shot generation quality, not the
  full council/gate loop. Council retry-count-per-gate and end-to-end completion
  through all 4 gates (the richer signal named in the original idea) are left to a
  follow-up that wires the benchmark into a live gate run — see README "Future
  extensions". This run establishes the cheaper upstream signal first.
- **Cost model is configurable** via `*_COST_IN`/`*_COST_OUT` env vars; the
  defaults (sonnet 3/15, opus 15/75 $/MTok) drive the cost column above.
