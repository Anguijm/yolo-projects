# Council Escalation — experiments/fix-council-bugs-hallucination

**Gate:** outcome
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T23:24:43.310191+00:00

## Angle positions

### BUGS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: goalpost move, 0.41 overlap vs prior bugs objection] The hallucination detection logic will auto-downgrade an entire BUGS OBJECT verdict if only *some* of the claimed 'undefined' symbols are actually defined, causing legitimate bug reports for truly undefined symbols to be ignored.
- **Required fix:** Modify `detect_bugs_hallucination` to return `True` (triggering auto-downgrade) only if *all* `claimed_symbols` are found to be defined across the scanned files, rather than if *any* single symbol is found.
- **Evidence:** ````python
    for raw_path in files:
        # ... file reading and error handling ...
        ext = resolved.suffix.lower()
        # Definition-pattern check
        for s in claimed_symbols:
            if _symbol_defined_in_content(s, content, ext):
                return True # This line causes`

### SECURITY — OBJECT (high)
- **Reason:** The feature introduces multiple regular expressions that process untrusted input (verdict reason/evidence, and project file content up to 2MB), creating a potential ReDoS (Regular Expression Denial of Service) vulnerability.
- **Required fix:** All regular expressions used in `detect_bugs_hallucination` and `_symbol_defined_in_content` must be reviewed and hardened against ReDoS attacks, ensuring they cannot be exploited by crafted input to cause excessive processing time or resource consumption.
- **Evidence:** `The `detect_bugs_hallucination` function processes `verdict.reason` with `_HALLUCINATION_CLAIM_RE` and `_SYMBOL_FROM_FIX_RE`, `verdict.evidence` with `_FILE_REF_RE`, and file `content` (up to 2MB) with language-specific definition patterns within `_symbol_defined_in_content`.`

### UI — APPROVE (low)
- **Reason:** This change is an internal council logic improvement that prevents false positive BUGS objections, indirectly reducing friction for developers without direct UI impact.

### GUIDE — APPROVE (low)
- **Reason:** The auto-downgrade mechanism includes a clear prefix in the verdict, making the new behavior self-documenting for users and AI agents.
- **Evidence:** `Deliverable (experiments/fix-council-bugs-hallucination/changes.md): Modified main() -> '[AUTO-DOWNGRADED: hallucinated symbol claim, ...]' prefix; Behavior changes section; Full updated detect_bugs_hallucination function docstring`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly improves the accuracy and reliability of the automated code review system by preventing false-positive 'undefined symbol' objections, saving developer time and frustration.
- **Evidence:** `The 'OUTCOME' gate specifically mentions a historical hallucination ('byDirectionChk') that is no longer reproduced, demonstrating a real problem being solved.`

### COOL — APPROVE (low)
- **Reason:** The system's ability to auto-correct a reviewer's 'hallucinated' bug claim is a unique and memorable signature move, demonstrating self-awareness and preventing unnecessary developer friction.

### LESSONS — APPROVE (low)
- **Reason:** The deliverable addresses a documented failure mode (hallucination) and utilizes an established pattern (auto-downgrading verdicts).
- **Evidence:** `INSIGHT: Haiku UI hallucination pattern — across all 3 benchmark fixtures, the UI angle independently fabricated the same specific detail... This is a systematic single-angle hallucination type: Haiku invents a plausible-sounding technical detail and applies it uniformly. A cross-fixture comparison `

## Resolution

Human decision required. Resume the build after updating session_state.json.
