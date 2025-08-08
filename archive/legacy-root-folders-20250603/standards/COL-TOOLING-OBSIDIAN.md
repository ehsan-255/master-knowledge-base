---
title: 'Collection: Obsidian Usage Conventions'
aliases:
- Obsidian Usage Rules
- COL-TOOLING-OBSIDIAN
tags:
- content-type/standards-collection
- criticality/p0-critical
- kb-id/standards
- status/deprecated
- topic/obsidian
- topic/tooling
kb-id: standards
info-type: standards-collection
primary-topic: 'DEPRECATED: Collection of specific conventions for using Obsidian
  features to enhance knowledge bases.'
related-standards:
- SF-LINKS-INTERNAL-SYNTAX
- CS-LINKING-INTERNAL-POLICY
- MT-TAGS-IMPLEMENTATION
- MT-TAGGING-STRATEGY-POLICY
- AS-STRUCTURE-KB-PART
- CS-POLICY-PART-OVERVIEW
- SF-TOC-SYNTAX
- CS-TOC-POLICY
- SF-TRANSCLUSION-SYNTAX
- CS-MODULARITY-TRANSCLUSION-POLICY
- SF-CALLOUTS-SYNTAX
- CS-ADMONITIONS-POLICY
version: 0.5.0
date-created: '2025-05-15'
date-modified: '2025-06-17T02:29:13Z'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
**DEPRECATED:** This collection document is superseded by the new atomic standards architecture. Relevant content has been refactored into individual standard, policy, and guide documents located in `/master-knowledge-base/standards/src/`. Please refer to `[[AS-ROOT-STANDARDS-KB]]` for an overview of the new standards or consult `[[GM-GUIDE-KB-USAGE]]`.

# Obsidian Usage Conventions

This document outlines specific conventions for using Obsidian features to enhance the knowledge bases, ensuring consistency with universal standards.

## Table of Contents

