# git-xray

X-ray any git repo into a single interactive HTML visualization.

## What it does

Point it at a git repository and it analyzes the full history to produce an interactive dashboard with:

- **Overview** — stats, hottest files, language distribution
- **Hotspots** — sortable table of every file with commit count, churn, size, age, and top author (with inline bar charts)
- **Treemap** — visual map of the codebase sized by file size, colorable by language, hotspot intensity, or code age
- **Authors** — contributor ranking by commit count
- **Activity** — commit frequency over the last 90 days

Everything is a single self-contained HTML file. No server needed, just open it in a browser.

## How to run

```bash
# X-ray any repo
python3 git_xray.py /path/to/repo

# Custom output path
python3 git_xray.py /path/to/repo -o my-report.html

# Current directory (if it's a git repo)
python3 git_xray.py .
```

No dependencies beyond Python 3 stdlib. Just `git` on PATH.

## What you'd want to change

- The `first_seen` analysis caps at 500 files for speed — increase if you want full history on larger repos
- The treemap caps at 300 files — adjustable in `renderTreemap()`
- The hotspot table shows 200 files max — adjustable in `renderHotspots()`
- Activity timeline is hardcoded to 90 days — change the `--since` in `analyze_repo()`
- MFU reference is H100 — irrelevant here, this is just git analysis
