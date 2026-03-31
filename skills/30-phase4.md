# Skill: Phase 4 YouTube Pipeline

**Description:** Fetch new videos from monitored channels, process them into experiment cards, and maintain the experiment backlog. Run on daily cron or on-demand.

**Trigger:** Daily cron at 6:13am, or user says "fetch videos" / "phase 4" / "check channels".

---

## Methodology

### 1. Fetch
- Run `python3 phase4_fetch.py`
- This checks all 5 channels via yt-dlp, diffs against processed IDs
- New videos go to `phase4_queue.json`

### 2. Process Queue
- For each unprocessed video in `phase4_queue.json`:
  - Use `mcp__gemini__gemini-youtube-summary` (style: detailed) to get content
  - Evaluate: does this video contain actionable experiments for our dev loop?
  - If YES: extract 1-3 experiment cards following the schema in `phase4_experiments.md`
  - If NO: mark as processed with note "no experiments extracted — [reason]"
  - Check for duplicates against existing experiments before appending

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
- `phase4_queue.json` (what needs processing)
- `experiments.json` (existing experiments for dedup)
- `phase4_experiments.md` (processing protocol)

## Output
- Processed queue entries
- New experiment cards in `experiments.json`
- Updated `phase4_queue.json`
