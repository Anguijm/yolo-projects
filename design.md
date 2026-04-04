# YOLO Design System

Agent-readable design system. Reference this when building or refining any YOLO project.

## Philosophy

Maximum information density, minimal visual noise. Industrial/terminal aesthetic. Near-black backgrounds, greyscale text hierarchy, ghost buttons, sharp corners, no decoration.

## Colors

### Backgrounds
```
--bg-page:     #0a0a0a     /* Page background */
--bg-surface:  #111        /* Cards, panels, inputs */
--bg-elevated: #1a1a1a     /* Raised elements, empty cells */
--bg-hover:    #222        /* Hover/active states */
```

### Text (greyscale ladder)
```
--text-primary:    #fff    /* Display values, main output */
--text-body:       #ccc    /* Default body text */
--text-secondary:  #aaa    /* Interactive text, active buttons */
--text-tertiary:   #555    /* Slider values, metadata */
--text-label:      #444    /* Small labels, section headers */
--text-muted:      #333    /* Subtitles, hints */
--text-ghost:      #222    /* Barely visible, decorative */
--text-invisible:  #111    /* Placeholder text */
```

### Borders
```
--border-default:  #1a1a1a /* Default inactive border */
--border-subtle:   #111    /* Barely-there border */
--border-visible:  #222    /* Slightly more visible */
--border-active:   #444    /* Active/hover state */
--border-focus:    #555    /* Focused input */
```

### Semantic Status (use only for communicating state)
```
--color-success:   #3fb950  /* Green — win, pass, good */
--color-warning:   #d29922  /* Amber — caution, fair */
--color-error:     #f85149  /* Red — fail, danger, lose */
--color-info:      #58a6ff  /* Blue — info, refined, link */
```

### Accent Colors (pick ONE per project, use sparingly)
```
--accent-cyan:     #0ff     /* Neon cyan — most common */
--accent-red:      #ff003c  /* Neon red */
--accent-magenta:  #f0f     /* Neon magenta — secondary highlight */
```

Accent colors are for the "live" or "active" state only. Never decorative. One accent per project.

## Typography

### Font Stacks (pick ONE per project)
```css
/* Data/utility tools — use this */
font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;

/* Interactive/visual tools — use this */
font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
```

Never use web fonts or CDN imports. All form elements inherit the page font via `font-family: inherit`.

### Size Scale
```
Display large:  clamp(2rem, 8vw, 4rem)   /* Main output, timer, score */
Display:        clamp(1.2rem, 5vw, 2rem)  /* Primary value */
Heading:        0.75rem - 0.85rem         /* Page title, section headers */
Button:         0.6rem - 0.65rem          /* Button text */
Label:          0.45rem - 0.55rem         /* Control labels, metadata */
Hint:           0.4rem                    /* Ghost text, tiny hints */
```

### Text Treatment
- Labels and short UI strings: `text-transform: uppercase; letter-spacing: 0.1em - 0.3em`
- Display values: `font-weight: 200` (light) or `font-weight: 900` (heavy)
- Use `font-variant-numeric: tabular-nums` for numbers that change (timers, scores)
- Use `clamp()` for responsive display text

## Spacing

```
Container padding:  12px (mobile-friendly default)
Section gap:        8px - 12px
Control row gap:    6px - 8px
Tight grouping:     4px
Max-width layout:   480px (centered) for utility tools
Full-bleed:         For games and immersive experiences
```

Everything is compact and dense. No large paddings.

## Components

### Ghost Button (default control)
```css
.btn {
  padding: 4px 10px;
  background: transparent;
  border: 1px solid #1a1a1a;
  color: #444;
  font-family: inherit;
  font-size: 0.55rem;
  cursor: pointer;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.btn:active { border-color: #555; color: #888; }
.btn.active { border-color: var(--accent); color: var(--accent); }
```

### Range Slider
```css
input[type="range"] {
  height: 3px;
  accent-color: #555;  /* or project accent color */
}
```

### Text Input
```css
input[type="text"] {
  background: #111;
  border: 1px solid #222;
  color: #aaa;
  padding: 6px 8px;
  font-family: inherit;
  font-size: 0.75rem;
  outline: none;
}
input[type="text"]:focus { border-color: #555; }
```

### Panel / Card
```css
.panel {
  padding: 6px 8px;
  border: 1px solid #1a1a1a;
  /* No border-radius — sharp corners everywhere */
  /* No background — transparent against page bg */
}
```

## Layout Rules

1. No `border-radius` on controls (sharp industrial aesthetic)
2. No box-shadows (borders only for structure)
3. No background fills on inactive controls (ghost buttons)
4. One solid-fill button max per project (the "commit" CTA)
5. `border-radius: 4px` is acceptable only for game tiles, swatches, and toasts

## Required HTML Boilerplate

Every project must include:
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="theme-color" content="#000000">
<meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src *">
```

## Required CSS Reset

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  height: 100%;
  background: #0a0a0a;
  overflow: hidden; /* or overflow-y: auto for scrollable tools */
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}
```

## Rules

- Zero external dependencies (no CDNs, no web fonts, no frameworks)
- Everything inline in a single HTML file
- Mobile-first: touch targets 44px+, responsive clamp() text
- `user-select: none` on interactive surfaces (games, drawing)
- `-webkit-tap-highlight-color: transparent` always
- `font-family: inherit` on all buttons and inputs
