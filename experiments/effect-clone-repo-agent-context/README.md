# effect-clone-repo-agent-context

A research scaffold for pre-bundling repo context into council reviewer
prompts, adopted from the Effect "clone the repo into agent context" talk.

**Status:** scaffold — bundle generator + sample output + A/B protocol.
The actual wire-up into `.harness/scripts/council.py` is a follow-on tick
once the A/B confirms the bundle changes verdicts in useful ways.

## The argument we're testing

The talk's specific technique: instead of giving the LLM a tool to read
files one by one (which consumes turns and limits reasoning depth),
pre-compute a tightly-scoped repo context bundle — the filtered file
list, key files inlined, an import-graph summary — and pass it once.

Our council reviewers today see a unified diff plus PR metadata. They
do *not* see the surrounding code unless it's in the diff. The recent
BUGS hallucination auto-downgrade rule (`detect_bugs_hallucination` in
`.harness/scripts/council.py`) is direct evidence: reviewers without
enough context invented "undefined symbols" that the cited file actually
defined.

The hypothesis: a bounded repo bundle, prepended to the council prompt,
reduces context-starvation hallucinations without busting the
8K-token-bundle budget.

## Scope

In scope:
- `bundle_repo.py` — a CLI that takes a unified diff (or a list of
  changed paths) and produces a markdown bundle: changed files in full,
  filtered "related" files (siblings + same-directory neighbors),
  inlined contents of the top-5 most-related files, one-paragraph repo
  overview. 8K-token soft cap with a documented truncation strategy.
- `sample_bundle.md` — the bundle generated for one real historical PR
  (PR #8, the card-generator silent-truncation fix). Committed so
  reviewers can sanity-check the output without running the script.
- `quality_protocol.md` — the A/B procedure: replay 5 historical PRs
  through council.py with vs without the bundle, manually score whether
  the bundle changed the verdict or improved the reasoning quality.

Out of scope:
- Touching `.harness/scripts/council.py`. The integration is a follow-on
  tick once we know whether the bundle is worth its tokens.
- Cross-file static analysis. We don't compute an import graph — that's
  too much engineering for an unvalidated hypothesis. The "related files"
  filter is heuristic: directory-siblings + name-prefix matches.
- Token-accurate measurement. We approximate with `len(text) / 4`,
  which is close enough for a hypothesis test.

## How to run

```bash
cd experiments/effect-clone-repo-agent-context
# Bundle a diff (read from stdin or --diff PATH):
git -C ../.. diff main...HEAD | python3 bundle_repo.py > /tmp/bundle.md
# Or use the bundled fixture:
python3 bundle_repo.py --demo
```

The `--demo` mode regenerates `sample_bundle.md` from the fixture diff
that lives in this directory. Useful for re-running after tweaking the
bundle layout.

## Files in this directory

- `README.md` — this file
- `bundle_repo.py` — the bundle generator
- `sample_bundle.md` — output for the PR #8 fixture diff
- `fixture_diff.patch` — the PR #8 diff used as input to the demo
- `quality_protocol.md` — A/B test recipe

## Follow-on ticks this enables

1. **Execute the A/B** on 5 historical PRs and report verdict-delta
   results per `quality_protocol.md`.
2. **Wire bundle_repo.py into council.py** behind a
   `COUNCIL_BUNDLE_CONTEXT=1` flag, prepending the bundle to the diff
   in each angle's prompt. Run one week shadow-mode.
3. **If shadow mode shows reduced hallucination auto-downgrades**,
   make the bundle default-on for PR-mode council; cron-mode council
   keeps the existing prompt (cron processes its own state, not diffs).

## Why this is "low effort" despite the framing

We aren't building an import graph, AST analysis, or any code intelligence.
The bundle is filesystem traversal + token budgeting + markdown emission.
The expensive part is the A/B comparison itself — and that's a follow-on,
not in this scaffold.
