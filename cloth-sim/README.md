# Cloth Sim

Interactive cloth physics simulator using Verlet integration. Drag, tear, pin, and blow fabric in real-time.

## Features

- **Verlet integration** with constraint satisfaction for realistic cloth behavior
- **4 tools**: Drag (move cloth), Tear (rip fabric), Pin (fix points), Unpin (release points)
- **Tension-colored wireframe** — blue=relaxed, white=normal, red=about to tear
- **Image texture mapping** — upload any image to drape it onto the cloth mesh (affine-transformed triangles)
- **Wind with turbulence** — sine-wave variation for organic cloth movement
- **4 presets**: Curtain, Flag, Hammock, Web
- **Fixed-timestep physics** for framerate independence (consistent on 60Hz and 144Hz)
- **Keyboard shortcuts**: D/T/P/U for tools, R for reset
- **Mobile-first** with pointer events and responsive layout

## How to Run

Open `index.html` in a browser.

## What I'd Change

- Add diagonal constraints for shear resistance
- Implement cloth self-collision
- Add WebGL rendering for larger meshes
- Add undo for tear operations
