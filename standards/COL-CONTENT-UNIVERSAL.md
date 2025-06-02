---
title: 'Collection: Universal Content and Schemas Standards'
aliases:
- Universal Content Standards
- COL-CONTENT-UNIVERSAL
tags:
- content-type/standards-collection
- kb-id/standards
- status/deprecated
- topic/content-guidelines
- topic/schemas
kb-id: standards
info-type: standards-collection
primary-topic: 'DEPRECATED: Collection of universal standards for content creation, schemas, tone, scope, and digital abstraction.'
related-standards:
- AS-SCHEMA-METHODOLOGY-DESCRIPTION
- AS-SCHEMA-CONCEPT-DEFINITION
- CS-POLICY-TONE-LANGUAGE
- CS-POLICY-SCOPE-INCLUSION
- CS-POLICY-SCOPE-EXCLUSION
- CS-POLICY-DIGITAL-ABSTRACTION
version: 0.4.0
date-created: '2025-05-15'
date-modified: '2025-06-01T23:50:44Z'
---
**DEPRECATED:** This collection document is superseded by the new atomic standards architecture. Relevant content has been refactored into individual standard, policy, and guide documents located in `/master-knowledge-base/standards/src/`. Please refer to `[[AS-ROOT-STANDARDS-KB]]` for an overview of the new standards or consult `[[GM-GUIDE-KB-USAGE]]`.

# Universal Content and Schemas Standards

This document details universal standards for content creation, including specific schemas for common content types, general tone and language, scope inclusion/exclusion principles, and digital abstraction guidelines.

## Table of Contents

