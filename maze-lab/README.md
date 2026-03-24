# Maze Lab

Maze algorithm visualizer. Watch mazes generate and solve themselves step by step. 3 generation algorithms, 2 solving algorithms, adjustable speed and grid size.

## Features

### Generation Algorithms
- **Recursive Backtracker** — DFS-based, creates long winding corridors. Cursor shows current position.
- **Prim's** — frontier-based, grows outward organically. Frontier cells highlighted.
- **Kruskal's** — edge-based with Union-Find (path compression + tree linking). Random structure.

### Solving Algorithms
- **BFS** — guarantees shortest path. Explores in expanding wavefront.
- **DFS** — explores depth-first. May not find shortest path but visually dramatic.

### Visualization
- Animated step-by-step generation and solving
- Color-coded cells: generated (dark), frontier (orange tint), visited by solver (green tint), solution path (blue)
- Solution drawn as connected line from start (green) to end (red)
- Generation cursor indicator for backtracker algorithm
- Speed slider (1-50 steps per frame)

### Controls
- Grid size slider (5x5 to 40x40)
- Algorithm selectors for both generation and solving
- Generate button starts animated generation
- Solve button starts animated solving after generation
- Step button advances one step at a time (for studying algorithms)

### Architecture
- Union-Find with path compression for Kruskal's (O(α(N)) per operation)
- Canvas-rendered grid with per-cell wall drawing
- requestAnimationFrame animation loop with configurable batch stepping
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Kruskal's unionSets was O(N) flat array scan — replaced with O(1) tree linking (works with path compression in findSet)

## How to Run

Open `index.html`. Click Generate to watch the maze carve itself. Then click Solve to watch BFS or DFS find the path. Use Step for single-step mode. Adjust size and speed with sliders.
