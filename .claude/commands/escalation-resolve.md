---
scope: project
---
Usage: `/escalation-resolve` (no args; reads COUNCIL_ESCALATION.md if present)

Walk the user through clearing an active council escalation.

1. Read `COUNCIL_ESCALATION.md` at repo root. If it doesn't exist, say
   "(no active escalation)" and stop.
2. Show the user a one-paragraph summary of the escalation:
   - Project + gate that escalated.
   - The angle that vetoed (LESSONS / BUGS / SECURITY / etc).
   - The reason field, verbatim.
   - The deadlock or veto type (precondition_evidence missing,
     goalpost-move auto-downgrade, BUGS hallucination, parse failure, real
     veto).
3. Ask the user to choose one resolution path:
   - **Address the concern** — describe what fix is required and where.
   - **Override** — record an entry in `.harness/session_state.json` ->
     `council_escalations_resolved[]` with `resolution: "human override"`
     plus a short reason.
   - **Defer** — leave COUNCIL_ESCALATION.md in place, do not modify
     state.
4. After the user chooses, perform the corresponding state update and
   delete `COUNCIL_ESCALATION.md` (only if option 1 or 2).
5. Print the resulting `.harness/session_state.json -> council_escalations_resolved`
   tail (last 3 entries) so the user can verify.

Do not invoke the full council pipeline. This command is a manual
human-override path.
