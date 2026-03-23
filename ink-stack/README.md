# Ink Stack

Canvas drawing app with stroke-based undo/redo. Smooth bezier curves, curated color palette, and PNG export. Strokes are stored as vector data, not pixel snapshots.

## Features

- Smooth freehand drawing with quadratic bezier curve interpolation
- Stroke-based undo/redo stacks (not pixel snapshots — lightweight and precise)
- Ctrl+Z / Ctrl+Y (Cmd+Z / Cmd+Shift+Z on Mac) keyboard shortcuts
- Baked canvas for strokes beyond history limit (oldest strokes preserved visually)
- 7-color curated palette + custom color picker
- Adjustable brush size (1-30px)
- Stack depth indicator
- Clear canvas and Save as PNG
- High-DPI canvas rendering (devicePixelRatio scaling)
- Pointer capture for smooth drawing beyond canvas edges
- pointercancel discards interrupted strokes (not saved as partial)
- Redo stack cleared on new stroke (branching history model)
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- MAX_HISTORY shift caused oldest strokes to vanish from screen — implemented baked canvas for permanent stroke preservation
- pointercancel saved partial interrupted strokes — now discards them

## How to Run

Open `index.html`. Draw with mouse or touch. Use the palette to pick colors, slider for brush size. Undo/Redo with buttons or Ctrl+Z/Y. Save your drawing as PNG.
