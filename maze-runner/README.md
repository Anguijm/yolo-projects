# Maze Runner

Navigate procedurally generated mazes. Your trail glows behind you. Timer counts up. Beat your best time. Maze grows each level.

## Features

- Recursive backtracker maze generation (guaranteed solvable)
- Arrow keys / WASD for desktop, swipe for mobile
- Mobile swipe slides until wall (multiple cells per swipe)
- Glowing cyan trail with shadowBlur follows your path
- Smart backtracking: retracing steps removes trail (pop instead of push)
- Timer with cached DOM element (no 60fps getElementById)
- Escalating difficulty: 8x8 → 10x10 → 12x12... up to 30x30
- Best time per size tracked in localStorage
- Entrance at top-left, exit at bottom-right (walls opened)
- Green glowing exit marker
- Player shown as glowing cyan dot
- Haptic feedback on movement (5ms) and win (pattern)
- Game over overlay with time, best time, next size
- Next maze text shows correct clamped size
- touchmove prevented on canvas only
- OLED black, mobile-first, all PWA metas

## Improvements from Gemini Code Audit

- Next maze text showed size+2 before clamping (moved increment before display)
- getElementById in 60fps timer loop (cached element reference)
- Trail grew forever on backtracking (smart pop/push logic)
- Single-step mobile swipe was unplayable (slide-until-wall loop)

## How to Run

Open `index.html` on your phone. Tap START, swipe to navigate.

## What You'd Change

- Input buffering (queue next direction before reaching intersection)
- Fog of war (only see cells near player)
- Multiple maze algorithms (Prim's, Kruskal's)
- Share best time format
