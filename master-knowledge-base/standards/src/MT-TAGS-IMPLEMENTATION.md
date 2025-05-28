---
title: "Standard: Tag Implementation and Syntax"
standard_id: "MT-TAGS-IMPLEMENTATION"
aliases: ["Tag Syntax", "Tag Declaration Standard"]
tags:
  - status/draft
  - criticality/P1-High # Correct syntax is vital for processing
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Tag Syntax and Declaration" # As per prompt
related-standards: ["MT-TAGGING-STRATEGY-POLICY_ID_PLACEHOLDER", "U-METADATA-FRONTMATTER-RULES-001_ID_PLACEHOLDER", "MT-REGISTRY-TAG-GLOSSARY_ID_PLACEHOLDER"]
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "MT" # Metadata & Tagging
sub_domain: "TAGGING" # As per prompt
scope_application: "Defines the syntax and declaration rules for all tags used within the knowledge base frontmatter."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Metadata consistency", "Automated processing of tags", "Content discoverability", "Authoring accuracy"]
change_log_url: "./MT-TAGS-IMPLEMENTATION-changelog.md" # Placeholder
---

# Standard: Tag Implementation and Syntax (MT-TAGS-IMPLEMENTATION)

This standard defines the mandatory syntax and declaration rules for all tags used within the YAML frontmatter of knowledge base documents. Adherence to these rules is essential for ensuring metadata consistency, enabling reliable automated processing, and supporting effective content discovery.

## 1. Tag Declaration and Syntax Rules

### Rule 1.1: Declaration in YAML Frontmatter (Derived from U-TAG-001, Rule 1.1)
All tags associated with a document MUST be declared within the YAML frontmatter block at the beginning of the document.
*   **Rationale:** Centralizes metadata, making it easily parsable by automated tools and consistently accessible to authors.
*   **Reference:** General frontmatter structure is defined in [[U-METADATA-FRONTMATTER-RULES-001_ID_PLACEHOLDER]].

### Rule 1.2: `tags` Key and Block List Format (Derived from U-TAG-001, Rule 1.2)
Within the YAML frontmatter, tags MUST be listed under a key named exactly `tags`. The value of this key MUST be a block list of strings (each string being a single tag).
*   **Example:**
    ```yaml
    tags:
      - status/draft
      - topic/syntax
      - content-type/standard-definition
    ```
*   **Rationale:** Provides a consistent and machine-readable format for tag declaration.

### Rule 1.3: Kebab-Case for Tag Strings (Derived from U-TAG-001, Rule 1.3)
All tag strings MUST be in **kebab-case** (all lowercase, with words separated by single hyphens).
*   **Example (Correct):** `topic/research-methods`, `content-type/technical-standard`
*   **Example (Incorrect):** `topic/researchMethods`, `ContentType/TechnicalStandard`
*   **Rationale:** Ensures uniformity in tag appearance and simplifies programmatic processing of tags by avoiding case sensitivity issues.

### Rule 1.4: Hierarchical Tag Structure (Derived from U-TAG-001, Rule 1.4)
Tags MAY use forward slashes (`/`) to indicate an internal hierarchy or categorization.
*   **Guidance:**
    *   When used, the hierarchy should be logical and consistently applied (e.g., `category/sub-category/specific-tag`).
    *   Top-level categories (e.g., `topic/`, `status/`, `content-type/`, `criticality/`) should generally come first in the tag string.
*   **Example:** `topic/architecture/directory-structure`, `status/in-review`, `content-type/policy-document`
*   **Rationale:** Hierarchical tags allow for more granular categorization and faceted filtering, improving content organization and discoverability.

## 2. Tag Glossary Requirement (Derived from U-TAG-001, Rule 1.9 - part)

A dedicated Tag Glossary document MUST exist and be maintained. This glossary serves as the single source of truth for all officially recognized tags.
*   **Identification:** This glossary is identified by the standard ID [[MT-REGISTRY-TAG-GLOSSARY_ID_PLACEHOLDER]].
*   **Purpose:** The Tag Glossary lists all official tags, defines their intended meaning and scope, and illustrates their correct hierarchy and usage.
*   **Mandate for Conformance:** All tags used in any document's frontmatter MUST conform to a tag defined in the [[MT-REGISTRY-TAG-GLOSSARY_ID_PLACEHOLDER]]. The strategic application of these tags is further defined in [[MT-TAGGING-STRATEGY-POLICY_ID_PLACEHOLDER]].
*   **Rationale:** Ensures that tags are used consistently and meaningfully across the entire knowledge base, preventing tag proliferation and ambiguity.

## 3. Cross-References
- [[U-METADATA-FRONTMATTER-RULES-001_ID_PLACEHOLDER]] - Defines general YAML frontmatter structure and rules.
- [[MT-TAGGING-STRATEGY-POLICY_ID_PLACEHOLDER]] - Outlines the strategic application of different tag categories.
- [[MT-REGISTRY-TAG-GLOSSARY_ID_PLACEHOLDER]] - The official glossary of all approved tags and their definitions.

---
*This standard (MT-TAGS-IMPLEMENTATION) is based on rules 1.1, 1.2, 1.3, 1.4, and part of 1.9 previously defined in U-TAG-001 from COL-LINKING-UNIVERSAL.md.*
```
