---
title: 'Standard: Heading Syntax'
standard_id: SF-SYNTAX-HEADINGS
aliases:
- Heading Syntax
- ATX Headings
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
primary-topic: Heading Syntax
related-standards:
- SF-SYNTAX-EMPHASIS
- SF-SYNTAX-LINKS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines heading syntax for all Markdown documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Document structure
- Content hierarchy
---
# Standard: Heading Syntax (SF-SYNTAX-HEADINGS)

## 1. Standard Statement

This standard **MANDATES** ATX-style heading syntax for all Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: ATX Style Only
Headings **MUST** use hash symbols (`#`). Setext style is **PROHIBITED**.

**Syntax:** `# Heading Text`

### Rule 2.2: Single Space Required
**MUST** include exactly one space after hash symbols.
- **Correct:** `# Heading`  
- **Prohibited:** `#Heading`, `#  Heading`

### Rule 2.3: Blank Line Separation
**MUST** surround headings with blank lines.
- **Exception:** H1 after frontmatter requires no preceding blank line
- **Exception:** Final heading requires no trailing blank line

### Rule 2.4: Single H1 Per Document
Each document **MUST** contain exactly one H1 heading.

### Rule 2.5: Sequential Hierarchy
Heading levels **MUST** follow sequential order without skipping.
- **Correct:** H1 → H2 → H3
- **Prohibited:** H1 → H3

## 3. Example

```markdown
# Document Title

## Main Section

### Subsection

### Another Subsection

## Second Main Section
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 