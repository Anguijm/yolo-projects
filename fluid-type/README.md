# Fluid Type

Navier-Stokes fluid simulation with typography as obstacles. Text letterforms act as solid boundaries — dye bleeds from their edges and swirls when you drag to inject velocity. Type to change the text in real-time.

## Features

- Jos Stam "Stable Fluids" Navier-Stokes solver on 128x128 grid
- Text rendered as obstacle boundaries in the fluid grid
- Dye continuously emits from text edges in the selected color
- Drag/swipe to inject velocity and dye — fluid crashes around the letters
- RGB dye channels for full-color mixing
- 4 color palette swatches (cyan, magenta, green, amber)
- Type custom text via hidden input (tap canvas to focus keyboard)
- 5 preset words (FLUID, FLOW, CHAOS, DREAM, WAVE)
- Low-res fluid scaled to full screen with bilinear smoothing
- OLED black, mobile-first, pointer events for touch

## How to Run

Open `index.html`. Drag your finger or mouse across the screen to inject fluid flow. Watch the dye bleed off the letters and swirl around them. Tap the canvas and type to change the text. Pick colors from the palette.
