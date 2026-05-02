# Plan: phase4-add-karpathy

## Goal
Add Andrej Karpathy's YouTube channel to the Phase 4 ingestion roster so we
see his actual videos directly, not the four-turtles-down reaction
commentary we get today.

## Context
Today the channel roster (`fetch_youtube_rss.py` `CHANNELS` dict) tracks
11 channels. Karpathy's content reaches us only via NateBJones, NateHerk,
and DavidOndrej reacting to him. Recent indirect mentions:

| Date | Source | Title |
|---|---|---|
| 2026-04-22 | NateBJones | Karpathy's Wiki vs. Open Brain |
| 2026-04-19 | NateBJones | Karpathy's Agent Ran 700 Experiments While He Slept |
| 2026-04-06 | NateHerk | Andrej Karpathy Just 10x'd Everyone's Claude Code |

Each of these would be a stronger signal if it came from Karpathy's mouth
instead of a reactor's title.

## Scope

**In:**
- One-line addition to `CHANNELS` in `fetch_youtube_rss.py`:
  `"@AndrejKarpathy": "UCPk3RbfyaUwgTUXTgIANI3w"`
- Verify with the next cron run that his channel is fetched and his
  recent uploads appear in `experiments.json` (or are appropriately
  skipped).
- One-week observation period: read the resulting cards, decide if his
  content is generating useful experiment ideas or just noise.
- Document the decision in `experiments/phase4-add-karpathy/REPORT.md`.

**Out:**
- Re-classifying his channel's posting frequency / signal score (the
  existing `process_experiments.py` skip rules handle that).
- Adding any other new channels (separate decision).
- Re-fetching historical Karpathy uploads. Forward-only.

## Approach

### Why this is low risk
- Karpathy posts infrequently (~1-2 videos/month). Worst case the cron
  generates 1-2 extra cards/month. Most likely outcome: useful primary
  source, some cards `skipped` for being too educational/meta to be
  actionable.
- Reverting is a one-line removal.
- The existing skip rules already filter "pure news/commentary" and
  "Shorts" — applying them to a new channel costs nothing.

### Why this could be wrong
Karpathy's content skews educational ("how to think about LLMs") rather
than productized ("here's a tool you can adopt"). The YOLO loop wants
the latter. If a week's worth of his uploads all `skipped`, the answer
is "low-signal channel for our purpose" — not "broken pipeline".

## File Layout
- `experiments/phase4-add-karpathy/plan.md` — this file.
- `fetch_youtube_rss.py` — one line added to CHANNELS dict.
- `experiments/phase4-add-karpathy/REPORT.md` — written after the
  one-week observation. States: kept / removed / inconclusive.

## Function Map
None. Single dictionary entry.

## Security
- The channel ID `UCPk3RbfyaUwgTUXTgIANI3w` is public information.
- No new code paths, no new dependencies.

## UI / Guide
Not applicable.

## Edge Cases
- **Karpathy's channel ID was wrong** (I sourced it from public listings
  but didn't verify against the live YouTube API). Validation: the
  next cron run's stderr will show "Failed to fetch UCPk3..." if the
  ID is bad. Easy fix.
- **Channel uploads no videos in the observation week** → extend
  observation by one more week before deciding.
- **He uploads a 4-hour deep-dive that produces 8 cards** → the existing
  per-video card cap in `process_experiments.py` already handles this
  (1-2 cards per video).

## Test Strategy
- Manual: run `fetch_youtube_rss.py --since 2026-04-15` after the
  channel addition; confirm at least one Karpathy video appears in the
  output.
- One cron cycle: confirm the cron commit on origin/main includes
  Karpathy-sourced cards (or appropriately skipped entries).
- One-week observation: count of (kept / skipped / total) Karpathy
  cards. If kept >= 1 over the week, consider the addition successful.
- Rollback test: removing the line and re-running
  `fetch_youtube_rss.py` should produce the same output as before.

## Estimated effort
~10 minutes of build + 1 week of observation. Trivial tick.

## Council focus
- **PLAN**: is the channel ID correct? (verify before merge)
- **IMPLEMENTATION**: just the one-line addition; nothing else.
- **TESTS**: one cron cycle + one week of cards.
- **OUTCOME**: REPORT.md states keep / remove / extend, with the
  count of useful cards generated as the deciding number.
