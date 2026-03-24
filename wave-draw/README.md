# Wave Draw

Draw your own waveform and play it as a synthesizer. Sketch a shape on the canvas, and it becomes the sound source for a playable keyboard. DFT converts your drawing into a PeriodicWave in real-time.

## Features

### Waveform Drawing
- Full-width drawing canvas — sketch any waveform shape
- Interpolated drawing (fills gaps between pointer samples)
- Real-time DFT (Discrete Fourier Transform) converts drawing to Fourier coefficients
- PeriodicWave created from extracted real/imaginary components
- Presets: sine, square, sawtooth, or draw your own

### Synthesizer
- 13-note keyboard (C4 to C5) playable via mouse/touch or QWERTY keys
- Custom PeriodicWave applied to every note
- ADSR envelope with configurable attack and release
- setTargetAtTime for click-free release (no exponentialRamp from zero)
- osc.stop(time) scheduling on audio thread (not setTimeout)
- onended cleanup prevents memory leaks
- Feedback delay effect with LP filter for spatial sound

### Visual Feedback
- Real-time oscilloscope (AnalyserNode time domain data)
- Waveform preview on drawing canvas
- Keyboard press visual feedback

### Controls
- Attack time slider (5ms to 500ms)
- Release time slider (50ms to 2s)
- Delay amount slider (0 to 0.6)
- Preset waveform buttons + Clear

### Architecture
- DFT computed from 256-sample waveform → 128 Fourier harmonics
- Web Audio: Oscillator → Gain (envelope) → Master → Delay feedback → Destination
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- playNote checked audioCtx before calling initAudio (first note silently failed) — moved initAudio() before the check
- setTimeout used for oscillator cleanup (unreliable in background tabs) — switched to osc.stop(time) + onended
- activeNotes cleanup via onended with reference comparison (prevents rapid-retrigger bugs)

## How to Run

Open `index.html`. Draw a waveform shape on the canvas. Play it using the on-screen keyboard or QWERTY keys (A=C, W=C#, S=D...). Adjust attack, release, and delay. Try the presets, then draw something wild.
