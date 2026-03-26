# Regex Lab

Live regular expression tester. Type a pattern, paste test text, see matches highlighted in real-time with capture groups extracted. Flags toggle, replacement preview, and regex cheat sheet.

## Features

- Real-time match highlighting with alternating colors
- Flag toggles: global (g), case-insensitive (i), multiline (m), dotAll (s)
- Capture group extraction per match (numbered and named groups)
- Zero-width match visibility (visual indicator for ^, $, \b matches)
- Replacement preview with substitution patterns ($1, $2, etc.)
- XSS-safe HTML escaping (prevents injection from test text)
- Graceful error handling on invalid regex syntax
- Debounced input (150ms) for smooth typing experience
- Regex cheat sheet in collapsible details element
- Match count display
- Dark theme, monospace typography, mobile-first

## How to Run

Open `index.html`. Type a regex pattern, enter test text. Matches are highlighted instantly. Toggle flags, view capture groups, test replacements. Expand the cheat sheet for quick regex reference.
