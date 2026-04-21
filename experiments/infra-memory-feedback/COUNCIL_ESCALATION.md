# Council Escalation — experiments/infra-memory-feedback

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-21T22:30:54.711171+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The regex patterns for classifying 'prevented_bug' outcomes are too broad and risk misclassifying general agreements or non-bug-related resolutions as bug preventions, leading to incorrect metrics and flawed pruning decisions.
- **Required fix:** Refine the `prevented_bug` regex in `cmd_backfill_recall` to be more specific to actual bug fixes or preventions, avoiding terms like `ACCEPTED` or `legitimate` in isolation, which can refer to non-bug-related resolutions.
- **Evidence:** `Approach, Step 4: `prevented_bug`: `re.search(r'\bACCEPTED\b|\bFIX\s+APPLIED\b|\bAPPLY\s+FIX\b|\bFIX\s+ACCEPTED\b|\blegitimate\b', resolution, IGNORECASE)``

### SECURITY — APPROVE (low)
- **Reason:** The plan explicitly addresses SQL injection with parameterized queries and validates critical inputs. The tool is for dev-time use with no network I/O or web UI, significantly reducing attack surface.

### UI — OBJECT (high)
- **Reason:** The `mark-veto` and `mark-fp` commands require a `learning_id`, but the plan does not provide a clear, frictionless way for a user to discover this ID for an arbitrary learning.
- **Required fix:** Add a CLI command (e.g., `list-learnings`) that displays `learning_id` alongside learning content, project, and gate, or modify `mark-veto`/`mark-fp` to accept a more user-friendly identifier like a text snippet.
- **Evidence:** `Guide section: `python3 build_memory.py mark-veto <id> <proj> <gate>``

### GUIDE — APPROVE (low)
- **Reason:** The plan provides excellent self-documentation for both human users and AI agents, including clear CLI usage, naming, and detailed classification logic.

### USEFULNESS — APPROVE (low)
- **Reason:** This project provides a critical feedback loop to maintain the quality and utility of the 'learnings' corpus, preventing it from becoming a source of noise rather than signal.
- **Evidence:** `The problem of 'learning decay' (learnings becoming outdated, irrelevant, or false positives) is common in knowledge-based systems. This provides a mechanism to combat that, similar to how a bug tracker helps maintain software quality.`

### COOL — APPROVE (low)
- **Reason:** The explicit tracking of 'prevented_bug' vs. 'false_positive' for automated learnings, and the 'recall-stats' command to surface these, creates a unique feedback loop that differentiates this tool from generic metric trackers.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

Human decision required. Resume the build after updating session_state.json.
