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

Human decision required. Resume the build after updating session_state.json.
