---
scope: project
---
# Skill: Phase 4 YouTube Pipeline

**Description:** Fetch new videos from monitored channels, process them into experiment cards, and maintain the experiment backlog. Run on daily cron or on-demand.

**Trigger:** Daily cron at 6:13am, or user says "fetch videos" / "phase 4" / "check channels".

---

## Methodology

### 1. Fetch
- Run `python3 fetch_youtube_rss.py --since $(date -d '3 days ago' +%Y-%m-%d) --with-transcripts > /tmp/rss_scan.json`
- This polls the RSS feed for every channel in `CHANNELS` (12 as of 2026-05), diffs against video_ids already in `experiments.json`, and pulls auto-caption **transcripts**. Transcript source precedence (`fetch_transcript` in `fetch_youtube_rss.py`):
  1. Local JSON cache at `phase4_cache/transcripts/<video_id>.json`.
  2. **supadata.ai** when `SUPADATA_API_KEY` is set — residential-IP proxy that bypasses YouTube's datacenter-IP block; this is the primary source in the cron.
  3. **youtube-transcript-api** (pip package, installed by the workflow) as a fallback — usually blocked from datacenter IPs but cheap to try once.
  4. Title-only generation if all fail.
- Transcripts are cached and truncated (head 6000 / tail 4000 chars). **Captions only — no video or audio is downloaded, and there is no frame/screenshot/vision step.**
- The cron entry point is `.github/workflows/daily_research.yml`.

### 2. Process queue
- Run `python3 scripts/process_experiments.py /tmp/rss_scan.json`
- The script calls Anthropic to generate 1-2 experiment cards per video. Cards include the transcript when present (otherwise title-only).
- Skip rules: pure news/commentary, YouTube Shorts.
- Cards are appended directly to `experiments.json` (not a queue file).

### 3. Experiment Card Schema
```json
{
  "id": "<channel_shortcode>-<YYYY-MM-DD>-<slug>",
  "source": { "channel", "video_title", "video_url", "published_date", "ingested_date" },
  "experiment": {
    "title": "Imperative verb phrase",
    "hypothesis": "If we [X], then [Y] because [Z]",
    "what_they_did": "What the speaker described",
    "actionable_steps": ["Step 1", "Step 2"],
    "success_metric": "How we know it worked",
    "effort_estimate": "low | medium | high",
    "relevance_to_yolo_loop": "How this maps to our system",
    "target_project_ids": ["project-name"]
  },
  "status": "backlog"
}
```

### 4. Commit
- `git add phase4_queue.json experiments.json`
- `git commit` with summary of what was processed
- `git push`

## Monitored Channels
1. @NateBJones — AI strategy, daily
2. @MLOps — Production ML, weekly
3. @DavidOndrej — Autoresearch, agentic coding, 2-3/week
4. [un]prompted — Conference talks, batch
5. @NateHerk — AI workflows, Claude Code, 2-3/week

## Input
- RSS feed of each channel in `fetch_youtube_rss.py:CHANNELS` (live).
- `experiments.json` (existing experiments for dedup against video_id).
- `SUPADATA_API_KEY` env var — enables the **primary** (supadata) transcript source. Without it the pipeline falls back to `youtube-transcript-api` (installed by the workflow), then title-only.
- Transcript cache at `phase4_cache/transcripts/` (JSON snippet lists).

## Output
- New experiment cards appended directly to `experiments.json`.
- `phase4_run.json` updated with per-cron-cycle stats (channels scanned, transcripts fetched, etc).
