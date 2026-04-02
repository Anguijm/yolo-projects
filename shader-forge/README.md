# Shader Forge

Live GLSL fragment shader playground in the browser. Edit code, see it render in real-time via WebGL. No dependencies, fully offline.

## How to run

Open `index.html` in any browser with WebGL support. No server needed.

## What it does

- **Live editor**: Write GLSL fragment shader code in the left panel
- **Real-time rendering**: WebGL renders your shader on the right canvas at 60fps
- **8 presets**: Mandelbrot set, Julia set, Voronoi noise, Plasma, FBM noise, Kaleidoscope, Raymarching (metaballs), Domain Warp
- **Auto-compile**: Shader recompiles 1.2s after you stop typing, or instantly with Ctrl+Enter
- **Error display**: GLSL compilation errors shown with adjusted line numbers (preamble offset removed)
- **Pause/Resume**: Freeze u_time for static inspection
- **Screenshot**: Export current frame as PNG (uses toBlob + preserveDrawingBuffer)
- **Time reset**: Jump u_time back to 0
- **HiDPI aware**: Canvas renders at devicePixelRatio resolution
- **Mobile**: Touch controls update u_mouse; responsive layout stacks vertically

## Built-in uniforms

Every shader automatically has access to:

```glsl
uniform float u_time;       // seconds elapsed
uniform vec2 u_resolution;  // canvas size in pixels
uniform vec2 u_mouse;       // mouse position normalized 0-1
```

## Keyboard shortcuts

- `Ctrl+Enter` — compile immediately
- `Tab` — insert 2 spaces (triggers auto-compile)

## What to change

- Add more presets to the `PRESETS` object in the script
- Add a custom uniform UI (sliders that inject `#define` values into the preamble)
- Add syntax highlighting via a custom overlay or a small tokenizer
