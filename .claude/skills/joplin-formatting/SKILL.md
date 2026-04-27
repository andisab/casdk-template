---
name: joplin-formatting
description: >
  Joplin-compatible markdown formatting rules with strict heading hierarchy,
  spacing, and CSS-aware styling. Activates for any Joplin note creation or
  reformatting task. Also invoked by joplin-research skill.
---

⚠️ MANDATORY: Do NOT begin any editing until you have read this entire file. Complete reading the skill first, then begin work.

**Activate this skill when**:
- User mentions "Joplin" or requests markdown for note-taking
- User asks to "format", "reformat", "clean up", or "fix formatting" on a note
- Invoked by the `joplin-research` skill for any research output
- User explicitly requests content following their markdown preferences

**Reformat workflow**: When reformatting an existing note, apply rules in order:
fix heading hierarchy first → fix spacing → fix horizontal rules → fix special elements.

<formatting_rules>
## Rules — follow ALL of these on EVERY response

### 1. Heading Hierarchy
- **h1 (`#`)**: Reserved for document title only, rarely used. NEVER duplicate.
  *Why: Joplin uses the note title as h1. A second h1 creates visual redundancy and breaks the CSS border-bottom styling.*
- **h2 (`##`)**: Main document or chapter sections. Has CSS `border-bottom` — NEVER add `---` after h2.
- **h3 (`###`)**: Primary section dividers. The ONLY heading that gets `---` underneath.
- **h4 (`####`)**: Sub-sections within h3. No `---`, no special formatting.
- **h5 (`#####`)**: Detail-level sections. No `---`, no special formatting.
- **h6 (`######`)**: Less frequent. For emphasis, sub-labels, or 1-paragraph comments. Often used as: `###### [GitHub: Repo](url): *description*`

