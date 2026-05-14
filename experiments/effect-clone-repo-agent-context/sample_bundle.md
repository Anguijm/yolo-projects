# Repo context bundle

## Overview

**Repo conventions for Claude.** ## Responding to "status"

## Changed files

- `scripts/process_experiments.py`

## Changed files — full post-diff contents

### `scripts/process_experiments.py`

```py
#!/usr/bin/env python3
"""Process YouTube RSS scan results into Phase 4 experiment cards.

Uses Anthropic API to generate experiment cards from video titles.
Deduplicates against existing experiments.json.

Usage: python3 scripts/process_experiments.py /tmp/rss_scan.json
"""
import json
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def get_existing_video_ids(experiments):
    """Extract video IDs from existing experiments for dedup."""
    ids = set()
    for e in experiments:
        url = e.get("source", {}).get("video_url", "")
        m = re.search(r"v=([a-zA-Z0-9_-]+)", url)
        if m:
            ids.add(m.group(1))
    return ids


def generate_cards_via_api(videos, existing_count):
    """Call Anthropic API to generate experiment cards from video list."""
    import anthropic

    client = anthropic.Anthropic()

    blocks = []
    transcripts_present = 0
    for v in videos:
        block = f"- {v['channel']}: \"{v['title']}\" ({v['url']})"
        transcript = v.get("transcript")
        if transcript:
            transcripts_present += 1
            block += (
                f"\n  TRANSCRIPT (auto-captions, possibly truncated; "
                f"original {v.get('transcript_full_chars', len(transcript))} chars):\n"
                f"  ---\n{transcript}\n  ---"
            )
        blocks.append(block)
    video_list = "\n".join(blocks)

    transcript_note = (
        "Some videos include auto-generated captions in a TRANSCRIPT block. When a transcript is present, base hypothesis and what_they_did on the transcript content, NOT on the title alone. When absent, fall back to inferring from the title."
        if transcripts_present
        else "Transcripts are not provided for these videos; infer hypothesis and what_they_did from the title."
    )

    prompt = f"""You are the Phase 4 YouTube Experiment Tracker. Generate experiment cards from these videos.

{transcript_note}

Videos to process:
{video_list}

For each video, create 1-2 experiment cards IF the video contains an actionable idea for an AI development system. Skip pure news/commentary with no actionable experiment. Skip YouTube Shorts.

Output a JSON array. Each card must have this exact structure:
{{
  "id": "<channel_shortcode>-<YYYY-MM-DD>-<slug>",
  "source": {{
    "channel": "<channel name>",
    "video_title": "<title>",
    "video_url": "<url>",
    "published_date": "<YYYY-MM-DD>",
    "ingested_date": "{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
  }},
  "experiment": {{
    "title": "Short imperative title",
    "hypothesis": "If we [do X], then [outcome Y] because [reason Z].",
    "what_they_did": "What the speaker described.",
    "effort_estimate": "low | medium | high",
    "relevance_to_yolo_loop": "How this maps to our dev loop."
  }},
  "status": "backlog",
  "status_history": [{{"status": "backlog", "date": "{datetime.now(timezone.utc).strftime('%Y-%m-%d')}", "note": "Extracted from YouTube RSS"}}],
  "outcome": null,
  "verdict": null,
  "notes": ""
}}

Channel shortcodes: @NateBJones=nb, @MLOps=mlops, @DavidOndrej=do, [un]prompted=up, @NateHerk=nh, @swyx=swyx, @GregKamradt=gk, @AIJasonZ=aij, @echohive=eh, @ShawTalebi=st, @Mark_Kashef=mk, @AndrejKarpathy=ak, @aiDotEngineer=aie

Output ONLY the JSON array. No markdown, no explanation."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        # max_tokens raised 4000 -> 16000 (2026-05-08): with supadata transcripts
        # the prompt routinely processes 20+ videos with rich content. The output
        # is up to ~50 cards × ~500 tokens each. The prior 4000 cap silently
        # truncated the JSON mid-stream, the parse failed, and the broad
        # exception handler in main() swallowed the error as 0 cards added.
        # Sonnet supports much larger output budgets; 16K gives ~3x headroom.
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

    # Surface the stop reason so output truncation is diagnosable from logs.
    stop_reason = getattr(response, "stop_reason", None)
    if stop_reason and stop_reason != "end_turn":
        print(f"WARN: model stop_reason={stop_reason!r} — output may be truncated", file=sys.stderr)

    return json.loads(text)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/process_experiments.py /tmp/rss_scan.json")
        sys.exit(1)

    scan_file = sys.argv[1]
    scan = json.loads(Path(scan_file).read_text())

    # Filter out shorts and get new videos
    videos = [
        v for v in scan.get("new_videos", [])
        if "/shorts/" not in v.get("url", "")
    ]

    if not videos:
        print("No new videos to process.")
        Path("/tmp/new_count.txt").write_text("0")
        return

    # Load existing experiments
    exp_file = ROOT / "experiments.json"
    experiments = json.loads(exp_file.read_text()) if exp_file.exists() else []
    existing_ids = get_existing_video_ids(experiments)

    # Filter already-processed videos
    new_videos = [v for v in videos if v.get("video_id") not in existing_ids]

    if not new_videos:
        print("All videos already processed.")
        Path("/tmp/new_count.txt").write_text("0")
        return

    print(f"Processing {len(new_videos)} new videos...")

    # Generate experiment cards.
    # Verbose error reporting (2026-05-08): the prior `except Exception as e:
    # print(f"API error: {e}")` was swallowing JSON-parse failures from
    # truncated model output, so 25 transcript-rich videos silently produced
    # 0 cards. Now we log the type, message, and a slice of the raw response
    # when available so the failure mode is diagnosable from the workflow log.
    try:
        cards = generate_cards_via_api(new_videos, len(experiments))
    except json.JSONDecodeError as e:
        print(f"ERROR: card generator returned non-JSON: {e}", file=sys.stderr)
        print(f"  doc snippet (first 500 chars): {e.doc[:500]!r}", file=sys.stderr)
        print(f"  doc snippet (last 500 chars):  {e.doc[-500:]!r}", file=sys.stderr)
        print(f"  position: {e.pos} of {len(e.doc)} chars", file=sys.stderr)
        Path("/tmp/new_count.txt").write_text("0")
        return
    except Exception as e:
        import traceback
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        traceback.print_exc()
        Path("/tmp/new_count.txt").write_text("0")
        return

    # Deduplicate by ID
    existing_exp_ids = {e["id"] for e in experiments}
    added = 0
    for card in cards:
        if card.get("id") and card["id"] not in existing_exp_ids:
            experiments.append(card)
            existing_exp_ids.add(card["id"])
            added += 1

    # Save
    exp_file.write_text(json.dumps(experiments, indent=2))
    Path("/tmp/new_count.txt").write_text(str(added))
    print(f"Added {added} experiment cards. Total: {len(experiments)}")


