---
title: 'Standard: Key-Based Referencing Management (U-KEYREF-MANAGEMENT-001)'
tags:
  - standards-kb/universal
  - content-type/standard-document
  - utility-standards
  - keyref
  - governance
  - status/draft
  - kb-id/standards
date-created: 2025-05-19
date-modified: 2025-05-22
version: '0.1.1'
info-type: standard-document
primary-topic: 'Defines the management process for key-based referencing (keyrefs) in KB documents.'
related-standards:
  - U-KEYREF-SYNTAX-001
  - M-SYNTAX-YAML-001
aliases: [Keyref Management Standard]
---

# Standard: Key-Based Referencing Management (U-KEYREF-MANAGEMENT-001)

This document defines the universal standard for how and where key-based referencing (keyref) definitions are stored and managed. This ensures a single source of truth for all reusable key values.

## Table of Contents
- [[#Standard: Key Definition Storage and Structure (U-KEYREF-MANAGEMENT-001)]]

## Standard: Key Definition Storage and Structure (U-KEYREF-MANAGEMENT-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-KEYREF-MANAGEMENT-001`                 |
| Standard Name   | Key Definition Storage and Structure  |
| Standard Category | Utility Standards & Governance        |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | All globally reusable key definitions MUST be stored in a single, dedicated file named `_key_definitions.md` located in the root of the `master-knowledge-base` directory. | `master-knowledge-base/_key_definitions.md`                  | Centralizes all key definitions for easy management and script access.       |
| 1.2    | Key definitions within `_key_definitions.md` MUST be stored within the YAML frontmatter of this file, under a top-level dictionary key named `keys:`. | See Illustrative Example below.                              | Adheres to `M-SYNTAX-YAML-001`.                                              |
| 1.3    | Each key under `keys:` MUST be a string representing the key name (e.g., `productName`). Key names SHOULD follow camelCase convention. Key names are case-sensitive. | `productName: "Our Awesome App"`                             | Values can be strings, numbers, or booleans. Complex objects or lists are discouraged for simple keyrefs. |
| 1.4    | The Markdown body of `_key_definitions.md` SHOULD be used to document the purpose, scope, and usage guidelines for the defined keys, or to categorize them. | `# Key Definitions Documentation\n## Product Keys\n- productName: Used for...` | Provides human-readable context for the keys.                              |
| 1.5    | Changes to `_key_definitions.md` (adding, modifying, or removing keys) MUST trigger a re-run of the "Resolver Script" to update all "rendered" content. | N/A                                                          | Ensures consistency between source and rendered views.                       |

**Illustrative Examples (Overall):**

Content of `_key_definitions.md` YAML frontmatter:
```yaml
---
date-created: 2025-05-19
date-modified: 2025-05-20
info-type: key_definition_set
version: '0.1' # Version of this key set
keys:
  productName: "Our Awesome App"
  productVersion: "3.0"
  supportEmailAddress: "support@example.com"
  officialCompanyName: "Innovatech Solutions Ltd."
  defaultStatusDraft: "status/draft"
---
```

**Cross-References to Other Standard IDs:** [[U-KEYREF-SYNTAX-001|U-KEYREF-SYNTAX-001]], [[M-SYNTAX-YAML-001|M-SYNTAX-YAML-001]] 