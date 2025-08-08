---
title: 'Standard: Blockquote Syntax'
standard_id: SF-SYNTAX-BLOCKQUOTES
aliases:
- Blockquotes
- Quote Blocks
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
primary-topic: Blockquote Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax and usage rules for blockquotes in knowledge
  base documents.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content presentation
- Citation formatting
- Text emphasis
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Blockquotes (SF-SYNTAX-BLOCKQUOTES)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for creating blockquotes within all Knowledge Base documents. Strict and consistent use of blockquote syntax is **CRITICAL** for visually distinguishing quoted text, ensuring correct rendering, maintaining readability, and accurately conveying semantic meaning. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around block elements is also **MANDATORY**.

## 2. Core Blockquote Syntax Rules

### Rule 2.1: Blockquote Marker
All lines of text intended to be part of a blockquote **MUST** be prefixed with a greater-than symbol (`>`) followed by a single space.
*   **Mandatory Syntax:** `> Quoted text`
*   **Multi-line Blockquotes:** For blockquotes spanning multiple lines, including blank lines used to separate paragraphs within the quote, each and every line **MUST** be prefixed with `> `.
    *   **Example:**
        ```markdown
        > This is the first paragraph of a blockquote.
        >
        > This is the second paragraph within the same blockquote.
        ```
*   **Prohibited Syntax:** Omitting the `> ` prefix on any line within a blockquote, or using tabs for indentation, **MUST NOT** be done.
*   **Rationale:** The `> ` prefix is the singular, universally recognized Markdown indicator for blockquotes, essential for consistent parsing and rendering.

### Rule 2.2: Nested Blockquotes
Nested blockquotes (a blockquote contained within another blockquote) **MUST** be created by adding an additional greater-than symbol (`>`) for each level of nesting, each followed by a single space.
*   **Mandatory Syntax:** `>> Nested quoted text`
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
*   **Rationale:** Provides a clear, unambiguous, and standard method for representing multiple levels of quotation or attribution.

### Rule 2.3: Blank Lines Around Blockquotes
A single blank line **MUST** precede and a single blank line **MUST** follow every blockquote element to ensure clear separation from surrounding paragraphs or other block elements.
*   **Example:**
    ```markdown
    This is a paragraph before the blockquote.

    > This is the blockquote content.
    > It might have multiple lines.

    This is a paragraph after the blockquote.
    ```
*   **Rationale:** Ensures correct parsing and rendering of the blockquote as a distinct block element, preventing unintended merging with adjacent content and maintaining visual integrity.

## 3. Importance of Strict Blockquote Syntax

*   **Guaranteed Readability & Visual Distinction:** Clearly separates quoted material from original content, significantly improving comprehension and user experience.
*   **Accurate Semantic Meaning:** Unambiguously indicates that the enclosed text is a quotation, crucial for content integrity and automated analysis.
*   **Reliable Automated Processing:** Ensures that tools for linting, validation, and content transformation can accurately identify and process blockquoted material.
*   **Enhanced Authoring Consistency:** Provides a single, clear method for authors to correctly quote text, reducing errors and fostering uniformity across the Knowledge Base.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where text is quoted from external sources or other documents. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and any tooling interacting with KB Markdown files.

## 5. Cross-References
- [[CS-POLICY-TONE-LANGUAGE]] - For definitions of mandating keywords (MUST, SHOULD, MAY) and general language policy.
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines and file formatting that apply to block elements.

---
*This standard (SF-SYNTAX-BLOCKQUOTES) has been revised to provide strict, singular mandates for blockquote syntax, clarifying its application and incorporating absolute prohibitions. It replaces and supersedes any prior interpretations or practices where conflicts existed, establishing a single source of truth for quoted content representation within the Knowledge Base.*
