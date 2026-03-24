# ASCII Forge

Photo to ASCII art converter. Upload an image, convert to text art with multiple character sets, color mode, and adjustable resolution. Copy or download the result.

## Features

### Conversion Engine
- Luminance-based character mapping (BT.601: 0.299R + 0.587G + 0.114B)
- Brightness and contrast pre-processing
- Aspect ratio correction (0.5x height) for monospace font proportions
- Even character distribution (lum/256 × charset.length, not biased toward endpoints)
- HTML entity escaping in color mode (<, >, &, " safely rendered)

### Character Sets
- Standard (70 chars — full density range)
- Minimal (10 chars — clean look)
- Blocks (Unicode block elements — solid fill)
- Binary (0 and 1 — Matrix aesthetic)
- Braille (Unicode braille — ultra-high density dots)

### Modes
- Monochrome (terminal green on black)
- Full Color (each character colored by source pixel RGB)
- Invert toggle (reverse character mapping for light backgrounds)

### Controls
- Width slider (30-200 characters)
- Brightness slider (-80 to +80)
- Contrast slider (0.5x to 3x)
- Character set selector
- Color and invert toggles

### Export
- Copy as plain text (clipboard API + fallback)
- Download as PNG (text rendered to offscreen canvas)
- Sample image for instant demo

### Architecture
- Canvas-based pixel sampling via getImageData
- Debounced re-conversion (60ms) for smooth slider interaction
- Drag-and-drop + click-to-upload file input
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- HTML injection in color mode: charset contains <, >, & which broke DOM when inserted via innerHTML — added entity escaping
- Character index distribution biased (last character only selected at lum=255) — changed to lum/256 × length for even buckets

## How to Run

Open `index.html`. Click Sample to see a demo, or upload your own photo. Adjust character set, width, brightness, and contrast. Toggle color mode. Copy the text or download as PNG.
