---
title: 'Standard: Blockquote Syntax'
standard_id: SF-SYNTAX-BLOCKQUOTES
aliases:
- Blockquote Syntax
- Quote Formatting
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
primary-topic: Blockquote Syntax
related-standards:
- SF-SYNTAX-HEADINGS
- SF-SYNTAX-EMPHASIS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines blockquote syntax for all Markdown documents.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Quote formatting
- Content attribution
---
# Standard: Blockquote Syntax (SF-SYNTAX-BLOCKQUOTES)

## 1. Standard Statement

This standard **MANDATES** blockquote syntax for all Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Greater-Than Marker
**MUST** prefix each line with `> ` (greater-than plus space).

**Syntax:** `> Quote text`

### Rule 2.2: Nested Blockquotes
**MUST** use additional `>` symbols for each nesting level.

**Syntax:** `> > Nested quote`

### Rule 2.3: Blank Line Separation
**MUST** surround blockquotes with blank lines.

## 3. Examples

```markdown
> This is a blockquote.
> It spans multiple lines.

> > This is nested.
> > Second nested line.
>
> Back to first level.
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 