# CSV Cinema

Drop a CSV file, watch your data perform as animated visualizations. Bar chart races, animated line charts, scatter morphs — auto-detected from your columns. Single HTML file, zero dependencies.

## Features

- Drag-and-drop CSV loading (or browse button)
- Auto-detects delimiter (comma, tab, semicolon)
- Auto-infers column types: time, categorical, numeric
- 3 chart types: Bar Chart Race, Animated Line, Scatter Plot
- Smooth bar position/value lerp for buttery animation
- Playback controls: play/pause, scrubber timeline, speed +/-
- Keyboard shortcuts: Space=play, Left/Right=step
- 3 built-in demo datasets: World Population, Stock Prices, Temperatures
- Manual "Remap Columns" fallback if auto-detect guesses wrong
- Dynamic HSL color generation for 50+ categories
- Top-15 bar filtering for large datasets
- XSS-safe DOM construction for user-supplied headers
- K/M/B number formatting
- Responsive canvas

## How to Run

Open `index.html` in a browser. Drop a CSV or click a demo.

## What You'd Change

- Web Worker for parsing large files (50MB+)
- More chart types (pie, treemap, area)
- Export to GIF/video
- Transition morphs between chart types
