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
| `.harness/session_state.json` | tick/tock, council_escalations, build_memory |
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
  `done`. Canonical definitions and the four terminal shortcuts
  (`adopted`, `discarded`, `deferred`, `skipped`) are documented in
  `program.md` under *Status Lifecycle*.
- **Experiment verdict** (set when `done`): `adopt` (promote into portfolio),
  `discard` (reject), `iterate` (needs another pass).
- **Council escalation** — lessons-angle veto or two-attempt deadlock from
  `.harness/scripts/council.py`; writes `COUNCIL_ESCALATION.md` and halts builds until
  resolved.

## Council enforcement rules (auto-downgrade behavior)

`.harness/scripts/council.py` runs four enforcement passes after each gate. Each one converts
an OBJECT verdict to APPROVE-advisory and prefixes the reason with an
`[AUTO-DOWNGRADED: …]` tag. The full list — the same rules an AI agent
should expect to see firing in cron logs:

1. **Parse-failure retry** — unparseable JSON triggers one stricter retry
   before falling back to a phantom OBJECT.
2. **LESSONS VETO precondition_evidence enforcement** — LESSONS vetoes
   without a `file.ext:NN` citation OR the literal `precondition_evidence`
   in `evidence` are auto-downgraded.
3. **Goalpost-move auto-downgrade** — OBJECTs whose keyword overlap vs any
   prior reason for the same `(project, angle)` exceeds 0.35 are
   auto-downgraded.
4. **BUGS hallucination auto-downgrade** — BUGS OBJECTs that claim a
   symbol is "undefined/missing/not defined" but the cited file actually
   defines that symbol (via language-aware definition patterns) are
   auto-downgraded. Source: `detect_bugs_hallucination` in `.harness/scripts/council.py`.

See `.harness/learnings.md` "Council enforcement rules are now LIVE in code" for
the full rationale per rule and `experiments/fix-council-enforcement/` +
`experiments/fix-council-bugs-hallucination/` for the ticks that shipped them.

## V0.3.1 canonical conformance

This repo conforms to the [harness-cli V0.3.1](https://github.com/Anguijm/harness-cli/releases/tag/V0.3.1) canonical layout as of the conformance PR. Pinned in `.github/workflows/drift-check.yml`:

```
HARNESS_VERSION: V0.3.1
HARNESS_SHA: 12a9f3fe5fed4f8a7ebdfc1eb97838f8a750537d
```

**Path map** (everything under `.harness/` is the canonical home):

| What | Path |
|---|---|
| Personas | `.harness/council/{bugs,cool,guide,lessons,security,ui,usefulness}.md` (specialized 7) |
| Synthesizer placeholder | `.harness/council/lead-architect.md` (stub — see file for why) |
| The runner | `.harness/scripts/council.py` |
| Council rules ref | `.harness/scripts/council_rules.md` |
| Steering loop | `.harness/learnings.md` |
| Session state | `.harness/session_state.json` |
| Build log | `.harness/yolo_log.json` (kept `.json`, not canonical `.jsonl`) |
| Active plan | `.harness/active_plan.md` |
| Model-bump checklist | `.harness/model-upgrade-audit.md` |
| Halt instructions | `.harness/halt_instructions.md` |

**Project-portfolio data stays at root** (not harness artifacts):

`_hot.md`, `phase4_run.json`, `experiments.json`, `COUNCIL_ESCALATION.md`, `dashboard.html`, all the per-project subdirectories.

## Why this repo's council doesn't use a lead-architect synthesizer

Yolo-projects pre-dates the canonical multi-persona-synthesis pattern. Its `council.py` evolved its own synthesis discipline tailored to autonomous cron-driven gate review:

- **Per-angle JSON Verdict** with `verdict` / `severity` / `reason` / `required_fix` / `evidence` fields.
- **`lessons` veto power** — a lessons OBJECT halts builds before any other angle can override.
- **Four auto-downgrade passes** — parse-failure retry, LESSONS-veto precondition, goalpost-move, BUGS hallucination. See `.harness/scripts/council_rules.md` for the full rules.
- **Two-attempt deadlock escalation** — writes `COUNCIL_ESCALATION.md` at repo root, halts the build, awaits human resolution.

The canonical lead-architect synthesizer (verdict = CLEAR / CONDITIONAL / BLOCK based on persona scores) doesn't fire in this repo's hot path. `.harness/council/lead-architect.md` exists as a stub for canonical-topology completeness; only the rare PR-triggered `council.yml` workflow would consult it (manual changes like the conformance PR itself, not the hourly cron's project gates).

## Hook timeouts (`.claude/settings.json`)

JSON doesn't allow inline comments, so the rationale for the configured hook timeouts lives here:

- **`SessionStart` hook timeout: 10s.** Runs `.claude/hooks/session-start.sh`. Local file reads + `git log`. Typical run < 2s. Failure mode: hook killed, Claude proceeds without session-start context. Optimize the hook script rather than raising the timeout.
- **`PreToolUse` (Bash) hook timeout: 15s.** Runs `.claude/hooks/check-branch-not-merged.sh`. Includes `git fetch origin main`, which can be slow on poor networks. Failure mode: fail-OPEN by design — this is a best-effort developer guardrail, NOT a security gate. The hard merge-discipline gates are PR + council + branch-guard.yml.

## Cron-pause discipline for harness restructures

When a PR is restructuring files the hourly `tick_tock.yml` cron reads/writes (`.harness/session_state.json`, `.harness/yolo_log.json`), pause the cron via the GitHub Actions UI for the merge window. Re-enable + verify-by-manual-trigger after merge.

This was established in the V0.3.1 conformance PR (the file moves were atomic-single-commit, but a cron run firing during the merge moment could have written to old paths and diverged state). Documented here so the next restructure follows the same protocol.

## Branch-guard carve-out

The canonical `branch-guard.yml` flags any push to `main` that's not associated with a merged PR. Yolo's hourly cron pushes to `main` directly as `tick-tock-bot` (the build pipeline IS the discipline here). The local `.github/workflows/branch-guard.yml` has a `if: github.actor != 'github-actions[bot]'` carve-out at the job level so cron commits pass; human direct-pushes still get caught.

This is a deliberate deviation from the canonical V0.3.1 template. If a future harness-cli release reformulates `branch-guard.yml`, the `harness check` drift-modified flag will surface it, but the carve-out should be preserved.
