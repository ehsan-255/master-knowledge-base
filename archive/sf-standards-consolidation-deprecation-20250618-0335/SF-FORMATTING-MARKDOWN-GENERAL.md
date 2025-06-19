---
title: 'Standard: General Markdown Formatting'
standard_id: SF-FORMATTING-MARKDOWN-GENERAL
aliases:
- General Markdown Formatting
- Document Structure
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
primary-topic: General Markdown Formatting
related-standards:
- SF-FORMATTING-FILE-HYGIENE
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-18T02:15:00Z'
primary_domain: SF
sub_domain: FORMATTING
scope_application: Defines general formatting principles for Markdown documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Document formatting
- Content readability
- Parsing consistency
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: General Markdown Formatting (SF-FORMATTING-MARKDOWN-GENERAL)

## 1. Standard Statement

This standard **MANDATES** general formatting principles for Markdown documents to ensure consistent structure, readability, and processing across the Knowledge Base.

## 2. Core Formatting Rules

### Rule 2.1: Paragraph Separation
Paragraphs **MUST** be separated by exactly one blank line.
*   **Example:**
    ```markdown
    This is the first paragraph.

    This is the second paragraph.
    ```

### Rule 2.2: Line Length and Wrapping
Text lines **SHOULD** wrap naturally without hard breaks unless specifically required for formatting. Manual line breaks within paragraphs **MUST NOT** be used except for specific formatting purposes (such as poetry or addresses).

### Rule 2.3: HTML Elements
Raw HTML elements **MUST NOT** be used within Markdown documents except where explicitly permitted by specific standards.

### Rule 2.4: Horizontal Rules
Horizontal rules **MUST** be created using three hyphens (`---`) on their own line, with blank lines above and below.
*   **Example:**
    ```markdown
    Content above the rule.

    ---

    Content below the rule.
    ```

### Rule 2.5: Trailing Blank Lines
Documents **MUST NOT** have more than one trailing blank line at the end.

## 3. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository. Adherence is **MANDATORY** for all content creators, automated systems, and tooling.

## 4. Cross-References
*   [[SF-FORMATTING-FILE-HYGIENE]]
*   [[CS-POLICY-TONE-LANGUAGE]]

---
*This standard (SF-FORMATTING-MARKDOWN-GENERAL) establishes general formatting principles for consistent Markdown structure across the Knowledge Base.*
