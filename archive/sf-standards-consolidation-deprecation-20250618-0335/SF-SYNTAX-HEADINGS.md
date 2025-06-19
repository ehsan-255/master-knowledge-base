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
date-modified: '2025-06-18T02:05:00Z'
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

This standard **MANDATES** the exclusive Markdown syntax for creating headings (H1 through H6) in all Knowledge Base documents.

## 2. Core Heading Syntax Rules

### Rule 2.1: ATX Style Headings
Headings **MUST** be created exclusively using ATX style with hash symbols (`#`). The number of hash symbols **MUST** correspond to the heading level.
*   **Mandatory Syntax:**
    ```markdown
    # This is an H1 Heading
    ## This is an H2 Heading
    ### This is an H3 Heading
    #### This is an H4 Heading
    ##### This is an H5 Heading
    ###### This is an H6 Heading
    ```
*   **Prohibited:** Setext style headings (using `=` or `-` below text)

### Rule 2.2: Single Space After Hash Symbols
There **MUST** be a single space character immediately following the hash symbol(s) and preceding the heading text.
*   **Correct:** `# My Heading`
*   **Prohibited:** `#My Heading` (missing space), ` # My Heading` (leading space before `#`)

### Rule 2.3: Blank Lines Around Headings
A single blank line **MUST** precede and follow every heading.
*   **Example:**
    ```markdown
    Some paragraph text.

    ## My Heading

    More paragraph text.
    ```
*   **Exceptions:**
    *   H1 heading at document beginning (after YAML frontmatter) **MUST NOT** have a blank line before it
    *   Heading at document end **MUST NOT** have a blank line after it

### Rule 2.4: Single H1 Heading for Document Title
Each document **MUST** contain **exactly one** H1 heading as the first content element after YAML frontmatter, serving as the document's main title.

### Rule 2.5: Strict Hierarchical Heading Progression
Heading levels **MUST** be used in strict hierarchical order without skipping levels.
*   **Correct:** H1 → H2 → H3 → H3 → H2 → H3 → H4
*   **Prohibited:** H1 → H3 (skips H2), H2 → H4 (skips H3)

## 3. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository. Adherence is **MANDATORY** for all content creators, automated systems, and tooling.

## 4. Cross-References
*   [[CS-POLICY-TONE-LANGUAGE]]
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-HEADINGS) establishes strict, singular mandates for heading syntax and hierarchical usage, ensuring universal consistency for the Knowledge Base.*
