# Technical Survey Template

**Trigger**: User requests "Give me a technical survey of..." or asks to compare multiple tools in a category
**Use Case**: Compare 4–12 similar tools, frameworks, or services in a specific technology space
**Goal**: Structured comparison overview enabling informed tool selection
**Typical Length**: 4–12 pages (not counting citations section). Err on the side of thoroughness. Do NOT
condense research to fit a page target — include all substantive findings.

## Output Skeleton

Fill in PLACEHOLDERS with researched content. Preserve all heading levels, spacing, and
separator placement exactly as shown. Apply all joplin-formatting rules.

```markdown
>[toc]
## TECHNOLOGY_CATEGORY Survey

### Overview
---
BRIEF_INTRODUCTION to the technology category: what problem do these tools solve,
why are they being compared, and what are the key differentiating factors to consider
when choosing between them?

**Comparison Table**:
| Tool | Key Differentiator | Pricing | Best For |
|------|--------------------|---------|----------|
| TOOL_1 | DIFFERENTIATOR | PRICE_TIER | PRIMARY_USE_CASE |
| TOOL_2 | DIFFERENTIATOR | PRICE_TIER | PRIMARY_USE_CASE |
| TOOL_3 | DIFFERENTIATOR | PRICE_TIER | PRIMARY_USE_CASE |
| TOOL_N | DIFFERENTIATOR | PRICE_TIER | PRIMARY_USE_CASE |

### TOOL_NAME_1
---
**Background**: WHEN_WAS_IT_CREATED? WHO_MAINTAINS_IT? HOW_HAVE_ADOPTION_RATES_CHANGED?
WHAT_IS_ITS_BASIC_FUNCTION? HOW_DOES_IT_WORK_AT_A_HIGH_LEVEL (1 paragraph)?
WHAT_ARE_ITS_KEY_FEATURES?

**Key Resources**:
- [Official Site](URL)
- [Documentation](URL)
- [GitHub Repository](URL)

**Advantages & Disadvantages**:
\+ KEY_ADVANTAGE
\+ ANOTHER_STRENGTH
\- NOTABLE_LIMITATION
\- AREA_WHERE_COMPETITORS_EXCEL

### TOOL_NAME_2
---
**Background**: SAME_STRUCTURE_AS_TOOL_1.

**Key Resources**:
- [Official Site](URL)
- [Documentation](URL)
- [GitHub Repository](URL)

**Advantages & Disadvantages**:
\+ KEY_ADVANTAGE
\+ ANOTHER_STRENGTH
\- NOTABLE_LIMITATION
\- AREA_WHERE_COMPETITORS_EXCEL

### TOOL_NAME_N
---
[Repeat same structure for each tool]

### Index
---
<a id="ref-1"></a>1. FIRST_SOURCE
<a id="ref-2"></a>2. SECOND_SOURCE
<a id="ref-3"></a>3. THIRD_SOURCE
```

## Structural Guidelines

### Overview Section
- Open with 1-2 paragraphs explaining the technology category and why the comparison matters.
- The **Comparison Table** is mandatory — it gives the reader an at-a-glance summary before the detailed sections.
- Table columns should be adapted to the category. Common column sets:
  - General: Tool | Key Differentiator | Pricing | Best For
  - Databases: Tool | Type | Scaling Model | Query Language | Best For
  - Frameworks: Tool | Language | Performance | Learning Curve | Best For
  - Cloud Services: Tool | Provider | Free Tier | Key Feature | Best For

### Per-Tool Sections
- Each tool gets its own `### Tool Name` section with `---` separator.
- **Background** should be flowing prose (1-2 paragraphs), not a bulleted checklist. Cover: creation date, maintainer, adoption trends, core function, high-level architecture, key features.
- **Key Resources** — official links only. Omit if you cannot confirm the URL.
- **Advantages & Disadvantages** — at least 2 of each per tool. Make them specific and comparative: "Faster cold starts than Lambda [3]" rather than "Fast."
- Maintain **consistent structure** across all tool sections so the reader can compare easily.

### Tool Count and Depth
- For 4–6 tools: Full background + advantages/disadvantages for each.
- For 7–12 tools: Slightly condensed backgrounds (1 paragraph each), but still include advantages/disadvantages and key resources for every tool.
- If the user requests more than 12 tools, suggest splitting into sub-categories or focusing on the top candidates.

### Ordering
- Order tools by relevance or market position — lead with the most widely adopted or most relevant to the user's context, not alphabetically.
- If the user has specified a preference or use case, lead with the best-fit tools.

## Content Guidelines

- **Every tool must have the same sections** — consistency enables comparison. If one tool has Key Resources, they all must.
- **Comparison Table data must match the detailed sections** — don't put pricing in the table that isn't discussed in the tool's section.
- **Cite all factual claims** — adoption stats, GitHub stars, performance benchmarks, pricing, release dates. Each tool section will typically need 2-5 citations.
- **Be fair** — present genuine strengths and weaknesses for each tool, including popular/dominant tools. Avoid cheerleading or dismissiveness.

## Self-Check Before Output

- [ ] `>[toc]` present at document start?
- [ ] Overview section with comparison table?
- [ ] Every tool has Background, Key Resources, Advantages/Disadvantages?
- [ ] All tool sections follow the same structure (consistent for comparison)?
- [ ] Comparison table data matches detailed section content?
- [ ] All factual claims cited inline `<a href="#ref-1">[1]</a>`?
- [ ] `### Index` section at end with anchored numbered bibliography?
- [ ] If source material contains high-value diagrams (architecture, flowcharts, data visualizations), considered including 1-2 per the image policy?
- [ ] All joplin-formatting rules applied?
