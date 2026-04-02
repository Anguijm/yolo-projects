# Attractor Zoo

A 3D strange attractor particle explorer. 2000 particles trace six famous chaotic dynamical systems, rendered with additive blending for a nebula effect.

## How to Run

Open `index.html` directly in a browser. No server needed.

## What It Does

- **6 attractors**: Lorenz (butterfly), Rössler (spiral), Thomas (labyrinthine), Halvorsen (three-wing), Aizawa (torus), Chen (double-scroll)
- **2000 particles** integrated with RK4, all distributed along the attractor basin at init
- **3D rotation**: drag to orbit, auto-rotate toggle
- **Additive blending**: particles accumulate light — bright where they cluster, dark trails in sparse regions
- **Ambient sound**: optional drone chord (A1/E2/A2/E3 perfect fifths with delay reverb)
- **Speed control**: slider multiplies the integration timestep

## Controls

- **Drag** — rotate the attractor in 3D
- **Attractor buttons** — switch chaotic system
- **AUTO-ROT** — toggle continuous Y-axis rotation
- **RESET** — return to default view angle, reinit particles
- **SOUND** — toggle ambient drone
- **SPEED slider** — control simulation speed (affects dt multiplier)

## What I'd Change

- Add pinch-to-zoom for scale control
- Per-attractor audio pitch (map attractor name to a root note)
- Particle color by speed magnitude (requires storing velocity in buffer)
- WebGL backend for >10,000 particles
