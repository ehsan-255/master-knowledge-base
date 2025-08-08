---

title: 'Standard: Table Syntax'
standard_id: SF-SYNTAX-TABLES
aliases:
- Table Syntax
- Data Tables
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
primary-topic: Table Syntax
related-standards:
- SF-SYNTAX-HEADINGS
- SF-SYNTAX-EMPHASIS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines table syntax for all Markdown documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Data presentation
- Content structure
---
# Standard: Table Syntax (SF-SYNTAX-TABLES)

## 1. Standard Statement

This standard **MANDATES** table syntax for all Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Pipe Separators
**MUST** use pipe (`|`) characters to separate columns.

### Rule 2.2: Header Separator
**MUST** include header separator row with hyphens (`-`).

### Rule 2.3: Leading and Trailing Pipes
**MUST** include leading and trailing pipes on every row.

### Rule 2.4: Column Alignment
**MUST** specify alignment in separator row using colons:
- Left: `|----------|` (default)
- Center: `|:--------:|`
- Right: `|---------:|`

## 3. Examples

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|:--------:|---------:|
| Left     | Center   | Right    |
| Data     | More     | Values   |
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 