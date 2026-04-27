---
name: joplin-research
description: >
  Research content templates and citation standards for Joplin notes. Routes to
  the correct template based on request type. Delegates all markdown formatting
  to the joplin-formatting skill.
---

⚠️ MANDATORY: Do NOT begin any research, web searches, or content generation until you have read this entire file, the joplin-formatting SKILL.md, AND the matching template from the routing table below. Complete all three reads first, then begin work.

**Activate this skill when**:
- User requests a "Technical Rundown", "technical rundown", "technical survey", "book summary", "article summary", or "whitepaper summary"
- User requests any research document intended for Joplin
- User uses phrases like "What's new with...", "Compare these tools...", "Summarize this..."

**Before generating output**:
1. Read and apply all rules from the `joplin-formatting` skill for markdown structure and spacing.
2. Identify the correct template from the routing table below and read its resource file.
3. Apply the citation rules in this file to all factual claims.

## Research Format Routing Table

| Trigger Phrase | Template File | Typical Length |
|----------------|---------------|----------------|
| "Technical Rundown of..." | `~/.claude/skills/joplin-research/resources/templates/technical-rundown.md` | 4–12+ pages |
| "Technical Survey of..." | `~/.claude/skills/joplin-research/resources/templates/technical-survey.md` | 2–4 pages |
| "Book Summary of..." | `~/.claude/skills/joplin-research/resources/templates/book-summary.md` | 2–4 pages |
| "Article Summary of..." | `~/.claude/skills/joplin-research/resources/templates/article-summary.md` | 1–2 pages |
| "Whitepaper Summary of..." | `~/.claude/skills/joplin-research/resources/templates/whitepaper-summary.md` | 2–4 pages |
| "What's New with..." | `~/.claude/skills/joplin-research/resources/templates/research-notes.md` | ½–1 page |
| General research / notes | `~/.claude/skills/joplin-research/resources/templates/research-notes.md` | varies |

**Read the matching template file before generating output.** If no trigger phrase matches exactly, use `research-notes.md` as the default template.

**Content Depth Policy**
- Research output should be **as long as the material warrants**. Do NOT
  summarize or condense to hit a page target.
- If extended search produced detailed findings, preserve that detail in
  the formatted output. Formatting is a *presentation layer*, not a filter.
- When the formatted output would exceed ~4,000 words, use **iterative
  file creation**: write the document section-by-section using multiple
  `Write` / `Edit` calls rather than generating everything in a single pass.

<citation_rules>
## Citation Standard — applies to ALL templates

### Inline Citations
- Use clickable numbered references with HTML anchors: `<a href="#ref-1">[1]</a>`, `<a href="#ref-2">[2]</a>`
- Place AFTER the claim, BEFORE the period: `"Claude was released in 2023 <a href="#ref-1">[1]</a>."`
- Multiple sources for one claim: `<a href="#ref-1">[1]</a><a href="#ref-2">[2]</a>` or `<a href="#ref-1">[1]</a>, <a href="#ref-2">[2]</a>`
- Same source cited multiple times: reuse the same number and anchor
- Number sequentially in order of first appearance in the document

### Index Section (Bibliography)
- Always placed at the END of the document, after all content sections
- Use `### Index` heading with `---` separator (per joplin-formatting rules)
- **"Key Resources"** (curated links in Overview) vs **"Index"** (bibliography at end): Key Resources are hand-picked links for the reader to explore. The Index is the numbered bibliography of all cited sources. Keep them distinct.
- Each entry is prefixed with an HTML anchor: `<a id="ref-N"></a>` so inline citations link to it
- Entry format: `<a id="ref-N"></a>N. Author/Organization. "[Title](URL)." *Source/Publication*. Date.`
- **Title is the link** — embed the URL in the title text. Do NOT append a separate `[Link](URL)` at the end.
- If no author: use organization name
- If no date: use "n.d." or "Accessed YYYY-MM-DD"
- If no URL: omit URL but include all other fields
- Dates are **mandatory** for articles and blog posts — use publication date or "Accessed YYYY-MM-DD"
- NEVER fabricate URLs — only cite sources actually visited or returned by search

