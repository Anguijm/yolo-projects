# Tension Matrix

Interactive cloth simulation with Verlet integration. Grab, drag, toss, and tear a physics-driven fabric mesh. Tension-based dynamic coloring shifts from cyan to magenta as stress increases.

## Features

### Physics Engine
- Verlet integration for position-based dynamics (no velocity storage needed)
- Structural constraints (horizontal + vertical springs)
- Weighted constraint relaxation (free point takes full correction when neighbor is pinned)
- Configurable iteration count for stiffness control
- Friction damping on velocity
- Boundary collision (floor, walls)

### Interaction
- **Drag**: Left-click grabs nearest point, moves with cursor
- **Toss**: Release to throw — velocity applied from mouse movement
- **Cut**: Shift+drag or right-click drag — line intersection severs constraints
- **Pin preservation**: Dragging a pinned point restores its pin state on release (curtain doesn't fall)

### Visuals
- Tension-based HSL coloring: cyan (200°) at rest → magenta (320°) under stress
- Line width increases at high tension
- Spark particles on constraint snap (tear)
- Trail effect via semi-transparent canvas clear
- Pinned points shown as small squares

### Controls
- Gravity slider (0-2)
- Wind slider (0-1.5) — oscillating sine-based force
- Tear resistance slider (1.5-8x resting distance)
- Stiffness slider (1-8 constraint iterations)
- Presets: Default (pinned every 6), Curtain (full top row), Swing (corners only)

### Architecture
- ~45x30 mesh (~1400 points, ~2700 constraints)
- Zero external assets
- Single-file HTML
- Glassmorphism auto-hiding control panel
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Drag release unpinned structurally pinned points (curtain fell) — now restores basePinned state
- Constraint relaxation used fixed 0.5 weight (incorrect when one point pinned) — weighted by pin status
- Tension color math divided by zero when tearDist=1 — added Math.max(0.001, ...) guard

## How to Run

Open `index.html`. Grab the cloth and drag it around. Shift+drag to cut. Right-click to cut. Try the presets. Adjust physics with the sliders. Tear it apart.
