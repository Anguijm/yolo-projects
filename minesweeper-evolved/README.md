# Minesweeper Evolved

Classic minesweeper with a twist: correctly flag a mine and it EXPLODES, clearing adjacent tiles. Chain reactions possible. Supports hex AND square grids. Single HTML file, zero dependencies.

## Features

- The Evolved Mechanic: flagged mines explode, clearing a radius
- Chain reactions: explosions can trigger other flagged mines
- Chain depth tracking with "3x CHAIN!" flash notifications
- Hex grid (6-way adjacency) and Square grid (8-way adjacency)
- First-click safety (mines placed after first click)
- Flood fill for zero-adjacent cells
- Screen shake (intensity scales with chain depth)
- Particle explosions at detonation sites
- 3 difficulty levels: Easy (8x8), Medium (12x12), Hard (16x16)
- Dig/Flag mode toggle for mobile/touch support
- Color-coded numbers, emoji mines and flags
- Win/loss overlays with chain stats
- Keyboard: N/Enter = new game

## How to Run

Open `index.html` in a browser. Left-click to reveal, right-click to flag (or use the Mode toggle for touch).

## What You'd Change

- Sound effects (explosion boom, chain ding)
- Leaderboard with best chain per difficulty
- Animated mine counter countdown
- Custom grid sizes
