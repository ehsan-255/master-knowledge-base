---
title: "Standard: Markdown Syntax for Lists"
standard_id: "SF-SYNTAX-LISTS"
aliases: ["List Syntax", "Ordered Lists", "Unordered Lists", "Nested Lists"]
tags:
  - status/draft
  - criticality/P1-High # Correct list syntax is fundamental for readability
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Markdown List Syntax" # As per prompt
related-standards: ["SF-SYNTAX-TABLES_ID_PLACEHOLDER", "SF-SYNTAX-CODE-BLOCKS_ID_PLACEHOLDER", "SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER"]
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "SYNTAX" # As per prompt
scope_application: "Defines the mandatory Markdown syntax for creating ordered (numbered) and unordered (bulleted) lists, including rules for nesting and interaction with other block elements."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Document structure", "Readability", "Accessibility", "Automated parsing", "Authoring consistency"]
change_log_url: "./SF-SYNTAX-LISTS-changelog.md" # Placeholder
---

# Standard: Markdown Syntax for Lists (SF-SYNTAX-LISTS)

## 1. Standard Statement

This standard defines the mandatory Markdown syntax for creating ordered (numbered) and unordered (bulleted) lists. Consistent and correct list syntax is essential for document structure, readability, accessibility, and reliable parsing by Markdown processors. Adherence to [[SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER]] regarding blank lines around list blocks is also critical.

## 2. Core List Syntax Rules

### Rule 2.1: Unordered List Marker (Derived from M-SYNTAX-LISTS-001, Rule 1.1)
Unordered lists MUST use a hyphen (`-`) followed by a single space as the item marker.
*   **Example (Correct):**
    ```markdown
    - Item A
    - Item B
    ```
*   **Prohibition:** Other common markers like asterisk (`*`) or plus (`+`) MUST NOT be used for unordered lists to ensure uniformity.
*   **Rationale:** Consistency in markers improves visual uniformity in raw Markdown and predictability for parsers.

### Rule 2.2: Ordered List Marker (Derived from M-SYNTAX-LISTS-001, Rule 1.2)
Ordered lists MUST use a number followed by a period (`.`) and a single space as the item marker.
*   **Starting Number:** For each distinct ordered list, the numbering MUST start from `1.`.
*   **Example (Correct):**
    ```markdown
    1. First item
    2. Second item
    3. Third item
    ```
*   **Note on Sequential Numbering:** While Markdown renderers typically handle sequential numbering even if all source numbers are `1.`, it is recommended to use sequential numbers in the source for clarity where feasible. However, the primary rule is the `1. ` format for the first item and consistent `number. ` format for subsequent items.
*   **Rationale:** Ensures clarity and proper rendering of ordered sequences.

### Rule 2.3: Nested List Indentation (Derived from M-SYNTAX-LISTS-001, Rule 1.3)
Nested list items MUST be indented by exactly **two (2) spaces** relative to the start of the parent item's marker text (i.e., two spaces before the `-` or `1. ` marker of the child item).
*   **Example (Correct):**
    ```markdown
    - Parent item
      - Child item 1 (indented 2 spaces)
        - Grandchild item A (indented 4 spaces total)
      - Child item 2
    1. Ordered parent
      - Unordered child (indented 2 spaces)
      - Unordered child
        1. Ordered grandchild (indented 4 spaces total)
    ```
*   **Prohibition:** Inconsistent indentation (e.g., 3 or 4 spaces for the first level of nesting) MUST be avoided. Tab characters MUST NOT be used for indentation.
*   **Rationale:** Precise two-space indentation is crucial for reliable parsing of nested structures across different Markdown processors and improves readability of complex lists in raw text.

### Rule 2.4: Blank Lines Around List Blocks (Derived from M-SYNTAX-LISTS-001, Rule 1.4)
A single blank line MUST precede and a single blank line MUST follow every list block to separate it from surrounding paragraphs or other block elements.
*   **Example:**
    ```markdown
    This is a paragraph before the list.

    - List item one
    - List item two

    This is a paragraph after the list.
    ```
*   **Rationale:** Ensures correct list parsing and rendering, preventing adjacent paragraphs from being unintentionally absorbed into list items or lists from merging.

### Rule 2.5: Prohibited Content Directly Inside List Items (Derived from M-SYNTAX-LISTS-001, Rule 1.5)
Complex block elements such as tables (see [[SF-SYNTAX-TABLES_ID_PLACEHOLDER]]) or fenced code blocks (see [[SF-SYNTAX-CODE-BLOCKS_ID_PLACEHOLDER]]) MUST NOT be placed directly inside list items without proper separation or advanced list continuation syntax.
*   **Guidance:**
    *   For simple cases, such elements should be placed outside the list, separated by blank lines.
    *   If a table or code block logically belongs *within* a list item's content, it typically requires an additional level of indentation (usually 4 spaces or 1 tab, depending on the parser, beyond the list item's own indentation) and often a blank line between the list item's text and the complex block. However, for maximum compatibility and simplicity, placing them outside the list is preferred. This standard primarily discourages direct, unindented embedding that breaks list flow.
*   **Rationale:** Direct nesting of complex blocks within list items can be fragile across different Markdown parsers and often leads to rendering issues or broken list structures.

## 3. Illustrative Example (Comprehensive) (Derived from M-SYNTAX-LISTS-001 Example)

```markdown
Paragraph before list.

- Unordered item A
  - Nested unordered B (indented 2 spaces)
    1. Ordered sub-item C1 (indented 4 spaces)
    2. Ordered sub-item C2
- Unordered item D

Paragraph between lists.

1. Ordered item X
   - Unordered sub-item Y (indented 3 spaces from start of line, 2 from parent '1.')
2. Ordered item Z

Paragraph after list.
```

## 4. Importance of Correct List Syntax

*   **Readability:** Well-formed lists are easier to read and understand in both raw Markdown and rendered views.
*   **Accessibility:** Screen readers and assistive technologies rely on correct list markup to announce list structure and items properly.
*   **Automated Processing:** Tools that parse Markdown for content extraction, conversion, or linting depend on valid list syntax.
*   **Consistency:** Uniform list formatting contributes to the overall visual and structural consistency of the knowledge base.

## 5. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where ordered or unordered lists are used.

## 6. Cross-References
- [[SF-SYNTAX-TABLES_ID_PLACEHOLDER]] - For syntax rules related to tables.
- [[SF-SYNTAX-CODE-BLOCKS_ID_PLACEHOLDER]] - For syntax rules related to code blocks.
- [[SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER]] - For rules on blank lines and file formatting.

---
*This standard (SF-SYNTAX-LISTS) is based on rules 1.1 through 1.5 and the illustrative example previously defined in M-SYNTAX-LISTS-001 from COL-SYNTAX-MARKDOWN.md.*
```
