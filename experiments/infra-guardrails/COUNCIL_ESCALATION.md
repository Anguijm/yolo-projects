# Council Escalation — experiments/infra-guardrails

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-13T20:02:31.044198+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The stated goal is to formalize structural guardrails as "machine-checkable build constraints" and "testable boolean assertions", but the `check_constraints.py` proof-of-concept only verifies the *structural presence* of constraint IDs and the section header, not that the *content* of the constraints adheres to a machine-parsable format or is actually a testable boolean assertion, creating a risk that the constraints will not be truly machine-readable as intended.
- **Required fix:** The `check_constraints.py` must be extended to verify that each constraint (C1-C10) in `program.md` follows the specified machine-parsable format (e.g., 'ID | Rule | Pass condition | Fail action') to ensure the content is indeed structurally machine-readable, not just that the IDs exist.
- **Evidence:** `Function Map: `check_constraints(path)` — reads `program.md`, verifies: (1) `## Build Constraints` section heading exists, (2) all constraint IDs C1–C10 appear, (3) no existing required sections ... were removed. Test Strategy: Verify all 10 constraint IDs (C1–C10) appear in the section.`

### SECURITY — OBJECT (high)
- **Reason:** The plan introduces machine-readable constraints into `program.md`, which an LLM agent reads, but the proposed `check_constraints.py` only verifies structural elements (section header, constraint IDs) and does not validate the *content* of the constraints or prevent the injection of malicious instructions into `program.md`, creating a prompt injection vulnerability.
- **Required fix:** The `check_constraints.py` proof-of-concept, or a planned follow-up, must include content validation for the `## Build Constraints` section to prevent prompt injection, such as verifying the exact text of the constraints or ensuring no unauthorized text is present beyond the defined structure.
- **Evidence:** `program.md is a human-review document read by the agent at session start. It is not executed by any production system and is not user-facing. No production trust boundary. (from plan's Security section)`

### UI — APPROVE (low)
- **Reason:** This change is an internal documentation update and does not involve any user-facing UI elements or interactions.
- **Evidence:** `UI section explicitly states 'N/A — infrastructure change to a documentation file. No browser UI involved.'`

### GUIDE — APPROVE ()
- **Reason:** 

### USEFULNESS — APPROVE (low)
- **Reason:** Formalizing operational guardrails in a machine-readable format is a fundamental step towards robust, predictable agent behavior and enables future automated enforcement.
- **Evidence:** `The proposed constraints address real-world operational challenges (e.g., build size, council gate adherence, escalation policies) that benefit from clear, centralized, and eventually machine-enforced definitions. The `check_constraints.py` proof-of-concept demonstrates the critical 'machine-readabl`

### COOL — APPROVE ()
- **Reason:** The `check_constraints.py` proof-of-concept transforms a human-readable Markdown document into a partially machine-verifiable specification, creating a signature move for lightweight, hybrid policy enforcement.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

**Resolved 2026-04-19 by John (interactive session, via Claude).**

**BUGS OBJECT — ACCEPTED.** Plan amended: `check_constraints.py` now also verifies each constraint row parses into the canonical `C# | Rule | Pass | Fail` format with four non-empty pipe-separated fields (Function Map + Test Strategy updated in `plan.md`). BUGS's concern was legitimate — "machine-checkable" means parseable content, not just ID presence. Estimated verifier size grows from ~30 to ~40 lines.

**SECURITY OBJECT — OVERRIDDEN.** Precedent: `adopt-planning-mode` plan-gate escalation resolved 2026-04-09 ("plan artifacts are human-review documents, not machine inputs — SECURITY may not require producer-side sanitization absent a concrete downstream parser"). The broadened goalpost-moving rule in `learnings.md` (2026-04-09) applies here: same angle, substantively similar "prompt injection on LLM-read document" concern, no new evidence of a concrete production parser. `program.md` is self-authored by the agent, human-reviewed at commit time, committed to the repo, and read by the agent at session start — the agent is both producer and consumer and human review sits between. No trust boundary is crossed.

Build may proceed to IMPLEMENTATION gate with the amended plan.
