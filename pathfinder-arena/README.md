# Pathfinder Arena

Draw walls, click "Race!", and watch 6 pathfinding algorithms compete on the same grid simultaneously. See which explores fewer nodes and finds the shortest path. Single HTML file, zero dependencies.

## Features

- 6 algorithms racing at once: A*, Dijkstra, BFS, Greedy Best-First, DFS, Bidirectional BFS
- Draw walls by clicking/dragging, erase, set start/end points
- All algorithms visible on same grid with color-coded overlays
- Path lines offset per algorithm to prevent overlap
- Live stats panel: nodes visited, path length, steps used
- Progress bars showing exploration coverage
- 4 maze presets: Random, Spiral, Rooms, Diagonal
- 3 grid sizes: 30x30, 40x40, 60x60
- Speed slider (1-50 steps/frame)
- Keyboard shortcuts: Space=race, R=reset, C=clear, 1-4=tools

## How to Run

Open `index.html` in a browser. Draw some walls (or pick a maze preset) and click "Race!"

## What You'd Change

- Binary min-heap for A*/Dijkstra priority queues
- Algorithm visibility toggles per card
- Diagonal movement option (8-way with Euclidean heuristic)
- Step-by-step mode (advance one step at a time)
