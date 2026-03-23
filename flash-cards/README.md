# Flash Cards

Spaced repetition flashcard app with 3D card flip animation. Create, study, and review cards with adaptive scheduling.

## Features

- CSS 3D card flip animation (preserve-3d, backface-visibility)
- Spaced repetition: Hard=1min, OK=double interval (max 1 day), Easy=4x (max 1 week)
- Edit mode: plain text format (`front | back`, one per line)
- Editing preserves existing study progress (matched by front+back text)
- Reset button makes all cards due again without wiping intervals
- Due card count in progress bar
- Cards persisted in localStorage
- Haptic feedback on flip
- OLED black, mobile-first, all PWA metas

## Bug Fixed by Gemini Audit

- parseEditor destroyed all spaced repetition progress on every edit (now preserves progress for unchanged cards)
- Shuffle button unnecessarily reset intervals (changed to Reset that only clears nextReview times)
- Rating fallthrough defaulted to "Easy" on invalid input (added explicit rating===3 check)

## How to Run

Open `index.html`. Tap Edit to add cards (`front | back` format). Tap Study to review. Tap card to flip, then rate difficulty.
