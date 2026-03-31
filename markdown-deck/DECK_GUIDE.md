# Markdown Deck — Authoring Guide

Use this guide to generate slide decks and design themes for the Markdown Deck tool. The tool takes markdown text (left panel) and a design.md token sheet (Theme panel) to produce styled presentations with live preview, fullscreen mode, and PowerPoint export.

---

## CRITICAL: Rules for AI-Generated Slides

When using an AI model (Gemini, Claude, GPT, etc.) to generate slide markdown, include these instructions in your prompt to prevent common failures:

### Must-Have Prompt Instructions

```
Generate a markdown slide deck following these STRICT rules:

1. OUTPUT RAW MARKDOWN ONLY — do NOT wrap the entire output in a code fence.
   Your response should start with the first slide heading, not with ```markdown.

2. EVERY code block MUST have both opening and closing triple backticks.
   Opening: ```language
   Closing: ```
   Count your backticks. If you opened one, you MUST close it.

3. Slide separator is --- on its own line with blank lines above and below.
   Do NOT use --- inside a slide (use *** for horizontal rules within slides).

4. Do NOT nest code blocks. Never put ``` inside another ``` block.

5. For the design.md theme, output it SEPARATELY from the slides — not inline.

6. Fragment breaks use -- on its own line (two dashes, not three).
   Three dashes (---) = slide break. Two dashes (--) = fragment reveal.

7. Two-column layout uses ||| on its own line between the two columns.

8. Per-slide theme overrides use HTML comments: <!-- bg: #color, text: #color -->
   Place these at the very top of a slide, before any content.

9. Positioned elements use [@ x:10% y:20% w:40%] on its own line.

10. Speaker notes go after ??? at the end of a slide.
```

### Common AI Failures and How to Avoid Them

| Failure | Cause | Fix |
|---------|-------|-----|
| Broken code blocks | AI wraps entire output in ``` | Tell it: "do NOT wrap output in a code fence" |
| Missing closing ``` | AI forgets to close a code block | Tell it: "count your backticks" |
| Slides don't separate | AI uses `---` without blank lines | Tell it: "blank line before and after ---" |
| Fragment breaks create new slides | AI uses `---` instead of `--` | Tell it: "-- for fragments, --- for slides" |
| Theme overrides don't work | AI puts `<!-- -->` after content | Tell it: "theme comments go FIRST in the slide" |
| Nested code blocks | AI puts ``` inside another ``` | Tell it: "never nest code blocks" |

### Example Prompt

```
Using the Markdown Deck format, create a 6-slide deck about [TOPIC].

Rules:
- Output raw markdown, NOT wrapped in a code fence
- Every code block must have opening AND closing ```
- Separate slides with --- (blank line above and below)
- Use ## for slide titles, ### for subtitles
- Use -- for progressive reveal (NOT ---)
- Use ||| for two-column layouts
- Include speaker notes after ??? on at least 2 slides
- First slide should use <!-- bg: #0f172a, text: #e2e8f0, align: center -->

Include: a title slide, an agenda slide, 3 content slides with a mix of
bullets/code/tables, and a closing slide.
```

### Validating AI Output

After receiving AI-generated markdown:
1. Count backtick pairs — every opening ``` needs a closing ```
2. Check that `---` slide separators have blank lines around them
3. Verify `--` (fragments) vs `---` (slides) are correct
4. Paste into Markdown Deck — the auto-close heuristic will fix one unclosed fence, but not multiple

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

**Supported languages for syntax highlighting:** JavaScript (`js`, `javascript`), Python (`python`, `py`), HTML (`html`), CSS (`css`). Code blocks with a recognized language tag get full-color tokenization — keywords (purple), strings (green), numbers (orange), comments (grey), functions (blue), operators (cyan). Unrecognized languages render as plain monochrome.

---

## Diagrams

