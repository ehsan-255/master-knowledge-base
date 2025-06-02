---
title: 'Standard: Heading Syntax'
standard_id: SF-SYNTAX-HEADINGS
aliases:
  - Headings
  - Header Syntax
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Heading Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating headings in knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Document structure
  - Navigation
  - Content hierarchy
change_log_url: ./changelog.md
---
# Standard: Markdown Syntax for Headings (SF-SYNTAX-HEADINGS)

## 1. Standard Statement

This standard defines the mandatory Markdown syntax for creating headings (H1 through H6) in all knowledge base documents. Consistent and correct heading syntax is fundamental for document structure, readability, accessibility, and reliable automated processing (such as Table of Contents generation).

While this document specifies the *syntax*, the *semantic application* of these headings (e.g., using a single H1 for the document title, not skipping levels, how H2s structure a chapter) is governed by content structure standards like [[AS-STRUCTURE-DOC-CHAPTER]] and policies like [[CS-POLICY-DOC-CHAPTER-CONTENT]]. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around headings is also critical.

## 2. Core Heading Syntax Rules

### Rule 2.1: ATX Style Headings (Derived from M-SYNTAX-HEADINGS-001, Rule 1.1)
Headings MUST be created using the ATX style, which employs hash symbols (`#`) at the beginning of the line. The number of hash symbols corresponds to the heading level (one `#` for H1, two `##` for H2, and so on, up to six `######` for H6).
*   **Example:**
    ```markdown
    # This is an H1 Heading
    ## This is an H2 Heading
    ### This is an H3 Heading
    #### This is an H4 Heading
    ##### This is an H5 Heading
    ###### This is an H6 Heading
    ```
*   **Prohibition:** Setext style headings (using `=` for H1 and `-` for H2 on the line below the text) MUST NOT be used.
*   **Rationale:** ATX style is more widely supported, visually clearer in raw Markdown, and less prone to ambiguity than Setext style.

### Rule 2.2: Space After Hash Symbols (Derived from M-SYNTAX-HEADINGS-001, Rule 1.2)
There MUST be a single space character between the hash symbol(s) and the heading text.
*   **Example (Correct):** `# My Heading`
*   **Example (Incorrect):** `#My Heading` (missing space), ` # My Heading` (leading space before `#`)
*   **Rationale:** Ensures correct parsing by Markdown processors and improves readability of the raw text.

### Rule 2.3: Blank Lines Around Headings (Derived from M-SYNTAX-HEADINGS-001, Rule 1.5)
A single blank line MUST precede and a single blank line MUST follow every heading.
*   **Example:**
    ```markdown
    Some paragraph text.

    ## My Heading

    More paragraph text.
    ```
*   **Exceptions:**
    *   A heading at the very beginning of a document (typically the H1 title) does not require a blank line before it (as it's preceded by the YAML frontmatter).
    *   A heading at the very end of a document does not require a blank line after it (though the file should still end with a single newline character as per [[SF-FORMATTING-FILE-HYGIENE]]).
*   **Rationale:** Improves readability of the raw Markdown source and prevents potential parsing issues with some Markdown processors, ensuring headings are correctly rendered as distinct blocks.

## 3. Semantic Application of Headings (Context from M-SYNTAX-HEADINGS-001, Rules 1.3 & 1.4)

While this document focuses on syntax, the following semantic rules are critical for proper document structure and are primarily governed by other standards:

### Rule 3.1: Single H1 Heading for Document Title
Each document MUST begin with a single H1 heading, which serves as the document's main title. No other H1 headings should appear in the document.
*   **Syntax Example:** `# Document Title Here`
*   **Governance:** This rule's application and how it forms the basis of chapter structure is detailed in [[AS-STRUCTURE-DOC-CHAPTER]].

### Rule 3.2: No Skipping Heading Levels
Heading levels MUST be used hierarchically without skipping levels. For example, an H2 heading can be followed by an H3, but not directly by an H4.
*   **Correct Sequence Example:** H1 -> H2 -> H3 -> H2 -> H3
*   **Incorrect Sequence Example:** H1 -> H3 (skips H2)
*   **Governance:** The policy ensuring correct hierarchical heading usage for content organization is detailed in [[CS-POLICY-DOC-CHAPTER-CONTENT]].

## 4. Importance of Correct Heading Syntax

*   **Readability:** Clear headings make documents easier to read and scan, both in raw Markdown and rendered views.
*   **Accessibility:** Screen readers and other assistive technologies rely on correct heading syntax and hierarchy to provide navigation and structure to users with disabilities.
*   **Automated Processing:** Tools that generate Tables of Contents, parse document structure for indexing, or convert Markdown to other formats depend on valid heading syntax.
*   **Maintainability:** Consistent heading usage simplifies document maintenance and refactoring.

## 5. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository.

## 6. Cross-References
- [[AS-STRUCTURE-DOC-CHAPTER]] - Defines the overall internal structure for Chapter documents, including the use of the H1 as the title.
- [[CS-POLICY-DOC-CHAPTER-CONTENT]] - Governs the semantic use of headings (H2-H6) for content organization within Chapters.
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines and EOF characters that interact with heading formatting.

---
*This standard (SF-SYNTAX-HEADINGS) is based on rules 1.1, 1.2, and 1.5 previously defined in M-SYNTAX-HEADINGS-001 from COL-SYNTAX-MARKDOWN.md. Rules 1.3 and 1.4 regarding semantic application are noted and deferred to content structure standards.*
