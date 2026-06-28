# adopt-session-checkpointing

**Tick type:** infrastructure
**Source experiment:** `nh-2026-04-20-claude-session-limit` (NateHerk, 2026-04-20)
**Ships:** `compress_session.py` (repo root)

## What it is

A fast, deterministic, **read-only** session-handoff generator. Instead of a
fresh YOLO session re-reading the ~287 KB raw `session_state.json` to figure
out where things stand, `compress_session.py` synthesizes a compact handoff
covering the four things a resuming session actually needs:

1. **Cadence** — next/last session type and the last tock flagship.
2. **Top of queue** — the head approved tick (name / type / idea / council_focus)
   and how many remain.
3. **Escalations** — open and deferred council escalations, each annotated
   with a one-line *resolution hint* (how to resume that specific gate).
4. **Drift flags** — mismatches between the `_hot.md` headline cache and live
   `session_state.json` (queue lengths, portfolio counts), so a resuming
   session knows when the fast-read cache is stale.

Plus a **de-noised recent-commit log**: signal commits (tick/tock/escalation/
resolve/fix/queue/council) are listed individually; high-frequency low-signal
commits (the `cron(phase4)` daily scans and merge commits) collapse to a count
+ newest example so they don't flood the handoff.

No network, no `ANTHROPIC_API_KEY`, no writes to any state file. Runs in ~1–2s.

## When to invoke

- **At session start** — pipe the markdown into your startup context as a
  faster substitute for reading raw state.
- **Mid-session when context feels bloated** — regenerate a clean snapshot of
  where the work stands without scrolling back through the transcript.

## Usage

```bash
python3 compress_session.py                  # markdown handoff to stdout (default)
python3 compress_session.py --json           # structured JSON (machine-readable)
python3 compress_session.py --out HANDOFF.md # write to a file (stdout stays clean)
python3 compress_session.py -n 30            # widen the commit window (default 15)
```

Path overrides (`--state`, `--hot`) exist for testing against fixtures.

## Output anatomy (markdown mode)

```
# Session handoff
## Cadence          → next/last session type, last tock flagship
## Top of queue     → head approved tick + council_focus + remaining count
## Escalations      → open 🔴 / deferred ⏸, each with a resolution hint
## Drift            → _hot.md-vs-live mismatches (or "none — cache matches")
## Recent commits   → signal commits listed; phase4/merge collapsed
```

## Design notes

- **Markdown-first, JSON available.** The default shape is markdown because
  that is what plugs directly into the next session's startup read; `--json`
  exists for tooling. (This was the PLAN council_focus.)
- **Deterministic body.** No wall-clock timestamps are embedded in the scored
  content, so the same git history + state produce the same handoff.
- **Defensive reads.** A corrupt/locked `session_state.json` (e.g. caught
  mid-cron-write) triggers one 100 ms retry, then degrades to "(state
  unavailable)" rather than crashing. Schema drift (queue under a flattened
  top-level key) is tolerated.
- **Sanitized.** Commit subjects and escalation reasons are treated as data:
  angle brackets are escaped and backticks defanged before rendering, so the
  handoff can't carry markdown/HTML injection into a downstream renderer.

## Verdict

**Adopt.** A deterministic handoff is strictly faster and lower-context than
re-reading the full state file, and it surfaces drift + escalation-resume hints
that the raw file does not make obvious.
