# Lead Architect — yolo-projects

> **NOTE:** This repo's `council.py` does its own synthesis via auto-downgrade rules + lessons-veto + escalation, NOT the canonical lead-architect-persona pattern.
>
> See `.harness/scripts/council.py` and `.harness/scripts/council_rules.md` for how synthesis actually works here:
>
> 1. Each angle (`bugs`, `cool`, `guide`, `lessons`, `security`, `ui`, `usefulness`) returns a `Verdict` JSON.
> 2. `lessons` has veto power — a `lessons` OBJECT with valid `precondition_evidence` halts the build.
> 3. Four enforcement passes auto-downgrade specific OBJECT classes (parse-failure retry, LESSONS-veto precondition enforcement, goalpost-move, BUGS hallucination).
> 4. Two-attempt deadlock on a single angle writes `COUNCIL_ESCALATION.md` at repo root and halts the build.
>
> No persona synthesizes the angles into a single verdict — the deterministic rules in `council.py` do it.
>
> This file exists because:
>
> 1. The canonical `harness check` topology requires `.harness/council/lead-architect.md` for any V0.3.x consumer repo.
> 2. The harness-cli's PR-triggered `council.yml` (separate from this repo's `tick_tock.yml` cron) DOES use a lead-architect synthesis pattern, and would invoke this file as its synthesizer if a PR-triggered council run happened. **In practice the PR-triggered council in this repo will be running over rare manual changes (like the conformance PR itself), not the hourly cron's project gates** — so the canonical synthesis pattern is a fallback for human-driven PRs only.
>
> If a PR-triggered council DOES fire and ends up reading this file as the synthesizer, default to the canonical synthesis rules from harness-cli's V0.3.1 `lead-architect.md` (verdict = CLEAR / CONDITIONAL / BLOCK based on persona scores + drift detection). The `tick_tock` cron does NOT consult this file.
