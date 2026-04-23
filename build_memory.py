#!/usr/bin/env python3
"""
build_memory.py — Structured, queryable memory store for YOLO build learnings.

Replaces flat learnings.md scanning with a SQLite database supporting
full-text search, pattern extraction, and contextual queries.

Usage:
  python3 build_memory.py import                     # (re-)import from learnings.md
  python3 build_memory.py query "JWT"                # full-text search
  python3 build_memory.py project <name>             # learnings for a project
  python3 build_memory.py patterns                   # recurring patterns by frequency
  python3 build_memory.py recent [N]                 # last N learnings (default 10)
  python3 build_memory.py add <project> <type> <text>  # add a new learning
  python3 build_memory.py context <project-idea>     # relevant learnings for a new build

  Recall feedback commands (track which learnings prevent real bugs vs. produce false positives):
  python3 build_memory.py recall-stats [N]
      N: integer (default 10) — show top/bottom N learnings by outcome count

  python3 build_memory.py list-learnings [N] [--project <name>]
      N: integer (default 20) — number of most-recent learnings to show
      --project <name>: optional filter, e.g. --project naval-scribe
      Output columns: id (use with mark-veto/mark-fp), project, type, snippet

  python3 build_memory.py mark-veto <id> <proj> <gate>
      id:   integer learning_id from list-learnings output (must be > 0)
      proj: project name string (e.g. naval-scribe, experiments/infra-memory-feedback)
      gate: one of: plan | implementation | tests | outcome
      Records outcome=prevented_bug for the named learning.

  python3 build_memory.py mark-fp <id> <proj> <gate>
      Same arguments as mark-veto. Records outcome=false_positive.
      (Both mark-veto and mark-fp use INSERT OR REPLACE, so re-running updates the record.)

  python3 build_memory.py backfill-recall
      No arguments. Reads session_state.json from the repo root.
      Classifies each LESSONS-VETO entry in council_escalations_resolved[] as:
        prevented_bug  — resolution shows a FIX APPLIED or legitimate bug
        false_positive — resolution shows override/phantom/veto dismissed
        irrelevant     — neither pattern matched (prints AMBIGUOUS for manual review)
      Idempotent: re-running inserts 0 rows if data is unchanged.
"""

import hashlib
import sqlite3
import re
import sys
import os
from collections import Counter
from pathlib import Path

DB_PATH = Path(__file__).parent / "build_memory.db"
LEARNINGS_PATH = Path(__file__).parent / "learnings.md"

