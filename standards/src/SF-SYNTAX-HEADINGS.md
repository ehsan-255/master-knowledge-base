---
title: 'Standard: Heading Syntax'
standard_id: SF-SYNTAX-HEADINGS
aliases:
- Headings
- Header Syntax
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Heading Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating headings in knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Document structure
- Navigation
- Content hierarchy
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Headings (SF-SYNTAX-HEADINGS)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for creating headings (H1 through H6) in all Knowledge Base documents. Consistent and absolutely correct heading syntax is **CRITICAL** for robust document structure, predictable rendering, guaranteed accessibility, and reliable automated processing (e.g., Table of Contents generation, semantic analysis). This document is the **single authoritative source** for how headings **MUST** be formed and applied hierarchically.

## 2. Core Heading Syntax Rules

### Rule 2.1: ATX Style Headings
Headings **MUST** be created exclusively using the ATX style, employing hash symbols (`#`) at the line's beginning. The number of hash symbols **MUST** directly correspond to the heading level (one `#` for H1, two `##` for H2, up to six `######` for H6).
*   **Mandatory Syntax:**
    ```markdown
    # This is an H1 Heading
    ## This is an H2 Heading
    ### This is an H3 Heading
    #### This is an H4 Heading
    ##### This is an H5 Heading
    ###### This is an H6 Heading
    ```
*   **Prohibited Syntax:** Setext style headings (using `=` for H1 and `-` for H2 below text) **MUST NOT** be used.
*   **Rationale:** ATX style is universally supported, visually unambiguous, and essential for machine readability and automated parsing.

### Rule 2.2: Single Space After Hash Symbols
There **MUST** be a single space character immediately following the hash symbol(s) and preceding the heading text.
*   **Correct Example:** `# My Heading`
*   **Prohibited Examples:** `#My Heading` (missing space), ` # My Heading` (leading space before `#`)
*   **Rationale:** Ensures correct parsing by all Markdown processors and maintains high raw source readability.

### Rule 2.3: Blank Lines Around Headings
A single blank line **MUST** precede and a single blank line **MUST** follow every heading.
*   **Example:**
    ```markdown
    Some paragraph text.

    ## My Heading

    More paragraph text.
    ```
*   **Exceptions:**
    *   An H1 heading at the document's beginning (immediately after YAML frontmatter) **MUST NOT** have a blank line before it.
    *   A heading at the document's very end **MUST NOT** have a blank line after it, though the file **MUST** still end with a single newline character as per [[SF-FORMATTING-FILE-HYGIENE]].
*   **Rationale:** Strictly defined blank lines prevent parsing ambiguities and ensure headings are correctly rendered as distinct blocks.

### Rule 2.4: Single H1 Heading for Document Title
Each Markdown document **MUST** contain **exactly one** H1 heading, and this H1 heading **MUST** be the very first content element (after the YAML frontmatter), serving exclusively as the document's main title. No other H1 headings **MUST** appear anywhere else.
*   **Rationale:** Ensures a clear, singular title for every document, critical for navigation, indexing, and overall document identity.

### Rule 2.5: Strict Hierarchical Heading Progression
Heading levels **MUST** be used in strict hierarchical order without skipping levels. For example, an H2 heading **MUST** be followed directly by an H3 if subdivision is needed; it **MUST NOT** be followed directly by an H4 or a lower level.
*   **Correct Sequence Example:** H1 -> H2 -> H3 -> H3 -> H2 -> H3 -> H4
*   **Prohibited Sequence Example:** H1 -> H3 (skips H2), H2 -> H4 (skips H3)
*   **Rationale:** Essential for accessibility (screen reader navigation), automated Table of Contents generation, and maintaining a logical, scannable document structure.

## 3. Importance of Strict Heading Syntax and Hierarchy

*   **Universal Readability and Scannability:** Consistent syntax and logical hierarchy make documents easy to read and understand.
*   **Guaranteed Accessibility:** Correct heading structure is fundamental for users relying on screen readers and assistive technologies.
*   **Reliable Automated Processing:** Tools for Table of Contents generation, content indexing, search, and semantic analysis depend entirely on strict heading syntax and hierarchy.
*   **Enhanced Maintainability:** Uniform approach simplifies document creation, editing, and long-term maintenance.
*   **Unified KB Structure:** Establishes a professional and consistent architectural foundation for all documentation.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 5. Cross-References
*   [[CS-POLICY-TONE-LANGUAGE]]
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-HEADINGS) has been revised to provide strict, singular mandates for heading syntax and hierarchical usage, consolidating previously distributed semantic rules. It replaces and supersedes any prior interpretations from M-SYNTAX-HEADINGS-001 or content structure policies where conflicts existed, ensuring a single source of truth for heading application.*
