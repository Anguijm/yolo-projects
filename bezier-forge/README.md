# Bezier Forge

Interactive CSS cubic-bezier easing editor. Drag control point handles to design custom animation timing, preview in real-time, and copy the CSS with one click.

## Features

### Curve Editor
- SVG-based interactive coordinate grid
- Two draggable P1/P2 bezier control point handles
- Real-time cubic bezier curve rendering
- X-axis clamped to 0-1 (CSS spec requirement)
- Y-axis allows -1 to 2 for bounce/overshoot effects
- Handle lines from endpoints show control arm direction
- Linear reference line for comparison

### Animation Preview
- Ball animates across track using custom easing
- Ghost ball runs simultaneously with linear easing for comparison
- Configurable duration (200ms to 3000ms)
- Play button triggers animation

### Presets
- ease, ease-in, ease-out, ease-in-out
- back (overshoot), bounce-ish, snap, linear
- Click preset to apply and auto-play preview

### CSS Output
- Live updating cubic-bezier(x1, y1, x2, y2) string
- Click to copy to clipboard
- Coordinate display (P1, P2 values)

### Architecture
- SVG for crisp vector rendering of curve and handles
- CSS transition on preview elements (not JS animation)
- Pointer events with setPointerCapture for smooth dragging
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Drag the cyan handles on the curve editor. Watch the animation preview update. Select presets for common easings. Click the CSS output to copy. Adjust duration with the slider.
