# Changes — infra-guardrails implementation

## Files modified

### program.md (lines 47–69, +23 lines)
- Inserted `## Build Constraints` section between `## Bedrock Rules` and `## Rules`
- Section contains a 10-row pipe-delimited markdown table (C1–C10)
- Each row: `ID | Rule | Pass condition | Fail action`
- Versioning note appended below table

### experiments/infra-guardrails/check_constraints.py (new, ~45 lines)
- `check_constraints(path)` — opens program.md, verifies:
  1. All 4 required section headings present (`## Build Constraints`, `## Bedrock Rules`, `## Rules`, `## Testing Protocol`)
  2. All constraint IDs C1–C10 found in the section
  3. Every constraint row matches `^\| C\d+ \| non-empty \| non-empty \| non-empty \|` (4 non-empty pipe-separated fields)
- `main()` — CLI entry point; exits 1 on any failure

### experiments/infra-guardrails/changes.md (new, this file)
- Post-implementation summary for council IMPLEMENTATION gate context

## What was NOT changed
- `council.py`, `test_project.py`, `eval_bugs.py`, `security_scan.py` — all unchanged
- No skills/ files touched
- No other program.md sections modified (Bedrock Rules, Rules, Testing Protocol all intact)
