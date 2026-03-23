# Type Forge

Typography sandbox with curated Google Fonts. Live preview with adjustable size, weight, line-height, and letter-spacing. Dark/light mode toggle and CSS export.

## Features

- 13 fonts: 10 curated Google Fonts (variable weight) + 3 system font stacks
- Contenteditable live preview — type directly in the preview area
- Real-time sliders: font-size (12-120px), font-weight (100-900), line-height (0.8-3.0), letter-spacing (-0.1 to 0.5em)
- CSS variables drive all typography properties
- Dark/light mode toggle for contrast testing
- Copy CSS button with clipboard API + fallback
- Async clipboard toast only on confirmed success
- NaN-safe parsing (isNaN check, not || operator, to allow zero values)
- Google Fonts loaded via CDN with variable font support
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Falsy zero bug: `parseInt(v) || default` treated 0 as falsy, snapping back to default (switched to explicit isNaN check)

## How to Run

Open `index.html`. Select a font from the dropdown, adjust sliders, type in the preview area. Toggle dark/light mode for contrast testing. Click "Copy CSS" to get the exact styles.