if __name__ == "__main__":
    main()

```

## Related files (heuristic — directory-siblings + name-prefix)

### `experiments/deterministic-script-verification/fixtures/process_experiments_expected_shape.json`

```json
{
  "top_level": "array",
  "min_items": 1,
  "max_items": 10,
  "required_keys": [
    "id",
    "source",
    "experiment",
    "status",
    "status_history"
  ],
  "key_types": {
    "id": "string",
    "source": "object",
    "experiment": "object",
    "status": "string",
    "status_history": "array",
    "outcome": "null_or_string",
    "verdict": "null_or_string",
    "notes": "string"
  },
  "source_required_keys": [
    "channel",
    "video_title",
    "video_url",
    "published_date",
    "ingested_date"
  ],
  "experiment_required_keys": [
    "title",
    "hypothesis",
    "what_they_did",
    "effort_estimate",
    "relevance_to_yolo_loop"
  ],
  "status_allowed_values": [
    "backlog",
    "in_progress",
    "done",
    "discarded",
    "deferred",
    "skipped"
  ]
}

```

### `experiments/deterministic-script-verification/fixtures/process_experiments_input.json`

```json
{
  "scan_date": "2026-05-11",
  "new_videos": [
    {
      "channel": "@NateBJones",
      "title": "How I run 10 deterministic verification checks before every deploy",
      "url": "https://www.youtube.com/watch?v=fixture00001",
      "video_id": "fixture00001",
      "published_date": "2026-05-10",
      "transcript": "Today we cover deterministic verification: pin your script outputs against fixtures, then any silent regression fails CI loud. The trick is golden-fixture diffing — don't check the text content, check the shape. Number of items in a range. Required keys present. Types match. That's it.",
      "transcript_full_chars": 320
    },
    {
      "channel": "@MLOps",
      "title": "Five ways your agent dies in production and how to monitor each",
      "url": "https://www.youtube.com/watch?v=fixture00002",
      "video_id": "fixture00002",
      "published_date": "2026-05-10",
      "transcript": "Silent truncation. Drift. Cost blow-outs. Stale dependencies. And the worst one: your agent succeeds at the wrong thing because your success metric is wrong. For each, you need a probe: log the stop reason, score outputs against a golden set, cap tokens per call, pin versions, instrument the success metric directly.",
      "transcript_full_chars": 380
    },
    {
      "channel": "@DavidOndrej",
      "title": "Random commentary on the AI scene this week",
      "url": "https://www.youtube.com/watch?v=fixture00003",
      "video_id": "fixture00003",
      "published_date": "2026-05-10",
      "transcript": "Just some thoughts on what I've been seeing this week. No real experiment to share.",
      "transcript_full_chars": 90
    },
    {
      "channel": "@AndrejKarpathy",
      "title": "Why I run my prompts through a stub-LLM before the real one",
      "url": "https://www.youtube.com/watch?v=fixture00004",
      "video_id": "fixture00004",
      "published_date": "2026-05-10",
      "transcript": "Local stub mode for any LLM-using script. Take your prompt template, render with sample inputs, save the rendered template. Then a stub mode reads a saved canonical response. You can run your full pipeline end-to-end with zero API calls. Catches shape regressions, prompt drift, and code bugs separate from model behavior.",
      "transcript_full_chars": 360
    },
    {
      "channel": "@aiDotEngineer",
      "title": "Talk: making LLM scripts CI-testable in 30 lines",
      "url": "https://www.youtube.com/watch?v=fixture00005",
      "video_id": "fixture00005",
      "published_date": "2026-05-10",
      "transcript": "Wrap your LLM call in a thin adapter. The adapter has two modes: real and stub. Stub reads JSON from disk. Real hits the API. CI runs stub mode. Production runs real. Same code path otherwise. Costs nothing to test, catches all shape regressions.",
      "transcript_full_chars": 290
    }
  ]
}

```

---
_Bundle stats: ~2858 tokens (budget 8000); 1 changed file(s), 2 related file(s)._
