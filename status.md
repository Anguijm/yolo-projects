# yolo-projects: status

Updated 2026-10-24 (JST), docs refresh.

## Current state (2026-10-24)
- Operating mode since 2026-10-19 (John): no tick/tock. Keep up the three flagships and review the daily cards.
- Flagships: Markdown Deck (README refreshed 2026-10-22), Naval Scribe (unchanged since 2026-06-26, c20bed6;
  `naval-scribe/COUNCIL_ESCALATION.md` is the 2026-04-25 record from the old pipeline, kept for history), PDF to CSV
  v0.8.11 live (source `~/projects/pdf-to-csv`, private remote, all pushed). The GenAI.mil prompt series in
  `prompt-built-tools/GENAI-*` (moved from pdf-to-csv/ on 2026-10-24, PR #69; estimator v0.6, the weight test v0.2, batch v0.8, planned v0.5,
  resource map, leveler, style, xlsx (superseded for new builds by the converter), the dictionary page (PR #72),
  the workbook converter page (PR #74), build guide v0.6, two design pages) are written by the next-big-thing
  session and reviewed and merged here (PRs #51 to #98; #98, 2026-10-31, was the edge-case round John lifted his hold for: eight faults plus two slice-boundary gaps pinned, 237 edge checks, 0 failing). From 2026-10-27 (John's ruling, relayed by next-big-thing): when
  John tells it to handle or push a series, or that he is walking away, next-big-thing merges its own prompt PR once the
  build passes and its scan is clean; this session then reviews the merged commit and any point becomes its next PR.
  PRs opened without that instruction are still reviewed and merged here.
- Daily cards: cron 05:50 JST, `scripts/daily_cards.sh` under job-guard `yolo-cards-daily`, merges its own PR on
  secret-scan plus validate, then nudges this session through `tmux -L yolo` (the nudge was missing from PR #46,
  2026-10-21, until it was restored 2026-10-23 at John's word). Verdicts: `.harness/card_reviews.md`.
- Local engine benchmark 2026-10-22 (`experiments/local-engine-bench/results.md`): no switch of dictation's
  llama.cpp build.
- DraftKings salary job: paused 2026-10-21 (crontab lines commented; backup `~/fantasy/app/crontab.bak-2026-10-21`).

## Open items
- 2026-10-25 | The card nudge reaches this session's input box but is never submitted: `tmux capture-pane` shows the
  PR #68 and PR #78 nudges typed, unsent, at the prompt (the text and Enter in one send-keys call arrive as one paste,
  so Enter becomes a newline). Fixed 2026-10-25 at John's go: daily_cards.sh sends the text, then Enter on its own a
  second later. Cards from both days were reviewed by hand. Still failing on 2026-10-27: the PR #88 nudge sat unsent in the input box like the others. A throwaway session on its own
  tmux socket takes the same text plus a separate Enter and runs it, even with older text already in the box, so the fault is
  specific to this session (remote control on; a dialog on screen at 05:52 would eat the Enter, which the test reproduced).
  Cards from PR #88 reviewed by hand. PR #90 (John: snapshot and retry) saves the pane to nudge-*.txt and retries Enter once. Root cause found 2026-10-31: under set -e the 124 exit of the
  one-second wait ended the script before every Enter since PR #81 (only nudge-before.txt was ever written); fixed in PR #95.
  Cards from PRs #91 to #94 reviewed by hand 2026-10-31. Confirmed 2026-11-01: PR #99 run logged "nudge sent on the retry" (the first Enter left it in the box, the retry submitted it, and the eight stacked nudges from PRs #68 to #99 arrived as one message). The tighter card rules (PR #96) made 1 card that day. | me
- 2026-10-26 | The 05:50 run wrote no rows.json: a second Claude in Chrome browser has been connected since 2026-10-25, and
  the reader would not pick one. Fixed in PR #86: the reader selects this Chrome by device id (`CHROME_DEVICE` in
  `scripts/daily_cards.sh`), both browsers stay connected (John's ruling via ops). Reader tested alone: 7 rows. The
  missed rows fall inside the next run's 3-day window. Confirmed 2026-10-27: 11 rows read, 6 cards merged as PR #88. | me
- 2026-10-24 | GENAI-PROMPTS-converter.md says Prompts X and X2 "stay in the private source", but they are public in
  the folder; next-big-thing fixed its source and will carry it on its next public touch. | next-big-thing
- 2026-10-23 | The superseded commits of PRs 60 and 61 on GitHub still show the real workforce report name; only GitHub
  support can purge them. | John
- daily | Review the 05:50 JST cards and log verdicts in `.harness/card_reviews.md`. | me

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

