---
title: 'Standard: Footnote Syntax'
standard_id: SF-SYNTAX-FOOTNOTES
aliases:
- Footnotes
- Reference Notes
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p3-low
- kb-id/standards
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Footnote Syntax
related-standards:
- SF-SYNTAX-MARKDOWN-TEXT
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-18T03:05:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating footnotes in knowledge base documents.
criticality: P3-Low
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Reference formatting
- Content annotation
- Document structure
---
# Standard: Markdown Syntax for Footnotes (SF-SYNTAX-FOOTNOTES)

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax for creating footnotes within Markdown documents. Footnotes provide supplementary information without disrupting main text flow. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around footnote definition blocks is also **MANDATORY**.

## 2. Core Footnote Syntax

### Rule 2.1: Footnote Marker in Text
A footnote marker **MUST** be placed in the text where the reference occurs, without a preceding space.
*   **Syntax:** `[^identifier]`
*   **Identifier:** Unique label that **MUST** be numeric (e.g., `[^1]`) or descriptive alphanumeric (e.g., `[^note1]`). **MUST NOT** contain spaces or special Markdown characters.
*   **Example:**
    ```markdown
    This text requires a footnote.[^1]
    Another reference needs a note.[^note-alpha]
    ```

### Rule 2.2: Footnote Definition
The definition **MUST** provide the footnote content.
*   **Syntax:** `[^identifier]: Footnote text.`
*   **Identifier:** **MUST** exactly match the identifier in the corresponding inline marker.
*   **Placement:** Footnote definitions **MUST** be placed at the end of the document, separated by blank lines.

### Rule 2.3: Multi-line Footnote Content
For footnotes containing multiple paragraphs or block elements, subsequent lines **MUST** be indented (typically four spaces) to align under the footnote text start.
*   **Example:**
    ```markdown
    [^complex]: This is the first paragraph of the footnote.
        This continues the same footnote, indented.

        A new paragraph within the footnote, also indented.
        - A list item within the footnote
    ```

### Rule 2.4: Unique Identifiers
Footnote identifiers **MUST** be unique within a single document.

## 3. Parser Compatibility and Placement

Footnote definitions **MUST** be placed together at the end of the document to improve raw Markdown readability and ensure consistent rendering.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where footnotes are used. Adherence is **MANDATORY** for all content creators, automated systems, and tooling.

## 5. Cross-References
*   [[SF-FORMATTING-FILE-HYGIENE]]
*   [[SF-SYNTAX-MARKDOWN-TEXT]]

---
*This standard (SF-SYNTAX-FOOTNOTES) establishes strict footnote syntax requirements, ensuring consistency and reliable rendering across the Knowledge Base.*
