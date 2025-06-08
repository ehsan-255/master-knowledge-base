---
title: 'Standard: General Markdown Formatting Guidelines'
standard_id: SF-FORMATTING-MARKDOWN-GENERAL
aliases:
  - Markdown Guidelines
  - General Formatting
tags:
  - status/draft
  - criticality/p2-medium
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: General Markdown Formatting Guidelines
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines general formatting guidelines for Markdown documents in
  the knowledge base.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Document formatting
  - Consistency
  - Readability
---
# Standard: Markdown General Formatting Conventions (SF-FORMATTING-MARKDOWN-GENERAL)

## 1. Standard Statement

This standard defines general Markdown formatting conventions for paragraphs, line breaks, horizontal rules, and the use of blank lines. Adherence to these conventions is important for ensuring the readability, consistency, and correct parsing of Markdown documents across the knowledge base. These rules complement the file-level hygiene rules defined in [[SF-FORMATTING-FILE-HYGIENE]].

## 2. Core General Formatting Rules

### Rule 2.1: Paragraphs
Paragraphs are sequences of text separated by one or more blank lines.
*   **Requirement:** A single blank line (i.e., a line containing no characters or only whitespace) MUST be used to separate distinct paragraphs.
*   **Example:**
    ```markdown
    This is the first paragraph. It can span multiple lines of text
    but will be rendered as a single block.

    This is the second paragraph, separated from the first by a single blank line.
    ```
*   **Rationale:** Clearly delineates paragraphs for both raw text readability and correct rendering in HTML or other formats.

### Rule 2.2: Line Breaks (Soft vs. Hard)
Markdown treats most newlines within a paragraph as "soft" line breaks, which are typically rendered as a single space, joining lines together into a continuous paragraph.
*   **Soft Line Breaks (Standard Behavior):**
    ```markdown
    This line is part of the first paragraph.
    This line will join the previous one, separated by a space.
    ```
    *Renders as:* This line is part of the first paragraph. This line will join the previous one, separated by a space.
*   **Hard Line Breaks (Explicit Breaks within a Paragraph):**
    If an explicit hard line break (forcing a line to end and the next text to start on a new line *within the same paragraph block*) is absolutely necessary, the following methods MAY be used, but their use should be minimized in favor of starting new paragraphs for distinct ideas.
    1.  **Two or More Spaces at End of Line (Recommended for Markdown Purity):** End a line with two or more spaces before the newline character.
        ```markdown
        Line one with a hard break.  
        Line two, still in the same paragraph.
        ```
        *Renders as:*
        Line one with a hard break.
        Line two, still in the same paragraph.
    2.  **HTML `<br>` Tag (Use Sparingly):** The HTML break tag `<br>` can be used.
        ```markdown
        Line one with an HTML break.<br>
        Line two, same paragraph.
        ```
        *Renders as:*
        Line one with an HTML break.
        Line two, same paragraph.
*   **Guidance:** Prefer distinct paragraphs for separate thoughts. Use hard line breaks only when semantically appropriate (e.g., lines of an address, poetry) and not for creating artificial spacing between paragraphs (use blank lines for that). The two-space method is generally preferred over `<br>` for maintaining Markdown purity.
*   **Rationale:** Understanding line break behavior is crucial for predictable rendering. Overuse of hard line breaks can make raw Markdown harder to read and edit.

### Rule 2.3: Horizontal Rules
Horizontal rules are used to create a thematic break between sections of content.
*   **Syntax:** MUST be created using three or more hyphens (`---`), asterisks (`***`), or underscores (`___`) on a line by themselves.
*   **Consistency:** For consistency across the knowledge base, **three or more hyphens (`---`) ARE THE PREFERRED STYLE.**
*   **Spacing:**
    *   The characters forming the rule MAY be separated by spaces.
    *   A blank line MUST precede and follow a horizontal rule, as per [[SF-FORMATTING-FILE-HYGIENE]].
*   **Example (Preferred):**
    ```markdown
    Some content above.

    ---

    Some content below.
    ```
*   **Example (Alternative, also valid but less preferred):**
    ```markdown
    Some content above.

    * * *

    Some content below.
    ```
*   **Rationale:** Provides a clear visual separation between content sections. Standardizing on one style (`---`) improves consistency.

### Rule 2.4: Use of Multiple Blank Lines
The use of more than one consecutive blank line to separate content elements (e.g., between paragraphs, before/after headings, lists, code blocks) SHOULD generally be avoided.
*   **Standard Separation:** A single blank line is typically sufficient to separate block-level elements in Markdown.
*   **Exception:** Using more than one blank line (e.g., two blank lines) before or after complex elements like code blocks or tables MAY be acceptable if it significantly improves the readability of the *raw Markdown source*, but this should not be a common practice. Excessive blank lines do not usually affect the rendered HTML output but can make the raw source less compact.
*   **Rationale:** Maintains consistency in raw Markdown formatting and avoids excessive vertical spacing that can make documents harder to scroll through and read in their source form.

## 3. Importance of General Formatting Conventions

*   **Readability:** Consistent formatting makes raw Markdown documents easier to read, edit, and review.
*   **Predictable Rendering:** Ensures that Markdown is parsed and rendered as intended across different platforms and tools.
*   **Authoring Efficiency:** Clear rules reduce ambiguity for authors.
*   **Maintainability:** Well-formatted documents are easier to maintain over time.

## 4. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository.

## 5. Cross-References
- [[SF-FORMATTING-FILE-HYGIENE]] - For file-level hygiene rules including blank lines around block elements and EOF characters.

---
*This standard (SF-FORMATTING-MARKDOWN-GENERAL) is based on common Markdown conventions for paragraphs, line breaks, horizontal rules, and blank line usage.*
