---
title: 'Standard: Table Syntax'
standard_id: SF-SYNTAX-TABLES
aliases:
- Tables
- Markdown Tables
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
primary-topic: Table Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating tables in knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Table formatting
- Data presentation
- Content structure
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Tables (SF-SYNTAX-TABLES)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for creating tables to structure and present data within all Knowledge Base documents. Strict and consistent table syntax is **CRITICAL** for ensuring universal readability, precise data presentation, and reliable automated parsing. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around table blocks is also **MANDATORY**.

## 2. Core Table Syntax Rules

### Rule 2.1: Basic Table Structure
Tables **MUST** be created using pipes (`|`) for column borders and hyphens (`-`) for the header row separator. Every row (**MUST** include header, separator, and body rows), **MUST** begin and end with a pipe (`|`).
*   **Header Row:** The first row **MUST** define table headers.
*   **Separator Row:** The second row **MUST** be a separator line of hyphens (`-`), separating header cells from body cells.
*   **Body Rows:** Subsequent rows **MUST** define table data.
*   **Columns:** Pipes (`|`) **MUST** separate cells within a row.
*   **Example (Mandatory Syntax):**
    ```markdown
    | Header 1 | Header 2 |
    |----------|----------|
    | Cell 1.1 | Cell 1.2 |
    ```
*   **Prohibited:** Omitting outer pipes (`|`) at the beginning or end of any row.
*   **Rationale:** Ensures clear, universally parsable, and visually consistent table structure.

### Rule 2.2: Header Row Separator Length
The separator line **MUST** use at least three hyphens (`---`) per column segment. For readability, it is **RECOMMENDED** that hyphen count roughly matches header cell content length.
*   **Example (Minimum Valid):**
    ```markdown
    | Header 1 | Header 2 |
    |---|---|
    | Cell 1.1 | Cell 1.2 |
    ```
*   **Example (Recommended for Readability):**
    ```markdown
    | Long Header Name | Another Header |
    |------------------|----------------|
    | Data Value       | More Data      |
    ```
*   **Rationale:** Distinguishes header from body and aids raw Markdown source readability.

### Rule 2.3: Column Alignment Specification
Column alignment (**MUST** be left, right, or center) **MUST** be specified using colons (`:`) within the header separator line. Default is left alignment if no colon is present.
*   **Left Alignment (Default or Explicit):** `| :--- |` or `| --- |`
*   **Right Alignment:** `| ---: |`
*   **Center Alignment:** `| :---: |`
*   **Example:**
    ```markdown
    | Left Aligned Column | Center Aligned Column | Right Aligned Column |
    | :------------------ | :-------------------: | -------------------: |
    | Text Example        |     Centered Text     |         Right Text   |
    | Numerical Data      |         123.45        |                 987  |
    ```
*   **Rationale:** Provides precise visual formatting for tabular data, improving readability.

### Rule 2.4: Blank Lines Around Tables
A single blank line **MUST** precede and a single blank line **MUST** follow every table block to separate it from surrounding paragraphs or other block elements.
*   **Example:**
    ```markdown
    This is a paragraph before the table.

    | Header A | Header B |
    |----------|----------|
    | Data 1   | Data 2   |

    This is a paragraph after the table.
    ```
*   **Rationale:** Ensures correct table parsing and rendering as a distinct block element, preventing unintended merging.

## 3. Importance of Strict Table Syntax

*   **Guaranteed Data Presentation Clarity:** Ensures tables are clear, readable, and consistent.
*   **Reliable Automated Processing:** Allows accurate identification, parsing, and processing of tabular data by tools.
*   **Enhanced Authoring Consistency:** Provides a single, clear method for authors, reducing errors and fostering uniformity.
*   **Unified KB Aesthetic:** Contributes to professional and consistent visual presentation of tabular data.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where tabular data is presented. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 5. Cross-References
*   [[CS-POLICY-TONE-LANGUAGE]]
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-TABLES) has been extensively revised to provide strict, singular mandates for table syntax, including specific rules for structure, separators, and alignment. It replaces and supersedes any prior interpretations or practices where conflicts existed, establishing a single source of truth for tabular data representation within the Knowledge Base.*
