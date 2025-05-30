---
title: 'Standard: Metadata Value Validation (U-VALIDATION-METADATA-001) - DEPRECATED'
tags:
  - standards-kb/universal
  - utility-standards
  - metadata
  - validation
  - data-integrity
  - status/deprecated # Changed from status/draft
  - kb-id/standards
  - content-type/standard-document
date-created: "2025-05-19T00:00:00Z" # Standardized
date-modified: "2025-05-30T00:00:00Z" # Deprecation date
version: '0.1.2'
info-type: standard-document
primary-topic: Defines rules for validating the semantic values of specific metadata fields
related-standards:
  - QM-VALIDATION-METADATA # Points to new standard
aliases: [Metadata Validation Standard, YAML Value Validation]
---

> [!WARNING] DEPRECATED: This Standard is No Longer Active
> **Reason for Deprecation:** This standard has been superseded by [[QM-VALIDATION-METADATA]].
> Please refer to the new standard for current guidelines. This document is retained for historical purposes only.

# Standard: Metadata Value Validation (U-VALIDATION-METADATA-001)

This document defines standards for validating the *semantic values* of specific YAML frontmatter metadata fields, beyond basic syntax checks. This ensures data integrity, consistency, and reliability for querying and automated processing.

## Table of Contents
- [[#Standard: Rules for Validating Metadata Field Values (U-VALIDATION-METADATA-001)]]
- [[#Specific Field Validation Rules]]

## Standard: Rules for Validating Metadata Field Values (U-VALIDATION-METADATA-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-VALIDATION-METADATA-001`           |
| Standard Name   | Metadata Value Validation             |
| Standard Category | Metadata & Data Integrity             |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Validation of metadata values MUST be performed by automated scripts (e.g., linters, pre-commit hooks, dedicated validation scripts) or Dataview queries where feasible. | A Python script checks `kb-id` values against a known list.  | Manual checking is insufficient for large KBs.                               |
| 1.2    | For metadata fields intended to reference other entities within the KB system (e.g., `kb-id`, `related-standards`, links in `reltable`), the referenced entity ID or path MUST exist and be valid. | `related-standards: [U-ARCH-001]` (U-ARCH-001.md must exist) | Prevents broken semantic links in metadata.                                  |
| 1.3    | For metadata fields with a controlled vocabulary (e.g., `status`, `content-type`, `audience`, `platform`), values MUST be one of the officially defined values in the relevant standard (e.g., `U-TAG-001`, `U-PROFILING-ATTRIBUTES-001`). | `status: draft` (Correct, if 'draft' is defined in U-TAG-001) | Enforces use of standardized terminology.                                    |
| 1.4    | Date fields (e.g., `date-created`, `date-modified`) MUST be in `YYYY-MM-DD` format.                                                              | `date-created: 2025-05-19`                                   | Ensures consistent date parsing.                                             |
| 1.5    | Version fields (e.g., `version`) SHOULD follow semantic versioning (MAJOR.MINOR.PATCH, e.g., `1.0.0`, `0.1.2`) where applicable. Simple `0.1` is acceptable for initial drafts. | `version: 1.2.3`                                             | Provides clarity on content maturity and change magnitude.                   |

## Specific Field Validation Rules

| Key                | Expected Data Type         | Controlled Vocabulary Source                | Format Constraints / Validation Rules                                                                                 |
|--------------------|--------------------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| title              | String                   | N/A                                        | Must match H1 heading. Quoted if special YAML chars.                                                                |
| aliases            | String or List of Strings| N/A                                        | If no aliases, must be 'N/A'. Otherwise, concise list.                                                              |
| tags               | List of Strings          | tag-glossary-definition.md                  | Must include at least one of each: kb-id/*, content-type/*, status/*, topic/*. All tags must be kebab-case.          |
| kb-id              | String                   | tag-glossary-definition.md                  | Must match a kb-id/* tag. Use 'global' for vault-level files.                                                       |
| info-type          | String                   | U-METADATA-FRONTMATTER-RULES-001           | Must be kebab-case. Must match controlled vocabulary for info-type.                                                  |
| primary-topic      | String                   | N/A                                        | Concise 1-2 sentence description.                                                                                    |
| related-standards  | String or List of Strings| N/A                                        | If no related standards, must be 'N/A'. Otherwise, list of valid Standard IDs.                                       |
| version            | String                   | N/A                                        | Must be quoted. Semantic versioning (e.g., '1.0.0').                                                                |
| date-created       | String                   | N/A                                        | Must be YYYY-MM-DD. Should not change after creation.                                                                |
| date-modified      | String                   | N/A                                        | Must be YYYY-MM-DD. Must update on substantive change.                                                               |

- Existence/Referential Integrity: Each ID in related-standards must correspond to an existing standard file or section. All tags must be defined in tag-glossary-definition.md.

**Cross-References to Other Standard IDs:** [[M-SYNTAX-YAML-001|M-SYNTAX-YAML-001]], [[U-TAG-001|U-TAG-001]], [[../../_backup/master-knowledge-base-backup/standards/U-PROFILING-ATTRIBUTES-001|U-PROFILING-ATTRIBUTES-001]] 