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

**RESOLVED 2026-04-22 by John (interactive session). Both objections ACCEPTED — plan.md updated.**

This is the first escalation since `fix-council-enforcement` shipped (`967c98e` + `5522e24`) and the first qualitatively different one: 5 of 7 angles approve cleanly, the two surviving OBJECTs are **substantive design critiques**, and both are being addressed by improving the plan rather than overriding the council. This is what the council is supposed to do.

### BUGS OBJECT — ACCEPTED
Critique: `prevented_bug` classification regex was too broad (`\bACCEPTED\b|\blegitimate\b`), matching general approvals like *"the override was legitimate"* or *"escalation ACCEPTED as overruled"* and misclassifying them as bug preventions.

**Fix (in plan.md, Approach Step 4)**: Tightened to require bug-contextualizing anchor words:
```
\bFIX\s+APPLIED\b | \bFIX\s+ACCEPTED\b | \bACCEPTED[,.\s—-]+FIX\b
| \blegitimate\s+(?:bug|concern|critique|issue|fix|objection|defect|regression)\b
| \b(?:real|genuine)\s+(?:bug|defect|regression)\b
```

Also added regex smoke test (Test Strategy step 10) that asserts the tightened pattern does NOT match resolution text from real overridden escalations.

### UI OBJECT — ACCEPTED
Critique: `mark-veto <id>` and `mark-fp <id>` require a numeric `learning_id` but the plan provided no CLI command to discover those IDs.

**Fix (in plan.md)**: Added `cmd_list_learnings(db, limit=20, project=None)` to in-scope commands. Prints id/project/gate/snippet table. Optional `--project <name>` filter. Documented in Guide section with a worked example:

```
$ python3 build_memory.py list-learnings 10 --project naval-scribe
  id   project          gate     snippet
  42   naval-scribe     outcome  KEEP: createDocumentFragment batch...
$ python3 build_memory.py mark-fp 42 naval-scribe outcome
```

Function Map and Test Strategy updated (new tests 5 and 6).

### Other 5 angles (APPROVE) — preserved

SECURITY, GUIDE, USEFULNESS, COOL, LESSONS all approved cleanly on the first attempt. The patched council is behaving well.

Cron may rerun PLAN gate; expected clean pass now that both critiques are incorporated.
