---
title: 'Standard: Markdown Syntax for Code (Inline and Blocks)'
standard_id: SF-SYNTAX-CODE
aliases:
- Code Syntax
- Markdown Code Blocks
- Inline Code Syntax
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
primary-topic: Markdown Code Syntax
related-standards:
- SF-FORMATTING-FILE-HYGIENE
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the mandatory Markdown syntax for representing inline code
  and code blocks (both fenced and indented) in all knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Readability of technical content
- Accuracy of code representation
- Authoring consistency
- Syntax highlighting in rendered views
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Code (Inline and Blocks) (SF-SYNTAX-CODE)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for representing inline code snippets and extended code blocks within all Knowledge Base documents. Strict and consistent code syntax is **CRITICAL** for ensuring accuracy, enabling reliable automated processing (e.g., syntax highlighting, code extraction), and maintaining a unified technical presentation across the entire Knowledge Base. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around code blocks is also **MANDATORY**.

## 2. Core Code Syntax Rules

### Rule 2.1: Inline Code
Inline code snippets **MUST** be created exclusively by enclosing the code within single backticks (`` ` ``).
*   **Mandatory Syntax:** `` `code snippet here` ``
*   **Usage:** This syntax **MUST** be used for short code references, variable names, function names, commands, file paths, or any technical term that represents code, embedded directly within a paragraph or sentence.
*   **Example:** `To start the application, execute the `main.py` script. The configuration is defined by the `MAX_RETRIES` parameter.`
*   **Rationale:** Provides clear and consistent visual distinction for code elements within prose, enhancing readability and preventing misinterpretation of special characters.

### Rule 2.2: Fenced Code Blocks (Mandatory Method for Blocks)
Fenced code blocks **MUST** be used for all multi-line code examples or longer code snippets. They are created by enclosing the code block within triple backticks (```` ``` ````) on separate lines immediately preceding and following the code content.
*   **Mandatory Language Identifier:** A language identifier **MUST** be specified immediately after the opening triple backticks to enable proper syntax highlighting and semantic interpretation by automated tools.
    *   **Mandatory Syntax:**
        ````markdown
        ```language-identifier
        multiple lines
        of code
        go here
        ```
        ````
    *   **Common Language Identifiers (MUST be used where applicable):** `python`, `javascript`, `java`, `csharp`, `bash`, `yaml`, `json`, `html`, `css`, `sql`, `markdown`, `text` (for plain text where no specific language applies).
*   **Blank Lines:** A single blank line **MUST** precede and a single blank line **MUST** follow every fenced code block to ensure correct block-level rendering and separation from surrounding content.
*   **Prohibited Syntax:** Indented code blocks (using four spaces or a tab for indentation) **MUST NOT** be used under any circumstances.
*   **Example:**
    ````markdown
    ```python
    def calculate_sum(a, b):
        return a + b

    result = calculate_sum(10, 20)
    print(f"The sum is: {result}")
    ```
    ````
*   **Rationale:** Fenced code blocks with language identifiers are the most robust, universally supported, and machine-readable method for displaying code, providing explicit delimitation and enabling crucial syntax highlighting for improved comprehension and maintainability.

## 3. Importance of Strict Code Syntax

*   **Guaranteed Readability & Accuracy:** Strict adherence ensures that all code snippets are clearly distinguishable from regular text and are rendered with consistent formatting and correct syntax highlighting.
*   **Reliable Automated Processing:** Enables tools to accurately parse, extract, and validate code examples, which is vital for linting, documentation generation, and automated testing.
*   **Enhanced Maintainability:** A uniform approach simplifies the authoring, reviewing, and updating of technical content, reducing potential errors and ensuring consistency.
*   **Unified Technical Presentation:** Contributes to a professional and consistent visual and functional presentation of all code within the Knowledge Base.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where inline code or code blocks are used. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and any tooling interacting with KB Markdown files.

## 5. Cross-References
- [[CS-POLICY-TONE-LANGUAGE]] - For definitions of mandating keywords (MUST, SHOULD, MAY) and general language policy.
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines around block elements.

---
*This standard (SF-SYNTAX-CODE) has been extensively revised to provide strict, singular mandates for code syntax, emphasizing fenced code blocks with mandatory language identifiers and prohibiting deprecated indented code blocks. It replaces and supersedes any prior interpretations or practices where conflicts existed, establishing a single source of truth for code representation within the Knowledge Base.*
