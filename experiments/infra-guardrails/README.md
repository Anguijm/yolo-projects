# infra-guardrails

Formalizes structural guardrails as machine-checkable build constraints in `program.md`.

## What this tick does

Adds a `## Build Constraints` section to `program.md` containing 10 named constraints (C1–C10),
each expressed as `ID | Rule | Pass condition | Fail action`. Adds `check_constraints.py` as a
proof-of-concept verifier that confirms the section is structurally intact before any build ships.

## Running the verifier

```bash
# From the repo root:
python3 experiments/infra-guardrails/check_constraints.py

# With an explicit path (for testing against a different file):
python3 experiments/infra-guardrails/check_constraints.py path/to/program.md
```

Exit 0 = PASS. Exit 1 = FAIL with a list of failures.

## Parser rules (for AI agents and tooling)

The verifier enforces these structural rules on `program.md`:

1. **Required headings** (all must be present, anywhere in the file):
   - `## Build Constraints`
   - `## Bedrock Rules`
   - `## Rules`
   - `## Testing Protocol`

2. **Exactly-once rule**: `## Build Constraints` must appear exactly once.

3. **Section scope**: Rows are parsed only within the body of `## Build Constraints` —
   from the heading line to the next `## ` heading (or end of file).
   SECTION_RE: `r"^\s*## Build Constraints\s*$(.*?)(?=^\s*## |\Z)"` (MULTILINE|DOTALL)

4. **Row format**: Each constraint row must match:
   `r"^\s*\|\s*(C\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|"` (MULTILINE)
   — leading whitespace before `|` is tolerated. The regex allows empty fields so malformed
   rows still match; the subsequent non-empty check reports them as "Row CN: one or more
   empty fields" rather than silently skipping (which would produce a misleading
   "Missing constraint: CN" error).

5. **Exact ID set**: The section must contain exactly C1, C2, C3, C4, C5, C6, C7, C8, C9, C10.
   Missing IDs and extra `C\d+` IDs both fail.

## Constraints defined (C1–C10)

| ID | Rule |
|----|------|
| C1 | Max 50 files modified per build |
| C2 | Max 2000 lines added per build |
| C3 | Pre-filter (test_project + eval_bugs + security_scan) passes before TESTS gate |
| C4 | Council OBJECT triggers fix-and-retry (no skipping) |
| C5 | LESSONS VETO is a hard halt — no auto-fix |
| C6 | Max 3 fix attempts per gate before escalation |
| C7 | Commit message must start with cron( / tick: / tock: / ESCALATION: |
| C8 | council_escalations must be empty at build start |
| C9 | .harness_halt must not exist at build start |
| C10 | All 4 gates must pass before git push |
