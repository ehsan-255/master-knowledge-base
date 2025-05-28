---
title: "Standard: Templates Directory Structure and Usage"
standard_id: "AS-STRUCTURE-TEMPLATES-DIRECTORY"
aliases: ["Templates Directory Standard", "Document Templates Location"]
tags:
  - status/draft
  - criticality/P2-Medium # Important for consistency and efficiency
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Templates Directory and Usage" # As per prompt
related-standards: [
  "AS-KB-DIRECTORY-STRUCTURE_ID_PLACEHOLDER",
  "AS-SCHEMA-METHODOLOGY-DESCRIPTION_ID_PLACEHOLDER",
  "AS-SCHEMA-CONCEPT-DEFINITION_ID_PLACEHOLDER",
  "tpl-canonical-frontmatter_ID_PLACEHOLDER"
]
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "AS" # Architectural Standard
sub_domain: "STRUCTURE" # As per prompt
scope_application: "Defines the mandatory location, naming conventions, and content requirements for the directory housing standard document templates."
criticality: "P2-Medium"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Authoring efficiency", "Content consistency", "Standards adherence", "Onboarding new authors"]
change_log_url: "./AS-STRUCTURE-TEMPLATES-DIRECTORY-changelog.md" # Placeholder
---

# Standard: Templates Directory Structure and Usage (AS-STRUCTURE-TEMPLATES-DIRECTORY)

## 1. Standard Statement

This standard defines the requirements for the creation, maintenance, and content of a dedicated directory for standard document templates. Utilizing a centralized templates directory promotes authoring efficiency, ensures consistency in document structure, and aids in the correct application of content schemas.

## 2. Core Requirements for the Templates Directory

### Rule 2.1: Dedicated Templates Directory (Derived from U-TEMPLATES-DIR-001, Rule 1.1, adapted)
A dedicated directory for housing standard document templates MUST be maintained at the following path: `/master-knowledge-base/standards/templates/`.
*   **Rationale:** Centralizes templates for easy discovery and consistent application across the knowledge base. This specific path aligns with the established directory structure for standards-related resources (see [[AS-KB-DIRECTORY-STRUCTURE_ID_PLACEHOLDER]]).
*   **Notes:** This directory was established in Phase 0 (Task 0.4.3).

### Rule 2.2: Content of the Templates Directory (Derived from U-TEMPLATES-DIR-001, Rule 1.2)
The `/master-knowledge-base/standards/templates/` directory MUST contain Markdown template files (`.md`) for common standard document types. These templates are intended to:
    a.  Pre-fill the basic structure of a new document according to relevant `AS-SCHEMA-*` (Architectural Standard - Schema) documents, such as [[AS-SCHEMA-METHODOLOGY-DESCRIPTION_ID_PLACEHOLDER]] and [[AS-SCHEMA-CONCEPT-DEFINITION_ID_PLACEHOLDER]].
    b.  Include placeholder content or comments to guide authors on filling out various sections.
    c.  May also include utility templates, such as a canonical frontmatter template (e.g., [[tpl-canonical-frontmatter_ID_PLACEHOLDER]], which was created in Phase 0, Task 0.4.3).

*   **Examples of Templates:**
    *   `tpl-standard-definition.md`
    *   `tpl-policy-document.md`
    *   `tpl-methodology-schema.md` (based on [[AS-SCHEMA-METHODOLOGY-DESCRIPTION_ID_PLACEHOLDER]])
    *   `tpl-concept-schema.md` (based on [[AS-SCHEMA-CONCEPT-DEFINITION_ID_PLACEHOLDER]])
    *   `tpl-canonical-frontmatter.md`

### Rule 2.3: Template Naming Convention
All template filenames within the `/master-knowledge-base/standards/templates/` directory MUST be prefixed with `tpl-`.
*   **Example:** `tpl-standard-definition.md`, `tpl-canonical-frontmatter.md`.
*   **Rationale:** Clearly identifies files as templates and allows for easy programmatic identification or filtering. This convention was established in Phase 0 (Task 0.4.3).

## 3. Importance of Standardized Templates

*   **Efficiency:** Authors can create new standards-compliant documents more quickly by starting from a template.
*   **Consistency:** Ensures that all documents of a particular type share a common structure and include all mandatory sections and frontmatter fields.
*   **Accuracy:** Helps authors adhere to specific content schemas and frontmatter rules, reducing errors.
*   **Ease of Onboarding:** New contributors can more easily understand expected document structures by referring to or using templates.

## 4. Scope of Application

This standard applies to the management of the templates directory and the creation of new templates. Authors creating new standard documents are strongly encouraged to use these templates.

## 5. Cross-References
- [[AS-KB-DIRECTORY-STRUCTURE_ID_PLACEHOLDER]] - Defines the overall location of the `/master-knowledge-base/standards/templates/` directory.
- [[AS-SCHEMA-METHODOLOGY-DESCRIPTION_ID_PLACEHOLDER]] - An example of a schema for which a template should exist.
- [[AS-SCHEMA-CONCEPT-DEFINITION_ID_PLACEHOLDER]] - Another example of a schema for which a template should exist.
- [[tpl-canonical-frontmatter_ID_PLACEHOLDER]] - Reference to the existing canonical frontmatter template. (Note: This is a direct reference to a template file, not a standard. It's included as it's a key example of a utility template.)

---
*This standard (AS-STRUCTURE-TEMPLATES-DIRECTORY) is based on rules 1.1 and 1.2 previously defined in U-TEMPLATES-DIR-001 from COL-GOVERNANCE-UNIVERSAL.md, adapting them for the new directory structure and emphasizing established naming conventions.*
```
