---
title: "Standard: Markdown Syntax for Blockquotes"
standard_id: "SF-SYNTAX-BLOCKQUOTES"
aliases: ["Blockquote Syntax", "Markdown Quoting"]
tags:
  - status/draft
  - criticality/P2-Medium # Basic but important for clear quoting
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Markdown Blockquote Syntax" # As per prompt
related-standards: ["SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER"] # For blank line rules
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "SYNTAX" # As per prompt
scope_application: "Defines the mandatory Markdown syntax for creating blockquotes in all knowledge base documents."
criticality: "P2-Medium"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Readability", "Authoring consistency", "Correct rendering of quoted text", "Accessibility"]
change_log_url: "./SF-SYNTAX-BLOCKQUOTES-changelog.md" # Placeholder
---

# Standard: Markdown Syntax for Blockquotes (SF-SYNTAX-BLOCKQUOTES)

## 1. Standard Statement

This standard defines the mandatory Markdown syntax for creating blockquotes within all knowledge base documents. Consistent use of blockquote syntax is important for visually distinguishing quoted text, ensuring correct rendering, and maintaining readability. Adherence to [[SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER]] regarding blank lines around block elements is also critical.

## 2. Core Blockquote Syntax Rules

### Rule 2.1: Blockquote Marker (Derived from M-SYNTAX-BLOCKQUOTE-001, Rule 1.1)
Blockquotes MUST be created by prefixing each line of the quoted text with a greater-than symbol (`>`) followed by a single space.
*   **Syntax:** `> Quoted text`
*   **Example:**
    ```markdown
    > This is a single-line blockquote.
    ```
*   **Multi-line Blockquotes:** For blockquotes spanning multiple lines, each line of the quoted text MUST be prefixed with `> `. Blank lines within a multi-line blockquote (to separate paragraphs within the quote) MUST also be prefixed with `> `.
    ```markdown
    > This is the first paragraph of a blockquote.
    >
    > This is the second paragraph within the same blockquote.
    ```
*   **Rationale:** The `> ` prefix is the standard Markdown indicator for blockquotes, universally recognized by parsers.

### Rule 2.2: Nested Blockquotes (Derived from M-SYNTAX-BLOCKQUOTE-001, Rule 1.2)
Nested blockquotes (a blockquote within another blockquote) MUST be created by using additional greater-than symbols (`>`) for each level of nesting.
*   **Syntax:** `>> Nested quoted text`
*   **Example:**
    ```markdown
    > This is the first level of quoting.
    >
    > > This is a nested blockquote (second level).
    > > It can also span multiple lines.
    >
    > Back to the first level of quoting.
    >
    > > > This is a third level of nesting!
    ```
*   **Rationale:** Provides a clear and standard way to represent multiple levels of quotation or attribution.

### Rule 2.3: Blank Lines Around Blockquotes (Derived from M-SYNTAX-BLOCKQUOTE-001, Rule 1.3)
A single blank line MUST precede and a single blank line MUST follow every blockquote element.
*   **Example:**
    ```markdown
    This is a paragraph before the blockquote.

    > This is the blockquote content.
    > It might have multiple lines.

    This is a paragraph after the blockquote.
    ```
*   **Rationale:** Ensures correct parsing and rendering of the blockquote as a distinct block element, separating it visually and structurally from surrounding content. This aligns with general file hygiene rules for block elements (see [[SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER]]).

## 3. Importance of Correct Blockquote Syntax

*   **Readability:** Clearly distinguishes quoted material from the author's own text, improving comprehension.
*   **Visual Distinction:** Most renderers style blockquotes uniquely (e.g., with an indent and/or a vertical line), aiding visual organization.
*   **Semantic Meaning:** Indicates that the enclosed text is a quotation from another source.
*   **Authoring Consistency:** Ensures all authors use the same method for quoting text.

## 4. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where text is quoted from external sources or other documents.

## 5. Cross-References
- [[SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER]] - For rules on blank lines and file formatting that apply to block elements.

---
*This standard (SF-SYNTAX-BLOCKQUOTES) is based on rules 1.1 through 1.3 previously defined in M-SYNTAX-BLOCKQUOTE-001 from COL-SYNTAX-MARKDOWN.md.*
```
