# yolo-projects: status

Updated 2026-10-23 (JST), docs refresh.

## Current state (2026-10-23)
- Operating mode since 2026-10-19 (John): no tick/tock. Keep up the three flagships and review the daily cards.
- Flagships: Markdown Deck (README refreshed 2026-10-22), Naval Scribe (unchanged since 2026-06-26, c20bed6;
  `naval-scribe/COUNCIL_ESCALATION.md` is the 2026-04-25 record from the old pipeline, kept for history), PDF to CSV
  v0.8.11 live (source `~/projects/pdf-to-csv`, private remote, all pushed). The GenAI.mil prompt series in
  `pdf-to-csv/GENAI-*` (estimator, batch, planned, resource map, leveler, style, xlsx, build guide, two design
  pages) are written by the next-big-thing session and reviewed and merged here (PRs #51 to #65).
- Daily cards: cron 05:50 JST, `scripts/daily_cards.sh` under job-guard `yolo-cards-daily`, merges its own PR on
  secret-scan plus validate, then nudges this session through `tmux -L yolo` (the nudge was missing from PR #46,
  2026-10-21, until it was restored 2026-10-23 at John's word). Verdicts: `.harness/card_reviews.md`.
- Local engine benchmark 2026-10-22 (`experiments/local-engine-bench/results.md`): no switch of dictation's
  llama.cpp build.
- DraftKings salary job: paused 2026-10-21 (crontab lines commented; backup `~/fantasy/app/crontab.bak-2026-10-21`).

## Query tool: yolo_index.py (2026-10-18)
Local search over everything written and unwritten in this repo. Rebuilds `.index/yolo.db` from the files
on every `build` (the folder is excluded from git via `.git/info/exclude`). No network, no GPU, no API key.

Indexes: 219 built project folders (README + build log entry), 1,167 cards in experiments.json
(status, verdict, outcome, history), 2,033 build_memory.db learnings, 247 build log entries, 17 phase4 queue
videos, root and .harness docs, 214 experiments/ folder files.

Commands: `python3 yolo_index.py build | stats | search "text" [--kind K --status S] | cards --status discarded -q text | projects -q text | show <slug>`

Card counts at build time: backlog 609, discarded 348, adopted 90, deferred 56, done 48, in_progress 10, skipped 6.

## Disabled on purpose (do not re-enable)
- Phase 4 research workflow: off since 2026-10-17 (no API key).
- Feed snapshot cron: off since 2026-10-18 (John's Gemini task replaced it).

## Direct pushes to main (noted 2026-10-22, at John's request; no history rewrite)
Nine doc commits by this session reached main without a pull request between 2026-10-20 and 2026-10-22:
1e26cec, 2bcbf90, d79868a, 78697bf, 03127c9, f1f5765, edcf7e4, 46c783b, 776df60. branch-guard failed on the
three 2026-10-22 pushes (f1f5765, edcf7e4, 776df60). From 2026-10-22 on, changes go through a pull request.
Check: `git log origin/main --format='%h %s' | grep -v '(#[0-9]*)$' | grep -v 'Cards from the Gemini'`.