- [[#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)]]
- [[#Standard: Obsidian Tag Implementation (O-USAGE-TAGS-001)]]
- [[#Standard: Obsidian Folder Notes for Part Overviews (O-USAGE-FOLDERS-NOTES-001)]]
- [[#Standard: Obsidian Table of Contents Mandate (O-USAGE-TOC-MANDATE-001)]]
- [[#Standard: Obsidian Content Embedding (Transclusion) (O-USAGE-TRANSCLUSION-001)]]
- [[#Standard: Obsidian Callout Usage (O-USAGE-CALLOUTS-001)]]
- [[#Standard: Obsidian Table of Contents Plugin Usage (O-USAGE-TOC-PLUGIN-001)]]

## Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `O-USAGE-LINKS-001`                   |
| Standard Name   | Obsidian Internal Linking Conventions |
| Standard Category | Obsidian Feature Usage & Conventions  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                      | Example (if illustrative)                                    | Notes / Further Specification (if any)                                 |
| :----- | :------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------- |
| 1.1    | Wikilink format `[[path/from/master-kb-root/to/file]]` or `[[path/from/master-kb-root/to/file|Optional Display Text]]` IS THE MANDATORY format for all internal links to other documents (notes) within Obsidian. The path MUST start from the `master-knowledge-base` root directory (e.g., `Standards/standard-file.md` or `llm-content-generation-cookbook-kb/recipe.md`). This ensures link portability and unambiguous targeting. | `[[Standards/01-Universal-Architecture-And-Structure]]`<br/>`[[llm-content-generation-cookbook-kb/part-ii-recipes/01-recipe-methodology-schema|Methodology Recipe]]` | This rule is critical for link integrity when using automation scripts or when the vault is processed by external tools. Shortest paths or relative paths MUST NOT be used. |
| 1.2    | To link to specific headings within a note, `[[path/from/master-kb-root/to/file#Heading Name]]` or `[[path/from/master-kb-root/to/file#Heading Name|Optional Display Text]]` MUST be used. The path MUST start from the `master-knowledge-base` root. | `[[Standards/01-Universal-Architecture-And-Structure#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)]]` |
| 1.3    | Obsidian's path autocompletion for links (triggered by typing `[[`) MUST be utilized to ensure accuracy. Authors should start typing the path from the root (e.g., `[[Standards/...`). | Begin typing `[[Standards/...` Obsidian suggests files.      |
| 1.4    | Pipe characters `|` within wikilink display text or filenames MUST NOT be escaped with a backslash.                                                   | Correct: `[[filename|Display Text with | Pipe]]` Incorrect: `[[filename|Display Text with \| Pipe]]` | Escaping is unnecessary and may break links. |
| 1.5    | Internal links using Markdown link syntax `[Text](file.md)` or `[Text](../file.md)` MUST NOT be used for linking to notes within the vault. Only wikilinks are allowed for internal links. | Incorrect: `[See this](../concepts/my-other-note.md)` | Use only wikilinks for internal notes. |
| 1.6    | The use of relative paths (e.g., `[[../folder/file]]`) or shortest unique paths (e.g., `[[file]]`) in wikilinks is PROHIBITED. Only paths from the `master-knowledge-base` root are allowed. | Incorrect: `[[../concepts/my-note]]`, `[[my-note]]`<br/>Correct: `[[kb-name/concepts/my-note]]` |

**Illustrative Example Table:**

| Path Type                      | Example (Linking from any file to `master-knowledge-base/Standards/01-Universal-Architecture-And-Structure.md`) | Allowed? |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------|----------|
| **Path from master KB root**   | `[[Standards/01-Universal-Architecture-And-Structure]]`                                                         | ✅       |
| Shortest path when possible    | `[[01-Universal-Architecture-And-Structure]]`                                                                   | ❌       |
| Relative path from file        | `[[../Standards/01-Universal-Architecture-And-Structure]]` (if current file is in a subfolder of root)           | ❌       |

## Standard: Obsidian Tag Implementation (O-USAGE-TAGS-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `O-USAGE-TAGS-001`                    |
| Standard Name   | Obsidian Tag Implementation           |
| Standard Category | Obsidian Feature Usage & Conventions  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                          | Example (if illustrative)                              | Notes / Further Specification (if any)                                   |
| :----- | :------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :----------------------------------------------------------------------- |
| 1.1    | Tags MUST be declared in YAML frontmatter as per [[03-Universal-Linking-Metadata-And-Utility#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]]. Inline `#tag` usage within the body of the text MUST NOT be used for primary content tagging. | See [[03-Universal-Linking-Metadata-And-Utility#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]] example.                                 | Maintains structured metadata. Inline tags may be used for temporary, personal organization if clearly distinguished from formal KB content. |
| 1.2    | Obsidian's "Tags" pane (typically in the left sidebar) MUST be used for exploring and navigating by tag.                        | Access via left sidebar (default UI).                 |                                                                          |
| 1.3    | The "Tag Wrangler" community plugin IS THE RECOMMENDED tool for managing tags (renaming, merging, etc.) once a KB is established and has a significant number of tags.  | Use "Tag Wrangler" to rename `#topic/old` to `#topic/new`. | Aids tag hygiene. Install from community plugins.                   |

**Cross-References to Other Standard IDs:** [[COL-LINKING-UNIVERSAL#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]].

## Standard: Obsidian Folder Notes for Part Overviews (O-USAGE-FOLDERS-NOTES-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `O-USAGE-FOLDERS-NOTES-001`           |
| Standard Name   | Obsidian Folder Notes for Part Overviews |
| Standard Category | Obsidian Feature Usage & Conventions  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                      | Example (if illustrative)                                                  | Notes / Further Specification (if any)                |
| :----- | :--------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- | :---------------------------------------------------- |
| 1.1    | When Parts of a KB are organized into sub-folders (per [[01-Universal-Architecture-And-Structure#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)|U-ARCH-001]]), the `_overview.md` file for that Part MUST be configured as a "folder note" using a community plugin like "Folder Note Core" or a similar, well-maintained alternative that allows clicking a folder to open its associated note. | Folder `/part-i/` has note `_overview.md` shown when clicking folder. | Creates a seamless overview experience.                     |

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)|U-ARCH-001]], [[COL-ARCH-UNIVERSAL#Standard: Primary KB Section ("Part") Structure (U-STRUC-001)|U-STRUC-001]].

## Standard: Obsidian Table of Contents Mandate (O-USAGE-TOC-MANDATE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `O-USAGE-TOC-MANDATE-001`             |
| Standard Name   | Obsidian Table of Contents Mandate    |
| Standard Category | Obsidian Feature Usage & Conventions  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                               | Example (if illustrative)                          | Notes / Further Specification (if any)              |
| :----- | :---------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------- | :-------------------------------------------------- |
| 1.1    | A Table of Contents, as mandated by [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]], MUST be present in 'Chapter' documents. While manual creation is possible, using an Obsidian community plugin to generate and maintain this ToC is a best practice for accuracy and efficiency. | Command: `Insert Table of Contents`.            | Ensures ToC is accurate and automatically updated. The generated ToC MUST use standard Markdown anchor links. |

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]].

## Standard: Obsidian Content Embedding (Transclusion) (O-USAGE-TRANSCLUSION-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `O-USAGE-TRANSCLUSION-001`            |
| Standard Name   | Obsidian Content Embedding (Transclusion) |
| Standard Category | Obsidian Feature Usage & Conventions  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                          | Example (if illustrative)                                             | Notes / Further Specification (if any)            |
| :----- | :------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------ |
| 1.1    | Obsidian's block/section embedding (transclusion) `![[filename#^blockID]]` or `![[filename#Section Heading]]` MUST be used when content from one note needs to be displayed verbatim in another to maintain a single source of truth (as per [[03-Universal-Linking-Metadata-And-Utility#Standard: Designing for Content Modularity (U-MODULAR-001)|U-MODULAR-001]]). | `![[shared-definitions#^pico]]` (to embed a block named `^pico`) | Reduces content duplication and improves maintainability. |
| 1.2    | For transcluding entire notes, `![[filename]]` MUST be used.                                                                  | `![[important-disclaimer]]`                                        |                                                   |

**Cross-References to Other Standard IDs:** [[COL-LINKING-UNIVERSAL#Standard: Designing for Content Modularity (U-MODULAR-001)|U-MODULAR-001]].

## Standard: Obsidian Callout Usage (O-USAGE-CALLOUTS-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `O-USAGE-CALLOUTS-001`                |
| Standard Name   | Obsidian Callout Usage                |
| Standard Category | Obsidian Feature Usage & Conventions  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Standard Obsidian callout syntax (`> [!TYPE] Optional Title`) MUST be used for admonitions like notes, warnings, errors, tips, abstracts, etc. | `> [!NOTE] This is important.`<br>`> [!WARNING] Proceed with caution.` | Supported types include `note`, `abstract`, `info`, `todo`, `tip`, `success`, `question`, `warning`, `failure`, `danger`, `bug`, `example`, `quote`. |
| 1.2    | Callout types MUST be used semantically according to their intended meaning (e.g., `[!WARNING]` for warnings, not for general emphasis).        | N/A                                                          | Consistent use improves readability and accessibility.                     |
| 1.3    | Callout titles, if used, SHOULD be concise and accurately reflect the callout's content.                                                        | `> [!TIP] Performance Boost`                                 |                                                                              |
| 1.4    | Content within callouts MUST be indented correctly under the callout block.                                                                     | `> [!NOTE]\n> This is the first line.\n> This is the second line.` |                                                                              |

**Cross-References to Other Standard IDs:** [[COL-GOVERNANCE-UNIVERSAL#Standard: Deprecation Policy for Standards (U-DEPRECATION-001)|U-DEPRECATION-001]] (example usage).

## Standard: Obsidian Table of Contents Plugin Usage (O-USAGE-TOC-PLUGIN-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `O-USAGE-TOC-PLUGIN-001`              |
| Standard Name   | Obsidian Table of Contents Plugin Usage |
| Standard Category | Obsidian Feature Usage & Conventions  |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | When a Table of Contents (ToC) is required by a content standard (e.g., [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]]), an Obsidian community plugin (e.g., "Dynamic ToC" or a similar well-maintained plugin) IS THE RECOMMENDED method for generating and maintaining the ToC. | Using a plugin command like "Insert/Update Table of Contents". | This promotes accuracy and reduces manual effort.                            |
| 1.2    | The generated ToC MUST use standard Markdown anchor links (`[Section Name](#section-name)`) that are compatible with Obsidian's navigation.   | `- [My Section](#my-section)`                                |                                                                              |
| 1.3    | The ToC SHOULD typically be configured to include H2 and H3 headings. Deeper levels (H4-H6) MAY be included if essential for navigation in very long documents. | N/A                                                          |                                                                              |
| 1.4    | The ToC generated by a plugin SHOULD be periodically reviewed to ensure it accurately reflects the document structure.                            | N/A                                                          | Especially after significant heading changes.                              |

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]], [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Table of Contents Mandate (O-USAGE-TOC-MANDATE-001)|O-USAGE-TOC-MANDATE-001]].
