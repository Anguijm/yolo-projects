# Changes — infra-guardrails implementation

## Files modified

### program.md (lines 47–69, +23 lines)
- Inserted `## Build Constraints` section between `## Bedrock Rules` and `## Rules`
- Section contains a 10-row pipe-delimited markdown table (C1–C10)
- Each row: `ID | Rule | Pass condition | Fail action`
- Versioning note appended below table

### experiments/infra-guardrails/check_constraints.py (new, ~60 lines)
- `check_constraints(path)` — opens program.md, verifies:
  1. All 4 required section headings present (`## Build Constraints`, `## Bedrock Rules`, `## Rules`, `## Testing Protocol`)
  2. The `## Build Constraints` section heading must appear **exactly once** (len(SECTION_RE.findall(text)) == 1); multiple occurrences fail
  3. The `## Build Constraints` section content is sliced out via `SECTION_RE = r"^\s*## Build Constraints\s*$(.*?)(?=^\s*## |\Z)"` (from its heading to the next `## ` heading, tolerating optional leading whitespace) and row-parsing is scoped to that slice only
  3. Every constraint row inside the slice matches the regex `r"^\s*\|\s*(C\d+)\s*\|([^|]+)\|([^|]+)\|([^|]+)\|"` compiled with `re.MULTILINE` — leading whitespace before `|` is tolerated; capture group 1 is the constraint ID, groups 2–4 are the Rule / Pass / Fail fields; all four must be non-empty after strip
  4. The set of IDs found in the slice equals exactly `REQUIRED_IDS = ["C1", …, "C10"]` — missing IDs and extra `C\d+` IDs both fail
- `main()` — CLI entry point; reads `program.md` from cwd by default, accepts optional `sys.argv[1]` to override for testing, exits 1 on any failure

### experiments/infra-guardrails/README.md (new, ~55 lines)
- Documents CLI usage, exact parser rules (SECTION_RE, ROW_RE), and the C1–C10 constraint summary
- Satisfies GUIDE requirement: discoverable reference for AI agents and human tooling

### experiments/infra-guardrails/changes.md (new, this file)
- Post-implementation summary for council IMPLEMENTATION gate context

## What was NOT changed
- `council.py`, `test_project.py`, `eval_bugs.py`, `security_scan.py` — all unchanged
- No skills/ files touched
- No other program.md sections modified (Bedrock Rules, Rules, Testing Protocol all intact)
