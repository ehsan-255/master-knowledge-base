---
title: Standards Templates Directory
standard_id: UA-DOC-TEMPLATES-README # Changed standard_id
aliases:
  - Templates README
tags:
  - status/active
  - content-type/documentation # Assuming 'documentation' is valid, alt 'guide-document'
  - topic/readme
  - kb-id/standards # Assuming kb-id/standards is a valid tag for this context
kb-id: "kb-id/standards" # Corrected kb-id format
info-type: "guide-document" # Confirmed info-type
primary-topic: Overview and guidance for the templates directory and its contents.
related-standards: []
version: 1.0.0
date-created: '2025-06-01T11:33:47Z'
date-modified: '2025-06-01T11:33:47Z' # Will be updated by CI upon commit
primary_domain: "UA" # Changed primary_domain
sub_domain: "DOCUMENTATION" # Changed sub_domain
scope_application: Provides an overview for the /app/master-knowledge-base/standards/templates directory.
criticality: "P3-Low" # Changed criticality
lifecycle_gatekeeper: No-Gatekeeper
impact_areas:
  - documentation
  - usability
change_log_url: https://example.com/placeholder-changelog-url # Changed change_log_url
---

# Standards Templates Directory

This directory (`/master-knowledge-base/standards/templates/`) contains template files designed to assist authors in creating new, standards-conformant documents for the knowledge base ecosystem. Using these templates provides a consistent starting point and helps ensure that all necessary metadata and structural elements are considered from the outset.

## Purpose

The primary purpose of these templates is to:
- Promote consistency across all documented standards and related artifacts.
- Simplify the creation process for new documents.
- Ensure adherence to core structural and metadata standards, particularly `[[MT-SCHEMA-FRONTMATTER]]`.
- Reduce errors and omissions in document setup.

## Available Templates

Currently, the following templates are available:

1.  **`UA-TPL-CANONICAL-FRONTMATTER.MD`**:
    *   **Purpose:** Provides the standard YAML frontmatter structure required for all new Markdown documents, especially for standards, policies, and guides. It includes all mandatory keys as defined in `[[MT-SCHEMA-FRONTMATTER]]`, along with placeholders and comments to guide the author.
    *   **When to use:** Use this as the starting point for the frontmatter of any new standard, policy, or detailed guide document.

2.  **`UA-TPL-STANDARD-DEFINITION.MD`**:
    *   **Purpose:** Provides a full template for creating new standard definition documents. It includes the canonical frontmatter and a basic Markdown body structure with common sections like Purpose, Scope, Rules & Guidelines, and Cross-References.
    *   **When to use:** When creating a new document that defines a standard.

3.  **`UA-TPL-POLICY-DOCUMENT.MD`**:
    *   **Purpose:** Provides a full template for creating new policy documents. It includes the canonical frontmatter and a basic Markdown body structure with common sections like Purpose & Rationale, Scope, Policy Statements, Responsibilities, and Cross-References.
    *   **When to use:** When creating a new document that defines a policy.

4.  **`UA-TPL-CHANGELOG-DOCUMENT.MD`**:
    *   **Purpose:** Provides a template for creating changelog documents that track modifications to a specific standard or document. It includes the necessary frontmatter for a changelog.
    *   **When to use:** When creating a dedicated changelog file for another standard or important document. The `change_log_url` in the parent document should then point to this file.

> [!NOTE]
> Other templates that have been aligned and renamed:
> - `UA-TPL-ANALYSIS-REPORT.MD`: A template for structuring analysis reports. (Formerly `analysis-report-template.md`)
> - `UA-TPL-ROADMAP.MD`: A template for outlining roadmaps. (Formerly `roadmap-template.md`)
> These are now aligned with the `UA-TPL-*` series frontmatter and naming conventions.

## Maintenance

These templates should be regularly reviewed and updated to ensure they remain aligned with the latest versions of core standards, especially `[[MT-SCHEMA-FRONTMATTER]]` and any relevant structural standards (e.g., `[[AS-STRUCTURE-DOC-CHAPTER]]`). If core standards evolve, these templates MUST be updated accordingly.
