---
title: 'Collection: Universal Architecture and Structure Standards'
aliases: ['Universal Architecture Standards', 'COL-ARCH-UNIVERSAL']
tags:
  - kb-id/standards
  - content-type/standards-collection
  - status/deprecated # Updated status
  - topic/architecture
  - topic/structure
kb-id: standards
info-type: standards-collection # This info-type is still valid for a collection, even if deprecated
primary-topic: 'DEPRECATED Collection of universal standards governing overall KB architecture and fundamental document/section structure. Superseded by atomic standards.'
related-standards: ["AS-STRUCTURE-KB-ROOT", "AS-STRUCTURE-MASTER-KB-INDEX", "AS-STRUCTURE-KB-PART", "AS-STRUCTURE-DOC-CHAPTER", "CS-POLICY-LAYERED-INFORMATION", "SF-CONVENTIONS-NAMING"] # Listing some of the new standards
version: '0.4.0' # Increment version due to significant change (deprecation)
date-created: '2025-05-15'
date-modified: '2024-07-15T12:00:00Z' # Placeholder for current date
---

**<font color="red">IMPORTANT: This document is deprecated.</font>**

The standards and guidelines previously contained in this collection have been refactored into individual, atomic standard documents. Please refer to the new standards located in the `/master-knowledge-base/standards/src/` directory, particularly those with `AS-` (Architectural Standards) and related `CS-` (Content Standards/Policies) prefixes.

Key new standards that supersede content from this collection include:
- [[AS-STRUCTURE-KB-ROOT]]
- [[CS-POLICY-KB-ROOT]]
- [[AS-STRUCTURE-MASTER-KB-INDEX]]
- [[CS-POLICY-KB-IDENTIFICATION]]
- [[AS-STRUCTURE-KB-PART]]
- [[CS-POLICY-KB-PART-CONTENT]]
- [[AS-STRUCTURE-DOC-CHAPTER]]
- [[CS-POLICY-DOC-CHAPTER-CONTENT]]
- [[CS-POLICY-LAYERED-INFORMATION]]
- [[SF-CONVENTIONS-NAMING]]

For guidance on the new standards structure, please consult [[GM-GUIDE-KB-USAGE_ID_PLACEHOLDER]] (once available).

---

# Universal Architecture and Structure Standards

This document details the universal standards governing the overall architecture of knowledge bases and the fundamental structure of documents and their primary sections.

## Table of Contents

