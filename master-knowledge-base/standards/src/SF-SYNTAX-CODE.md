---
title: "Standard: Markdown Syntax for Code (Inline and Blocks)"
standard_id: "SF-SYNTAX-CODE"
aliases: ["Code Syntax", "Markdown Code Blocks", "Inline Code Syntax"]
tags:
  - status/draft
  - criticality/P1-High # Correct code representation is vital
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Markdown Code Syntax" # As per assumed keyword
related-standards: ["SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER"] # For blank line rules around blocks
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "SYNTAX" # As per prompt
scope_application: "Defines the mandatory Markdown syntax for representing inline code and code blocks (both fenced and indented) in all knowledge base documents."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Readability of technical content", "Accuracy of code representation", "Authoring consistency", "Syntax highlighting in rendered views"]
change_log_url: "./SF-SYNTAX-CODE-changelog.md" # Placeholder
---

# Standard: Markdown Syntax for Code (Inline and Blocks) (SF-SYNTAX-CODE)

## 1. Standard Statement

This standard defines the mandatory Markdown syntax for representing inline code snippets and extended code blocks within all knowledge base documents. Consistent and correct code syntax is essential for readability, accuracy, and proper rendering, including syntax highlighting where applicable. Adherence to [[SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER]] regarding blank lines around block elements is also important for code blocks.

## 2. Core Code Syntax Rules

### Rule 2.1: Inline Code
Inline code snippets MUST be created by enclosing the code within single backticks (`` ` ``).
*   **Syntax:** `` `code snippet here` ``
*   **Usage:** Used for short code references, variable names, function names, commands, or file paths embedded within a paragraph or sentence.
*   **Example:**
    ```markdown
    To install the package, run `npm install my-package`. The function `calculateTotal()` returns an integer.
    ```
*   **Rationale:** Clearly distinguishes code elements from surrounding prose, improving readability and preventing misinterpretation of special characters.

### Rule 2.2: Fenced Code Blocks (Preferred Method for Blocks)
Fenced code blocks MUST be used for multi-line code examples or longer code snippets. They are created by enclosing the code block within triple backticks (```` ``` ````) on the lines immediately before and after the code.
*   **Syntax (Basic):**
    ````markdown
    ```
    multiple lines
    of code
    go here
    ```
    ````
*   **Language Identifier (Highly Recommended):** A language identifier SHOULD be specified immediately after the opening triple backticks to enable syntax highlighting in rendered views.
    *   **Syntax (with language identifier):**
        ````markdown
        ```python
        def hello_world():
            print("Hello, world!")
        ```
        ````
    *   **Common Language Identifiers:** `python`, `javascript`, `java`, `csharp`, `bash`, `yaml`, `json`, `html`, `css`, `sql`, `markdown`, `text` (for plain text).
*   **Blank Lines:** A blank line SHOULD precede and follow the fenced code block for readability and to ensure correct parsing, as per [[SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER]].
*   **Rationale:** Fenced code blocks are the most common and robust method for displaying code, offering clear delimitation and support for language-specific syntax highlighting, which significantly improves readability and comprehension.

### Rule 2.3: Indented Code Blocks (Alternative, Less Preferred)
Indented code blocks, created by indenting each line of the code block by four (4) spaces or one (1) tab, are a valid Markdown syntax but are generally less preferred than fenced code blocks.
*   **Syntax:**
    ```markdown
        // This is an indented code block
        function example() {
            return true;
        }
    ```
    (Note: The above example has 4 leading spaces on each code line.)
*   **Preference:** Fenced code blocks (Rule 2.2) with language identifiers ARE STRONGLY PREFERRED over indented code blocks.
*   **Rationale for Preference:**
    *   Fenced code blocks explicitly define the start and end of the block, reducing ambiguity.
    *   Fenced code blocks allow for easy specification of the language for syntax highlighting, which is not possible with indented blocks.
    *   Indented blocks can sometimes be accidentally created or interact confusingly with list indentation.
*   **Usage Note:** If used, indented code blocks MUST also be separated from surrounding text by a blank line.

## 3. Importance of Correct Code Syntax

*   **Readability:** Clearly distinguishes code from narrative text. Syntax highlighting (with fenced code blocks) significantly improves the readability of code.
*   **Accuracy:** Ensures that code is displayed correctly, preserving indentation and special characters.
*   **Authoring Consistency:** Provides a uniform way for authors to represent code.
*   **Maintainability:** Easy to identify and update code sections.
*   **Accessibility:** While not a replacement for accessible code practices, clear visual separation helps all users.

## 4. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where inline code or code blocks are used.

## 5. Cross-References
- [[SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER]] - For rules on blank lines around block elements.

---
*This standard (SF-SYNTAX-CODE) is based on common Markdown conventions for inline code and code blocks, emphasizing the preference for fenced code blocks with language identifiers.*
```
