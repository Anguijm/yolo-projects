# Wheel of Fate

A physics-driven spinning wheel for group decisions. Tap to spin, haptic ticks on each segment, dramatic landing. Mobile-first PWA.

## Features

- Canvas-rendered wheel with customizable options
- Physics-based spin: friction deceleration, random initial velocity
- Haptic tick (8ms vibration) and synthesized click on each segment boundary
- Tick cooldown (30ms) prevents vibration spam at high speed
- Celebratory arpeggio + triple haptic burst on landing
- Color-coded result display matching winning segment
- Duplicate-safe result coloring (uses segment index, not indexOf)
- Minimum wheel size (200px) prevents negative radius crash
- CSS pointer/flapper above canvas
- Edit modal: one option per line, textarea-based
- localStorage persistence for wheel options
- OLED black, mobile-first, viewport + apple-mobile meta
- Dual pointerdown + click events for iOS compatibility
- Spin guard prevents double-spin

## Bugs Fixed by Gemini Code Audit

- Result color used indexOf (broken with duplicate options) — now uses segment index
- No minimum wheel size — tiny windows could cause negative canvas arc radius crash

## How to Run

Open `index.html` on your phone. Tap the wheel or SPIN button.

## What You'd Change

- Swipe-to-spin with velocity from gesture speed
- Multiple saved wheel presets
- Confetti particle burst on landing
- Share result as image
