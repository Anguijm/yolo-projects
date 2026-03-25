# Tale Weaver

Interactive fiction engine with a pre-loaded sci-fi survival story. Branching narrative, inventory system, stat tracking, conditional choices. Make decisions, gather items, shape the outcome.

## The Story: Station Erebos

You wake on a damaged deep space research station. A crystalline organism has breached the hull and is eating through the structure. You have minutes to decide: seal the breach, call for help, trigger a lockdown — or some combination. Your choices determine who lives and who dies.

**4 possible endings** — from self-sacrifice to strategic triumph.

## Features

### Narrative Engine
- JSON-based node graph with branching choices
- ~15 story nodes with 4 distinct endings
- Simple markdown rendering (*italic*, **bold**, paragraph breaks)
- Choices navigate between nodes with state side-effects

### State System
- Inventory: pick up items (flashlight, keycard), use them later
- Stats: health and trust values change based on decisions
- Conditional choices: some options require specific items or minimum stat values
- Locked choices shown dimmed with requirement text

### UI
- Typography-focused reading interface (Georgia serif, 1.8 line-height)
- Sidebar showing live stats (color-coded by value) and inventory
- Step counter tracking decision depth
- Scroll-to-top on each new passage
- Restart button and replay on ending

### Architecture
- Pure DOM/text rendering (no Canvas — total break from recent builds)
- Story defined as JSON object with nodes, choices, actions, conditions
- Action types: item (add to inventory), stat (modify value), set (flag)
- Condition types: item (requires possession), stat (requires minimum)
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Read the story. Make choices. Explore different paths to discover all 4 endings. Try to escape Station Erebos with everyone alive.
