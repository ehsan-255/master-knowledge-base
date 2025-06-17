---
title: 'Standard: Table of Contents Syntax'
standard_id: SF-TOC-SYNTAX
aliases:
- TOC Syntax
- Table of Contents
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p2-medium
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Table of Contents Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating table of contents in knowledge
  base documents.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Navigation
- Document structure
- Content organization
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Table of Contents (ToC) Markdown Syntax (SF-TOC-SYNTAX)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for Tables of Contents (ToCs) within Knowledge Base documents. Adherence to this syntax is **CRITICAL** for ensuring universal consistency, proper rendering, and guaranteed compatibility with all automated tooling. This document is the **single authoritative source** for ToC structural formation.

## 2. Core ToC Syntax Rules

### Rule 2.1: Unordered List Format
A Table of Contents **MUST** be constructed as a Markdown unordered list, where each list item represents a document heading.
*   Nested lists **MUST** represent heading hierarchy (e.g., H3s under H2s, H4s under H3s).
*   **Example:**
    ```markdown
    - [Section 1: Introduction](#section-1-introduction)
      - [Subsection 1.1: Background](#subsection-11-background)
      - [Subsection 1.2: Scope](#subsection-12-scope)
    - [Section 2: Main Content](#section-2-main-content)
    ```
*   **Rationale:** Ensures standardized, hierarchical structure that is both human-readable and machine-parsable.

### Rule 2.2: Link to Headings (Mandatory Internal Links)
Each ToC list item **MUST** be an internal Markdown link pointing to the corresponding heading anchor within the document.
*   **Link Text:** The link text **MUST** precisely reflect the exact heading title.
*   **Link Destination (Anchor):** The link destination **MUST** be the auto-generated anchor for that heading. Standard Knowledge Base tooling **MUST** generate anchors by converting heading text to lowercase, replacing spaces with hyphens (`-`), and removing special characters (except hyphens).
    *   **Example:** A heading `## My Section Title` **MUST** have an anchor `#my-section-title`.
    *   **Example:** A heading `### What is a K.B.?` **MUST** have an anchor `#what-is-a-kb`.
*   **Rationale:** Guarantees functional navigation, enhances accessibility, and ensures reliable automated ToC generation and validation.

### Rule 2.3: Automated Generation (Mandatory)
ToCs **MUST** be generated automatically by official Knowledge Base tooling. Manual creation is **PROHIBITED** to prevent inconsistencies and errors.
*   **Validation:** Automated tools **MUST** ensure the generated ToC strictly conforms to Rules 2.1 and 2.2.
*   **Placement:** ToC placement is governed by structural standards (e.g., [[AS-STRUCTURE-DOC-CHAPTER]]).
*   **Rationale:** Eliminates human error in ToC maintenance, ensures real-time accuracy, and supports large-scale content management.

## 3. Importance of Strict ToC Syntax

*   **Universal Navigation:** Provides consistent and reliable navigation.
*   **Guaranteed Accessibility:** Essential for users relying on screen readers and assistive technologies.
*   **Reliable Automated Processing:** Ensures tools accurately generate, validate, and integrate ToCs.
*   **Enhanced Document Structure:** Reinforces hierarchical organization, improving comprehension.
*   **Reduced Maintenance Burden:** Eliminates manual ToC updates, reducing effort and errors.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository that require a Table of Contents. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 5. Cross-References
*   [[CS-POLICY-TONE-LANGUAGE]]
*   [[CS-TOC-POLICY]]
*   [[SF-LINKS-INTERNAL-SYNTAX]]
*   [[SF-SYNTAX-HEADINGS]]

---
*This standard (SF-TOC-SYNTAX) has been extensively revised to provide strict, singular mandates for Table of Contents syntax and automated generation. It consolidates and supersedes any prior interpretations or policies regarding ToC structure and creation, establishing a single source of truth for ToC application within the Knowledge Base.*
