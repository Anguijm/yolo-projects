# Repo conventions for Claude

## Responding to "status"

When the user asks for `status` (or a close variant), reply with a live report
sourced from artifacts on disk — **not** from Claude's memory. Every number
must come from a file read at response time.

### Output shape

```
<TL;DR headline — one line, see below>

## Cadence
- Current: tick | tock        (session_state.json.tick_tock.next_session_type)
- Last:    <type> on <date>   (tick_tock.last_session_type + timestamp)
- Queue:   <N> approved       (session_state or _hot.md tick queue)

## Portfolio
- <total> projects / <active> active   (_hot.md)
- Recent: <up to 5 slugs>

## Phase 4 ingestion
- Last cron: <age>h ago (<UTC> / <JST>) — status: success | empty | stale
- Channels:  <tracked> tracked, <failed> feeds failed last run
- Videos:    <new> new in last scan
- Experiments: <backlog> backlog · <in_progress> in-flight · <done> done
  (verdicts: <adopt> adopt · <discard> discard · <iterate> iterate)
- Top backlog: <id> — <title>   (up to 3; fewer if backlog is smaller)

## Council
- Escalations open: <N>   (COUNCIL_ESCALATION.md present? when?)
- Last gate run:    <gate> on <project> — <verdict summary>

## Session
### Work done     Commits on this branch: <SHA> <one-line summary>
### In flight     Uncommitted edits, running processes, open investigations
### Blockers      Concrete, not vague
### Next          1–2 bullets, not a roadmap
```

### TL;DR headline (line 1, always)
One line. Dot-separated. Example:
`tick · P4 fresh 2h · 3 backlog · 0 escalations · 1 uncommitted`

Fields, in order: cadence · Phase 4 freshness · backlog count · open
escalations · session state (`clean` / `N uncommitted` / `N ahead`).

### Sources of truth
Always read these at response time — never recall from prior context:

| Source | For |
|---|---|
| `session_state.json` | tick/tock, council_escalations, build_memory |
| `_hot.md` | portfolio totals, recent builds, tick queue |
| `phase4_run.json` | last cron (last_run_utc, feeds_successful/failed, new_videos_found, new_experiments_added, backlog_count) |
| `experiments.json` | per-experiment status + verdict + source |
| `fetch_youtube_rss.py` CHANNELS dict | authoritative channel roster |
| `COUNCIL_ESCALATION.md` (if present) | open veto/deadlock |
| `git status`, `git log -1`, current branch | session work state |

### Rules

1. **Live reads only.** No cached values, no recall. If a source file is
   missing or malformed, render the affected field as `unknown` — never
   `0`, never an empty placeholder.
2. **Defensive parsing.** Use `.get()` with defaults for every field;
   tolerate schema drift (renamed keys) by falling through to `unknown`.
3. **Race-safe reads.** The cron writes `phase4_run.json` and
   `experiments.json`. If a read fails mid-write, retry once after 100ms;
   on second failure render `unknown` rather than partial data.
4. **Cron freshness.**
   - `<12h` since `last_run_utc` → `success`
   - `12–24h` → `stale`
   - `>24h` → `failed` (surface prominently)
5. **Dual timezone** for cron timestamps: `21:37 UTC / 06:37 JST`. Ages
   in hours (one decimal ok under 10h, integer above).
6. **Length cap: 40 lines.** If content exceeds the cap: keep every heading,
   keep the TL;DR, elide bullets past the cap with `… +N more` at the end
   of that section. Never drop the `Session` or `Cadence` block.
7. **Drop genuinely empty sections** (say so briefly in TL;DR) but always
   keep `Cadence` and `Session`.
8. **No preamble.** No "Here's the status:". No recap of the question.

### Glossary

- **tick** — YOLO session: one new prototype from scratch this sitting.
  *Opposite of tock.* Alternates every session.
- **tock** — Flagship session: multi-session work on Markdown Deck or
  Naval-Scribe; higher quality bar.
- **Experiment status** (`experiments.json`): `backlog` → `in_progress` →
  `done`. Canonical definitions in `program.md:286-298`.
- **Experiment verdict** (set when `done`): `adopt` (promote into portfolio),
  `discard` (reject), `iterate` (needs another pass).
- **Council escalation** — lessons-angle veto or two-attempt deadlock from
  `council.py`; writes `COUNCIL_ESCALATION.md` and halts builds until
  resolved.
