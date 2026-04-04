# Skill: Tick (YOLO Build Session)

**Description:** Build one new project from scratch in a single session. Follow the full build pipeline: ideate → build → test → review → fix → log → commit. Use this when session_state says next_session_type is "tick".

**Trigger:** Tick-Tock cron, or user says "build" / "tick" / "new project".

---

## Methodology

### 1. Ideate
- Read `learnings.md` (first 50 lines — accumulated principles)
- Read `yolo_log.json` to avoid duplicates
- Check `markdown-deck/deck_roadmap.md` → YOLO Feeder Projects for unbuilt feeders
- If feeder available → build that (it serves double duty)
- Otherwise → generate a fresh idea biased toward useful dev tools
- Bounce idea off Gemini brainstorm (whimsical vs too-cool dynamic)

### 2. Build
- Read `design.md` for visual system
- Single HTML file, zero dependencies
- Follow bedrock rules: test everything, Gemini audits all code, learn from every build
- Mobile-first, PWA meta tags, touch-friendly

### 3. Test
- Run `python3 test_project.py <project-name>`
- If ANY check fails → fix → retest (max 3 retries per Dark Factory protocol)
- **Halt escalation:** If test_project.py fails 3 times in a row on the same project, STOP. Write a `.harness_halt` file in the project directory containing the error output and timestamp. Do NOT attempt more builds until a human removes the halt file. This prevents infinite retry loops in autonomous cron runs.

### 4. Review
- Send actual JS code to `mcp__gemini__gemini-analyze-code` (focus: bugs)
- Fix every real bug Gemini identifies
- Retest after fixes
- **Gemini call cap:** Track total Gemini MCP calls this session. If the count reaches 15, skip remaining council review angles and ship with partial review. Log "PARTIAL REVIEW: Gemini cap reached" in the commit message. This prevents runaway API costs in autonomous sessions.

### 5. Ship
- Write `README.md` in project folder
- Add entry to `yolo_log.json`
- Regenerate dashboard: `python3 update_dashboard.py`
- Add learnings entry to `learnings.md`
- If feeder: mark as "FEEDER: ready for Deck integration"

### 6. Commit & Update State
- `git add <project>/ yolo_log.json dashboard.html learnings.md`
- `git commit` with Co-Authored-By trailer
- `git push`
- Update session log in `markdown-deck/deck_roadmap.md`
- Run `python3 update_session_state.py`

## Input
- `session_state.json` (context)
- `design.md` (visual system)
- `learnings.md` (patterns)
- `yolo_log.json` (what exists)

## Output
- One shipped project (HTML file + README)
- Updated yolo_log.json, dashboard, learnings
- Updated session_state.json
