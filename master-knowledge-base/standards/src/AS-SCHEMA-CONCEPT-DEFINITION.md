---
title: "Standard: Content Schema for Concept Definitions"
standard_id: "AS-SCHEMA-CONCEPT-DEFINITION"
aliases: ["Concept Definition Schema", "Terminology Schema"]
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "Schema for Concept Definitions"
related-standards: ["AS-STRUCTURE-DOC-CHAPTER"]
version: '1.0.0'
date-created: "2024-07-15T12:00:00Z"
date-modified: "2025-05-30T12:00:00Z"
primary_domain: "AS"
sub_domain: "STRUCTURE"
scope_application: "Defines the mandatory content structure (schema) for documents that primarily define a core concept or term."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Content consistency", "Clarity of definitions", "User understanding of terminology", "Knowledge base coherence"]
change_log_url: "./AS-SCHEMA-CONCEPT-DEFINITION-changelog.md"
---
# Standard: Content Schema for Concept Definitions (AS-SCHEMA-CONCEPT-DEFINITION)

This standard defines the mandatory content structure (schema) for documents whose primary purpose is to define a core concept or term. Adherence to this schema ensures that concepts are explained clearly, consistently, and comprehensively.

## 1. Scope and Applicability (Derived from U-SCHEMA-CONCEPT-001, Rule 1.1)

This schema MUST be applied to all documents that primarily define a core concept or term.
*   **Example Application:** A document defining `statistical-significance.md` or `machine-learning-bias.md`.

## 2. Mandatory Document Structure

Documents following this schema MUST adhere to the general internal structure for "Chapters" as defined in [[AS-STRUCTURE-DOC-CHAPTER]]. This includes:

### Rule 2.1: H1 Title (Derived from U-SCHEMA-CONCEPT-001, Rule 1.2)
The H1 title of the document MUST be the specific name of the concept or term being defined.
*   **Example:** `# Statistical Significance`

### Rule 2.2: Introductory Abstract (Derived from U-SCHEMA-CONCEPT-001, Rule 1.3)
An introductory abstract that summarizes the concept's meaning and significance MUST be included immediately after the H1 title.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for details on abstract content.

### Rule 2.3: Table of Contents (ToC) (Derived from U-SCHEMA-CONCEPT-001, Rule 1.4)
A Table of Contents (ToC) MUST follow the abstract, linking to all H2 sections and significant H3 sections.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for ToC requirements.

## 3. Required Sections (H2 Level) (Derived from U-SCHEMA-CONCEPT-001, Rule 1.5)

The following H2 sections MUST be included in the document, at a minimum, and should appear in a logical order similar to that presented below:

1.  **`## Definition`** (Derived from U-SCHEMA-CONCEPT-001, Rule 1.6)
    *   This section MUST provide a clear, concise, and unambiguous definition of the concept or term.
    *   It should be easily understandable and serve as the primary explanation.
2.  **`## Key Characteristics / Principles`**
    *   Describe the essential features, attributes, properties, or underlying principles that define or govern the concept.
3.  **`## Importance / Relevance`**
    *   Explain why the concept is important, its significance in relevant domains, or its practical relevance.
4.  **`## Common Misconceptions`** (If Applicable)
    *   Address any common misunderstandings, myths, or incorrect interpretations related to the concept. This section is optional if no common misconceptions are known.
5.  **`## Practical Examples / Applications`** (Derived from U-SCHEMA-CONCEPT-001, Rule 1.7)
    *   This section MUST illustrate the concept in use through practical examples, applications, or case studies.
    *   Examples should be clear and help solidify understanding.

*   **Note:** Other H2 sections can be added as needed to fully explain the concept.

## 4. Illustrative Example (Partial H2 Outline)

For a document named `statistical-significance.md`:
```markdown
# Statistical Significance
(Abstract: This document defines statistical significance, explaining its role in hypothesis testing...)
(Table of Contents: ...)

## Definition
Statistical significance refers to the likelihood that an observed result or relationship in a dataset is not due to random chance...

## Key Characteristics / Principles
- Based on hypothesis testing (null and alternative hypotheses).
- Involves calculating a p-value.
- Threshold for significance (alpha level, e.g., 0.05).
- Does not imply practical significance or importance of the effect.

## Importance / Relevance
- Crucial for drawing valid conclusions from research data.
- Widely used in scientific research, A/B testing, quality control, etc.
- Helps in making data-driven decisions.

## Common Misconceptions
- That statistical significance implies a large or important effect.
- That a non-significant result proves the null hypothesis is true.

## Practical Examples / Applications
### Example 1: A/B Testing
A website tests two versions of a button (A and B). Version B gets a 5% higher click-through rate. Statistical significance testing determines if this 5% difference is likely real or due to chance...

### Example 2: Medical Trials
A new drug is tested against a placebo. Statistical significance helps determine if the observed improvement in patients taking the drug is a real effect of the drug...

## Summary
(Summary of statistical significance...)

## See Also
- [[CONCEPT-HYPOTHESIS-TESTING]]
- [[CONCEPT-P-VALUE]]
```

## 5. Cross-References
- [[AS-STRUCTURE-DOC-CHAPTER]] - For general chapter structure requirements (H1, abstract, ToC, summary, see also).

---
*This standard (AS-SCHEMA-CONCEPT-DEFINITION) is based on rules 1.1 through 1.7 previously defined in U-SCHEMA-CONCEPT-001 from COL-CONTENT-UNIVERSAL.md.*
