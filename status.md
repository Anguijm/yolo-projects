# yolo-projects: status (index tool)

Updated 2026-10-18 (JST).

## Query tool: yolo_index.py
Local search over everything written and unwritten in this repo. Rebuilds `.index/yolo.db` from the files
on every `build` (the folder is excluded from git via `.git/info/exclude`). No network, no GPU, no API key.

Indexes: 219 built project folders (README + build log entry), 1,167 cards in experiments.json
(status, verdict, outcome, history), 2,033 build_memory.db learnings, 247 build log entries, 17 phase4 queue
videos, root and .harness docs, 214 experiments/ folder files.

Commands: `python3 yolo_index.py build | stats | search "text" [--kind K --status S] | cards --status discarded -q text | projects -q text | show <slug>`

Card counts at build time: backlog 609, discarded 348, adopted 90, deferred 56, done 48, in_progress 10, skipped 6.

## Disabled on purpose (do not re-enable)
- Phase 4 research workflow: off since 2026-10-17 (no API key).
- Feed snapshot cron: off since 2026-10-18 (John's Gemini task replaced it).
