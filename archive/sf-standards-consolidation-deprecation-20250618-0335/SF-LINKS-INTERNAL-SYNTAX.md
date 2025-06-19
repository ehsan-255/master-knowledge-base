---
title: Internal Linking Syntax Standard
standard_id: SF-LINKS-INTERNAL-SYNTAX
aliases:
- Linking Standard
- Wikilink Syntax
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/links
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Internal Linking Syntax
related-standards:
- CS-LINKING-INTERNAL-POLICY
version: 0.1.0
date-created: '2024-07-15T10:00:00Z'
date-modified: '2025-06-17T02:29:15Z'
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
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# SF-LINKS-INTERNAL-SYNTAX: Internal Linking Syntax Standard

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax and strict procedures for creating all internal links within Knowledge Base Markdown documents. Adherence to these rules is **CRITICAL** for ensuring universal consistency, preserving link integrity, enabling robust automated validation, and providing predictable navigation across the entire Knowledge Base ecosystem.

## 2. Core Internal Linking Rules

### Rule 2.1: Canonical Linking to Standard Documents by `standard_id`
Internal links to other formal standard documents (those with an assigned `standard_id` in their frontmatter) **MUST** be created exclusively by referencing their unique `standard_id`.
*   **Mandatory Syntax:** `[[STANDARD_ID]]` or `[[STANDARD_ID|Display Text]]`
*   **Example (without alias):** `[[AS-STRUCTURE-KB-ROOT]]`
*   **Example (with alias):** `[[AS-STRUCTURE-KB-ROOT|Knowledge Base Root Structure Standard]]`
*   **Rationale:** Referencing `standard_id` directly makes links highly resilient to file renames or moves, as the unique identifier remains stable. This is crucial for maintaining long-term link integrity in a dynamic knowledge base.

### Rule 2.2: Mandatory Descriptive Link Text for Readability
For all internal links (both to standard documents and non-standard documents), the link text **MUST** be descriptive and clearly indicate the nature of the target content to the user, enhancing readability and navigation. Using the raw `STANDARD_ID` or filename as link text is **PROHIBITED** if it is not immediately clear or sufficiently descriptive in context.
*   **Mandatory Use of Alias:** When the `STANDARD_ID` or filename is not inherently clear, an alias (display text) **MUST** be provided using the pipe (`|`) separator.
    *   **Example (Correct):** `For details, see the [[SF-SYNTAX-EMPHASIS|Text Emphasis Syntax Standard]].`
    *   **Prohibited (if not descriptive):** `For details, see [[SF-SYNTAX-EMPHASIS]].`
*   **Rationale:** Descriptive link text improves scannability, accessibility (for screen readers), and helps users understand the destination of a link before clicking, fostering a better user experience.

### Rule 2.3: Linking to Specific Sections (Headings)
To link directly to a specific heading or section within a target document, the heading text **MUST** be appended to the target document reference using the hash symbol (`#`).
*   **Mandatory Syntax:** `[[STANDARD_ID#Heading Text]]` or `[[STANDARD_ID#Heading Text|Display Text]]`
*   **Example (Standard ID):** `[[AS-STRUCTURE-KB-ROOT#Master Table of Contents]]`
*   **Example (Non-Standard Document):** `[[./path/to/document.md#Specific Section Name|Learn More]]`
*   **Requirement:** The `Heading Text` portion **MUST** exactly match the target heading in the linked document, including capitalization, spaces, and punctuation, to ensure the link resolves correctly.
*   **Rationale:** Allows for precise deep-linking within documents, improving navigability and user efficiency.

### Rule 2.4: Internal Linking for Non-Standard Documents (Path-Based)
For internal links to Markdown documents that do **NOT** have a `standard_id` (e.g., project notes, guides, or other general documentation files), relative file paths **MUST** be used. These paths **MUST** be relative to the repository root to ensure maximum stability, consistency, and portability across different tools and environments.
*   **Mandatory Syntax:** `[Link Text](./path/from/repo/root/to/document.md)`
*   **Example:** `[Project Guidelines](./active-project/project-guidelines/project-reminders.md)`
*   **Prohibited:** Direct path-based links relative to the *current* file's directory (e.g., `../another/file.md`) are **PROHIBITED** to avoid ambiguity and fragility when files are moved.
*   **Rationale:** A consistent root-relative path strategy minimizes the likelihood of broken links when files are reorganized within the repository, and simplifies automated processing like linting and indexing.

### Rule 2.5: Prohibition of Direct Path-Based Linking for Standard Documents
Direct file path-based links (e.g., `[text](./standards/src/AS-STRUCTURE-KB-ROOT.md)`) to standard documents that possess a `standard_id` are **PROHIBITED**. All references to such documents **MUST** use their `standard_id` as defined in Rule 2.1.
*   **Rationale:** Enforces the `standard_id` as the single canonical identifier for standard documents, which is more robust and maintainable than file paths.

### Rule 2.6: External Linking
Links to external web resources **MUST** use standard Markdown URL syntax.
*   **Mandatory Syntax:** `[Link Text](https://example.com/external-resource)`
*   **Rationale:** Provides a clear and universally understood method for referencing external content.

## 3. Importance of Strict Internal Linking

*   **Guaranteed Link Integrity:** Strict rules and preferred `standard_id` linking for standards drastically reduce the chance of broken links, even as the file structure evolves.
*   **Enhanced Navigation & Discoverability:** Consistent linking and descriptive text make the Knowledge Base highly navigable and ensure users can easily find related information.
*   **Reliable Automated Processing:** Tools for validation, indexing, and content transformation can reliably parse and resolve links, which is crucial for maintaining a healthy KB.
*   **Improved Maintainability:** A single, clear approach to linking simplifies authoring, reviewing, and updating content, especially in a large repository.
*   **Unified User Experience:** Provides a predictable and professional linking experience across all documents.

## 4. Scope of Application

This standard applies to **ALL** internal and external links created within **ALL** Markdown documents across the entire Knowledge Base repository. Adherence is **MANDATORY** for all content creators, automated systems, and any tooling interacting with KB Markdown files.

## 5. Cross-References
- [[CS-POLICY-TONE-LANGUAGE]] - For definitions of mandating keywords (MUST, SHOULD, MAY) and general language policy.
- [[CS-LINKING-INTERNAL-POLICY]] - General policy on the strategy and best practices for internal linking.

---
*This standard (SF-LINKS-INTERNAL-SYNTAX) has been extensively revised to provide strict, singular mandates for internal linking syntax, path resolution, and descriptive text, consolidating previous guidelines into absolute requirements. It replaces and supersedes any prior interpretations or practices where conflicts existed, establishing a single source of truth for linking within the Knowledge Base.*
