# Reaction Diffusion

Gray-Scott reaction-diffusion simulator. Two virtual chemicals (A and B) diffuse and react to spontaneously produce animal-skin patterns, coral growth, fingerprints, maze labyrinths, and more.

## How to run

Open `index.html` in a browser. No server required.

## What it does

- **200×200 grid** running Gray-Scott equations at up to 8 simulation steps per frame
- **8 presets**: CORAL, MITOSIS, MAZE, ZEBRA, RIPPLE, WORM, SPOTS, PULSE — each a distinct region of the F/K parameter space
- **4 color maps**: MONO (greyscale), THERMAL (blue→red→white), ACID (black→purple→green→yellow), OCEAN (deep blue→cyan→white)
- **Paint on the canvas** — click/drag to inject B-chemical seeds, seeding new growth
- **Seed button** — scatter 10 random seeds across the current pattern
- **Save** — exports a 600×600 PNG of the current frame
- **FPS counter** — live render rate in the sidebar

## Controls

| Control | Description |
|---|---|
| Preset buttons | Switch to a named F/K parameter region |
| F slider | Feed rate (how fast A is replenished) |
| K slider | Kill rate (how fast B is removed) |
| Speed | Steps per frame (1-8) |
| Reset | Clear the grid and start with a center seed |
| Seed | Scatter 10 random B-seeds on the current pattern |
| Pause/Play | Freeze/resume simulation (painting still works while paused) |
| Save | Download the current frame as a 600x600 PNG |

## Technical notes

- Pure Canvas 2D — no WebGL, no external dependencies
- Float32Array double-buffer swap (zero per-frame GC)
- Uint32Array view over ImageData for single-write-per-pixel rendering
- Toroidal (wrap-around) boundary conditions
- 3x3 Laplacian kernel: corners=0.05, edges=0.20, center=-1.00
