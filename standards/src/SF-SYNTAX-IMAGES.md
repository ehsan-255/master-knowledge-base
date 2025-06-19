---
title: 'Standard: Image Syntax'
standard_id: SF-SYNTAX-IMAGES
aliases:
- Image Syntax
- Image References
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
primary-topic: Image Syntax
related-standards:
- SF-ACCESSIBILITY-IMAGE-ALT-TEXT
- SF-SYNTAX-LINKS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines image syntax for all Markdown documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Visual content
- Accessibility
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Image Syntax (SF-SYNTAX-IMAGES)

## 1. Standard Statement

This standard **MANDATES** image syntax for all Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Standard Image Syntax
**MUST** use exclamation mark followed by square brackets and parentheses.

**Syntax:** `![alt text](image-url "optional title")`

### Rule 2.2: Alt Text Required
Alt text **MUST** be meaningful and descriptive. **MUST** follow [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]].

### Rule 2.3: Relative Paths Preferred
**SHOULD** use relative paths for repository images.

**Syntax:** `![Description](./images/filename.png)`

### Rule 2.4: Absolute URLs Permitted
External images **MAY** use absolute URLs.

**Syntax:** `![Description](https://example.com/image.png)`

## 3. Examples

```markdown
![Process flow diagram showing three stages](./images/process-flow.png "Process Flow")
![Company logo](https://example.com/logo.png)
![Chart displaying quarterly results](../assets/q4-chart.svg "Q4 Results")
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 