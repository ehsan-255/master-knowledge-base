---
title: 'Standard: Link Syntax'
standard_id: SF-SYNTAX-LINKS
aliases:
- Link Syntax
- Internal and External Links
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
primary-topic: Link Syntax
related-standards:
- SF-SYNTAX-HEADINGS
- SF-SYNTAX-EMPHASIS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines link syntax for all Markdown documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Navigation
- Cross-references
---
# Standard: Link Syntax (SF-SYNTAX-LINKS)

## 1. Standard Statement

This standard **MANDATES** link syntax for all Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: External Links
**MUST** use inline format for external URLs.

**Syntax:** `[Display Text](URL)`

### Rule 2.2: Internal Standard Links
**MUST** use standard ID format for documents with `standard_id`.

**Syntax:** `[[STANDARD_ID]]` or `[[STANDARD_ID|Display Text]]`

### Rule 2.3: Section Links
**MUST** append heading text with `#` for section references.

**Syntax:** `[[STANDARD_ID#Heading Text]]`

### Rule 2.4: Non-Standard Internal Links
**MUST** use relative paths from repository root.

**Syntax:** `[Link Text](./path/to/document.md)`

### Rule 2.5: Autolinks
**MUST** enclose raw URLs in angle brackets.

**Syntax:** `<https://example.com>`

### Rule 2.6: Descriptive Text Required
Link text **MUST** describe destination. Generic text is **PROHIBITED**.

## 3. Examples

```markdown
External: [W3C Website](https://www.w3.org/)
Standard: [[SF-SYNTAX-HEADINGS]]
Section: [[SF-SYNTAX-HEADINGS#Mandatory Rules]]
Internal: [Guidelines](./active-project/project-guidelines/main-project-guidelines.md)
Autolink: <https://example.com>
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 