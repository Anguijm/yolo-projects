# Stellar Forge

2048-style sliding puzzle themed as stellar nucleosynthesis. Merge identical elements to fuse heavier atoms: Hydrogen → Helium → Carbon → ... → Iron. Reach Iron and the star goes supernova.

## Features

- 4x4 sliding grid with 2048 mechanics (slide, merge, spawn)
- 11-tier element progression: H, He, C, N, O, Ne, Mg, Si, S, Ar, Fe
- Unified rotation approach (rotate grid → slide left → rotate back) for all 4 directions
- Tiles show element symbol, atomic number, and name with unique colors per element
- 90% Hydrogen / 10% Helium spawn ratio
- Score based on atomic number of fused elements
- High score persisted in localStorage
- Win detection (Iron synthesized) with one-time haptic + status
- Game over detection respects merge ceiling (max-tier tiles can't merge)
- Touch swipe support with touchmove scroll prevention
- Arrow keys + WASD keyboard support
- Spawn and merge pop animations
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Iron softlock: canMove() reported merge possible for max-tier tiles but slideRow refused to merge them — infinite loop. Fixed by skipping WIN_TIER tiles in canMove.
- Win vibration spam: every move after winning triggered vibration and status update. Fixed with winAlerted flag.
- Mobile scroll during swipe: no touchmove preventDefault — page scrolled while playing. Added scoped touchmove handler.

## How to Run

Open `index.html`. Swipe or use arrow keys/WASD to slide tiles. Merge matching elements to create heavier ones. Goal: synthesize Iron (Fe).
