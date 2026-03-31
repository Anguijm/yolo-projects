# Skill: Bootstrap

**Description:** Initialize a session by reading state files and determining what to do next. This is the first skill loaded in any session. It reads session_state.json, determines Tick vs Tock, and routes to the appropriate skill chain.

**Trigger:** Start of any new session, or when the user says "let's go" / "what's next" / "continue".

---

## Methodology

1. Read `session_state.json` for full context recovery
2. Read `tick_tock.next_session_type` to determine mode
3. If **Tick**: load `skills/10-tick.md`
4. If **Tock**: load `skills/11-tock.md`
5. If user overrides with specific request, follow that instead

## Input
- `session_state.json` (auto-generated)

## Output
- Decision: Tick or Tock
- Route to the correct skill chain
