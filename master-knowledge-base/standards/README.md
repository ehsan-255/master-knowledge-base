---
title: Standards Knowledge Base Directory
standard_id: DOC-STANDARDS-README
aliases:
  - Standards README
tags:
  - status/active
  - content-type/documentation
  - topic/readme
  - kb-id/standards
kb-id: standards
info-type: guide-document
primary-topic: Overview and guidance for the standards directory and its contents.
related-standards: []
version: 1.0.0
date-created: '2025-06-01T11:33:47Z'
date-modified: '2025-06-01T11:33:47Z'
primary_domain: GM
sub_domain: GUIDE
scope_application: Provides an overview for the /app/master-knowledge-base/standards/README.md.
criticality: P4-Informational
lifecycle_gatekeeper: No-Gatekeeper
impact_areas:
  - documentation
  - usability
change_log_url: ./README-CHANGELOG.MD
---

# Standards Knowledge Base Directory

This directory (`/standards`) houses the core knowledge base dedicated to defining and managing standards, policies, guidelines, and supporting documentation for the overall knowledge management ecosystem.

The primary goal of this knowledge base is to ensure consistency, quality, and interoperability across all managed knowledge domains. It follows a Single-Source Multi-View (SSMV) architectural principle, where atomic standards documents are the single source of truth, which can then be aggregated or referenced in various views or contexts.

## Directory Structure

The `/standards` knowledge base is organized into the following primary subdirectories:

*   **`src/`**:
    *   Contains the source Markdown files for all atomic (individual) standards, policies, and guidelines. Each document here represents a specific rule, definition, or procedure.
    *   These are the foundational building blocks of the knowledge management framework.

*   **`registry/`**:
    *   Contains YAML (`.yaml`) and Markdown (`.md`) files that define controlled vocabularies, glossaries, and registries.
    *   Examples include:
        *   `domain_codes.yaml`: Defines allowed primary domain codes.
        *   `subdomain_registry.yaml`: Defines allowed sub-domain codes per primary domain.
        *   `tag-glossary-definition.md`: Provides definitions for all official tags used across knowledge bases.
    *   These registries are crucial for maintaining metadata consistency and enabling automation.

*   **`templates/`**:
    *   Contains template files to aid in the creation of new standards documents and other content types.
    *   These templates ensure that new documents adhere to the required frontmatter schema and structural conventions from the outset.
    *   Examples include:
        *   `tpl-canonical-frontmatter.md`: A template for the YAML frontmatter block.
        *   Templates for specific standard document structures (if developed).

## Core Principles

*   **Atomicity:** Standards are broken down into the smallest reasonable units to promote reusability and clarity.
*   **Clarity and Precision:** Standards are written to be unambiguous and easily understandable.
*   **Centralization:** This directory serves as the central point of reference for all governance-related documentation.
*   **Version Control:** All standards and supporting documents are version-controlled using Git to track changes and manage their lifecycle.

Refer to individual standards within the `src/` directory for specific rules and guidelines. The `[[kb-id/standards]]` tag should be used on all documents within this knowledge base, and the `kb-id: "standards"` frontmatter key should be set accordingly.
The master index for this KB can be found at `[[AS-STRUCTURE-MASTER-KB-INDEX]]` (once created, assuming it points to a `kb-directory.md` or similar).
