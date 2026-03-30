# Markdown Deck — Authoring Guide

Use this guide to generate slide decks and design themes for the Markdown Deck tool. The tool takes markdown text (left panel) and a design.md token sheet (Theme panel) to produce styled presentations with live preview, fullscreen mode, and PowerPoint export.

---

## Slide Structure

Slides are separated by `---` on its own line. Each slide is an independent markdown block.

```
# Slide 1 Title

Content here.

---

## Slide 2 Title

More content.

---

# Slide 3 Title

Final slide.
```

---

## Headings

```
# H1 — Main title (largest, use once per slide)
## H2 — Section heading (use for most slide titles)
### H3 — Subsection heading
#### H4 — Label/caption text
```

A slide typically starts with one heading, then body content below it.

---

## Text Formatting

```
**bold text**
*italic text*
~~strikethrough~~
==highlighted text==
`inline code`
^superscript^
~subscript~
[link text](https://url.com)
```

These can be combined: `**bold and *italic* together**`

---

## Lists

### Unordered (bullets)
```
- First item
- Second item
  - Nested item (indent 2 spaces)
    - Deep nested (indent 4 spaces)
- Back to top level
```

### Ordered (numbered)
```
1. First step
2. Second step
3. Third step
```

### Task Lists (checkboxes)
```
- [x] Completed task
- [x] Another done
- [ ] Still pending
- [ ] Not started
```

---

## Two-Column Layout

Place `|||` on its own line to split content into left and right columns. Any heading above the split stays full-width as the slide title.

```
## Comparison Title

- Left column point
- Second point
- Third point

|||

- Right column point
- Parallel content
- Side by side data
```

Columns work with any content type — bullets, text, code blocks, quotes. Both columns get equal width.

---

## Code Blocks

Fenced with triple backticks. Include the language name for a label.

````
```python
def greet(name):
    return f"Hello, {name}"
```
````

````
```javascript
const add = (a, b) => a + b;
```
````

The language tag appears as a small label above the code block.

---

## Blockquotes

```
> Single line quote.

> Multi-line quotes work too.
> Just keep using the > prefix
> on consecutive lines.
```

---

## Tables

```
| Feature | Status | Priority |
|---------|--------|----------|
| Export  | Done   | High     |
| Themes  | Done   | Medium   |
| Images  | Done   | Low      |
```

The first row renders as a bold header. The separator row (`|---|---|`) is required.

---

## Images

```
![Description of image](https://url-to-image.png)
```

Images auto-scale to fit the slide (max-width 100%, max-height 50vh in preview, 60vh in presentation).

---

## Horizontal Rules

```
***
```

or `---` (but be careful — `---` on its own line between blank lines is a slide separator, not an HR. Use `***` for in-slide rules).

---

## Speaker Notes

Place `???` on its own line at the end of a slide. Everything after it is a speaker note — invisible in the presentation.

```
## Important Slide

Key points here.

???
Remind the audience about the deadline.
Mention the budget constraint.
```

---

## Slide Separator Reference

```
---        Separates slides (must be on its own line with blank lines above/below)
|||        Splits content into two columns
???        Starts speaker notes (hidden from presentation)
```

---

## Design.md Token Sheet

The Theme panel accepts a structured token document that controls all visual styling. Write tokens as `key: value` pairs under markdown headings.

### Full Token Reference

```
# Slide Design

## Colors
background: #0a0a0a
text: #cccccc
heading: #ffffff
subheading: #60a5fa
accent: #a78bfa
strong: #ffffff
emphasis: #fbbf24
code-text: #4ade80
code-bg: #1a1a1a
pre-bg: #111111
quote-text: #888888
quote-border: #333333
link: #60a5fa
hr: #333333

## Typography
heading-font: system-ui, sans-serif
body-font: system-ui, sans-serif
code-font: Consolas, monospace
h1-size: 3.5rem
h2-size: 2.2rem
h3-size: 1.6rem
body-size: 1.4rem
code-size: 1.1rem
line-height: 1.6
h1-weight: 700
h2-weight: 600

## Layout
slide-padding: 4rem 5rem
content-align: left
border-radius: 8px
```

### Token Descriptions

#### Colors
| Token | Controls | Example |
|-------|----------|---------|
| `background` | Slide background color | `#0a0a0a` (dark) or `#ffffff` (light) |
| `text` | Default body text, bullets, paragraphs | `#cccccc` |
| `heading` | H1 heading color | `#ffffff` |
| `subheading` | H2 heading color | `#60a5fa` (blue) |
| `accent` | H3 headings, decorative accents | `#a78bfa` (purple) |
| `strong` | Bold text color | `#ffffff` |
| `emphasis` | Italic text color | `#fbbf24` (amber) |
| `code-text` | Inline code text color | `#4ade80` (green) |
| `code-bg` | Inline code background | `#1a1a1a` |
| `pre-bg` | Code block background | `#111111` |
| `quote-text` | Blockquote text color | `#888888` |
| `quote-border` | Blockquote left border | `#333333` |
| `link` | Hyperlink color | `#60a5fa` |
| `hr` | Horizontal rule color | `#333333` |

