---

title: 'Standard: Key Reference Syntax'
standard_id: SF-SYNTAX-KEY-REFERENCES
aliases:
- Key Reference Syntax
- Variable References
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p2-medium
- kb-id/standards
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Key Reference Syntax
related-standards:
- MT-KEYREF-MANAGEMENT
- UA-KEYDEFS-GLOBAL
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines key reference syntax for variable substitution.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content management
- Variable substitution
---
# Standard: Key Reference Syntax (SF-SYNTAX-KEY-REFERENCES)

## 1. Standard Statement

This standard **MANDATES** key reference syntax for variable substitution in Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Double Curly Braces
**MUST** use `{{key.keyName}}` format with mandatory `key.` prefix.

**Syntax:** `{{key.keyName}}`

### Rule 2.2: CamelCase Naming
Key names **MUST** follow camelCase convention.

### Rule 2.3: No Whitespace
Whitespace within braces is **PROHIBITED**.

**Correct:** `{{key.companyName}}`
**Prohibited:** `{{ key.companyName }}`, `{{key. companyName}}`

### Rule 2.4: Key Definition Source
All keys **MUST** be defined in [[UA-KEYDEFS-GLOBAL]].

## 3. Examples

```markdown
Welcome to {{key.companyName}}.
Project started on {{key.projectStartDate}}.
Contact {{key.supportEmail}} for help.
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 