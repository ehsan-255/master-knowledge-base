---
title: 'Policy: Internal Knowledge Base Linking Strategy'
standard_id: CS-LINKING-INTERNAL-POLICY
aliases:
- Internal Linking Policy
- KB Linking Strategy
tags:
- status/draft
- criticality/p2-medium
- content-type/policy-document
kb-id: standards
info-type: policy-document
primary-topic: Internal Linking Strategy and Best Practices
related-standards:
- SF-LINKS-INTERNAL-SYNTAX
- AS-STRUCTURE-DOC-CHAPTER
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-01T23:30:16Z'
primary_domain: CS
sub_domain: POLICY
scope_application: Governs the strategy and best practices for creating internal links within and between documents in all Knowledge Bases.
criticality: P2-Medium
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
- Knowledge discovery
- KB navigability
- Content cohesion
- User experience
- Information architecture
---

# Policy: Internal Knowledge Base Linking Strategy (CS-LINKING-INTERNAL-POLICY)

## 1. Policy Statement

This policy outlines the strategy and best practices for creating internal links within documents in the Knowledge Base (KB). Effective internal linking is crucial for knowledge discovery, enhancing navigability, creating content cohesion, and improving the overall user experience. All internal links MUST adhere to the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]].

## 2. Core Linking Policies

### Rule 2.1: Extensive Use of Internal Links (Derived from U-INTERLINK-001, Rule 1.1)
Internal links between documents, notes, and specific sections within the same Knowledge Base MUST be used extensively and purposefully to connect related concepts, methodologies, definitions, and supporting information.
*   **Rationale:** Promotes discoverability of related information, helps users build a more holistic understanding of topics, and transforms the KB into a truly interconnected web of knowledge rather than a collection of isolated documents.

### Rule 2.2: Descriptive Link Text (Derived from U-INTERLINK-001, Rule 1.3)
Link text MUST be descriptive and clearly indicate the nature of the target content.
*   **Guidance for `[[STANDARD_ID]]` or `[[filename]]` style links:** If the raw `STANDARD_ID` or filename (used as link text by default in some syntaxes) is not sufficiently descriptive for the context, an alias or display text MUST be used.
    *   **Example:** Instead of just `See [[SF-LINKS-INTERNAL-SYNTAX]].`, prefer `For detailed syntax rules, see the [[SF-LINKS-INTERNAL-SYNTAX|Internal Linking Syntax Standard]].`
*   **Rationale:** Descriptive link text improves scannability, accessibility (for screen reader users), and helps users decide whether to follow a link by providing clear context about the destination.

### Rule 2.3: "See Also" Sections for Grouped Links (Derived from U-INTERLINK-001, Rule 1.4)
"See Also" sections, as defined in [[AS-STRUCTURE-DOC-CHAPTER]], ARE a primary and mandatory mechanism for grouping links to related documents, standards, or external resources at the end of a document.
*   **Rationale:** Provides a dedicated and consistent location for users to find further relevant information, acting as a curated list of related readings or next steps.

### Rule 2.4: Contextual Relevance and Avoidance of Over-Linking (Derived from U-INTERLINK-001, Rule 1.5)
Links embedded within the main body of the text MUST be contextually relevant to the specific point being discussed. Over-linking (creating too many links in a way that distracts from the primary content) MUST be avoided.
*   **Guidance:**
    *   A link should add value and enhance understanding at the point where it is inserted.
    *   Avoid linking common terms or every possible keyword. Focus on links that provide significant additional context, definitions for specialized terms, or direct pathways to closely related procedures or concepts.
    *   Consider whether a concept is better explained briefly in situ or if a link to a more detailed explanation is truly necessary.
*   **Rationale:** Ensures that links are helpful rather than distracting, maintaining readability and focus on the current document's narrative.

## 3. Adherence to Link Syntax Standard

All internal links, regardless of the specific linking strategy employed, MUST strictly adhere to the syntactical rules defined in [[SF-LINKS-INTERNAL-SYNTAX]]. This ensures consistency, maintainability, and allows for potential automated processing or validation of links.

## 4. Rationale for Linking Policy

A coherent internal linking strategy provides significant benefits:

*   **Enhanced Knowledge Discovery:** Allows users to naturally explore related topics and discover information they might not have found otherwise.
*   **Improved Navigability:** Makes it easier for users to move between related pieces of information, creating intuitive pathways through the KB.
*   **Reduced Redundancy:** Encourages linking to a single authoritative source for a concept or definition rather than repeating information across multiple documents.
*   **Increased Content Cohesion:** Weaves individual documents into a more cohesive and integrated knowledge resource.
*   **Better User Experience:** A well-linked KB feels more like an integrated system and is generally easier and more satisfying to use.

## 5. Scope of Application

This policy applies to all content creators, editors, and curators working within any Knowledge Base in the repository. It governs the creation and maintenance of all internal links.

## 6. Cross-References
- [[SF-LINKS-INTERNAL-SYNTAX]] - Defines the mandatory syntax for internal links.
- [[AS-STRUCTURE-DOC-CHAPTER]] - Defines the requirement for "See Also" sections in documents.

---
*This policy (CS-LINKING-INTERNAL-POLICY) is based on rules 1.1, 1.3, 1.4, and 1.5 previously defined in U-INTERLINK-001 from COL-LINKING-UNIVERSAL.md. Rule 1.2 regarding syntax is now covered by [[SF-LINKS-INTERNAL-SYNTAX]].*
