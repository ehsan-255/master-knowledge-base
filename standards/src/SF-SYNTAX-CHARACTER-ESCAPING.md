---
title: 'Standard: Character Escaping Syntax'
standard_id: SF-SYNTAX-CHARACTER-ESCAPING
aliases:
- Character Escaping
- Literal Characters
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
primary-topic: Character Escaping Syntax
related-standards:
- SF-SYNTAX-EMPHASIS
- SF-SYNTAX-LINKS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines character escaping for literal display.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Character handling
- Literal text display
---
# Standard: Character Escaping Syntax (SF-SYNTAX-CHARACTER-ESCAPING)

## 1. Standard Statement

This standard **MANDATES** backslash escaping for literal character display in Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Backslash Escaping
**MUST** use backslash (`\`) immediately before special characters for literal display.

**Syntax:** `\character`

### Rule 2.2: Common Escaped Characters
The following characters **MUST** be escaped when literal display is required:

- `\*` (asterisk)
- `\_` (underscore)  
- `\#` (hash at line start)
- `\[` `\]` (square brackets)
- `\(` `\)` (parentheses)
- `\{` `\}` (curly braces)
- `\\` (backslash)
- `` \` `` (backtick)

## 3. Examples

```markdown
\*not italic\* displays: *not italic*
\#not a heading displays: #not a heading
1\. not a list displays: 1. not a list
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 