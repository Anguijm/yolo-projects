# Algo Vision

Sorting algorithm visualizer with 4 algorithms, animated bars, audio feedback, and comparison/swap counters. Watch Bubble Sort, Insertion Sort, Quick Sort, and Merge Sort in action.

## Features

- 4 algorithms: Bubble Sort, Insertion Sort, Quick Sort, Merge Sort
- Animated bar chart with color-coded states (comparing/swapping/sorted/pivot)
- Async/await animation with configurable speed slider
- Array size slider (10-120 elements)
- Start/Stop with clean cancellation across all algorithms
- Audio mode: sine tone mapped to bar height (value → frequency)
- Audio node cleanup via onended disconnect (prevents memory leaks)
- Comparison and swap counters with immediate reset on new sort
- Generate new random array button
- DOM bar reuse (add/remove only as needed, not full rebuild)
- Cancel checks at every loop level (outer loops, recursive branches, inner merges)
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- insertionSort outer loop missing cancel check — sort continued after stop clicked
- mergeSort second recursive branch executed after cancel — added cancel check between branches
- Stats display not reset until first comparison — added updateInfo() on start
- Audio oscillator/gain nodes never disconnected — added onended cleanup to prevent memory leaks

## How to Run

Open `index.html`. Select an algorithm, adjust size and speed, click Start. Toggle Sound for audio feedback. Click Stop to cancel mid-sort.
