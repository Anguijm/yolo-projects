# Word Garden

Type any word or name. Watch it grow into a unique procedural tree. Each word creates a completely different plant. Save as wallpaper.

## Features

- Deterministic generative trees — same word = same tree every time
- Seeded PRNG (mulberry32) for infinite reproducible entropy from any string
- Recursive branching with quadratic bezier curves (organic, not rigid)
- 8 curated color palettes selected by word hash
- Character DNA: word hash determines branch angle, decay, spread, curvature, asymmetry, max depth
- Growth animation sorted by depth (breadth-first = natural bottom-up growth)
- Leaf/bloom nodes at terminals with glow (shadowBlur)
- Branch count capped at 15,000 to prevent CPU freeze on extreme seeds
- Debounced text input (400ms) and debounced window resize (200ms)
- Save as PNG with word name in filename
- Auto-focus input on load
- OLED black, mobile-first, all PWA metas, click events only

## Improvements from Gemini Code Audit

- Branches sorted by depth for natural growth animation (was depth-first = awkward)
- Branch cap at 15,000 prevents CPU freeze (maxDepth 10 + 3-way branching = 88K theoretical)
- Resize debounced to prevent mobile keyboard resize glitch

## How to Run

Open `index.html` in a browser. Type a name. Watch it grow.

## What You'd Change

- Gentle sway animation on finished tree (sine-wave vertex displacement)
- Ambient generative chord per word (Web Audio)
- Share as image to social media
- Gallery of saved word-gardens
