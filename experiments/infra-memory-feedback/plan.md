## Goal
Extend `build_memory.py` with a `recall_outcomes` table and CLI tools to measure which learnings prevent real bugs vs. produce false positives, enabling evidence-based pruning of the learnings corpus.

## Scope
**In scope:**
- New `recall_outcomes` SQLite table added to `build_memory.db` schema (non-destructive migration)
- New CLI subcommands: `recall-stats`, `list-learnings`, `mark-veto`, `mark-fp`, `backfill-recall`
- Backfill from `session_state.json.council_escalations_resolved` (LESSONS VETO entries classified by resolution text)
- Updated module docstring listing new commands

**Not in scope:**
- Automatic citation tracking or hooks into `council.py`
- Embeddings / semantic search for learning matching
- Dashboard or `dashboard.html` integration
- Changes to `learnings.md`, `council.py`, or any other file outside `build_memory.py`
- Web UI of any kind

## Approach
Work order — each step depends on the previous:

1. **Schema extension** — append `recall_outcomes` table definition to `SCHEMA` constant in `build_memory.py`. `CREATE TABLE IF NOT EXISTS` is non-destructive on existing DBs. Add unique constraint `(learning_id, project, gate)` for idempotent backfill.

2. **`cmd_recall_stats(db, top_n)`** — query `recall_outcomes` grouped by `learning_id`, counting each outcome type. LEFT JOIN back to `learnings` for text snippet. Print two tables: top-N by `prevented_bug` count, bottom-N by `false_positive` count.

3. **`cmd_mark_outcome(db, learning_id, project, gate, outcome, notes)`** — validate args (learning_id > 0, gate in GATES set, outcome in valid set), `INSERT OR REPLACE INTO recall_outcomes`. Used by both `mark-veto` and `mark-fp` dispatch paths.

4. **`cmd_backfill_recall(db)`** — read `session_state.json`, iterate `council_escalations_resolved`. For each entry where `reason` matches `re.search(r'LESSONS\s+VETO|VETO', reason, re.IGNORECASE)`:
   - Classification uses **priority-ordered regex** (first match wins):
     1. `false_positive`: `re.search(r'false[\s._-]?positive|phantom|override.*veto|veto.*false', resolution, IGNORECASE)`
     2. `prevented_bug`: `re.search(r'\bFIX\s+APPLIED\b|\bFIX\s+ACCEPTED\b|\bACCEPTED[,.\s—-]+FIX\b|\blegitimate\s+(?:bug|concern|critique|issue|fix|objection|defect|regression)\b|\b(?:real|genuine)\s+(?:bug|defect|regression)\b', resolution, IGNORECASE)` — **tightened per BUGS critique on PLAN escalation**: bare `ACCEPTED` and bare `legitimate` previously matched too broadly (e.g., "override was legitimate" or "escalation ACCEPTED as overruled" → incorrectly counted as prevented bugs). Now requires bug-contextualizing anchor words.
     3. `irrelevant`: fallback for anything matching neither — these are printed to stdout as "AMBIGUOUS: project=X gate=Y — first 100 chars of resolution" so a human can manually `mark-veto` or `mark-fp` them afterward
   - `learning_id` = 0 (sentinel for escalation-sourced records without a DB-matched learning)
   - `INSERT OR IGNORE` on unique constraint `(learning_id, project, gate)` for idempotency

5. **`cmd_list_learnings(db, limit=20, project=None)`** — added per UI critique on PLAN escalation. `mark-veto`/`mark-fp` both require a numeric `learning_id` but the plan originally provided no discovery path. This command prints up to `limit` recent learnings with columns: `id`, `project`, `gate`, and a truncated 80-char snippet of learning text. Optional `--project <name>` filter for scoping. The user pipes to `grep` or scrolls to find the relevant `id` for the next `mark-veto`/`mark-fp` call. Alias: `list-learnings`.

6. **Dispatcher update** — wire the five new subcommands into `main()`, update module docstring.

7. **Test** — `python3 -c "import ast; ast.parse(open('build_memory.py').read())"`, then run each new command manually (see Test Strategy below).

## File Layout
- `build_memory.py` — sole modified file (currently 534 lines, est. +130 lines → ~664)

