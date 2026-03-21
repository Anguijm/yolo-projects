# Regex Quest

An RPG where you fight monsters by writing regex patterns. Learn regex from basics to advanced as enemies get harder. Single HTML file, zero dependencies.

## Features

- 7 enemy types across 5 difficulty tiers:
  - Tier 1: Literals, character classes (\d, \w, [a-z])
  - Tier 2: Quantifiers ({n,m}, *), anchors (^), HTML tags
  - Tier 3: Groups, alternation, backreferences (\1)
  - Tier 4: Lookaheads (?=), non-capturing groups (?:)
  - Tier 5: Boss — email, phone number, JS variable patterns
- 21 unique challenge texts with curated goals and hints
- Live regex preview with match highlighting as you type
- RPG progression: XP, leveling, damage scaling, HP growth
- Gold economy with shop (potions, runes, gems, hint scrolls)
- Hint system: Ctrl+H reveals the expected pattern
- ReDoS protection: regex timeout prevents catastrophic backtracking
- Anti-cheat: penalty for lazy patterns like `.*`
- Debounced live preview to prevent input lag
- XSS-safe match highlighting

## How to Run

Open `index.html` in a browser. Click "Begin Quest" to start.

## What You'd Change

- More enemies and challenge texts per tier
- Persistent save via localStorage
- Boss special mechanics (multi-phase, time limit)
- Achievement system for regex mastery milestones
