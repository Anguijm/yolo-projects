# Council Escalation — experiments/infra-yolo-evals

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-21T13:05:55.279266+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The 'table-overflow' check in mobile_usability.py incorrectly flags valid responsive table implementations where 'overflow-x:auto' is applied to a parent wrapper element instead of directly to the <table>, leading to false positive warnings.
- **Required fix:** The 'table-overflow' check must be refined to detect if 'overflow-x:auto' is applied to the <table> element itself or to a direct parent/ancestor wrapper, rather than merely checking for its global presence or absence.
- **Evidence:** `mobile_usability.py check 4: "flags <table> without overflow-x:auto anywhere in the file"`

### SECURITY — OBJECT (high)
- **Reason:** The scripts accept an arbitrary file path via sys.argv[1] which, despite canonicalization with os.path.abspath, allows reading any file on the system accessible to the script's user if an attacker can control the input argument, leading to arbitrary file disclosure.
- **Required fix:** Implement strict path validation to ensure the input path is a child of an explicitly allowed, sandboxed directory (e.g., the project root or a temporary build directory), or use a more robust sandboxing mechanism to prevent reading arbitrary files.
- **Evidence:** `path = os.path.abspath(sys.argv[1])
    # ...
def read_html(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()`

### UI — APPROVE (low)
- **Reason:** All proposed evaluation lenses encourage best practices for user experience, including accessibility, responsiveness, feedback, and clear interaction patterns.

### GUIDE — APPROVE (low)
- **Reason:** All discoverability concerns from previous attempt have been addressed; comprehensive in-app help and documentation are provided.

### USEFULNESS — APPROVE (low)
- **Reason:** These advisory lenses provide practical, recurring utility for developers building YOLO projects, catching common oversights and prompting valuable polish.
- **Evidence:** `The portfolio hit rates demonstrate real-world catches like 'focus-ring' on all projects, 'table-overflow' regression, and correct 'cult_status' grading for markdown-deck. This indicates the heuristics are effective for the target single-file HTML projects. The tools address common development blind`

### COOL — APPROVE (low)
- **Reason:** Internal pipeline tools are explicitly exempt from the signature-move requirement per PLAN gate approval and the broadened goalpost rule.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

**RESOLVED 2026-04-22 by John (interactive session).**

### BUGS OBJECT — OVERRIDDEN (false positive)
The angle claimed the `table-overflow` check in `mobile_usability.py` false-flags valid responsive tables where `overflow-x:auto` is on a parent wrapper instead of the `<table>`. This is factually incorrect. Code at `mobile_usability.py:85-87`:
```python
has_table = bool(re.search(r'<table', text, re.IGNORECASE))
has_overflow_x = bool(re.search(r'overflow-x\s*:\s*auto', text))
if has_table and not has_overflow_x:
```
The `overflow-x:auto` check scans the whole file — a CSS rule on a wrapper selector counts. The portfolio hit-rate table in `changes.md` confirms this works correctly (naval-scribe genuinely has no overflow-x:auto anywhere → correctly caught; markdown-deck has overflow-x on a wrapper → correctly passed). The objection fails the lessons-reviewer protocol precondition check: the code does not match the described defect.

### SECURITY OBJECT — FIXED AT SOURCE
Rather than override (the precedent from infra-guardrails), the `sys.argv[1]` path input was hardened to repo-root containment in all three lens scripts:
```python
REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.realpath(sys.argv[1])
if not (path == REPO_ROOT or path.startswith(REPO_ROOT + os.sep)):
    print(f"ERROR: {path} is outside the repo root ({REPO_ROOT}); refusing to read")
    sys.exit(1)
```
Uses `realpath` (not `abspath`) so symlink escapes resolve. Tested end-to-end: legit `naval-scribe/index.html` works; `/etc/passwd` and `../../etc/passwd` both rejected with clear errors. Hit rates on naval-scribe match the original portfolio table exactly (ux: 1 warning, mobile: 2 warnings, cult: 2 warnings).

The pattern is codified as a standing rule in `learnings.md` ("Internal verifier path containment") so future lens/verifier ticks apply the same check automatically — SECURITY may not re-raise the pattern when the canonical containment check is in place.

All other angles (UI/GUIDE/USEFULNESS/COOL/LESSONS) approved. Cron should rerun IMPLEMENTATION (expected PASS), then advance to TESTS and OUTCOME.
