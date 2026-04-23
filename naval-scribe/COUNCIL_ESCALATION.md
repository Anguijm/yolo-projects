# Council Escalation — naval-scribe

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-23T06:34:34.971780+00:00

## Angle positions

### BUGS — OBJECT (medium)
- **Reason:** The `setDraftStatus` helper function does not explicitly handle the edge case where the provided `id` does not correspond to an existing draft, which could lead to a misleading 'storage full' error message.
- **Required fix:** Modify `setDraftStatus` to explicitly check if a draft with the given `id` was found. If no draft is found, it should return `false` without attempting to modify a non-existent object, preventing a `TypeError` and ensuring the 'storage full' error is not displayed for an 'ID not found' scenario.
- **Evidence:** `Subtask 2 — Data layer: `setDraftStatus()` helper and draft save update: 'reads drafts array, finds entry by `id`, sets `.status`'`

### SECURITY — APPROVE (low)
- **Reason:** The plan explicitly states that status values are hardcoded and all user-visible strings, including status labels, will continue to be routed through `esc()` before rendering, which mitigates injection risks given the architectural constraints.

### UI — APPROVE ()
- **Reason:** 

### GUIDE — APPROVE (low)
- **Reason:** The plan includes excellent provisions for discoverability, including clear UI hints, descriptive naming, and explicit documentation for AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** This feature provides essential workflow management for users handling multiple formal documents, directly enhancing the tool's core utility.
- **Evidence:** `Users drafting multiple letters frequently need to track their progress (e.g., awaiting signature, sent, awaiting reply) to manage their workload effectively. This centralizes that tracking within the document creation tool, preventing the need for external systems or manual notes.`

### COOL — APPROVE (low)
- **Reason:** The status tracking feature directly reinforces Naval Scribe's identity as a reliable, standards-conforming utility by enhancing workflow management for formal correspondence, without introducing unnecessary complexity or 'toys'.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The plan introduces a new user-facing feature (status tracking) but fails to include updating the `ai-prompt-content` block, violating the documented lesson about AI prompt discoverability.
- **Required fix:** Add a subtask to update the `ai-prompt-content` block in `index.html` with a new section documenting the Letter Status Tracker feature, including its states, how to interact with badges, and filter functionality.
- **Evidence:** `KEEP — AI prompt updated on every feature tock: The ai-prompt-content block is part of the tool's discoverability surface. Every tock that adds a user-facing feature must update it. GUIDE will object if it's missing — don't wait for the objection.`

## Resolution

Human decision required. Resume the build after updating session_state.json.
