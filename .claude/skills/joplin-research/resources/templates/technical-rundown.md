# Technical Rundown Template

**Trigger**: User requests "Give me a technical rundown of..." or similar deep-dive on a single tool
**Use Case**: Software engineering tools, libraries, frameworks, platforms, services
**Goal**: Condensed material for accelerated learning and technical proficiency
**Typical Length**: 4–12 pages (not counting citations section). Err on the side of thoroughness. Do NOT
condense research to fit a page target — include all substantive findings.

## Output Skeleton

Fill in PLACEHOLDERS with researched content. Preserve all heading levels, spacing, and
separator placement exactly as shown. Apply all joplin-formatting rules.

```markdown
>[toc]
## TOOL_OR_FRAMEWORK_NAME

### Overview
---
**General Information**: PROVIDE_CONTEXT. Address all of the following in flowing prose:
- How is it different from competitors?
- Who created it and when?
- How have adoption rates changed recently?
- What is its basic function and purpose?
- How does it work at a high level (1-paragraph explanation)?
- What are its key features and capabilities?

**Key Resources**:
- [Official Site](URL)
- [Documentation](URL)
- [GitHub Repository](URL)
- [Key Learning Resources](URL)
- [Community Forum / Discord / Slack](URL)

**Advantages & Disadvantages**:
\+ MAJOR_ADVANTAGE_OVER_COMPETITORS
\+ ANOTHER_KEY_STRENGTH
\+ UNIQUE_FEATURE_OR_CAPABILITY
\- NOTABLE_LIMITATION_OR_WEAKNESS
\- AREA_WHERE_COMPETITORS_MAY_EXCEL
\- POTENTIAL_DRAWBACK_OR_CONCERN

### Common Commands
---
- `COMMAND_SYNTAX`: *BRIEF_DESCRIPTION_OF_WHAT_IT_DOES*
- `ANOTHER_COMMAND`: *PURPOSE_AND_TYPICAL_USAGE*
- `THIRD_COMMAND`: *WHEN_AND_WHY_TO_USE_IT*
- `FOURTH_COMMAND`: *DESCRIPTION*

### ADDITIONAL_SECTION_1 (e.g., Architecture, Core Concepts, How It Works)
---
DETAILED_CONTENT_ABOUT_THIS_TOPIC.

#### SUBSECTION_IF_NEEDED
SUBSECTION_CONTENT.

### ADDITIONAL_SECTION_2 (e.g., Language Support, SDK Coverage)
---
SECTION_CONTENT.

### ADDITIONAL_SECTION_3 (e.g., Pricing / Licensing)
---
SECTION_CONTENT.

### ADDITIONAL_SECTION_4 (e.g., Market Position / Adoption)
---
MARKET_SHARE_DATA, GITHUB_STARS, DOWNLOAD_STATS, ADOPTION_TRENDS.

### ADDITIONAL_SECTION_N (as many as needed)
---
SECTION_CONTENT.

### Index
---
<!-- Index = numbered bibliography of all cited sources. Distinct from "Key Resources" (curated links in Overview). -->
<a id="ref-1"></a>1. FIRST_SOURCE_IN_BIBLIOGRAPHY_FORMAT
<a id="ref-2"></a>2. SECOND_SOURCE
<a id="ref-3"></a>3. THIRD_SOURCE
```

## Required Sections

Always include **Overview** and **Common Commands**. Additionally, include the following
sections when the information is relevant and available for the tool being documented:

| Section | Include When... |
|---------|-----------------|
| **Architecture / Core Concepts** | Tool has a non-trivial architecture worth understanding |
| **Getting Started / Installation** | Setup is non-obvious or has multiple paths |
| **Language Support / SDKs** | Tool supports multiple languages or has SDK options |
| **Pricing / Licensing** | Relevant tiers, free/open-source status, enterprise pricing |
| **Security & Deployment** | Cloud, on-premise, package manager, container options |
| **Market Position / Adoption** | GitHub stars, download stats, notable adopters, trend direction |
| **API Flexibility** | REST, GraphQL, SDK coverage, webhook support, extensibility |
| **Computational Requirements** | CPU/GPU, memory, storage, or scaling considerations |
| **Integration Capabilities** | Integrations with other tools, plugin ecosystems, middleware |
| **Roadmap / Recent Changes** | Active development, upcoming features, recent major releases |
| **Comparison with Alternatives** | Brief positioning vs. 2-3 closest competitors |

The exact section titles should be adapted to the specific tool — use descriptive names
that reflect the content (e.g., "Plugin Ecosystem" rather than generic "Integration Capabilities").

## Content Guidelines

- **Overview General Information** should read as flowing prose, not a bulleted checklist. Cover the listed points naturally within 2-4 paragraphs.
- **Common Commands** should include the 6-12 most essential commands a new user needs. Prioritize commands for getting started, daily usage, and common troubleshooting.
- **Advantages & Disadvantages** should be specific and substantive — not generic. "Fast" is weak; "Processes 9,000+ req/s on Starlette, comparable to Go and Node.js frameworks [1]" is strong.
- **Key Resources** should include only working, official links. Do not guess at URLs.
- **Cite all factual claims** per the citation rules in SKILL.md — especially performance benchmarks, adoption statistics, release dates, pricing, and competitive comparisons.
- **Images**: When a section describes architecture, data flow, protocol interactions, or performance characteristics, check whether official documentation contains a diagram that meets the image policy criteria. Include it inline using the `<figure class="img-center">` pattern from joplin-formatting Rule 9. Prefer diagrams from the project's own docs over generic search results.
- **Iterative writing**: For documents exceeding 4,000 words, write the file in stages — create it with the first 2–3 sections via `Write`, then append remaining sections with `Edit`. This avoids single-pass length limits. Always write to a file, not an artifact, for long documents. Do NOT truncate or condense content to fit into a single generation pass.

## Self-Check Before Output

- [ ] `>[toc]` present at document start?
- [ ] Overview includes General Information (as prose), Key Resources, and Advantages/Disadvantages?
- [ ] Common Commands section present with 6-12 commands?
- [ ] Additional sections cover the most important aspects of this specific tool?
- [ ] All factual claims have inline citations `<a href="#ref-1">[1]</a>`?
- [ ] `### Index` section at end with anchored numbered bibliography?
- [ ] All joplin-formatting rules applied (spacing, heading hierarchy, `---` only after h3)?
