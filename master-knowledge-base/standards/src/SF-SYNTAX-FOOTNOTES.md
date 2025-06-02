---
title: 'Standard: Footnote Syntax'
standard_id: SF-SYNTAX-FOOTNOTES
aliases:
  - Footnotes
  - Reference Notes
tags:
  - status/draft
  - criticality/p3-low
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Footnote Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating footnotes in knowledge base documents.
criticality: P3-Low
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Reference formatting
  - Content annotation
  - Document structure
change_log_url: ./changelog.md
---
# Standard: Markdown Syntax for Footnotes (SF-SYNTAX-FOOTNOTES)

## 1. Standard Statement

This standard defines the recommended syntax for creating footnotes within Markdown documents. Footnotes are used to provide supplementary information, explanations, or citations without disrupting the main flow of the text. While not part of the core CommonMark specification, footnote syntax is a common extension supported by many Markdown processors.

Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around block elements (like the footnote definition block) is also important.

## 2. Core Footnote Syntax (Common Extension)

The most common syntax for footnotes, often associated with PHP Markdown Extra, Pandoc, and other extended Markdown flavors, involves two parts: an inline marker and a definition block.

### Rule 2.1: Footnote Marker in Text
A footnote marker is placed in the text where the reference to the footnote occurs.
*   **Syntax:** `[^identifier]`
*   **`identifier`**: This is a label used to link the marker to its corresponding definition.
    *   It can be numeric (e.g., `[^1]`, `[^2]`).
    *   It can be a descriptive textual label (e.g., `[^note1]`, `[^important-clarification]`). Textual labels MUST NOT contain spaces or special Markdown characters that would break the marker. Simple alphanumeric strings with hyphens or underscores are generally safe.
*   **Placement:** The marker is placed directly after the text it refers to, without a preceding space.
*   **Example:**
    ```markdown
    This is some text that requires a footnote.[^1]
    Another piece of information needs a different kind of note.[^note-alpha]
    ```

### Rule 2.2: Footnote Definition
The definition provides the content of the footnote.
*   **Syntax:** `[^identifier]: Footnote text.`
*   **`identifier`**: This MUST exactly match the identifier used in the corresponding inline marker.
*   **`Footnote text.`**: The content of the footnote. This can include multiple lines, paragraphs, and even some block elements (like lists or blockquotes), provided they are indented correctly under the footnote definition.
*   **Placement:** Footnote definitions are typically placed at the end of the document, or at the end of the section they pertain to. They MUST be separated from the main text and from each other by blank lines.
*   **Indentation for Multi-line/Block Content:** If a footnote definition contains multiple paragraphs or other block elements, subsequent lines/blocks MUST be indented (typically by four spaces) to align under the start of the footnote text.
    ```markdown
    [^identifier]: This is the first paragraph of the footnote.
        This is still part of the same footnote, indented.

        A new paragraph within the footnote, also indented.
        - A list item within the footnote
    ```

### Rule 2.3: Uniqueness of Identifiers
Footnote identifiers (the text within `[^...]`) MUST be unique within a single document.
*   **Rationale:** Duplicate identifiers will lead to ambiguous references and incorrect rendering by most parsers.

## 3. Illustrative Examples

### Example 3.1: Numeric Identifiers
```markdown
This is the first statement that needs a footnote.[^1] Later, another point is made.[^2]

[^1]: This is the first footnote's content.
[^2]: This is the second footnote's content, which can be longer and even span multiple lines if needed, as long as subsequent lines are indented.
    This second line is part of footnote 2.
```
**Conceptual Rendered Output:**
This is the first statement that needs a footnote.<sup>1</sup> Later, another point is made.<sup>2</sup>

---
1.  This is the first footnote's content.
2.  This is the second footnote's content, which can be longer and even span multiple lines if needed, as long as subsequent lines are indented.
    This second line is part of footnote 2.

### Example 3.2: Labeled Identifiers
```markdown
Here's a concept that requires some clarification.[^clarify] We also need to cite a source for this claim.[^citation-smith2023]

[^clarify]: This footnote provides additional details and context for the preceding statement.
[^citation-smith2023]: Smith, J. (2023). *Advanced Topics in Markdown*. Publisher.
```
**Conceptual Rendered Output:**
Here's a concept that requires some clarification.<sup>3</sup> We also need to cite a source for this claim.<sup>4</sup>

---
3.  This footnote provides additional details and context for the preceding statement.
4.  Smith, J. (2023). *Advanced Topics in Markdown*. Publisher.

*(Note: Rendered footnote numbers (e.g., 3, 4) are usually sequential regardless of identifier text.)*

## 4. Parser Compatibility and Placement of Definitions

*   **Not Core CommonMark:** Footnote syntax as described is an extension to Markdown.
*   **Supported Environments:** This syntax is supported by many popular Markdown processors, including Pandoc, many static site generators, and some note-taking applications.
*   **Placement of Definitions:** While many parsers allow footnote definitions to be placed almost anywhere in the document (as long as they are separated by blank lines), the convention and **BEST PRACTICE** is to place all footnote definitions together at the end of the document (or, for very long documents, sometimes at the end of a major section). This improves readability of the raw Markdown.
*   **Rendering Order:** Regardless of where definitions are placed in the source, most parsers will render the footnotes in the order their markers appear in the text and typically list the footnote content at the bottom of the rendered document.

## 5. Importance of Consistent Footnote Syntax

*   **Clarity:** Provides a standard way to offer supplementary information without disrupting the main text flow.
*   **Readability:** When rendered, footnotes are usually clearly linked and presented in a dedicated section, aiding readability.
*   **Authoring Consistency:** Ensures all authors use the same method for creating footnotes when the feature is employed.
*   **Academic/Referential Integrity:** Useful for citations or elaborations in more formal or academic documents.

## 6. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where footnotes are used for supplementary information, explanations, or citations.

## 7. Cross-References
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines around block elements like footnote definition blocks.

---
*This standard (SF-SYNTAX-FOOTNOTES) is based on common Markdown extension syntax for footnotes.*
