# Plan: fix-council-bugs-hallucination

## Goal
Add a council.py enforcement rule that auto-downgrades BUGS OBJECT verdicts whose cited evidence doesn't match actual file contents. Closes off the hallucination-loop pattern observed on Letter Status Tracker (rounds 7-9) and Template Letter Library (rounds 1-3) where cron kept objecting with fabricated "symbol X is undefined at file:line" claims pointing at lines where the symbol is actually defined.

## Why this matters

Current enforcement rules (shipped in fix-council-enforcement 2026-04-22) successfully catch:
1. LESSONS VETOs missing `precondition_evidence` → auto-downgrade (5 live production catches to date)
2. Goalpost-move OBJECTs with >0.35 keyword overlap vs priors → auto-downgrade
3. Parse-failure phantom OBJECTs → retry once with stricter JSON

These three rules solved the costly false-positive patterns from the fix-council-enforcement saga. But a new pattern emerged on naval-scribe tocks:

- **LST round 7**: BUGS claimed function `cycleDraftStatus` exists — actual function is `setDraftStatus`
- **LST round 8**: BUGS cited evidence string `substr(2, 9)` — actual code uses `.slice(2, 10)`
- **LST round 9**: BUGS claimed `F.id` and `F.status` in `getFullState` — neither reference exists in the file
- **Template Lib rounds 1-3**: BUGS claimed `byDirectionChk`, `actingChk`, `restoreParties` are undefined — all three defined at specific lines (2332, 2333, 2399); the 3rd attempt's evidence literally cited those definition lines

The goalpost-move rule doesn't fire on these because the citation strings vary slightly between rounds (different line numbers, slightly different wording) even though the underlying claim is identical. Each round reads as a "new" objection by the keyword-overlap check.

The cost of this loop: **6 real fixes + 3 hallucinations on LST; 0 real fixes + 3 hallucinations on Template Lib**. Both tocks ultimately shipped via retroactive 4-gate stamps. Preventing the hallucinations at the enforcement layer saves those stamp cycles.

## Scope

**In scope** — single new helper function in `council.py` plus integration in `main()`:
1. `detect_bugs_hallucination(verdict, project) -> bool` that verifies the claimed "undefined/missing symbol" matches actual file contents
2. Call from `main()` after `run_gate` and after the existing `enforce_lessons_precondition` + `check_goalpost_moves` passes
3. Unit tests + historical fixture replay

**Out of scope**:
- AST analysis or language-aware parsing (regex + grep is enough for the patterns observed)
- LLM-based claim verification
- Extending to other angles (UI, SECURITY, GUIDE) — those false-positive patterns differ and need their own rules
- Changing existing enforcement rules or their thresholds
- New `Verdict` fields (reuse existing `reason`, `required_fix`, `evidence`)

## Approach

### Subtask 1 — detect_bugs_hallucination helper

New function in `council.py`, called after the existing enforcement passes:

