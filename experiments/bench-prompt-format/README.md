# bench-prompt-format

Empirical A/B/C of **prompt encoding** — markdown vs JSON vs XML — on the
council's **BUGS** angle reviewer. Does rendering the *same* reviewer
instructions in a different syntax change how well Claude catches planted bugs?

The claim "JSON beats markdown for prompts" is common but contested; Anthropic
specifically recommends XML tags for Claude. This tick produces grounded
numbers on the YOLO loop's own prompt instead of repeating blog claims.

## What it measures

- **Corpus** — `eval_bugs.json` (repo root): 26 mined bug patterns, each with an
  `example_bad` (buggy) and `example_fix` (clean) snippet. `eval_bugs.py` is a
  *regex* scanner and does **not** call the LLM; this bench builds its own LLM
  classification task on the same corpus.
- **Task** — show a snippet to the BUGS reviewer (system prompt = one variant),
  ask for the JSON verdict. `example_bad` → reviewer should `OBJECT`;
  `example_fix` → `APPROVE`. Both versions of every pattern are included so a
  trigger-happy "always OBJECT" reviewer is penalised symmetrically.
- **Score** — 1.0 if the verdict matches ground truth, else 0.0.
- **Compliance** — fraction of outputs that parsed as clean JSON.
- **Stats** — paired Wilcoxon signed-rank on per-task mean-score differences.

## Controlled variable

Only the **prompt** encoding varies. The **requested output is held constant**
(JSON) for all three variants, so the verdict parser is identical and
answer-correctness scoring is apples-to-apples. Letting each variant emit its
own output format would confound prompt-encoding effect with output-parsing
fragility. Compliance is reported as a separate column.

## Semantic-equivalence checklist

The three prompt files must encode identical content — content drift is the
single most likely way this experiment misleads. Each semantic element and
where it lives:

| Element | `bugs_angle.md` | `bugs_angle.json` | `bugs_angle.xml` |
|---|---|---|---|
| Role (advocate for correctness only) | `# Role` section | `role` string | `<role>` |
| What to focus on (8 bullet items) | `## Focus on` list | `focus_on` array | `<focus><item>` |
| What to ignore (3 items) | `## Ignore` list | `ignore` array | `<ignore><item>` |
| Output schema (6 JSON fields) | `## Output schema` block | `output_schema` object | `<output_schema>` |
| Instruction (APPROVE only if clean; JSON only) | `## Instruction` | `instruction` string | `<instruction>` |

The eight focus items and three ignore items are byte-for-byte the same text
across all three files (only the surrounding syntax differs). Diff them:

```bash
diff <(grep -oE 'Edge cases.*|Boundary.*|Error handling.*' prompts/bugs_angle.md) ...
```

## Run

```bash
python3 bench.py --self-test          # verify Wilcoxon + parser, no API calls
python3 bench.py --limit 1 --runs 1   # smoke: 1 pattern (2 tasks) x 3 variants = 6 calls
python3 bench.py                       # full: 10 patterns -> 20 tasks x 3 runs x 3 variants = 180 calls
python3 bench.py --analyze-only        # re-render RESULTS.md from runs.jsonl
```

`--self-test` asserts the Wilcoxon implementation against a hand-computed
fixture (`diffs=[1,-2,3,-4,5]` → W=6) because `scipy` is not installed here.

## Model

Runs with `claude-haiku-4-5` for cost/latency tractability inside the
autonomous cron turn (the build must finish synchronously). A format effect —
or its absence — on Haiku is real data; the original plan's Opus-4.7 confirming
run is a documented follow-on if Haiku shows a worth-confirming effect.
RESULTS.md scopes its verdict to the model it ran on.

## Files

- `prompts/bugs_angle.{md,json,xml}` — the three semantically-equivalent variants.
- `bench.py` — runner (resumable via `results/runs.jsonl`), stats, self-test.
- `results/runs.jsonl` — one JSON record per (variant, task, run).
- `results/RESULTS.md` — generated analysis + ship/iterate/discard verdict.
- `plan.md` — design rationale and council focus.