- [[#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)]]
- [[#Standard: Master KB Directory and Unique KB Identification (U-ARCH-002)]]
- [[#Standard: Primary KB Section ("Part") Structure (U-STRUC-001)]]
- [[#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)]]
- [[#Standard: Layered Information Presentation (U-DETAIL-LEVEL-001)]]
- [[#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)]]

## Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-ARCH-001`                          |
| Standard Name   | KB Root Structure and Top-Level Part Organization |
| Standard Category | Overall Knowledge Base Architecture |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                                                                                                    | Example (if illustrative)                                                                                                             | Notes / Further Specification (if any)                                                                                               |                                                                                                           |
| :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| 1.1    | Each KB MUST have a designated primary folder.                                                                                                                                                                       | Folder name: `prompt-engineering-kb`                                                                                                  | Per [[01-Universal-Architecture-And-Structure#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)                     | U-FORMAT-NAMING-001]].                                                                                    |
| 1.2    | Within this primary folder, a root document named `root.md` MUST exist.                                                                                                                                              | `prompt-engineering-kb/root.md`                                                                                                       | This is the KB's main entry point.                                                                                                   |                                                                                                           |
| 1.3    | The `root.md` MUST contain a master Table of Contents (ToC) linking to all top-level primary sections ("Parts") of that KB.                                                                                          | See Illustrative Example below.                                                                                                       | Links MUST use syntax per [[05-Markdown-Syntax-Conventions#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001) | M-SYNTAX-LINKS-001]].                                                                                     |
| 1.4    | For **larger KBs**, top-level "Parts" MUST be implemented as distinct sub-folders within the primary KB folder. Each such sub-folder represents one "Part".                                                          | `research-methodology-kb/part-i-foundations/`                                                                                         | Per [[01-Universal-Architecture-And-Structure#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)                     | U-FORMAT-NAMING-001]].                                                                                    |
| 1.5    | For **smaller/moderately sized KBs**, top-level "Parts" MUST be major H1 sections (used as H2 in this document context, see [[05-Markdown-Syntax-Conventions#Standard: Markdown for Headings (M-SYNTAX-HEADINGS-001) | M-SYNTAX-HEADINGS-001]]) directly within `root.md`, with content nested or linked to subordinate files in the same primary KB folder. | Heading in `root.md`: `## Part I: Core Methods`                                                                                      | Decision criterion for "larger" is subjective but consider if `root.md` or file listing becomes unwieldy. |
| 1.6    | The content structure choice for Parts (sub-folders vs. `root.md` sections) MUST be consistently applied within a single KB.                                                                                         | N/A                                                                                                                                   |                                                                                                                                      |                                                                                                           |

**Illustrative Examples (Overall):**

For `root.md` in a larger KB linking to Part sub-folders:

```markdown
# Research Methodology Knowledge Base - Master Index

## Master Table of Contents

### Part I: Foundations of Research Methodology
- [Overview of Foundations](part-i-foundations-of-research-methodology/_overview.md)
- [Introduction to Research Methodology](part-i-foundations-of-research-methodology/01-introduction-to-research-methodology.md)

### Part II: Key Processes in Research
- [Overview of Key Processes](part-ii-key-processes-in-research/_overview.md)
```

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]], [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]], [[COL-ARCH-UNIVERSAL#Standard: Primary KB Section ("Part") Structure (U-STRUC-001)|U-STRUC-001]].

## Standard: Master KB Directory and Unique KB Identification (U-ARCH-002)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-ARCH-002`                          |
| Standard Name   | Master KB Directory and Unique KB Identification |
| Standard Category | Overall Knowledge Base Architecture |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                        | Example (if illustrative)                          | Notes / Further Specification (if any)            |
| :----- | :----------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- | :---------------------------------------------- |
| 2.1    | All individual KBs MUST reside within a single, master top-level directory.                                                                | `/digital-brain-vault/`                            | Name this master directory as preferred.         |
| 2.2    | Each KB primary folder name (per [[01-Universal-Architecture-And-Structure#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)|U-ARCH-001]]) MUST be globally unique.                                                                    | `research-methodology-kb`                           |                                                   |
| 2.3    | A master index file, named `kb-directory.md`, MUST reside within the master top-level directory.                                           | `/digital-brain-vault/kb-directory.md`             |                                                   |
| 2.4    | `kb-directory.md` MUST list all KBs, provide a 1-3 sentence description of each, and link to their respective `root.md` files.            | See Illustrative Example.                          | Uses [[05-Markdown-Syntax-Conventions#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]].  |
| 2.5    | The `root.md` of each KB MUST state the full name and primary scope of that KB in its introduction, matching its `kb-directory.md` entry. | Text in `root.md`: "Prompt Engineering Knowledge Base..." | Reinforces identity.                               |

**Illustrative Examples (Overall):**

Snippet from `/digital-brain-vault/kb-directory.md`:

```markdown
# Knowledge Base Directory

- **[Research Methodology KB](research-methodology-kb/root.md)**: Focuses on research design, data collection, analysis, and open science practices for generating complex workflows. Excludes funding and ethics.
- **[Prompt Engineering KB](prompt-engineering-kb/root.md)**: Covers principles, techniques, and frameworks for designing effective prompts for Large Language Models.
```

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]], [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]], [[COL-LINKING-UNIVERSAL#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]].

## Standard: Primary KB Section ("Part") Structure (U-STRUC-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-STRUC-001`                         |
| Standard Name   | Primary KB Section ("Part") Structure |
| Standard Category | Document Structure                    |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                                 | Example (if illustrative)                                 | Notes / Further Specification (if any)                                          |
| :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------- | :------------------------------------------------------------------------------ |
| 1.1    | Each "Part" (top-level primary section) MUST be fronted by an overview.                                                                             | File: `part-i-foundations/_overview.md`                  | Naming as per [[01-Universal-Architecture-And-Structure#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]] (for `_overview.md`). |
| 1.2    | If Parts are sub-folders (larger KBs per [[01-Universal-Architecture-And-Structure#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)|U-ARCH-001]]), the overview MUST be in an `_overview.md` file directly within that Part's folder.                           | `research-methodology-kb/part-i-foundations/_overview.md` |                                                                                 |
| 1.3    | If Parts are H2 sections in `root.md` (smaller KBs per [[01-Universal-Architecture-And-Structure#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)|U-ARCH-001]]), the overview and "Chapter" links MUST directly follow the Part's H2 heading.                 | `root.md` section H2: `## Part I: Principles`            |                                                                                 |
| 1.4    | This overview MUST briefly explain the Part's scope/purpose and include a linked Table of Contents to its main sub-sections ("Chapters").           | See Illustrative Example.                                 | Links are to Chapter files or H2 headings within the Part.                  |
| 1.5    | "Chapters" within a "Part" MUST be in a logical sequence.                                                                                          | N/A                                                       | Order set by naming prefix ([[01-Universal-Architecture-And-Structure#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]]) or heading order. |
| 1.6    | Each "Chapter" file/document MUST address a distinct, coherent topic.                                                                            | `01-introduction.md` for Introduction chapter          |                                                                                 |

**Illustrative Examples (Overall):**

Snippet from `/research-methodology-kb/part-i-foundations/_overview.md`:

```markdown
# Part I: Foundations of Research Methodology
This part lays the groundwork for understanding research...

## Chapters in this Part:
- [Chapter 1: Introduction](01-introduction-to-research-methodology.md)
- [Chapter 2: Core Concept of Research](02-core-concept-of-research.md)
```

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]], [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]], [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]].

## Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-STRUC-002`                         |
| Standard Name   | Content Document ("Chapter") Internal Structure |
| Standard Category | Document Structure                    |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                     | Example (if illustrative)                   | Notes / Further Specification (if any)           |
| :----- | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :----------------------------------------------- |
| 2.1    | Every "Chapter" document MUST begin with an H1 heading (the document title), which is the only H1 in the document.       | `# My Chapter Title`                        | Per [[05-Markdown-Syntax-Conventions#Standard: Markdown for Headings (M-SYNTAX-HEADINGS-001)|M-SYNTAX-HEADINGS-001]]. |
| 2.2    | An introductory "Topic Abstract" (1-3 paragraphs) MUST immediately follow the H1, summarizing purpose, scope, and takeaways. | Text follows H1.                            |                                                  |
| 2.3    | A Table of Contents (ToC) linking to all H2 (and significant H3) sections within the document MUST follow the abstract. | Markdown ToC links: `- [Section 1](#section-1)`      | Manual creation or user's chosen tool/plugin can be used for this. |
| 2.4    | Content MUST use hierarchical Markdown headings (H2-H6). Heading levels MUST NOT be skipped.                                  | `## Section 1` then `### Subsection 1.1`     | Per [[05-Markdown-Syntax-Conventions#Standard: Markdown for Headings (M-SYNTAX-HEADINGS-001)|M-SYNTAX-HEADINGS-001]]. |
| 2.5    | Each H2 section MUST represent a major sub-topic.                                                                       | N/A                                         |                                                  |
| 2.6    | A concluding section (e.g., H2 named "Summary") MUST be included.                                                         | `## Summary`                                |                                                  |
| 2.7    | A "See Also" section (H2) linking to related documents/sections MUST be included if relevant cross-references exist. | `## See Also` then `- [Related Document](related-doc.md)` | Uses [[05-Markdown-Syntax-Conventions#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]].   |

**Illustrative Examples (Overall):**

Partial structure of `01-introduction.md`:

```markdown
# Introduction to Research Methodology
This chapter introduces the core concepts...

## Table of Contents
- [What is Research?](#what-is-research)
- [Importance of Methodology](#importance-of-methodology)

## What is Research?
Research is a systematic investigation...
### Defining Research
...

## Importance of Methodology
...

## Summary
Key concepts include...

## See Also
- [Core Concept of Research](02-core-concept-of-research.md)
```

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]], [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Headings (M-SYNTAX-HEADINGS-001)|M-SYNTAX-HEADINGS-001]], [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]], [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Table of Contents Plugin Usage (O-USAGE-TOC-PLUGIN-001)|O-USAGE-TOC-PLUGIN-001]].

## Standard: Layered Information Presentation (U-DETAIL-LEVEL-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-DETAIL-LEVEL-001`                  |
| Standard Name   | Layered Information Presentation      |
| Standard Category | Hierarchical Organization & Detail Levels |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                   | Example (if illustrative)                                        | Notes / Further Specification (if any)                      |
| :----- | :------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------- | :-------------------------------------------------------- |
| 1.1    | Content MUST be structured to allow understanding from high-level overview down to specific details.                | `root.md` -> `_overview.md` -> `chapter.md` -> `H2/H3 sections` | This is an overarching principle.                         |
| 1.2    | Every major concept, method, or "Part" MUST begin with a concise summary/abstract.                                   | As per [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]] rule 2.2; [[02-Universal-Content-And-Schemas#Standard: Content Schema for "Methodology/Technique Descriptions" (U-SCHEMA-METHOD-001)|U-SCHEMA-METHOD-001]] rule 1.3     | Reinforces the information funnel approach.            |
| 1.3    | Following a summary, core principles or main ideas MUST be presented before detailed elaborations.                     | Within a "Method" schema, `Core Principles` H2 section.         |                                                           |
| 1.4    | Detailed elaborations (e.g., step-by-step instructions, complex arguments) MUST be placed within deeper hierarchical levels (e.g., H3, H4, or sub-documents if very extensive). | An `H3 Step 1.1 Sub-task`                                      | Avoid very long unbroken blocks of text at high levels.  |
| 1.5    | Practical examples or application notes MUST be included to concretize abstract information, typically after theoretical explanations. | H2 or H3 for "Examples" in a `Concept Definition` document. |                                                           |

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)|U-ARCH-001]], [[COL-ARCH-UNIVERSAL#Standard: Primary KB Section ("Part") Structure (U-STRUC-001)|U-STRUC-001]], [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]], [[COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Methodology/Technique Descriptions" (U-SCHEMA-METHOD-001)|U-SCHEMA-METHOD-001]], [[COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Concept Definitions" (U-SCHEMA-CONCEPT-001)|U-SCHEMA-CONCEPT-001]].

## Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-FORMAT-NAMING-001`                 |
| Standard Name   | File and Folder Naming Conventions    |
| Standard Category | Formatting & Styling                  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                                                | Notes / Further Specification (if any)                                                                                                |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| 1.1    | **Folder Names:** MUST be in all lowercase kebab-case.                                                                                          | `part-i-foundations/`, `kb-specific-standards/`                                          | Words separated by hyphens.                                                                                                           |
| 1.2    | **Individual Standard Definition Files:** The filename (excluding `.md` extension) MUST be the exact Standard ID. Casing of the ID MUST be preserved. | `U-ARCH-001.md`, `M-SYNTAX-TODO-001.md`                                                  | This applies to files that define one specific standard.                                                                              |
| 1.3    | **General Content Files (Non-Standards, Non-Guides, Non-Collections):** Filenames (excluding extension) MUST be descriptive and in all lowercase kebab-case. Numerical prefixes (`00-`, `01-`) MAY be used for sequencing. | `01-introduction.md`, `llm-capabilities.md`                                              | This is for typical content chapters/articles within other KBs.                                                                       |
| 1.4    | **Collection/Grouping Documents (e.g., within Standards KB):** These files group related individual standard definitions or discuss a category. Filename pattern: `COL-[SUBJECT]-[DESCRIPTOR].md`. `COL-` prefix is literal. `[SUBJECT]` and `[DESCRIPTOR]` SHOULD be uppercase, concise, hyphenated keywords. | `COL-ARCH-UNIVERSAL.md`, `COL-SYNTAX-MARKDOWN.md`                                        | Used for thematic compilations. The old numerical prefixes (`01-`) are superseded by this naming. Order is managed by `root.md` ToC.  |
| 1.5    | **Guide Documents (e.g., within Standards KB):** These files provide guidance on using items or processes. Filename pattern: `GUIDE-[TASK/SUBJECT].md`. `GUIDE-` prefix is literal. `[TASK/SUBJECT]` SHOULD be uppercase, concise, hyphenated keywords. | `GUIDE-TASK-BASED.md`, `GUIDE-ASSEMBLY-SCRIPT.md`                                        | For how-to or explanatory guides related to the KB's subject matter.                                                                  |
| 1.6    | **Reserved Names for Structural Files:** Names like `root.md`, `_overview.md`, `_kb_definition.md`, `_key_definitions.md`, `kb-directory.md`, `tag-glossary-definition.md` MUST be used exactly as specified (all lowercase kebab-case). | `_overview.md`, `_key_definitions.md`                                                    | Enforces architectural consistency.                                                                                                   |
| 1.7    | **Script Files & Their Documentation:** Script basenames (e.g., `.py`, `.sh`) SHOULD use snake_case and reside in `scripts/`. User-facing guides for scripts in `scripts/docs/` SHOULD use `GUIDE-[SCRIPT-NAME].md`. Detailed technical/developer documentation for scripts in `scripts/docs/` SHOULD use `DOC-[SCRIPT-NAME]-LOGIC.md` or similar. | `scripts/resolver_script.py`, `scripts/docs/GUIDE-RESOLVER-SCRIPT.md`, `scripts/docs/DOC-RESOLVER-LOGIC.md` | Separates user guides from technical docs for scripts. |
| 1.8    | **General Principle:** All file and folder names MUST be descriptive and concise, clearly indicating primary content or purpose.                    | N/A                                                                                      |                                                                                                                                       |

**Cross-References to Other Standard IDs:** [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]], [[COL-LINKING-UNIVERSAL#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]].