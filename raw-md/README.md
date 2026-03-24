# Raw MD

Zero-dependency markdown previewer with custom regex parser. Split-pane editor with live preview, synchronized scrolling, and HTML export.

## Features

- Custom regex-based markdown parser (no external libraries)
- Supports: H1-H6 headers, bold, italic, strikethrough, links, images
- Code blocks (fenced with ```) and inline code
- Unordered and ordered lists
- Blockquotes, horizontal rules
- XSS protection: HTML entities escaped before parsing
- Code blocks extracted before inline parsing (prevents interference)
- Split-pane layout: editor left, preview right (stacks on mobile)
- Synchronized scroll between editor and preview
- Debounced rendering (150ms) for smooth typing
- localStorage auto-save
- Copy HTML button with clipboard API
- Word count, character count, reading time stats
- Default sample content demonstrating all features
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Type markdown in the left pane, see rendered HTML in the right pane. Click "Copy HTML" to copy the rendered output. Content auto-saves to localStorage.
