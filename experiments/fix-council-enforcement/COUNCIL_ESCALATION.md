# Council Escalation — experiments/fix-council-enforcement

**Gate:** plan
**Reason:** LESSONS VETO — The plan proposes to implement a 'Goalpost-move auto-downgrade' rule, claiming it is documented in `learnings.md` (added 2026-04-09), but this specific rule (automated downgrade based on >0.6 keyword overlap) is not present in the provided `learnings.md` content.
**Timestamp:** 2026-04-21T18:53:24.542633+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** Council member returned unparseable output
- **Required fix:** Re-run this angle with stricter JSON instructions
- **Evidence:** `{
  "angle": "bugs",
  "verdict": "OBJECT",
  "severity": "high",
  "reason": "The proposed enforcement of LESSONS VETO `precondition_evidence` is flawed, using a regex that is too restrictive for common file paths and a keyword check that is too permissive, leading to incorrect downgrades or preser`

### SECURITY — OBJECT (high)
- **Reason:** The plan introduces file system access based on a 'project' variable, which could lead to path traversal if not strictly validated against the repository root.
- **Required fix:** Explicitly add `proj_dir.resolve().is_relative_to(REPO_ROOT)` before any file system operations (like `.exists()` or `.glob()`) within the `check_goalpost_moves` function to prevent reading files outside the intended project directory.
- **Evidence:** `File: council.py (implied location in `check_goalpost_moves` function)
Code snippet: `proj_dir = REPO_ROOT / project` (from plan, under Subtask 3)
Proposed fix in plan: `proj_dir.resolve().is_relative_to(REPO_ROOT)` (from Security section)`

### UI — APPROVE (low)
- **Reason:** The proposed changes improve the clarity and actionability of system feedback in logs, reducing unnecessary friction and cognitive load for users by preventing transient errors and repetitive escalations.

### GUIDE — APPROVE (low)
- **Reason:** The plan explicitly documents new enforcement rules in `learnings.md` and provides clear log messages for runtime discoverability.
- **Evidence:** `plan.md: Guide section, specifically 'Append a short section to learnings.md...'`

### USEFULNESS — APPROVE (low)
- **Reason:** This project directly addresses high-frequency, high-impact friction points in the automated review system, improving reliability and reducing human intervention for false positives.
- **Evidence:** `The plan explicitly details four consecutive council escalations in a single afternoon due to these bugs, demonstrating a clear, recurring problem that costs human decision cycles.`

### COOL — OBJECT (critical)
- **Reason:** The proposed changes are internal reliability and enforcement improvements, not user-facing features that create a memorable or differentiated experience.
- **Required fix:** Introduce a user-facing 'signature move' that leverages one of these internal enforcement mechanisms in a unique, interactive, or shareable way, beyond simple log statements. For example, a 'Council Self-Correction Report' that visualizes the goalpost-move detection.
- **Evidence:** `other internal CI/CD or automated review systems`

### LESSONS — OBJECT (critical) 🚫 VETO
- **Reason:** The plan proposes to implement a 'Goalpost-move auto-downgrade' rule, claiming it is documented in `learnings.md` (added 2026-04-09), but this specific rule (automated downgrade based on >0.6 keyword overlap) is not present in the provided `learnings.md` content.
- **Required fix:** Document the 'broadened no-goalpost-moving rule' in `learnings.md` with the specified criteria (keyword overlap > 0.6 leading to auto-downgrade) before attempting to implement its enforcement in `council.py`.
- **Evidence:** `From plan.md: 'The broadened no-goalpost-moving rule (`learnings.md`, added 2026-04-09) specifies that if an angle OBJECTed on the same (project, feature) at any prior gate AND the new reason's keyword overlap against any prior reason exceeds 0.6, the new OBJECT auto-downgrades to advisory. Not impl`

## Resolution

**RESOLVED 2026-04-22 by John (interactive session). Override all four, no plan changes.**

Meta-recursive irony: the council exhibited three of the four bugs this tick is designed to fix, during the PLAN gate of the tick itself.

### LESSONS VETO — FALSE POSITIVE (4th in 2 days)
Claimed the "Goalpost-move auto-downgrade" rule with 0.6 keyword overlap is not in `learnings.md`. **Verified present at `learnings.md:22`** with exact wording:

> "If keyword overlap exceeds 0.6 (count shared non-stopword tokens / max token count of the two reasons), auto-downgrade the new objection to advisory."

Plus no `precondition_evidence` field per the enforcement rule. This is precisely the symptom the tick fixes.

### BUGS OBJECT — PARSE FAILURE
Reason: `"Council member returned unparseable output"`. Evidence field shows the truncated JSON that would have been a legitimate review if parsed. This is `council.py:80-87` — the bug the tick fixes. Not a real objection.

### SECURITY OBJECT — NON-OBJECTION
Required fix: `"Explicitly add proj_dir.resolve().is_relative_to(REPO_ROOT) before any file system operations"`. **The plan already specifies this exact check in its `## Security` section.** SECURITY even quotes the plan text in its own evidence:

> "Proposed fix in plan: `proj_dir.resolve().is_relative_to(REPO_ROOT)` (from Security section)"

The angle agrees with the plan but submitted an OBJECT verdict. Either orchestrator mis-classification or the angle mis-routed its own review as a disagreement. Not a finding.

### COOL OBJECT — WRONG RUBRIC
Demands a "user-facing signature move" for internal orchestrator infrastructure. `council.py` runs in cron, not a browser. Per the standing override pattern (infra-guardrails, infra-yolo-evals), COOL does not apply to internal build infrastructure.

### Value added from this escalation

Added this episode as the **5th replay fixture** in `plan.md`'s test strategy — it is the cleanest triple-bug demonstration available (LESSONS false positive + BUGS parse failure + SECURITY non-objection in one package). Implementation will verify the patched code correctly handles all three.

Cron may resume PLAN gate. No plan changes.
