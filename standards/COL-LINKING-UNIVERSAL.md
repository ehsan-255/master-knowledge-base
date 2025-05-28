---
title: "Collection: Universal Linking, Metadata, and Utility Standards"
aliases:
  - Universal Linking Standards
  - COL-LINKING-UNIVERSAL
tags:
  - kb-id/standards
  - content-type/standards-collection
  - status/deprecated # Updated status
  - topic/linking
  - topic/metadata
  - topic/utility-standards
kb-id: standards
info-type: standards-collection # This info-type is still valid for a collection, even if deprecated
primary-topic: 'DEPRECATED: Collection of universal standards for interlinking, metadata, tagging, citations, modularity, accessibility, and assets.'
related-standards: ["SF-LINKS-INTERNAL-SYNTAX", "CS-LINKING-INTERNAL-POLICY", "MT-TAGS-IMPLEMENTATION", "MT-TAGGING-STRATEGY-POLICY", "SF-FORMATTING-CITATIONS", "SF-TRANSCLUSION-SYNTAX", "CS-MODULARITY-TRANSCLUSION-POLICY", "SF-ACCESSIBILITY-IMAGE-ALT-TEXT", "CS-POLICY-ACCESSIBILITY", "AS-STRUCTURE-ASSET-ORGANIZATION"]
version: '0.4.0' # Incremented version
date-created: '2025-05-15'
date-modified: '2024-07-15T12:00:00Z' # Placeholder for current date
---

**<font color="red">IMPORTANT: This document is deprecated.</font>**

The standards and guidelines previously contained in this collection have been refactored into individual, atomic standard documents. Please refer to the new standards located in the `/master-knowledge-base/standards/src/` directory.

Key new standards that supersede content from this collection include:
*   `[[SF-LINKS-INTERNAL-SYNTAX]]` and `[[CS-LINKING-INTERNAL-POLICY]]` (for U-INTERLINK-001)
*   `[[MT-TAGS-IMPLEMENTATION]]` and `[[MT-TAGGING-STRATEGY-POLICY]]` (for U-TAG-001)
*   `[[SF-FORMATTING-CITATIONS]]` (for U-CITE-001)
*   `[[SF-TRANSCLUSION-SYNTAX]]` and `[[CS-MODULARITY-TRANSCLUSION-POLICY]]` (for U-MODULAR-001)
*   `[[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]` and `[[CS-POLICY-ACCESSIBILITY]]` (for U-ACCESSIBILITY-001)
*   `[[AS-STRUCTURE-ASSET-ORGANIZATION]]` (for U-ASSETS-001)

For guidance on the new standards structure, please consult [[GM-GUIDE-KB-USAGE_ID_PLACEHOLDER]] (once available).

---

# Universal Linking, Metadata, and Utility Standards

This document details universal standards for interlinking content, metadata and tagging strategies, citation practices, content modularity, accessibility, and asset organization.

## Table of Contents