### Example
```markdown
### Index
---
<a id="ref-1"></a>1. Anthropic. "[Claude 3.5 Sonnet Model Card](https://docs.anthropic.com/...)." *Anthropic Documentation*. 2024.
<a id="ref-2"></a>2. Vaswani, A. et al. "[Attention Is All You Need](https://arxiv.org/abs/1706.03762)." *NeurIPS*. 2017.
<a id="ref-3"></a>3. Mozilla. "[MDN Web Docs: Fetch API](https://developer.mozilla.org/...)." *MDN*. Accessed 2025-01-15.
```

### When Citations Are Required
| Template | Required? | What to Cite |
|----------|-----------|--------------|
| Technical Rundown | Yes | Official docs, benchmarks, adoption data |
| Technical Survey | Yes | Each tool's docs, comparison sources, market data |
| Book Summary | Minimal | The book itself + any supplementary sources consulted |
| Article Summary | Yes | The article + sources referenced within it |
| Whitepaper Summary | Yes | The paper + key references it cites |
| Research Notes | Yes | All sources used during research |

### Capturing Sources from Web Search
When using the web search tool during research:
- Capture: page title, domain/organization, date (if visible), full URL
- Record sources as you find them — don't try to reconstruct URLs from memory after the fact
- If a source was used but URL is uncertain: `[N] "Title." *Source*. [URL not confirmed]`
</citation_rules>

<image_policy>
When research output would benefit from diagrams (architecture, flowcharts, data visualizations),
apply the image policy in `~/.claude/skills/joplin-research/resources/image-policy.md`. The policy
defines decision criteria, high-value image types, sourcing workflow, and per-template quantity ceilings.
Format all images per joplin-formatting Rule 9.
</image_policy>

## Two-Phase Workflow for Long Documents

**Working directory**: Always write draft files to `~/Documents/ClaudeResearch/drafts/`.
Use a slug derived from the note title (e.g., `~/Documents/ClaudeResearch/drafts/docker-compose.md`).
This directory is always writable. Do NOT use `/tmp/` or project directories.

1. **Content phase**: Write the full document to a file in `~/Documents/ClaudeResearch/drafts/`
   with all research detail, using correct heading hierarchy and citations, but don't obsess
   over spacing/separator rules yet. Focus on completeness — every
   substantive finding from the research phase should appear in the output.
   When `web_fetch` returns content containing image references, evaluate
   them against the image policy and capture qualifying URLs alongside
   citations. Use iterative `Write` + `Edit` calls to build the document
   section-by-section if it exceeds ~4,000 words.
2. **Format phase**: Run the validator (`validate_joplin_md.py`), fix any
   spacing/separator errors, and do a formatting cleanup pass. This phase
   should never remove content — only adjust whitespace, heading levels,
   and separator placement.

This separation prevents formatting concerns from competing with content
generation and ensures research depth is preserved through to the final output.

## Pre-Output Self-Check

Before delivering any research output, verify:
- [ ] Correct template file was read and followed?
- [ ] All joplin-formatting rules applied (heading hierarchy, spacing, `---` only after h3)?
- [ ] Inline citations `<a href="#ref-1">[1]</a>` present for factual claims?
- [ ] `### Index` section at the end with numbered bibliography (anchored entries)?
- [ ] No fabricated URLs — all links are from actual sources?
- [ ] Images (if any) meet the whitepaper-quality bar and use correct `<figure>` syntax?
- [ ] **Validator passed**: Run `python3 ~/.claude/skills/joplin-formatting/resources/validate_joplin_md.py ~/Documents/ClaudeResearch/drafts/<slug>.md` and fix all errors before presenting to user.

⚠️ If using extended search or any tool that returns pre-formatted content, treat that content as RAW INPUT that must be reformatted to match the template. Never deliver tool output directly.

**Full citation details**: `~/.claude/skills/joplin-research/resources/citation-guide.md`
