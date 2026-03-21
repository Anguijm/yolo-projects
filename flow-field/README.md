# Flow Field

Audiovisual generative art sandbox. Place emitters to release particle streams that follow mathematical flow fields. Attractors create gravity wells that trigger ambient pentatonic synth notes. Single HTML file, zero dependencies.

## Features

- 8000 particles in Float32Array (zero GC, stride-based access)
- 4 flow field types: Noise, Spiral, Converge, Turbulent
- Custom Perlin noise implementation (no libraries)
- Place emitters (click), attractors (Shift+click), repulsors (Alt+click)
- Attractors trigger pentatonic notes based on particle density + Y position
- Web Audio with DynamicsCompressor, 8-voice polyphony limit, ADSR envelopes
- Long-exposure visual effect (semi-transparent fade + additive blending)
- 5 curated palettes: Neon Tokyo, Abyssal Glow, Infrared, Aurora, Monochrome
- Save as PNG (S key)
- Cycle palettes (Space), field types (F), clear (C)
- Immersive full-screen canvas, controls fade after 6s

## How to Run

Open `index.html` in a browser. Click to place emitters. Shift+click for gravity wells.

## What You'd Change

- Touch/mobile support (gesture-based placement)
- Stereo panning based on attractor X position
- More field types (magnetic dipole, reaction-diffusion)
- Record to video/GIF
