# CSS Reference — Joplin Custom Stylesheet

This is a lookup reference for the user's custom Joplin CSS (userstyle.css and userchrome.css).
Load this file only when you need to understand WHY a formatting rule exists or need specific
CSS values. The formatting RULES themselves are all in SKILL.md.

## Typography Stack

| Element | Font Family | Size | Weight | Notes |
|---------|-------------|------|--------|-------|
| h1 | Bitter (serif) | 2rem | 500 | Has `border-bottom`. Rarely used — Joplin note title serves as h1. |
| h2 | Bitter (serif) | 1.8rem | 400 | Has `border-bottom`. Main section headings. |
| h3 | Bitter (serif) | 1.5rem | 400 | NO border-bottom — gets manual `---` separator instead. |
| h4 | Bitter (serif) | 1.25rem | 400 | Regular subheading. No special CSS treatment. |
| h5 | Bitter (serif) | 1.25em | 400 | Detail-level heading. No special CSS treatment. |
| h6 | Sans-serif | 0.9rem | 600 | Differentiated from main headings. Used for sub-labels. |
| Body text | Inter (sans-serif) | 14px | 300 | High readability for extended reading. |
| Code (block & inline) | Fira Code (monospace) | 12px | — | Programming ligatures enabled. |

## Color Palette

### Heading Colors

| Heading | Hex | Description |
|---------|-----|-------------|
| h1 | `#000000` | Black |
| h2 | `#942001` | Dark red |
| h3 | `#13505B` | Dark teal |
| h4 | `#8BAAAD` | Muted teal |
| h5 | `#a89984` | Warm gray |
| h6 | `#4d4d4d` | Dark gray |

### UI Element Colors

| Element | Color | Notes |
|---------|-------|-------|
| Body text | `#4d4d4d` | Dark gray — high contrast without harsh black |
| Links | `#8BAAAD` | Muted teal (h4 color) |
| Links (visited) | `#13505B` | Dark teal (h3 color) |
| Links (hover) | `#3486f3` | Bright blue |
| Code background | `#f5f5f5` | Light gray — subtle differentiation |
| `.error` | `#9d0006` | Faded red — for deprecation/error highlights |

### Callout Colors

| Type | Background | Icon BG | Icon Color | Icon Char |
|------|-----------|---------|------------|----------|
| `.idea` | `rgba(245,199,15, 0.1)` | `rgba(245,199,15, 0.3)` | `#8B7A0B` | "i" |
| `.todo` | `rgba(139,170,173, 0.15)` | `rgba(139,170,173, 0.4)` | `#5A7A7D` | "✓" |
| `.warning` | `rgba(148,32,1, 0.1)` | `rgba(148,32,1, 0.3)` | `#942001` | "!" |

### Gruvbox-Inspired Full Palette

Available as CSS variables for custom `<span style="color:var(--name)">` if needed.

| Category | Name | Hex |
|----------|------|-----|
| Bright | `--bright_red` | `#fb4934` |
| Bright | `--bright_green` | `#b8bb26` |
| Bright | `--bright_yellow` | `#fabd2f` |
| Bright | `--bright_blue` | `#3486f3` |
| Bright | `--bright_blue2` | `#458588` |
| Bright | `--bright_blue3` | `#0999b3` |
| Bright | `--bright_purple` | `#d3869b` |
| Bright | `--bright_aqua` | `#8ec07c` |
| Bright | `--bright_orange` | `#fe8019` |
| Neutral | `--neutral_red` | `#cc241d` |
| Neutral | `--neutral_green` | `#98971a` |
| Neutral | `--neutral_yellow` | `#d79921` |
| Neutral | `--neutral_blue` | `#83a598` |
| Neutral | `--neutral_purple` | `#b16286` |
| Neutral | `--neutral_aqua` | `#689d6a` |
| Neutral | `--neutral_orange` | `#d65d0e` |
| Faded | `--faded_red` | `#9d0006` |
| Faded | `--faded_green` | `#79740e` |
| Faded | `--faded_yellow` | `#b57614` |
| Faded | `--faded_blue` | `#076678` |
| Faded | `--faded_purple` | `#8f3f71` |
| Faded | `--faded_aqua` | `#427b58` |
| Faded | `--faded_orange` | `#af3a03` |
| Light | `--light0` | `#fbf1c7` |
| Light | `--light1` | `#ebdbb2` |
| Light | `--light3` | `#bdae93` |
| Light | `--light4` | `#a89984` |
| Dark | `--dark-gray` | `#4d4d4d` |
| Dark | `--dark_green` | `#0d610e` |

## CSS Border Behaviors

This is the key reason behind the `---` horizontal rule policy:

- **h1**: Has `border-bottom` → Adding `---` creates a visible double line. NEVER add `---`.
- **h2**: Has `border-bottom` → Adding `---` creates a visible double line. NEVER add `---`.
- **h3**: NO `border-bottom` → `---` provides the visual separator. Add `---` consistently.
- **h4, h5, h6**: No `border-bottom` → But `---` is NOT used either. These are lightweight sub-headings.

## Other CSS Details

- **Blockquotes**: `border: 1px dotted`, `border-radius: 5px`, `border-color: var(--light-gray)`, italic text, `opacity: 0.85`
- **Task list checked items**: `.checkbox-label-checked` renders italic with `opacity: 0.65`
- **Inline code**: `.inline-code` — `#f5f5f5` background, Fira Code 12px, `border-radius: 3px`, `padding: 0.3em`
- **`.error`**: `color: var(--faded_red)` (`#9d0006`) — inline red text for error/deprecation states
- **`.resource-icon`**: `background-color: var(--light-gray)` — styling for PDF/attachment icons
- **`#rendered-md`**: `padding: 3%` — container padding for the rendered note body
- **Callout boxes**: `margin: 12px 0`, `padding: 0.75em 1em`, `border-radius: 4px`, no border
- **Figures**: `figure { margin: 20px auto }`, `figure.img-center { width: 80%; text-align: center }`, `figcaption { font-size: 0.9em; font-style: italic }`

## Print Styles (`@media print`)

| Behavior | CSS Rule |
|----------|----------|
| h1, h2 start new page | `page-break-before: always` |
| Code blocks don't split | `pre { page-break-inside: avoid }` |
| Tables don't split | `table { page-break-inside: avoid }` |
| Callouts don't split | `.idea, .todo, .warning { page-break-inside: avoid }` |
| Figures don't split | `figure, img { page-break-inside: avoid }` |
| Links show URL | `a[href^="http"]:after { content: " (" attr(href) ")" }` |
| Body font size | `10pt` |
| Code font size | `8pt` |
| Widow/orphan control | `widows: 3; orphans: 3` |
