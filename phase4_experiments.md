# Phase 4: YouTube Experiment Tracker

R&D intelligence pipeline that extracts actionable experiments from YouTube content and feeds them into the dev loop.

## Status (as of 2026-04-03)

**32 experiments processed: 22 adopted, 10 parked, 0 backlog.**

The original backlog is fully cleared. New experiments arrive daily via RSS auto-discovery cron (06:15 JST).

## Architecture

Phase 4 runs as a **daily automated cron** (trigger ID: `trig_01ABkrVvExqfkAQMKTNSjXmS`):
- **Auto-discovery**: Fetches YouTube RSS feeds from 6 channels, extracts new videos
- **Processing**: Summarizes videos, extracts experiment cards, deduplicates
- **Backlog review**: Flags stale items, recommends top 3
- **State update**: Updates experiments.json + session_state.json, commits and pushes

Phase 4 does NOT replace the build/refine cycle — it injects new ideas into surviving projects.

## Channels We Monitor

1. **@NateBJones** — AI News & Strategy Daily
   - Focus: AI strategy, developer workflows, agentic systems, implementation patterns.
   - Signal: concrete practices, tool recommendations, workflow patterns, what doesn't work.

2. **@MLOps** (MLOps.community — Demetrios Brinkmann)
   - Focus: Production ML, LLMOps, agents, evaluation, memory, fine-tuning, deployment.
   - Signal: practitioner techniques, architecture patterns, production gotchas, emerging tooling.

3. **@DavidOndrej** — David Ondrej
   - Focus: AI agents, autoresearch, agentic coding, self-improving systems, privacy-first tools.
   - Signal: hands-on tutorials, agent architectures, tool comparisons, implementation walkthroughs.

4. **[un]prompted** — Conference channel (Daniel Miessler, security researchers)
   - Focus: Personal AI infrastructure, agentic systems, AI security, ML vs LLMs, vibe coding.
   - Signal: conference talks on building personal AI stacks, security-aware agent architectures, research methodologies.

5. **@NateHerk** — Nate Herk
   - Focus: AI workflows, Claude Code integrations, business automation, agentic tool comparisons.
   - Signal: practical AI workflow builds, tool reviews, integration patterns, what businesses actually want.

6. **@TwoMinutePapers** — Károly Zsolnai-Fehér
   - Focus: AI/ML research breakthroughs, physics simulations, computer graphics, generative AI.
   - Signal: concise explainers of cutting-edge papers, practical implications of new techniques.

Only process content from these six channels. If given a URL from another channel, note it and skip.

## Processing a Video

Use `gemini-youtube-summary` or `gemini-youtube` tools to get video content.

### Step 1 — Summarize (3-5 sentences max)
What is the core argument or finding? Who said it? What problem does it address?

### Step 2 — Extract Experiments (1-5 per video)
For each distinct actionable idea, create an experiment card:

```json
{
  "id": "<channel_shortcode>-<YYYY-MM-DD>-<slug>",
  "source": {
    "channel": "@NateBJones | @MLOps",
    "video_title": "...",
    "video_url": "...",
    "published_date": "YYYY-MM-DD",
    "ingested_date": "YYYY-MM-DD"
  },
  "experiment": {
    "title": "Short imperative title (e.g. 'Replace prompt chains with context engineering')",
    "hypothesis": "If we [do X], then [outcome Y] because [reason Z].",
    "what_they_did": "What the speaker described doing or recommending.",
    "actionable_steps": ["Step 1", "Step 2", "..."],
    "success_metric": "How we'll know if the experiment worked.",
    "effort_estimate": "low | medium | high",
    "relevance_to_yolo_loop": "How this maps to our dev loop specifically.",
    "target_project_ids": ["project-name-1", "project-name-2"]
  },
  "status": "backlog",
  "status_history": [],
  "outcome": null,
  "verdict": null,
  "notes": ""
}
```

### Step 3 — Output
Return summary + experiment cards as JSON. Prefer fewer, higher-quality cards. If a video is primarily news/commentary with no actionable experiment, output the summary and note "no experiments extracted."

## Effort Estimates

- **low** = try it in one session
- **medium** = a day or two of integration work
- **high** = architectural change or multi-session effort

## Status Lifecycle

```
backlog → in_progress → done → (adopt | discard | iterate)
```

When updating status, append to `status_history`:
```json
{ "status": "in_progress", "date": "YYYY-MM-DD", "note": "..." }
```

When done:
- `outcome`: What actually happened when we tried it.
- `verdict`: `adopt` (integrate permanently), `discard` (archive), `iterate` (create follow-up card).

## Tracker File

All experiment cards live in `~/yolo_projects/experiments.json`. Append-only — never delete cards, only update status.

## Backlog Review

When asked to "review backlog" or "prioritize experiments":
1. List all backlog items grouped by effort_estimate (low first).
2. Flag any superseded by newer content (mark as stale).
3. Recommend top 3 to start next based on:
   - Low effort + high relevance to yolo loop
   - Recency of source (newer = more relevant)
   - Whether prerequisite experiments are already adopted
   - Which surviving projects they target

## Duplicate Handling

Before appending a new card, check existing cards for the same idea. If duplicate, add `also_mentioned_in` to the existing card's source rather than creating a new card.

## Initial Seeding (run once)

Process the last 5 videos from EACH channel (10 total), **sequentially** (one video per processing step). Complete Steps 1-3 for each. The combined JSON array becomes the seed in `experiments.json`.

## Execution Bridge

When executing an experiment from the backlog:
1. Set status to `in_progress` with date and note.
2. Identify which surviving YOLO project(s) to test on.
3. Implement the change, test it, and evaluate against the `success_metric`.
4. Set status to `done` and fill in `outcome` + `verdict`.
5. If `adopt`: update the project permanently and note in learnings.md.
6. If `iterate`: create a follow-up experiment card with refined hypothesis.
7. Commit and push.

## Rules

- Only process @NateBJones and @MLOps content.
- Keep experiment titles action-oriented (imperative verbs).
- Never invent outcomes — `outcome` and `verdict` stay null until real results.
- Prefer fewer, higher-quality experiment cards over quantity.
- If a video has no actionable experiments, say so — don't force cards.
