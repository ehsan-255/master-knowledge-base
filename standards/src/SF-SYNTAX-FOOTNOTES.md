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
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Footnote Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating footnotes in knowledge base documents.
criticality: P3-Low
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Reference formatting
- Content annotation
- Document structure
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Footnotes (SF-SYNTAX-FOOTNOTES)

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax for creating footnotes within Markdown documents. Footnotes provide supplementary information, explanations, or citations without disrupting the main text flow. Adherence to this syntax is **CRITICAL** for consistency and compatibility with Markdown processors.

Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around footnote definition blocks is also **MANDATORY**.

## 2. Core Footnote Syntax

Footnote syntax involves two parts: an inline marker and a definition block.

### Rule 2.1: Footnote Marker in Text
A footnote marker **MUST** be placed in the text where the reference occurs, without a preceding space.
*   **Syntax:** `[^identifier]`
*   **`identifier`**: A unique label linking the marker to its definition. It **MUST** be numeric (e.g., `[^1]`) or a descriptive textual label (e.g., `[^note1]`). Textual labels **MUST NOT** contain spaces or special Markdown characters; use simple alphanumeric strings with hyphens or underscores.
*   **Example:**
    ```markdown
    This is some text that requires a footnote.[^1]
    Another piece of information needs a different kind of note.[^note-alpha]
    ```

### Rule 2.2: Footnote Definition
The definition **MUST** provide the content of the footnote.
*   **Syntax:** `[^identifier]: Footnote text.`
*   **`identifier`**: This **MUST** exactly match the identifier in the corresponding inline marker.
*   **`Footnote text.`**: The content of the footnote. This can include multiple lines, paragraphs, and block elements, provided they are indented correctly.
*   **Placement:** Footnote definitions **MUST** be placed at the end of the document, separated from main text and each other by blank lines.
*   **Indentation for Multi-line/Block Content:** If a footnote definition contains multiple paragraphs or block elements, subsequent lines/blocks **MUST** be indented (typically by four spaces) to align under the start of the footnote text.
    ```markdown
    [^identifier]: This is the first paragraph of the footnote.
        This is still part of the same footnote, indented.

        A new paragraph within the footnote, also indented.
        - A list item within the footnote
    ```

### Rule 2.3: Uniqueness of Identifiers
Footnote identifiers **MUST** be unique within a single document.
*   **Rationale:** Duplicate identifiers lead to ambiguous references and incorrect rendering.

## 3. Parser Compatibility and Placement of Definitions

Footnote syntax is a Markdown extension. The chosen authoring and publishing toolchain for the Knowledge Base **MUST** support this syntax.

Footnote definitions **MUST** be placed together at the end of the document to improve raw Markdown readability and consistent rendering.

## 4. Importance of Strict Footnote Syntax

*   **Clarity:** Provides a standard way to offer supplementary information without disrupting main text flow.
*   **Readability:** Footnotes are clearly linked and presented in a dedicated section, aiding comprehension.
*   **Authoring Consistency:** Ensures all authors use the same method for creating footnotes.
*   **Academic/Referential Integrity:** Useful for citations or elaborations in formal documents.

## 5. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where footnotes are used. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 6. Cross-References
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-FOOTNOTES) has been revised to mandate a strict, singular syntax for footnotes, ensuring consistency and reliable rendering across the Knowledge Base.*
