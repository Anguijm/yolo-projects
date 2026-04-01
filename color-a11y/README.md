# color-a11y

WCAG 2.1 color contrast and accessibility checker. Offline, zero dependencies.

## Features

- **Live contrast ratio** — WCAG 2.1 relative luminance formula, updates on every keystroke
- **WCAG badges** — AA Normal (4.5:1), AA Large (3:1), AAA Normal (7:1), AAA Large (4.5:1)
- **Color blindness simulation** — Protanopia, Deuteranopia, Tritanopia via CVD matrices in linear RGB space
- **Suggested fix** — Closest lightness adjustment on foreground that passes AA Normal (4.5:1); evaluates both lighter and darker directions and picks optimal
- **Live preview** — Sample text rendered at normal and large sizes with chosen colors
- **Swap button** — Exchange foreground and background instantly
- **Presets** — White/Black, GitHub Dark, Dracula, Solarized, Amber TRT, WCAG Fail

## Usage

Open `index.html` in any modern browser. No server required.

## Technical Notes

- CVD simulation applies Viénot/Brettel LMS matrices in **linearized** RGB space, not gamma-encoded sRGB
- WCAG 2.1 linearization: `c/12.92` if `c ≤ 0.04045`, else `((c+0.055)/1.055)^2.4`
- Contrast ratio: `(L_lighter + 0.05) / (L_darker + 0.05)`
- Fix suggestion: binary walks lightness 0→100 in both directions simultaneously, returns closest passing candidate
