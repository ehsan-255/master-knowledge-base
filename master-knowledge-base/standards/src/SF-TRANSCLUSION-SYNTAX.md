---
title: 'Standard: Transclusion Syntax for Content Embedding'
standard_id: SF-TRANSCLUSION-SYNTAX
aliases:
  - Content Embedding Syntax
  - Transclusion Standard
tags:
  - status/draft
  - criticality/p2-medium
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Transclusion Syntax
related-standards:
  - '[[CS-MODULARITY-TRANSCLUSION-POLICY]]'
  - '[[SF-LINKS-INTERNAL-SYNTAX]]'
  - '[[MT-SCHEMA-FRONTMATTER]]'
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-05-30T12:00:00Z'
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
change_log_url: ./changelog.md
---
# Standard: Transclusion Syntax for Content Embedding (SF-TRANSCLUSION-SYNTAX)

## 1. Standard Statement

This standard defines a generalized syntax for declaring the intent to transclude (embed) content from one document (or part of a document) into another within the knowledge base. The purpose of this syntax is to provide a consistent method for authors to specify content reuse, promoting the "Don't Repeat Yourself" (DRY) principle.

## 2. Transclusion Syntax

The generalized syntax for transclusion uses a double-bracketed link format, prefixed with an exclamation mark `!`.

### Rule 2.1: Embedding Entire Files
To embed the entire content of another document, use the following syntax:
*   **Syntax:** `![[TARGET_STANDARD_ID]]`
*   **`TARGET_STANDARD_ID`**: This MUST be the valid `standard_id` of an existing document within the knowledge base.
*   **Example:** `![[AS-SCHEMA-CONCEPT-DEFINITION]]`
*   **Behavior:** This declaration indicates that the entire content of the document identified by `AS-SCHEMA-CONCEPT-DEFINITION` should be embedded at this point.

### Rule 2.2: Embedding Specific Sections (Headings)
To embed a specific section from another document, identified by one of its headings, use the following syntax:
*   **Syntax:** `![[TARGET_STANDARD_ID#Heading Text]]`
*   **`TARGET_STANDARD_ID`**: The `standard_id` of the target document.
*   **`#Heading Text`**: The exact text of the heading (H1-H6) of the section to be embedded. The heading text is case-sensitive and must match precisely.
*   **Example:** `![[AS-SCHEMA-CONCEPT-DEFINITION#Rule 2.1: H1 Title]]`
*   **Behavior:** This indicates that only the content under the specified heading (and its sub-headings, up to the next heading of the same or higher level) should be embedded.

### Rule 2.3: Embedding Specific Blocks (Block IDs)
To embed a specific block of content (e.g., a paragraph, list item) from another document, a block identifier syntax can be used:
*   **Syntax:** `![[TARGET_STANDARD_ID#^blockID]]`
*   **`TARGET_STANDARD_ID`**: The `standard_id` of the target document.
*   **`#^blockID`**: The `^blockID` is a unique identifier assigned to a specific block of text (e.g., a paragraph, list item, table) within the target document.
    *   **Block ID Definition:** The method for defining `^blockID`s within a source document (e.g., `This is a paragraph. ^my-unique-block`) is a convention that needs to be supported by authoring and processing tools. This standard primarily defines how to *reference* such a block for transclusion.
*   **Example:** `![[AS-SCHEMA-CONCEPT-DEFINITION#^important-note-on-schemas]]`
*   **Behavior:** This indicates that only the specific block of content associated with `^blockID` in the target document should be embedded.

## 3. Key Considerations

### Rule 3.1: Target Identification
The `TARGET_STANDARD_ID` used in any transclusion syntax MUST correspond to a valid, existing `standard_id` of a document within the knowledge base. Broken transclusion links due to invalid IDs should be flagged by validation tools.

### Rule 3.2: Tooling Dependency for Rendering
The actual rendering and display of transcluded content are dependent on the capabilities of the authoring, publishing, or viewing tools used with the knowledge base. This standard defines the *syntax for declaring transclusion intent*, providing a consistent authoring experience.
*   **Fallback Behavior:** If a tool does not support transclusion, it MAY render the syntax as a standard internal link (e.g., `[[TARGET_STANDARD_ID]]`) or display a placeholder indicating that embedded content is intended.

### Rule 3.3: Avoiding Circular Transclusion
Authors MUST avoid creating circular transclusion dependencies (e.g., Document A transcludes Document B, and Document B transcludes Document A). Such circular dependencies can lead to processing errors or infinite loops in rendering tools. Validation tools SHOULD attempt to detect circular transclusions.

## 4. Rationale

*   **Consistency:** Provides a uniform syntax for authors to express the intent of embedding content.
*   **Modularity:** Supports the creation of modular content by allowing reusable chunks of information to be defined once and referenced multiple times, as outlined in [[CS-MODULARITY-TRANSCLUSION-POLICY]].
*   **Maintainability:** When transcluded content is updated in its source document, all instances where it is embedded reflect these changes automatically (assuming tool support), reducing redundancy and effort.
*   **Future-Proofing:** Establishes a clear syntax that can be adopted by various tools, even if full rendering support varies initially.

## 5. Scope of Application

This standard applies to all authors creating or editing content within the knowledge base who wish to embed content from one document into another.

## 6. Cross-References
- [[CS-MODULARITY-TRANSCLUSION-POLICY]] - Policy on when and how to use modularity and transclusion.
- [[SF-LINKS-INTERNAL-SYNTAX]] - For the base syntax of internal linking, which transclusion extends.
- [[MT-SCHEMA-FRONTMATTER]] - For the definition of `standard_id`.

---
*This standard (SF-TRANSCLUSION-SYNTAX) generalizes concepts from O-USAGE-TRANSCLUSION-001 and aims to provide a tool-agnostic syntax for declaring content embedding intent.*
