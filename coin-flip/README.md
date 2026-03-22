# Coin Flip

Tap anywhere. The coin flips. That's it. Obsessively polished execution of the simplest possible app.

## Features

- CSS 3D coin with preserve-3d, backface-visibility hidden
- Cumulative rotation tracking (always spins forward, never backward)
- Custom cubic-bezier easing for weighty physics feel
- Synthesized metallic "clink" on flip (sine sweep 2400→800Hz)
- Synthesized "thud" on landing (sine sweep 200→80Hz)
- Haptic pattern on flip (flutter) and landing (thud)
- HEADS / TAILS result displayed after animation
- Last 20 flips shown as color-coded dots (white=H, tan=T)
- Running H/T ratio with percentages
- NaN-safe localStorage with negative number guard
- AudioContext.resume() promise catch (no unhandled rejection)
- Entire screen is tap target (no buttons)
- Hint fades after first flip
- OLED black, mobile-first, all PWA metas, click events only

## Improvements from Gemini Code Audit

- Backward spinning: absolute rotation from zero caused reverse animation. Fixed with cumulative rotation tracking.
- NaN in localStorage: tampered data could show NaN%. Added isNaN guard + Math.max(0).
- AudioContext.resume() promise: unhandled rejection in strict browsers. Added .catch().

## How to Run

Open `index.html` on your phone. Tap the coin. That's it.

## What You'd Change

- transitionend instead of setTimeout for animation sync
- Multiple coin types (dice, yes/no)
- Satisfying "catch" animation
- Share flip result
