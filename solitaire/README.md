# Solitaire

Klondike Solitaire with CSS-rendered cards and smart-tap auto-move. Full game rules: 7 tableau columns, 4 foundations, stock/waste draw. Tap any face-up card to automatically move it to its best valid destination.

## Features

- Full Klondike Solitaire rules with proper move validation
- CSS-only card rendering with Unicode suits (no images)
- Smart-tap: tap a card to auto-move to foundation or best tableau column
- Stack moves: tap a middle card to move it plus all cards on top
- Undo support (up to 50 moves)
- Timer and move counter
- Best time saved to localStorage
- Responsive card sizing based on screen width
- Win detection with stats display
- OLED-friendly green felt theme, mobile-first

## How to Run

Open `index.html`. Tap face-up cards to auto-move them. Tap the stock pile (top-left) to draw cards. Build foundations (top-right) from Ace to King by suit. Build tableau columns in descending order, alternating colors.
