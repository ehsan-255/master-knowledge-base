---
title: 'Standard: Definition List Syntax'
standard_id: SF-SYNTAX-DEFINITION-LISTS
aliases:
- Definition List Syntax
- Glossary Lists
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
primary-topic: Definition List Syntax
related-standards:
- SF-SYNTAX-LISTS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines definition list syntax for all Markdown documents.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Terminology management
- Glossary content
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Definition List Syntax (SF-SYNTAX-DEFINITION-LISTS)

## 1. Standard Statement

This standard **MANDATES** definition list syntax for glossary and terminology content in Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Term Declaration
Terms **MUST** be placed on a line by themselves.

### Rule 2.2: Definition Format
Definitions **MUST** start on new line, begin with colon (`:`), and be indented four spaces.

**Syntax:** `:    Definition text`

### Rule 2.3: Multiple Definitions
Multiple definitions for one term **MUST** each start with colon and four spaces.

## 3. Examples

```markdown
Apple
:    A round fruit, typically red, green, or yellow.
:    Keeps the doctor away if consumed daily.

Banana
:    An elongated, curved fruit with yellow skin when ripe.

Git
:    A distributed version control system.
:    A command-line tool for tracking changes in source code.
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 