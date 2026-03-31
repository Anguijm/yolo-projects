# token-count

Browser-based LLM token counter and cost estimator. Paste text, see real-time token estimates across every major model — with context window usage bars and per-request cost.

## Features

- **BPE-approximate tokenizer** — custom heuristic based on how GPT/Claude/Gemini tokenizers actually behave: word length, numerics, CJK, emoji, punctuation, indentation
- **6 model coverage** — GPT-4o, GPT-4o mini, Claude Opus 4, Claude Sonnet 4, Gemini 1.5 Pro, Gemini 2.0 Flash
- **Context window bars** — visual fill showing % of context used; turns amber at 70%, red at 90%
- **Cost estimation** — input cost per request at published API rates (2025)
- **Text composition** — whitespace, punctuation, ASCII letter, and non-ASCII breakdown with bar charts
- **Text stats** — chars, words, lines, paragraphs, chars-per-token ratio
- **Presets** — system message, code block, and long engineering prompt to benchmark different text types
- **Copy as markdown** — exports a full token/cost table ready to paste into docs or issues

## Usage

Open `index.html` in any browser. Paste or type text. All stats update live.

## Token counting methodology

Tokenization is approximated without loading a real BPE vocabulary (~500KB download). The heuristic:

- Short English words (≤4 chars): 1 token each
- Medium words (5-10 chars): ~word_length / 4.5 tokens
- Long words (>10 chars): ~word_length / 3.5 tokens
- Numbers: 1 token per 3 digits
- CJK characters: 1 token each
- Emoji (surrogate pairs): 3 tokens each
- Newlines: 1 token each
- Indentation: ~1 token per 4 spaces

Accuracy: ±5-10% for typical English prose. Code and mixed-language text may vary more.

## No dependencies

Single HTML file. Zero external requests.
