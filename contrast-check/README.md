# Contrast Check

WCAG color accessibility checker with color blindness simulation. Pick foreground and background colors, see contrast ratio with AA/AAA pass/fail badges, preview how your colors look under different types of color blindness, and auto-fix failing combinations.

## Features

- Foreground/background color pickers with hex input
- WCAG 2.1 contrast ratio calculation (AA, AAA, AA Large)
- Live text preview showing selected colors
- Color blindness simulation: Normal, Protanopia (no red), Deuteranopia (no green), Tritanopia (no blue)
- Simulation uses Brettel/Vienot color matrix transforms with proper sRGB linearization
- Auto-fix button: adjusts foreground lightness to meet AA 4.5:1 ratio
- Palette contrast matrix: enter multiple hex colors, see all pairwise contrast ratios
- Pass/fail color-coded matrix cells
- OLED dark theme, mobile-first

## How to Run

Open `index.html`. Pick foreground and background colors using the color pickers or type hex values. See the contrast ratio and WCAG pass/fail status. Check how the colors appear under different color blindness types. Use Auto-fix if contrast fails. Enter a palette of colors to see the full contrast matrix.
