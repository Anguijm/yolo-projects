#!/usr/bin/env python3
"""Card coverage check for BAR.md section 4: every card ingested on or after SINCE has a line in
.harness/card_reviews.md (its id appears there) or status 'discarded' in experiments.json.
Also reports lag: cards older than one day with no line. Exit 1 if any card is missing.

Usage: python3 .harness/bar/check_cards.py [SINCE=2026-10-15]
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
since = sys.argv[1] if len(sys.argv) > 1 else "2026-10-15"
cards = json.load(open(os.path.join(ROOT, "experiments.json")))
reviews = open(os.path.join(ROOT, ".harness", "card_reviews.md")).read()
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

checked = missing = 0
for c in cards:
    ing = (c.get("source") or {}).get("ingested_date", "")
    if ing < since:
        continue
    checked += 1
    if c["id"] in reviews or c.get("status") == "discarded":
        continue
    missing += 1
    late = " (late: over a day old)" if ing < yesterday else ""
    print(f"MISSING {c['id']} ingested {ing}{late}")
print(f"{checked} cards since {since}; {missing} missing")
sys.exit(1 if missing else 0)
