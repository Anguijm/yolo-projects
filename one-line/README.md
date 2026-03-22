# One Line

A minimalist daily journal. One line per day. The constraint forces distillation. Over months, you build a mosaic of your days.

## Features

- One text input, 80 character limit
- Save with Enter or button
- Today's date displayed, existing entry pre-filled
- Edit or delete today's entry (empty save = clear)
- Mosaic view: monthly calendar grid with filled/empty day indicators
- Tap any filled day to read that entry
- Navigate months (prev/next arrows)
- Streak counter (consecutive days, tolerates not-yet-written today)
- Entry count and monthly count stats
- Auto-focus input on load (300ms delay for mobile keyboard)
- localStorage persistence with storage-full error feedback
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Code Audit

- Streak showed 0 if today not written yet (now checks yesterday first)
- Entry deletion unreachable (save() returned early on empty, removed early return)
- Silent storage failure (now shows "Storage full" error message)

## How to Run

Open `index.html` on your phone. Write one line about your day. Come back tomorrow.

## What You'd Change

- Export entries as JSON or text file
- Year mosaic view (365-dot grid)
- Daily reminder notification (Service Worker)
- Light theme toggle
