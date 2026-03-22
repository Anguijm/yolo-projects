# Tile Painter

A 16x16 pixel art editor that tiles seamlessly. Paint a tiny pattern, see it repeated as a wallpaper in real-time. Download at phone resolution.

## Features

- 16x16 drawing grid with tap and drag-to-paint
- Live tiling preview (entire background repeats your pattern)
- rAF-debounced preview (toDataURL only runs once per frame, not per pointermove)
- 4 curated color palettes: Midnight, Matcha, Ember, Mono
- Eraser tool toggle
- Clear grid button
- Download wallpaper as PNG (device resolution, capped at 2048px)
- toBlob export (avoids URL length limits on large canvases)
- setPointerCapture for reliable drag even outside grid bounds
- touch-action: none on grid (prevents mobile scroll during draw)
- pointercancel handler (prevents stuck paint state)
- Glassmorphic editor panel over tiled preview
- image-rendering: pixelated for crisp pixel art scaling
- OLED black compatible, mobile-first, all PWA metas

## Improvements from Gemini Code Audit

- toDataURL called on every pointermove (massive lag) → rAF-debounced dirty flag
- toDataURL for wallpaper download (URL length limit) → toBlob + createObjectURL
- Missing setPointerCapture (drag outside grid = stuck state) → added with release
- No touch-action: none (mobile scroll interrupted drawing) → added to grid

## How to Run

Open `index.html` in a browser. Select a palette, paint on the grid, watch the background tile. Tap "Save PNG" for a wallpaper.

## What You'd Change

- Store palette indices instead of hex (palette switching updates all pixels)
- Mirror/symmetry drawing mode
- Half-drop repeat option
- Undo/redo
