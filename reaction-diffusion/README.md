# Reaction Diffusion Explorer

GPU-accelerated Gray-Scott reaction-diffusion simulation. Two virtual chemicals (A and B) react and diffuse across a canvas, producing organic Turing patterns — coral, worms, mazes, spots — depending on the feed and kill rate parameters.

## How to Run

Open `index.html` in Chrome or Firefox. Requires WebGL2 (or WebGL1 with float framebuffer extension).

## What It Does

- **Real-time simulation** running in a WebGL fragment shader — no CPU, pure GPU math
- **8 presets** for classic Turing pattern types: Coral, Mitosis, Maze, Worms, Spots, Solitons, Bacteria, Waves
- **Interactive brush** — click/drag on the canvas to inject chemical B and create disturbances that evolve into patterns
- **8 color palettes** — each maps the B concentration to a different aesthetic
- **Live parameter sliders** — feed rate, kill rate, brush size, simulation speed (steps/frame)
- **Keyboard shortcuts**: Space=pause, R=reset, S=save screenshot, 1-8=preset, +/-=brush size, [/]=speed

## Technical Details

- Gray-Scott model: `dA/dt = Da∇²A - AB² + f(1-A)` and `dB/dt = Db∇²B + AB² - (f+k)B`
- Ping-pong framebuffer technique: two float textures, each frame reads from one and writes to the other
- Tries WebGL2 first (with `EXT_color_buffer_float`), falls back to WebGL1 + `WEBGL_color_buffer_float`
- Simulation runs at 50% canvas resolution for performance; display upscales with linear filtering
- `steps/frame` slider runs the simulation N times per animation frame for faster pattern growth

## What to Change

- **DPR / resolution**: Adjust `simScale` (default 0.5) for quality vs. performance
- **Add more presets**: Any (f, k) point from Karl Sims' famous parameter map will work
- **Add noise brushes**: Inject random B values in a ring shape for spiral patterns