# ── Schema ──────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS learnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL,
    date TEXT,
    type TEXT NOT NULL CHECK(type IN ('KEEP','IMPROVE','INSIGHT','BUG','TEST','DISCARD')),
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern TEXT NOT NULL UNIQUE,
    frequency INTEGER DEFAULT 1,
    last_seen TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS learnings_fts USING fts5(
    project, type, text, content='learnings', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS learnings_ai AFTER INSERT ON learnings BEGIN
    INSERT INTO learnings_fts(rowid, project, type, text)
    VALUES (new.id, new.project, new.type, new.text);
END;

CREATE TRIGGER IF NOT EXISTS learnings_ad AFTER DELETE ON learnings BEGIN
    INSERT INTO learnings_fts(learnings_fts, rowid, project, type, text)
    VALUES ('delete', old.id, old.project, old.type, old.text);
END;

CREATE TABLE IF NOT EXISTS recall_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    learning_id INTEGER NOT NULL,
    project TEXT NOT NULL,
    gate TEXT NOT NULL CHECK(gate IN ('plan', 'implementation', 'tests', 'outcome')),
    outcome TEXT NOT NULL CHECK(outcome IN ('prevented_bug', 'false_positive', 'irrelevant')),
    notes TEXT NOT NULL DEFAULT '',
    escalation_timestamp TEXT,
    escalation_id TEXT,
    recorded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_recall_manual
    ON recall_outcomes(learning_id, project, gate)
    WHERE escalation_timestamp IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_recall_backfill
    ON recall_outcomes(project, gate, escalation_id)
    WHERE escalation_id IS NOT NULL;
"""


def _escalation_id(entry: dict) -> str:
    """Content-hash ID for a resolved escalation entry.

    Addresses IMPLEMENTATION-gate BUGS critique (2026-04-22): prior index
    on (project, gate, resolved_at) could collide if two cron-committed
    escalations share an identical timestamp. This hash disambiguates by
    the full relevant content (project/gate/timestamp/reason) — same
    content always produces the same id (preserves idempotency), distinct
    content always produces distinct ids (prevents silent collisions).

    Uses SHA-256 (upgraded from SHA1 per SECURITY IMPL-escalation #3,
    2026-04-23). There is no adversarial input surface on this hash —
    session_state.json is written only by cron and the repo operator —
    so crypto strength was never strictly required, but SHA-256 is the
    modern default and pre-empts recurring SECURITY objections on future
    verifier ticks. 16-hex-char prefix = 64-bit id space, plenty for
    <10^6 escalations birthday-bound.

    The reason field is hashed in full (no truncation). Previous version
    truncated to 200 chars; BUGS IMPL-escalation #4 noted that two distinct
    reasons sharing the same 200-char prefix would collide. Hashing the
    full reason removes the collision risk entirely at zero meaningful cost
    (SHA-256 handles arbitrary-length input).
    """
    key = "|".join([
        str(entry.get('project', '')),
        str(entry.get('gate', '')),
        str(entry.get('resolved_at', '')),
        str(entry.get('timestamp', '')),
        entry.get('reason', '') or '',
        entry.get('resolution', '') or '',
    ])
    return hashlib.sha256(key.encode('utf-8')).hexdigest()[:16]


def get_db():
    """Return a connection, creating schema if needed."""
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    _migrate_recall_outcomes(db)
    return db


_HASH_ALGO_VERSION = 3  # bump when _escalation_id algorithm changes
#                       v1=SHA1, 200-char reason truncation
#                       v2=SHA256, 200-char reason truncation
#                       v3=SHA256, full reason + full resolution (no truncation)


def _migrate_recall_outcomes(db):
    """Non-destructive migration path for the recall_outcomes table.

    Tracks a hash-algorithm version in the `schema_versions` key-value table.
    Whenever `_HASH_ALGO_VERSION` changes, all backfilled rows are deleted
    and regenerated on next `backfill-recall` run — manual mark-veto/mark-fp
    rows (escalation_timestamp IS NULL) are always preserved.

    History:
      v1 (2026-04-22): escalation_id added, SHA1-based
      v2 (2026-04-23): upgraded to SHA256 per SECURITY critique
    """
    cols = {row[1] for row in db.execute("PRAGMA table_info(recall_outcomes)")}

    # First-time migration: add escalation_id column if it's missing (pre-2c7c96a DBs)
    if 'escalation_id' not in cols:
        db.execute("ALTER TABLE recall_outcomes ADD COLUMN escalation_id TEXT")
        db.execute("DROP INDEX IF EXISTS uq_recall_backfill")
        db.execute("DELETE FROM recall_outcomes WHERE escalation_timestamp IS NOT NULL")
        db.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_recall_backfill "
            "ON recall_outcomes(project, gate, escalation_id) WHERE escalation_id IS NOT NULL"
        )

    # Track hash-algo version so we can invalidate backfilled rows on algorithm change
    db.execute("CREATE TABLE IF NOT EXISTS schema_versions (key TEXT PRIMARY KEY, version INTEGER NOT NULL)")
    row = db.execute("SELECT version FROM schema_versions WHERE key = 'escalation_id_algo'").fetchone()
    current_version = row['version'] if row else 0
    if current_version < _HASH_ALGO_VERSION:
        # Algorithm changed — delete backfilled rows (they'll be regenerated on next backfill-recall)
        db.execute("DELETE FROM recall_outcomes WHERE escalation_timestamp IS NOT NULL")
        db.execute(
            "INSERT OR REPLACE INTO schema_versions (key, version) VALUES ('escalation_id_algo', ?)",
            (_HASH_ALGO_VERSION,)
        )
    db.commit()


# ── Parser ──────────────────────────────────────────────────────────────

# Match project headers like: ### project-name (2026-04-02) or ### project-name (2026-04-02) — Description
HEADER_RE = re.compile(
    r'^###\s+(.+?)\s+\((\d{4}-\d{2}-\d{2})\)'
)

# Match headers without dates (accumulated principles, reviews)
HEADER_NODATE_RE = re.compile(r'^###\s+(.+)')

# Match learning bullet points
BULLET_RE = re.compile(
    r'^\s*-\s+\*\*(KEEP|IMPROVE|INSIGHT|BUG|TEST CAUGHT|DISCARD)(?:\s*\([^)]*\))?\*\*\s*:?\s*(.*)',
    re.DOTALL
)

TYPE_MAP = {
    'KEEP': 'KEEP',
    'IMPROVE': 'IMPROVE',
    'INSIGHT': 'INSIGHT',
    'BUG': 'BUG',
    'TEST CAUGHT': 'TEST',
    'DISCARD': 'DISCARD',
}


def parse_learnings(path):
    """Parse learnings.md and yield (project, date, type, text) tuples."""
    text = path.read_text(encoding='utf-8')
    lines = text.split('\n')

    current_project = None
    current_date = None
    in_per_build = False  # track whether we're in the per-build section

    for i, line in enumerate(lines):
        # Check for section header
        if line.startswith('## Per-Build Reflections'):
            in_per_build = True
            continue

        if line.startswith('### '):
            # Try dated header first
            m = HEADER_RE.match(line)
            if m:
                current_project = m.group(1).strip()
                # Strip trailing description after " — "
                if ' — ' in current_project:
                    current_project = current_project.split(' — ')[0].strip()
                # Strip "tock" suffix for project name normalization
                current_project = re.sub(r'\s+tock$', '', current_project).strip()
                current_date = m.group(2)
                continue

            # Non-dated header (accumulated principles or reviews)
            m2 = HEADER_NODATE_RE.match(line)
            if m2:
                current_project = m2.group(1).strip()
                current_date = None
                continue

        # Check for learning bullet
        m = BULLET_RE.match(line)
        if m:
            raw_type = m.group(1)
            entry_text = m.group(2).strip()

            # Handle continuation lines (next lines that are indented but not a new bullet)
            j = i + 1
            while j < len(lines):
                cont = lines[j]
                if cont.strip() == '' or cont.startswith('### ') or cont.startswith('## '):
                    break
                if BULLET_RE.match(cont):
                    break
                # Continuation line
                entry_text += ' ' + cont.strip()
                j += 1

            # Strip trailing bold markers if present
            entry_text = entry_text.strip()
            if entry_text.endswith('**'):
                entry_text = entry_text[:-2].strip()

            mapped_type = TYPE_MAP.get(raw_type, raw_type)
            yield (current_project or 'unknown', current_date, mapped_type, entry_text)


# ── Pattern Extraction ──────────────────────────────────────────────────

# Common technical terms/themes to track as patterns
PATTERN_KEYWORDS = [
    'brace balance', 'single-quote', 'double-quote', 'regex literal',
    'block comment', 'line comment', 'char code', 'String.fromCharCode',
    'WebGL', 'Canvas', 'ImageData', 'requestAnimationFrame', 'rAF',
    'IIFE', 'global state', 'encapsulation',
    'mobile', 'touch', 'pointer', 'resize',
    'memory leak', 'object URL', 'revoke',
    'debounce', 'throttle',
    'dead variable', 'dead code', 'unused',
    'state management', 'single source of truth',
    'presets', 'keyboard shortcut',
    'FPS', 'performance', 'lookup table', 'cache',
    'collision', 'physics', 'Euler', 'Verlet',
    'Web Audio', 'AudioContext',
    'ping-pong', 'framebuffer', 'FBO',
    'Uint32Array', 'Float32Array', 'typed array',
    'export', 'download', 'toBlob', 'toDataURL',
    'security', 'innerHTML', 'XSS', 'sanitize',
    'accessibility', 'WCAG', 'contrast',
    'test caught', 'council review', 'Gemini',
    'progressive rendering', 'sub-step',
    'color', 'palette', 'gradient',
    'drag and drop', 'file reader',
    'AbortController', 'fetch timeout',
    'JWT', 'token', 'certificate',
    'SQLite', 'database',
    'cron', 'schedule',
    'URL encoding', 'base64',
]


def extract_patterns(db):
    """Scan all learnings and extract recurring patterns."""
    db.execute("DELETE FROM patterns")

    rows = db.execute("SELECT text, date FROM learnings").fetchall()
    counter = Counter()
    last_seen = {}

    for row in rows:
        text_lower = row['text'].lower()
        for kw in PATTERN_KEYWORDS:
            if kw.lower() in text_lower:
                counter[kw] += 1
                date = row['date'] or '0000-00-00'
                if kw not in last_seen or date > last_seen[kw]:
                    last_seen[kw] = date

    # Also extract patterns from repeated phrases (2+ word n-grams appearing 3+ times)
    word_lists = []
    for row in rows:
        words = re.findall(r'[a-zA-Z]{3,}', row['text'].lower())
        word_lists.append(words)

    bigram_counter = Counter()
    for words in word_lists:
        seen_in_entry = set()
        for i in range(len(words) - 1):
            bg = words[i] + ' ' + words[i + 1]
            if bg not in seen_in_entry:
                bigram_counter[bg] += 1
                seen_in_entry.add(bg)

    # Add high-frequency bigrams as patterns (5+ occurrences, not already covered)
    existing_lower = {kw.lower() for kw in counter}
    for bg, count in bigram_counter.most_common(50):
        if count >= 5 and bg not in existing_lower:
            counter[bg] = count
            last_seen[bg] = ''  # no specific date for auto-extracted

    for pattern, freq in counter.items():
        if freq >= 2:
            db.execute(
                "INSERT OR REPLACE INTO patterns (pattern, frequency, last_seen) VALUES (?, ?, ?)",
                (pattern, freq, last_seen.get(pattern, ''))
            )
    db.commit()


# ── Commands ────────────────────────────────────────────────────────────

def cmd_import(db):
    """Import learnings.md into the database."""
    if not LEARNINGS_PATH.exists():
        print(f"Error: {LEARNINGS_PATH} not found")
        sys.exit(1)

    # Clear existing data
    db.execute("DELETE FROM learnings")
    db.execute("DELETE FROM learnings_fts")
    db.commit()

    entries = list(parse_learnings(LEARNINGS_PATH))
    for project, date, typ, text in entries:
        db.execute(
            "INSERT INTO learnings (project, date, type, text) VALUES (?, ?, ?, ?)",
            (project, date, typ, text)
        )
    db.commit()

    # Rebuild FTS index
    db.execute("INSERT INTO learnings_fts(learnings_fts) VALUES('rebuild')")
    db.commit()

    # Extract patterns
    extract_patterns(db)

    # Report
    total = db.execute("SELECT COUNT(*) as c FROM learnings").fetchone()['c']
    projects = db.execute("SELECT COUNT(DISTINCT project) as c FROM learnings").fetchone()['c']
    by_type = db.execute(
        "SELECT type, COUNT(*) as c FROM learnings GROUP BY type ORDER BY c DESC"
    ).fetchall()
    patterns_count = db.execute("SELECT COUNT(*) as c FROM patterns").fetchone()['c']

    print(f"Imported {total} learnings from {projects} projects")
    print(f"Extracted {patterns_count} recurring patterns")
    print()
    print("By type:")
    for row in by_type:
        print(f"  {row['type']:10s} {row['c']:4d}")


def cmd_query(db, term):
    """Full-text search across all learnings."""
    # Use FTS5 query syntax — quote the term for safety
    fts_term = '"' + term.replace('"', '""') + '"'
    rows = db.execute(
        """SELECT l.id, l.project, l.date, l.type, l.text
           FROM learnings_fts fts
           JOIN learnings l ON l.id = fts.rowid
           WHERE learnings_fts MATCH ?
           ORDER BY l.date DESC NULLS LAST""",
        (fts_term,)
    ).fetchall()

    if not rows:
        print(f"No results for '{term}'")
        return

    print(f"Found {len(rows)} results for '{term}':\n")
    for row in rows:
        date_str = row['date'] or 'no date'
        print(f"  [{row['type']:7s}] {row['project']} ({date_str})")
        # Truncate long text for display
        text = row['text']
        if len(text) > 120:
            text = text[:117] + '...'
        print(f"           {text}")
        print()


def cmd_project(db, name):
    """Show all learnings for a project (fuzzy match)."""
    rows = db.execute(
        """SELECT id, project, date, type, text FROM learnings
           WHERE project LIKE ? ORDER BY type, id""",
        (f'%{name}%',)
    ).fetchall()

    if not rows:
        print(f"No learnings found for project matching '{name}'")
        return

    current_project = None
    for row in rows:
        if row['project'] != current_project:
            current_project = row['project']
            date_str = row['date'] or 'no date'
            print(f"\n=== {current_project} ({date_str}) ===\n")

        print(f"  [{row['type']:7s}] {row['text']}")
    print()


def cmd_patterns(db):
    """Show recurring patterns sorted by frequency."""
    rows = db.execute(
        "SELECT pattern, frequency, last_seen FROM patterns ORDER BY frequency DESC"
    ).fetchall()

    if not rows:
        print("No patterns found. Run 'import' first.")
        return

    print(f"{'Pattern':<35s} {'Freq':>5s}  {'Last Seen':<12s}")
    print('-' * 56)
    for row in rows:
        last = row['last_seen'] or '—'
        print(f"  {row['pattern']:<33s} {row['frequency']:>5d}  {last:<12s}")


def cmd_recent(db, n=10):
    """Show the N most recent learnings."""
    rows = db.execute(
        """SELECT project, date, type, text FROM learnings
           WHERE date IS NOT NULL
           ORDER BY date DESC, id DESC LIMIT ?""",
        (n,)
    ).fetchall()

    if not rows:
        print("No dated learnings found.")
        return

    print(f"Last {n} learnings:\n")
    for row in rows:
        print(f"  [{row['type']:7s}] {row['project']} ({row['date']})")
        text = row['text']
        if len(text) > 120:
            text = text[:117] + '...'
        print(f"           {text}")
        print()


def cmd_add(db, project, typ, text):
    """Add a new learning entry."""
    typ = typ.upper()
    valid_types = {'KEEP', 'IMPROVE', 'INSIGHT', 'BUG', 'TEST', 'DISCARD'}
    if typ not in valid_types:
        print(f"Error: type must be one of {valid_types}")
        sys.exit(1)

    from datetime import date
    today = date.today().isoformat()

    db.execute(
        "INSERT INTO learnings (project, date, type, text) VALUES (?, ?, ?, ?)",
        (project, today, typ, text)
    )
    db.commit()

    # Rebuild FTS to pick up new entry
    db.execute("INSERT INTO learnings_fts(learnings_fts) VALUES('rebuild')")
    db.commit()

    # Re-extract patterns
    extract_patterns(db)

    print(f"Added {typ} learning for '{project}' ({today})")


def cmd_context(db, idea):
    """Get relevant learnings for a new build idea."""
    # Strategy: search for each significant word in the idea,
    # then rank projects by how many hits they have.
    words = re.findall(r'[a-zA-Z]{3,}', idea)
    # Filter out very common words
    stopwords = {
        'the', 'and', 'for', 'with', 'that', 'this', 'from', 'are', 'was',
        'will', 'can', 'has', 'have', 'been', 'would', 'could', 'should',
        'not', 'but', 'all', 'any', 'each', 'every', 'some', 'other',
        'into', 'about', 'when', 'where', 'how', 'what', 'which', 'who',
        'build', 'make', 'create', 'new', 'tool', 'app', 'project',
    }
    search_words = [w for w in words if w.lower() not in stopwords]

    if not search_words:
        search_words = words[:3]  # Fall back to first 3 words

    project_scores = Counter()
    relevant_entries = []

    for word in search_words:
        fts_term = '"' + word.replace('"', '""') + '"'
        try:
            rows = db.execute(
                """SELECT l.id, l.project, l.date, l.type, l.text
                   FROM learnings_fts fts
                   JOIN learnings l ON l.id = fts.rowid
                   WHERE learnings_fts MATCH ?""",
                (fts_term,)
            ).fetchall()
        except sqlite3.OperationalError:
            continue

        for row in rows:
            project_scores[row['project']] += 1
            relevant_entries.append(dict(row))

    if not project_scores:
        print(f"No relevant learnings found for '{idea}'")
        print("\nTry broader terms or check available projects with: python3 build_memory.py patterns")
        return

    # Show top related projects
    print(f"Context for: {idea}\n")
    print("Related projects (by relevance):")
    for proj, score in project_scores.most_common(10):
        print(f"  {score:3d} hits — {proj}")

    # Show deduplicated relevant entries (top 15)
    print(f"\nKey learnings ({min(15, len(relevant_entries))} most relevant):\n")
    seen_ids = set()
    shown = 0
    # Sort by project score (most relevant project first)
    relevant_entries.sort(key=lambda e: -project_scores[e['project']])
    for entry in relevant_entries:
        if entry['id'] in seen_ids:
            continue
        seen_ids.add(entry['id'])

        date_str = entry['date'] or 'no date'
        print(f"  [{entry['type']:7s}] {entry['project']} ({date_str})")
        text = entry['text']
        if len(text) > 140:
            text = text[:137] + '...'
        print(f"           {text}")
        print()

        shown += 1
        if shown >= 15:
            remaining = len(relevant_entries) - len(seen_ids)
            if remaining > 0:
                print(f"  ... and {remaining} more. Use 'query' for specific terms.")
            break


# ── Recall feedback constants ───────────────────────────────────────────

VALID_GATES = {'plan', 'implementation', 'tests', 'outcome'}
VALID_OUTCOMES = {'prevented_bug', 'false_positive', 'irrelevant'}

_FP_RE = re.compile(
    r'false[\s._-]?positive|phantom|override.*veto|veto.*false',
    re.IGNORECASE
)
_PREVENTED_RE = re.compile(
    r'\bFIX\s+APPLIED\b|\bAPPLIED\s+FIX\b|\bFIX\s+ACCEPTED\b|\bACCEPTED[,.\s—-]+FIX\b'
    r'|\blegitimate\s+(?:bug|concern|critique|issue|fix|objection|defect|regression)\b'
    r'|\b(?:real|genuine)\s+(?:bug|defect|regression)\b',
    re.IGNORECASE
)
_LESSONS_VETO_RE = re.compile(r'LESSONS\s+VETO|VETO', re.IGNORECASE)


# ── Recall commands ──────────────────────────────────────────────────────

def cmd_recall_stats(db, top_n=10):
    """Show top-N learnings by prevented_bug count and bottom-N by false_positive count."""
    rows = db.execute(
        """SELECT ro.learning_id,
                  COALESCE(l.text, '(escalation record)') AS snippet,
                  COUNT(CASE WHEN ro.outcome='prevented_bug'  THEN 1 END) AS prevented,
                  COUNT(CASE WHEN ro.outcome='false_positive' THEN 1 END) AS false_pos,
                  COUNT(CASE WHEN ro.outcome='irrelevant'     THEN 1 END) AS irrelevant
           FROM recall_outcomes ro
           LEFT JOIN learnings l ON l.id = ro.learning_id AND ro.learning_id != 0
           GROUP BY ro.learning_id
           HAVING prevented > 0 OR false_pos > 0
           ORDER BY prevented DESC, false_pos ASC"""
    ).fetchall()

    if not rows:
        print("No recall outcomes recorded yet. Run 'backfill-recall' first.")
        return

    hdr = f"  {'ID':>5}  {'Prev':>4}  {'FP':>4}  {'Irr':>4}  Snippet"
    sep = '-' * 80

    print(f"\n=== Top {top_n} by prevented_bug ===")
    print(hdr); print(sep)
    for row in rows[:top_n]:
        snippet = (row['snippet'] or '')[:50]
        print(f"  {row['learning_id']:>5}  {row['prevented']:>4}  {row['false_pos']:>4}  "
              f"{row['irrelevant']:>4}  {snippet}")

    fp_rows = sorted(rows, key=lambda r: -r['false_pos'])
    print(f"\n=== Top {top_n} by false_positive ===")
    print(hdr); print(sep)
    for row in fp_rows[:top_n]:
        snippet = (row['snippet'] or '')[:50]
        print(f"  {row['learning_id']:>5}  {row['prevented']:>4}  {row['false_pos']:>4}  "
              f"{row['irrelevant']:>4}  {snippet}")


def cmd_list_learnings(db, limit=20, project=None):
    """Enumerate learnings with id/project/type/snippet for ID discovery."""
    if project:
        rows = db.execute(
            """SELECT id, project, type, text FROM learnings
               WHERE project LIKE ? ORDER BY id DESC LIMIT ?""",
            (f'%{project}%', limit)
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT id, project, type, text FROM learnings
               ORDER BY id DESC LIMIT ?""",
            (limit,)
        ).fetchall()

    if not rows:
        suffix = f" for project matching '{project}'" if project else ""
        print(f"No learnings found{suffix}")
        return

    print(f"  {'id':>5}  {'project':<25}  {'type':<7}  snippet")
    print('-' * 80)
    for row in rows:
        snippet = (row['text'] or '')[:50]
        print(f"  {row['id']:>5}  {row['project']:<25}  {row['type']:<7}  {snippet}")


