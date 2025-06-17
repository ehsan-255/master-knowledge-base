---
title: 'Standard: Key Reference Syntax'
standard_id: SF-SYNTAX-KEYREF
aliases:
- Key References
- Keyref Syntax
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/links
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Key Reference Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: LINKS
scope_application: Defines the syntax for key references in knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Key references
- Content linking
- Variable substitution
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Key-Based Referencing Syntax (SF-SYNTAX-KEYREF)

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax for key-based referencing (keyref) placeholders within all Knowledge Base content. These placeholders **MUST** allow for indirect referencing of centrally defined values, promoting consistency and maintainability. This document is the **single authoritative source** for keyref syntax.

## 2. Core Keyref Syntax Rules

### Rule 2.1: Placeholder Format
Keyref placeholders **MUST** use double curly braces `{{ }}` enclosing the mandatory prefix `key.` followed by the key name (e.g., `key.yourKeyName`). Key names are case-sensitive as defined in [[UA-KEYDEFS-GLOBAL]].
*   **Mandatory Syntax:** `{{key.yourKeyName}}`
*   **Rationale:** This syntax is chosen for its commonality in templating languages and to minimize conflict with standard Markdown or HTML. The `key.` prefix provides a clear namespace.

### Rule 2.2: Key Naming Convention
Key names within the placeholder **MUST** follow camelCase convention (e.g., `officialCompanyName`). The ultimate source of truth for key names is [[UA-KEYDEFS-GLOBAL]].
*   **Rationale:** Enforces a consistent style for all key names, simplifying management and improving readability.

### Rule 2.3: Whitespace
Whitespace within the curly braces, around the key name or `key.` prefix, is **PROHIBITED**.
*   **Correct Example:** `{{key.yourKeyName}}`
*   **Prohibited Examples:** `{{ key.yourKeyName }}` or `{{key. yourKeyName}}`
*   **Rationale:** Ensures simpler parsing logic for the resolver script and consistent machine readability.

## 3. Importance of Strict Keyref Syntax

*   **Consistency:** Ensures all authors use the same syntax for referencing centrally managed values.
*   **Maintainability:** Centralized value definition ([[UA-KEYDEFS-GLOBAL]]) means changes update all references automatically.
*   **Automation:** Strict syntax allows for reliable automated processing (e.g., by a resolver script) to replace placeholders.
*   **Readability:** The `{{key.name}}` format is clear and indicates a placeholder in raw Markdown.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where key-based references are used. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 5. Cross-References
*   [[MT-KEYREF-MANAGEMENT]]
*   [[UA-KEYDEFS-GLOBAL]]

---
*This standard (SF-SYNTAX-KEYREF) has been revised to mandate a strict, singular syntax for key-based referencing, replacing previous guidelines with clear requirements.*
