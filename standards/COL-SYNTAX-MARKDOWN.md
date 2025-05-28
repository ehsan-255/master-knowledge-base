---
title: 'Collection: Markdown Syntax Conventions'
aliases: ['Markdown Syntax Rules', 'COL-SYNTAX-MARKDOWN']
tags:
  - kb-id/standards
  - content-type/standards-collection
  - status/final
  - topic/markdown
  - topic/syntax
kb-id: standards
info-type: standards-collection
primary-topic: 'Collection of specific Markdown syntax rules for consistency, readability, and interoperability.'
related-standards: ['M-SYNTAX-YAML-001', 'U-METADATA-FRONTMATTER-RULES-001']
version: '0.3.3'
date-created: '2025-05-15'
date-modified: '2025-05-23'
---

# Markdown Syntax Conventions

This document details the specific Markdown syntax rules that MUST be followed for all content creation to ensure consistency, readability, and interoperability.

## Table of Contents

- [[#Standard: Markdown YAML Frontmatter (M-SYNTAX-YAML-001)]]
- [[#Standard: Markdown for Headings (M-SYNTAX-HEADINGS-001)]]
- [[#Standard: Markdown for Lists (Ordered and Unordered) (M-SYNTAX-LISTS-001)]]
- [[#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)]]
- [[#Standard: Markdown for Emphasis (Bold, Italic) (M-SYNTAX-EMPHASIS-001)]]
- [[#Standard: Markdown for Blockquotes (M-SYNTAX-BLOCKQUOTE-001)]]
- [[#Standard: Markdown for Code (Inline and Blocks) (M-SYNTAX-CODE-001)]]
- [[#Standard: Markdown for Tables (M-SYNTAX-TABLE-001)]]
- [[#Standard: Markdown General Formatting (M-SYNTAX-GENERAL-001)]]
- [[#Standard: Markdown for Images (M-SYNTAX-IMAGES-001)]]
- [[#Standard: Escaping Special Markdown Characters (M-SYNTAX-ESCAPING-001)]]
- [[#Standard: Markdown for Definition Lists (M-SYNTAX-DEFLIST-001)]]
- [[#Standard: Markdown for Footnotes (M-SYNTAX-FOOTNOTES-001)]]
- [[#Standard: Markdown for Math Equations (M-SYNTAX-MATH-001)]]
- [[#Standard: Markdown for Diagrams (Mermaid) (M-SYNTAX-DIAGRAMS-001)]]

## Standard: Markdown YAML Frontmatter (M-SYNTAX-YAML-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-SYNTAX-YAML-001`                   |
| Standard Name   | Markdown YAML Frontmatter             |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                             | Example (if illustrative)                               | Notes / Further Specification (if any)                               |
| :----- | :------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------ | :------------------------------------------------------------------- |
| 1.1    | A single YAML frontmatter block, enclosed by triple hyphens (`---`), MUST be present at the very beginning of every Markdown document. | See Illustrative Example.                             | No content or blank lines are permitted before the opening `---`.    |
| 1.2    | YAML keys in Markdown frontmatter MUST use **kebab-case** (e.g., `date-created`). Snake_case (e.g., `date_created`) MUST NOT be used for YAML keys in frontmatter. The use of snake_case is permissible only within Python code examples or when referring to Python-specific variable names discussed in the document body, and not for defining YAML frontmatter keys themselves. | `date-created: 2023-10-28`                          | Enforces a single, consistent style for all YAML keys in frontmatter.      |
| 1.3    | Values for YAML keys MUST be appropriately typed (string, number, boolean, list, dictionary). Strings do not typically require quotes unless they contain special characters. | `version: 1.0` (number), `draft: true` (boolean)      |                                                                      |
| 1.4    | Lists in YAML MUST use the block list syntax (hyphen and space followed by the item).                           | `tags:\n  - tag1\n  - tag2`                             | Inline list syntax (e.g., `tags: [tag1, tag2]`) MUST NOT be used. |
| 1.5    | HTML comments or any other non-rendered metadata MUST NOT be used within the YAML block or anywhere else in the document for metadata purposes. | N/A                                                   | All metadata intended for processing MUST be in valid YAML format. |

**Illustrative Examples (Overall):**

```yaml
---
title: My Document Title
date-created: 2023-01-15
tags:
  - primary-topic
  - status/draft
version: 1.1
custom-field: Some value
---

# Document Content Starts Here
...
```

**Cross-References to Other Standard IDs:** [[COL-LINKING-UNIVERSAL#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]].

## Standard: Markdown for Headings (M-SYNTAX-HEADINGS-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-SYNTAX-HEADINGS-001`               |
| Standard Name   | Markdown for Headings                 |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                     | Example (if illustrative)                      | Notes / Further Specification (if any)  |
| :----- | :-------------------------------------------------------------------------------------------------- | :------------------------------------------- | :------------------------------------ |
| 1.1    | Headings MUST be created using ATX style (hash symbols `#` at the beginning of the line).             | `# H1` `## H2` `### H3`                       | Setext style (underline) MUST NOT be used. |
| 1.2    | There MUST be a single space between the hash symbol(s) and the heading text.                       | `# My Heading` (Correct) ` #My Heading` (Incorrect) |                                         |
| 1.3    | Heading levels MUST NOT be skipped (e.g., H1 followed by H3 directly is incorrect).                   | Correct: H1 -> H2 -> H3. Incorrect: H1 -> H3. | Governed by [[01-Universal-Architecture-And-Structure#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]]. |
| 1.4    | Documents MUST start with one H1, which is the document title. All subsequent section headings MUST use H2 or lower.    | `# Document Title\n## Section 1`             | Enforces a single top-level title per document. |
| 1.5    | A blank line MUST precede and follow every heading for readability and to prevent parsing issues.     | `Text above\n\n## Heading\n\nText below`      |                                         |

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]].

## Standard: Markdown for Lists (Ordered and Unordered) (M-SYNTAX-LISTS-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-SYNTAX-LISTS-001`                  |
| Standard Name   | Markdown for Lists (Ordered and Unordered) |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                    | Example (if illustrative)                             | Notes / Further Specification (if any)                    |
| :----- | :------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------- | :-------------------------------------------------------- |
| 1.1    | Unordered lists MUST use a hyphen (`-`) followed by a space as the marker.                                                            | `- Item 1\n- Item 2`                                   | Asterisk (`*`) or plus (`+`) MUST NOT be used for unordered list markers. |
| 1.2    | Ordered lists MUST use a number followed by a period and a space (e.g., `1. `) as the marker. Numbers MUST start from 1 for each distinct list.         | `1. First item\n2. Second item`                       | Markdown renderers typically handle sequential numbering even if source numbers are all `1.`. |
| 1.3    | Nested list items MUST be indented by exactly two (2) spaces relative to the start of the parent item's marker text.      | `- Parent\n  - Child 1\n    - Grandchild`             | Inconsistent indentation (e.g., 3 or 4 spaces) MUST be avoided. |
| 1.4    | A blank line MUST precede and follow every list block to separate it from surrounding paragraphs or elements.                             | `Paragraph.\n\n- List item\n\nParagraph.`          | Ensures correct list parsing.                             |
| 1.5    | Tables or code blocks MUST NOT be placed directly inside list items. They MUST be outside the list, separated by blank lines. | N/A                                                   | See [[05-Markdown-Syntax-Conventions#Standard: Markdown for Tables (M-SYNTAX-TABLE-001)|M-SYNTAX-TABLE-001]] and [[05-Markdown-Syntax-Conventions#Standard: Markdown for Code (Inline and Blocks) (M-SYNTAX-CODE-001)|M-SYNTAX-CODE-001]]. |

**Illustrative Examples (Overall):**

```markdown
Paragraph before list.

- Unordered item A
  - Nested unordered B
    1. Ordered sub-item C1
    2. Ordered sub-item C2
- Unordered item D

Paragraph between lists.

1. Ordered item X
   - Unordered sub-item Y
2. Ordered item Z

Paragraph after list.
```

**Cross-References to Other Standard IDs:** [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Tables (M-SYNTAX-TABLE-001)|M-SYNTAX-TABLE-001]], [[COL-SYNTAX-MARKDOWN#Standard: Markdown for Code (Inline and Blocks) (M-SYNTAX-CODE-001)|M-SYNTAX-CODE-001]].

## Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-SYNTAX-LINKS-001`                  |
| Standard Name   | Markdown for Links (Internal and External) |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                                     | Example (if illustrative)                                                                                                        | Notes / Further Specification (if any)                        |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| 1.1    | Internal links (to other documents within the KB) MUST use the wikilink format `[[filename-without-extension]]` or `[[filename-without-extension|Optional Display Text]]` when using Obsidian. For standard Markdown, relative paths `[Link Text](path/to/file.md)` MUST be used. | Obsidian: `[[my-other-document]]` or `[[my-concept|My Concept Page]]`<br>Standard MD: `[My Concept Page](concepts/my-concept.md)` | Platform-specific usage is detailed in [[06-Obsidian-Usage-Conventions#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)|O-USAGE-LINKS-001]]. |
| 1.2    | External links MUST use the standard Markdown inline link format `[Link Text](URL)`.                                                                 | `[Example Website](https://example.com)`                                                                                       |                                                               |
| 1.3    | Reference-style links MUST NOT be used.                                                                               | Incorrect: `[text][id]` then `[id]: url`                                                                                           | Promotes readability by keeping link destination next to text. |
| 1.4    | Autolinks for URLs MUST use angle brackets `<URL>`.                                                                                                  | `<https://example.com>`                                                                                                          | For displaying clickable raw URLs.                           |
| 1.5    | Pipe characters `|` within wikilink display text or filenames MUST NOT be escaped with a backslash.                                                   | Correct: `[[filename|Display Text with | Pipe]]` Incorrect: `[[filename|Display Text with \| Pipe]]` | Escaping is unnecessary and may break links in some parsers. |

**Cross-References to Other Standard IDs:** [[COL-LINKING-UNIVERSAL#Standard: Internal Knowledge Base Linking (U-INTERLINK-001)|U-INTERLINK-001]], [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)|O-USAGE-LINKS-001]].

## Standard: Markdown for Emphasis (Bold, Italic) (M-SYNTAX-EMPHASIS-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-SYNTAX-EMPHASIS-001`               |
| Standard Name   | Markdown for Emphasis (Bold, Italic)  |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule | Example (if illustrative) | Notes / Further Specification (if any) |
| :----- | :---------------- | :------------------------ | :------------------------------------- |
| 1.1    | Italic text MUST be created using single asterisks (`*text*`) or underscores (`_text_`). | `*italic*` or `_italic_` | Use one style consistently within a document. |
| 1.2    | Bold text MUST be created using double asterisks (`**text**`) or double underscores (`__text__`). | `**bold**` or `__bold__` | Use one style consistently within a document. |
| 1.3    | Bold and italic together MUST be created using triple asterisks (`***text***`) or triple underscores (`___text___`). | `***bold italic***` or `___bold italic___` | |

**Cross-References to Other Standard IDs:** None.

## Standard: Markdown for Blockquotes (M-SYNTAX-BLOCKQUOTE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-SYNTAX-BLOCKQUOTE-001`             |
| Standard Name   | Markdown for Blockquotes              |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule | Example (if illustrative) | Notes / Further Specification (if any) |
| :----- | :---------------- | :------------------------ | :------------------------------------- |
| 1.1    | Blockquotes MUST be created using the greater-than symbol (`>`) at the start of a line. | `> This is a blockquote.` | |
| 1.2    | Nested blockquotes MUST use additional `>` symbols, one per level of nesting. | `>> Nested blockquote` | |
| 1.3    | A blank line MUST precede and follow every blockquote. | `Text before.\n\n> Blockquote\n\nText after.` | |

**Cross-References to Other Standard IDs:** None.

## Standard: Markdown for Code (Inline and Blocks) (M-SYNTAX-CODE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-SYNTAX-CODE-001`                   |
| Standard Name   | Markdown for Code (Inline and Blocks) |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                              | Example (if illustrative) | Notes / Further Specification (if any) |
| :----- | :------------------------------------------------------------- | :------------------------ | :------------------------------------- |
| 1.1    | Inline code MUST be enclosed in single backticks `` `code` ``. | `` `                      |                                        |