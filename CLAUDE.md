# Repo conventions for Claude

## Responding to "status"

When the user asks for "status" (or a close variant), reply with these four
sections, in this order. Omit a section only if it is genuinely empty — say
"none" rather than dropping the heading.

### Work done
What has been completed in this session. Include commit SHAs, branch names,
and file:line references where relevant.

### In flight
What is currently underway but not finished — uncommitted edits, running
processes, open investigations, pending reviews.

### Blockers
What is preventing progress — failing tests, missing info, denied tool calls,
waiting on user input. State the blocker concretely.

### Next
The immediate next step(s) planned. One or two bullets; not a roadmap.

Keep it terse. No preamble, no recap of the user's question.
