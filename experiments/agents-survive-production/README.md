# agents-survive-production

An honest audit of `tick_tock.yml` (yolo-projects' production agent) against
the MLOps "agents in production" survival checklist.

**Status:** scaffold — checklist + scored audit + top-3 gap proposals.
The follow-on ticks remediate specific gaps; this scaffold is the
diagnostic, not the cure.

## Why this experiment exists

The MLOps talk's argument: most agent prototypes survive demos but die in
production from drift, silent failures, missing observability, and lack
of runbooks. Yolo's `tick_tock.yml` cron pipeline IS our production
agent — autonomous, hourly when enabled, mutates state on `main`. The
May 2026 card-generator silent-truncation incident (PR #8) is exactly
the failure mode the talk warned about: the workflow "succeeded" while
producing zero useful output, for days, with nothing alerting.

The deliverable is a scored audit so we know **where else** we are one
incident away from a similar failure, plus three concrete follow-on tick
proposals for the highest-impact gaps.

## Scope

In scope:
- `audit_checklist.md` — 14 criteria adapted from the MLOps talk, with
  our additions (idempotency, secret-rotation, gitleaks coverage, etc.).
  Each criterion has a one-paragraph rubric so the score is defensible.
- `yolo_score.md` — every criterion scored PASS / PARTIAL / FAIL with
  evidence pointing at a real file path, workflow file, or workflow run.
  Honest scoring — we fail several.
- `top_gaps.md` — the three FAIL items reformulated as follow-on tick
  cards (effort estimate, hypothesis, deliverables) ready to promote.

Out of scope:
- Fixing the gaps. Each becomes a follow-on tick.
- Auditing other cron workflows (drift-check, daily-research) — those
  are smaller blast radius; tick_tock first.
- Stretching the checklist to cover user-facing agents (we don't have
  any yet).

## Files in this directory

- `README.md` — this file
- `audit_checklist.md` — the 14-criterion rubric
- `yolo_score.md` — pass/partial/fail evidence for each criterion
- `top_gaps.md` — three follow-on tick proposals for the highest-impact
  FAILs

## How to consume this

1. Read `audit_checklist.md` first — understand what each criterion
   means before reading the score so you can challenge the rubric, not
   just the verdict.
2. Read `yolo_score.md` — every score cites a file path; spot-check
   three at random to validate.
3. Read `top_gaps.md` — these are tick-ready proposals. Promote any of
   them at the next backlog triage.

## Honesty pledge

This audit was built knowing the answer: yolo-loop will fail several
criteria. The scoring leans toward FAIL when ambiguity exists, because
PARTIAL is cheap and PASS without evidence is worthless. If the audit
passes everything, the audit is wrong.
