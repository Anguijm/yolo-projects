# Sonic Reflex

Audio-visual reaction tester. A rising synth builds tension, then drops — click the instant the screen flashes. How fast are your reflexes? Single HTML file, zero dependencies.

## Features

- Synthesized audio tension: rising sine + LFO noise pumping + DynamicsCompressor
- Sharp "snap" drop sound (pitch-swept square wave)
- Full-screen white flash as visual trigger
- performance.now() for sub-millisecond timing accuracy
- pointerdown event for zero-delay input (no mobile tap delay)
- "Too Early" detection with red feedback
- Random 2-6 second delay prevents prediction
- Performance ranks: INHUMAN, ELITE, FAST, AVERAGE, SLOW, ASLEEP?
- Result chime using pentatonic frequencies (C5/E5/G5/C6)
- Statistics: best time, rolling average, total tries, rank
- Color-coded histogram (7 buckets)
- localStorage persistence across sessions
- Share button: copies score + rank to clipboard
- Photosensitivity warning
- Bluetooth latency note
- Click anywhere or press Space to interact
- Brutalist dark UI with giant monospace numbers

## How to Run

Open `index.html` in a browser. Click START. Wait for the drop.

## What You'd Change

- Latency calibration via metronome test
- Multiple game modes (audio-only, visual-only, pattern sequence)
- Global leaderboard via API
- Vibration feedback on mobile
