# Model Eval Suite

Regression test framework for verifying YOLO build quality across model upgrades. Contains 8 golden prompts covering the full range of YOLO project types. After a model upgrade, rebuild from these prompts and run the eval to detect quality regressions.

## Files

- `prompts.json` -- 8 representative build prompts with success criteria and minimum council scores
- `run_eval.py` -- Runner that tests built projects and generates comparison reports
- `reports/` -- Generated eval reports (gitignored, created on first run)

## Workflow

### 1. Review prompts

```bash
python3 run_eval.py --list
```

### 2. Build projects from prompts

This is a manual step. For each prompt in `prompts.json`, feed it to Claude and save the output as a YOLO project. Name the project directory to match the eval ID (e.g., `eval-1-devtool/index.html`).

### 3. Run the eval

```bash
python3 run_eval.py --model "opus-4" --run
```

This runs `test_project.py` against each built project and saves a timestamped JSON report to `reports/`.

Run a subset:

```bash
python3 run_eval.py --model "opus-4" --run --ids eval-1-devtool,eval-6-game
```

### 4. Compare two runs

After upgrading the model and rebuilding, compare reports:

```bash
python3 run_eval.py --compare reports/eval-opus-4-20260401.json reports/eval-opus-4.5-20260415.json
```

Output shows per-prompt status changes, regressions, improvements, and pass-rate delta.

## Prompt Categories

| ID | Category | What it tests |
|----|----------|---------------|
| eval-1-devtool | Dev tool | JWT decoder -- form input, parsing, error handling |
| eval-2-productivity | Productivity | Pomodoro timer -- state machine, localStorage, animation |
| eval-3-creative | Creative tool | Drum machine -- Web Audio API, grid UI, real-time playback |
| eval-4-docgen | Doc generator | README generator -- form-to-markdown, live preview, download |
| eval-5-reference | Reference tool | HTTP status codes -- data density, search/filter, expandable UI |
| eval-6-game | Game with depth | Picross -- puzzle generation, validation, undo stack, timer |
| eval-7-converter | Converter | CSS unit converter -- math precision, formula display, calc() |
| eval-8-dataviz | Data viz | CSV visualizer -- file handling, Canvas charts, drag-and-drop |

## Report Format

```json
{
  "model": "opus-4",
  "date": "2026-04-02T...",
  "total_prompts": 8,
  "passed": 6,
  "failed": 1,
  "skipped": 1,
  "results": [
    {
      "id": "eval-1-devtool",
      "status": "passed",
      "time_seconds": 2.3,
      "test_checks": { ... }
    }
  ]
}
```

## Extending

Add new prompts to `prompts.json` following the existing schema. Each prompt needs:
- `id` -- unique identifier matching `eval-N-slug` pattern
- `category` -- human-readable category label
- `prompt` -- the full build prompt (specific enough for a single-HTML-file project)
- `success_criteria` -- list of testable properties
- `min_council_scores` -- minimum acceptable council review scores per dimension
