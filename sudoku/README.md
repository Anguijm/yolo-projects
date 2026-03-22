# Sudoku

Classic Sudoku with algorithmic puzzle generation. 3 difficulty levels. Mobile-first with numpad and keyboard support.

## Features

- Backtracking solver generates valid complete boards
- Random cell removal creates puzzles (Easy: 35, Medium: 45, Hard: 55 removed)
- Tap cells to select, numpad or keyboard 1-9 to fill
- Arrow key navigation
- Row/column/box highlighting on selection
- Check button validates using Sudoku rules (not against one specific solution)
- Error highlighting in red
- Erase button and Delete/Backspace support
- Given cells locked (can't overwrite)
- Haptic on solve
- OLED black, mobile-first, all PWA metas

## Bug Fixed by Gemini Audit

- Validation compared against ONE solution (penalized valid alternative solutions). Now validates using isValid() Sudoku rules.

## How to Run

Open `index.html`. Select difficulty. Tap cells and enter numbers.
