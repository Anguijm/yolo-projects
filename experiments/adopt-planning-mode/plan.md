# Plan: adopt-planning-mode

## Goal
Wire Claude Code planning mode into the PLAN gate so every infrastructure and YOLO build starts with a structured hierarchical plan (subtasks, file targets, sequencing) rather than free-form prose.

## Scope
**Single file change only:** `.github/workflows/tick_tock_prompt.md`

This tick does NOT:
- Modify council.py
- Modify any Python pre-filter scripts
- Create a new project directory at repo root
- Add new gating logic or exit codes

## Approach

### What "planning mode" means here
Claude Code's planning mode produces a hierarchical task breakdown BEFORE any code is written:
- Top-level goal decomposed into named subtasks
- Each subtask lists the specific file(s) it touches and the function(s) it adds/modifies
- Subtasks are sequenced (dependencies noted)
- The breakdown is machine-readable enough that a reviewer can verify completeness without running the code

### What changes in tick_tock_prompt.md
The `### Gate PLAN — before writing any code` section currently says:

> Write your plan to `<project>/plan.md` (vertical outline: goal, scope, approach, file layout, test strategy).

This will be replaced with an instruction that:
1. Opens with "Use structured planning mode" — unambiguous directive
2. Specifies the required hierarchical structure: Goal → Subtasks → per-subtask: file path + function names added/modified
3. Specifies that sequencing/dependencies must be listed
4. Specifies that the plan MUST still end with the standard review sections so council review is unchanged:
   - `## Goal` (one-liner)
   - `## Scope` (what's in / what's NOT in)
   - `## Approach` (narrative)
   - `## File Layout` (every file touched, with line-range if modifying)
   - `## Function Map` (NEW section: every function added or modified, with file path)
   - `## Security` (threat model / CSP notes)
   - `## UI` (interaction design)
   - `## Guide` (user-facing copy / labels)
   - `## Edge Cases` (error states, empty states)
   - `## Test Strategy` (how the build will be verified)
5. States explicitly: **"the plan must enumerate each file that will be touched and each function that will be added/modified before any code is written."**

The infrastructure tick variant also updates its PLAN gate instruction to match.

## File Layout
- `experiments/adopt-planning-mode/plan.md` — this file (plan artifact only, not a deliverable)
- `.github/workflows/tick_tock_prompt.md` — the single deliverable; two sections modified:
  - `### Gate PLAN — before writing any code` (~line 74-88)
  - The infrastructure PLAN gate description (~line 145)

## Function Map
No Python functions. Markdown-only change. Two blocks of prose replaced.

## Security
The plan.md output is a human-readable document reviewed by the council and the human operator. It is NOT parsed or executed programmatically — no automated system consumes the file paths or function names listed in it. The `tick_tock_prompt.md` prompt instructs the agent to write these sections for human review purposes only. No sanitization or validation is needed for the plan artifact itself because it is read by humans, not executed by scripts.

**Trust-boundary note (added after SECURITY objection 2026-04-08):** plan.md is explicitly a human-review artifact; no downstream automated parser consumes it. If that ever changes — i.e., if any script begins reading file paths or function names out of plan.md and acting on them — a sanitization layer must be added at the consumer before that parser ships. Sanitizing the producer ahead of a hypothetical consumer is out of scope for this tick.

## UI
N/A — this is a prompt instruction change.

## Guide
The new planning-mode instructions use imperative language ("Use structured planning mode", "enumerate each file", "must list") so the downstream agent cannot interpret them as optional.

## Edge Cases
- If a build is very small (1 file, 1 function), the planning mode overhead is low. The instruction covers this by saying "enumerate each file ... before any code is written" — even a 1-file plan must list it.
- If a builder skips the Function Map section, the council reviewer will notice its absence during the PLAN gate review and object. The council evaluates the plan holistically — no code change to council.py is required for this enforcement. The plan template in tick_tock_prompt.md is the authoritative spec; the council reads and reviews against it.

## Test Strategy
1. The modified tick_tock_prompt.md is the prompt for the NEXT cron run. We cannot run it in-process.
2. Council PLAN/IMPLEMENTATION/TESTS/OUTCOME gates review the change text itself and assess clarity.
3. OUTCOME gate checks: section is present, wording is imperative, Function Map is named, no regression in surrounding gate flow.
4. Snapshot comparison: before-text vs. after-text shows the two modified blocks.
