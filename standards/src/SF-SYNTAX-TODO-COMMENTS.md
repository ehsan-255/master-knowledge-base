---
title: 'Standard: TODO Comment Syntax'
standard_id: SF-SYNTAX-TODO-COMMENTS
aliases:
- TODO Comment Syntax
- Task Comments
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p3-low
- kb-id/standards
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: TODO Comment Syntax
related-standards:
- SF-SYNTAX-HEADINGS
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines TODO comment syntax for task tracking.
criticality: P3-Low
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Task tracking
- Content workflow
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: TODO Comment Syntax (SF-SYNTAX-TODO-COMMENTS)

## 1. Standard Statement

This standard **MANDATES** HTML comment syntax for TODO items in Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: HTML Comment Delimiters
**MUST** use `<!--` and `-->` delimiters.

**Syntax:** `<!-- TODO: description -->`

### Rule 2.2: TODO Keyword
**MUST** begin with uppercase `TODO:` immediately after opening delimiter.

### Rule 2.3: Own Line Placement
**MUST** place TODO comments on their own line between content blocks.

### Rule 2.4: Optional Date Format
Dates **MUST** use `YYYY-MM-DD` format if included.

**Syntax:** `<!-- TODO: 2024-05-30 description -->`

### Rule 2.5: Optional Assignee Format
Assignees **MUST** use `@username` format if specified.

**Syntax:** `<!-- TODO: @user description -->`

## 3. Examples

```markdown
This is content.

<!-- TODO: Add diagram here -->
<!-- TODO: 2024-05-30 Review section -->
<!-- TODO: @reviewer Verify accuracy -->

More content follows.
```

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 