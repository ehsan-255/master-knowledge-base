---
title: Internal Linking Syntax Standard
standard_id: SF-LINKS-INTERNAL-SYNTAX
aliases:
  - Linking Standard
  - Wikilink Syntax
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Internal Linking Syntax
related-standards:
  - CS-LINKING-INTERNAL-POLICY
version: 0.1.0
date-created: '2024-07-15T10:00:00Z'
date-modified: '2025-05-30T12:00:00Z'
primary_domain: SF
sub_domain: LINKS
scope_application: All knowledge base documents utilizing Markdown for internal linking.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Authoring workflow
  - Content reusability
  - Link integrity
  - Automated validation
---
# SF-LINKS-INTERNAL-SYNTAX: Internal Linking Syntax Standard

## 1. Overview

This standard defines the syntax and best practices for creating internal links within knowledge base documents. Adherence to this standard ensures consistency, maintainability, and optimal functionality of the linking system across the knowledge base.

## 2. Canonical Link Style: `[[STANDARD_ID]]`

The canonical and mandatory method for internal linking to other standard documents is by using their unique `standard_id`.

*   **Syntax:** `[[STANDARD_ID]]`
*   **Example:** `[[AS-STRUCTURE-KB-ROOT]]`

This style directly references the unique identifier of the target standard, making links resilient to file renaming or moves (assuming the `standard_id` remains stable and an index maps IDs to paths).

## 3. Linking to Specific Headings

To link to a specific heading or section within a target document, use the following syntax:

*   **Syntax:** `[[STANDARD_ID#Heading Text]]`
*   **Example:** `[[AS-STRUCTURE-KB-ROOT#Section 2.1]]`

The heading text MUST exactly match the target heading in the linked document, including capitalization and punctuation.

## 4. Link Text Aliases (Display Text)

If the link text needs to be different from the `STANDARD_ID` or `STANDARD_ID#Heading Text`, an alias can be used:

*   **Syntax:** `[[STANDARD_ID|Display Text]]`
*   **Syntax (with heading):** `[[STANDARD_ID#Heading Text|Display Text]]`
*   **Example:** `[[AS-STRUCTURE-KB-ROOT|Knowledge Base Root Structure]]`
*   **Example (with heading):** `[[AS-STRUCTURE-KB-ROOT#Section 2.1|Details on KB Root]]`

## 5. Transitional Policy for Path-Based Links

During the transition to a fully `standard_id`-based linking system:

*   **Current State:** Direct path-based links (e.g., `[link text](./path/to/file.md)`) or relative wikilinks that resolve via file paths may exist in older documents.
*   **Linter Behavior (Phase 0):** Automated linters and validation tools will issue a **warning** for any internal links that use direct file paths instead of the `[[STANDARD_ID]]` format.
*   **Future State (Post-Transition):** Path-based internal links will be flagged as **errors** and must be remediated. The goal is to exclusively use `[[STANDARD_ID]]`-based links for referencing other standard documents.

## 6. Non-Standard Document Linking

For linking to documents that are not part of the formal standards collection (e.g., external documentation, supplementary resources not having a `standard_id`), standard Markdown relative or absolute links should be used:

*   **Syntax (Relative):** `[Link Text](./path/to/document.md)`
*   **Syntax (Absolute URL):** `[Link Text](https://example.com/resource)`

## 7. Generalization and Tool Independence

The linking mechanisms described herein are intended to be tool-agnostic. While some authoring tools may offer enhanced features for creating or managing these link types (e.g., Obsidian, Foam), the underlying syntax and principles must remain consistent with this standard to ensure interoperability and long-term maintainability. Tool-specific features that deviate from this standard should not be used for canonical linking between standard documents.
