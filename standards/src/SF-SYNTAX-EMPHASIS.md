---
title: 'Standard: Emphasis Syntax'
standard_id: SF-SYNTAX-EMPHASIS
aliases:
- Emphasis Syntax
- Bold and Italic
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
primary-topic: Emphasis Syntax
related-standards:
- SF-SYNTAX-HEADINGS
- SF-SYNTAX-LINKS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines emphasis syntax for all Markdown documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Text formatting
- Content emphasis
---
# Standard: Emphasis Syntax (SF-SYNTAX-EMPHASIS)

## 1. Standard Statement

This standard **MANDATES** asterisk-based emphasis syntax for all Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Italic Emphasis
**MUST** use single asterisks. Underscores are **PROHIBITED**.

**Syntax:** `*italic text*`

### Rule 2.2: Bold Emphasis
**MUST** use double asterisks. Underscores are **PROHIBITED**.

**Syntax:** `**bold text**`

### Rule 2.3: Combined Emphasis
**MUST** use triple asterisks for bold and italic.

**Syntax:** `***bold and italic text***`

## 3. Examples

```markdown
This is *italic* text.
This is **bold** text.
This is ***bold and italic*** text.
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 