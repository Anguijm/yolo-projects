# phase4-add-karpathy

**Status:** Implemented 2026-04-30 on branch `claude/phase4-ingest-scopes`.
Built directly without going through the tick queue.

Source plan at `experiments/phase4-add-karpathy/plan.md`.

## What changed

`fetch_youtube_rss.py` `CHANNELS` dict gained:

```python
"@AndrejKarpathy": "UCXUPKJO5MZQN11PqgIvyuvQ",
```

That's it. The cron picks up his channel on next run.

`scripts/process_experiments.py` channel-shortcode list updated to include `@AndrejKarpathy=ak`.

## Channel ID verification

The plan originally proposed `UCPk3RbfyaUwgTUXTgIANI3w` — that ID returned a 404 from YouTube's RSS endpoint, so it was wrong. The correct ID was resolved by following the `/@AndrejKarpathy` handle redirect:

```
$ curl -sL https://www.youtube.com/@AndrejKarpathy | grep -oE '/channel/[A-Za-z0-9_-]+' | head -1
/channel/UCXUPKJO5MZQN11PqgIvyuvQ
```

Confirmed working: the RSS feed for `UCXUPKJO5MZQN11PqgIvyuvQ` returned 15 videos including "How I use LLMs" (2025-02-27, his most recent at time of writing).

## Tests run

Live RSS fetch from this sandbox returned all 12 channels successfully (was 11 before). Karpathy slot empty in the latest scan window because his most recent upload is from Feb 2025 — that's expected; he posts infrequently.

## Observation period

Per the plan, this needs one week of cron cycles to gauge whether his content yields useful actionable cards or is mostly skipped as educational/meta. The decision (`keep` / `remove`) gets recorded in a follow-up `experiments/phase4-add-karpathy/REPORT.md` after that observation window.

## Rollback

One-line removal from the CHANNELS dict.
