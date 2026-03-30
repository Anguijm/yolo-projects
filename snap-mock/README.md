# snap-mock

Browser-based UI screenshot mockup generator. Pick a device frame, paste or type content, customize the background, and export a clean PNG — zero dependencies, fully offline.

## Features

- **5 device frames**: iPhone 15, Android phone, iPad, MacBook, Desktop browser
- **3 content modes**: paste an image (clipboard or file), type raw HTML, or set a URL bar
- **Customizable backgrounds**: solid color presets + custom picker, or 12 gradient presets
- **Controls**: padding, shadow intensity, device scale slider
- **Export presets**: Auto (2x), Twitter card, OG image, Instagram, LinkedIn, 1080p
- **PNG export** via Canvas + SVG foreignObject (aspect-ratio-preserving)
- Zero dependencies — single HTML file, works offline

## Usage

1. Open `index.html` in a browser
2. Pick a device frame from the left panel
3. Load content:
   - **Image mode**: press `Ctrl+V` to paste a screenshot, or click "browse..." to upload
   - **HTML mode**: type HTML into the textarea and click "Apply"
   - **URL bar mode** (browser frame): type a URL to show in the address bar
4. Customize background, padding, shadow, and scale
5. Choose an export preset (or leave on Auto for 2x resolution)
6. Click **Export PNG** to download

## Use cases

- Slide decks (Markdown Deck, PowerPoint, etc.)
- Portfolio screenshots
- Social media cards (Twitter, LinkedIn, OG images)
- Documentation illustrations
- App store screenshots

## Technical notes

- Export uses SVG `<foreignObject>` to capture the styled DOM, then draws to Canvas
- Aspect ratio is preserved when fitting into preset canvas sizes (letterbox)
- Blob URLs are revoked after export to prevent memory leaks
- Gradient parser handles `rgb()` / `rgba()` colors correctly via paren-aware splitting
