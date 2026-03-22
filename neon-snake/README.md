# Neon Snake

Snake, but beautiful. Each segment is a different hue — the snake becomes a flowing gradient ribbon. Eating food plays escalating pentatonic notes. Canvas glow effects make it look like light painting.

## Features

- HSL gradient snake — hue cycles through segments + time for animated rainbow
- Canvas `globalCompositeOperation = 'lighter'` for neon bloom
- `shadowBlur` glow on every segment
- Alpha fades from head to tail
- Pulsing white glow on food
- Pentatonic notes on eat (sine + detuned triangle layered for shimmer)
- Pitch escalates with snake length
- Sawtooth death sound with pitch sweep
- Haptic on eat (15ms) and death (pattern)
- Swipe controls for mobile (touchstart + touchend delta)
- touchmove prevented during gameplay (no page scroll)
- Arrow keys for desktop (only game keys prevent default)
- Win state detection (snake fills entire grid)
- High score in localStorage
- Score display, game over overlay
- OLED black, mobile-first, all PWA metas
- Click events only, no pointerdown

## Bugs Fixed by Gemini Code Audit

- e.preventDefault() on ALL keydown (blocked F5, devtools) — now only arrow keys
- DOM query in 60fps render loop (removed redundant getElementById from loop)
- Page scrolls during swipe gameplay (added touchmove preventDefault)
- No win state (snake fills grid → spawnFood infinite loop) — added board-full check

## How to Run

Open `index.html` on your phone. Tap PLAY, swipe to steer.

## What You'd Change

- Input queue for rapid direction changes
- Particle decay on tail segments
- Speed acceleration as snake grows
- Wrap-around mode (walls become portals)
