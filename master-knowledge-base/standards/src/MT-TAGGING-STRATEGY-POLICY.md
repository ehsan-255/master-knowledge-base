---
title: "Policy: Core Tagging Strategy"
standard_id: "MT-TAGGING-STRATEGY-POLICY"
aliases: ["Tagging Strategy", "Metadata Tagging Policy"]
tags:
  - status/draft
  - criticality/P1-High # A coherent strategy is vital
  - content-type/policy-document
kb-id: "" # Global policy
info-type: "policy-document"
primary-topic: "Core Tagging Strategy" # As per prompt
related-standards: ["MT-TAGS-IMPLEMENTATION", "MT-REGISTRY-TAG-GLOSSARY", "MT-SCHEMA-FRONTMATTER"]
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2025-05-29T16:10:25Z"
primary_domain: "MT" # Metadata & Tagging
sub_domain: "POLICY" # As per prompt
scope_application: "Governs the strategic application of mandatory and recommended tag categories across all knowledge base documents."
criticality: "P1-High"
lifecycle_gatekeeper: "Editorial-Board-Approval" # Tagging strategy is often a governance decision
impact_areas: ["Content discoverability", "Faceted search and filtering", "Semantic understanding of content", "Automation capabilities", "KB organization"]
change_log_url: "./MT-TAGGING-STRATEGY-POLICY-changelog.md" # Placeholder
---

# Policy: Core Tagging Strategy (MT-TAGGING-STRATEGY-POLICY)

## 1. Policy Statement

This policy defines the core strategy for applying tags to knowledge base documents. It mandates the use of specific tag categories to ensure consistent metadata, enhance content discoverability, support faceted search and filtering, and provide semantic meaning for automated processing. All tags MUST conform to the syntax defined in [[MT-TAGS-IMPLEMENTATION]] and be defined in the [[MT-REGISTRY-TAG-GLOSSARY]].

## 2. Mandatory Tag Categories and Usage

The following tag categories and their usage rules are mandatory for all relevant documents:

### Rule 2.1: `topic/*` Tag (Derived from U-TAG-001, Rule 1.5)
Every content document (e.g., standards, guides, detailed concepts, methodologies) MUST include at least one `topic/*` tag that accurately reflects its primary subject matter.
*   **Guidance:** Multiple `topic/*` tags are encouraged for interdisciplinary topics to enhance discoverability across different subject areas.
*   **Example:** `topic/architecture`, `topic/metadata/frontmatter`
*   **Rationale:** `topic/*` tags are fundamental for subject-based searching, filtering, and navigation.

### Rule 2.2: `status/*` Tag (Derived from U-TAG-001, Rule 1.6)
Every document MUST include exactly ONE `status/*` tag to indicate its current lifecycle stage.
*   **Guidance:** Valid status values (e.g., `status/draft`, `status/in-review`, `status/approved`, `status/deprecated`) are defined in the [[MT-REGISTRY-TAG-GLOSSARY]].
*   **Example:** `status/draft`
*   **Rationale:** Clearly communicates the maturity and reliability of the document content.

### Rule 2.3: Structural Identification Tags (Derived from U-TAG-001, Rule 1.7)
Specific tags MUST be used to identify key structural documents within the knowledge base ecosystem:
    a.  **`kb-master-index`**: MUST be applied to the master `kb-directory.md` file.
    b.  **`kb-root`**: MUST be applied to the `root.md` file of each individual Knowledge Base.
    c.  **`kb-id/{kb-name}`**: MUST be applied to the `root.md` file of each individual Knowledge Base, where `{kb-name}` is the unique identifier for that KB (e.g., `kb-id/standards-kb`).
    d.  **`kb-part-overview`**: MUST be applied to `_overview.md` files that serve as the overview for a "Part" (major section) within a Knowledge Base.
*   **Rationale:** These tags enable automated identification and processing of key navigational and structural files.

### Rule 2.4: `content-type/*` Tag (Derived from U-TAG-001, Rule 1.8)
Every document MUST include at least one `content-type/*` tag that describes its nature or format.
*   **Guidance:** The controlled vocabulary for the `{type}` part of `content-type/{type}` (e.g., `standard-document`, `policy-document`, `guide-document`) is defined in the `tag-glossary-definition.md` file, referenced as [[MT-REGISTRY-TAG-GLOSSARY]]. This aligns with, but is distinct from, the `info-type` frontmatter key detailed in [[MT-SCHEMA-FRONTMATTER]].
*   **Example:** `content-type/technical-standard`, `content-type/conceptual-explanation`
*   **Rationale:** Allows users and systems to filter content based on its type, facilitating easier access to specific kinds of information.

## 3. Conformance to Tag Glossary (Derived from U-TAG-001, Rule 1.9 - part)

All tag values used in any document's frontmatter (across all categories like `topic/*`, `status/*`, `content-type/*`, `criticality/*`, etc.) MUST strictly conform to a tag explicitly defined in the official Tag Glossary document ([[MT-REGISTRY-TAG-GLOSSARY]]).
*   **Rationale:** Ensures that the tagging system remains controlled, consistent, and meaningful. Prevents the proliferation of ad-hoc or redundant tags, which would degrade the quality and utility of the metadata. The Tag Glossary is the single source of truth for all approved tags.

## 4. Rationale for Tagging Strategy

A robust and consistently applied tagging strategy offers numerous benefits:

*   **Enhanced Discoverability:** Tags provide multiple dimensions for finding relevant content beyond folder structures or titles.
*   **Faceted Search and Filtering:** Allows users to narrow down searches and browse content by combining different tag facets (e.g., find all `status/approved` documents with `topic/security` and `content-type/technical-standard`).
*   **Semantic Meaning:** Adds semantic context to documents, making their purpose and relevance clearer to both humans and machines.
*   **Automation Potential:** Enables automated workflows, such as generating specialized reports, validating content, or managing content lifecycles based on tags.
*   **Improved Knowledge Base Organization:** Complements the structural organization of the KB by providing flexible, metadata-driven views of the content.

## 5. Scope of Application

This policy applies to all documents within the knowledge base ecosystem that utilize YAML frontmatter for metadata. All contributors and maintainers of content are responsible for adhering to this tagging strategy.

## 6. Cross-References
- [[MT-TAGS-IMPLEMENTATION]] - Defines the syntax and declaration rules for tags.
- [[MT-REGISTRY-TAG-GLOSSARY]] - The official glossary of all approved tags, their hierarchies, and definitions.
- [[MT-SCHEMA-FRONTMATTER]] - Defines the `info-type` key and overall frontmatter structure.

---
*This policy (MT-TAGGING-STRATEGY-POLICY) is based on rules 1.5, 1.6, 1.7, 1.8, and the conformance aspect of 1.9 previously defined in U-TAG-001 from COL-LINKING-UNIVERSAL.md.*
```
