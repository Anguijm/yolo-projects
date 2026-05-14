# Quality A/B protocol — does the bundle change verdicts in useful ways?

## Goal

Decide whether to wire `bundle_repo.py` into `.harness/scripts/council.py`
for PR-mode reviewers by comparing verdicts WITH vs WITHOUT the bundle
on 5 historical PRs.

## What "useful" means

Three classes of outcome are useful; one is not.

1. **Bundle prevents a hallucination.** Without bundle: angle objects
   citing an "undefined symbol"; with bundle: angle correctly approves.
   This is the gold-standard signal.
2. **Bundle improves a reason** without changing the verdict. The
   verdict stays APPROVE but the reason is more specific
   ("approves because foo.py:42 defines bar correctly"). Still useful;
   evidence accuracy compounds across reviews.
3. **Bundle catches a real bug** the no-bundle path missed. Less likely
   for a context bundle, but possible — sometimes a reviewer needs to
   see the surrounding code to spot a contract violation.

NOT useful: the bundle changes the verdict in a direction we can't
explain. Treat any unexplained flip as evidence the bundle is making
the model worse, not better.

## Procedure

1. **Pick 5 historical PRs** from the repo, ideally including:
   - PR #8 (card-generator silent-truncation fix) — small, targeted
   - one PR that the BUGS angle auto-downgraded for hallucination
   - one PR that touched multi-file changes
   - one PR that was small and uncontroversial (control)
   - one PR that was contested in review

2. **For each PR, generate two prompt bodies:**
   - **A (no bundle):** the exact council.py prompt for one angle
     (start with BUGS), unchanged.
   - **B (with bundle):** the same prompt with `bundle_repo.py` output
     prepended in a `## Repo context` section before the diff.

3. **Run both through the same model** (whatever council.py uses today
   for the BUGS angle). Same temperature, same model ID, same seed if
   the provider supports it. Capture raw response + parsed Verdict.

4. **Score each PR on 4 axes** (0/1 each, scored independently by hand):
   - `verdict_changed`: did the parsed verdict flip APPROVE↔OBJECT?
   - `reason_improved`: is the reason more specific / better-grounded
     with the bundle?
   - `evidence_more_concrete`: does the with-bundle reason cite a
     specific `file:line` more often than the no-bundle one?
   - `hallucination_avoided`: did the no-bundle path invent a fact
     contradicted by the actual code?

5. **Tally + decide.**

   | Total points | Decision |
   |--------------|----------|
   | ≥12 / 20     | Wire it up (follow-on tick #2) |
   | 8–11 / 20    | Iterate on the bundle layout, re-run |
   | <8 / 20      | Park the experiment; context bundles aren't worth the tokens for this repo's PRs |

## What we deliberately are not measuring

- **Latency.** The bundle adds ~3K tokens to each prompt; latency
  impact is real but secondary. If quality wins, latency cost is
  worth it.
- **Cost.** Same reasoning. Bundle adds at most ~$0.01 per review
  at current Sonnet pricing; quality dominates.
- **Token efficiency of the bundle.** The bundle generator can be
  optimized later (smarter related-file selection, AST summaries,
  etc.). The hypothesis under test is "context helps", not "this
  bundle is optimal."

## Why 5 PRs and not 50

This is a binary decision with a clear effect-size threshold. If 5 PRs
don't show a useful signal, 50 won't either — context bundles either
help reviewers ground their verdicts or they don't. 5 keeps the manual
scoring honest (we can read every output) while still spanning the
PR-type diversity we care about.

## Why BUGS first

The BUGS angle is the one with the documented hallucination problem
(auto-downgrade rule #4). If the bundle helps anywhere, it helps here
first. Promote to other angles only after BUGS shows signal.

## Shadow mode rollout

If the A/B is positive, wire `bundle_repo.py` into council.py behind a
`COUNCIL_BUNDLE_CONTEXT=1` env flag, default OFF. Run one week of
PRs in shadow mode (compute both prompts, send both to the model,
log both verdicts, use the no-bundle one for the real decision).
After a week, compare disagreement rates and surface any (no-bundle
APPROVE, with-bundle OBJECT) cases for human review before flipping
the flag default-on.
