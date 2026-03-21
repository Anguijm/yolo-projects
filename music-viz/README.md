# Music Visualizer

Real-time audio visualizer with 5 modes, using Web Audio API. Single HTML file, zero dependencies.

## Features

- Microphone input or audio file upload
- 5 visualization modes:
  - Frequency Bars with reflections
  - Waveform with glow effect
  - Circular Spectrum with inner glow
  - Particle Burst with bass pulse ring
  - Mountain Range (frequency history)
- Sensitivity and smoothing sliders
- Play/pause controls for uploaded audio
- Responsive fullscreen canvas

## How to Run

Open `index.html` in a browser. Click "Microphone" or load an audio file.

## What You'd Change

- WebGL shaders for GPU-accelerated visuals
- Particle object pooling for zero-GC
- Beat detection for synchronized effects
