---
title: "Standard: Relational Table (Reltable) Definition Schema"
standard_id: "AS-SCHEMA-RELTABLE-DEFINITION"
aliases: ["Reltable Schema", "Schema for Relational Data Tables"]
tags: ["status/draft", "criticality/P3-Medium", "content-type/schema-document", "topic/schemas", "topic/data-structures", "topic/structured-data", "kb-id/standards"]
kb-id: "kb-id/standards"
info-type: "schema-document"
primary-topic: "Defines the standard structure and syntax for representing relational table-like data (Reltables) within knowledge base documents."
related-standards: ["MT-SCHEMA-FRONTMATTER", "SF-FORMATTING-MARKDOWN-GENERAL", "SF-SYNTAX-TABLES"] # May also relate to YAML standards if applicable
version: "0.1.0"
date-created: "2025-05-29T15:55:50Z"
date-modified: "2025-05-29T15:55:50Z"
primary_domain: "AS" # Architecture & Structure
sub_domain: "SCHEMA" # Defines a data schema
scope_application: "Applies to any content requiring the structured representation of relational data in a tabular format, potentially beyond standard Markdown tables, for clarity, consistency, or automated processing."
criticality: "P3-Medium" # Importance depends on adoption and use cases.
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Structured data representation", "Data consistency", "Automated data extraction", "Content requiring tabular relational data"]
change_log_url: "./AS-SCHEMA-RELTABLE-DEFINITION-changelog.md"
---

# Standard: Relational Table (Reltable) Definition Schema (AS-SCHEMA-RELTABLE-DEFINITION)

## 1. Standard Statement

This standard defines the recommended structure and syntax for representing "Reltables" – structured, relational table-like data – within knowledge base documents. The goal is to provide a consistent method for authors to include tabular data that may have relational characteristics or require more explicit schema definition than standard Markdown tables alone offer.

> [!TODO] This standard is a placeholder based on the ID `U-RELTABLE-DEFINITION-001`. The concept of "Reltable" needs further definition and justification. The content below is speculative and requires significant review and elaboration based on actual use cases. If this concept is not deemed necessary or is covered by other standards (e.g., advanced use of Markdown tables, CSV embedding, or specific YAML structures for data), this standard may be deprecated or significantly revised.

## 2. Purpose and Use Cases

Reltables are intended for scenarios where:
-   Standard Markdown tables (`[[SF-SYNTAX-TABLES]]`) are insufficient to capture data type constraints, relationships, or complex cell structures.
-   Data needs to be easily parsed by automated tools for validation, extraction, or further processing.
-   A consistent, schema-driven representation of tabular data is required across multiple documents.

Potential use cases:
-   Comparison tables with defined column types.
-   Small, embedded datasets.
-   Glossaries or definition lists requiring structured fields per term.
-   Representing outputs of analyses or experiments.

## 3. Reltable Definition and Syntax

*(This section requires significant elaboration based on the chosen representation for Reltables.)*

Two potential approaches (to be decided):

### Approach A: Extended Markdown Table Conventions
-   Utilizes standard Markdown table syntax.
-   Defines specific conventions for header rows to indicate column names and potentially data types (e.g., `Header (string)`, `Count (integer)`).
-   May define conventions for indicating primary keys or links to other Reltables or documents.

### Approach B: YAML Structure for Reltables
-   Defines a specific YAML schema for representing the table's metadata (column definitions, data types) and its row data.
-   This YAML block could be included in the document frontmatter or as a distinct YAML code block in the body.

**Key elements to define for a Reltable Schema:**
-   **Table Identifier/Name:** A unique name for the Reltable instance or type.
-   **Column Definitions:**
    -   `column_id`: A unique identifier for the column.
    -   `column_label`: The human-readable header for the column.
    -   `data_type`: Expected data type (e.g., `string`, `integer`, `boolean`, `date`, `uri`, `[[Standard_ID]]`).
    -   `is_required`: Boolean, whether the column must have a value for each row.
    -   `is_primary_key`: Boolean, indicates if this column (or combination of columns) serves as a primary key for the row.
    -   `description`: Optional description of the column's content.
-   **Row Data:** The actual data, structured as a list of objects (if YAML) or rows in a Markdown table.

## 4. Examples

> [!TODO] Provide concrete examples once the Reltable syntax (Markdown-based or YAML-based) is finalized.

### Example (Conceptual Markdown-based Reltable):

```markdown
| ID (string, PK) | Name (string) | Status (enum:active,inactive) | Last Updated (date) |
|-----------------|---------------|-------------------------------|---------------------|
| ITEM-001        | Example Item A| active                        | 2024-01-15          |
| ITEM-002        | Example Item B| inactive                      | 2024-01-10          |
```

### Example (Conceptual YAML-based Reltable):

```yaml
reltable_id: "UserActivitySummary"
columns:
  - column_id: "userId"
    column_label: "User ID"
    data_type: "string"
    is_primary_key: true
  - column_id: "lastLogin"
    column_label: "Last Login"
    data_type: "date-time"
  - column_id: "actionCount"
    column_label: "Actions This Month"
    data_type: "integer"
rows:
  - userId: "user123"
    lastLogin: "2025-05-29T10:00:00Z"
    actionCount: 42
  - userId: "user456"
    lastLogin: "2025-05-28T14:30:00Z"
    actionCount: 15
```

## 5. Validation and Usage
- Reltables SHOULD be validated against their defined schema.
- Tools MAY be developed to parse, validate, or transform Reltables.

## 6. Scope of Application
This standard applies to any document within the knowledge base ecosystem where structured, relational tabular data needs to be presented in a standardized manner that potentially exceeds the capabilities or consistency of basic Markdown tables.
