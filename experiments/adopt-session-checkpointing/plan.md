# Plan — adopt-session-checkpointing (infrastructure tick)

## Goal
Add `compress_session.py`, a fast (~2s, offline) utility that emits a markdown **session-handoff** document so a fresh YOLO session can resume work faster than reading raw `session_state.json` — summarizing recent commits (grouped, de-noised), open/deferred council escalations with resolution hints, the top-of-queue tick spec, and memory-drift flags.

## Scope
**In scope:**
- `compress_session.py` (~180 LOC) — a read-only CLI that synthesizes a resumable handoff blob from git history + `.harness/session_state.json` + `_hot.md`.
- Markdown output by default (the shape that plugs directly into the next session's startup context), with an opt-in `--json` structured mode (answers the PLAN council_focus: markdown-first, JSON available).
- `experiments/adopt-session-checkpointing/README.md` — what it is, when to invoke, how the output plugs into session startup.

**Explicitly NOT in scope:**
- Any change to the tick-tock dispatch code, cron workflow, or `council.py`.
- Writing/mutating `session_state.json` or any state file — the tool is strictly read-only.
- Creating a root-level `<name>/` project dir or `index.html` (infrastructure ticks live only under `experiments/<name>/`).
- A live "context compression" LLM call — compression here is deterministic summarization, no network, no cost, no `ANTHROPIC_API_KEY`.

## Approach
Subtasks, in sequence:
1. **Git collection (`collect_commits`)** — shell out to `git log` with a stable `%H%x00%P%x00%s` format; parse hash, parent list, subject. Bounded by `-n`.
2. **Commit classification (`classify_commit`)** — map each commit to a category from its subject prefix (`cron(tick)`, `cron(tock)`, `cron(phase4)`, `drain`, `resolve`, `ESCALATION`, `fix`, …) and merge-ness (≥2 parents → `merge`). This is the IMPLEMENTATION council_focus: phase4 cron + merge commits must collapse to noise-free summaries, not flood the handoff.
3. **Grouping (`group_commits`)** — bucket by category; collapse high-frequency low-signal buckets (`phase4`, `merge`) to a one-line count + newest example, list signal buckets (tick/tock/escalation/resolve) individually.
4. **State extraction** — `load_state` (defensive JSON read with one retry on race), `top_of_queue` (head approved tick + its council_focus), `escalations` (open + deferred, each with a resolution hint).
5. **Drift detection (`memory_drift_flags`)** — parse the headline counts in `_hot.md` and compare to live `session_state.json` (portfolio total/active, approved/pending queue lengths); flag any mismatch so a resuming session knows the cache is stale.
6. **Rendering** — `render_markdown` (default) and `render_json` (`--json`); both built from one `build_handoff` dict so they never drift.
7. **CLI (`main`)** — argparse: `-n/--commits` (default 15), `--json`, `--out PATH` (default stdout), `--state`, `--hot` path overrides for testability.

Sequencing: 1→2→3 produce the commit section; 4/5 are independent reads; 6 consumes all; 7 wraps. `build_handoff` is the single source the two renderers consume.

## File Layout
- `compress_session.py` (new, ~180 lines, repo root) — the utility.
- `experiments/adopt-session-checkpointing/README.md` (new) — usage + when-to-invoke + output anatomy.
- `experiments/adopt-session-checkpointing/plan.md`, `changes.md`, `council_*.json` — gate artifacts.

## Function Map
`compress_session.py`:
- `collect_commits(n: int) -> list[dict]` — run `git log`, parse to `{hash, parents, subject}`.
- `classify_commit(subject: str, parents: list[str]) -> str` — category label.
- `group_commits(commits: list[dict]) -> dict` — bucketed + collapsed groups.
- `load_state(path: str) -> dict` — defensive JSON read, one 100ms retry on failure, `{}` on hard fail.
- `top_of_queue(state: dict) -> dict | None` — head approved tick spec (name/type/idea/council_focus).
- `escalations(state: dict) -> dict` — `{open: [...], deferred: [...]}` each with a `hint`.
- `resolution_hint(esc: dict) -> str` — derive a one-line "how to resume" from gate/reason.
- `parse_hot_counts(path: str) -> dict` — extract headline numbers from `_hot.md`.
- `memory_drift_flags(state: dict, hot: dict) -> list[str]` — mismatch flags.
- `build_handoff(args) -> dict` — orchestrates all of the above into one dict.
- `render_markdown(h: dict) -> str` — handoff markdown.
- `render_json(h: dict) -> str` — `json.dumps(h, indent=2)`.
- `main(argv=None) -> int` — argparse CLI.

## Security
Read-only tool: no writes to any state file, no network, no secrets. `git log` is invoked with a fixed argument list (`subprocess.run([...], shell=False)`) — no shell interpolation, no injection surface from commit content (subjects are data, never executed). Path overrides are opened read-only. No `eval`/`exec`. The tool reads `_hot.md` and `session_state.json` which are repo-internal; it emits nothing that isn't already on disk.

## UI
N/A — CLI tool. Output states: default markdown handoff to stdout; `--json` machine summary; `--out` writes to a file and prints a one-line confirmation to stderr. Empty/error states: missing/corrupt `session_state.json` → state sections render `unknown`/empty with an explicit "(state unavailable)" note rather than a traceback; empty approved queue → "Queue: empty — next session is a tock" note; no escalations → "none open" line. Not in a git repo → commit section notes the failure and continues.

## Guide
README documents: the premise (a deterministic handoff beats re-reading 287 KB of `session_state.json`), exact invocation (`python3 compress_session.py`, `--json`, `--out HANDOFF.md`, `-n 30`), when to invoke (session start; mid-session when context feels bloated), and how the markdown plugs into the next session's startup read. Copy is plain and imperative.

## Edge Cases
- Merge commits (≥2 parents) collapsed into a `merge` bucket, not listed individually.
- `cron(phase4)` daily-scan commits collapsed to a count + newest date (the IMPLEMENTATION focus).
- Corrupt/locked `session_state.json` mid-cron-write → one 100ms retry, then `{}` and "(state unavailable)".
- `_hot.md` missing or schema-drifted headline → drift section says "cache headline unparseable" instead of crashing.
- Empty approved queue → top-of-queue renders "none" and notes tock-eligibility.
- `-n` larger than total history → uses whatever git returns; no padding.
- Deterministic body: no wall-clock timestamps embedded in the scored content (only a "generated from N commits" note), so output is reproducible for the same git+state.

## Test Strategy
- Pre-filter: `python3 -c "import ast; ast.parse(open('compress_session.py').read())"` must pass.
- Run `python3 compress_session.py` against today's real git history + state — must exit 0 and produce a readable handoff containing a Commits section, an Escalations section, a Top-of-queue section, and a Drift section.
- Run `python3 compress_session.py --json | python3 -m json.tool` — must emit valid JSON.
- Verify phase4 cron commits are collapsed (not one bullet each) and merge commits are not listed individually — confirms the IMPLEMENTATION focus.
- Verify drift detection by comparing `_hot.md` headline (83 approved) vs live state and confirming a match/mismatch flag renders correctly.
- `--out /tmp/handoff.md` writes the file and prints confirmation; stdout stays clean for piping in default mode.
