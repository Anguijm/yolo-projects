# Wire Forge

Pure software 3D wireframe renderer. No WebGL — all 3D math computed from scratch using Canvas2D. Rotate polyhedra with mouse drag, scroll to zoom.

## Features

### 3D Engine (Pure Math)
- Rotation matrices (X, Y, Z Euler angles)
- Perspective projection (FOV-based, configurable)
- Painter's algorithm z-sorting (far edges drawn first)
- Z-depth coloring (near = bright cyan, far = dim purple)
- Angle wrapping prevents float precision loss over time

### Shapes (7 models)
- **Platonic solids:** Cube, Tetrahedron, Octahedron, Icosahedron, Dodecahedron
- **Parametric:** Torus (ring segments × tube segments), Sphere (lat × lon grid)
- Golden ratio (φ) used for icosahedron/dodecahedron vertex computation

### Interaction
- Drag to rotate on X/Y axes
- Scroll wheel to zoom (adjusts FOV)
- Auto-spin toggle with configurable speed
- Show/hide vertex dots
- Depth coloring toggle

### Visual
- Neon wireframe on deep black
- Line width scales with depth (near = thick, far = thin)
- Vertex alpha scales with depth
- 60fps Canvas2D rendering

### Architecture
- Zero external dependencies (no Three.js, no WebGL)
- All projection/rotation is custom math
- Single-file HTML, OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Painter's algorithm sorted ascending (drew near edges first, far on top) — reversed to descending
- Depth coloring inverted (far edges bright, near dim) — inverted t value: t = 1 - (z-min)/(range)
- Rotation angles grew infinitely — wrapped with modulo 2π

## How to Run

Open `index.html`. Select a shape. Drag to rotate. Scroll to zoom. Toggle auto-spin, vertex display, and depth coloring.
