# Git Time Machine

Type real Git commands, watch the commit DAG animate in real-time. Learn branching, merging, rebasing, and cherry-picking visually. Single HTML file, zero dependencies.

## Features

- Mock Git engine: commit, branch, checkout (-b), merge, rebase, cherry-pick, log, status
- Visual DAG: colored lanes per branch, bezier curves for cross-lane connections
- Branch labels as colored tags, HEAD indicator with glow
- Merge detection: fast-forward vs merge commit (BFS ancestor check)
- Rebase: replays commits onto target branch with visual re-routing
- Cherry-pick: copies commit with attribution
- 5 progressive challenges: First Commit, Branching, Merge, Feature Workflow, Cherry Pick
- Sandbox mode for free play
- Terminal with command history (up/down arrows)
- Color-coded output: blue=commands, green=success, red=errors
- Built-in help command
- Readable short commit IDs (c0, c1, c2...)

## How to Run

Open `index.html` in a browser. Type `help` in the terminal to see all commands.

## What You'd Change

- git reset (hard/soft/mixed) with visual pointer sliding
- Graph panning/zooming for large DAGs
- Animated transitions (nodes sliding on rebase)
- More challenges (conflict resolution, interactive rebase)
