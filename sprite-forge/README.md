# Sprite Forge

Pixel art animation studio. Draw frames on a 16x16 grid, preview the animation, and export as a PNG sprite sheet. Onion skinning, flood fill, and adjustable FPS.

## Features

- 16x16 pixel drawing canvas with checkerboard transparency
- Tools: pencil, eraser, flood fill (stack-based BFS)
- Color picker for any color
- Frame timeline: add, duplicate, delete frames
- Onion skinning (15% opacity ghost of previous frame)
- Live animation preview with adjustable FPS (1-24)
- PNG sprite sheet export (horizontal strip via toBlob)
- Optimized timeline: only redraws active frame thumbnail during drawing (not full DOM rebuild)
- Pointer capture for smooth drag drawing
- Canvas auto-sizes to fit available space
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Timeline DOM thrash: rebuilt ALL canvas thumbnails on every pixel painted (60fps DOM creation) — now only updates active frame thumbnail during drawing
- Dead code: fill tool had impossible `tool === 'eraser'` check inside `tool === 'fill'` branch — simplified
- FPS clamp: 0 FPS caused Infinity interval — clamped to minimum 1

## How to Run

Open `index.html`. Select a tool and color, draw on the grid. Add frames with +, duplicate with ⧉, delete with −. Toggle onion skinning. Adjust FPS in preview. Click "Export Sprite Sheet" to download.
