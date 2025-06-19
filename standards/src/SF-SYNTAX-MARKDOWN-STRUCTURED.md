---
title: 'Standard: Markdown Structured Content Syntax'
standard_id: SF-SYNTAX-MARKDOWN-STRUCTURED
aliases:
- Structured Markdown Syntax
- Lists and Tables
- Code and Images
- Block Content
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Markdown Structured Content Syntax
related-standards:
- SF-SYNTAX-MARKDOWN-TEXT
- SF-FORMATTING-MARKDOWN-GENERAL
- SF-ACCESSIBILITY-IMAGE-ALT-TEXT
version: 1.0.0
date-created: '2025-06-18T02:45:00Z'
date-modified: '2025-06-18T02:45:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines comprehensive Markdown syntax for structured content elements (lists, tables, code, images).
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Document structure
- Data presentation
- Code representation
- Content accessibility
---
# Standard: Structured Markdown Syntax (SF-SYNTAX-MARKDOWN-STRUCTURED)

## 1. Standard Statement

This standard **MANDATES** comprehensive syntax for structured Markdown elements. This consolidated standard covers lists, tables, code blocks, images, and definition lists, ensuring universal consistency for structured content across the Knowledge Base.

## 2. List Syntax

### Rule 2.1: Unordered Lists
Unordered lists **MUST** use hyphens (`-`) as the list marker.
*   **Basic Syntax:** `- List item`
*   **Example:**
    ```markdown
    - First item
    - Second item
    - Third item
    ```

### Rule 2.2: Ordered Lists
Ordered lists **MUST** use numbers followed by periods.
*   **Basic Syntax:** `1. List item`
*   **Example:**
    ```markdown
    1. First step
    2. Second step
    3. Third step
    ```

### Rule 2.3: Nested Lists
For nested lists, **MUST** use exactly **four spaces** for each indentation level.
*   **Example:**
    ```markdown
    - Top level item
        - Nested item (4 spaces)
            - Double nested item (8 spaces)
        - Another nested item
    - Another top level item
    ```

### Rule 2.4: Mixed List Types
Ordered and unordered lists **MAY** be mixed in nested structures.
*   **Example:**
    ```markdown
    1. First ordered item
        - Nested unordered item
        - Another nested unordered item
    2. Second ordered item
    ```

## 3. Table Syntax

### Rule 3.1: Basic Table Structure
Tables **MUST** use pipe (`|`) characters to separate columns and hyphens (`-`) in the header separator row.
*   **Basic Structure:**
    ```markdown
    | Header 1 | Header 2 | Header 3 |
    |----------|----------|----------|
    | Row 1 Col 1 | Row 1 Col 2 | Row 1 Col 3 |
    | Row 2 Col 1 | Row 2 Col 2 | Row 2 Col 3 |
    ```

### Rule 3.2: Column Alignment
Column alignment **MUST** be specified in the separator row using colons.
*   **Left-aligned:** `|----------|` (default)
*   **Center-aligned:** `|:--------:|`
*   **Right-aligned:** `|---------:|`
*   **Example:**
    ```markdown
    | Left | Center | Right |
    |------|:------:|------:|
    | L1   | C1     | R1    |
    | L2   | C2     | R2    |
    ```

### Rule 3.3: Table Formatting
*   **Leading and trailing pipes:** **MUST** be present on every row
*   **Consistent spacing:** **RECOMMENDED** for readability but not mandatory
*   **Empty cells:** **PERMITTED** but **MUST** maintain pipe structure

## 4. Code Block Syntax

### Rule 4.1: Inline Code
Inline code **MUST** use single backticks.
*   **Syntax:** `` `code` ``
*   **Example:** Use the `printf()` function for output.

### Rule 4.2: Fenced Code Blocks
Multi-line code blocks **MUST** use triple backticks with optional language identifier.
*   **Basic Syntax:**
    ````markdown
    ```
    code content
    ```
    ````
*   **With Language Identifier:**
    ````markdown
    ```python
    def hello_world():
        print("Hello, World!")
    ```
    ````

### Rule 4.3: Language Identifiers
Language identifiers **SHOULD** use standard language names for syntax highlighting.
*   **Common identifiers:** `python`, `javascript`, `bash`, `yaml`, `json`, `markdown`

## 5. Image Syntax

### Rule 5.1: Basic Image Syntax
Images **MUST** use the standard Markdown image syntax.
*   **Syntax:** `![alt text](image-url "optional title")`
*   **Example:** `![Diagram showing process flow](./images/process-flow.png "Process Flow Diagram")`

### Rule 5.2: Alt Text Requirements
Alt text **MUST** be meaningful and descriptive. Adherence to [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]] is **MANDATORY**.

### Rule 5.3: Image Paths
*   **Relative paths:** **PREFERRED** for images within the repository
*   **Absolute URLs:** **PERMITTED** for external images
*   **Example paths:** `./images/filename.png`, `../assets/diagram.svg`

## 6. Definition List Syntax

### Rule 6.1: Term Declaration
Terms to be defined **MUST** be placed on a line by themselves.
*   **Syntax:** `Term to be defined`

### Rule 6.2: Definition Format
Each definition **MUST** start on a new line, be preceded by a colon (`:`), and be indented by **four spaces**.
*   **Single Definition:**
    ```markdown
    Term
    :    Definition of the term.
    ```
*   **Multiple Definitions:**
    ```markdown
    Term
    :    First definition or first paragraph.
    :    Second definition or second paragraph.
    ```

### Rule 6.3: Definition List Example
```markdown
Apple
:    A round fruit, typically red, green, or yellow.
:    Keeps the doctor away if consumed daily.

Banana
:    An elongated, curved fruit with yellow skin when ripe.
```

## 7. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository. Adherence is **MANDATORY** for all content creators, automated systems, and tooling.

## 8. Cross-References
*   [[SF-SYNTAX-MARKDOWN-TEXT]]
*   [[SF-UTILITIES-MARKDOWN]]
*   [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-MARKDOWN-STRUCTURED) provides comprehensive syntax requirements for all structured Markdown elements, ensuring consistency and reliability across the Knowledge Base.* 