---
title: 'Standard: Markdown Syntax for Lists'
standard_id: SF-SYNTAX-LISTS
aliases:
- List Syntax
- Ordered Lists
- Unordered Lists
- Nested Lists
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
primary-topic: Markdown List Syntax
related-standards:
- SF-SYNTAX-TABLES
- SF-SYNTAX-CODE
- SF-FORMATTING-FILE-HYGIENE
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the mandatory Markdown syntax for creating ordered (numbered)
  and unordered (bulleted) lists, including rules for nesting and interaction with
  other block elements.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Document structure
- Readability
- Accessibility
- Automated parsing
- Authoring consistency
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Lists (SF-SYNTAX-LISTS)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for creating ordered (numbered) and unordered (bulleted) lists. Consistent and strictly correct list syntax is **CRITICAL** for robust document structure, predictable rendering across all Markdown processors, guaranteed accessibility, and reliable automated parsing. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around list blocks is also **MANDATORY**.

## 2. Core List Syntax Rules

### Rule 2.1: Unordered List Marker
Unordered list items **MUST** be initiated exclusively with a hyphen (`-`) followed by a single space.
*   **Mandatory Syntax:** `- Item text`
*   **Prohibited Syntax:** Asterisks (`* Item text`), plus signs (`+ Item text`), or any other character **MUST NOT** be used as unordered list item markers.
*   **Example:**
    ```markdown
    - Task 1: Initialize system
    - Task 2: Configure settings
    ```
*   **Rationale:** Ensures a single, consistent visual and programmatic identifier for unordered list items across the entire Knowledge Base.

### Rule 2.2: Ordered List Marker
Ordered list items **MUST** be initiated exclusively with a number followed by a period (`.`) and a single space. The numbering for the first item in any new ordered list **MUST** start with `1.`.
*   **Mandatory Syntax:** `1. Item text`
*   **Prohibited Syntax:** Any numbering that does not start with `1.` for a new list (e.g., `2. Item text`), or the omission of the period or space, **MUST NOT** be used.
*   **Example:**
    ```markdown
    1. First step of the process
    2. Second step, following the first
    3. Third and final step
    ```
*   **Rationale:** Ensures clear, predictable sequential numbering and reliable parsing for ordered lists.

### Rule 2.3: Strict Indentation for Nested Lists
Nested list items **MUST** be indented by exactly **two (2) spaces** relative to the *start of the parent list item's content text* (i.e., the first character after the parent item's marker and its space). This typically results in a four-space indentation from the beginning of the line for a single level of nesting.
*   **Mandatory Indentation:** Two spaces relative to parent's content text.
*   **Prohibited Indentation:** Any other number of spaces (e.g., 3, 4, 1), or the use of tab characters for indentation, **MUST NOT** be used.
*   **Example:**
    ```markdown
    - Parent item content begins here.
      - Nested item 1 (indented 2 spaces from 'P')
        - Grand-nested item A (indented 2 spaces from 'N')
    1. Another parent item.
       - Nested unordered item (indented 2 spaces from 'A')
         1. Nested ordered item (indented 2 spaces from 'N')
    ```
*   **Rationale:** Strict indentation is paramount for consistent rendering and unambiguous parsing of complex, multi-level list structures across all Markdown processors.

### Rule 2.4: Blank Lines Around List Blocks
A single blank line **MUST** precede and a single blank line **MUST** follow every list block to clearly separate it from surrounding paragraphs or other block elements.
*   **Example:**
    ```markdown
    This is a paragraph before the list.

    - List item one
    - List item two

    This is a paragraph after the list.
    ```
*   **Rationale:** Prevents unintended merging of lists with adjacent content and ensures correct block-level rendering.

### Rule 2.5: Complex Block Elements Within List Items
When including complex block elements (such as paragraphs, code blocks, or tables) as part of a list item's content, these elements **MUST** be indented to align with the list item's content text (i.e., at least two spaces beyond the list item's marker indentation).
*   **Example (Code Block within a list item):**
    ```markdown
    - List item with a code block:

      ```python
      print("Hello, World!")
      ```
    ```
*   **Prohibition:** Placing complex block elements directly inside list items without proper indentation, or in a manner that breaks the list's logical flow, **MUST NOT** be done.
*   **Rationale:** Ensures that nested blocks are correctly associated with their parent list item and are rendered as part of the list item's content, maintaining structural integrity.

## 3. Importance of Strict List Syntax

*   **Universal Readability and Scannability:** Consistent list formatting makes complex information easier to digest and navigate for all users.
*   **Guaranteed Accessibility:** Correctly formatted lists are crucial for screen readers, allowing them to accurately convey list structure and content to users with disabilities.
*   **Reliable Automated Processing:** Tools for linting, validation, Table of Contents generation, and content transformation depend on strict and predictable list syntax to function correctly.
*   **Enhanced Maintainability:** A single, clear approach to lists simplifies document creation, editing, and long-term maintenance, reducing errors and ensuring consistency across the entire Knowledge Base.
*   **Unified KB Aesthetic:** Contributes to a professional and consistent visual aesthetic.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where ordered or unordered lists are used. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and any tooling interacting with KB Markdown files.

## 5. Cross-References
- [[CS-POLICY-TONE-LANGUAGE]] - For definitions of mandating keywords (MUST, SHOULD, MAY) and general language policy.
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines and file formatting.

---
*This standard (SF-SYNTAX-LISTS) has been revised to provide strict, singular mandates for list syntax and indentation, ensuring universal consistency as required for the Knowledge Base. It replaces and supersedes any prior interpretations or practices where conflicts existed, establishing a single source of truth for list application.*
