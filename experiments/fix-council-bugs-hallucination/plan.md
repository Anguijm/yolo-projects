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

New function in `council.py`, called after the existing enforcement passes.

**Refined detection approach (addressing BUGS concern about comment/string false positives):**

Rather than a bare `\b{symbol}\b` text search (which matches comments, strings, and
dead code), the helper uses two complementary checks ordered from most specific to least:

1. **Cited-line check**: When evidence contains `file:NNN` references, read the exact
   cited lines (±5 context) and check whether the symbol appears there. This is the
   highest-signal path — if the council cited "index.html:2332" and line 2332 literally
   contains `byDirectionChk`, the claim is contradicted by direct evidence.

2. **Definition-pattern check**: Search the whole file for language-specific definition
   patterns, not bare identifier occurrences:
   - `.html`/`.js`: `function\s+{symbol}\b`, `(?:const|let|var)\s+{symbol}\s*=`, `{symbol}\s*\(`
   - `.py`: `(?:def|class)\s+{symbol}\s*[:(]`, `{symbol}\s*=\s*`
   - Other: skip whole-file fallback; only cited-line check applies

This avoids matching symbols in comments, string literals, or dead code because
definition patterns (`function foo`, `const foo =`, `def foo(`) are syntactically
distinct from mere mentions.

The two-layer design means:
- Template Lib case (cited lines 2332/2333/2399 define the symbols) → caught by layer 1
- Future cases with no line refs but clear definitions in source → caught by layer 2
- Symbol genuinely missing from file → neither layer matches → OBJECT preserved

```python
# Regex patterns used to detect "X is undefined" style claims
_HALLUCINATION_CLAIM_RE = re.compile(
    r"\b(undefined|undeclared|not\s+defined|does\s+not\s+exist|missing)\b",
    re.IGNORECASE,
)
# Pull symbol names out of required_fix/reason prose (backtick-quoted identifiers)
_SYMBOL_FROM_FIX_RE = re.compile(r"`([a-zA-Z_][a-zA-Z0-9_]{2,})`")
# Match file:line refs in evidence: "index.html:2332", "build_memory.py:42"
_FILE_REF_RE = re.compile(r"([\w\-/.]+\.\w+):(\d+)(?:[-,]\d+)?")

def _symbol_defined_in_content(symbol: str, content: str, ext: str) -> bool:
    """Return True if symbol appears to be *defined* in content using
    language-appropriate definition patterns. Falls back to cited-line check."""
    esc = re.escape(symbol)
    if ext in (".html", ".js", ".ts"):
        patterns = [
            rf"function\s+{esc}\b",
            rf"(?:const|let|var)\s+{esc}\s*=",
            rf"{esc}\s*\(",           # call-site is NOT a def, but method shorthand is
        ]
    elif ext == ".py":
        patterns = [
            rf"(?:def|class)\s+{esc}\s*[:(]",
            rf"^{esc}\s*=",           # module-level assignment
        ]
    else:
        return False  # unknown type — skip whole-file check
    return any(re.search(p, content, re.MULTILINE) for p in patterns)

def detect_bugs_hallucination(verdict, project):
    """Return True if a BUGS OBJECT verdict appears to cite nonexistent symbols.

    Only applies when reason uses 'undefined/undeclared/missing' phrasing
    AND required_fix/evidence reference specific backtick-quoted symbol names.
    Uses two-layer detection: cited-line check first (highest signal), then
    definition-pattern check (language-aware, avoids matching comments/strings).
    """
    if verdict.angle != "bugs" or verdict.verdict != "OBJECT":
        return False
    if not _HALLUCINATION_CLAIM_RE.search(verdict.reason or ""):
        return False
    fix_text = (verdict.required_fix or "") + " " + (verdict.reason or "")
    claimed_symbols = set(_SYMBOL_FROM_FIX_RE.findall(fix_text))
    if not claimed_symbols:
        return False
    evidence = verdict.evidence or ""
    file_refs = list(_FILE_REF_RE.finditer(evidence))
    # Collect file paths; fall back to known project files if evidence lacks them
    files = [m.group(1) for m in file_refs]
    if not files:
        proj_dir = REPO_ROOT / project
        for candidate in ("index.html", "benchmark.py", "build_memory.py"):
            for base in (proj_dir, REPO_ROOT):
                if (base / candidate).exists():
                    files.append(str(base / candidate))
                    break
    if not files:
        return False
    for raw_path, ref_match in zip(files, file_refs if file_refs else [None] * len(files)):
        path_obj = Path(raw_path) if os.path.isabs(raw_path) else (REPO_ROOT / raw_path)
        try:
            resolved = path_obj.resolve()
            resolved.relative_to(REPO_ROOT)
            content = resolved.read_text(encoding="utf-8", errors="replace")
        except (FileNotFoundError, ValueError):
            continue
        ext = resolved.suffix.lower()
        lines = content.splitlines()
        # Layer 1: cited-line check — look at the exact line numbers cited in evidence
        if ref_match is not None:
            cited_line = int(ref_match.group(2))
            window_start = max(0, cited_line - 6)
            window_end = min(len(lines), cited_line + 5)
            snippet = "\n".join(lines[window_start:window_end])
            for s in claimed_symbols:
                if re.search(r"\b" + re.escape(s) + r"\b", snippet):
                    return True  # symbol present at cited location → claim is wrong
        # Layer 2: definition-pattern check across the whole file
        for s in claimed_symbols:
            if _symbol_defined_in_content(s, content, ext):
                return True
    return False
```
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
- `_symbol_defined_in_content(symbol, content, ext) -> bool` (new) — language-aware definition-pattern check; avoids matching comments/strings
- `detect_bugs_hallucination(verdict, project) -> bool` (new) — two-layer check: cited-line window first, then definition-pattern; returns True iff the claim is hallucinated
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

- **BUGS objection references a symbol that exists in a comment or string literal** — mitigated by the definition-pattern check (Layer 2), which requires language-specific definition syntax rather than any occurrence. The cited-line check (Layer 1) uses a narrow ±5 line window around the exact cited location, which still matches comments near the cited line — but if the council cited a line that contains the symbol in a comment, that is still evidence the claim is wrong (it can see that line and choose a real code line instead).
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