## Function Map
**`build_memory.py`**
- Modified: `SCHEMA` (string constant) — append `recall_outcomes` table DDL
- New: `cmd_recall_stats(db, top_n=10)` — display outcome rankings
- New: `cmd_list_learnings(db, limit=20, project=None)` — enumerate learnings with id/project/gate/snippet so users can find IDs for mark-veto/mark-fp
- New: `cmd_mark_outcome(db, learning_id, project, gate, outcome, notes='')` — insert/replace one record
- New: `cmd_backfill_recall(db)` — classify and bulk-insert from session_state.json escalation history (with tightened prevented_bug regex)
- Modified: `main()` — add five new elif branches + updated docstring

## Security
- All SQL uses parameterized queries (`?` placeholders) — no string interpolation into SQL
- `learning_id` cast to `int()` before use; ValueError on non-integer input is caught and reported
- `gate` validated against `{'plan', 'implementation', 'tests', 'outcome'}` before insert
- `outcome` validated against `{'prevented_bug', 'false_positive', 'irrelevant'}` before insert
- `session_state.json` is read-only during backfill; no writes to it
- No network I/O introduced; no subprocess calls
- `build_memory.py` is a dev-time tool with no production trust boundary

## UI
N/A — CLI output only. All output formatted to fit 80 columns. `recall-stats` renders two fixed-width tables with headers.

## Guide
New commands added to module docstring and `main()`:

```
python3 build_memory.py recall-stats [N]                         # top/bottom N by outcome (default 10)
python3 build_memory.py list-learnings [N] [--project <name>]    # enumerate recent learnings with id/text snippet
python3 build_memory.py mark-veto <id> <proj> <gate>             # record prevented_bug outcome
python3 build_memory.py mark-fp   <id> <proj> <gate>             # record false_positive outcome
python3 build_memory.py backfill-recall                          # seed from session_state.json history
```

**Discovery workflow** (per UI critique):
```
$ python3 build_memory.py list-learnings 10 --project naval-scribe
  id   project          gate     snippet
  42   naval-scribe     outcome  KEEP: createDocumentFragment batch for lists >50 items...
  41   naval-scribe     tests    IMPROVE: CSP sha256 hashes when unsafe-inline absent...
$ python3 build_memory.py mark-fp 41 naval-scribe tests
```

## Edge Cases
- `recall_outcomes` references `learning_id = 0` for escalation-sourced records that don't have a matched DB row — stats query uses LEFT JOIN and shows "(escalation record)" for missing text
- `backfill-recall` is idempotent: unique constraint `(learning_id, project, gate)` with `INSERT OR IGNORE` prevents duplicates on repeated runs
- Ambiguous resolutions (match neither false_positive nor prevented_bug regex) → classified as `irrelevant` and printed to stdout so human can manually correct via `mark-veto`/`mark-fp`
- All regex patterns use `re.IGNORECASE` and `re.search` (not `str.contains`) to tolerate varied casing and surrounding text
- `session_state.json` absent or malformed: print clear error, exit 1; do not corrupt DB
- `learning_id` not found in `learnings` table: warn but still insert (learning may have been re-imported with new rowid)
- Empty `council_escalations_resolved`: print "0 escalation records to backfill" and exit cleanly

## Test Strategy
1. `python3 -c "import ast; ast.parse(open('build_memory.py').read())"` — syntax clean
2. `python3 build_memory.py import` — existing import still works, schema migration non-destructive
3. `python3 build_memory.py backfill-recall` — runs without error, prints count of rows inserted
4. `python3 build_memory.py recall-stats 5` — produces formatted table with ≥1 row (backfill populated it)
5. `python3 build_memory.py list-learnings 10` — prints id/project/gate/snippet table (NEW test per UI critique)
6. `python3 build_memory.py list-learnings 5 --project naval-scribe` — filter works (NEW test)
7. `python3 build_memory.py mark-veto 1 infra-memory-feedback plan` — inserts row; re-run `recall-stats` shows it
8. `python3 build_memory.py mark-fp 1 infra-memory-feedback plan` — `INSERT OR REPLACE` updates the row
9. Run `backfill-recall` twice — idempotency: same count reported, no duplicate rows
10. **Regex smoke test** (NEW per BUGS critique): `backfill-recall` dry-run mode (or inspection of classifier output) confirms the tightened `prevented_bug` regex does NOT match the resolution text of overridden escalations (e.g., commits 10bd394, e634ccd resolutions contain "override" + "legitimate" but should classify as `false_positive` or `irrelevant`, not `prevented_bug`).
