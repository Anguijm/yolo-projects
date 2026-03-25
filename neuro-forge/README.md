# Neuro Forge

Interactive neural network playground. Paint data points on canvas, watch a 2-layer network learn to classify them in real-time. Decision boundary updates live as a heatmap. Network diagram shows weights and activations.

## Features

- Vanilla JS neural network (2→4→4→1) with unrolled backpropagation — zero dependencies
- Real-time decision boundary visualization via low-res heatmap scaled up
- Live network diagram showing weight magnitudes (blue=positive, orange=negative) and node activations
- 4 preset datasets: XOR, Spiral, Clusters, Circle
- Paint data points by clicking/dragging — select orange (Class A) or blue (Class B)
- Adjustable learning rate slider
- Pause/play training, reset weights, clear data
- Keyboard shortcuts: A/1=orange, B/2=blue, Space=pause, R=reset, C=clear
- Epoch counter and current loss display
- OLED black, mobile-first, pointer events for touch

## How to Run

Open `index.html`. The XOR dataset loads by default and the network starts training immediately. Paint your own data points or try the presets. Watch the decision boundary morph as the network learns.
