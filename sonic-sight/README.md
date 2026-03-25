# Sonic Sight

Interactive sound wave synthesizer with real-time oscilloscope and spectrum analyzer. Mix 4 oscillators, see waveforms and frequency spectra animate live. Guided lessons teach the fundamentals of sound — from sine waves to additive synthesis to beating.

## Features

- 4 independent oscillators (sine, square, sawtooth, triangle)
- Per-oscillator frequency (20-2000 Hz) and volume sliders
- Real-time oscilloscope waveform display with CRT-style grid
- Real-time FFT frequency spectrum analyzer
- 8 guided lessons: sine waves, pitch, square waves, additive synthesis, sawtooth, octaves, beating, free exploration
- Each lesson auto-configures oscillators to demonstrate the concept
- Master volume control
- Web Audio API with AudioContext resume for iOS/Safari compatibility
- Smooth parameter updates via setTargetAtTime (no zipper noise)
- OLED black oscilloscope aesthetic, mobile-first

## How to Run

Open `index.html`. Tap to unlock audio. Press Play to hear the default sine wave. Click Lessons for a guided tour of sound wave fundamentals. Toggle oscillators on/off, change wave types, adjust frequencies and volumes.