Use ````diagram` fenced blocks to render flowcharts directly in your slides. Uses a simple text DSL — no external tools needed.

### Syntax
````
```diagram
[Start] --> [Process Data] --> [Output]
[Process Data] --error--> [Error Handler]
[Error Handler] --> [Start]
```
````

### DSL Rules
- `[Node Name]` — defines a box/node
- `-->` — creates a directed arrow between nodes
- `--label-->` — creates a labeled arrow
- Chain multiple: `[A] --> [B] --> [C]`
- `//` at end of line — comment (ignored)
- Nodes auto-deduplicate by name (case-insensitive)

### Layout
- Nodes are auto-positioned using layered graph layout (no manual coordinates)
- Direction is always top-to-bottom
- Layers are centered relative to the widest layer
- Bezier curve edges with arrowheads

### Example: Software Architecture
````
```diagram
[Browser] --> [API Gateway]
[API Gateway] --> [Auth Service]
[API Gateway] --> [App Server]
[App Server] --> [Database]
[App Server] --> [Cache]
[Auth Service] --> [Database]
```
````

### Example: Decision Flow
````
```diagram
[Input] --> [Validate]
[Validate] --valid--> [Process]
[Validate] --invalid--> [Error]
[Process] --> [Output]
[Error] --retry--> [Input]
```
````

### Notes
- Renders as inline SVG (scales responsively, max-height 50vh)
- Works in preview and presentation mode
- In PPTX export, diagrams are rendered as embedded PNG images (SVG → Canvas → PNG pipeline)
- Self-referencing edges (`[A] --> [A]`) are not supported in the deck renderer

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

## Progressive Reveal

Use `--` on its own line within a slide to create fragment breaks. Content after each `--` is hidden until the presenter presses right arrow or space. Each press reveals the next fragment with a fade-in transition.

```
## Key Findings

Our research revealed three insights:

--

**1. Speed matters** — Users abandon after 3 seconds

--

**2. Simplicity wins** — Fewer features, higher adoption

--

**3. Trust compounds** — Each good experience builds loyalty
```

### How it works in presentation mode
- Right arrow / Space → reveals next fragment (0.3s fade)
- Left arrow → hides last fragment, then goes to previous slide
- Going back to a previous slide shows all its fragments

### How it works in PPTX export
Fragments are expanded into **duplicate slides** for maximum compatibility:
- Slide 1a: Only "Our research revealed..."
- Slide 1b: + "1. Speed matters"
- Slide 1c: + "2. Simplicity wins"
- Slide 1d: + "3. Trust compounds"

This works in every PowerPoint viewer without animation support.

### Notes
- `--` must be on its own line with blank lines around it
- Fragments work with any content: bullets, text, images, code blocks
- In the preview panel, all fragments are visible (no progressive reveal in edit mode)
- Combine with per-slide themes for dramatic section reveals

---

## Per-Slide Theme Overrides

Override the global theme on any individual slide using HTML comment directives at the top of the slide.

### Syntax
```
<!-- bg: #1e3a5f, text: #e2e8f0 -->
```

### Supported Properties
| Property | Controls | Example |
|----------|----------|---------|
| `bg` | Slide background color | `bg: #1e3a5f` |
| `text` | Default text color | `text: #e2e8f0` |
| `font` | Font family | `font: Georgia, serif` |
| `align` | Text alignment | `align: center` |
| `padding` | Slide padding | `padding: 6rem` |
| `size` | Base font size | `size: 1.6rem` |

### Examples

#### Title slide with dark blue background
```
<!-- bg: #0f172a, text: #e2e8f0, align: center -->

# Company Name

*Annual Report 2026*
```

#### Section divider with accent color
```
<!-- bg: #7c3aed, text: #ffffff, align: center -->

# Part Two

## Market Analysis
```

#### Light slide in a dark deck
```
<!-- bg: #f8fafc, text: #1e293b -->

## Financial Summary

| Quarter | Revenue | Growth |
|---------|---------|--------|
| Q1 | $2.1M | +12% |
| Q2 | $2.8M | +33% |
```

