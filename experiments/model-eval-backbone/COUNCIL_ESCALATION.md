# Council Escalation — experiments/model-eval-backbone

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-06-25T09:59:22.470947+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The `parse_envelope` function might incorrectly calculate `clarification_count` if the model returns a non-list value for `clarifying_questions` (e.g., a string), leading to silent data corruption for a key metric.
- **Required fix:** `parse_envelope` must ensure the `clarifying_questions` field is always a list (potentially empty) before `len()` is called, or the `clarification_count` logic must be robust to non-list types to prevent miscalculation.
- **Evidence:** `Approach §3: `clarification_count = len(clarifying_questions)`. Function Map: `parse_envelope(text) -> dict` — tolerant parse of the model's JSON reply (fenced/bare).`

### SECURITY — APPROVE (low)
- **Reason:** The plan demonstrates robust security considerations, particularly in handling untrusted model output and preventing path traversal.

### UI — APPROVE (low)
- **Reason:** The plan for the CLI tool provides excellent user feedback, clear error handling, and good first-use experience via dry-run and comprehensive help.

### GUIDE — APPROVE (low)
- **Reason:** The plan explicitly addresses discoverability through a comprehensive README, detailed CLI help, clear error messages, and documentation for AI model interaction.

### USEFULNESS — APPROVE (low)
- **Reason:** This project provides a critical, recurring internal tool for data-driven decision-making on LLM backbone upgrades, directly supporting the portfolio's core generation capability.
- **Evidence:** `It solves the specific problem of objectively evaluating new generation models (performance vs. cost) before promotion, a recurring need for maintaining core infrastructure.`

### COOL — APPROVE ()
- **Reason:** The robust 'clarification_count' metric, derived from a strict JSON contract, provides a unique and measurable signal of model uncertainty, and the clear 'promote / keep / mixed' recommendation offers an opinionated, actionable signature output for this internal benchmark.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

Human decision required. Resume the build after updating session_state.json.
