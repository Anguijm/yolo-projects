# Color Forge

Color harmony generator with HSL wheel visualization. Pick a seed color and generate complementary, analogous, triadic, split-complementary, and monochromatic palettes. Click swatches to copy hex values.

## Features

- 5 harmony modes: complementary, analogous, triadic, split-complementary, monochromatic
- Canvas HSL color wheel with positioned harmony nodes
- Seed color via hex input (3 or 6 char, with or without #), native color picker, or H/S/L sliders
- All inputs synced bidirectionally in real-time
- Palette swatches with dynamic text contrast (light/dark based on luminance)
- Click swatch or CSS export to copy to clipboard
- CSS variable export (:root { --color-1: #hex; ... })
- Clipboard API with textarea fallback, toast only on confirmed success
- Seed preview swatch
- Dark mode UI, OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Clipboard toast showed even when copy failed (async writeText can reject) — now only toasts on .then() success
- Hex input regex too strict (required # and exactly 6 chars) — now accepts 3-char hex and optional #

## How to Run

Open `index.html`. Pick a color using the hex field, color picker, or HSL sliders. Select a harmony mode. Click any swatch to copy its hex value. Click the CSS export block to copy all variables.
