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
date-modified: '2025-06-18T02:00:00Z'
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

This standard **MANDATES** the exclusive Markdown syntax for creating ordered (numbered) and unordered (bulleted) lists. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around list blocks is also **MANDATORY**.

## 2. Core List Syntax Rules

### Rule 2.1: Unordered List Marker
Unordered list items **MUST** be initiated exclusively with a hyphen (`-`) followed by a single space.
*   **Mandatory Syntax:** `- Item text`
*   **Prohibited:** Asterisks (`* Item text`), plus signs (`+ Item text`)
*   **Example:**
    ```markdown
    - Task 1: Initialize system
    - Task 2: Configure settings
    ```

### Rule 2.2: Ordered List Marker
Ordered list items **MUST** be initiated with a number followed by a period (`.`) and a single space. The numbering **MUST** start with `1.` for new ordered lists.
*   **Mandatory Syntax:** `1. Item text`
*   **Prohibited:** Starting with numbers other than `1.` (e.g., `2. Item text`)
*   **Example:**
    ```markdown
    1. First step of the process
    2. Second step, following the first
    3. Third and final step
    ```

### Rule 2.3: Strict Indentation for Nested Lists
Nested list items **MUST** be indented by exactly **two (2) spaces** relative to the parent list item's content text.
*   **Critical Example (showing exact spacing):**
    ```markdown
    - Parent item content begins here.
      - Nested item 1 (indented 2 spaces from 'P')
        - Grand-nested item A (indented 2 spaces from 'N')
    1. Another parent item.
       - Nested unordered item (indented 2 spaces from 'A')
         1. Nested ordered item (indented 2 spaces from 'N')
    ```

### Rule 2.4: Blank Lines Around List Blocks
A single blank line **MUST** precede and follow every list block.
*   **Example:**
    ```markdown
    This is a paragraph before the list.

    - List item one
    - List item two

    This is a paragraph after the list.
    ```

### Rule 2.5: Complex Block Elements Within List Items
Complex block elements within list items **MUST** be indented to align with the list item's content text.
*   **Example (Code Block within list item):**
    ```markdown
    - List item with a code block:

      ```python
      print("Hello, World!")
      ```
    
    - Another list item with paragraph:

      This is a paragraph within the list item.
      It continues the list item content.
    ```

## 3. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where ordered or unordered lists are used. Adherence is **MANDATORY** for all content creators, automated systems, and tooling.

## 4. Cross-References
- [[CS-POLICY-TONE-LANGUAGE]] - For definitions of mandating keywords (MUST, SHOULD, MAY)
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines and file formatting

---
*This standard (SF-SYNTAX-LISTS) establishes strict, singular mandates for list syntax and indentation, ensuring universal consistency for the Knowledge Base.*
