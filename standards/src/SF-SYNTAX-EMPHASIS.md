---
title: 'Standard: Text Emphasis Syntax'
standard_id: SF-SYNTAX-EMPHASIS
aliases:
- Text Emphasis
- Bold and Italic
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
primary-topic: Text Emphasis Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for text emphasis (bold, italic) in knowledge
  base documents.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Text formatting
- Content emphasis
- Readability
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Emphasis (SF-SYNTAX-EMPHASIS)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for applying emphasis—specifically italic, bold, and bold italic—to text within all knowledge base documents. Strict and consistent application of these syntax rules is **CRUCIAL** for ensuring consistent rendering across all Markdown processors, enabling robust automated processing, and maintaining a unified visual and semantic style across the entire Knowledge Base.

## 2. Core Emphasis Syntax Rules

### Rule 2.1: Italic Text
Italic text **MUST** be created by enclosing the text in single asterisks (`*`).
*   **Mandatory Syntax:** `*text to be italicized*`
*   **Prohibited Syntax:** Underscores (`_text to be italicized_`) **MUST NOT** be used for italics.
*   **Example:** `This is *important* to note.` will render as: This is *important* to note.
*   **Rationale:** Ensures a single, consistent approach to italicization, simplifying parsing and reducing ambiguity.

### Rule 2.2: Bold Text
Bold text **MUST** be created by enclosing the text in double asterisks (`**`).
*   **Mandatory Syntax:** `**text to be bolded**`
*   **Prohibited Syntax:** Double underscores (`__text to be bolded__`) **MUST NOT** be used for bold text.
*   **Example:** `This is **very important** for the user.` will render as: This is **very important** for the user.
*   **Rationale:** Establishes a singular, unambiguous method for bolding, vital for automated processing and visual uniformity.

### Rule 2.3: Bold and Italic Text
Text that requires both bold and italic emphasis **MUST** be created by enclosing the text in triple asterisks (`***`).
*   **Mandatory Syntax:** `***text to be bolded and italicized***`
*   **Prohibited Syntax:** Triple underscores (`___text to be bolded and italicized___`) and any combination of asterisks and underscores (e.g., `**_text_**`, `*__text__*`) **MUST NOT** be used.
*   **Example:** `This is ***extremely critical*** information.` will render as: This is ***extremely critical*** information.
*   **Rationale:** Ensures a definitive and singular syntax for combined emphasis, critical for consistent rendering and machine readability.

## 3. Importance of Consistent Emphasis Syntax

*   **Unambiguous Interpretation:** A single, mandated syntax eliminates confusion for authors and ensures Markdown processors interpret emphasis consistently.
*   **Predictable Rendering:** Guarantees that emphasis is rendered identically across all platforms and tools, maintaining visual integrity.
*   **Automated Processing Reliability:** Simplifies the development of parsing, linting, and transformation tools by providing a single target syntax to process.
*   **Enhanced Readability and Maintainability:** A uniform approach makes the raw Markdown easier to read, write, and maintain over time, reducing errors and enabling more efficient content management.
*   **Unified KB Aesthetic:** Contributes to a professional and consistent visual aesthetic across the entire Knowledge Base.

## 4. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where textual emphasis is required. Adherence is **MANDATORY** for all content creators and automated systems.

## 5. Cross-References
- [[CS-POLICY-TONE-LANGUAGE]] - For definitions of mandating keywords (MUST, SHOULD, MAY) and general language policy.

---
*This standard (SF-SYNTAX-EMPHASIS) replaces previous flexible guidelines with strict mandates for emphasis syntax, ensuring universal consistency as required for the Knowledge Base. It is derived from previous concepts in M-SYNTAX-EMPHASIS-001 from COL-SYNTAX-MARKDOWN.md, with updated enforcement.*