### Notes
- Multiple properties separated by commas in one comment
- Overrides reset between slides — they don't bleed
- Works in preview, presentation mode, and PPTX export
- The comment is stripped from the rendered slide (invisible to audience)

---

## Presenter View

Click the **Presenter** button to open a dual-window presentation setup:

- **Main window** → enters fullscreen presentation mode (audience sees this)
- **Presenter window** → opens as a pop-up showing:
  - Current slide (large, left 2/3)
  - Next slide preview (top right)
  - Speaker notes from `???` (bottom right)
  - Elapsed timer (bottom bar)
  - Slide counter

### How to use
1. Click **Presenter** (not **Present**)
2. Allow the pop-up if browser asks
3. Drag the presenter window to your laptop screen
4. The main window goes fullscreen on the projector/external display
5. Navigate from either window — both stay synced

### Notes
- Syncs via localStorage events — no server needed
- Fragment reveals (--) sync to the presenter window
- Speaker notes update on each slide change
- Timer starts when the presenter window opens
- If the pop-up is blocked, the main window still enters presentation mode

---

## Slide Reordering

Drag and drop thumbnails in the bottom strip to reorder slides. The markdown source is automatically updated to match.

- Grab any thumbnail and drag it to a new position
- The active slide follows the move
- The textarea content is rewritten with the new slide order
- Auto-saves after every reorder

---

## Save, Load, and File Operations

### Auto-save
Your deck auto-saves to the browser's localStorage every second while editing. Close the tab and reopen — your content is restored.

### Ctrl+S / Cmd+S
Press Ctrl+S (or Cmd+S on Mac) for an immediate save. The Save button flashes green to confirm.

### Save to file
Click **Save** to download your deck as a `.md` file. On supported browsers (Chrome/Edge), you'll get a native file picker. On others, it downloads directly.

### Open a file
Click **Open** to load a `.md` file from your computer. This replaces the current editor content (auto-saved to localStorage).

### Tips
- Save your `.md` files to version control for history
- The design.md theme tokens are saved separately in localStorage
- Opening a new file doesn't change your theme — themes persist independently

---

## Positioned Elements

Place `[@ x:... y:... w:...]` on its own line to start a positioned block. Everything after it until the next `[@...]` or end of slide goes into that block.

### Syntax
```
[@ x:10% y:20% w:45%]
```

### Properties
| Property | Description | Example |
|----------|-------------|---------|
| `x` | Left position (% of slide width) | `x:10%` |
| `y` | Top position (% of slide height) | `y:20%` |
| `w` | Width (% of slide width) | `w:45%` |
| `h` | Height (% of slide height) | `h:30%` |
| `align` | Text alignment within block | `align:center` |
| `size` | Font size override | `size:2rem` |

### Example: Custom Layout
```
# Product Launch

[@ x:5% y:25% w:40%]
### Features
- Real-time sync
- Offline support
- End-to-end encryption

[@ x:55% y:25% w:40%]
### Pricing
- Free tier: 1GB
- Pro: $9/mo, 100GB
- Enterprise: custom

[@ x:15% y:80% w:70% align:center]
**Available March 2026** — [Sign up now](https://example.com)
```

### Example: Title Slide with Positioned Subtitle
```
[@ x:10% y:25% w:80%]
# The Future of AI

[@ x:10% y:55% w:60%]
A roadmap for the next decade

[@ x:10% y:75% w:50% size:0.8rem]
*John Doe — CTO, Acme Corp*
*March 2026*
```

### Visual Layout Mode

Click the **Layout** button to enter visual positioning mode:

1. An overlay appears over the slide preview
2. Click **+ Block** to add a positioned element
3. **Drag** blocks to move them
4. **Drag the corner handle** to resize
5. **Double-click** a block to edit its content
6. **Delete key** while hovering removes a block
7. Click **Layout** again to exit — all positions are written back to the markdown as `[@...]` directives

This gives you a visual alternative to typing `[@ x:... y:... w:...]` by hand. The output is identical — the Layout mode just generates the directives for you.

