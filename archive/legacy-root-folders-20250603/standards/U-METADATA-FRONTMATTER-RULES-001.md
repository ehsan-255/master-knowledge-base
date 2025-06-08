---
title: 'Standard: Frontmatter Structure and Content Rules (U-METADATA-FRONTMATTER-RULES-001) - DEPRECATED'
aliases:
- Frontmatter Standard
- YAML Metadata Rules
- FM-RULES-001
tags:
- content-type/standard-document
- kb-id/standards
- status/deprecated
- topic/governance
- topic/metadata
- topic/yaml
kb-id: standards
info-type: standard-document
primary-topic: Defines the canonical structure, key order, data types, and population rules for YAML frontmatter in all knowledge base documents.
related-standards:
- MT-SCHEMA-FRONTMATTER
version: 1.3.0
date-created: '2025-05-19T00:00:00Z'
date-modified: '2025-06-02T00:46:42Z'
---
**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: [[MT-SCHEMA-FRONTMATTER]].

> [!WARNING] DEPRECATED: This Standard is No Longer Active
> **Reason for Deprecation:** This standard has been superseded by [[MT-SCHEMA-FRONTMATTER]].
> Please refer to the new standard for current guidelines. This document is retained for historical purposes only.

# Standard: Frontmatter Structure and Content Rules (U-METADATA-FRONTMATTER-RULES-001)

This standard defines the canonical structure, key order, data types, and population rules for YAML frontmatter in all Markdown documents within the knowledge base system. Adherence to this standard is critical for consistency, machine-readability, automated processing, and effective metadata management.

