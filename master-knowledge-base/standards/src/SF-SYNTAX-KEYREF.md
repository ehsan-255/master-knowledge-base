---
title: "Standard: Key-Based Referencing Syntax"
standard_id: "SF-SYNTAX-KEYREF"
aliases: ["Keyref Syntax", "Key-Based Referencing"]
tags:
  - status/draft
  - content-type/standard-definition
  - topic/syntax
  - topic/keyref
  - primary_domain/SF
  - sub_domain/SYNTAX
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "Defines the Markdown-compatible syntax for key-based referencing (keyrefs) used for dynamic content insertion."
related-standards: ["MT-KEYREF-MANAGEMENT"] # Assuming U-KEYREF-MANAGEMENT-001 will become MT-KEYREF-MANAGEMENT
version: "1.0.0"
date-created: "2025-05-29T13:24:53Z" # Placeholder
date-modified: "2025-05-29T13:24:53Z" # Placeholder
primary_domain: "SF"
sub_domain: "SYNTAX"
scope_application: "Applies to all knowledge base documents where key-based referencing is used for content reuse and consistency."
criticality: "P2-Medium"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Content consistency", "Maintainability", "Automation (keyref resolution)", "Authoring efficiency"]
change_log_url: "./SF-SYNTAX-KEYREF-changelog.md"
---

# Standard: Key-Based Referencing Syntax (SF-SYNTAX-KEYREF)

## 1. Introduction

This document defines the universal standard for the syntax of key-based referencing (keyref) placeholders within content. These placeholders allow for indirect referencing of values defined centrally, promoting consistency and maintainability.

## 2. Rule/Guideline Statement(s)

| Rule ID | Statement                                                                                                                                                                                             | Notes                                                                                                                                                                                                                            |
| :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.1     | Keyref placeholders MUST use double curly braces `{{ }}` enclosing the prefix `key.` followed by the key name (e.g., `key.yourKeyName`). Key names are case-sensitive as defined in [[UA-KEYDEFS-GLOBAL]]. The `key.` prefix is mandatory. | This syntax is chosen for its commonality in templating languages and to minimize conflict with standard Markdown or HTML. The `key.` prefix provides a clear namespace.                                                              |
| 2.2     | Key names within the placeholder SHOULD follow camelCase convention (e.g., `officialCompanyName`) for readability and consistency, though the ultimate source of truth for key names is [[UA-KEYDEFS-GLOBAL]]. | While camelCase is recommended for new key creation, the resolver MUST use the exact case as defined in `[[UA-KEYDEFS-GLOBAL]]`.                                                                                                  |
| 2.3     | Whitespace within the curly braces, around the key name or `key.` prefix, is NOT PERMITTED.                                                                                                              | Example (Incorrect): `{{ key.yourKeyName }}` or `{{key. yourKeyName}}`. <br> Example (Correct): `{{key.yourKeyName}}`. <br> This ensures simpler parsing logic for the resolver script.                                                   |

## 3. Importance of Keyref Syntax

*   **Consistency:** Ensures all authors use the same syntax for referencing centrally managed values.
*   **Maintainability:** When a value changes, it only needs to be updated in the central definitions file ([[UA-KEYDEFS-GLOBAL]]), and all keyrefs will reflect the change upon rendering.
*   **Automation:** A clear and strict syntax allows for reliable automated processing (e.g., by a resolver script) to replace placeholders with their actual values.
*   **Readability:** The `{{key.name}}` format is generally readable in raw Markdown and clearly indicates a placeholder.

## 4. Cross-References
- [[MT-KEYREF-MANAGEMENT]] - Defines the policy and process for managing the central key definition file.
- [[UA-KEYDEFS-GLOBAL]] - The actual file where key-value pairs are stored (this standard will define its structure and rules).

---
*This standard (SF-SYNTAX-KEYREF) is based on the rules previously defined in U-KEYREF-SYNTAX-001.*