### Notes
- All positions use **percentages** relative to the slide dimensions
- Positioned blocks work in preview, presentation mode, and PPTX export
- Mixing positioned and flow content on the same slide is possible — flow content appears normally, positioned blocks overlay on top
- Don't use `|||` (two-column) and `[@]` (positioning) on the same slide — use positioning to create columns instead
- Visual Layout mode reads existing `[@...]` blocks from the current slide and makes them draggable

---

## Slide Separator Reference

```
---           Separates slides (must be on its own line with blank lines above/below)
|||           Splits content into two columns (simpler alternative to positioning)
--            Fragment break for progressive reveal (content hidden until click)
[@...]        Starts a positioned block (absolute placement on slide)
???           Starts speaker notes (hidden from presentation)
<!-- -->      Per-slide theme override (bg, text, font, align, padding, size)
```diagram    Renders a flowchart/diagram from text DSL ([Node] --> [Node])
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

## PDF Export

Click **PDF** to export your deck as a PDF via the browser's print dialog.

- Each slide renders as a full landscape page
- All fragments are shown (no progressive reveal in PDF)
- Per-slide theme overrides (backgrounds, colors) are preserved
- Syntax highlighting, diagrams, and columns carry through
- Select "Save as PDF" in the print dialog

### Tips
- Use Chrome/Edge for best PDF quality
- Set margins to "None" in print settings for full-bleed slides
- The dark background prints correctly (enable "Background graphics" in print options if needed)

---

## PPTX Export

Click **PPTX** to download a `.pptx` file. The export:
- Applies your current design tokens (colors, fonts) to the PowerPoint slides
- Converts markdown formatting to PPTX text runs (bold, italic, code, bullets)
- Renders two-column layouts as side-by-side text boxes
- Per-slide theme overrides applied to individual slide backgrounds
- Progressive reveal fragments expanded into duplicate slides
- Uses dark/light background from your theme
- Opens in PowerPoint, Keynote, and Google Slides
- Tables rendered as formatted text rows with bold header + underline separator
- Images appear as `[image: url]` placeholders (full embedding coming soon)

---

## Example: Complete Deck (showcasing all features)

```markdown
<!-- bg: #0f172a, text: #e2e8f0, align: center -->

# Q4 Product Update

Engineering Team — December 2026

---

## What We Shipped

- [x] User authentication v2
- [x] Dashboard redesign
- [x] API rate limiting
- [ ] Mobile app beta (in progress)

--

#### And what we learned along the way...

---

## Performance: Before vs After

- API latency: **420ms**
- Page load: **3.2s**
- Error rate: **2.1%**

|||

- API latency: **180ms** ↓57%
- Page load: **1.1s** ↓66%
- Error rate: **0.3%** ↓86%

---

## Key Insight

The single biggest improvement came from one change:

--

```python
# New caching layer
@cache(ttl=300)
def get_user(id):
    return db.users.find(id)
```

--

> Reduced database queries by ==73%==

---

## Next Quarter

| Initiative | Owner | Target |
|-----------|-------|--------|
| Mobile beta | Sarah | Jan 15 |
| API v3 | Mike | Feb 1 |
| Analytics | Chen | Feb 15 |

???
Budget discussion is confidential — only share if asked directly.
Mobile beta delay was due to iOS review process, not engineering.

---

<!-- bg: #7c3aed, text: #ffffff, align: center -->

# Part Two

## Strategic Outlook

---

## Market Position

[@ x:5% y:20% w:45%]
### Strengths
- 98% uptime SLA
- 2M+ active users
- Zero-knowledge encryption

[@ x:55% y:20% w:40%]
### Opportunities
- Mobile market untapped
- Enterprise pilot pipeline
- API marketplace

[@ x:15% y:80% w:70% align:center]
*Source: Internal analysis, Q4 2026*

---

<!-- bg: #0f172a, text: #e2e8f0, align: center -->

# Thank You

Questions?

???
If asked about headcount: we're hiring 12 engineers in Q1.
If asked about competitors: redirect to the product differentiation slide.
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
