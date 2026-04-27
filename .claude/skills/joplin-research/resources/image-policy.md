# Image Policy

## Decision Criteria

Include an image only when it communicates structural relationships, data patterns, spatial/temporal flows, or mathematical/geometric concepts more efficiently than prose. The standard: **"Would this appear in a peer-reviewed paper or technical whitepaper?"** If yes, include it. If it's decorative, branding, or restates a single sentence — skip it.

## High-Value Image Types

- Architecture diagrams
- System/network topology
- Flowcharts and state machines
- Sequence diagrams and protocol handshakes
- Data flow / pipeline visualizations
- Mathematical or geometric relationship diagrams
- Scientific charts and graphs (benchmark results, performance curves)
- ER diagrams and schema visualizations
- Annotated UI screenshots showing non-obvious interaction patterns

## Exclude List

- Logos, icons, badges/shields
- Stock photos and memes
- Screenshots of text or terminal output (use code blocks instead)
- Trivial diagrams that restate a single sentence

## Sourcing Workflow

1. **Organic discovery**: During normal `web_fetch`, inspect image references (`![...](...))` when surrounding context (alt text, heading, caption, nearby paragraph) suggests a high-value diagram. Fetch the image URL directly to verify it loads and is a real diagram (not a sprite sheet, placeholder, or tracking pixel).
2. **Targeted search**: When a section clearly warrants a visual but none was found organically, use `web_search` to find diagrams from official documentation or reputable technical sources.
3. **Never fabricate**: Do not hallucinate or guess image URLs. Only include images from URLs you have actually fetched or confirmed.

Record qualifying image URLs, alt text, source page, and a proposed caption as you go — don't try to reconstruct these after the fact.

## Quantity Guidelines

These are **ceilings, not targets** — zero images is fine if nothing meets the bar.

| Template | Image Ceiling |
|----------|---------------|
| Technical Rundown | 1-4 |
| Technical Survey | 0-2 |
| Whitepaper Summary | 0-2 |
| Article Summary | 0-1 |
| Book Summary | 0 (rarely applicable) |
| Research Notes | 0-1 |

## Formatting

Use the `<figure class="img-center">` pattern from joplin-formatting Rule 9. Every image must have:
- `width="600px"` default (adjust as needed)
- Descriptive `alt` attribute (never opaque filenames like `"diagram1.png"`)
- `<figcaption>` with sequential numbering: "Figure 1. Description"
