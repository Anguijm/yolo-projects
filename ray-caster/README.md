# Ray Caster

A Wolfenstein 3D-style first-person raycasting engine in a single HTML file. No dependencies, no build step.

## Features

- DDA raycasting with fisheye correction
- Procedural brick textures (8 wall types, sine-wave noise)
- WASD + mouselook + sprint movement with wall sliding
- Head bobbing with smooth decay
- Minimap with player dot and FOV cone (offscreen-cached)
- Live map editor (click to place walls, right-click to erase)
- Fog and texture toggles
- FOV, view distance, and speed sliders
- FPS counter
- Pause on ESC / pointer lock release

## How to Run

Open `index.html` in any modern browser. Click the viewport to capture the mouse.

## What You'd Change

- Add sprites/enemies (needs a 1D depth buffer per column)
- Textured floors/ceilings
- Map import/export in the editor
- Sound effects
