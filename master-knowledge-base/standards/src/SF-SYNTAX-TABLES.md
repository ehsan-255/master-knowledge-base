---
title: 'Standard: Table Syntax'
standard_id: SF-SYNTAX-TABLES
aliases:
  - Tables
  - Markdown Tables
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Table Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating tables in knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Table formatting
  - Data presentation
  - Content structure
change_log_url: ./changelog.md
---
# Standard: Markdown Syntax for Tables (SF-SYNTAX-TABLES)

## 1. Standard Statement

This standard defines the mandatory Markdown syntax for creating tables to structure and present data within all knowledge base documents. Consistent and correct table syntax is essential for readability, clear data presentation, and reliable parsing by Markdown processors. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around block elements is also important for tables.

## 2. Core Table Syntax Rules

### Rule 2.1: Basic Table Structure
Tables are created using pipes (`|`) to define column borders and hyphens (`-`) to create the header row separator.
*   **Header Row:** The first row defines the table headers.
*   **Separator Row:** The second row MUST be a separator line consisting of hyphens (`-`) for each column, separating the header cells from the body cells.
*   **Body Rows:** Subsequent rows define the table data.
*   **Columns:** Pipes (`|`) are used to separate cells within a row.

### Rule 2.2: Header Row Separator
The separator line between the header and the table body MUST use at least three hyphens (`---`) per column.
*   **Example (Minimum):**
    ```markdown
    | Header 1 | Header 2 |
    |---|---|
    | Cell 1.1 | Cell 1.2 |
    ```
*   **Example (More readable in raw text):**
    ```markdown
    | Header 1 | Header 2 |
    |----------|----------|
    | Cell 1.1 | Cell 1.2 |
    ```
*   **Rationale:** Clearly distinguishes the header from the table body.

### Rule 2.3: Column Alignment
Column alignment (left, right, center) can be specified by adding colons (`:`) to the header separator line.
*   **Left Alignment (Default):** `| :--- |` or `| --- |` (no colon or colon on the left)
*   **Right Alignment:** `| ---: |` (colon on the right)
*   **Center Alignment:** `| :---: |` (colons on both sides)
*   **Example:**
    ```markdown
    | Left Align | Center Align | Right Align |
    | :--------- | :----------: | ----------: |
    | Text       |    Text      |        Text |
    | Data       |    Data      |        Data |
    ```
*   **Rationale:** Allows for clear visual formatting of tabular data, improving readability in the rendered output.

### Rule 2.4: Outer Pipes (Optional but Recommended)
Outer pipes (`|`) at the beginning and end of each row are optional in many Markdown parsers but ARE RECOMMENDED for clarity and consistency in the raw Markdown source.
*   **Example (With outer pipes - Recommended):**
    ```markdown
    | Header 1 | Header 2 |
    |----------|----------|
    | Cell 1.1 | Cell 1.2 |
    ```
*   **Example (Without outer pipes - Allowed but less clear):**
    ```
    Header 1 | Header 2
    -------- | --------
    Cell 1.1 | Cell 1.2
    ```
*   **Rationale:** Including outer pipes makes the table structure more explicit and visually organized in the raw Markdown text, reducing ambiguity.

### Rule 2.5: Blank Lines Around Tables
A single blank line MUST precede and a single blank line MUST follow every table block to separate it from surrounding paragraphs or other block elements, as per [[SF-FORMATTING-FILE-HYGIENE]].
*   **Rationale:** Ensures correct table parsing and rendering.

## 3. Illustrative Example (Comprehensive)

```markdown
This is a paragraph before the table.

| Column A (Left) | Column B (Center) | Column C (Right) | Notes                       |
| :-------------- | :---------------: | ---------------: | :-------------------------- |
| Value 1         |   Centered Text   |       Right Text | First row of data           |
| Value 2         | Another Centered  |     Aligned Data | Second row with more detail |
| Value 3         |     Item C        |           $10.00 | Numeric data often right-aligned |

This is a paragraph after the table.
```
**Rendered Output (Conceptual):**

| Column A (Left) | Column B (Center) | Column C (Right) | Notes                       |
| :-------------- | :---------------: | ---------------: | :-------------------------- |
| Value 1         |   Centered Text   |       Right Text | First row of data           |
| Value 2         | Another Centered  |     Aligned Data | Second row with more detail |
| Value 3         |     Item C        |           $10.00 | Numeric data often right-aligned |

## 4. Best Practices for Table Readability

*   **Consistent Column Widths (Raw Text):** While rendered output varies, try to maintain somewhat consistent column widths in the raw Markdown source using spaces. This can improve the readability of the raw table definition, though it does not affect the final rendered output.
*   **Clear Headers:** Use concise and descriptive headers for each column.
*   **Simplicity:** For very complex data, consider if a table is the best presentation format or if the data should be broken down or presented differently. Markdown tables are best suited for relatively simple tabular data.
*   **Data Formatting:** Ensure data within cells is consistently formatted (e.g., alignment of numbers, date formats) where applicable.

## 5. Importance of Correct Table Syntax

*   **Clear Data Presentation:** Tables are essential for presenting structured data in a clear and understandable way.
*   **Readability:** Well-formatted tables improve the readability of documents containing tabular data.
*   **Authoring Consistency:** Ensures all authors use the same method for creating tables.
*   **Reliable Rendering:** Correct syntax is crucial for Markdown parsers to render tables accurately.

## 6. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where tabular data is presented.

## 7. Cross-References
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines around block elements like tables.

---
*This standard (SF-SYNTAX-TABLES) is based on common Markdown table syntax conventions.*
