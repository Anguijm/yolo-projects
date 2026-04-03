# css-units

CSS Length Unit Converter — offline, zero-dependency, single HTML file.

## What it does

Convert any CSS length value between all major CSS length units instantly:

- **Absolute**: px, pt, pc, cm, mm, in
- **Root-relative**: rem
- **Parent-relative**: em, %
- **Viewport**: vw, vh, vmin, vmax
- **Dynamic viewport**: dvh, dvw, svh, svw, lvh, lvw
- **Character** (approximate): ch, ex

Features:
- Type a value, select a unit → all conversions update live
- Click any result row to copy as a CSS value (e.g. `1.5625rem`)
- Context panel: set base font size, parent font size, and viewport dimensions for accurate relative unit math
- Device presets: iPhone SE, iPhone 14, iPad, Laptop, Desktop, 4K — click to load viewport dimensions
- Pixel ruler: visual bar showing the physical pixel size relative to the panel
- Keyboard: press `C` to copy the current value
- Persists context settings in localStorage

## How to run

Open `index.html` directly in any browser. No server needed.

## Customization

- Edit `VP_PRESETS` in the `<script>` block to add/remove device presets
- Edit `UNIT_GROUPS` to reorder or hide unit categories
- Change `--accent` in `:root` to switch the highlight color