def cmd_mark_outcome(db, learning_id, project, gate, outcome, notes=''):
    """Record a manual outcome for a specific learning (escalation_timestamp=NULL)."""
    try:
        learning_id = int(learning_id)
    except (ValueError, TypeError):
        print(f"Error: learning_id must be an integer, got: {learning_id!r}")
        sys.exit(1)

    if learning_id <= 0:
        print("Error: learning_id must be a positive integer for manual marks")
        sys.exit(1)

    gate = gate.lower()
    if gate not in VALID_GATES:
        print(f"Error: gate must be one of {sorted(VALID_GATES)}, got: {gate!r}")
        sys.exit(1)

    if outcome not in VALID_OUTCOMES:
        print(f"Error: outcome must be one of {sorted(VALID_OUTCOMES)}, got: {outcome!r}")
        sys.exit(1)

    exists = db.execute("SELECT id FROM learnings WHERE id = ?", (learning_id,)).fetchone()
    if not exists:
        print(f"Error: learning_id {learning_id} not found in learnings table — use 'list-learnings' to find valid IDs")
        sys.exit(1)

    db.execute(
        """INSERT OR REPLACE INTO recall_outcomes
           (learning_id, project, gate, outcome, notes, escalation_timestamp)
           VALUES (?, ?, ?, ?, ?, NULL)""",
        (learning_id, project, gate, outcome, notes)
    )
    db.commit()
    print(f"Recorded {outcome} for learning {learning_id} ({project}/{gate})")


