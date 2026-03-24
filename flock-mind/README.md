# Flock Mind

Boid flocking simulation with separation, alignment, and cohesion. 600+ autonomous agents form organic swarms, schools, and flocks. Predator mode scatters the flock from your cursor.

## Features

### Flocking Behavior
- 3 classic boid rules: separation (avoid crowding), alignment (match neighbor velocity), cohesion (steer toward group center)
- 4 color groups — alignment and cohesion apply within groups, separation applies to all
- Inverse-distance separation (stronger repulsion when closer, not constant)
- Two-pass update (calculate all forces first, then apply — prevents directional drift)
- Minimum speed enforcement prevents dead/stalled boids

### Interaction
- Click canvas to attract all boids toward cursor
- Predator mode toggle: cursor repels boids (with visual radius indicator)
- Scatter button randomizes all velocities
- Phantom mouse guard: -9999 initialization doesn't wrap to visible position

### Controls
- Count slider (100-1500 boids)
- Separation, alignment, cohesion weight sliders
- Max speed and view range sliders
- Reset and scatter buttons

### Rendering
- Oriented triangles (pointed in velocity direction) — boids look alive
- Batch rendering by color group (single beginPath per group)
- Trail effect via semi-transparent canvas clear
- Toroidal wrap (boids wrap around edges)

### Architecture
- Float32Array SoA layout for positions/velocities
- O(N²) with wrap-distance optimization
- Zero external dependencies, single-file HTML
- Glassmorphism auto-hiding panel
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- In-place update caused directional drift (boids saw partially updated state) — split into two-pass: calculate forces, then apply
- Phantom predator: mouse at -9999 wrapped to visible canvas position via toroidal math — added mouseX > -1 guard
- Separation force was constant regardless of distance — switched to inverse-distance (dx/d²)
- Zero velocity boids stalled forever — added random nudge when speed hits exactly 0

## How to Run

Open `index.html`. Watch the flocks self-organize. Adjust sliders. Click to attract, toggle Predator mode to scatter. Hit Scatter for chaos.