```python
# Regex patterns used to detect "X is undefined" style claims
_HALLUCINATION_CLAIM_RE = re.compile(
    r"\b(undefined|undeclared|not\s+defined|does\s+not\s+exist|missing)\b",
    re.IGNORECASE,
)
# Pull symbol names out of required_fix prose like "Define `X`", "Declare `foo`",
# "implement `bar` function". Also catches backtick-quoted identifiers anywhere.
_SYMBOL_FROM_FIX_RE = re.compile(r"`([a-zA-Z_][a-zA-Z0-9_]{2,})`")
# Match file:line refs in evidence: "index.html:2332", "build_memory.py:42"
_FILE_REF_RE = re.compile(r"([\w\-/.]+\.\w+):(\d+)(?:[-,]\d+)?")

def detect_bugs_hallucination(verdict, project):
    """Return True if a BUGS OBJECT verdict appears to cite nonexistent symbols.

    Only applies when reason uses 'undefined/undeclared/missing' phrasing
    AND required_fix/evidence reference specific symbol names. If those
    symbols ARE present in the referenced file(s), the claim is hallucinated.
    """
    if verdict.angle != "bugs" or verdict.verdict != "OBJECT":
        return False
    if not _HALLUCINATION_CLAIM_RE.search(verdict.reason or ""):
        return False
    # Collect symbols to check from required_fix backtick-quoted tokens
    fix_text = (verdict.required_fix or "") + " " + (verdict.reason or "")
    claimed_symbols = set(_SYMBOL_FROM_FIX_RE.findall(fix_text))
    if not claimed_symbols:
        return False  # No specific symbols to verify → don't downgrade
    # Collect files from evidence; fall back to common project file paths
    evidence = verdict.evidence or ""
    files = [m.group(1) for m in _FILE_REF_RE.finditer(evidence)]
    if not files:
        # Try common project files
        proj_dir = REPO_ROOT / project
        for candidate in ("index.html", "benchmark.py", "build_memory.py"):
            if (proj_dir / candidate).exists():
                files.append(str(proj_dir / candidate))
            elif (REPO_ROOT / candidate).exists():
                files.append(str(REPO_ROOT / candidate))
    if not files:
        return False
    # For each symbol, if it's found in any of the cited files → claim is wrong
    for file_path in files:
        # Resolve relative paths against REPO_ROOT if not absolute
        path_obj = Path(file_path) if os.path.isabs(file_path) else (REPO_ROOT / file_path)
        try:
            resolved = path_obj.resolve()
            resolved.relative_to(REPO_ROOT)  # containment safety
            content = resolved.read_text(encoding="utf-8", errors="replace")
        except (FileNotFoundError, ValueError):
            continue
        found_here = [s for s in claimed_symbols if re.search(r"\b" + re.escape(s) + r"\b", content)]
        if found_here:
            # At least one "undefined" symbol is actually defined here → hallucination
            return True
    return False
```

### Subtask 2 — Integrate in main()

Call after `check_goalpost_moves`:

```python
verdicts = run_gate(...)
verdicts = enforce_lessons_precondition(verdicts)
verdicts = check_goalpost_moves(args.project, verdicts)
# Patch 4: detect BUGS hallucinations
for v in verdicts:
    if detect_bugs_hallucination(v, args.project):
        print(f"[council] BUGS auto-downgraded (hallucinated symbol) — verified definition exists in cited files")
        v.verdict = "APPROVE"
        v.severity = "advisory"
        v.reason = f"[AUTO-DOWNGRADED: hallucinated symbol claim, symbols present in cited files] {v.reason}"
```

### Subtask 3 — Unit tests

Add to `experiments/fix-council-enforcement/test_enforcement.py` (extend existing suite rather than new file):

```python
class TestBugsHallucination(unittest.TestCase):
    def test_downgrades_when_symbol_defined_in_cited_file(self):
        # Create a synthetic project dir with a file that defines `myFunc`
        # Build a BUGS verdict claiming `myFunc` is undefined
        # Assert verdict gets downgraded
        ...
    def test_preserves_when_symbol_truly_missing(self):
        # File does NOT contain `myFunc`
        # Assert verdict preserved
        ...
    def test_only_applies_to_bugs_angle(self):
        # Same text but angle=security → preserved
        ...
    def test_only_applies_to_object_verdict(self):
        # APPROVE verdict with similar text → preserved
        ...
    def test_requires_undefined_phrasing(self):
        # Objection about "too broad regex" (no undefined/missing keyword) → preserved
        ...
    def test_requires_at_least_one_symbol_citation(self):
        # "Something is missing" with no backtick-quoted symbol → preserved (too vague)
        ...
```

### Subtask 4 — Historical fixture replay

Add 4 historical cases to `test_enforcement.py`:
1. **LST round 9** — BUGS claims `F.id`/`F.status` in `getFullState`; actual file has no such refs → should NOT downgrade (symbols truly absent)
2. **Template Lib round 1** — BUGS claims `byDirectionChk`/`actingChk`/`restoreParties` undefined in index.html:1900-1904; actual file has all three at lines 2332/2333/2399 → SHOULD downgrade
3. **LST round 7** — BUGS claims function `cycleDraftStatus` exists; actual function is `setDraftStatus` — ambiguous case since `cycleDraftStatus` is legitimately absent → don't downgrade, let human review
4. **infra-memory-feedback round 3 (legitimate BUGS)** — real table-overflow fix needed; claim is not "undefined symbol" → preserved

