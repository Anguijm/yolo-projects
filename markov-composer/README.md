# Markov Composer

Paste any text, watch it become a force-directed word graph. Click nodes to steer procedural text generation in real-time. Single HTML file, zero dependencies.

## Features

- Markov chain builder with configurable n-gram order (1-4)
- Force-directed graph visualization (Coulomb repulsion + Hooke attraction)
- Animated playhead walks the chain, generating text word by word
- Click any node to steer generation to that word
- Trail glow shows recent generation path through the graph
- Edge thickness proportional to transition probability
- Node size logarithmic (handles Zipf's law)
- 4 built-in sample texts: Shakespeare, Sci-Fi, Cooking, Philosophy
- Generation speed slider (1-20 words/sec)
- Max nodes slider (20-200)
- Debounced n-gram rebuild on slider change
- Dead-end detection with auto-restart
- Off-graph word handling (playhead fades when word not in top-N)
- Keyboard: Space=toggle, C=clear

## How to Run

Open `index.html` in a browser. Click a sample text or paste your own, then click "Build Chain."

## What You'd Change

- Web Worker for chain building (large texts)
- Barnes-Hut spatial partitioning for 500+ nodes
- Corpus blending (mix two texts, watch nodes bridge the gap)
- Audio — words trigger notes as they're generated
