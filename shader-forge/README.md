# shader-forge

Live GLSL fragment shader editor with real-time WebGL rendering. Zero dependencies, single HTML file.

## What it does

Type GLSL fragment shader code in the left pane, see it render on the GPU in real-time on the right. Built-in uniforms (`u_time`, `u_resolution`, `u_mouse`) enable animated, interactive shaders.

## Features

- Real-time WebGL compilation with 300ms debounce
- GLSL syntax highlighting (keywords, types, builtins, numbers, comments, swizzles)
- Line numbers, Tab indentation (with block indent support)
- 3 presets: plasma, raymarched sphere, moiré pattern
- Error console with adjusted line numbers
- URL hash sharing (base64-encoded shader source)
- Responsive layout (stacks on mobile)

## How to run

Open `index.html` in any modern browser. No server needed.

## Uniforms available

- `u_time` — seconds since page load (float)
- `u_resolution` — canvas size in pixels (vec2)
- `u_mouse` — normalized mouse position 0-1 (vec2)

## What to change

- Add more presets to the `PRESETS` object
- Add `u_frame` uniform for frame count
- Add multi-pass rendering for feedback effects
