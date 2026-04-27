# Whitepaper Summary Template

**Trigger**: User requests "Whitepaper summary of...", "Summarize this paper...", or provides a research paper to summarize
**Use Case**: Summary of a technical whitepaper, research paper, or academic publication
**Goal**: Distill the paper's methodology, findings, and implications for a practitioner audience
**Typical Length**: 2–4 pages

## Output Skeleton

Fill in PLACEHOLDERS with content. Preserve all heading levels, spacing, and
separator placement exactly as shown. Apply all joplin-formatting rules.

```markdown
>[toc]

## PAPER_TITLE

### Overview
---
**Authors**: AUTHOR_LIST (e.g., "Vaswani, A.; Shazeer, N.; Parmar, N. et al.")
**Published**: YEAR, VENUE_OR_PUBLISHER (e.g., "2017, NeurIPS" or "2024, Anthropic Technical Report")
**URL**: [PAPER_TITLE](URL)
**TL;DR**: ONE_SENTENCE_SUMMARY of the paper's key contribution.

### Abstract & Motivation
---
WHY does this paper exist? What problem does it address? What gap in existing work does
it fill? Restate the paper's abstract in plain language (1-2 paragraphs), focusing on
the motivation and the claimed contribution. Avoid jargon where possible — translate
academic language into practitioner-accessible terms.

### Methodology
---
HOW was the research conducted? Describe the key approaches, experimental setup, datasets
used, models compared, and evaluation metrics. This section should give the reader enough
understanding to evaluate the validity of the results.

#### METHODOLOGY_SUBSECTION_IF_NEEDED (e.g., "Dataset", "Model Architecture", "Training Setup")
DETAILS about a specific aspect of the methodology.

### Key Findings
---
MAIN_RESULTS and discoveries. Lead with the most important finding. Include specific
numbers, metrics, and data points where the paper provides them.

#### FINDING_CATEGORY_1 (e.g., "Performance Results", "Scaling Behavior")
SPECIFIC_FINDINGS with data points. "The model achieved X on benchmark Y, a Z% improvement
over the previous state of the art [1]."

#### FINDING_CATEGORY_2 (e.g., "Ablation Studies", "Comparison with Baselines")
ADDITIONAL_FINDINGS.

### Implications
---
WHAT_DOES_THIS_MEAN for practitioners, the field, or future research? Connect the findings
to real-world applications. What should engineers, researchers, or decision-makers do
differently based on this work?

### Limitations
---
ACKNOWLEDGED_LIMITATIONS noted by the authors themselves, plus any apparent gaps or
concerns not addressed in the paper. Be specific: "The evaluation was limited to English-language
tasks" rather than "The paper has some limitations."

### Index
---
<a id="ref-1"></a>1. AUTHORS. "[PAPER_TITLE](URL)." *VENUE*. YEAR.
<a id="ref-2"></a>2. KEY_REFERENCE_CITED_IN_THE_PAPER
<a id="ref-3"></a>3. ANOTHER_KEY_REFERENCE
```

## Content Guidelines

### Overview Section
- **All metadata fields are required**. Author list can be abbreviated with "et al." for 4+ authors.
- **TL;DR** should be a single sentence that a busy practitioner could read and understand the paper's contribution. "This paper introduces the Transformer architecture, replacing recurrence with self-attention to achieve better parallelization and faster training for sequence-to-sequence tasks."
- If the paper has a commonly known short name (e.g., "the Attention paper", "GPT-4 technical report"), mention it.

### Abstract & Motivation
- Rewrite the abstract in accessible language — assume the reader is a senior engineer, not necessarily a researcher.
- Clearly state the **gap** the paper addresses: what couldn't be done before, or what was the paper trying to improve?
- If the paper builds on prior work, briefly note what came before.

### Methodology
- Describe enough that the reader can evaluate whether the results are credible.
- For ML papers: model architecture, training data, hyperparameters, evaluation benchmarks.
- For systems papers: implementation details, hardware, workload characteristics, baselines compared.
- For empirical studies: sample size, methodology, statistical approach, controls.
- Use subsections (`####`) to break up complex methodologies.

### Key Findings
- **Lead with the most impactful finding**.
- Include **specific numbers**: accuracy, speedup, cost reduction, etc. "Faster than previous methods" is weak; "3.2x faster training with comparable BLEU scores [1]" is strong.
- Use subsections (`####`) to organize findings by category.
- Note if findings were surprising or contradicted conventional wisdom.

### Implications
- This is the "so what?" section — translate academic results into practitioner impact.
- What should someone **do differently** based on this paper?
- What follow-up research does this enable?

### Limitations
- Include limitations the authors acknowledge AND any apparent gaps you notice.
- Be specific and constructive, not dismissive.
- Common limitation categories: dataset/scope limitations, evaluation gaps, scalability questions, reproducibility concerns, missing comparisons.

### Citation
- Citation [1] is always the paper itself.
- Include **key references the paper cites** that are important to understanding its contribution — typically the most important prior work it builds on or compares against.
- Do not exhaustively cite the paper's entire bibliography — select the 3-8 most important references.

## Self-Check Before Output

- [ ] `>[toc]` present at document start?
- [ ] Overview includes Authors, Published, URL, and TL;DR?
- [ ] Abstract & Motivation explains the gap and contribution in accessible language?
- [ ] Methodology provides enough detail to evaluate credibility?
- [ ] Key Findings include specific numbers and data points?
- [ ] Implications connect findings to real-world practitioner impact?
- [ ] Limitations are specific and constructive?
- [ ] `### Index` section at end with the paper itself as [1]?
- [ ] If the paper contains high-value diagrams (architecture, flowcharts, data visualizations), considered including 1-2 per the image policy?
- [ ] All joplin-formatting rules applied?
