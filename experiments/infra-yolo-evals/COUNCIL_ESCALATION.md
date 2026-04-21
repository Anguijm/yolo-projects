# Council Escalation — experiments/infra-yolo-evals

**Gate:** implementation
**Reason:** LESSONS VETO — The deliverable claims to implement a 'new learnings.md "Internal verifier path containment" rule' which is not present in the provided learnings.md content, indicating a critical documentation gap in the system's memory.
**Timestamp:** 2026-04-21T16:05:00.912340+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The `focus-ring` check in `ux_completeness.py` relies on imprecise file-level regex to determine the absence of `:focus-visible` or `box-shadow` within `:focus` rules, which can lead to false positives due to the inability to accurately parse CSS rule scope and relationships.
- **Required fix:** Implement CSS parsing using a dedicated library (e.g., cssutils) to accurately identify and relate `outline` properties with `:focus` and `:focus-visible` rules within their correct scope, rather than relying on potentially ambiguous global regex searches.
- **Evidence:** `ux_completeness.py: focus-ring: flags `outline:none/0` without `:focus-visible` or `box-shadow` in a `:focus` rule`

### SECURITY — APPROVE (low)
- **Reason:** The critical path traversal vulnerability via sys.argv[1] is explicitly mitigated by a repo-root containment check using os.path.realpath before any file operations.
- **Evidence:** `All three scripts were hardened 2026-04-22 with a repo-root containment check on `sys.argv[1]` (added per the new `learnings.md` 'Internal verifier path containment' rule): `os.path.realpath(path)` is checked against `REPO_ROOT = os.path.dirname(os.path.realpath(__file__))`, and paths outside the re`

### UI — OBJECT (medium)
- **Reason:** The 'cult_status.py' script flags the absence of animations and custom drawing (canvas/SVG) as warnings, but their absence does not inherently cause user confusion, slowness, or friction, and thus are not strict user experience problems.
- **Required fix:** Re-evaluate or remove the 'animation' and 'canvas-svg' checks from 'cult_status.py' as they do not align with core UX problems that cause user friction or confusion.
- **Evidence:** `cult_status.py checks 1 and 2`

### GUIDE — APPROVE (low)
- **Reason:** All prior discoverability concerns have been addressed with comprehensive --help flags and a detailed README.md.

### USEFULNESS — APPROVE (low)
- **Reason:** The scripts provide actionable, recurring feedback on common UX, mobile, and differentiation issues in quickly built web projects, addressing real pain points for developers.
- **Evidence:** `The 'portfolio hit rates' demonstrate that the checks identify actual, common oversights (e.g., focus-ring, responsive, tap-target, table-overflow) in existing YOLO projects, indicating a clear need for such advisory tools.`

### COOL — APPROVE (low)
- **Reason:** The 'cult_status.py' script is a unique meta-tool that explicitly evaluates projects for differentiation, interactivity, and memorability, which aligns perfectly with the 'COOL' council's mandate.

### LESSONS — OBJECT (critical) 🚫 VETO
- **Reason:** The deliverable claims to implement a 'new learnings.md "Internal verifier path containment" rule' which is not present in the provided learnings.md content, indicating a critical documentation gap in the system's memory.
- **Required fix:** The 'Internal verifier path containment' rule must be formally added to learnings.md, or the claim in changes.md must be removed/corrected to reflect that it is not a documented lesson.
- **Evidence:** `All three scripts were hardened 2026-04-22 with a repo-root containment check on `sys.argv[1]` (added per the new `learnings.md` "Internal verifier path containment" rule)`

## Resolution

**RESOLVED 2026-04-22 by John (interactive session, via auto-wake). Override all three, no code changes.**

### LESSONS VETO — FALSE POSITIVE
Claimed the "Internal verifier path containment" rule is not in learnings.md. **Verified present at `learnings.md:30`** (committed in `10bd394`, 2026-04-22). Quote:

> **Internal verifier path containment (added 2026-04-22):** Any dev-time verifier or lens script at repo root that accepts a file path via `sys.argv` MUST validate that the canonicalized path is contained within the repo root before opening the file. The canonical pattern is: [...]

**Also procedurally invalid**: per the `learnings.md` *Enforcement (added 2026-04-08 after 3rd false positive)* rule, every LESSONS VETO with a stated precondition must include a `precondition_evidence` field quoting the verbatim source line proving the precondition is met. This VETO has no `precondition_evidence` field. Per the rule, the orchestrator should have auto-downgraded it to advisory and NOT blocked the build. The orchestrator is failing to enforce its own rule — flagged as a follow-up, but not blocking this tick.

### BUGS OBJECT — SCOPE CREEP OVERRIDE
Objection demands replacing the `focus-ring` regex with `cssutils` for correct CSS-rule scoping. Rejected on three grounds:
1. `ux_completeness.py` is documented as an **advisory lens** using regex heuristics (see docstring + `--help` output: "Advisory — never blocks the build"). Correctness is not the bar; useful signal-to-noise is.
2. Pulling in `cssutils` violates the zero-dep pattern the YOLO portfolio follows across 97 active tools.
3. The tick's PLAN gate explicitly constrained each lens to "100-200 lines, Python regex". `cssutils` integration would exceed plan scope and require rewriting plan.md.

Heuristic regex is the stated design, not an accidental simplification.

### UI OBJECT — WRONG RUBRIC OVERRIDE
UI angle evaluates `cult_status.py`'s `animation` and `canvas-svg` checks against **UX-friction** criteria (does absence cause confusion/slowness?). But `cult_status.py` is explicitly the **differentiation** lens — its own docstring:

> Heuristic check for signature-move indicators: animations, canvas/SVG, keyboard shortcuts, real-time interactivity, and memorable hook presence.

UX usability is `ux_completeness.py`'s mandate (error-state, empty-state, loading-state, focus-ring, primary-cta). `cult_status.py` measures memorability/cult-potential — a different rubric. The UI objection is applying the wrong rubric to the wrong artifact. Removing those two checks would gut the differentiation lens of its stated purpose.

---

All other angles (SECURITY/GUIDE/USEFULNESS/COOL) approve. Cron should rerun IMPLEMENTATION (expected PASS — no code changed), then TESTS and OUTCOME.

### Follow-up (non-blocking)
The council orchestrator is not enforcing the `precondition_evidence` rule on LESSONS VETOs. This is the second false-positive LESSONS VETO on this tick alone (first was infra-guardrails, 2026-04-21). A next-tick fix to `council.py` should reject VETOs that lack `precondition_evidence` when the cited rule has a stated precondition.
