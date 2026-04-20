# Session Handoff — 2026-04-20

Read this first, then `CLAUDE.md`, then run the `status` procedure live.

## TL;DR

`tick · P4 stale ~21h · 17 backlog · 0 escalations · clean, merged`

Next session opens with a clean slate: no open escalations, no in-flight
work, `infra-guardrails` ready to resume at the IMPLEMENTATION gate.

## What's in flight

Nothing. Branch `claude/add-status-feature-RKkG1` was merged into `main`
as PR #5 (`b79dd17`). Local workspace is clean.

Last commits on main:

- `b79dd17` — merge PR #5 (infra-guardrails plan-gate escalation resolution)
- `747bee5` — tick: resolve infra-guardrails plan-gate escalation
- `ce65cd3` — cron(phase4): daily scan (the manual workflow_dispatch run
  that fixed the 9/11 feed-failure regression — all 11 feeds now healthy)

## What got done this session

1. **Phase 4 ingestion recovered.** Manual `workflow_dispatch` run produced
   11/11 feeds healthy (previous cron had only 2/11), +15 new videos, +6
   new experiment cards. `phase4_run.json` at 2026-04-19T19:34 UTC.
2. **infra-guardrails plan-gate escalation resolved.**
   - **BUGS OBJECT accepted.** Amended `experiments/infra-guardrails/plan.md`
     so `check_constraints.py` must verify each constraint row parses to
     `C# | Rule | Pass | Fail` (four non-empty pipe-separated fields), not
     just that IDs C1–C10 exist. Verifier grows ~30 → ~40 lines.
   - **SECURITY OBJECT overridden.** Same shape as `adopt-planning-mode`
     2026-04-09 precedent; broadened goalpost rule applies (program.md is
     self-authored, human-reviewed at commit time, no concrete downstream
     parser, no trust boundary). Resolution recorded in
     `experiments/infra-guardrails/COUNCIL_ESCALATION.md`.
   - `session_state.json` updated: escalation moved to
     `council_escalations_resolved`; `resume_instructions` now points at
     IMPLEMENTATION gate.
3. **Stale state files refreshed.** `_hot.md` and `session_state.json`
   phase4 section were showing pre-recovery numbers (75 experiments, 6
   channels). Bumped to live values (92 experiments / 17 backlog / 11
   channels).

## Open issues to investigate

### 1. Experiment status enum mismatch (carried from prior handoff)
`experiments.json` still uses `adopted` / `deferred` / `discarded` /
`skipped` as statuses alongside the canonical `backlog` / `in_progress` /
`done`. Live breakdown (2026-04-20): done 44, adopted 10, discarded 11,
deferred 8, skipped 2, backlog 17. Either `CLAUDE.md` glossary /
`program.md:286-298` need expanding to sanction these, or the ledger
needs migrating. Not urgent — the status procedure tolerates it — but
the canonical documentation still doesn't match reality.

### 2. `tick_tock.last_session_timestamp` still missing
`session_state.json.tick_tock` has `last_session_date` (2026-04-13) but
no timestamp. `CLAUDE.md` status spec expects one; it currently renders
as the date alone. Backfill from the last tock commit or accept as known
gap.

### 3. Phase 4 `status: success` threshold is too lenient
Root cause behind last handoff's "9/10 feeds failed" false-success.
`.github/workflows/daily_research.yml:92` only requires
`feeds_successful > 0`. Today's run happened to be 11/11, but the bug is
still latent — one working feed will still report `success`. Tighten to
e.g. `feeds_successful >= channels_scanned * 0.8` and surface `partial`
or `degraded` below that.

### 4. Why did feeds regress 2/11 → 11/11 on a manual dispatch?
Worth an inspection. IP-based rate-limit? GitHub Actions runner pool
variance? User-Agent / rolling-cache effects? A targeted probe (fire
the workflow twice in quick succession, compare) would narrow it down.

## Policy / convention changes made this session

None. This session was pure state reconciliation — no new rules, no new
skills, no new council angles.

## Current state (read live — these numbers will drift)

| Area | Last known (2026-04-20) |
|---|---|
| Branch | `claude/add-status-feature-RKkG1` — fully merged to main, 0 unmerged commits |
| Open PRs | 0 |
| Open escalations | 0 |
| Phase 4 backlog | 17 |
| Tick queue | 9 approved, 0 pending |
| Portfolio | 223 built, 97 active |
| Experiments | 92 total: 44 done, 10 adopted, 11 discarded, 8 deferred, 17 backlog, 2 skipped |
| Verdicts (done) | 34 adopt, 10 discard, 0 iterate |
| Channels | 11 tracked, 0 failed on last run |
| Last cron | 2026-04-19 19:34 UTC |
| Cadence | next = `tick`; last = `tock` on 2026-04-13 |
| `resume_instructions` | "Resume infra-guardrails build at IMPLEMENTATION gate with amended plan.md" |

## Next-session first moves

1. `git checkout main && git pull` — pick up the merged PR #5.
2. Delete stale local branch: `git branch -d claude/add-status-feature-RKkG1`
   (if still present).
3. Run the `status` procedure live and confirm numbers match this handoff
   (allow drift for a fresh cron — next scheduled run is 21:37 UTC).
4. Start the next tick. Per `resume_instructions`, that means resuming
   `infra-guardrails` at the IMPLEMENTATION gate with the amended
   `plan.md`: write `check_constraints.py` (~40 lines) that validates
   both (a) C1–C10 presence and (b) each constraint row parses to the
   `C# | Rule | Pass | Fail` format, then proceed to TESTS and OUTCOME
   gates.
5. Only after `infra-guardrails` closes, pop the next item from
   `tick_queue_approved` (currently `infra-yolo-evals`).

## Key files

- `CLAUDE.md` — status response spec (unchanged this session)
- `session_state.json` — tick/tock, escalations (now 0 open), phase4 counts
- `_hot.md` — 30-line portfolio snapshot (refreshed this session)
- `phase4_run.json` — last cron report (11/11 healthy, 2026-04-19 19:34 UTC)
- `experiments.json` — experiment ledger (92 entries)
- `fetch_youtube_rss.py:17-31` — CHANNELS dict (11 channels, authoritative)
- `experiments/infra-guardrails/` — next tick's workspace
  - `plan.md` — approved, format-validation scope added 2026-04-19
  - `COUNCIL_ESCALATION.md` — resolved, kept for audit trail
- `council/angles/*.md` — 7 advocate prompts (for inline council fallback
  when neither `GEMINI_API_KEY` nor `ANTHROPIC_API_KEY` is set)
