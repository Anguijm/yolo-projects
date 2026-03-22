# dB — Sound Meter

A brutalist mobile sound level meter. Measure decibels around you with one tap. OLED black, big reactive typography, haptic alerts on dangerous noise levels.

## Features

- Real-time dB reading from microphone (Web Audio AnalyserNode)
- RMS-to-dB conversion with +94 dB SPL offset approximation
- Color-coded levels: Quiet (<40), Moderate (40-60), Loud (60-75), Very Loud (75-85), Dangerous (85+)
- Level bar showing current dB as percentage of range
- Stats: peak dB, rolling average, minimum
- Haptic vibration on dangerous threshold (85+ dB) with 1-second cooldown
- Screen Wake Lock API keeps screen on during monitoring
- AudioContext created synchronously before async getUserMedia (iOS compatibility)
- AudioContext resume on visibility change (handles OS background suspension)
- Double-start guard prevents overlapping streams
- Proper stream cleanup on stop (track.stop, context.close)
- OLED black (#000), mobile-first, viewport meta, apple-mobile meta
- Dual pointerdown+click event handling for iOS
- Reset button clears peak/avg/min stats

## Bugs Fixed by Gemini Code Audit

- iOS AudioContext created after async await (moved to synchronous, before getUserMedia)
- Vibration fired 60x/second when loud (added 1-second cooldown)
- No guard against double-starting (added running check)
- AudioContext not resumed after OS background suspension (added visibilitychange handler)

## How to Run

Open `index.html` on your phone (HTTPS required for microphone). Tap LISTEN.

## What You'd Change

- Microphone disconnect detection (stream track 'ended' event)
- Noise log with timestamps
- Configurable threshold with custom haptic patterns
- Frequency spectrum visualization
