# Prose X-Ray

Paste any text, get an instant visual breakdown of your writing. Word frequency, reading level, sentence rhythm, vocabulary richness. A fitness tracker for prose. Single HTML file, zero dependencies.

## Features

- Instant analysis on paste or type (300ms debounce)
- Flesch-Kincaid Grade Level and Reading Ease with color-coded meter
- Word count, sentence count, paragraph count, character count
- Reading time estimate (238 wpm)
- Vocabulary richness (unique words ratio)
- Average word length and sentence length
- Sentence rhythm histogram (bar per sentence, color-coded by length)
- Top 12 words bar chart (excluding stop words)
- 4 demo texts: Hemingway, Academic, Marketing, Dickens
- Abbreviation-safe sentence splitting (Mr., Dr., etc.)
- Proper syllable counting (handles silent e, vowel groups)
- XSS-safe HTML escaping (including quotes)

## Bugs Fixed by Gemini Code Audit

- Syllable counter split 3+ vowel groups incorrectly (fixed regex)
- Sentence metrics used different divisors (harmonized)
- Sentence splitter broke on abbreviations (added protection)
- escapeHtml missing quote escaping (added)
- Variable ordering bug (validSentCount used before declaration — fixed)

## How to Run

Open `index.html` in a browser. Paste text or click a demo.

## What You'd Change

- Adverb/passive voice highlighting
- Side-by-side text comparison
- Export analysis as PDF
- Paragraph-level density heatmap
