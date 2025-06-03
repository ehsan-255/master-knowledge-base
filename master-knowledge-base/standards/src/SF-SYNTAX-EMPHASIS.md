---
title: 'Standard: Text Emphasis Syntax'
standard_id: SF-SYNTAX-EMPHASIS
aliases:
  - Text Emphasis
  - Bold and Italic
tags:
  - status/draft
  - criticality/p2-medium
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Text Emphasis Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
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
---
# Standard: Markdown Syntax for Emphasis (SF-SYNTAX-EMPHASIS)

## 1. Standard Statement

This standard defines the mandatory Markdown syntax for applying emphasis—specifically italic, bold, and bold italic—to text within all knowledge base documents. Consistent application of these syntax rules enhances readability, ensures correct rendering across different Markdown processors, and supports semantic interpretation of emphasis.

## 2. Core Emphasis Syntax Rules

### Rule 2.1: Italic Text (Derived from M-SYNTAX-EMPHASIS-001, Rule 1.1)
Italic text MUST be created by enclosing the text in either single asterisks (`*`) or single underscores (`_`).
*   **Syntax Options:**
    *   `*text to be italicized*`
    *   `_text to be italicized_`
*   **Consistency:** While both syntaxes are valid, authors SHOULD choose one style (either asterisks or underscores) for italics and use it consistently within a single document to maintain stylistic uniformity. Project-wide consistency is also encouraged but not strictly mandated by this syntax rule if intra-document consistency is met.
*   **Example (using asterisks):** `This is *important* to note.` will render as: This is *important* to note.
*   **Example (using underscores):** `This is _also important_ to note.` will render as: This is _also important_ to note.
*   **Rationale:** Provides standard ways to apply light emphasis, typically used for highlighting key terms, foreign words, or for subtle emphasis.

### Rule 2.2: Bold Text (Derived from M-SYNTAX-EMPHASIS-001, Rule 1.2)
Bold text MUST be created by enclosing the text in either double asterisks (`**`) or double underscores (`__`).
*   **Syntax Options:**
    *   `**text to be bolded**`
    *   `__text to be bolded__`
*   **Consistency:** Similar to italics, authors SHOULD choose one style (either double asterisks or double underscores) for bold text and use it consistently within a single document.
*   **Example (using double asterisks):** `This is **very important** for the user.` will render as: This is **very important** for the user.
*   **Example (using double underscores):** `This is __also very important__ for the user.` will render as: This is __also very important__ for the user.
*   **Rationale:** Provides standard ways to apply strong emphasis, typically used for highlighting critical information, warnings, or for strong emphasis.

### Rule 2.3: Bold and Italic Text (Derived from M-SYNTAX-EMPHASIS-001, Rule 1.3)
Text that requires both bold and italic emphasis MUST be created by enclosing the text in either triple asterisks (`***`) or triple underscores (`___`).
*   **Syntax Options:**
    *   `***text to be bolded and italicized***`
    *   `___text to be bolded and italicized___`
*   **Consistency:** The choice between triple asterisks or triple underscores should naturally follow from the chosen styles for italic and bold emphasis within the document (e.g., if using `*italic*` and `**bold**`, then `***bold italic***` is the consistent choice).
*   **Example (using triple asterisks):** `This is ***extremely critical*** information.` will render as: This is ***extremely critical*** information.
*   **Example (using triple underscores):** `This is ___also extremely critical___ information.` will render as: This is ___also extremely critical___ information.
*   **Alternative Combination:** It is also syntactically valid to combine asterisk and underscore styles, such as `**_bold italic_**` or `*__bold italic__*`. However, for simplicity and maximum compatibility, using triple asterisks or triple underscores is recommended. If combining, ensure the opening and closing tags are correctly mirrored.
*   **Rationale:** Provides a standard way to apply the strongest level of combined emphasis.

## 3. Importance of Consistent Emphasis Syntax

*   **Readability:** Consistent use of emphasis syntax makes raw Markdown easier to read and edit.
*   **Predictable Rendering:** Ensures that emphasis is rendered correctly and predictably across different Markdown platforms and tools.
*   **Semantic Meaning:** While Markdown emphasis is primarily presentational, consistent usage can subtly reinforce semantic meaning (e.g., italics for terms, bold for warnings).
*   **Authoring Efficiency:** Clear rules reduce ambiguity for authors when deciding how to apply emphasis.

## 4. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where textual emphasis is required.

## 5. Cross-References
*(None directly applicable for basic emphasis syntax, but related to overall Markdown authoring.)*

---
*This standard (SF-SYNTAX-EMPHASIS) is based on rules 1.1 through 1.3 previously defined in M-SYNTAX-EMPHASIS-001 from COL-SYNTAX-MARKDOWN.md.*
