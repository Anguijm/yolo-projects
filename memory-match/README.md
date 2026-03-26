# Memory Match

Classic card-flip memory game. Find all matching pairs by flipping two cards at a time. CSS 3D card animations, emoji icons, three difficulty levels, move counter, timer, and best score tracking.

## Features

- CSS 3D card flip animations (rotateY with backface-visibility)
- 3 difficulty levels: Easy (4x3, animals), Medium (4x4, mixed), Hard (5x4, abstract)
- Strict state machine prevents clicking during card evaluation
- Move counter and timer
- Best score per difficulty saved to localStorage
- Responsive card grid using CSS aspect-ratio (adapts to screen rotation)
- Themed emoji sets per difficulty level
- Board locked during mismatch evaluation to prevent race conditions
- Mobile-first with tap targets

## How to Run

Open `index.html`. Tap cards to flip them. Find two matching emojis to clear them. Match all pairs to win. Try to minimize your moves. Switch difficulty for larger grids.
