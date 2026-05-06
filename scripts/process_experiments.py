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
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

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

    # Generate experiment cards
    try:
        cards = generate_cards_via_api(new_videos, len(experiments))
    except Exception as e:
        print(f"API error: {e}")
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
