---
title: 'Standard: Frontmatter Structure and Content Rules (U-METADATA-FRONTMATTER-RULES-001)'
aliases: ['Frontmatter Standard', 'YAML Metadata Rules', 'FM-RULES-001']
tags:
  - kb-id/standards
  - content-type/standard-document
  - status/final
  - topic/metadata
  - topic/governance
  - topic/yaml
kb-id: standards
info-type: standard-document
primary-topic: 'Defines the canonical structure, key order, data types, and population rules for YAML frontmatter in all knowledge base documents.'
related-standards: ['M-SYNTAX-YAML-001', 'U-TAG-001', 'U-VALIDATION-METADATA-001']
version: '1.2.2'
date-created: '2025-05-19'
date-modified: '2025-05-23'
---

# Standard: Frontmatter Structure and Content Rules (U-METADATA-FRONTMATTER-RULES-001)

This standard defines the canonical structure, key order, data types, and population rules for YAML frontmatter in all Markdown documents within the knowledge base system. Adherence to this standard is critical for consistency, machine-readability, automated processing, and effective metadata management.

## Table of Contents
- [[#Standard: Canonical Frontmatter Definition (U-METADATA-FRONTMATTER-RULES-001)]]
- [[#Canonical Key List and Order]]
- [[#Detailed Key Population Rules]]
- [[#Process for Review and Updates]]

## Standard: Canonical Frontmatter Definition (U-METADATA-FRONTMATTER-RULES-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-METADATA-FRONTMATTER-RULES-001`    |
| Standard Name   | Frontmatter Structure and Content Rules |
| Standard Category | Metadata & Governance                 |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | All Markdown documents MUST use the exact list of keys, in the specified order, as defined in the "Canonical Key List and Order" section of this standard. | N/A                                                          | No additional keys are permitted unless this standard is updated.            |
| 1.2    | Each key MUST be populated according to the data type and rules specified in the "Detailed Key Population Rules" section of this standard.        | `version: '1.0.0'` (string)                                  | Ensures data integrity and consistency.                                      |
| 1.3    | YAML frontmatter MUST adhere to `M-SYNTAX-YAML-001` for general syntax (e.g., triple-dash delimiters, indentation).                             | N/A                                                          | Reinforces existing syntax standard.                                         |
| 1.4    | Frontmatter for new documents MUST be populated completely upon creation.                                                                       | N/A                                                          | Avoids placeholder or incomplete metadata.                                   |
| 1.5    | Frontmatter MUST be reviewed and updated (especially `date-modified`, `version`, `status`, and `related-standards`) whenever a document undergoes significant changes to its content or lifecycle state. | Change `status/draft` to `status/final` after review.        | See "Process for Review and Updates".                                        |

## Canonical Key List and Order

The following keys MUST be present in the YAML frontmatter of every Markdown document, in this exact order:

1.  `title`
2.  `aliases`
3.  `tags`
4.  `kb-id`
5.  `info-type`
6.  `primary-topic`
7.  `related-standards`
8.  `version`
9.  `date-created`
10. `date-modified`

## Detailed Key Population Rules

### 1. `title`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** Must exactly match the H1 heading of the document. Enclosed in single quotes if it contains colons or other special YAML characters.

### 2. `aliases`
-   **Type:** String or List of Strings
-   **Required:** Yes
-   **Rule:** If no aliases apply, the value MUST be the string "N/A". Otherwise, it is a list of strings containing alternative titles, common misspellings, acronyms, or search terms for the document. For standards documents, SHOULD include the Standard ID (e.g., `U-ARCH-001`). Values should be concise.

### 3. `tags`
-   **Type:** List of Strings
-   **Required:** Yes (must contain at least the mandatory sub-categories)
-   **Rule:** Adheres to `U-TAG-001`. Must include:
`content-type/*` (Tag): A hierarchical tag used for broad categorization, filtering, and navigation. Values are defined in `./master-knowledge-base/tag-glossary-definition.md` and MUST use kebab-case (e.g., `content-type/standard-document`, `content-type/llm-resource/recipe`).
    -   One `kb-id/{id}` tag (e.g., `kb-id/standards`).
    -   One `content-type/{type}` tag (e.g., `content-type/standard-document`). See controlled vocabulary below.
    -   One `status/{status}` tag (e.g., `status/draft`). Values for `status/*` tags MUST be chosen from the `status` category defined in `./master-knowledge-base/tag-glossary-definition.md`.
    -   At least one `topic/{topic}` tag (e.g., `topic/metadata`).
    -   Other relevant tags as appropriate.
-   **Controlled Vocabulary for `content-type/*`:**
    - Values for `content-type/*` tags MUST be chosen from the `content-type` category defined in `./master-knowledge-base/tag-glossary-definition.md`.

#### Special Clarification for Standards Directory
For documents within the `Standards/` directory:
- Files whose primary purpose is to define a specific standard (e.g., `U-ARCH-001.md`, `M-SYNTAX-YAML-001.md`) MUST use `content-type: standard-document` and `info-type: standard-document`.
- Files whose primary purpose is to collect or group standards (e.g., `COL-ARCH-UNIVERSAL.md`) MUST use `content-type: standards-collection` and `info-type: standards-collection`.
- Files whose primary purpose is to provide guidance on standards or processes (e.g., `GUIDE-TASK-BASED.md`) MUST use `content-type: standards-guide` and `info-type: standards-guide`.

### 4. `kb-id`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** The identifier of the knowledge base this document belongs to (e.g., `standards`, `llm-cookbook`). Must match the suffix of the `kb-id/*` tag. Use `global` for vault-level utility files not specific to one KB (e.g., `kb-directory.md`, `_key_definitions.md`).

### 5. `info-type`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** A specific, non-hierarchical string value that directly maps to a processing instruction, a specific content schema (e.g., a `U-SCHEMA-*` ID), or a unique structural role of the document. This key is critical for automation scripts and schema validation. Values for `info-type` MUST use kebab-case (e.g., `standard-document`, `llm-recipe`, `kb-definition-map`). The controlled vocabulary for `info-type` is maintained within this standard (`U-METADATA-FRONTMATTER-RULES-001`) under the 'Controlled Vocabulary for `info-type`' subsection.
-   **Controlled Vocabulary (initial set, mirrors `content-type` intent, all kebab-case):**
    - standard-document
    - standard-overview-document
    - kb-specific-standard-document
    - llm-recipe
    - llm-cookbook-standard-document
    - kb-definition-map
    - kb-root-document
    - kb-part-overview
    - kb-master-index-document
    - content-template-chapter
    - content-template-concept
    - content-template-methodology
    - content-template-reference
    - content-template-task
    - utility-script-documentation
    - key-definition-set
    - task-guide
    - tag-glossary-document
    - assembly-manifest-document
    - standards-collection
    - standards-guide
    - script-documentation
    - script-guide

### 6. `primary-topic`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** A concise (1-2 sentences) description of the document's main subject matter or purpose. Used for quick understanding and potentially in search results or summaries.

### 7. `related-standards`
-   **Type:** String or List of Strings
-   **Required:** Yes
-   **Rule:** If no related standards apply, the value MUST be the string "N/A". Otherwise, it is a list of strings, where each string is a valid Standard ID (e.g., `U-ARCH-001`) corresponding to an existing standard.

### 8. `version`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** Semantic versioning (e.g., `1.0.0`, `0.1.2`) is preferred. Initial drafts typically start at `0.1.0`. Increment according to SemVer rules (PATCH for fixes, MINOR for non-breaking additions, MAJOR for breaking changes). **The value MUST be enclosed in single quotes in the YAML frontmatter to ensure it is always parsed as a string (e.g., `version: '1.0.0'`, `version: '0.1'`).**

### 9. `date-created`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** The date the document was originally created, in `YYYY-MM-DD` format. This value SHOULD NOT change after initial creation.

### 10. `date-modified`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** The date the document was last significantly modified, in `YYYY-MM-DD` format. Must be updated upon every substantive change.

## Process for Review and Updates

1.  **New Document Creation:** All frontmatter keys listed above must be populated accurately.
2.  **Document Modification:**
    *   `date-modified` MUST be updated to the current date.
    *   `version` MUST be incremented appropriately if changes are substantive.
    *   `status` tag MAY change (e.g., from `status/draft` to `status/review-needed` or `status/final`).
    *   `related-standards`, `aliases`, `tags`, `primary-topic` should be reviewed and updated if the scope or content relationships of the document have changed.
3.  **Standard Evolution:** If new mandatory frontmatter keys are added to this standard (`U-METADATA-FRONTMATTER-RULES-001`), all existing documents MUST be updated to include them. This typically involves a batch update process.

**Cross-References to Other Standard IDs:** [[M-SYNTAX-YAML-001|M-SYNTAX-YAML-001]], [[U-TAG-001|U-TAG-001]], [[U-VALIDATION-METADATA-001|U-VALIDATION-METADATA-001]], [[COL-GOVERNANCE-UNIVERSAL#Standard: Versioning and Changelogs for Standard Files (U-VERSIONING-001)|U-VERSIONING-001]] 

## Exceptions for Specific info-type Files

While the canonical list of 10 frontmatter keys applies universally, the following exceptions are permitted for specific `info-type` values due to their unique structural requirements for machine processing:

-   Files with `info-type: kb-definition-map` are permitted to use the additional frontmatter key `parts:`. This key is essential for defining the structural components of a knowledge base and is used for automated KB assembly and navigation. The `parts:` key contains a list of objects, each defining a part of the KB.
-   Files with `info-type: key-definition-set` are permitted to use the additional frontmatter key `keys:`. This key is essential for the central management of reusable text snippets (keyrefs) and contains a dictionary of key-value pairs. 