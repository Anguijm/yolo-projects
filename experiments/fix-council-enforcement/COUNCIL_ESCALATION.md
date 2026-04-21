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

Human decision required. Resume the build after updating session_state.json.
