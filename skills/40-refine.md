# Skill: Refine Existing Project

**Description:** Take an existing survivor project, send its code to Gemini for adversarial review, fix all bugs, update learnings. Used during refinement sweeps or on-demand.

**Trigger:** User says "refine [project]" / "improve [project]", or during a batch refinement sweep.

---

## Methodology

### 1. Select Project
- If user specified: use that project
- If batch sweep: read `yolo_log.json`, find next unrefined survivor
- Check `learnings.md` for existing refinement entries to avoid re-refining

### 2. Read Code
- Read the main file (usually `<project>/index.html`)
- If large: read in sections

### 3. Review
- Load `skills/20-review.md` protocol
- Send code to Gemini for bug review
- Fix all real bugs

### 4. Test
- Run `python3 test_project.py <project-name>`
- Dark Factory retry loop: fix → retest, max 3 cycles

### 5. Log
- Add refinement entry to `learnings.md`:
  ```
  ### <project> refinement (<date>) — PHASE 2 #N
  - **FIX**: [what was fixed]
  - **INSIGHT**: [generalizable pattern]
  ```

### 6. Commit
- `git add <project>/ learnings.md`
- `git commit -m "Refine <project> — <summary>"`
- `git push`

## Input
- Project name
- Project source code
- `learnings.md` (check for existing refinement)

## Output
- Fixed project code
- Learnings entry
- Git commit
