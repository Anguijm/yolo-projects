# Interval Timer

A hyper-sensory HIIT/Tabata/circuit workout timer. Massive countdown numbers, synthesized audio cues, haptic patterns, screen wake lock. Mobile-first PWA.

## Features

- 4 presets: Tabata (20/10x8), HIIT (40/20x6), Circuit (45/15x10), Equal (30/30x8)
- Custom work/rest/rounds with input validation (no negative values)
- Massive viewport-filling countdown number
- Phase states: GET READY (3s countdown), WORK (cyan), REST (amber), DONE (green)
- Absolute-time countdown (Date.now() based) — accurate even when backgrounded
- Synthesized audio cues: work start (ascending notes), rest start, countdown ticks, done arpeggio
- Done arpeggio scheduled via audioCtx.currentTime (reliable when backgrounded)
- Haptic choreography: heartbeat in last 3 seconds, snap on work start, triple buzz on done
- Tap anywhere to pause/resume, tap on DONE to return
- Screen Wake Lock with release listener and visibilitychange re-acquisition
- AudioContext resume on visibility change (handles OS suspension)
- Double-start guard prevents overlapping rAF loops
- Round counter: "Round 3 / 8"
- OLED black background with subtle phase color shifts
- Mobile-first: viewport meta, apple-mobile, theme-color, touch-action

## Bugs Fixed by Gemini Code Audit

- Timer paused in background (dt=0 cap killed the countdown) — switched to Date.now() absolute timing
- Double-speed from dual pointerdown+click firing startTimer twice (added running guard)
- Negative number inputs bypassed || fallback (added proper validation with isNaN + min check)
- playDone used setTimeout (throttled in background) — switched to audioCtx.currentTime scheduling

## How to Run

Open `index.html` on your phone. Tap a preset or customize, then START.

## What You'd Change

- Exercise name display per round
- Rest skip button
- Total workout time estimate
- Session history with localStorage