- [[#Standard: Content Schema for "Methodology/Technique Descriptions" (U-SCHEMA-METHOD-001)]]
- [[#Standard: Content Schema for "Concept Definitions" (U-SCHEMA-CONCEPT-001)]]
- [[#Standard: Clarity, Objectivity, and Consistency in Language (U-TONE-LANG-001)]]
- [[#Standard: Universal Principles for Content Inclusion (U-SCOPE-INCLUDE-001)]]
- [[#Standard: Universal Principles for Content Exclusion (U-SCOPE-EXCLUDE-001)]]
- [[#Standard: Translating Non-Digital Concepts for Digital Workflows (U-ABSTR-DIGITAL-001)]]

## Standard: Content Schema for "Methodology/Technique Descriptions" (U-SCHEMA-METHOD-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-SCHEMA-METHOD-001`                 |
| Standard Name   | Content Schema for "Methodology/Technique Descriptions" |
| Standard Category | Content Templates & Schemas           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                    | Example (if illustrative)                   | Notes / Further Specification (if any)            |
| :----- | :------------------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :---------------------------------------------- |
| 1.1    | Documents describing a specific methodology, technique, or detailed process MUST follow this schema.                 | A file `systematic-literature-review.md`    | Applies to "how-to" type content.                 |
| 1.2    | The H1 title MUST be the name of the methodology/technique.                                                           | `# Systematic Literature Review`             |                                                   |
| 1.3    | An introductory abstract (per [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]]) MUST summarize the method.                                              | "This document outlines how to conduct a systematic..." |                                                   |
| 1.4    | A ToC (per [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]]) MUST be included.                                                                          |                                             |                                                   |
| 1.5    | The document MUST include dedicated H2 sections (at minimum) for: "Purpose," "Core Principles," "When to Use / Not Use," "Key Steps" (or "Process"), "Advantages," "Limitations," and "Variations/Alternatives." | Heading: `## Purpose`                       | "Key Steps" can be further broken down with H3s.  |
| 1.6    | The "Key Steps" / "Process" section MUST detail actionable steps, numbered or clearly sequenced.                    | `### Step 1: Define Research Question`      |                                                   |
| 1.7    | Each "Key Step" MUST (if applicable) specify inputs required for the step and outputs/deliverables produced by the step. | "Input: Defined scope; Output: Search strategy" | This aids decomposability for workflows.          |

**Illustrative Examples (Overall):**

Partial H2 Outline for `systematic-literature-review.md`:

```markdown
# Systematic Literature Review
(Abstract & ToC)

## Purpose
To synthesize existing evidence rigorously...

## Core Principles
Transparency, reproducibility...

## When to Use / Not Use
Use when: Answering focused questions...
Not Use when: Broad exploratory research needed...

## Key Steps
### Step 1: Formulate the Question (PICO)
Inputs: Initial research problem.
Outputs: Focused, answerable question.
(Detailed actions)
### Step 2: Develop Protocol
...

## Advantages
Reduces bias, highly credible...

## Limitations
Time-consuming, requires expertise...

## Variations/Alternatives
Scoping reviews, rapid reviews...

## Summary
## See Also
```

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]], [[COL-ARCH-UNIVERSAL#Standard: Layered Information Presentation (U-DETAIL-LEVEL-001)|U-DETAIL-LEVEL-001]].

## Standard: Content Schema for "Concept Definitions" (U-SCHEMA-CONCEPT-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-SCHEMA-CONCEPT-001`                |
| Standard Name   | Content Schema for "Concept Definitions" |
| Standard Category | Content Templates & Schemas           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                  | Example (if illustrative)                            | Notes / Further Specification (if any)       |
| :----- | :----------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :------------------------------------------- |
| 1.1    | Documents primarily defining a core concept or term MUST follow this schema.                                        | `statistical-significance.md`                          |                                              |
| 1.2    | The H1 title MUST be the name of the concept.                                                                         | `# Statistical Significance`                            |                                              |
| 1.3    | An introductory abstract (per [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]]) MUST summarize the concept's meaning.                                 | "Statistical significance refers to the likelihood..." |                                              |
| 1.4    | A ToC (per [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]]) MUST be included.                                                                        |                                                      |                                              |
| 1.5    | The document MUST include dedicated H2 sections (at minimum) for: "Definition," "Key Characteristics / Principles," "Importance / Relevance," "Common Misconceptions" (if any), and "Practical Examples" or "Applications." | `## Definition`                                      | Other H2s can be added as needed.             |
| 1.6    | The "Definition" section MUST provide a clear, concise, and unambiguous definition.                               |                                                      |                                              |
| 1.7    | "Practical Examples" or "Applications" MUST illustrate the concept in use.                                          |                                                      |                                              |

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]].

## Standard: Clarity, Objectivity, and Consistency in Language (U-TONE-LANG-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-TONE-LANG-001`                     |
| Standard Name   | Clarity, Objectivity, and Consistency in Language |
| Standard Category | Tone & Language                       |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                              | Example (if illustrative)                                    | Notes / Further Specification (if any)                           |
| :----- | :------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------- | :------------------------------------------------------------- |
| 1.1    | Language MUST be clear, concise, precise, and unambiguous. Overly complex sentence structures MUST be avoided.              | "The method involves..." not "It is the case that the method necessitates..." | Prioritize directness.                                       |
| 1.2    | The tone MUST be objective, academic, and informative. Overly informal, opinionated, or persuasive language MUST NOT be used (unless the KB specifically calls for persuasive argumentation). |                                                            | Default is informative/expository.                               |
| 1.3    | Terminology specific to a domain MUST be used consistently. If a term has multiple meanings, the intended one MUST be clarified on first use or linked to a definition. |  Use "Systematic Review" consistently if that's the chosen term. | May reference a KB-specific glossary if one exists.         |
| 1.4    | Acronyms and abbreviations MUST be defined upon first use in any given document, followed by the acronym in parentheses. | "Large Language Model (LLM)..." then use "LLM" thereafter. | Exception: Widely understood universal acronyms may not require definition in every document. |
| 1.5    | Active voice MUST be used more frequently than passive voice for clarity and directness where appropriate.                   | "The researcher analyzes data." vs "Data is analyzed by the researcher." |                                                                  |

**Cross-References to Other Standard IDs:** None.

## Standard: Universal Principles for Content Inclusion (U-SCOPE-INCLUDE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-SCOPE-INCLUDE-001`                 |
| Standard Name   | Universal Principles for Content Inclusion |
| Standard Category | Content Inclusion/Exclusion Principles |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                   | Example (if illustrative)                      | Notes / Further Specification (if any)                 |
| :----- | :------------------------------------------------------------------------------------------------------------------ | :------------------------------------------- | :----------------------------------------------------- |
| 1.1    | Content included in any KB MUST be directly relevant to the stated scope and purpose of that specific KB.         |  KB "X" only includes "X"-related information. | Defined by each KB's `root.md` & `kb-directory.md`.   |
| 1.2    | Content MUST be verifiable or derived from citable sources (for factual KBs) or based on logical reasoning (for conceptual/philosophical KBs). | Link to or cite external sources.            | Per [[03-Universal-Linking-Metadata-And-Utility#Standard: Citing External Sources (U-CITE-001)|U-CITE-001]].                        |
| 1.3    | Content MUST focus on information and actionable knowledge (how-to, why, what) rather than ephemeral news, personal unprotected opinions (unless a specific template like "Expert Opinion Snippet" is defined and used), or transient discussions. | Focus on evergreen principles, methods.      | This promotes longevity.                                |

**Cross-References to Other Standard IDs:** [[COL-LINKING-UNIVERSAL#Standard: Citing External Sources (U-CITE-001)|U-CITE-001]].

## Standard: Universal Principles for Content Exclusion (U-SCOPE-EXCLUDE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-SCOPE-EXCLUDE-001`                 |
| Standard Name   | Universal Principles for Content Exclusion |
| Standard Category | Content Inclusion/Exclusion Principles |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                    | Example (if illustrative)                  | Notes / Further Specification (if any)                  |
| :----- | :--------------------------------------------------------------------------------------------------- | :--------------------------------------- | :---------------------------------------------------- |
| 1.1    | Content that is illegal, unethical (by broad consensus), or promotes harm MUST NOT be included.        | N/A (Obvious exclusion)                  |                                                         |
| 1.2    | Sensitive Personally Identifiable Information (PII) MUST NOT be included, unless explicitly mandated by the KB's secure design and for specific, legitimate internal operational use only, and under strict access controls. | Do not embed lists of users' emails publicly. | Err on the side of caution.                          |
| 1.3    | Proprietary information from third parties to which rights are not held MUST NOT be included.         | Avoid pasting copyrighted book chapters.   |                                                         |
| 1.4    | Redundant information that is already well-covered elsewhere within the *same KB section or direct hierarchy* without adding new value or perspective MUST NOT be included (linking is preferred). | Link to original definition, don't repeat. | Aids maintainability. Differs from summarization/synthesis. |

**Cross-References to Other Standard IDs:** None.

## Standard: Translating Non-Digital Concepts for Digital Workflows (U-ABSTR-DIGITAL-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-ABSTR-DIGITAL-001`                 |
| Standard Name   | Translating Non-Digital Concepts for Digital Workflows |
| Standard Category | Digital Abstraction Principles        |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                      | Example (if illustrative)                                         | Notes / Further Specification (if any)                             |
| :----- | :------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- | :--------------------------------------------------------------- |
| 1.1    | When a methodology traditionally involves physical real-world actions, interpersonal interactions, or ethically sensitive areas that are OUT OF SCOPE for the KB's digital/informational focus, those aspects MUST be explicitly excluded or abstracted. | Physical lab work: focus on design, data interpretation steps. | Guided by KB-specific exclusion rules.                          |
| 1.2    | Abstracted methodologies MUST focus on the information-based processes, decision points, inputs, and outputs that *can* be executed or managed digitally. | Instead of "conduct interview," rule describes "design interview questions," "structure interview protocol (digital document)," "analyze transcript data." | Emphasize the data/document artifacts.                             |
| 1.3    | If a traditional step is entirely out of scope, its absence in the digital abstraction and the rationale for exclusion MUST be noted if critical to understanding the context of the abstracted version. | Note: "Physical sample collection is excluded; data assumed available." | Helps maintain clarity.                                         |

**Cross-References to Other Standard IDs:** None.