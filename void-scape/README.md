# Void Scape

Generative ambient engine with Euclidean polyrhythms. Four concentric orbital rings play FM-synthesized plucks through an algorithmic delay reverb, creating evolving ambient soundscapes. Canvas visuals react to the audio.

## Features

- 4 concentric rings with independent Euclidean rhythm patterns
- Bjorklund/Bresenham algorithm distributes pulses evenly across steps
- FM synthesis plucks (sine carrier + high-ratio sine modulator) for bell-like tones
- Frequencies quantized to C Lydian scale across 3 octaves
- Algorithmic ping-pong delay reverb (cross-fed delay network with LP filters)
- Lookahead audio scheduler decoupled from visual framerate
- Canvas visuals: orbital nodes with glow-on-trigger, sweeping playhead, audio-reactive center
- Adjustable steps (3-16) and pulses per ring, BPM control (40-180)
- Safe scheduling guard for tab-throttled timers
- Visual flash properly synced (clamps negative elapsed time)
- Glassmorphic auto-hiding controls
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Euclidean algorithm (recursive continued-fraction) produced empty patterns for some inputs — replaced with reliable Bresenham/modulo approach
- Visual flash fired before audio due to lookahead scheduling (negative elapsed) — added >= 0 clamp
- Tab throttling could schedule oscillators in the past — added Math.max(time, currentTime) guard

## How to Run

Open `index.html`. Click ENTER to start. Adjust steps and pulses per ring with the controls (hover bottom to reveal). Change BPM to alter tempo.