## Table of Contents
- [[#Standard: Canonical Frontmatter Definition (U-METADATA-FRONTMATTER-RULES-001)]]
- [[#Canonical Key List and Order]]
- [[#Detailed Key Population Rules]]
- [[#File Naming and Identifier Conventions]]
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
| 1.1    | All Markdown documents MUST use the keys as defined in the "Detailed Key Population Rules" section and adhere to the order specified in the "Recommended Frontmatter Order" section of this standard. | N/A                                                          | No additional keys are permitted unless this standard is updated.            |
| 1.2    | Each key MUST be populated according to the data type and rules specified in the "Detailed Key Population Rules" section of this standard.        | `version: '1.0.0'` (string)                                  | Ensures data integrity and consistency.                                      |
| 1.3    | YAML frontmatter MUST adhere to `M-SYNTAX-YAML-001` for general syntax (e.g., triple-dash delimiters, indentation).                             | N/A                                                          | Reinforces existing syntax standard.                                         |
| 1.4    | Frontmatter for new documents MUST be populated completely upon creation with all mandatory keys.                                               | N/A                                                          | Avoids placeholder or incomplete metadata.                                   |
| 1.5    | Frontmatter MUST be reviewed and updated (especially `date-modified`, `version`, `status`, and `related-standards`) whenever a document undergoes significant changes to its content or lifecycle state. | Change `status/draft` to `status/final` after review.        | See "Process for Review and Updates".                                        |

## Technical Requirements for Frontmatter

This subsection details the technical encoding and formatting requirements for YAML frontmatter.

### Encoding and Line Endings

-   **Rule 2.1 (UTF-8 Encoding):** YAML frontmatter in all Markdown files MUST use "UTF-8" (Unicode Transformation Format—8-bit) encoding. A Byte Order Mark (BOM) MUST NOT be used.
    -   *Rationale:* Ensures universal compatibility across platforms and tools, prevents parsing issues, and aligns with common web standards.
-   **Rule 2.2 (LF Line Endings):** YAML frontmatter in all Markdown files MUST use Line Feed (LF) line endings. Carriage Return Line Feed (CRLF) line endings are not permitted.
    -   *Rationale:* Ensures consistency across different operating systems (Unix-style endings) and prevents issues with version control systems and text processing tools.

## Recommended Frontmatter Order

The following order for YAML frontmatter keys is recommended for all Markdown documents to ensure consistency and improve readability. Mandatory keys are indicated; others are optional or conditionally required based on the document type and content.

1.  `title` (Mandatory)
2.  `standard_id` (Mandatory for standards, recommended for others where applicable)
3.  `aliases` (Optional. If no aliases apply, the value MUST be the string "N/A")
4.  `tags` (Mandatory. Must include `status/*`, `content-type/*`. Recommended: `criticality/*`, `topic/*`, `kb-id/*` if applicable)
5.  `kb-id` (Conditionally Mandatory: If the document belongs to a specific knowledge base)
6.  `info-type` (Mandatory)
7.  `primary-topic` (Mandatory)
8.  `related-standards` (Optional. If no related standards apply, the value MUST be the string "N/A")
9.  `version` (Mandatory)
10. `date-created` (Mandatory)
11. `date-modified` (Mandatory)
12. `primary_domain` (Mandatory)
13. `sub_domain` (Mandatory)
14. `scope_application` (Mandatory)
15. `criticality` (Mandatory)
16. `lifecycle_gatekeeper` (Mandatory)
17. `impact_areas` (Mandatory, list at least one)
18. `change_log_url` (Conditionally Mandatory: For documents with a version history)

This list represents the comprehensive order. The "Detailed Key Population Rules" section provides specifics on each key's requirements and data types. Adherence to this order is critical for automated processing and metadata management.

## Detailed Key Population Rules

### 1. `title`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** Must exactly match the H1 heading of the document. Enclosed in single quotes if it contains colons or other special YAML characters.

### 2. `standard_id`
-   **Type:** String
-   **Required:** Yes (for standards documents, recommended for others where applicable)
-   **Rule:** A unique identifier for the standard. MUST conform to the regex `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`. See the "`standard_id` Format and Regex" section under "File Naming and Identifier Conventions" for full details. The filename (excluding the `.md` extension) SHOULD be identical to this value for standards documents, as per the "Filename and `standard_id` Equivalence" rule.

### 3. `aliases`
-   **Type:** String or List of Strings
-   **Required:** Yes (If no aliases apply, the value MUST be the string "N/A")
-   **Rule:** A list of strings containing alternative titles, common misspellings, acronyms, or search terms for the document. For standards documents, SHOULD include the Standard ID (e.g., `U-ARCH-001`). Values should be concise.

### 4. `tags`
-   **Type:** List of Strings
-   **Required:** Yes (must contain at least the mandatory sub-categories)
-   **Rule:** Adheres to `U-TAG-001`. Must include:
`content-type/*` (Tag): A hierarchical tag used for broad categorization, filtering, and navigation. Values are defined in `./master-knowledge-base/tag-glossary-definition.md` and MUST use kebab-case (e.g., `content-type/standard-document`, `content-type/llm-resource/recipe`).
    -   One `kb-id/{id}` tag (e.g., `kb-id/standards`), if applicable.
    -   One `content-type/{type}` tag (e.g., `content-type/standard-document`). See controlled vocabulary in `master-knowledge-base/standards/registry/tag-glossary-definition.md`.
    -   One `status/{status}` tag (e.g., `status/draft`). Values for `status/*` tags MUST be chosen from the `status` category defined in `master-knowledge-base/standards/registry/tag-glossary-definition.md`.
    -   One or more `criticality/{level}` tags (e.g., `criticality/P0-Critical`) if the `criticality` key is not used.
    -   At least one `topic/{topic}` tag (e.g., `topic/metadata`).
    -   Other relevant tags as appropriate.
-   **Controlled Vocabulary for `content-type/*`:**
    - Values for `content-type/*` tags MUST be chosen from the `content-type` category defined in `./master-knowledge-base/tag-glossary-definition.md`.

#### Special Clarification for Standards Directory
For documents within the `Standards/` directory:
- Files whose primary purpose is to define a specific standard (e.g., `U-ARCH-001.md`, `M-SYNTAX-YAML-001.md`) MUST use `info-type: standard-definition` and an appropriate `content-type/*` tag.
- Files whose primary purpose is to collect or group standards (e.g., `COL-ARCH-UNIVERSAL.md`) MUST use `info-type: registry-document` or similar and an appropriate `content-type/*` tag.
- Files whose primary purpose is to provide guidance on standards or processes (e.g., `GUIDE-TASK-BASED.md`) MUST use `info-type: guide-document` and an appropriate `content-type/*` tag.

### 5. `kb-id`
-   **Type:** String
-   **Required:** Yes, if the document belongs to a specific knowledge base.
-   **Rule:** The identifier of the knowledge base this document belongs to (e.g., `standards`, `llm-cookbook`). Must match the suffix of the `kb-id/*` tag. Use `global` for vault-level utility files not specific to one KB (e.g., `kb-directory.md`, `_key_definitions.md`).

### 6. `info-type`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** A specific, non-hierarchical string value that directly maps to a processing instruction, a specific content schema (e.g., a `U-SCHEMA-*` ID), or a unique structural role of the document. This key is critical for automation scripts and schema validation. Values for `info-type` MUST use kebab-case (e.g., `standard-definition`, `policy-document`). The controlled vocabulary for `info-type` is defined below.
-   **Controlled Vocabulary for `info-type`:**
    *   `standard-definition`: For documents that define specific rules, syntax, or structural requirements (the "how/where").
    *   `policy-document`: For documents that outline mandates, guidelines, or strategic approaches (the "what/when/why").
    *   `guide-document`: For instructional or explanatory documents that help users apply standards or navigate the KB.
    *   `glossary-document`: For documents that primarily define terms.
    *   `tag-glossary-document`: Specifically for glossaries defining tags.
    *   `key-definition-set`: For documents defining sets of keys or variables.
    *   `kb-definition-map`: For documents that define the structure or map of a knowledge base.
    *   `registry-document`: For documents that act as a registry for controlled vocabulary terms (e.g. domain codes, sub-domain codes).
    *   `template-document`: For files that serve as templates for creating new documents.
    *   `schema-definition`: For documents defining data schemas (e.g., JSON schema, frontmatter schema).
    *   `report-document`: For documents that are outputs of tools, like validation or index reports.

### 7. `primary-topic`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** A concise (1-2 sentences) description of the document's main subject matter or purpose. Used for quick understanding and potentially in search results or summaries.

### 8. `related-standards`
-   **Type:** String or List of Strings
-   **Required:** Yes
-   **Rule:** If no related standards apply, the value MUST be the string "N/A". Otherwise, it is a list of strings, where each string is a valid Standard ID (e.g., `U-ARCH-001`) corresponding to an existing standard.

### 9. `version`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** Semantic versioning (e.g., `1.0.0`, `0.1.2`) is preferred. Initial drafts typically start at `0.1.0`. Increment according to SemVer rules (PATCH for fixes, MINOR for non-breaking additions, MAJOR for breaking changes). **The value MUST be enclosed in single quotes in the YAML frontmatter to ensure it is always parsed as a string (e.g., `version: '1.0.0'`, `version: '0.1'`).**

### 10. `date-created`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** The date and time the document was originally created. MUST use the full ISO-8601 date-time format, including the time and a 'Z' for UTC (e.g., `2025-05-27T15:42:00Z`). This value SHOULD NOT change after initial creation.

### 11. `date-modified`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** The date and time the document was last significantly modified. MUST use the full ISO-8601 date-time format, including the time and a 'Z' for UTC (e.g., `2025-05-27T15:42:00Z`). Must be updated upon every substantive change.

### 12. `primary_domain`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** The primary domain code this standard or document belongs to. Values MUST correspond to a `DOMAIN_CODE` defined in `master-knowledge-base/standards/registry/domain_codes.yaml`. (e.g., `AS` for Architectural Standards, `CS` for Content Standards).

### 13. `sub_domain`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** The sub-domain code within the primary domain. Values MUST correspond to a `code` defined under the respective `DOMAIN_CODE` in `master-knowledge-base/standards/registry/subdomain_registry.yaml`. (e.g., `STRUCTURE` for Architectural Standards > Structural Standards).

### 14. `scope_application`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** A clear and concise description of the scope or context where this standard or document applies (e.g., "All knowledge base documents", "Technical documentation for Project X only", "API development standards").

### 15. `criticality`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** The criticality level of the standard or document. Values MUST correspond to a `level` defined in `master-knowledge-base/standards/registry/criticality_levels.yaml` (e.g., `P0-Critical`, `P1-High`). It is also recommended to include a corresponding `criticality/{level}` tag in the `tags` field (e.g., `criticality/P0-Critical`). Using the dedicated `criticality` key is the preferred method for explicit metadata.

### 16. `lifecycle_gatekeeper`
-   **Type:** String
-   **Required:** Yes
-   **Rule:** Specifies the review or approval process needed for this standard or document. Values MUST correspond to a `gatekeeper` value defined in `master-knowledge-base/standards/registry/lifecycle_gatekeepers.yaml` (e.g., `Architect-Review`, `SME-Consensus`).

### 17. `impact_areas`
-   **Type:** List of Strings
-   **Required:** Yes
-   **Rule:** A list of areas, systems, processes, or teams potentially impacted by this standard or document (e.g., ["Authoring workflow", "Publishing pipeline", "System X integration", "Developer onboarding"]). Provide at least one impact area.

### 18. `change_log_url`
-   **Type:** String (URL)
-   **Required:** Yes, for documents with a version history.
-   **Rule:** A relative or absolute URL pointing to the change log or history for this standard or document.
    -   If the URL is a relative path (e.g., starting with `./` or `../`), it MUST point to an existing file within the repository. Automated validation processes (linters) MUST check for the existence of this linked file.
    -   If it's an absolute URL, it MUST be a valid URL format. Automated validation processes (linters) MUST perform basic syntax validation (e.g., ensuring it starts with `http://` or `https://`).
    -   Example: `./changelogs/U-METADATA-FRONTMATTER-RULES-001.md` or `https://example.com/standards/changelog/U-METADATA-FRONTMATTER-RULES-001`.

## File Naming and Identifier Conventions

This section outlines the standards for naming files and constructing identifiers to ensure consistency and machine-readability across the knowledge base.

### Atomic File Naming Convention

All atomic knowledge base files (individual Markdown documents representing a single concept, standard, guide, etc.) MUST adhere to the following naming convention:

`{DOMAIN_CODE}-{SUB_DOMAIN_CODE}-{PRIMARY_TOPIC_KEYWORD}-{OPTIONAL_SECONDARY_TOPICS*}.md`

**Components:**

*   **`DOMAIN_CODE`**: A 2-letter uppercase code representing the primary domain of the content (e.g., `U` for Universal, `M` for Methodological, `T` for Technical, `P` for Product).
*   **`SUB_DOMAIN_CODE`**: A 2-6 letter uppercase code representing the specific sub-domain or category within the primary domain (e.g., `ARCH` for Architecture, `META` for Metadata, `SEC` for Security).
*   **`PRIMARY_TOPIC_KEYWORD`**: A concise, descriptive keyword (or hyphenated multi-word keyword) in uppercase that clearly indicates the main subject of the file (e.g., `FRONTMATTER-RULES`, `ACCESS-CONTROL`).
*   **`OPTIONAL_SECONDARY_TOPICS*`**: Optional, hyphenated uppercase keywords that further specify the content if needed. These are used to differentiate files with the same primary topic keyword but different nuances or sub-topics (e.g., `U-META-FRONTMATTER-RULES-ADVANCED.md` vs. `U-META-FRONTMATTER-RULES-BASIC.md`). Each secondary topic should be preceded by a hyphen.

**Examples:**

*   `U-METADATA-FRONTMATTER-RULES-001.md` (A universal standard for metadata frontmatter rules, version/identifier 001)
*   `T-AWS-S3-BUCKET-ENCRYPTION-POLICY.md` (A technical document about AWS S3 bucket encryption policies)
*   `M-AGILE-SCRUM-DAILY-STANDUP-GUIDE.md` (A methodological guide for Agile Scrum daily standups)

Adherence to this naming convention is crucial for discoverability, organization, and automated processing.

### `standard_id` Format and Regex

The `standard_id` field in the frontmatter is a critical unique identifier for standards documents. Its value MUST conform to the following regular expression:

`^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`

**Explanation of the Regex:**

*   `^`: Asserts the start of the string.
*   `[A-Z]{2}`: Exactly two uppercase English letters. This represents the `DOMAIN_CODE`.
*   `-`: A literal hyphen.
*   `[A-Z]{2,6}`: Between two and six uppercase English letters. This represents the `SUB_DOMAIN_CODE`.
*   `-`: A literal hyphen.
*   `[A-Z0-9\-]+`: One or more uppercase English letters, numerals (0-9), or hyphens. This represents the `PRIMARY_TOPIC_KEYWORD` and any `OPTIONAL_SECONDARY_TOPICS` or versioning numbers (e.g., `001`).
*   `$`: Asserts the end of the string.

**Examples of valid `standard_id` values:**

*   `U-METADATA-FRONTMATTER-RULES-001`
*   `T-AWS-S3-ENCRYPTION`
*   `M-AGILE-SPRINT-PLANNING-V2`

This regex ensures that `standard_id` values are consistently formatted, facilitating automated validation, linking, and reporting.

### Filename and `standard_id` Equivalence

For optimal consistency, discoverability, and linkability, the filename of a standards document (excluding the `.md` extension) SHOULD ideally be identical to the value in its `standard_id` frontmatter field.

**Example:**

*   If `standard_id: U-ARCH-HIGH-AVAILABILITY-003`
*   Then the filename SHOULD be: `U-ARCH-HIGH-AVAILABILITY-003.md`

While minor deviations might occur due to historical reasons or specific tooling limitations, new documents MUST strive for this equivalence. This simplifies cross-referencing and makes it intuitive to locate a standard document given its ID, and vice-versa.

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