### 2. Spacing
- **Two blank lines** BEFORE every h2 heading
- **One blank line** BEFORE h3, h4, h5, h6 headings
- **ZERO extra blank lines** AFTER any heading — content starts immediately on the next line
- **Heading-to-heading transitions**: When a heading is immediately followed by another heading (no content between them), the "blank line(s) before" rule of the **next** heading takes precedence. E.g., h2 followed directly by h3: place one blank line between them (satisfying h3's requirement). Do NOT add filler content just to avoid this pattern.
- **One blank line** between content paragraphs — no more
  *Why: Joplin's CSS adds padding around headings. Extra blank lines create double-spacing that looks broken.*

### 3. Horizontal Rules (`---`)
- `---` goes ONLY under h3 headings. Be consistent: if one h3 has it, all h3s in the document should.
- NEVER place `---` under h1 or h2 — they already have CSS `border-bottom`.
- NEVER place `---` under h4, h5, or h6.
  *Why: h1/h2 have border-bottom in the custom CSS. Adding `---` creates a double line. h3 lacks this CSS border, so `---` provides visual separation.*

### 4. Table of Contents
- Use `>[toc]` at the very start of documents longer than 4-5 pages.
- **No blank line** after `>[toc]` — the first `##` heading follows immediately on the next line.
- This is an exception to the "two blank lines before h2" rule. The first h2 after `>[toc]` gets zero blank lines before it.

### 5. Links
- Standard format: `- [Descriptive Text](URL)`
- Sub-label format: `###### [Source: Title](URL): *description*`

### 6. Code Blocks & Inline Code
- Fenced code blocks: ALWAYS specify the language tag (```python, ```bash, etc.)
- One blank line before and after code blocks.
- Inline code: backticks for all technical terms, commands, filenames.
- CLI commands in lists: `` `command`: *Brief description* ``

### 7. Advantages & Disadvantages
- Use escaped `\+` and `\-` — NOT bullet points.
  *Why: Unescaped `+` and `-` render as list markers in markdown, breaking the intended format.*
```markdown
\+ This is an advantage
\- This is a disadvantage
```

### 8. Content Density
- Maximize information density. Minimize blank lines.
- If in doubt, use LESS spacing rather than more.
- CLI commands follow compact formatting like all other content.
- **Index (bibliography) entries**: NO blank lines between entries. Each `<a id="ref-N"></a>` line follows immediately after the previous one.

### 9. Images
- ALWAYS convert markdown `![alt](src)` to HTML `<figure class="img-center">`.
- A bare `<figure>` without `img-center` gets no centering or width styling from the CSS.
- Use 2-space indentation inside `<figure>` blocks.
- Always include `width="600px"` on `<img>` as the default. Adjust narrower or wider as needed.
- Always include `<figcaption>` with sequential numbering: "Figure 1. Description"
- Always include a descriptive `alt` attribute on `<img>`.
- For Joplin resources, preserve the `:/hash` in `src`. For external images, use the full URL.
- For full syntax, see `resources/element-catalog.md`.

### 10. Callout Boxes
- Three CSS classes: `idea` (yellow, "i" icon), `todo` (teal, "✓" icon), `warning` (red, "!" icon).
- Title text is customizable — the icon comes from CSS `::before`, not from the text content. E.g., `<div class="idea-title">Key Insight</div>` renders the "i" icon followed by "Key Insight".
- **No markdown inside callouts.** Joplin does NOT render markdown inside HTML `<div>` blocks. Use HTML tags instead: `<code>`, `<strong>`, `<em>`, `<a href="...">`, `<br>` for line breaks.
- Do NOT nest callout divs inside each other.
- No extra blank lines needed before/after callout `<div>` blocks — CSS handles margin (12px).
- For full syntax, see `resources/element-catalog.md`.

### 11. Tables
- Standard markdown tables with compact spacing.
- Use header row for column labels.
- Keep column widths reasonable.

### 12. Lists
- Unordered: `-` with 2-space indent for nesting.
- Ordered: `1.`, `2.`, `3.`
- Task lists: `- [ ]` unchecked, `- [x]` checked.

### 13. Error/Highlight Spans
- Use `<span class="error">text</span>` for red-highlighted inline text.
- Renders in faded red (`#9d0006`). Use for deprecation notices, critical values, or error states.

### 14. Print Considerations
- h1 and h2 headings trigger `page-break-before: always` in print/PDF — each major section starts a new page.
- Code blocks, tables, callouts, and figures have `page-break-inside: avoid` — they will not split across pages.
- Printed links append the URL in parentheses after the link text.
- Keep these behaviors in mind when structuring long documents intended for print or PDF export.
</formatting_rules>

## Output Skeleton

Use this heading and spacing pattern. Replace PLACEHOLDERS with content:

```markdown
>[toc]
## DOCUMENT_TITLE
INTRODUCTORY_PARAGRAPH starts immediately after the heading. No blank line between heading and first line of content.


## MAJOR_SECTION OR CHAPTER
SECTION_CONTENT starts immediately — no blank line after h2.

### SECTION
---
CONTENT starts immediately after separator. This is the ONLY heading level with `---`.

#### SUB_SECTION
CONTENT starts immediately — no blank line after h4, no `---`.

##### DETAIL_SECTION
MORE_CONTENT.

## SECTION_WITH_NO_BODY_TEXT

### SUBSECTION_HEADING
---
CONTENT here. (Heading-to-heading transition: h3's "one blank line before" rule applies.)


## NEXT_MAJOR_SECTION
CONTENT continues.
```

<example>
### ✅ Correct Formatting
```markdown
>[toc]
## FastAPI Framework
FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+.


## Overview

### Key Features
---
FastAPI leverages Python type hints for automatic validation and documentation.

#### Async Support
Built on Starlette, FastAPI provides first-class async/await support.

##### Performance Benchmarks
Comparable to NodeJS and Go in independent benchmarks [1].

**Advantages & Disadvantages**:
\+ Automatic OpenAPI documentation generation
\+ Native async support with excellent performance
\- Smaller ecosystem compared to Django or Flask
\- Limited built-in admin interface
```
</example>

<example>
### ❌ Common Violations
```markdown
## FastAPI Framework            ← Missing >[toc] for long document

---                             ← WRONG: --- after h2 (CSS already has border-bottom)

### Key Features                ← Missing --- after h3 (inconsistent with other h3s)

FastAPI leverages Python...     ← Content should start on the line immediately after ---

#### Async Support

                                ← WRONG: Extra blank line after heading
Built on Starlette...

+ Automatic OpenAPI docs        ← WRONG: Unescaped +, renders as list marker
- Smaller ecosystem             ← WRONG: Unescaped -, renders as list marker

```python                       ← WRONG: Missing language tag on code block
```
</example>

## Pre-Output Self-Check

Before generating or delivering ANY Joplin markdown, verify:
- [ ] No `---` after h1 or h2 headings? (`---` ONLY after h3)
- [ ] Two blank lines before h2, one blank line before h3/h4/h5/h6, ZERO after any heading?
- [ ] `>[toc]` present at document start for long documents?
- [ ] Code blocks have language tags? Advantages use `\+`/`\-`?
- [ ] Proper heading hierarchy maintained (no jumps like h2 → h5)?
- [ ] Images use `<figure class="img-center">` with `<figcaption>` and sequential numbering?
- [ ] Callout boxes use HTML-only content (no raw markdown inside `<div>` blocks)?
- [ ] No nested callout divs?

## Mechanical Validation (MANDATORY for file output)

After creating the output file and BEFORE presenting it to the user, run the validator:

```bash
python3 ~/.claude/skills/joplin-formatting/resources/validate_joplin_md.py <output-file.md>
```

If the validator reports errors, fix them (manually or with `--fix`) and re-run until clean:

```bash
python3 ~/.claude/skills/joplin-formatting/resources/validate_joplin_md.py <output-file.md> --fix
```

Do NOT present the file to the user until the validator passes with 0 errors. Warnings are acceptable but should be reviewed.

**Reference files** (load on demand for syntax lookups):
- `resources/validate_joplin_md.py` — Mechanical validator script (run before delivery)
- `resources/css-reference.md` — Typography stack, font sizes, color palette, CSS border behaviors
- `resources/element-catalog.md` — Full HTML syntax for callout boxes, `<figure>` images, task lists, blockquotes