#### Typography
| Token | Controls | Example |
|-------|----------|---------|
| `heading-font` | Font for H1, H2 | `Georgia, serif` |
| `body-font` | Font for body text, lists | `system-ui, sans-serif` |
| `code-font` | Font for code blocks | `Consolas, monospace` |
| `h1-size` | H1 font size | `3.5rem` |
| `h2-size` | H2 font size | `2.2rem` |
| `h3-size` | H3 font size | `1.6rem` |
| `body-size` | Body text font size | `1.4rem` |
| `code-size` | Code font size | `1.1rem` |
| `line-height` | Body text line spacing | `1.6` |
| `h1-weight` | H1 boldness | `700` (bold) or `300` (light) |
| `h2-weight` | H2 boldness | `600` |

#### Layout
| Token | Controls | Example |
|-------|----------|---------|
| `slide-padding` | Inner padding of each slide | `4rem 5rem` |
| `content-align` | Text alignment | `left`, `center` |
| `border-radius` | Slide corner rounding | `8px` or `0px` |

### Available Fonts (system-safe, no CDN)
- `system-ui, sans-serif` — clean, modern
- `Georgia, serif` — warm, editorial
- `SF Mono, Fira Code, monospace` — technical, terminal
- `Consolas, monospace` — code-focused
- `Palatino, serif` — elegant, academic
- `Impact, sans-serif` — bold headers only

---

## Built-in Theme Presets

Click these in the Theme panel to load a full token set:

| Preset | Vibe |
|--------|------|
| **Dark** | Default. Near-black bg, monospace, cyan/purple accents |
| **Midnight** | Deep navy bg, system sans-serif, sky blue accents |
| **Light** | White bg, dark text, blue accents, high contrast |
| **Warm** | Stone/earth tones, Georgia headings, amber accents |
| **Neon** | Pure black bg, cyan/magenta neon, thin weight |
| **Corporate** | Clean white bg, system fonts, minimal color, heavy weights |

---

## PPTX Export

Click **Export** to download a `.pptx` file. The export:
- Applies your current design tokens (colors, fonts) to the PowerPoint slides
- Converts markdown formatting to PPTX text runs (bold, italic, code, bullets)
- Renders two-column layouts as side-by-side text boxes
- Uses dark/light background from your theme
- Opens in PowerPoint, Keynote, and Google Slides

---

## Example: Complete Deck

```markdown
# Q4 Product Update

Engineering Team — December 2024

---

## What We Shipped

- [x] User authentication v2
- [x] Dashboard redesign
- [x] API rate limiting
- [ ] Mobile app beta (in progress)

---

## Performance Gains

Before (Q3)

|||

After (Q4)

---

## Performance Gains

- API latency: **420ms**
- Page load: **3.2s**
- Error rate: **2.1%**

|||

- API latency: **180ms** ↓57%
- Page load: **1.1s** ↓66%
- Error rate: **0.3%** ↓86%

---

## Architecture

```python
# New caching layer
@cache(ttl=300)
def get_user(id):
    return db.users.find(id)
```

> Reduced database queries by 73%

---

## Next Quarter

| Initiative | Owner | Target |
|-----------|-------|--------|
| Mobile beta | Sarah | Jan 15 |
| API v3 | Mike | Feb 1 |
| Analytics | Chen | Feb 15 |

---

# Thank You

Questions?

???
Budget discussion is confidential — only share if asked directly.
Mobile beta delay was due to iOS review process, not engineering.
```

---

## Example: Design Brief for Corporate Theme

```
# Corporate Presentation

## Colors
background: #ffffff
text: #1f2937
heading: #111827
subheading: #1f2937
accent: #2563eb
strong: #111827
emphasis: #059669
code-text: #dc2626
code-bg: #f3f4f6
pre-bg: #f9fafb
quote-text: #6b7280
quote-border: #d1d5db
link: #2563eb
hr: #e5e7eb

## Typography
heading-font: system-ui, sans-serif
body-font: system-ui, sans-serif
code-font: Menlo, monospace
h1-size: 3rem
h2-size: 2rem
h3-size: 1.4rem
body-size: 1.3rem
code-size: 0.95rem
line-height: 1.8
h1-weight: 800
h2-weight: 700

## Layout
slide-padding: 4rem 6rem
content-align: left
border-radius: 4px
```

---

## Example: Design Brief for Dark Tech Theme

```
# Dark Technical

## Colors
background: #0a0a0a
text: #a5b4fc
heading: #00ffff
subheading: #ff00ff
accent: #00ff88
strong: #ffffff
emphasis: #ff00ff
code-text: #00ff88
code-bg: #0a0a2e
pre-bg: #0a0a1a
quote-text: #6366f1
quote-border: #ff00ff
link: #00ffff
hr: #1e1b4b

## Typography
heading-font: SF Mono, Fira Code, monospace
body-font: SF Mono, monospace
code-font: SF Mono, monospace
h1-size: 3.5rem
h2-size: 2.2rem
h3-size: 1.6rem
body-size: 1.3rem
code-size: 1.1rem
line-height: 1.6
h1-weight: 300
h2-weight: 300

## Layout
slide-padding: 4rem 5rem
content-align: left
border-radius: 0px
```
