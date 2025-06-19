---
title: 'Standard: List Syntax'
standard_id: SF-SYNTAX-LISTS
aliases:
- List Syntax
- Ordered and Unordered Lists
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: List Syntax
related-standards:
- SF-SYNTAX-HEADINGS
- SF-SYNTAX-EMPHASIS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines list syntax for all Markdown documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content organization
- Document hierarchy
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: List Syntax (SF-SYNTAX-LISTS)

## 1. Standard Statement

This standard **MANDATES** list syntax for all Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Unordered Lists
**MUST** use hyphens (`-`) as the list marker. Asterisks and plus signs are **PROHIBITED**.

**Syntax:** `- List item`

### Rule 2.2: Ordered Lists
**MUST** use numbers followed by periods.

**Syntax:** `1. List item`

### Rule 2.3: Nested Lists
**MUST** use exactly four spaces for each indentation level.

### Rule 2.4: Mixed Nesting
Ordered and unordered lists **MAY** be mixed in nested structures.

## 3. Examples

```markdown
- First item
- Second item
    - Nested item (4 spaces)
        - Double nested (8 spaces)
- Third item

1. First step
2. Second step
    - Nested unordered
    - Another nested
3. Third step
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 