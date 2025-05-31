---
title: 'Standard: Frontmatter Schema Definition'
standard_id: MT-SCHEMA-FRONTMATTER
aliases:
- Frontmatter Schema
- Metadata Schema for Frontmatter
tags:
- status/draft
- criticality/p0-critical
- content-type/standard-definition
- topic/metadata
- topic/frontmatter
- topic/schema
kb-id: standards
info-type: standard-definition
primary-topic: Defines the comprehensive schema for YAML frontmatter, including all keys, their order, data types, validation rules, and controlled vocabularies.
related-standards:
- SF-SYNTAX-YAML-FRONTMATTER
- SF-FORMATTING-FILE-HYGIENE
- MT-REGISTRY-TAG-GLOSSARY
- AS-STRUCTURE-TEMPLATES-DIRECTORY
- QM-VALIDATION-METADATA
version: 0.1.0
date-created: '2025-05-29T15:40:18Z'
date-modified: '2025-05-30T12:00:00Z'
primary_domain: MT
sub_domain: FRONTMATTER
scope_application: Applies to the YAML frontmatter of all Markdown documents in all knowledge bases.
criticality: p0-critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Metadata integrity
- Content validation
- Authoring consistency
- Automated processing
- Interoperability
change_log_url: ./MT-SCHEMA-FRONTMATTER-changelog.md
---
# Standard: Frontmatter Schema Definition

## Introduction

This document defines the official schema for YAML frontmatter in all Markdown documents. It specifies the allowed keys, their required order, the data types for their values, their mandatory or optional status, and associated validation rules. 

Adherence to this schema is crucial for maintaining consistency across the knowledge base, enabling automated validation of metadata, and facilitating various automated processing tasks.

For rules regarding the syntax of YAML frontmatter itself (e.g., the use of `---` delimiters), refer to `[[SF-SYNTAX-YAML-FRONTMATTER]]`. For requirements related to file encoding, line endings, and other file hygiene aspects, see `[[SF-FORMATTING-FILE-HYGIENE]]`.

## Overall Structure and Key Order

The YAML frontmatter block MUST contain the following keys in the specified order. This order integrates the original 10 keys and the 7 new extension keys.

1.  `title`
2.  `standard_id` (for standards documents, optional otherwise but recommended if it has a canonical ID)
3.  `aliases`
4.  `tags`
5.  `kb-id`
6.  `info-type`
7.  `primary-topic`
8.  `related-standards`
9.  `version`
10. `date-created`
11. `date-modified`
12. `primary_domain` (for standards documents, optional otherwise)
13. `sub_domain` (for standards documents, optional otherwise)
14. `scope_application`
15. `criticality`
16. `lifecycle_gatekeeper`
17. `impact_areas`
18. `change_log_url`

This order is **mandatory**.

## Detailed Key Definitions

### `title`
*   **Description/Purpose:** The official title of the document.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must not be empty.

### `standard_id`
*   **Description/Purpose:** A unique identifier for a standard document.
*   **Mandatory/Optional:** Mandatory for `info-type` values such as `standard-definition`, `policy-document`. Optional for other document types, but recommended if the document has a canonical identifier.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** MUST follow the regex pattern: `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`. The filename of the document (excluding the `.md` extension) SHOULD be identical to the `standard_id`.

### `aliases`
*   **Description/Purpose:** A list of alternative names or titles by which the document might be known.
*   **Mandatory/Optional:** Optional.
*   **Data Type:** List of Strings.
*   **Validation Rules & Constraints:** None beyond being a list of strings.

### `tags`
*   **Description/Purpose:** A list of keywords or labels used to categorize the document. Tags help in searching, filtering, and understanding the document's context.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** List of Strings.
*   **Validation Rules & Constraints:** All tags MUST be in kebab-case. The list MUST include tags from specific categories, such as `status/*`, `content-type/*`, and `topic/*`. For a comprehensive list of allowed tags and their meanings, refer to `[[MT-REGISTRY-TAG-GLOSSARY]]`.

### `kb-id`
*   **Description/Purpose:** An identifier for the knowledge base this document belongs to.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must be in kebab-case. Value must come from a controlled vocabulary defined in `[[MT-REGISTRY-TAG-GLOSSARY]]` or a dedicated knowledge base registry.

### `info-type`
*   **Description/Purpose:** Specifies the type or category of information the document represents (e.g., a standard, a policy, a guide). This is critical for automation and consistent processing.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must be in kebab-case. The value MUST be one of the predefined values in the Controlled Vocabularies section below.

### `primary-topic`
*   **Description/Purpose:** A concise statement (typically a sentence) describing the main subject or purpose of the document.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must not be empty.

