# Glitch Studio

Pixel sorting and chromatic aberration tool for generative glitch art. Drop an image, sort pixels by luminance thresholds, and apply RGB channel shifts.

## Features

- Drag-and-drop or tap-to-upload image input
- Pixel sorting by luminance threshold band (adjustable min/max)
- Horizontal and vertical sort directions
- Chromatic aberration (RGB channel offset)
- Uint32Array pixel manipulation for performance
- Vertical sort via transpose-sort-transpose
- SMPTE test pattern on load with pre-applied glitch demo
- Image export via toBlob (no URL length limits)
- Threshold sliders auto-clamp to prevent crossing
- Resolution capped at 1080px for performance
- Brutalist dark UI, OLED black, mobile-first

## Bugs Fixed by Gemini Audit

- UI desync on init: canvas showed aberration=8 but slider said 0 (now UI matches applied values)
- Threshold sliders could cross (lower > upper), silently disabling pixel sort (now auto-clamped)
- Missing dragenter preventDefault allowed browser to navigate away on drop
- sortRow used Array.push in hot loop causing GC pressure (switched to Uint32Array)

## How to Run

Open `index.html`. See the pre-glitched SMPTE test pattern. Drop your own image, adjust thresholds and aberration, click Sort. Save the result.
