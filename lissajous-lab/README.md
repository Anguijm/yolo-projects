# Lissajous Lab

Oscilloscope-style Lissajous curve explorer. Glowing phosphor trails on a pitch-black canvas. Adjust frequency ratios and phase to create mesmerizing harmonic patterns.

## Features

- Real-time animated Lissajous curves: x = sin(a·t + δ), y = sin(b·t)
- Phosphor trail effect (semi-transparent fade simulates CRT persistence)
- 4 color modes: Phosphor Green, Amber, Cyan, Rainbow (hue cycling)
- Canvas shadowBlur glow for neon oscilloscope aesthetic
- Auto-phase toggle slowly rotates the pattern (creates 3D illusion)
- Adjustable: Freq X (1-12), Freq Y (1-12), Phase (0-2π), Decay speed
- White dot shows current pen position
- Clear button resets canvas
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Watch the curve draw with auto-phase. Adjust frequency ratios for different patterns (try 3:2, 5:4, 1:1). Change colors and decay speed.
