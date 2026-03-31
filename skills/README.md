# YOLO Skills System

Agent-readable skill files that decompose the YOLO build loop into discrete, chainable units.

## Architecture

```
skills/
  00-bootstrap.md   — Session init: read state, route to Tick or Tock
  10-tick.md         — YOLO build session (ideate → build → test → review → ship)
  11-tock.md         — Markdown Deck flagship session (read roadmap → implement → test → document)
  20-review.md       — Gemini code review sub-skill (used by Tick and Tock)
  30-phase4.md       — YouTube pipeline (fetch → summarize → extract experiments)
  40-refine.md       — Refine an existing project (review → fix → log)
```

## How to Use

At the start of any session:
1. Read `session_state.json` for context recovery
2. Read `skills/00-bootstrap.md` to determine what to do
3. Follow the routed skill's methodology step by step
4. Each skill defines its Input (what to read) and Output (what to produce)

## Design Principles

- **Under 150 lines per skill** — focused, not monolithic
- **Description first** — tells the agent WHEN to trigger this skill
- **Input/Output contracts** — output of one skill feeds the next
- **Reasoning over steps** — explains WHY, not just WHAT
- **Composable** — skills can be chained (bootstrap → tick → review → commit)

## Relationship to program.md

`program.md` remains the canonical reference for bedrock rules and constraints. These skills are the *executable decomposition* of program.md — same rules, structured for agent consumption.
