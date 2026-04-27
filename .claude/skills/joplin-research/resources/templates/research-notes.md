# Research Notes Template

**Trigger**: User requests "What's new with...", general research tasks, or any research request that doesn't match a more specific template
**Use Case**: General research findings, recent updates/changes, exploratory notes
**Goal**: Organized research findings with clear sources for future reference
**Typical Length**: ½ page to 3 pages (varies with scope). Err on the side of thoroughness. Do NOT condense research to fit a page target — include all substantive findings.

This template has TWO output skeletons — choose based on the request type.

---

## Skeleton A: "What's New With..." (Short Format)

Use for recent updates, changelogs, version releases, or "what's changed" requests.
Typically ½–1 page.

```markdown
## TOPIC — What's New (DATE_RANGE, e.g., "Q1 2025" or "Since v3.0")

### Recent Developments
---
SUMMARY_OF_RECENT_CHANGES in flowing prose (1-2 paragraphs). What happened, when,
and why does it matter? Lead with the most significant change.

### Key Changes
---
- **CHANGE_1**: DESCRIPTION_WITH_CONTEXT — what changed and what it means for users [1]
- **CHANGE_2**: DESCRIPTION [2]
- **CHANGE_3**: DESCRIPTION [3]
- **CHANGE_N**: DESCRIPTION

### Implications
---
WHAT_DO_THESE_CHANGES_MEAN for users, developers, or the ecosystem? Are there
migration steps, deprecations, or new opportunities to be aware of?

### Index
---
<a id="ref-1"></a>1. SOURCE_1
<a id="ref-2"></a>2. SOURCE_2
<a id="ref-3"></a>3. SOURCE_3
```

### Short Format Guidelines
- **Recent Developments**: 1-2 paragraphs of prose summarizing the overall picture.
- **Key Changes**: Bulleted list is appropriate here — each item should be 1-2 sentences with bold label and inline citation.
- **Implications**: 1 paragraph on practical impact.
- `>[toc]` may be omitted for short notes (under 1 page).
- Always include References even for short notes.

---

## Skeleton B: General Research Notes (Long Format)

Use for exploratory research, topic deep-dives, or any research that doesn't fit
another template. Scales from 1 to 3+ pages depending on scope.

```markdown
>[toc]
## RESEARCH_TOPIC

### Context & Background
---
OVERVIEW of the topic: why it matters, current state of the field, and what prompted
this research. 1-3 paragraphs of flowing prose.

### Key Findings
---
MAIN_DISCOVERIES_OR_INSIGHTS organized logically. Lead with the most important finding.

#### FINDING_CATEGORY_1
DETAILED_FINDINGS with specific data points and citations.

#### FINDING_CATEGORY_2
ADDITIONAL_FINDINGS.

#### FINDING_CATEGORY_N
MORE_FINDINGS as needed.

### OPTIONAL_SECTION (e.g., "Methodology", "Current Tools", "Comparison", "Best Practices")
---
ADDITIONAL_CONTENT organized into whatever sections best serve the topic.
Use judgment — not every research note needs the same sections.

### Implications
---
WHAT_THIS_MEANS and how it can be applied. Practical takeaways for the reader.

### Open Questions
---
- QUESTION_1 — what remains unclear or needs further investigation?
- QUESTION_2
- QUESTION_N

### Index
---
<a id="ref-1"></a>1. SOURCE_1
<a id="ref-2"></a>2. SOURCE_2
<a id="ref-3"></a>3. SOURCE_3
```

### Long Format Guidelines
- **Context & Background**: Set the stage. Why is this topic being researched? What does the reader need to know to understand the findings?
- **Key Findings**: The core of the document. Use `####` subsections to organize findings by category. Include specific data, numbers, and citations.
- **Optional sections**: Add sections as the topic demands. Common additions:
  - "Methodology" — if you used a specific research approach worth documenting
  - "Current Tools / Solutions" — if the research surveyed available options
  - "Comparison" — if findings involve comparing approaches
  - "Best Practices" — if the research yields actionable recommendations
  - "Timeline / History" — if chronological context matters
- **Implications**: The "so what?" section — translate findings into practical action.
- **Open Questions**: Honest about what you don't know. This section is valuable for future research sessions — it tells future-you where to pick up.
- Include `>[toc]` for notes exceeding ~1 page.

## Content Guidelines (Both Formats)

- **Cite all factual claims** — even in short "What's New" notes. Every data point, release date, feature claim, and statistic needs a citation.
- **Write for future reference** — these notes will be read weeks or months later. Include enough context that the note is self-contained and comprehensible without remembering the original research session.
- **Date your notes** — include the date range or "as of YYYY-MM-DD" in the title or overview so future readers know the currency of the information.
- **Be honest about uncertainty** — if sources conflict or information is unconfirmed, say so.

## Self-Check Before Output

- [ ] Correct skeleton used (Short for "What's New", Long for general research)?
- [ ] `>[toc]` present for long-format notes (1+ page)?
- [ ] All factual claims cited inline `<a href="#ref-1">[1]</a>`?
- [ ] Date range or currency indicated in title or overview?
- [ ] `### Index` section at end with anchored numbered bibliography?
- [ ] All joplin-formatting rules applied?