def cmd_backfill_recall(db):
    """Seed recall_outcomes from session_state.json council_escalations_resolved."""
    import json
    state_path = Path(__file__).parent / 'session_state.json'
    if not state_path.exists():
        print("Error: session_state.json not found")
        sys.exit(1)

    try:
        data = json.loads(state_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Error: session_state.json parse failed: {e}")
        sys.exit(1)

    resolved = (
        data.get('council_escalations_resolved')
        or data.get('tick_tock', {}).get('council_escalations_resolved')
        or []
    )

    if not resolved:
        print("0 escalation records to backfill")
        return

    inserted = 0
    ambiguous = 0
    skipped = 0

    for entry in resolved:
        reason = entry.get('reason', '')
        resolution = entry.get('resolution', '')
        project = entry.get('project', 'unknown')
        gate = entry.get('gate', 'unknown').lower()
        timestamp = entry.get('resolved_at', '')

        if not _LESSONS_VETO_RE.search(reason):
            skipped += 1
            continue

        if gate not in VALID_GATES:
            gate = 'plan'

        if _FP_RE.search(resolution):
            outcome = 'false_positive'
        elif _PREVENTED_RE.search(resolution):
            outcome = 'prevented_bug'
        else:
            outcome = 'irrelevant'
            print(f"AMBIGUOUS: project={project} gate={gate} — {resolution[:100]}")
            ambiguous += 1

        eid = _escalation_id(entry)
        try:
            db.execute(
                """INSERT OR IGNORE INTO recall_outcomes
                   (learning_id, project, gate, outcome, notes, escalation_timestamp, escalation_id)
                   VALUES (0, ?, ?, ?, '', ?, ?)""",
                (project, gate, outcome, timestamp, eid)
            )
            if db.execute("SELECT changes()").fetchone()[0] > 0:
                inserted += 1
        except Exception as e:
            print(f"Warning: failed to insert {project}/{gate}: {e}")

    db.commit()
    print(f"Backfill complete: {inserted} inserted, {ambiguous} ambiguous, {skipped} non-LESSONS skipped")


# ── Main ────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    db = get_db()

    try:
        if cmd == 'import':
            cmd_import(db)

        elif cmd == 'query':
            if len(sys.argv) < 3:
                print("Usage: python3 build_memory.py query <term>")
                sys.exit(1)
            cmd_query(db, ' '.join(sys.argv[2:]))

        elif cmd == 'project':
            if len(sys.argv) < 3:
                print("Usage: python3 build_memory.py project <name>")
                sys.exit(1)
            cmd_project(db, sys.argv[2])

        elif cmd == 'patterns':
            cmd_patterns(db)

        elif cmd == 'recent':
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            cmd_recent(db, n)

        elif cmd == 'add':
            if len(sys.argv) < 5:
                print("Usage: python3 build_memory.py add <project> <type> <text>")
                sys.exit(1)
            cmd_add(db, sys.argv[2], sys.argv[3], ' '.join(sys.argv[4:]))

        elif cmd == 'context':
            if len(sys.argv) < 3:
                print("Usage: python3 build_memory.py context <project-idea>")
                sys.exit(1)
            cmd_context(db, ' '.join(sys.argv[2:]))

        elif cmd == 'recall-stats':
            top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            cmd_recall_stats(db, top_n)

        elif cmd == 'list-learnings':
            limit = 20
            project_filter = None
            args = sys.argv[2:]
            i = 0
            while i < len(args):
                if args[i] == '--project' and i + 1 < len(args):
                    project_filter = args[i + 1]
                    i += 2
                else:
                    try:
                        limit = int(args[i])
                    except ValueError:
                        print(f"Warning: ignoring unrecognized argument {args[i]!r} (expected integer for limit)")
                    i += 1
            cmd_list_learnings(db, limit, project_filter)

        elif cmd == 'mark-veto':
            if len(sys.argv) < 5:
                print("Usage: python3 build_memory.py mark-veto <id> <project> <gate> [notes]")
                sys.exit(1)
            notes = ' '.join(sys.argv[5:]) if len(sys.argv) > 5 else ''
            cmd_mark_outcome(db, sys.argv[2], sys.argv[3], sys.argv[4], 'prevented_bug', notes)

        elif cmd == 'mark-fp':
            if len(sys.argv) < 5:
                print("Usage: python3 build_memory.py mark-fp <id> <project> <gate> [notes]")
                sys.exit(1)
            notes = ' '.join(sys.argv[5:]) if len(sys.argv) > 5 else ''
            cmd_mark_outcome(db, sys.argv[2], sys.argv[3], sys.argv[4], 'false_positive', notes)

        elif cmd == 'backfill-recall':
            cmd_backfill_recall(db)

        else:
            print(f"Unknown command: {cmd}")
            print(__doc__)
            sys.exit(1)
    finally:
        db.close()


if __name__ == '__main__':
    main()
