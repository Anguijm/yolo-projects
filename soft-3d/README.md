# Soft 3D

A software 3D renderer built from scratch. No WebGL — pure math and Canvas 2D. Hand-rolled linear algebra renders flat-shaded, z-sorted 3D meshes with an orbit camera.

## Features

- **Hand-rolled linear algebra**: Vec3 and Mat4 operations (multiply, rotate, translate, perspective projection)
- **5 meshes**: Cube, Sphere, Torus, Icosahedron, Diamond — all procedurally generated
- **3 render modes**: Flat shading, Wireframe, Both
- **Flat shading** with configurable directional light
- **Painter's algorithm** z-sorting for correct face ordering
- **Backface culling** via screen-space cross product
- **Near-plane clipping** via w-component rejection
- **Orbit camera** with mouse drag rotation and scroll zoom
- **Fixed-timestep animation** for framerate independence
- **4 presets**: Crystal, Planet, Gem, Orbit
- **Keyboard shortcuts**: 1-5 for meshes, W/F/B for render modes

## How to Run

Open `index.html` in a browser.

## What I'd Change

- Add proper triangle clipping against the near plane (instead of face rejection)
- Implement Gouraud or Phong shading for smooth lighting on curved surfaces
- Add specular highlights
- Port to WebGL for massively higher triangle counts
