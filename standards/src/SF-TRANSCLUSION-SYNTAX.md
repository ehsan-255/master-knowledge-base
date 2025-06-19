---
title: 'Standard: Transclusion Syntax for Content Embedding'
standard_id: SF-TRANSCLUSION-SYNTAX
aliases:
- Content Embedding Syntax
- Transclusion Standard
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p2-medium
- kb-id/standards
- status/draft
- topic/sf
- topic/transclusion
kb-id: standards
info-type: standard-definition
primary-topic: Transclusion Syntax
related-standards:
- '[[CS-MODULARITY-TRANSCLUSION-POLICY]]'
- '[[SF-LINKS-INTERNAL-SYNTAX]]'
- '[[MT-SCHEMA-FRONTMATTER]]'
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: TRANSCLUSION
scope_application: Defines a generalized syntax for declaring the intent to transclude
  (embed) content from one document into another within the knowledge base.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content reusability
- Maintainability
- Authoring tools
- KB rendering systems
---
# Standard: Transclusion Syntax for Content Embedding (SF-TRANSCLUSION-SYNTAX)

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax for declaring the intent to transclude (embed) content from one document (or part of a document) into another within the Knowledge Base. The purpose of this syntax is to provide a **strictly consistent and unambiguous method** for authors to specify content reuse, rigorously enforcing the "Don't Repeat Yourself" (DRY) principle across the entire Knowledge Base.

## 2. Core Transclusion Syntax Rules

All transclusion declarations **MUST** begin with an exclamation mark (`!`) followed immediately by double brackets (`[[...]]`).

### Rule 2.1: Embedding Entire Documents by `standard_id`
To embed the entire content of another formal standard document (one with a `standard_id`), the `standard_id` **MUST** be used within the transclusion syntax.
*   **Mandatory Syntax:** `![[TARGET_STANDARD_ID]]`
*   **`TARGET_STANDARD_ID`**: This **MUST** be the valid and existing `standard_id` of the source document.
*   **Prohibited Syntax:** Directly embedding a document using its file path (e.g., `![[./path/to/document.md]]`) is **PROHIBITED** if the document possesses a `standard_id`.
*   **Example:** `![[AS-SCHEMA-CONCEPT-DEFINITION]]`
*   **Rationale:** Ensures that content reuse leverages the robust and stable `standard_id` system, preventing broken embeds due to file renames or moves.

### Rule 2.2: Embedding Specific Sections (Headings)
To embed a specific section from another document, identified by one of its headings, the heading text **MUST** be appended to the target document reference using the hash symbol (`#`).
*   **Mandatory Syntax:** `![[TARGET_DOCUMENT_ID#Heading Text]]`
    *   `TARGET_DOCUMENT_ID` can be a `standard_id` (for standards) or a root-relative file path (for non-standard documents, as per [[SF-LINKS-INTERNAL-SYNTAX]]).
*   **Requirement:** The `Heading Text` portion **MUST** exactly match the target heading in the source document, including capitalization, spaces, and punctuation, to ensure successful embedding.
*   **Example (from a Standard):** `![[AS-SCHEMA-CONCEPT-DEFINITION#Rule 2.1: H1 Title]]`
*   **Example (from a non-Standard document):** `![[./guides/setup/quick-start.md#Installation Steps]]`
*   **Rationale:** Allows for precise embedding of modular content blocks defined by headings, crucial for targeted content reuse.

### Rule 2.3: Embedding Specific Blocks (Block IDs)
To embed a specific, smaller block of content (e.g., a paragraph, list item, or code block) from another document, a unique block identifier **MUST** be used.
*   **Mandatory Syntax:** `![[TARGET_DOCUMENT_ID#^blockID]]`
    *   `TARGET_DOCUMENT_ID` can be a `standard_id` or a root-relative file path.
*   **`^blockID`**: The `^blockID` **MUST** be a unique identifier assigned directly to the specific block of text within the source document (e.g., `This is a paragraph. ^my-unique-block`). The method for defining these `^blockID`s **MUST** be consistently applied and supported by tooling.
*   **Example:** `![[AS-SCHEMA-CONCEPT-DEFINITION#^important-note-on-schemas]]`
*   **Rationale:** Provides the most granular control over content reuse, enabling the embedding of very specific content snippets while adhering to the DRY principle.

## 3. Mandatory Considerations for Transclusion

### Rule 3.1: Valid Target Identification
The `TARGET_DOCUMENT_ID` (whether `standard_id` or root-relative path) used in any transclusion syntax **MUST** correspond to a valid, existing document or section within the Knowledge Base. Broken transclusion links due to invalid identifiers **MUST** be flagged as critical errors by validation tools.

### Rule 3.2: Tooling Support for Rendering
While this standard defines the syntax for declaring transclusion intent, the actual rendering and display of transcluded content is dependent on the capabilities of the authoring, publishing, or viewing tools used with the Knowledge Base. All official Knowledge Base tooling **MUST** support the full rendering of transcluded content as defined by this standard.
*   **Prohibition:** Tools that do not support the defined transclusion syntax, or that render it inconsistently, **MUST NOT** be used for authoring or publishing official Knowledge Base content.

### Rule 3.3: Prohibition of Circular Transclusion
Authors and automated processes **MUST NOT** create circular transclusion dependencies (e.g., Document A transcludes Document B, and Document B transcludes Document A). Such circular dependencies **WILL** lead to processing errors or infinite loops in rendering tools. Validation tools **MUST** be in place to detect and report circular transclusions as critical errors.

## 4. Importance of Strict Transclusion Syntax

*   **Guaranteed Content Reusability:** Provides an unambiguous and reliable mechanism for content embedding, ensuring the DRY principle is rigorously applied.
*   **Enhanced Maintainability:** Updating content in one source document automatically propagates changes to all embedded instances, drastically reducing maintenance overhead and error potential.
*   **Consistency Across KB:** Ensures that common definitions, warnings, or procedural steps are presented identically wherever they appear, fostering a unified and authoritative knowledge base.
*   **Reliable Automated Processing:** Tools for content assembly, validation, and publishing can depend on a predictable transclusion syntax, improving automation reliability.
*   **Streamlined Authoring:** Authors can efficiently build documents by assembling modular content blocks, reducing manual effort and improving content quality.

## 5. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where content embedding from other documents is required. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and any tooling interacting with KB Markdown files.

## 6. Cross-References
- [[CS-POLICY-TONE-LANGUAGE]] - For definitions of mandating keywords (MUST, SHOULD, MAY) and general language policy.
- [[CS-MODULARITY-TRANSCLUSION-POLICY]] - Policy on when and how to use modularity and transclusion.
- [[SF-LINKS-INTERNAL-SYNTAX]] - For the base syntax of internal linking, which transclusion extends, and rules for path resolution for non-standard documents.
- [[MT-SCHEMA-FRONTMATTER]] - For the definition of `standard_id`.

---
*This standard (SF-TRANSCLUSION-SYNTAX) has been extensively revised to provide strict, singular mandates for transclusion syntax, clarifying its application and incorporating absolute prohibitions to ensure universal consistency and adherence to the DRY principle within the Knowledge Base. It replaces and supersedes any prior interpretations or practices where conflicts existed, establishing a single source of truth for content embedding.*
