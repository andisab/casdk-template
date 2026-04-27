# Element Catalog — Joplin Special Elements

Copy-paste reference for HTML elements and special syntax patterns used in Joplin notes.
Load this file when you need the exact syntax for a specific element type.

## Callout Boxes

Three types available. Each uses the same HTML structure with a different class name.

> **⚠️ Markdown does NOT render inside `<div>` blocks in Joplin.** All content inside callout boxes must use HTML tags (`<code>`, `<strong>`, `<em>`, `<a href>`, `<br>`) — never raw markdown like backticks, `**bold**`, or `[links](url)`.

### Idea Callout
```html
<div class="idea">
  <div class="idea-title">Idea</div>
Your idea content goes here. Can include multiple paragraphs, code, lists, etc.
</div>
```
**When to use**: Insights, suggestions, creative thoughts, alternative approaches.

### Todo Callout
```html
<div class="todo">
  <div class="todo-title">Todo</div>
Your todo content goes here. Renders with a circular checkmark icon.
</div>
```
**When to use**: Action items, tasks, reminders, follow-up items.

### Warning Callout
```html
<div class="warning">
  <div class="warning-title">Warning</div>
Your warning content goes here. Renders with an exclamation icon.
</div>
```
**When to use**: Important cautions, security notes, critical information, breaking changes.

### Callout with Custom Title and HTML Content
The title text is customizable — the CSS `::before` pseudo-element generates the icon ("i", "✓", "!") automatically. Put any text you want in the title div.
```html
<div class="warning">
  <div class="warning-title">Breaking Change in v3.0</div>
The <code>legacy_api()</code> endpoint has been removed.<br>
Use <code>v2_api()</code> instead. See the <a href="https://docs.example.com/migration">migration guide</a>.
</div>
```

```html
<div class="idea">
  <div class="idea-title">Performance Tip</div>
Enable <code>--parallel</code> flag to reduce build time by <strong>40%</strong>.
</div>
```

## Images

Convert standard markdown images to HTML `<figure>` elements for proper styling.

### Markdown image (convert FROM this):
```markdown
![image.png](:/76cd4725a4e0415c9c36e5fc90c3c19d)
```

### HTML figure — Joplin resource (convert TO this):
```html
<figure class="img-center">
  <img src=":/76cd4725a4e0415c9c36e5fc90c3c19d" alt="Description of image">
  <figcaption>Figure 1. Caption describing the image content.</figcaption>
</figure>
```

### HTML figure — External URL:
```html
<figure class="img-center">
  <img src="https://example.com/diagram.png" alt="Architecture diagram">
  <figcaption>Figure 2. System architecture overview.</figcaption>
</figure>
```

### HTML figure — Narrower width override:
```html
<figure class="img-center">
  <img src=":/abc123" alt="Small icon" width="200px">
  <figcaption>Figure 3. Application icon.</figcaption>
</figure>
```

- Always use `class="img-center"` — a bare `<figure>` gets no centering or width styling.
- Use 2-space indentation inside `<figure>` blocks.
- Adjust narrower (e.g., `width="200px"`) or wider as needed.
- Preserve the Joplin resource ID (`:/<hash>`) in `src` for local resources.
- Always include a descriptive `alt` attribute.
- Number figures sequentially: Figure 1, Figure 2, etc.

## Blockquotes

### Primary use — Table of Contents:
```markdown
>[toc]
```
Place at the very beginning of the document, before any headings.

### Secondary use — Tips and quotes:
```markdown
> **Pro tip**: Always validate user input on both client and server side to prevent injection attacks.
```
CSS renders blockquotes with: dotted border, 5px border-radius, light-gray background, italic text, 0.85 opacity.

## Task Lists

```markdown
- [ ] Unchecked item (renders normally)
- [x] Checked item (CSS renders italic with reduced opacity)
- [ ] Another unchecked item
```
Note: Checked items get CSS styling that makes them appear "completed" (italic + reduced opacity).

## Links

### Standard link list:
```markdown
- [Official Documentation](https://docs.example.com)
- [GitHub Repository](https://github.com/org/project)
- [Tutorial Series](https://learn.example.com)
```

### Sub-label format (using h6):
```markdown
###### [GitHub: Repository](https://github.com/org/project): *Description of what you'll find*
```

## CLI Commands

Format as backtick command followed by italic description:
```markdown
- `npm install package`: *Installs the specified package*
- `git commit -m "message"`: *Creates a commit with a message*
- `docker build -t name .`: *Builds a Docker image with specified tag*
```

## Advantages & Disadvantages

Use escaped characters to prevent markdown list rendering:
```markdown
\+ This is an advantage or positive aspect
\+ Another benefit or strength
\- This is a disadvantage or limitation
\- Another concern or weakness
```

## Error/Highlight Spans

Use for deprecation notices, critical values, or error states. Renders in faded red (`#9d0006`).

```html
<span class="error">DEPRECATED</span> — this method will be removed in v4.0.
```

```html
Status: <span class="error">FAILED</span> — see logs for details.
```

## Code Blocks

Always specify the language for syntax highlighting:
```markdown
```python
def example_function():
    """This is a docstring"""
    return "formatted code"
`` `
```

Supported languages include: python, javascript, typescript, bash, css, html, go, rust, java, sql, json, yaml, and more.
One blank line before and after code blocks.
