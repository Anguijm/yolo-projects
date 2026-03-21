# speedtype

A terminal-based typing speed test that uses real code snippets instead of boring pangrams.

## Features

- Curses TUI with real-time character-by-character feedback (green = correct, red = wrong)
- Live WPM and accuracy display while you type
- Scans your machine for Python/JS/Go files to use as snippets, falls back to built-in samples
- Saves results to `~/.speedtype_history.json`
- Filter by language with `--lang`

## Requirements

- Python 3.6+
- Linux (uses `curses`)
- Zero external dependencies

## Usage

```bash
# Run a typing test (random language)
python3 speedtype.py

# Run with a specific language
python3 speedtype.py --lang python
python3 speedtype.py --lang js
python3 speedtype.py --lang go

# View past results
python3 speedtype.py --history
```

## Controls

- Just start typing to begin the test
- **Backspace** to fix mistakes
- **ESC** to quit early
