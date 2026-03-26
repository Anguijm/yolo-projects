# Zenodoro

Pomodoro focus timer with SVG progress ring, dynamic color themes, session tracking, and synthesized audio chime. Timestamp-based timing immune to background tab throttling.

## Features

- SVG circular progress ring with smooth animation
- Work (25m), Short Break (5m), Long Break (15m after 4 sessions)
- Timestamp-based timing using Date.now() — accurate even in background tabs
- Dynamic color themes: red for focus, green for short break, blue for long break
- Session dots showing progress toward long break
- Synthesized chime via Web Audio API on completion
- Device vibration on timer end (mobile)
- Screen Wake Lock API keeps display on during focus
- Re-acquires wake lock on tab return via visibilitychange
- Customizable durations with persistence
- Daily session counter saved to localStorage
- Mobile-first, centered layout

## How to Run

Open `index.html`. Press Start to begin a 25-minute focus session. The ring counts down and the screen stays awake. When it ends, a chime plays and it auto-switches to break mode. Complete 4 work sessions for a long break.
