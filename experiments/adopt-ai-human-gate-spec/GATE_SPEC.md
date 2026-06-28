# GATE_SPEC — who decides what in the YOLO loop

> **What this is:** the canonical answer to "who owns / who reviews / who can override step X" in this repo's autonomous build loop.
> **When to read it:** any time the actor boundary is unclear — a new gate, a disputed verdict, an escalation, or onboarding.
> Every load-bearing claim below has a grep-verifiable anchor in the [Evidence map](#evidence-map). Nothing here is aspirational; it describes the loop as it runs today (2026-06-28).

## Actors

- **cron** — the autonomous builder running headless in GitHub Actions as `tick-tock-bot`. Executes the mechanical loop one-shot per invocation. (The hourly `phase4` ingestion lane is a *separate* automated process — see note ‡ — not part of the build loop scored here.)
- **council** — the 7-angle advocate review in `.harness/scripts/council.py`. Runs at each of the 4 gates. **Normally** the `lessons` angle has veto power and 2-attempt deadlocks escalate; **during the active drain it is advisory-only and never blocks** (see ※).
- **human** — the repo owner. Sets policy, approves what enters the build queue, resolves escalations, and is the only actor permitted to direct-push to `main` outside the cron carve-out.

## Loop order

`brainstorm → plan → implement → test → review → commit → push`

## Ownership matrix

Legend: **Owns** = performs the step · **Reviews** = inspects/advises, no execution · **Overrides** = can reverse the outcome · **—** = not involved.

| Loop step | cron | council | human |
|---|---|---|---|
| **brainstorm** (idea → `tick_queue_pending`) | Owns | — | Overrides (approves into `tick_queue_approved`) ① |
| **plan** (`plan.md`) | Owns | Reviews (PLAN gate, 7 angles) | Overrides ② |
| **implement** (write deliverable) | Owns | Reviews (IMPLEMENTATION gate) | Overrides ② |
| **test** (pre-filter + TESTS gate) | Owns | Reviews (TESTS gate) | Overrides ② |
| **review** (OUTCOME gate / verdict synthesis) | Owns (records verdicts) | Owns (the verdict itself) ③ | Overrides ② |
| **commit** (`cron(tick\|tock)` to local branch) | Owns | — | Overrides (revert) |
| **push** (`git push origin main`) | Owns (cron carve-out) ④ | — | Owns (only other permitted direct-pusher) ④ |

① The human decides what is *worth building*: cron may only build items already in `tick_queue_approved`; it brainstorms into `tick_queue_pending` and never self-approves. — *cron proposes, the owner disposes.*
② The human override is exercised asynchronously via `resume_instructions` / queue edits / PR review (human + Codex), not inline during a cron run.
③ Council **owns the verdict content** but cron **owns logging it** (`council_<gate>.json`) and, during the drain, **owns the decision to ship regardless** of that verdict.
④ Both cron (`tick-tock-bot`, via the `branch-guard.yml` actor carve-out) and the human may push to `main`; every *other* direct push is flagged.

## Override ladder

Lowest authority at the bottom; each rung can reverse the one below it.

1. **human** — final say. Approves queue items, sets `resume_instructions`, resolves/defers escalations, reverts commits. Nothing overrides the owner.
2. **`lessons` council angle** — normally a hard veto that halts the build before any other angle can pass it (※ suspended to advisory during the drain).
3. **other 6 council angles** — an OBJECT triggers at most one cheap fix pass; unresolved, it is logged and (in normal mode) can deadlock-escalate after 2 attempts.
4. **council auto-downgrade passes** — four mechanical rules in `council.py` *demote* OBJECTs to APPROVE-advisory (parse-failure retry, LESSONS-veto precondition, goalpost-move, BUGS-hallucination), so a bad objection can't outrank a real build.
5. **cron** — executes; obeys all of the above. The only thing it decides unilaterally is the mechanical *how* of a build already approved.

## Why this division

**cron owns mechanical throughput.** The build loop — plan, implement, test, commit, push — is deterministic enough to automate and runs hourly without a human in the seat. The commit ledger proves this is the dominant lane: cron is the author of every `cron(tick)`, `cron(tock)`, and `cron(phase4)` commit.

**council owns judgment, not control.** Seven advocate angles each defend one lens (bugs, security, ui, guide, usefulness, cool, lessons) and emit APPROVE/OBJECT per gate. Their value is catching what a single builder misses, so they *review* every gate — but per the owner directive the drain treats them as **advisory**: verdicts are recorded for the record and the build ships regardless. This keeps a flaky reviewer from stalling a queue of 80+ approved items while preserving the audit trail.

**the human owns intent and exceptions.** Two things are deliberately *not* automated: deciding what is worth building (approval into the queue — *cron proposes, the owner decides*) and resolving the genuinely-stuck cases (escalations). The escalation ledger is real and human-touched: 65 resolved + 1 deferred, with at least one `resolve(council)` merge closing one out. Direct-push to `main` is likewise owner-or-cron-only by design; the build pipeline *is* the discipline that substitutes for human PR review on autonomous work.

‡ **phase4 note:** `cron(phase4)` commits are the YouTube/RSS ingestion scan, a separate automated lane that feeds the experiment backlog. It is cron-owned end-to-end and out of scope for the build-gate ownership above; it appears here only so its 38 commits aren't mis-read as build activity.

※ **drain note:** the advisory-only posture is the current owner directive ("COUNCIL IS ADVISORY — never blocks the drain"). When the approved queue empties and the drain ends, council's `lessons` veto and 2-attempt escalation regain blocking power; this spec marks both states so it stays accurate across that transition.

## Evidence map

Each claim → a command you can run to confirm it. All anchors resolve as of 2026-06-28.

| Claim | Grep-verifiable anchor |
|---|---|
| cron authors tick/tock/phase4 commits | `git log --oneline -200 \| grep -E 'cron\((tick\|tock\|phase4)\)'` (8 tick, 3 tock, 38 phase4) |
| escalations are real and human-resolved | `git log --oneline \| grep -E 'ESCALATION:\|resolve\(council\)'`; `session_state.json.council_escalations_resolved` (65) |
| council runs 7 angles per gate | `python3 .harness/scripts/council.py --help`; per-project `council_*.json` files |
| `lessons` has veto power (normal mode) | `grep -n 'veto' .harness/scripts/council.py` |
| four auto-downgrade passes exist | `grep -n 'AUTO-DOWNGRADED\|auto-downgrade\|detect_bugs_hallucination' .harness/scripts/council.py` and `CLAUDE.md` "Council enforcement rules" |
| council is advisory during the drain | `grep -n 'COUNCIL IS ADVISORY' .github/workflows/tick_tock_prompt.md` (the stored cron prompt) |
| cron proposes, owner approves the queue | `tick_queue_pending` vs `tick_queue_approved` in `session_state.json`; CLAUDE.md "approval-gated" |
| cron may direct-push to `main`, others flagged | `grep -n "github.actor != 'github-actions" .github/workflows/branch-guard.yml`; CLAUDE.md "Branch-guard carve-out" |
| drain is owner directive, tick-only | `grep -n 'TICK-ONLY DRAIN' .github/workflows/tick_tock_prompt.md`; `session_state.json.resume_instructions` |

---
*Canonical reference. If observed behavior diverges from a row above, the row is wrong — fix the spec, and cite the new anchor.*
