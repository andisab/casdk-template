# Citation Guide — Full Reference

This file expands on the citation rules in SKILL.md. Load this when you need guidance on
edge cases or citation formatting details beyond the basics.

## Inline Citation Format — Detailed Rules

### Placement
- Use clickable HTML anchors: `<a href="#ref-N">[N]</a>`
- Place citation AFTER the claim, BEFORE the period:
  `"FastAPI processes 9,000+ requests/second in benchmarks <a href="#ref-1">[1]</a>."`
- For claims spanning a full sentence, place at end:
  `"The framework was created by Sebastián Ramírez in 2018 and has since accumulated over 70k GitHub stars <a href="#ref-2">[2]</a>."`
- For claims within a compound sentence, place after the specific claim:
  `"FastAPI outperforms Flask in benchmarks <a href="#ref-1">[1]</a>, though Flask has a larger plugin ecosystem <a href="#ref-3">[3]</a>."`

### Multiple Sources
- Two sources: `<a href="#ref-1">[1]</a><a href="#ref-2">[2]</a>` or `<a href="#ref-1">[1]</a>, <a href="#ref-2">[2]</a>`
- Three or more: prefer comma notation `<a href="#ref-1">[1]</a>, <a href="#ref-2">[2]</a>, <a href="#ref-3">[3]</a>`

### Reusing Citations
- If the same source supports multiple claims, reuse its number and anchor
- Do NOT assign a new number to the same source
- Numbers should be sequential by first appearance only

### When NOT to Cite
- Common knowledge that any practitioner would know ("Python is an interpreted language")
- The user's own statements or requirements
- Your own analysis, opinions, or synthesis
- Structural or transitional sentences ("In this section, we'll examine...")

## Index Entry Formats

Every entry in the Index section gets an HTML anchor for clickable inline citations.
**No blank lines between entries** — each citation line follows immediately after the previous one.

**Format at a glance** (canonical pattern):
```
<a id="ref-N"></a>N. Author. "[Title](URL)." *Source*. Date.
```

### Standard web source
```
<a id="ref-N"></a>N. Organization. "[Page Title](URL)." *Site Name*. Date.
```
Example: `<a id="ref-1"></a>1. Anthropic. "[Claude 3.5 Sonnet](https://docs.anthropic.com/...)." *Anthropic Docs*. 2024.`

### Academic paper
```
<a id="ref-N"></a>N. Author(s). "[Paper Title](URL)." *Venue/Journal*. Year.
```
Example: `<a id="ref-2"></a>2. Vaswani, A. et al. "[Attention Is All You Need](https://arxiv.org/abs/1706.03762)." *NeurIPS*. 2017.`

### Book
```
<a id="ref-N"></a>N. Author. *Book Title*. Publisher. Year.
```
Example: `<a id="ref-3"></a>3. Kleppmann, M. *Designing Data-Intensive Applications*. O'Reilly. 2017.`

### GitHub repository
```
<a id="ref-N"></a>N. Organization/Author. "[Repository Name](URL)." *GitHub*.
```
Example: `<a id="ref-4"></a>4. tiangolo. "[FastAPI](https://github.com/tiangolo/fastapi)." *GitHub*.`

### Blog post or article
```
<a id="ref-N"></a>N. Author. "[Post Title](URL)." *Blog/Publication Name*. Date.
```
Date is **mandatory** for articles and blog posts — use publication date or "Accessed YYYY-MM-DD".
Example: `<a id="ref-5"></a>5. Ramírez, S. "[Introducing FastAPI](https://tiangolo.com/...)." *tiangolo.com*. 2018.`

### Documentation page
```
<a id="ref-N"></a>N. Organization. "[Page Title](URL)." *Documentation Name*. Accessed YYYY-MM-DD.
```
Example: `<a id="ref-6"></a>6. FastAPI. "[First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)." *FastAPI Documentation*. Accessed 2025-06-01.`

### Source with uncertain URL
```
<a id="ref-N"></a>N. "Title." *Source*. [URL not confirmed]
```
Use this ONLY when you know you used a source but cannot confirm the exact URL. Prefer omitting the source over fabricating a URL.

## Citation Requirements by Template Type — Expanded

### Technical Rundown
- **Required**: Official documentation, GitHub repo, key benchmark sources, adoption/market data
- **Typical count**: 5–15 citations
- **Key areas needing citation**: Performance claims, adoption statistics, pricing details, feature comparisons, release dates

### Technical Survey
- **Required**: Each tool's official docs, comparison/benchmark sources, market data
- **Typical count**: 10–25 citations (scales with number of tools compared)
- **Key areas needing citation**: Per-tool background facts, comparison table data, pricing, GitHub stars, adoption rates

### Book Summary
- **Required**: The book itself (always citation [1])
- **Optional**: Supplementary sources if you consult reviews, author interviews, or related works
- **Typical count**: 1–5 citations

### Article Summary
- **Required**: The article itself (always citation [1])
- **Expected**: Key sources the article references, if you can identify them
- **Typical count**: 2–8 citations

### Whitepaper Summary
- **Required**: The paper itself (always citation [1])
- **Expected**: Key references the paper cites that are important to understanding its contribution
- **Typical count**: 3–10 citations

### Research Notes / What's New
- **Required**: All sources consulted during research
- **Typical count**: 3–10 citations (scales with research depth)
- **Key areas needing citation**: Recent announcements, version changes, statistics, quotes
