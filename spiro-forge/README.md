# Spiro Forge

Interactive spirograph generator. Watch mesmerizing mathematical curves draw themselves in real-time. Hypotrochoid and epitrochoid modes with gradient coloring and gear visualization.

## Features

### Math Engine
- Hypotrochoid (rolling inside): x = (R-r)cos(t) + d·cos((R-r)/r·t)
- Epitrochoid (rolling outside): x = (R+r)cos(t) - d·cos((R+r)/r·t)
- Automatic rotation count via GCD calculation (curve closes perfectly)
- Parametric equations compute exact x,y for any angle theta

### Animation
- Real-time animated drawing (watch the pen trace the curve)
- Instant draw mode (complete shape rendered immediately)
- Adjustable speed (1-30)
- Progress percentage and rotation count display

### Visualization
- Gradient hue shift along curve (rainbow coloring)
- Flat cyan mode for clean single-color curves
- Gear visualization toggle (shows fixed circle, rolling circle, pen arm)
- Adjustable line width (0.5-4px)

### Presets
- Classic Flower — elegant inner curve
- Star Burst — wide inner pattern
- Fine Lace — many-petaled delicate pattern (small r)
- Atomic Orbit — outer epitrochoid
- Bloom — large pen offset creates loops
- Wild Spiral — chaotic epitrochoid

### Controls
- R (fixed circle radius: 50-250)
- r (rolling circle radius: 5-150)
- d (pen offset: 5-200)
- Speed, line width sliders
- Hypotrochoid/epitrochoid toggle
- Gear visualization toggle
- PNG export

### Architecture
- Canvas-rendered with per-segment HSL coloring
- GCD-based rotation calculation for perfect loop closure
- Zero external dependencies, single-file HTML
- Glassmorphism auto-hiding panel
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Watch the default curve draw itself. Select presets for instant beautiful patterns. Adjust R, r, d sliders to discover new shapes. Toggle epitrochoid mode. Enable gear visualization to see the rolling mechanism.
