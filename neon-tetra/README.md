# Neon Tetra

Falling block puzzle with neon glow aesthetic. 7-bag randomizer, ghost piece, wall kicks, hard/soft drop, progressive difficulty.

## Features

- 10x20 grid, 7 standard tetrominoes (I, J, L, O, S, T, Z)
- 7-bag randomizer ensures fair piece distribution
- Ghost piece shows landing position
- Hard drop (Space) with screen shake, soft drop (Down) with bonus points
- Wall kick rotation (basic SRS with 6 kick positions)
- O-piece skip rotation (prevents wobble)
- Next piece preview
- Line clearing with NES-style scoring (100/300/500/800 × level)
- Level progression every 10 lines, speed increases
- Gravity tick decoupled from render loop
- 1-second restart delay on game over (prevents accidental restart)
- Arrow keys + WASD + touch controls for mobile
- Neon glow via Canvas shadowBlur
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- O-piece (square) rotation caused wall-kick shifting (now skips rotation entirely)
- Instant restart on game over — player couldn't see final board state (added 1s delay)
- Grid not initialized before first draw call (caused console error on load)

## How to Run

Open `index.html`. Press any key or tap to start. Arrow keys/WASD to move and rotate, Space for hard drop. Clear lines to level up.
