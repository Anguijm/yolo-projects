# Plan: infra-guardrails

## Goal
Add a `## Build Constraints` section to `program.md` formalizing 7 structural guardrails as machine-readable checklist items the agent must verify before shipping.

## Scope

**In scope:**
- Adding a new `## Build Constraints` section to `program.md` with 10 explicit, enumerated constraints.
- Each constraint is stated as a testable boolean assertion (pass/fail), not narrative prose.
- A minimal proof-of-concept `experiments/infra-guardrails/check_constraints.py` (~30 lines) that reads `program.md` and verifies all C1–C10 constraint IDs exist, demonstrating the constraints are structurally machine-readable. This is the "signature move" that transforms the document into a verifiable specification.
- Full encoding into the build pipeline (pre-filter enforcement) is a follow-on tick.

**Explicitly out of scope:**
- Modifying `council.py`, `test_project.py`, `eval_bugs.py`, or `security_scan.py`
- Adding enforcement scripts (that is `infra-yolo-evals` in the queue)
- Changing the tick/tock prompt itself
- Changing any `skills/` files

## Approach

### Subtask 1 — Draft constraint list (no dependency)
Review the plan_summary constraints against the actual current session protocol. Verify each constraint maps to a real, observable build artifact or behavior. Augment with any gaps.

The 7 proposed constraints from plan_summary:
1. Max files modified per build: 50
2. Max lines added per build: 2000
3. test_project + eval_bugs + security_scan must all pass before council TESTS gate
4. Any council OBJECT halts build for fix-and-retry (no skipping)
5. Lessons VETO is a hard halt with no human override
6. Max 3 fix attempts per gate before escalation
7. Git commit message must include 'cron', 'tick', or 'tock' prefix

Additional gaps identified after reviewing current protocol:
8. `council_escalations` must be empty before any build begins (pre-flight)
9. `.harness_halt` must not exist before any build begins (pre-flight)
10. No partial push — all 4 council gates must pass before `git push`

### Subtask 2 — Write plan.md (this file) → council PLAN gate
Enumerate constraints, define pass/fail criteria for each.

### Subtask 3 — Edit program.md (depends on PLAN gate approval)
Insert `## Build Constraints` section after `## Bedrock Rules` (before `## Rules`). Format as numbered checklist with constraint ID, description, pass condition, and fail action.

### Subtask 4 — Write changes.md (depends on Subtask 3)
Brief summary of what was added/modified for implementation gate context.

### Subtask 5 — Council gates (sequential, depends on prior subtasks)
PLAN → IMPLEMENTATION → TESTS (pre-filter) → OUTCOME

## File Layout

| File | Action | Lines affected |
|------|--------|----------------|
| `program.md` | MODIFY — insert `## Build Constraints` section after line 48 (end of `## Bedrock Rules`) | +60 lines approx |
| `experiments/infra-guardrails/check_constraints.py` | CREATE — 30-line proof-of-concept verifier | ~30 lines |
| `experiments/infra-guardrails/plan.md` | CREATE | this file |
| `experiments/infra-guardrails/changes.md` | CREATE (post-implementation) | ~15 lines |

No other files modified.

## Function Map

**`experiments/infra-guardrails/check_constraints.py`**
- `check_constraints(path)` — reads `program.md`, verifies: (1) `## Build Constraints` section heading exists, (2) all constraint IDs C1–C10 appear, (3) no existing required sections (`## Bedrock Rules`, `## Rules`, `## Testing Protocol`) were removed. Returns list of failures; empty list = pass. ~25 lines.
- `main()` — CLI entry point: calls `check_constraints("program.md")`, prints PASS or failure list, exits 1 on failures. ~8 lines.

**`program.md`** — documentation only, no functions.

## Security

- `program.md` is a human-review document read by the agent at session start. It is not executed by any production system and is not user-facing. No production trust boundary.
- Constraints are declarative text. No injection surface in any live parser.
- The pre-filter test step does read `program.md` mechanically (grep/regex) to verify structural integrity — this is a one-shot verification tool used only during the build, not a production parser. The risk model differs: the verifier is read-only, not networked, and trusted. This does not contradict the "no production parser" claim.
- Per `council_escalations_resolved` policy (adopt-planning-mode, 2026-04-10): plan artifacts are human-review documents. SECURITY may not require producer-side sanitization absent a concrete downstream parser.

## UI

N/A — infrastructure change to a documentation file. No browser UI involved.

## Guide

The `## Build Constraints` section will use:
- Numbered constraints (1–10) so they can be referenced by number in build logs
- Each constraint: **ID** | **Rule** | **Pass condition** | **Fail action**
- Section header clearly states these are pre-ship gates, not guidelines

## Edge Cases

- **Constraint too vague**: If a constraint cannot be verified by inspection (e.g., "max lines" requires counting), note the verification method inline.
- **Conflicting constraints**: If two constraints conflict (e.g., "fix-and-retry 3x" vs "hard halt on VETO"), note which takes precedence. VETO always wins over retry loop.
- **program.md length**: Current file is 329 lines. Adding ~60 lines stays well within readable bounds.
- **Future constraints added**: Section includes an explicit note that the list is versioned and can be amended by the human via the tick queue.

## Test Strategy

**Pre-filter (infrastructure tick):**
- `program.md` is Markdown, not Python/JSON/shell — no `ast.parse` needed
- Verify `program.md` is syntactically valid Markdown (no broken headers, unclosed code blocks) by reading it back
- Verify the new section heading appears exactly once in the file
- Verify all 10 constraint IDs (C1–C10) appear in the section
- Verify no existing section was accidentally overwritten (check that `## Bedrock Rules`, `## Rules`, and `## Testing Protocol` still exist verbatim)

**Council TESTS gate:**
Pick 3 historical builds and check which constraints would have fired:
1. `naval-scribe` command-address-book (2026-04-08): had LESSONS VETO on tests gate → C5 (hard halt) correctly applies, C6 (max 3 attempts) also applies.
2. `experiments/adopt-planning-mode` (2026-04-09): SECURITY deadlocked after 3 attempts → C6 (max 3 → escalation) correctly applies.
3. `markdown-deck Named Snapshots` (2026-04-13): clean 4-gate pass → all 10 constraints satisfied, build proceeds normally.
