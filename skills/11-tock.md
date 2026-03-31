# Skill: Tock (Markdown Deck Flagship Session)

**Description:** Work on the Markdown Deck flagship product. Pick the highest-priority item from deck_roadmap.md and implement it. Multi-session development — features may span multiple Tock sessions.

**Trigger:** Tick-Tock cron, or user says "deck" / "tock" / "markdown deck".

---

## Methodology

### 1. Read Context
- Read `markdown-deck/deck_roadmap.md` for current priorities
- Read `session_state.json` → `markdown_deck.pending_items` for what's next
- If user gave specific feedback → address that first (user feedback overrides roadmap)

### 2. Implement
- Read current `markdown-deck/index.html`
- Implement the next unchecked item from the roadmap
- Higher quality bar than Tick: regression test all existing features
- If integrating a feeder project: extract the pure function, adapt to Deck's architecture

### 3. Test
- Verify JS syntax: extract script, run `node -c`
- Run `python3 test_project.py markdown-deck`
- Known false positive: brace_balance fails on OOXML strings (ignore if other checks pass)
- Manually verify: browser loads, no console errors

### 4. Update Documentation
- **MANDATORY:** Update `markdown-deck/DECK_GUIDE.md` with new feature syntax/behavior
- Update `markdown-deck/deck_roadmap.md`: check off item, add session log entry

### 5. Commit & Update State
- `git add markdown-deck/`
- `git commit` with Co-Authored-By trailer describing what was implemented
- `git push`
- Run `python3 update_session_state.py`

## Input
- `session_state.json` (context)
- `markdown-deck/deck_roadmap.md` (priorities)
- `markdown-deck/index.html` (current code)
- `markdown-deck/DECK_GUIDE.md` (documentation)

## Output
- One feature shipped in Markdown Deck
- Updated DECK_GUIDE.md
- Updated deck_roadmap.md (item checked, session logged)
- Updated session_state.json