### Subtask 5 — changes.md post-implementation

Document what shipped and which behaviors changed, plus the 4 fixture outcomes.

## File Layout

| File | Action | Lines |
|------|--------|-------|
| `council.py` | MODIFY — add helper + main() call | +35 |
| `experiments/fix-council-enforcement/test_enforcement.py` | MODIFY — add TestBugsHallucination class + 4 fixture tests | +80 |
| `experiments/fix-council-bugs-hallucination/plan.md` | CREATE (this file) | 180 |
| `experiments/fix-council-bugs-hallucination/changes.md` | CREATE post-implementation | ~30 |
| `learnings.md` | MODIFY — append new enforcement rule under the existing council-enforcement section | +6 |

## Function Map

**`council.py`**
- `_HALLUCINATION_CLAIM_RE` (new module constant) — regex matching "undefined/undeclared/missing" language
- `_SYMBOL_FROM_FIX_RE` (new module constant) — regex extracting backtick-quoted identifiers
- `_FILE_REF_RE` (new module constant) — regex extracting file:line references from evidence
- `detect_bugs_hallucination(verdict, project) -> bool` (new) — pure function, returns True iff the claim is hallucinated
- `main()` — add one loop after `check_goalpost_moves` to apply the check

No other functions modified. `Verdict` dataclass unchanged.

## Security

- New function only READS files, never writes
- Files resolved against `REPO_ROOT` via `path.resolve().relative_to(REPO_ROOT)` — path containment same as existing verifiers
- No new network calls, no new external deps
- Internal orchestrator tool per established pattern

## UI

N/A — internal orchestrator. Output is a stderr log line when a downgrade fires:
`[council] BUGS auto-downgraded (hallucinated symbol) — verified definition exists in cited files`

## Guide

- `[council]` log prefix matches existing enforcement rule messages (parse-retry, LESSONS precondition, goalpost)
- changes.md documents how to test manually and what behaviors changed
- learnings.md gets a new bullet under the existing "Council enforcement rules are now LIVE in code" section

## Edge Cases

- **BUGS objection references a symbol that exists but is deprecated / stubbed** — low risk; our pattern checks any presence via `\b{symbol}\b` boundary match, so e.g. `# TODO: remove` commented-out references would match. Acceptable false negative; human review catches if needed.
- **Symbol name is a common word** (e.g., "id" or "value") — backtick-quoted identifiers need 3+ characters in the regex (`[a-zA-Z0-9_]{2,}`), which filters out most noise but not all. Could tighten to 4+ later if false positives appear.
- **File path contains `..`** — `path.resolve().relative_to(REPO_ROOT)` raises `ValueError` and we skip that file. No escape surface.
- **File doesn't exist** — caught via `FileNotFoundError`, skipped quietly.
- **Non-UTF-8 file** — `errors="replace"` prevents crashes; symbol matching may still work on the replaced content.
- **Multiple files in evidence, symbol found in one but missing in another** — we downgrade if ANY cited file contains the claimed symbol. That matches the intent: if BUGS points at multiple locations and any one of them disproves the claim, the claim is wrong.
- **Legitimate "X is undefined" on a symbol that IS truly missing from the file** — preserved. The rule doesn't suppress real bugs; it only suppresses claims contradicted by grep.

## Test Strategy

- `python3 -m py_compile council.py` — syntax
- `python3 experiments/fix-council-enforcement/test_enforcement.py` — unit tests (existing 17 + 6 new + 4 fixtures = 27 total)
- **Live regression check**: after deploy, manually run `python3 council.py --gate implementation --project naval-scribe --context naval-scribe/index.html --goal "Template Library live verification"` → confirm no BUGS OBJECT on byDirectionChk/actingChk/restoreParties
- **Fixture replay**: the 4 historical cases should all behave as documented in Subtask 4
- **Non-regression on real bugs**: the 3 legitimate BUGS that caught real issues on Letter Status Tracker (id-not-found guard, Date.now collision, saveAddr rethrow) must still OBJECT — verify by feeding their original escalation reasons through the new check
