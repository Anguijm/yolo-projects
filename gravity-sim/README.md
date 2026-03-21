# Gravity Simulator

N-body gravity simulator with merging, trails, and presets. Single HTML file, zero dependencies.

## Features

- Click to spawn bodies, drag to set velocity
- 4 presets: Solar System, Binary Star, Star Cluster, Figure-8
- Particle merging with momentum conservation
- Fading trails that move correctly with camera
- Zoom to cursor, pan (middle-click or Alt+click)
- Sub-stepping physics for orbital stability
- Gravitational constant and time scale sliders
- Grid overlay, merge toggle
- Radial glow for massive bodies

## How to Run

Open `index.html` in any modern browser.

## What You'd Change

- Barnes-Hut quadtree for O(n log n) scaling
- GPU compute via WebGL for 10k+ bodies
- Save/load simulations
