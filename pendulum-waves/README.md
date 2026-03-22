# Pendulum Waves

A row of pendulums with incrementally different lengths creates mesmerizing wave patterns as they go in and out of phase. Optional audio tones on zero-crossings. Single HTML file, zero dependencies.

## Features

- N pendulums with incrementally increasing lengths (period proportional to sqrt of length)
- Adjustable: count (5-30), length spread, damping, gravity, amplitude, trail opacity
- Sub-stepped physics (4 steps/frame) for stability
- Color-coded bobs with HSL rainbow (hue mapped to position)
- Motion trails with fading alpha
- Bob glow effect (canvas shadowBlur)
- Optional pentatonic audio: tones trigger when pendulums cross center
- Octave-shifted frequencies for 10+ pendulums (prevents phasing from identical notes)
- Reset button, keyboard shortcuts (R=reset, A=audio, Space=reset)
- Responsive canvas with automatic pendulum re-initialization on resize
- DynamicsCompressor on audio master bus

## Bugs Fixed by Gemini Code Audit

- prevSign hardcoded to 1 regardless of initial amplitude sign (caused audio burst on first frame)
- Resize didn't re-init pendulums (pendulum lengths based on old window height)
- Audio frequencies wrapped at 10 pendulums (now octave-shifts to prevent phasing)

## How to Run

Open `index.html` in a browser. Pendulums start swinging immediately.

## What You'd Change

- 3D perspective rendering
- Interactive pendulum dragging
- Physics scale factor slider (pixel-to-meter conversion)
- Record to GIF/video
