# Neural Network Playground

Draw data points, watch a neural network learn to classify them in real-time. Decision boundary renders as a live heatmap. All ML math implemented from scratch — zero dependencies.

## Features

- Neural network with configurable architecture (1-6 hidden layers, 2-16 neurons)
- 3 activation functions: ReLU, Sigmoid, Tanh
- Xavier/Glorot weight initialization
- Backpropagation with gradient clipping
- L2 regularization with adjustable lambda
- Mini-batch SGD (full batch, 8, 16, 32, 64)
- Live decision boundary heatmap (40x40 grid, Float32Array)
- Real-time loss chart
- 5 data presets: Circle, Spiral, XOR, Clusters, Moons
- Left-click to paint Class A (cyan), right-click for Class B (pink)
- Drag to paint continuous streams of points
- Learning rate on log scale
- Accuracy and loss stats
- Keyboard shortcuts: Space=toggle, R=reset, C=clear

## How to Run

Open `index.html` in a browser. Click a preset or paint your own data.

## What You'd Change

- Web Worker for training (prevents UI lag on large networks)
- Adam optimizer for faster convergence
- WebGL fragment shader for pixel-level decision boundary
- Multi-class classification support
