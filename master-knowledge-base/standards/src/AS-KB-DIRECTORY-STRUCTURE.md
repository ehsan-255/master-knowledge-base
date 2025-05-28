---
title: "Knowledge Base Directory Structure Standard"
standard_id: "AS-KB-DIRECTORY-STRUCTURE"
aliases: ["Directory Structure", "Folder Organization"]
tags:
  - status/draft
  - criticality/P1-High
  - content-type/technical-standard
kb-id: "" # This standard is intended to be part of the global standards
info-type: "standard-definition"
primary-topic: "Directory Structure" # More descriptive primary topic
related-standards: [] # Optional: e.g., ["SF-CONVENTIONS-NAMING"]
version: "0.1.0"
date-created: "2024-07-15T10:00:00Z" # Placeholder for actual creation date
date-modified: "2024-07-15T10:00:00Z" # Placeholder for actual modification date
primary_domain: "AS" # Architectural Standards
sub_domain: "STRUCTURE" # Structural Standards
scope_application: "Overall repository and knowledge base file organization."
criticality: "P1-High" # As specified in tags
lifecycle_gatekeeper: "Architect-Review" # Standard gatekeeper for technical standards
impact_areas: ["Authoring workflow", "Build process", "Navigation"]
change_log_url: "./AS-KB-DIRECTORY-STRUCTURE-changelog.md" # Placeholder for changelog file
---

# AS-KB-DIRECTORY-STRUCTURE: Knowledge Base Directory Structure Standard

## 1. Overview

This standard defines the official directory structure for the master knowledge base. A consistent directory structure is crucial for organization, navigability, and automation.

## 2. Top-Level Organization

The primary content and operational files for the knowledge base are organized under a root directory named `master-knowledge-base/`.

## 3. Core Directories for Standards Development

Within `master-knowledge-base/standards/`, the following specialized directories are used:

*   **`/master-knowledge-base/standards/src/` (Task 0.4.1)**
    *   **Purpose:** This is the primary Layer 1 directory for all atomic standard documents (Standard Definitions, Policy Documents, Guide Documents, etc.).
    *   **Content:** Individual Markdown files (`.md`) representing single, atomic standards.
    *   **Naming:** Files in this directory MUST follow the [File Naming Convention]([[SF-CONVENTIONS-NAMING#Atomic File Naming Convention]]) (Note: Link to be updated once actual naming convention doc ID is set).

*   **`/master-knowledge-base/standards/registry/` (Task 0.4.2)**
    *   **Purpose:** This directory houses all controlled vocabulary manifests and registry definition files.
    *   **Content:** YAML files (`.yaml`) or Markdown files (`.md`) that define terms, codes, and their meanings for various metadata fields (e.g., domain codes, status tags, criticality levels).
    *   **Examples:** `domain_codes.yaml`, `tag-glossary-definition.md`.

*   **`/master-knowledge-base/standards/templates/` (Task 0.4.3)**
    *   **Purpose:** This directory contains standard templates for creating new documents.
    *   **Content:** Markdown files (`.md`) serving as boilerplate structures.
    *   **Naming:** Template filenames MUST be prefixed with `tpl-` (e.g., `tpl-canonical-frontmatter.md`, `tpl-standard-definition.md`).

## 4. Tooling and Automation Directory

*   **`/master-knowledge-base/tools/`**
    *   **Purpose:** This directory contains scripts and tooling used for validation, indexing, building, or other automation tasks related to the knowledge base.
    *   **Sub-directories:** May include `linter/`, `indexer/`, `builder/`, `validators/` for organization.
    *   **Examples:** `linter/kb_linter.py`, `indexer/generate_index.py`.

## 5. Other Key Directories (Illustrative - To Be Expanded)

*   **`/master-knowledge-base/assets/`**
    *   **Purpose:** For storing static assets like images, diagrams, or other binary files referenced in documents.
*   **`/dist/` or `/build/` (outside `master-knowledge-base/`, typically gitignored)**
    *   **Purpose:** Output directory for generated views, compiled sites, or other build artifacts.

This document will be updated as the directory structure evolves.
```
