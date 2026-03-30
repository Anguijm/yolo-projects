# commit-log

Visual git commit history explorer and analytics dashboard. Paste any `git log` output and get an interactive timeline, frequency heatmap, hour-of-day distribution, top contributors chart, and commit message word cloud.

## Usage

Open `index.html` in a browser. Paste git log output into the textarea and click **Parse & Analyze**.

### Supported input formats

```bash
# Pipe-delimited (richest — includes author, email, date)
git log --format="%h|%an|%ae|%ai|%s"

# Oneline (hash + message)
git log --oneline

# Oneline with graph decoration
git log --oneline --graph

# Full verbose git log
git log

# Plain commit messages (no hash — synthetic dates assigned)
```

## Features

- **Contribution heatmap** — 52-week GitHub-style grid showing commit frequency by day
- **Hour-of-day bars** — when does this team actually commit?
- **Top contributors** — horizontal bar chart with per-author color coding
- **Commit timeline** — density histogram with individual dots (clickable)
- **Word cloud** — most frequent words in commit messages (stop words filtered)
- **Author filter** — click any author to hide/show their commits across all charts
- **Commit detail** — click any commit for full hash, date, author, position in history
- **Presets** — four sample logs (react, vscode, linux kernel, solo-dev) loaded instantly

## Stats shown

- Total commits, active days, avg commits per active day
- Longest consecutive day streak
- Peak commit hour and peak day of week

## Project #156 — YOLO Projects
