---
title: "Standard: Key-Based Referencing Syntax (U-KEYREF-SYNTAX-001)"
tags:
  - standards-kb/universal
  - content-type/standard-document
  - utility-standards
  - keyref
  - syntax-rules
  - status/draft
  - kb-id/standards
date-created: 2025-05-19
date-modified: 2025-05-22
version: 0.1.1
info-type: standard-document
primary-topic: 'Defines the syntax for key-based referencing (keyrefs) in KB documents.'
related-standards:
  - U-KEYREF-MANAGEMENT-001
aliases:
  - Keyref Syntax Standard
---

# Standard: Key-Based Referencing Syntax (U-KEYREF-SYNTAX-001)

This document defines the universal standard for the syntax of key-based referencing (keyref) placeholders within content. These placeholders allow for indirect referencing of values defined centrally, promoting consistency and maintainability.

## Table of Contents
- [[#Standard: Keyref Placeholder Syntax (U-KEYREF-SYNTAX-001)]]

## Standard: Keyref Placeholder Syntax (U-KEYREF-SYNTAX-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-KEYREF-SYNTAX-001`                 |
| Standard Name   | Keyref Placeholder Syntax             |
| Standard Category | Utility Standards & Content Formatting |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Keyref placeholders MUST use double curly braces `{{ }}` enclosing the prefix `key.` followed by the key name (e.g., `key.yourKeyName`). Key names are case-sensitive as defined in `_key_definitions.md`. | `{{key.productName}}`, `{{key.supportEmail}}`             | The `key.` prefix is mandatory to distinguish keyrefs from other potential templating syntaxes. |
| 1.2    | Key names within the placeholder SHOULD follow camelCase convention (e.g., `officialCompanyName`) for readability and consistency, though the ultimate source of truth for key names is `_key_definitions.md`. | `{{key.officialCompanyName}}`                               | Consistency in key naming within `_key_definitions.md` is paramount.         |
| 1.3    | Whitespace within the curly braces, around the key name or `key.` prefix, is NOT PERMITTED.                                                        | Correct: `{{key.productName}}`. Incorrect: `{{ key.productName }}` | Ensures unambiguous parsing by resolution scripts.                           |

**Cross-References to Other Standard IDs:** [[U-KEYREF-MANAGEMENT-001|U-KEYREF-MANAGEMENT-001]] 