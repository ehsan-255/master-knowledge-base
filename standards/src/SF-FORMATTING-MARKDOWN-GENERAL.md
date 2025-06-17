---
title: 'Standard: General Markdown Formatting Guidelines'
standard_id: SF-FORMATTING-MARKDOWN-GENERAL
aliases:
- Markdown Guidelines
- General Formatting
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p2-medium
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: General Markdown Formatting Guidelines
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:15Z'
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
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown General Formatting Conventions (SF-FORMATTING-MARKDOWN-GENERAL)

## 1. Standard Statement

This standard **MANDATES** general Markdown formatting conventions for paragraphs, line breaks, horizontal rules, and blank lines. Adherence to these conventions is **CRITICAL** for ensuring readability, consistency, and correct parsing of Markdown documents. These rules complement file-level hygiene rules in [[SF-FORMATTING-FILE-HYGIENE]].

## 2. Core General Formatting Rules

### Rule 2.1: Paragraphs
Paragraphs are sequences of text separated by one or more blank lines.
*   **Mandatory:** A single blank line (**MUST**) separate distinct paragraphs.
*   **Example:**
    ```markdown
    This is the first paragraph. It can span multiple lines of text
    but will be rendered as a single block.

    This is the second paragraph, separated from the first by a single blank line.
    ```
*   **Rationale:** Clearly delineates paragraphs for both raw text readability and correct rendering.

### Rule 2.2: Line Breaks (Soft vs. Hard)
Markdown treats most newlines within a paragraph as "soft" line breaks, rendering as a single space.
*   **Soft Line Breaks (Standard Behavior):**
    ```markdown
    This line is part of the first paragraph.
    This line will join the previous one, separated by a space.
    ```
*   **Hard Line Breaks (Explicit Breaks within a Paragraph):**
    If an explicit hard line break is absolutely necessary within a paragraph, it **MUST** be created by ending a line with two or more spaces before the newline character. The use of HTML `<br>` tags is **PROHIBITED**.
    ```markdown
    Line one with a hard break.  
    Line two, still in the same paragraph.
    ```
*   **Rationale:** Ensures predictable rendering and maintains Markdown purity.

### Rule 2.3: Horizontal Rules
Horizontal rules **MUST** be created using three or more hyphens (`---`) on a line by themselves. The use of asterisks (`***`) or underscores (`___`) is **PROHIBITED**.
*   **Spacing:** The characters forming the rule **MAY** be separated by spaces.
*   **Blank Lines:** A blank line **MUST** precede and follow a horizontal rule, as per [[SF-FORMATTING-FILE-HYGIENE]].
*   **Example:**
    ```markdown
    Some content above.

    ---

    Some content below.
    ```
*   **Rationale:** Provides clear visual separation and standardizes consistency.

### Rule 2.4: Use of Multiple Blank Lines
The use of more than one consecutive blank line to separate content elements (e.g., between paragraphs, before/after headings, lists, code blocks) is **PROHIBITED**.
*   **Rationale:** Maintains consistency in raw Markdown formatting and avoids excessive vertical spacing.

## 3. Importance of Strict General Formatting Conventions

*   **Readability:** Consistent formatting makes raw Markdown documents easier to read, edit, and review.
*   **Predictable Rendering:** Ensures Markdown is parsed and rendered as intended across different platforms and tools.
*   **Authoring Efficiency:** Clear rules reduce ambiguity for authors.
*   **Maintainability:** Well-formatted documents are easier to maintain over time.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 5. Cross-References
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-FORMATTING-MARKDOWN-GENERAL) has been revised to mandate strict general Markdown formatting conventions, including explicit rules for paragraphs, line breaks, horizontal rules, and blank line usage, ensuring consistency and predictable rendering.*
