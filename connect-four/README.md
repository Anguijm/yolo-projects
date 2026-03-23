# Connect Four

Classic Connect Four against a minimax AI with alpha-beta pruning. Three difficulty levels. Drop pieces, connect four in a row to win.

## Features

- 7x6 grid with gravity drop mechanics
- Minimax AI with alpha-beta pruning (depth 2/5/7)
- Center-weighted heuristic using column weight array [0,1,2,3,2,1,0]
- Window scoring: evaluates all 4-cell windows for threats and opportunities
- Depth-aware terminal scoring (prefers faster wins, delays losses)
- Column hover preview showing where piece will land
- CSS drop animation on piece placement
- Win line highlighting (green glow)
- W/L/D score tracked in localStorage
- Move ordering (center-first) for better alpha-beta pruning
- AI thinking indicator with setTimeout yield to UI thread
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- renderBoard wiped all CSS classes including 'dropping' animation (now only toggles player classes)
- CENTER_WEIGHT array defined but unused — evaluate() hardcoded center check (now uses full weight array)
- AI didn't prefer faster wins or slower losses — all terminal states scored equally (added depth factor)
- Preview class could get stuck after piece drop (added clearPreviews before moves)

## How to Run

Open `index.html`. Click a column to drop your piece (red). AI responds with yellow. Select difficulty with Easy/Medium/Hard buttons.