- [[#Standard: Internal Knowledge Base Linking (U-INTERLINK-001)]]
- [[#Standard: Core Tagging Strategy for KB Content (U-TAG-001)]]
- [[#Standard: Citing External Sources (U-CITE-001)]]
- [[#Standard: Designing for Content Modularity (U-MODULAR-001)]]
- [[#Standard: Image Accessibility and Alt Text (U-ACCESSIBILITY-001)]]
- [[#Standard: Asset Organization (U-ASSETS-001)]]

## Standard: Internal Knowledge Base Linking (U-INTERLINK-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-INTERLINK-001`                     |
| Standard Name   | Internal Knowledge Base Linking       |
| Standard Category | Interlinking & Relationships          |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                | Example (if illustrative)                                    | Notes / Further Specification (if any)                        |
| :----- | :------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :------------------------------------------------------------ |
| 1.1    | Internal links between documents/notes within the same KB MUST be used extensively to connect related concepts, methods, and sections. | `See also [Related Concept](related-concept.md)`                            | Uses [[05-Markdown-Syntax-Conventions#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]].             |
| 1.2    | Links MUST use the syntax specified in [[05-Markdown-Syntax-Conventions#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]] and [[06-Obsidian-Usage-Conventions#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)|O-USAGE-LINKS-001]].                                                              | `[Some File](../part-i/some-file.md)` or `[[some-file]]`      | Ensures consistency.                                          |
| 1.3    | Link text MUST be descriptive. If using a raw wikilink as text is not descriptive, the pipe `|` for display text MUST be used: `[[file-name|Descriptive Link Text]]`. | `For more on PICO, see [[Standards/pico-framework|the PICO Framework]].` | This rule applies specifically to wikilinks ([[06-Obsidian-Usage-Conventions#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)|O-USAGE-LINKS-001]]). |
| 1.4    | "See Also" sections (per [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]]) are a primary mechanism for grouping related links.                                            | At end of document, lists related concept files.             |                                                               |
| 1.5    | Links within the main body of the text MUST be contextually relevant. Over-linking MUST be avoided.                                            | N/A                                                          | Links should enhance understanding, not distract.               |

**Cross-References to Other Standard IDs:** [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]], [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)|O-USAGE-LINKS-001]], [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]].

## Standard: Core Tagging Strategy for KB Content (U-TAG-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-TAG-001`                           |
| Standard Name   | Core Tagging Strategy for KB Content  |
| Standard Category | Metadata & Tagging Strategy           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                          | Example (if illustrative)                                        | Notes / Further Specification (if any)                            |
| :----- | :------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- | :-------------------------------------------------------------- |
| 1.1    | Tags MUST be declared within YAML frontmatter at the beginning of each document.                                             | See Illustrative Example.                                        | Enables structured metadata processing. Per [[05-Markdown-Syntax-Conventions#Standard: Markdown YAML Frontmatter (M-SYNTAX-YAML-001)|M-SYNTAX-YAML-001]]. |
| 1.2    | Within YAML, tags MUST be listed under a `tags:` key as a block list of strings.                                                   | `tags:\n  - my-tag\n  - another-tag`                              | Per [[05-Markdown-Syntax-Conventions#Standard: Markdown YAML Frontmatter (M-SYNTAX-YAML-001)|M-SYNTAX-YAML-001]]. |
| 1.3    | All tag strings MUST be in kebab-case.                                                                                       | `topic/research-methods`                                         | `topic/researchMethods` is incorrect.                              |
| 1.4    | Tags MAY use forward slashes `/` to indicate internal hierarchy or categorization. Hierarchy usage MUST be consistent.          | `topic/statistics/inferential`                                   | Top-level categories first (e.g., `topic/`, `status/`).         |
| 1.5    | Every content document MUST include at least one `topic/*` tag.                                                               | `topic/systematic-review`                                        | Multiple `topic/*` tags are allowed for interdisciplinary topics. |
| 1.6    | Every document MUST include ONE `status/*` tag (e.g., `status/idea`, `status/draft`, `status/review-needed`, `status/final`, `status/archived`). | `status/draft`                                               | Only one status tag per document.                               |
| 1.7    | `kb-master-index` MUST tag `kb-directory.md`. `kb-root` AND `kb-id/[kb-name]` (e.g., `kb-id/research-methodology`) MUST tag `root.md` files. `kb-part-overview` MUST tag Part `_overview.md` files. | `tags:\n  - kb-root\n  - kb-id/prompt-engineering`             | Required for structural identification.                      |
| 1.8    | `content-type/*` tags MUST be used (e.g., `content-type/concept-definition`, `content-type/methodology-guide`, `content-type/schema`). The controlled vocabulary for the `{type}` part of `content-type/{type}` is defined in [[U-METADATA-FRONTMATTER-RULES-001]]. | `content-type/methodology-guide`                              | Helps filter for specific kinds of content.                       |
| 1.9    | A `tag-glossary-definition.md` file, listing all official tags, their hierarchy, and meaning, MUST be maintained within the master top-level directory (per [[01-Universal-Architecture-And-Structure#Standard: Master KB Directory and Unique KB Identification (U-ARCH-002)|U-ARCH-002]]). | Located at `/digital-brain-vault/tag-glossary-definition.md` | Links to its tag standards, updated as new tags are officialized. **The file `tag-glossary-definition.md` (located at `./master-knowledge-base/tag-glossary-definition.md`) is the canonical source for the complete list of official tags, their hierarchies, and their definitions. All tag values used must conform to those defined in the glossary.** |

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: Master KB Directory and Unique KB Identification (U-ARCH-002)|U-ARCH-002]], [[COL-ARCH-UNIVERSAL#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]], [[COL-SYNTAX-MARKDOWN#Standard: Markdown YAML Frontmatter (M-SYNTAX-YAML-001)|M-SYNTAX-YAML-001]].

## Standard: Citing External Sources (U-CITE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-CITE-001`                          |
| Standard Name   | Citing External Sources               |
| Standard Category | Referencing & Citations               |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                                     | Example (if illustrative)                                    | Notes / Further Specification (if any)                   |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :------------------------------------------------------- |
| 1.1    | Claims, direct quotes, or specific data points derived from external published or citable sources MUST be attributed.                                    | N/A                                                          | Upholds academic integrity.                            |
| 1.2    | **APA 7th Edition** IS THE ADOPTED STYLE for in-text citations and reference lists. This style MUST be used consistently across all KBs.            | (Smith, 2023) or Smith (2023) stated...                    | Definitive choice of APA 7th.                           |
| 1.3    | In-text citations MUST be used for specific attributions within the body of the text.                                                                    | "...as shown by (Jones et al., 2022)."                      |                                                          |
| 1.4    | A "References" section (H2 heading) MUST be included at the end of any document that contains citations, listing all cited sources in APA 7th format. | `## References\nJones, P. (2022). *Book Title*. Publisher.` |                                                          |
| 1.5    | For online sources, a direct hyperlink to the source MUST be included in the References list if publicly available. A "retrieved date" MAY be included for non-archived links. | "... Retrieved from https://example.com/article"            | [[05-Markdown-Syntax-Conventions#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]]. "Retrieved date" helps with link rot awareness. |

**Cross-References to Other Standard IDs:** [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]].

## Standard: Designing for Content Modularity (U-MODULAR-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-MODULAR-001`                       |
| Standard Name   | Designing for Content Modularity      |
| Standard Category | Modularity & Reusability              |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                               | Example (if illustrative)                                                     | Notes / Further Specification (if any)                              |
| :----- | :------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| 1.1    | Content for distinct concepts, methods, or steps MUST be atomic enough to be understood and potentially reused with minimal context bleeding from surrounding, unrelated topics. | A "Definition of PICO" is its own section, not buried in a broader text. | Aligns with schema standards.                                  |
| 1.2    | Transclusion or embedding of content blocks/sections (per [[06-Obsidian-Usage-Conventions#Standard: Obsidian Content Embedding (Transclusion) (O-USAGE-TRANSCLUSION-001)|O-USAGE-TRANSCLUSION-001]]) MUST be used instead of duplicating substantial common content. | `![[core-principles#section-on-ethics]]` (Obsidian syntax)         | Reduces duplication.                    |
| 1.3    | Content documents ("Chapters") MUST be self-contained units where possible, using links (per [[03-Universal-Linking-Metadata-And-Utility#Standard: Internal Knowledge Base Linking (U-INTERLINK-001)|U-INTERLINK-001]]) to provide context from other documents rather than extensively repeating it. |                                                                             | A "Chapter" on T-Tests should link to basics of Hypothesis Testing. |

**Cross-References to Other Standard IDs:** [[COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Methodology/Technique Descriptions" (U-SCHEMA-METHOD-001)|U-SCHEMA-METHOD-001]], [[COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Concept Definitions" (U-SCHEMA-CONCEPT-001)|U-SCHEMA-CONCEPT-001]], [[COL-LINKING-UNIVERSAL#Standard: Internal Knowledge Base Linking (U-INTERLINK-001)|U-INTERLINK-001]], [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Content Embedding (Transclusion) (O-USAGE-TRANSCLUSION-001)|O-USAGE-TRANSCLUSION-001]].

## Standard: Image Accessibility and Alt Text (U-ACCESSIBILITY-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-ACCESSIBILITY-001`                 |
| Standard Name   | Image Accessibility and Alt Text      |
| Standard Category | Accessibility                         |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | All images embedded in content MUST include descriptive alternative text (alt text) using the Markdown image syntax `![Alt text](path/to/image.png)`. | `![Bar chart showing Q1 sales figures](assets/images/q1-sales.png)` | Alt text should convey the meaning or purpose of the image for visually impaired users or if the image fails to load. |
| 1.2    | Alt text MUST be concise yet sufficiently descriptive. Avoid generic alt text like "image" or "picture".                                          | Good: "Logo of Project Phoenix" Bad: "logo"                  | If an image is purely decorative and adds no informational value, an empty alt text `![]()` MAY be used, but this should be rare. |
| 1.3    | Headings (H1-H6) MUST be used semantically to structure content and serve as landmarks. They MUST be succinct and accurately reflect section content. | N/A                                                          | Aids screen reader navigation.                                               |

**Cross-References to Other Standard IDs:** [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]]

## Standard: Asset Organization (U-ASSETS-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-ASSETS-001`                        |
| Standard Name   | Asset Organization                    |
| Standard Category | Formatting & Styling                  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                                  | Example (if illustrative)                               | Notes / Further Specification (if any)                                       |
| :----- | :------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ | :--------------------------------------------------------------------------- |
| 1.1    | All non-Markdown assets (images, diagrams, PDFs, code snippets if stored as separate files) associated with a KB MUST reside in a top-level `assets` folder within that KB's primary folder. | `research-methodology-kb/assets/`                       |                                                                              |
| 1.2    | Within the `assets` folder, sub-folders SHOULD be used to categorize assets (e.g., `images`, `diagrams`, `code-snippets`, `pdfs`).                 | `research-methodology-kb/assets/images/my-chart.png`    |                                                                              |
| 1.3    | Asset file names MUST follow the `U-FORMAT-NAMING-001` standard (kebab-case, descriptive).                                                        | `q1-sales-report.pdf`, `user-flow-diagram.svg`          |                                                                              |
| 1.4    | Permitted image formats are `png`, `svg`, `jpg`/`jpeg`. `png` or `svg` ARE PREFERRED for diagrams and screenshots; `jpg` for photographic images. | N/A                                                     | This ensures broad compatibility and quality.                                |

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]], [[COL-LINKING-UNIVERSAL#Standard: Image Accessibility and Alt Text (U-ACCESSIBILITY-001)|U-ACCESSIBILITY-001]].