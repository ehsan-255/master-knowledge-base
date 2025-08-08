---
title: 'Standard: Emphasis Syntax'
standard_id: SF-SYNTAX-EMPHASIS
aliases:
- Emphasis
- Bold
- Italic
- Text Formatting
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Emphasis Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-18T02:10:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the mandatory Markdown syntax for emphasis (italics, bold, combined emphasis).
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Text formatting
- Visual emphasis
- Content readability
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Emphasis (SF-SYNTAX-EMPHASIS)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for creating emphasis through italic, bold, and combined formatting in all Knowledge Base documents.

## 2. Core Emphasis Syntax Rules

### Rule 2.1: Italic Emphasis
Italic emphasis **MUST** be created exclusively using single asterisks (`*`).
*   **Mandatory Syntax:** `*italic text*`
*   **Prohibited:** Single underscores (`_italic text_`)
*   **Example:** `This is *important* information.`

### Rule 2.2: Bold Emphasis
Bold emphasis **MUST** be created exclusively using double asterisks (`**`).
*   **Mandatory Syntax:** `**bold text**`
*   **Prohibited:** Double underscores (`__bold text__`)
*   **Example:** `This is **critical** information.`

### Rule 2.3: Combined Bold and Italic Emphasis
Combined bold and italic emphasis **MUST** be created using triple asterisks (`***`).
*   **Mandatory Syntax:** `***bold and italic text***`
*   **Prohibited:** Any combination of underscores and asterisks
*   **Example:** `This is ***extremely important*** information.`

## 3. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository. Adherence is **MANDATORY** for all content creators, automated systems, and tooling.

## 4. Cross-References
*   [[CS-POLICY-TONE-LANGUAGE]]

---
*This standard (SF-SYNTAX-EMPHASIS) establishes strict, singular mandates for emphasis syntax, ensuring universal consistency for the Knowledge Base.*
