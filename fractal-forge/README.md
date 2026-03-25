# Fractal Forge

L-System fractal explorer. Define axioms and production rules, watch stunning fractals emerge from simple string rewriting. 6 classic presets + custom rule editor.

## Features

### L-System Engine
- String rewriting: axiom + production rules → iterated replacement
- Turtle graphics interpreter: F/G (draw), +/- (turn), [ ] (push/pop branch)
- Simultaneous replacement (new characters don't trigger rules until next iteration)
- String length cap (500K chars) prevents browser crash

### Auto-Fit Rendering
- Dry-run bounding box calculation (simulates turtle path without drawing)
- Auto-scale and center: fractal always fits perfectly in viewport
- No manual pan/zoom needed — works at any iteration count

### Visual
- Gradient color mode: hue shifts along drawing progress (red → blue spectrum)
- Flat cyan mode for clean single-color fractals
- Dynamic line width scaled to fractal complexity
- Round line caps for smooth appearance

### Presets
- **Koch Snowflake** — classic 60° snowflake
- **Dragon Curve** — space-filling curve
- **Sierpinski Triangle** — 120° triangular fractal
- **Barnsley Fern** — organic branching plant
- **Fractal Tree** — symmetric tree with 22° branching
- **Hilbert Curve** — space-filling curve with 90° turns

### Controls
- Angle slider (1°-180°)
- Iteration slider (1-10) with +/- buttons
- Custom axiom input
- Custom rules textarea (one per line: X=...)
- Gradient toggle
- Draw button for custom rules
- String length display

### Architecture
- Canvas-rendered turtle graphics
- Two-pass rendering: bounding box pass → scaled drawing pass
- Zero external dependencies, single-file HTML
- Glassmorphism auto-hiding panel
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Select a preset to see a classic fractal. Adjust angle and iterations with the sliders. Edit the axiom and rules for custom fractals. Toggle gradient coloring.
