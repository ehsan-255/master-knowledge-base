---
title: 'Standard: Definition List Syntax'
standard_id: SF-SYNTAX-DEFINITION-LISTS
aliases:
- Definition Lists
- Term Definitions
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
primary-topic: Definition List Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating definition lists in knowledge base
  documents.
criticality: P3-Low
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content structure
- Term definitions
- Document formatting
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Definition Lists (SF-SYNTAX-DEFINITION-LISTS)

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax for creating definition lists within Markdown documents. Definition lists **MUST** present a series of terms, each followed by one or more definitions or descriptions. Adherence to this syntax is **CRITICAL** for consistency and compatibility with Markdown processors.

Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around definition list blocks is also **MANDATORY**.

## 2. Core Definition List Syntax

### Rule 2.1: Term
The term to be defined **MUST** be placed on a line by itself.
*   **Syntax:** `Term to be defined`

### Rule 2.2: Definition(s)
Each definition for the term **MUST** start on a new line, be preceded by a colon (`:`), and be indented by **four spaces**.
*   **Syntax (Single Definition):**
    ```markdown
    Term
    :    Definition of the term.
    ```
*   **Syntax (Multiple Definitions or Paragraphs per Term):**
    Multiple definition lines for the same term **MUST** each start with an indented colon. Blank lines between definition paragraphs for the same term **MUST** also start with an indented colon (or be sufficiently indented).
    ```markdown
    Term
    :    First definition or first paragraph.
    :    Second definition or second paragraph.
    ```
*   **Indentation:** Consistent four-space indentation after the colon is **MANDATORY**.

### Rule 2.3: Blank Lines
*   A blank line **MUST** precede the first term of a definition list.
*   A blank line **MUST** be used to separate one term-definition group from the next term in the list. Each definition line **MUST** start with an indented colon.
*   A blank line **MUST** follow the entire definition list block.

## 3. Illustrative Examples

### Example 3.1: Basic Definition List
```markdown
Apple
:    A round fruit, typically red, green, or yellow.
:    Keeps the doctor away if consumed daily.

Banana
:    An elongated, curved fruit with yellow skin when ripe.
```

## 4. Parser Compatibility

Definition list syntax is a Markdown extension. The chosen authoring and publishing toolchain for the Knowledge Base **MUST** support this syntax.

## 5. Importance of Strict Definition List Syntax

*   **Semantic Representation:** Clearly and semantically represents term-definition pairs.
*   **Readability:** Improves readability of glossaries and definitional content.
*   **Authoring Consistency:** Ensures all authors use the same method for creating definition lists.
*   **Styling:** Allows specific CSS styling in rendered HTML.

## 6. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where definition lists are used. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 7. Cross-References
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-DEFINITION-LISTS) has been revised to mandate a strict, singular syntax for definition lists, ensuring consistency and reliable rendering across the Knowledge Base.*