### `related-standards`
*   **Description/Purpose:** A list of other standards that are related to this document.
*   **Mandatory/Optional:** Optional.
*   **Data Type:** List of Strings.
*   **Validation Rules & Constraints:** Each string in the list MUST be a valid `standard_id` of another document or a valid internal link in the format `[[STANDARD_ID]]`.

### `version`
*   **Description/Purpose:** The version number of the document.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Semantic versioning (e.g., `'1.0.0'`, `'0.2.1-alpha'`) is preferred.

### `date-created`
*   **Description/Purpose:** The date and time when the document was originally created.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** MUST be in ISO-8601 date-time format: `YYYY-MM-DDTHH:MM:SSZ`.

### `date-modified`
*   **Description/Purpose:** The date and time when the document was last modified.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** MUST be in ISO-8601 date-time format: `YYYY-MM-DDTHH:MM:SSZ`.

### `primary_domain`
*   **Description/Purpose:** The primary domain code (e.g., "IT", "HR", "MT" for Meta).
*   **Mandatory/Optional:** Mandatory for standards documents; optional otherwise.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must be 2 uppercase letters. The value MUST exist in `[[domain_codes.yaml]]`.

### `sub_domain`
*   **Description/Purpose:** The sub-domain code (e.g., "SECURITY", "NETWORK", "SCHEMA").
*   **Mandatory/Optional:** Mandatory for standards documents; optional otherwise.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must be 2-6 uppercase letters. The value MUST exist in `[[subdomain_registry.yaml]]` for the given `primary_domain`.

### `scope_application`
*   **Description/Purpose:** Defines the scope to which this document applies (e.g., "All backend services", "Frontend components in Project X").
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must not be empty.

### `criticality`
*   **Description/Purpose:** The criticality level of the document or the standard it defines.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Value MUST come from the controlled vocabulary (e.g., `P0-Critical`, `P1-High`, `P2-Medium`). Refer to `[[MT-REGISTRY-TAG-GLOSSARY]]`.

### `lifecycle_gatekeeper`
*   **Description/Purpose:** Specifies the role or team responsible for approving transitions in the document's lifecycle (e.g., "Architect-Review", "Security-Team-Approval").
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Value MUST come from a controlled vocabulary. Refer to `[[MT-REGISTRY-TAG-GLOSSARY]]`.

### `impact_areas`
*   **Description/Purpose:** A list of areas or systems that are affected by this document or standard.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** List of Strings.
*   **Validation Rules & Constraints:** None beyond being a list of strings.

### `change_log_url`
*   **Description/Purpose:** A URL or relative path pointing to the document's changelog.
*   **Mandatory/Optional:** Mandatory for standards.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** If a relative path, it MUST start with `./`. A linter SHOULD check for the existence of the linked file if it's a relative path.

## Controlled Vocabularies

This section defines or references the controlled vocabularies for specific frontmatter keys.

### `info-type`

The `info-type` key MUST use one of the following string values (all in kebab-case):

*   `standard-definition`
*   `policy-document`
*   `guide-document`
*   `glossary-document`
*   `template-document`
*   `registry-document`
*   `schema-document`
*   `chapter-document`
*   `key-definition-set`
*   `kb-definition-map`
*   `how-to-guide`
*   `tutorial-document`
*   `troubleshooting-guide`
*   `reference-document`
*   `architecture-overview`
*   `design-specification`
*   `meeting-notes`
*   `report-document`
*   `process-definition`
*   `role-definition`
*   `service-definition`
*   `api-specification`
*   `data-model-definition`
*   `security-standard`
*   `compliance-guideline`

### Other Controlled Vocabularies

*   **`tags` (categories and specific tags):** See `[[MT-REGISTRY-TAG-GLOSSARY]]`.
*   **`kb-id`:** See `[[MT-REGISTRY-TAG-GLOSSARY]]` or a dedicated knowledge base registry.
*   **`criticality`:** See `[[MT-REGISTRY-TAG-GLOSSARY]]`.
*   **`lifecycle_gatekeeper`:** See `[[MT-REGISTRY-TAG-GLOSSARY]]`.
*   **`primary_domain`:** Values must exist in `[[domain_codes.yaml]]`.
*   **`sub_domain`:** Values must exist in `[[subdomain_registry.yaml]]` for the specified `primary_domain`.

## Relationship to Filename

For documents that have a `standard_id` (e.g., those with `info-type: standard-definition`), the filename (excluding the `.md` extension) SHOULD exactly match the value of the `standard_id` key. This promotes consistency and predictability in locating standard documents. For example, a document with `standard_id: MT-SCHEMA-FRONTMATTER` should be named `MT-SCHEMA-FRONTMATTER.md`.
