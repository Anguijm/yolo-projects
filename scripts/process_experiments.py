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

# Videos sent to Claude per API call. The May 8 fix raised max_tokens from
# 4K → 16K to handle "20+ video runs," but a 35-day backfill (54 videos) still
# truncated at the cap. Rather than chasing token limits, batch the input so
# each call's output fits comfortably under 16K with headroom. At up to 2
# cards/video × ~270 tokens/card, 15 videos = ~8K output tokens worst case.
BATCH_SIZE = 15

# The operator's projects, judged by the second relevance field of each card.
# Widened 2026-10-15 by the operator's ruling: until then the prompt asked only
# for ideas for "an AI development system" and the June 2026 triage rubric
# (experiments/backlog-triage-2026-06-24.md) discarded local-model, hardware,
# game-engine and app-development items as off-domain.
OPERATOR_PROJECTS = """\
- The flagship pages in this repo: Markdown Deck, Naval Scribe and PDF to CSV (offline single-file web tools), plus offline tools built from prompts inside a locked-down work chat model (an estimator, a resource map, a workbook converter)
- Push to Talk: an Android dictation bubble and keyboard backed by whisper.cpp and llama.cpp on a 128 GB AMD Strix Halo box (Ryzen AI Max+ 395, Radeon 8060S, Vulkan and ROCm); local inference, quantization and serving on that hardware count
- Local model training on the same box: fine-tuned writer and editor models (LoRA), and a shared CPU forecasting service
- mini-forge: text or image to 3D to Bambu Lab X1C miniature printing (local image generation, Hunyuan3D, Pixal3D, TRELLIS, mesh cleanup, slicing)
- A Flutter family calendar app (Android, self-hosted backend)
- Roadtripper: a road-trip planner web app on Firebase App Hosting
- Ghosts with Guns: an Unreal Engine 5.8 port of an action game, and video editing with Unreal effects
- A Markdown knowledge vault with a Quartz digital garden and a weekly newsletter (capture, verify, publish), and a daily researched-stories newsletter
- Forecasting side projects: Polymarket paper trading, fantasy football, NCAA bracket predictions
- Home operations: always-on Claude Code sessions run by an ops session, scheduled jobs under a failure guard, the home network"""

# Valid channel-shortcode pattern. The id prefix (e.g., "aie" in
# "aie-2026-06-11-foo") is the catalog's canonical channel identifier;
# source.channel is purely cosmetic and was previously inconsistent
# (@-prefix, casing, "Nate Herk" vs "NateHerk", etc.). We overwrite
# source.channel with the id prefix so aggregates work.
_SHORTCODE_RE = re.compile(r'^[a-z0-9_]+$')


def canonicalize_card_channel(card):
    """Set source.channel to the id-prefix shortcode. Skips cards whose id
    doesn't look like '<shortcode>-...' so unexpected formats don't get
    silently mangled."""
    eid = card.get('id', '')
    if not eid or '-' not in eid:
        return
    shortcode = eid.split('-', 1)[0]
    if not _SHORTCODE_RE.fullmatch(shortcode):
        return
    card.setdefault('source', {})['channel'] = shortcode


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

For each video, create 1-2 experiment cards IF the video contains an actionable idea for EITHER (a) an AI development system (agent workflows, harnesses, Claude Code practice) OR (b) one of the operator's projects listed below. Skip pure news/commentary with no actionable experiment. Skip YouTube Shorts.

The operator's projects (judge relevance_to_operator_projects against these):
{OPERATOR_PROJECTS}

Score both relevance fields the same way: start the field with high, medium or none, then a colon and one sentence saying what it maps to (for the projects field, name the project). A card is in scope when either field is high; a video that is high on neither gets no card.

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
    "relevance_to_yolo_loop": "<high|medium|none>: how this maps to our dev loop.",
    "relevance_to_operator_projects": "<high|medium|none>: which operator project and how, or none."
  }},
  "status": "backlog",
  "status_history": [{{"status": "backlog", "date": "{datetime.now(timezone.utc).strftime('%Y-%m-%d')}", "note": "Extracted from YouTube RSS"}}],
  "outcome": null,
  "verdict": null,
  "notes": ""
}}

Channel shortcodes: @NateBJones=nb, @MLOps=mlops, @DavidOndrej=do, [un]prompted=up, @NateHerk=nh, @AIJasonZ=aij, @echohive=eh, @ShawTalebi=st, @Mark_Kashef=mk, @aiDotEngineer=aie, @mattpocockuk=mp, @indydevdan=idd, @ColeMedin=cm, @AILABS-393=ail, @LatentSpacePod=ls, @anthropic-ai=ant, @LangChain=lc, @donatocapitella=dc, @AZisk=az, @AliElZoheiry=aez, @PhilippLackner=pl, @PixelArtistry_=pa

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

    print(f"Processing {len(new_videos)} new videos in batches of {BATCH_SIZE}...")

    # Batched API calls. Per-batch failures are logged but don't abort the
    # whole run — we keep whatever cards we got from successful batches.
    n_batches = (len(new_videos) + BATCH_SIZE - 1) // BATCH_SIZE
    all_cards = []
    failed_batches = 0
    for batch_idx in range(n_batches):
        start = batch_idx * BATCH_SIZE
        batch = new_videos[start:start + BATCH_SIZE]
        print(f"  Batch {batch_idx + 1}/{n_batches}: {len(batch)} videos...")
        try:
            cards = generate_cards_via_api(batch, len(experiments))
            for c in cards:
                canonicalize_card_channel(c)
            all_cards.extend(cards)
            print(f"    -> {len(cards)} cards")
        except json.JSONDecodeError as e:
            failed_batches += 1
            print(f"    ERROR batch {batch_idx + 1}: non-JSON output: {e}", file=sys.stderr)
            print(f"      doc tail (last 500 chars): {e.doc[-500:]!r}", file=sys.stderr)
            print(f"      position: {e.pos} of {len(e.doc)} chars", file=sys.stderr)
            continue
        except Exception as e:
            failed_batches += 1
            import traceback
            print(f"    ERROR batch {batch_idx + 1}: {type(e).__name__}: {e}", file=sys.stderr)
            traceback.print_exc()
            continue

    if failed_batches:
        print(f"WARN: {failed_batches}/{n_batches} batch(es) failed; "
              f"continuing with {len(all_cards)} cards from successful batches",
              file=sys.stderr)

    # Deduplicate by ID
    existing_exp_ids = {e["id"] for e in experiments}
    added = 0
    for card in all_cards:
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
