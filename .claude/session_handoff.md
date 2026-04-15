# Session Handoff — 2026-04-15

Read this first, then `CLAUDE.md`, then run the `status` procedure live.

## TL;DR

`tick · P4 stale 19.5h · 4 backlog · 1 escalation (drift?) · 3 ahead · PR#3 open`

## What's in flight

**PR Anguijm/yolo-projects#3** — `claude/add-video-phase-4-cron-uXuGU` → `main`.
Three commits, no review yet:

- `f72ef7e` — adds `@Mark_Kashef` (`UCHkzp52CldSPZqU5T49mOnA`) to
  `fetch_youtube_rss.py` CHANNELS. Roster goes 10 → 11.
- `0d3a89c` + `d36096e` — introduces `CLAUDE.md` with the repo-wide `status`
  response spec (council-reviewed, 3 OBJECT revisions folded in, no veto).

If the PR merges: delete the branch, `_hot.md` needs a refresh, next cron
will scan 11 channels. If it doesn't: keep working on this branch.

## Open issues to investigate

### 1. Phase 4 cron: 9/10 feeds failed last run
`phase4_run.json` (22:25 UTC on 2026-04-14): `feeds_successful: 1`,
`feeds_failed: 9`. Status still recorded as `success` because the workflow
only checks `feeds_successful > 0` (`.github/workflows/daily_research.yml:92`).
That threshold is too lenient — one working feed out of ten shouldn't count
as success. Either tighten the threshold or investigate why 9 feeds broke
simultaneously (YouTube rate-limit? GitHub Actions IP blocked? User-Agent
change?).

### 2. Council escalation drift
`session_state.json.council_escalations` has 1 entry but no
`COUNCIL_ESCALATION.md` exists on disk. This is the exact bug called out in
the previous handoff ("Council occasionally leaves a dangling `]` bracket …
council.py's state writing logic"). Either the escalation was resolved
without updating `session_state.json`, or the entry is stale. Inspect and
reconcile before the next tick build, or the escalation guard will halt it.

### 3. `tick_tock.last_session_timestamp` missing
`session_state.json.tick_tock` returns `?` for the last-session timestamp.
The CLAUDE.md status spec expects it. Either backfill it from git log of
the last `cron(tock):` / `cron(tick):` commit, or document it as a known
`unknown` and carry on.

### 4. Experiment status enum mismatch
`experiments.json` has `status` values of `adopted`, `deferred`,
`discarded`, `skipped` in addition to the canonical `backlog` /
`in_progress` / `done`. Either the CLAUDE.md glossary is incomplete (update
it to match reality) or `experiments.json` is using non-canonical values
that `program.md:286-298` doesn't sanction. Reconcile.

## Policy / convention changes made this session

- **`CLAUDE.md` now exists** at repo root. When the user asks for `status`,
  follow that spec exactly: TL;DR headline, 5 sections, live reads, dual-
  timezone timestamps, 40-line cap, `unknown` for missing fields.
- **Council fallback documented**: when neither `GEMINI_API_KEY` nor
  `ANTHROPIC_API_KEY` is set (e.g. Claude Code remote session), run the 7
  angles inline by reading `council/angles/*.md` yourself. Label clearly as
  an inline run, not a real `council.py` invocation.

## Current state (read live — these numbers will drift)

| Area | Last known |
|---|---|
| Branch | `claude/add-video-phase-4-cron-uXuGU`, clean, 3 ahead of origin/main |
| Open PR | Anguijm/yolo-projects#3 |
| Open escalations | 1 in session_state.json (may be drift — see above) |
| Phase 4 backlog | 4 |
| Tick queue | 5 approved in `_hot.md` |
| Portfolio | 223 built, 97 active |
| Experiments | 79 total: 44 done, 10 adopted, 11 discarded, 8 deferred, 4 backlog, 2 skipped |
| Verdicts (done) | 34 adopt, 10 discard |
| Last cron | 2026-04-14 22:25 UTC (19.5h ago — stale) |
| Cadence | next = `tick`; last = `tock` (timestamp missing) |

## Next-session first moves

1. Check if Anguijm/yolo-projects#3 merged. If yes, `git checkout main && git
   pull && git branch -d claude/add-video-phase-4-cron-uXuGU`.
2. Run `status` procedure and confirm the numbers match CLAUDE.md shape.
3. Investigate issue #1 (feed failures) before the next tick — an
   ingestion pipeline scanning one channel is not earning its cron slot.
4. Reconcile issue #2 (escalation drift) before any build starts, or the
   escalation guard will block it.

## Key files

- `CLAUDE.md` — status response spec (new this session)
- `session_state.json` — tick/tock, escalations, build memory
- `_hot.md` — 30-line portfolio snapshot (last updated 2026-04-13 19:00 UTC)
- `phase4_run.json` — last cron report
- `experiments.json` — experiment ledger
- `fetch_youtube_rss.py:17-31` — CHANNELS dict
- `COUNCIL_ESCALATION.md` — present iff a real escalation is open
- `council/angles/*.md` — 7 advocate prompts (for inline council fallback)
