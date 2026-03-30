# Syntax Glow

Zero-dependency browser-based code syntax highlighter. Paste code, get colored output.

## How to run

Open `index.html` in a browser.

## Features

- Auto-detects language (JavaScript, Python, HTML, CSS)
- Manual language override buttons
- Tokenizes: keywords, strings, numbers, comments, functions, operators, types, decorators, regex literals
- Dark theme matching YOLO design system
- Copy HTML button for extracting colored output
- Tab key works in textarea
- Pure tokenizer function (`syntaxHighlight(code, lang)`) designed for extraction into Markdown Deck

## FEEDER PROJECT

The `syntaxHighlight()` function is designed to be extracted into Markdown Deck's code block renderer for syntax-highlighted presentation slides.

## What I'd change

- Add more languages (Go, Rust, TypeScript, SQL, Shell)
- Line numbers
- Configurable theme via design tokens
