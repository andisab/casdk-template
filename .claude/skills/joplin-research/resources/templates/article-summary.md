# Article Summary Template

**Trigger**: User requests "Article summary of...", "Summarize this article...", or provides a URL/article to summarize
**Use Case**: Summary of a web article, blog post, news piece, or long-form online content
**Goal**: Capture the article's argument, evidence, and implications in a format useful for future reference
**Typical Length**: 1–2 pages

## Output Skeleton

Fill in PLACEHOLDERS with content. Preserve all heading levels, spacing, and
separator placement exactly as shown. Apply all joplin-formatting rules.

```markdown
## ARTICLE_TITLE

### Overview
---
**Author**: AUTHOR_NAME
**Source**: PUBLICATION_OR_WEBSITE
**Date**: PUBLICATION_DATE
**URL**: [ARTICLE_TITLE](URL)

### Summary
---
COMPREHENSIVE_SUMMARY providing a balanced mix of:
- The article's main argument or thesis
- Key evidence, data points, or examples the author uses
- Counterarguments or alternative perspectives presented (if any)
- Important conclusions or implications

Write as flowing prose (2-4 paragraphs), not a bulleted list. The summary should
capture the article's ARGUMENT, not just its topics.

### Key Takeaways
---
- TAKEAWAY_1 — the most important insight or finding
- TAKEAWAY_2 — a secondary insight or practical implication
- TAKEAWAY_3 — additional notable point
- TAKEAWAY_N (3-6 takeaways total)

### Index
---
<a id="ref-1"></a>1. AUTHOR. "[ARTICLE_TITLE](URL)." *PUBLICATION*. DATE.
<a id="ref-2"></a>2. ANY_SOURCES_REFERENCED_IN_THE_ARTICLE (if relevant)
```

## Content Guidelines

### Overview Section
- **All metadata fields are required**. If a field is unknown, use:
  - Author unknown: "Unknown" or the publication name
  - Date unknown: "n.d."
- The URL should be a clickable markdown link using the article title as link text.

### Summary Section
- **Write as prose**, not bullet points. Aim for 2-4 paragraphs.
- **First paragraph**: State the article's main argument or thesis and why it matters.
- **Middle paragraphs**: Key evidence, examples, or data the author presents. Include specific numbers when available.
- **Final paragraph**: Conclusions, implications, or the author's recommendations.
- If the article is **opinion/analysis**: include the counterarguments or limitations the author acknowledges (or should have acknowledged).
- If the article is **news/factual**: focus on the facts reported and their significance.

### Key Takeaways
- **3-6 takeaways** that stand alone as useful reference points.
- Frame as insights, not section titles: "LLM inference costs dropped 90% in 2024, making real-time applications economically viable" rather than "The article discusses cost trends."
- Include specific data points when the article provides them.

### Citation
- Citation [1] is always the article itself.
- If the article references or links to other notable sources that inform your summary, include them as additional citations.
- If the user provided the article content directly (paste or upload), still cite it as [1] with whatever metadata is available.

### Short Articles
- For articles under ~500 words (brief announcements, changelogs, short posts):
  - Summary can be a single paragraph.
  - Key Takeaways can be 2-3 items.
  - The `>[toc]` tag may be omitted since the document will be short.

## Self-Check Before Output

- [ ] Overview includes Author, Source, Date, and URL?
- [ ] Summary is written as flowing prose (not bullet points)?
- [ ] Summary captures the argument/thesis, not just topics?
- [ ] Key Takeaways are specific and standalone?
- [ ] `### Index` section at end (at minimum, the article itself as [1])?
- [ ] If the article contains high-value diagrams (architecture, flowcharts, data visualizations), considered including per the image policy?
- [ ] All joplin-formatting rules applied?
