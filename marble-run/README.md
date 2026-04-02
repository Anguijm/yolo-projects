# Marble Run

Physics-based marble simulator. Draw ramps with your mouse, drop marbles, watch them cascade.

## How to run

Open `index.html` in any browser. No server needed.

## Controls

| Action | How |
|--------|-----|
| Draw ramp | Select **Draw** mode, click-drag on canvas |
| Erase | Select **Erase** mode, drag over elements |
| Place bumper | Select **Bumper** mode, click |
| Drop marble | **Space** or click **▼ Drop** button |
| Clear | **C** or toolbar buttons |

## Features

- Hand-rolled 2D physics: gravity, circle-vs-line-segment collision, circle-vs-circle collision
- Bumpers with restitution > 1 for pinball-style energy boost
- 3 substeps per frame for stable high-speed collisions
- Colorful marbles with glowing trails, radial gradient spheres
- Adjustable gravity, bounce coefficient, marble size
- 4 presets: Zigzag, Funnel, Pinball, Chaos
- Up to 80 simultaneous marbles with automatic overflow eviction

## Physics notes

- Wall collision: reflect velocity using outward normal, coefficient of restitution = `bounce` slider
- Bumper collision: restitution 1.05 (adds 5% energy, pinball feel)
- Marble-marble: elastic collision formula `(1 + e) * 0.5 * relative_normal_velocity`
- Air friction: `Math.pow(FRICTION, subDt * 60)` — frame-rate-independent decay
