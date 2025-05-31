---
title: 'Standard: Table of Contents Syntax'
standard_id: SF-TOC-SYNTAX
aliases:
- TOC Syntax
- Table of Contents
tags:
- status/draft
- criticality/p2-medium
- content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Table of Contents Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating table of contents in knowledge base documents.
criticality: p2-medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Navigation
- Document structure
- Content organization
change_log_url: ./SF-TOC-SYNTAX-changelog.md
---
# Standard: Table of Contents (ToC) Markdown Syntax (SF-TOC-SYNTAX)

This standard defines the mandatory Markdown syntax for Tables of Contents (ToCs) within knowledge base documents. Adherence to this syntax ensures consistency, proper rendering, and compatibility with potential future tooling.

## 1. ToC Syntax Requirements

### Rule 1.1: Unordered List Format
A Table of Contents MUST be constructed as a Markdown unordered list.
*   Each list item represents a heading in the document.
*   Nested lists SHOULD be used to represent the heading hierarchy (e.g., H3s under H2s).

### Rule 1.2: Link to Headings
Each list item in the ToC MUST be a Markdown link pointing to the corresponding heading anchor within the document.
*   **Link Text:** The link text SHOULD accurately reflect the heading title.
*   **Link Destination (Anchor):** The link destination MUST be the auto-generated anchor for that heading. Most Markdown processors generate anchors by:
    1.  Converting the heading text to lowercase.
    2.  Replacing spaces with hyphens (`-`).
    3.  Removing or converting special characters (behavior can vary, so testing is advised).
    *   **Example:** A heading `## My Section Title` would typically have an anchor `#my-section-title`.

### Rule 1.3: Manual vs. Automated ToCs
*   **Manual Creation:** If a ToC is created manually, it MUST adhere to the syntax specified in Rules 1.1 and 1.2.
*   **Automated Generation:** If a tool or plugin is used to generate the ToC (as recommended in [[CS-TOC-POLICY]]), the output of that tool MUST conform to this Markdown syntax standard.

## 2. Illustrative Example

For a document with the following heading structure:

```markdown
# Document Title

## Section 1: Introduction
### Subsection 1.1: Background
### Subsection 1.2: Scope

## Section 2: Main Content
### Subsection 2.1: Key Concepts
#### Detail A
```

The corresponding ToC should be structured as follows:

```markdown
## Table of Contents
- [Section 1: Introduction](#section-1-introduction)
  - [Subsection 1.1: Background](#subsection-11-background)
  - [Subsection 1.2: Scope](#subsection-12-scope)
- [Section 2: Main Content](#section-2-main-content)
  - [Subsection 2.1: Key Concepts](#subsection-21-key-concepts)
```
*(Note: The depth of ToC (e.g., including H3s, H4s) is governed by [[CS-TOC-POLICY]]. This standard focuses on the syntax if they are included.)*

## 3. Verification
Authors should verify that ToC links correctly navigate to the intended sections. This is especially important for manually created ToCs or when heading titles are changed.

## 4. Cross-References
- [[CS-TOC-POLICY]] - Policy regarding ToC mandate, content depth, and generation.
- [[AS-STRUCTURE-DOC-CHAPTER]] - Defines the placement of ToCs within chapter documents.
- [[SF-LINKS-INTERNAL-SYNTAX]] - Governs general internal link syntax.
- [[SF-SYNTAX-HEADINGS]] - Governs heading syntax, which impacts anchor generation.

---
*This standard (SF-TOC-SYNTAX) formalizes the Markdown structure for Tables of Contents, supporting policies outlined in CS-TOC-POLICY and structural requirements in AS-STRUCTURE-DOC-CHAPTER. It derives from examples and implicit requirements in U-STRUC-002.*
