# Ipsum Gen

Configurable Lorem Ipsum text generator. Choose words, sentences, or paragraphs. Copy with one click.

## Features

- 3 output modes: words, sentences, paragraphs
- Quantity slider (1-50)
- Real-time generation as settings change
- Classic "Lorem ipsum dolor sit amet..." opening for sentences and paragraphs
- No wasted generation (classic start inserted directly, not overwritten)
- 120+ Latin vocabulary words for natural variation
- Word and character count display
- One-click copy with visual "COPIED" feedback and toast
- Clipboard API with execCommand fallback (also triggered on API rejection)
- Minimalist dark developer-tool aesthetic
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Clipboard API failure silently swallowed (catch was empty) — now falls back to execCommand on rejection
- First sentence generated then immediately overwritten — refactored to push classic start directly

## How to Run

Open `index.html`. Select mode (paragraphs/sentences/words), adjust quantity, copy the output.
