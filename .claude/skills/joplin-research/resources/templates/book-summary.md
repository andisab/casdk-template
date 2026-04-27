# Book Summary Template

**Trigger**: User requests "Book summary of...", "Summarize [book title]", or "Create chapter summaries for..."
**Use Case**: Summary of a technical or non-fiction book, capturing structure, arguments, and takeaways
**Goal**: Enable the reader to recall key arguments and apply insights without re-reading the full book
**Typical Length**: 2–4 pages (not counting source citations).

## Output Skeleton

Fill in PLACEHOLDERS with content. Preserve all heading levels, spacing, and
separator placement exactly as shown. Apply all joplin-formatting rules.

```markdown
>[toc]

## BOOK_TITLE

### Overview
---
**Author**: AUTHOR_NAME
**Published**: YEAR, PUBLISHER
**Context**: BACKGROUND_ABOUT_THE_AUTHOR — who are they, what is their expertise,
and what motivated this book? 1-2 sentences.
**Main Objectives**: CORE_GOALS_AND_THEMES of the book. What is the central thesis
or argument? What does the author set out to prove or teach? 2-3 sentences.

### Chapter 1: CHAPTER_TITLE
---
CHAPTER_SUMMARY — 2-5 sentences covering the key points, arguments, evidence,
and takeaways from this chapter. Focus on WHAT the author argues and WHY,
not just the topics covered.

### Chapter 2: CHAPTER_TITLE
---
CHAPTER_SUMMARY

### Chapter N: CHAPTER_TITLE
---
CHAPTER_SUMMARY

[Continue for all chapters or major sections of the book]

### Key Takeaways
---
- ACTIONABLE_TAKEAWAY_1
- ACTIONABLE_TAKEAWAY_2
- ACTIONABLE_TAKEAWAY_3
- ACTIONABLE_TAKEAWAY_4
- ACTIONABLE_TAKEAWAY_5

### Index
---
<a id="ref-1"></a>1. AUTHOR. *BOOK_TITLE*. PUBLISHER. YEAR.
<a id="ref-2"></a>2. ANY_SUPPLEMENTARY_SOURCES_CONSULTED
```

## Content Guidelines

### Overview Section
- **Context** should establish the author's credibility and motivation — why should the reader trust this author on this topic?
- **Main Objectives** should capture the book's thesis, not just its subject. "Explores software architecture" is weak; "Argues that most software complexity is accidental, not essential, and proposes concrete patterns for managing it" is strong.

### Chapter Summaries
- **2-5 sentences per chapter**. Target 3 sentences for most chapters.
- Focus on **arguments and evidence**, not just topics. "This chapter covers testing" is weak; "The author argues that test-driven development reduces defect rates by 40-80% based on IBM and Microsoft case studies, and provides a practical framework for adopting TDD incrementally" is strong.
- Include **specific data points or examples** when the chapter provides them.
- Note when a chapter builds on or contradicts earlier chapters.

### Key Takeaways
- **5-8 takeaways** that the reader can act on or remember.
- Frame as actionable insights, not chapter titles: "Prefer composition over inheritance for flexible system design" rather than "Chapter 3 discusses composition."
- These should stand alone — someone reading only the takeaways should get lasting value.

### Chapter Grouping
- For books with many short chapters (20+), consider grouping into **Parts** if the book uses that structure:
  ```markdown
  ### Part I: PART_TITLE (Chapters 1-5)
  ---
  PART_OVERVIEW — 1-2 sentences on the theme of this part.

  #### Chapter 1: CHAPTER_TITLE
  CHAPTER_SUMMARY

  #### Chapter 2: CHAPTER_TITLE
  CHAPTER_SUMMARY
  ```
- For books without explicit Parts, summarize each chapter individually.

### Citation
- Citation [1] is always the book itself.
- Only add additional citations if you consulted external sources (reviews, author interviews, related works) to inform the summary.
- Do NOT cite the book's own internal references unless they're crucial to understanding the summary.

## Self-Check Before Output

- [ ] `>[toc]` present at document start?
- [ ] Overview includes Author, Published, Context, and Main Objectives?
- [ ] Every chapter has a 2-5 sentence summary focused on arguments, not just topics?
- [ ] Key Takeaways are actionable and standalone?
- [ ] `### Index` section at end (at minimum, the book itself as [1])?
- [ ] All joplin-formatting rules applied?
