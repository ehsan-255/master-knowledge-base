---
title: 'Standard: Content Schema for "Reference Topics" (U-SCHEMA-REFERENCE-001)'
tags:
  - standards-kb/universal
  - schemas
  - content-type/standard-document
  - status/draft
  - kb-id/standards
date-created: 2025-05-19
date-modified: 2025-05-23
version: '0.1.2'
info-type: standard-document
primary-topic: Defines the structure for reference-type content documents
related-standards:
  - U-STRUC-002
aliases: [Reference Topic Schema]
---

# Standard: Content Schema for "Reference Topics" (U-SCHEMA-REFERENCE-001)

This document details the universal standard schema for "Reference Topics." Reference topics provide factual, descriptive information, such as API specifications, command syntax, parts lists, glossaries, or configuration parameters. They are looked up for specific details rather than read sequentially.

## Table of Contents
- [[#Standard: Schema Definition for Reference Topics (U-SCHEMA-REFERENCE-001)]]
- [[#Core Sections]]
- [[#Optional Sections]]

## Standard: Schema Definition for Reference Topics (U-SCHEMA-REFERENCE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-SCHEMA-REFERENCE-001`              |
| Standard Name   | Content Schema for "Reference Topics" |
| Standard Category | Content Templates & Schemas           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Documents classified with `content-type: reference-topic` in their YAML frontmatter MUST adhere to this schema.                                 | File: `api-endpoint-xyz.md` with `content-type: reference-topic` | Ensures consistency for reference materials.                                   |
| 1.2    | The H1 title MUST be the specific name of the item being referenced (e.g., API Endpoint Name, Command Name, Term).                               | `# GET /users/{id}`                                          | Clear and specific identification.                                           |
| 1.3    | An introductory abstract (per `U-STRUC-002`) MUST briefly define or summarize the reference item and its purpose.                                 | "This document describes the `get_user_data` function..."    | Provides immediate context.                                                  |
| 1.4    | A Table of Contents (per `U-STRUC-002`) MUST be included, linking to all H2 sections.                                                           | `- [[#Syntax]]\n- [[#Parameters]]`                           | Essential for navigating reference information.                              |
| 1.5    | The document structure is flexible but typically includes H2 sections relevant to the type of reference material. Common sections are listed below. Authors MUST choose sections appropriate for the reference item. | N/A                                                          | Unlike Concept or Methodology, Reference topics have more structural variance. |

## Core Sections

While flexible, most Reference Topics will benefit from some of the following H2 sections, chosen as appropriate:

-   **`## Description` / `## Overview`**: A more detailed explanation than the abstract.
-   **`## Syntax` / `## Signature`**: For commands, functions, API calls.
-   **`## Parameters` / `## Arguments` / `## Properties` / `## Fields`**: Detailed list of inputs or attributes, often in a table. Each parameter should ideally have its own H3 or table row detailing type, description, and whether it's required.
-   **`## Return Values` / `## Output`**: For functions, APIs.
-   **`## Examples`**: Illustrative code snippets or usage scenarios.
-   **`## Attributes` / `## Values`**: For configuration items, enumerations.
-   **`## Error Codes` / `## Exceptions`**: Possible errors and their meanings.
-   **`## Definition`** (for glossary-like reference topics).

## Optional Sections

-   **`## Remarks` / `## Notes`**: Additional important information or context.
-   **`## Usage Guidelines`**: Best practices or specific instructions for using the reference item.
-   **`## Version History` / `## Changelog`**: If the reference item evolves.
-   **`## Summary`** (per `U-STRUC-002`)
-   **`## See Also`** (per `U-STRUC-002`)

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]] 