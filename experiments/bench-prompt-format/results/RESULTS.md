# RESULTS — bench-prompt-format

Model: `claude-haiku-4-5` · runs per (variant, task): 3 · tasks: 20 · variants: md, json, xml

> Output format held constant (JSON) across all three variants; only the PROMPT encoding differs. Compliance = fraction of outputs that parsed as clean JSON.

## Verdict

**DISCARD (no-significant-difference)** — best variant `md` beats worst `xml` by only 5.0%, and no pairwise Wilcoxon reaches p<0.05. For the BUGS angle on this model, prompt ENCODING does not measurably change bug-catch accuracy. Do not migrate the production prompt format on quality grounds.

**Power caveat (honest framing):** this is a *bounded* null, not proof of zero effect. At 20 tasks × 3 runs the design can only detect a large encoding effect (≈≥10pp); a small real difference would be invisible here. The defensible claim is "no effect large enough to justify a migration was found," not "the formats are provably identical." Confirming on Opus and widening the task set would tighten the bound — only worth it if a later signal appears.

## Per-variant

| variant | mean score | task-score variance | compliance | calls | errors |
|---|---|---|---|---|---|
| md | 0.550 | 0.261 | 1.000 | 60 | 0 |
| json | 0.550 | 0.261 | 1.000 | 60 | 0 |
| xml | 0.500 | 0.263 | 1.000 | 60 | 0 |

## Pairwise Wilcoxon (paired per-task mean scores)

**Plain-language read:** `p` is the chance the score gap between two encodings is just sampling noise. `p` near 1.0 means *no detectable difference*. `W`/`z` are the test internals. When nearly every task scores identically across two encodings, only a handful of tasks differ, so `W` and `z` collapse toward 0 and `p` toward 1 — that is the signature of "these encodings behave the same," not a bug.

| pair | n tasks | mean diff | W | z | p |
|---|---|---|---|---|---|
| md_vs_json | 20 | +0.000 | — | — | 1.0 |
| md_vs_xml | 20 | +0.050 | 0 | 0.0 | n/a ⚠ |
| json_vs_xml | 20 | +0.050 | 0 | 0.0 | n/a ⚠ |

- ⚠ `md_vs_xml`: UNDERPOWERED: only 1 nonzero paired diff(s); normal approximation unreliable, treat p as non-informative.
- ⚠ `json_vs_xml`: UNDERPOWERED: only 1 nonzero paired diff(s); normal approximation unreliable, treat p as non-informative.

## Reading this

- **mean score** — fraction of (task, run) cells where the reviewer's APPROVE/OBJECT matched ground truth. Buggy and clean snippets are both present, so this rewards precision AND recall.

- **compliance** — did the model return parseable JSON. A low compliance with a high score means the verdict was readable but the wrapper was malformed.

- **p** — two-sided Wilcoxon signed-rank, normal approximation with continuity correction. `scipy` is not installed here; the implementation is asserted against a hand-computed fixture in `--self-test`.


Raw records: `results/runs.jsonl` (180 total).
