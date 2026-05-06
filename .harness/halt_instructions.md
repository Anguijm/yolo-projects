# Halt — circuit breaker

Create the file `.harness_halt` at the repo root with a one-line reason to stop all harness automation:

```bash
echo "Council spiraling on PR #42 — investigating" > .harness_halt
```

While this file exists:
- `.github/workflows/council.yml` skips the Gemini call (with a PR comment explaining why).
- Any cron / scheduled workflows that check `.harness_halt` exit silently.
- `python3 .harness/scripts/council.py` exits with code 2 before any API call.

**The post-commit hook does NOT respect halt.** Local bookkeeping (`session_state.json`, `yolo_log.jsonl`) keeps running so the audit trail stays complete.

## Resume

Delete `.harness_halt` (or rename it) and the next workflow run will proceed normally:

```bash
rm .harness_halt
git add -A && git commit -m "chore: resume harness"
```

## When to halt

- Council is producing contradictory verdicts across rounds on the same surface (drift).
- Gemini is hallucinating about repo structure (e.g., flagging files that don't exist).
- A scheduled cron is producing bad data and you need time to investigate.
- You're paying for council calls during a refactor that doesn't need review.

## When NOT to halt

- A single 🔴 BLOCK that you disagree with — use admin override + paperwork instead.
- A workflow failure caused by missing secrets — fix the secret, not the harness.
- Wanting to merge faster — `[skip council]` in the PR title is the right tool for that single PR.
