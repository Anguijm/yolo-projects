# Skill: Code Review

**Description:** Send code to Gemini for adversarial bug review and fix all identified issues. Used as a sub-skill within Tick and Tock sessions.

**Trigger:** After code is written and initial tests pass. Called by Tick and Tock skills.

---

## Methodology

### 1. Extract Code
- For HTML projects: extract the `<script>` content
- If file is too large for one call: send in sections (JS first, then HTML structure)

### 2. Send to Gemini
- Use `mcp__gemini__gemini-analyze-code` with `focus: bugs`
- Send the ACTUAL CODE, not a summary

### 3. Triage Results
Gemini will report: bugs, edge cases, runtime errors, suggestions.

**Fix immediately:**
- Real bugs (logic errors, crashes, security issues)
- Edge cases that cause data loss or corruption
- Missing null/undefined guards that crash the app

**Evaluate case-by-case:**
- Performance issues (fix if easy, note if architectural)
- UX issues (fix if the user would notice)

**Skip:**
- Style suggestions (unless they affect readability)
- DOM load order warnings (script is at bottom of body)
- Hypothetical issues on platforms we don't target

### 4. Retest
- After fixing all bugs, run the full test suite again
- If new failures → fix → retest (Dark Factory loop, max 3 cycles)

## Input
- Source code (JS extracted from HTML)
- Language identifier

## Output
- List of bugs found and fixed
- Clean test results
- Learnings entry material (FIX/INSIGHT entries)
