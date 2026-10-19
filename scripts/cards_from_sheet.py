#!/usr/bin/env python3
"""Turn new rows of the Gemini "YOLO Watch Log" sheet into experiment cards, on the Claude subscription.

Replaces the API-key step of scripts/process_experiments.py (paused 2026-10-18). Input is the sheet exported as CSV
(first argument). Rows whose video id is already on a card are skipped. New cards are appended to experiments.json
in the same shape the old workflow wrote. Nothing is committed or pushed here.
Usage: cards_from_sheet.py sheet.csv [--dry]
"""
import csv, io, json, os, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from process_experiments import OPERATOR_PROJECTS, canonicalize_card_channel  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EXP = REPO / "experiments.json"
SHORT = {"@NateBJones": "nb", "@MLOps": "mlops", "@DavidOndrej": "do", "[un]prompted": "up", "@NateHerk": "nh",
         "@AIJasonZ": "aij", "@echohive": "eh", "@ShawTalebi": "st", "@Mark_Kashef": "mk", "@aiDotEngineer": "aie",
         "@mattpocockuk": "mp", "@indydevdan": "idd", "@ColeMedin": "cm", "@AILABS-393": "ail", "@LatentSpacePod": "ls",
         "@anthropic-ai": "ant", "@LangChain": "lc", "@donatocapitella": "dc", "@AZisk": "az", "@AliElZoheiry": "aez",
         "@PhilippLackner": "pl", "@PixelArtistry_": "pa"}
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def vid(url_or_id):
    m = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url_or_id or "")
    return m.group(1) if m else (url_or_id or "").strip()


def main():
    rows = list(csv.DictReader(io.StringIO(Path(sys.argv[1]).read_text())))
    dry = "--dry" in sys.argv
    exp = json.loads(EXP.read_text())
    seen = {vid(e.get("source", {}).get("video_url", "")) for e in exp}
    new = [r for r in rows if r.get("video_id") and r["video_id"] not in seen and r.get("watch_status", "").lower() == "watched"]
    print(f"{len(rows)} rows, {len(new)} new watched videos without a card")
    if not new:
        return
    block = "\n\n".join(
        f"VIDEO {r['video_id']} | channel {r['channel']} (shortcode {SHORT.get(r['channel'], re.sub(r'[^a-z0-9]', '', r['channel'].lower())[:4])}) | "
        f"published {r['published_date']} | {r['duration_min']} min | {r['format']}\nTitle: {r['video_title']}\nURL: {r['video_url']}\n"
        f"Summary: {r['summary']}\nMethods: {r['methods']}\nClaims: {r['claims']}\nDemos: {r['demos']}\nCaveats: {r['caveats']}"
        for r in new)
    prompt = f"""You are the Phase 4 YouTube Experiment Tracker. Generate experiment cards from these watched-video records. Each record is a factual account of what the video says, written by another assistant; base hypothesis and what_they_did on it.

{block}

For each video, create 1-2 experiment cards IF it contains an actionable idea for EITHER (a) an AI development system (agent workflows, harnesses, Claude Code practice) OR (b) one of the operator's projects below. Skip pure news or commentary with no actionable experiment.

The operator's projects (judge relevance_to_operator_projects against these):
{OPERATOR_PROJECTS}

Score both relevance fields: start with high, medium or none, then a colon and one sentence (name the project for the projects field). A card is in scope when either field is high; a video high on neither gets no card.

Output a JSON array. Each card must have exactly this structure:
{{"id": "<shortcode>-<YYYY-MM-DD published>-<slug>",
 "source": {{"channel": "<shortcode>", "video_title": "<title>", "video_url": "<url>", "published_date": "<YYYY-MM-DD>", "ingested_date": "{TODAY}"}},
 "experiment": {{"title": "Short imperative title", "hypothesis": "If we [do X], then [outcome Y] because [reason Z].", "what_they_did": "What the speaker described.", "effort_estimate": "low | medium | high", "relevance_to_yolo_loop": "<high|medium|none>: ...", "relevance_to_operator_projects": "<high|medium|none>: ..."}},
 "status": "backlog", "status_history": [{{"status": "backlog", "date": "{TODAY}", "note": "Extracted from YOLO Watch Log sheet (Gemini)"}}],
 "outcome": null, "verdict": null, "notes": ""}}

Output ONLY the JSON array. No markdown, no explanation."""
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    p = subprocess.run([os.path.expanduser("~/.local/bin/claude"), "-p", "--model", "sonnet", "--system-prompt", "You output only valid JSON.",
                        "--setting-sources", "", "--tools", "", "--no-session-persistence"],
                       input=prompt, capture_output=True, text=True, timeout=600, env=env)
    out = p.stdout.strip()
    if p.returncode or not out:
        sys.exit(f"claude failed rc={p.returncode}: {p.stderr[:300]}")
    out = re.sub(r"^```(?:json)?|```$", "", out.strip(), flags=re.M).strip()
    cards = json.loads(out)
    ids = {e["id"] for e in exp}
    added = []
    for c in cards:
        canonicalize_card_channel(c)
        if c.get("id") and c["id"] not in ids and vid(c["source"]["video_url"]) not in seen:
            added.append(c)
            ids.add(c["id"])
    print(f"{len(cards)} cards returned, {len(added)} added")
    for c in added:
        print(" -", c["id"], "|", c["experiment"]["title"][:90])
    if added and not dry:
        EXP.write_text(json.dumps(exp + added, indent=2))


main()
