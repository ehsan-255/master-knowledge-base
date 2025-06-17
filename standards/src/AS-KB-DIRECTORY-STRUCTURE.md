---
title: Knowledge Base Directory Structure Standard
standard_id: AS-KB-DIRECTORY-STRUCTURE
aliases:
- Directory Structure
- Folder Organization
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/as
- topic/structure
kb-id: standards
info-type: standard-definition
primary-topic: Directory Structure
related-standards: []
version: 0.1.0
date-created: '2024-07-15T10:00:00Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: AS
sub_domain: STRUCTURE
scope_application: Overall repository and knowledge base file organization.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Authoring workflow
- Build process
- Navigation
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# AS-KB-DIRECTORY-STRUCTURE: Knowledge Base Directory Structure Standard

## 1. Overview

This standard defines the official directory structure for the master knowledge base as part of a **sophisticated three-layer enterprise architecture**. This document represents the **Physical Layer** of the architecture, focusing on file system organization and storage structures.

**🏗️ ARCHITECTURAL CONTEXT:**
- **Physical Layer (This Document):** File system organization, directory structures, storage patterns
- **Logical/Semantic Layer:** `AS-MAP-STANDARDS-KB.md` (DITA map + ontological structure)
- **Presentation Layer:** `AS-ROOT-STANDARDS-KB.md` (navigation interface)

**⚠️ CRITICAL:** This three-layer separation is **INTENTIONAL SOPHISTICATED DESIGN** inspired by DITA and RDF/OWL principles. Do not consolidate these files.

A consistent directory structure is crucial for organization, navigability, and automation while supporting the broader semantic web and topic-based architecture capabilities.

## 2. Top-Level Organization

The primary content and operational files for the knowledge base are organized under a root directory named `master-knowledge-base/`.

## 3. Core Directories for Standards Development

Within `standards/`, the following specialized directories are used:

*   **`/standards/src/` (Task 0.4.1)**
    *   **Purpose:** This is the primary Layer 1 directory for all atomic standard documents (Standard Definitions, Policy Documents, Guide Documents, etc.).
    *   **Content:** Individual Markdown files (`.md`) representing single, atomic standards.
    *   **Naming:** Files in this directory MUST follow the [[GM-CONVENTIONS-NAMING#Atomic File Naming Convention|File Naming Convention]] (Note: Link to be updated once actual naming convention doc ID is set).

*   **`/standards/registry/` (Task 0.4.2)**
    *   **Purpose:** This directory houses all controlled vocabulary manifests and registry definition files.
    *   **Content:** YAML files (`.yaml`) or Markdown files (`.md`) that define terms, codes, and their meanings for various metadata fields (e.g., domain codes, status tags, criticality levels).
    *   **Examples:** `mt-schema-frontmatter.yaml`, `mt-registry-tag-glossary.yaml`.

*   **`/standards/templates/` (Task 0.4.3)**
    *   **Purpose:** This directory contains standard templates for creating new documents.
    *   **Content:** Markdown files (`.md`) serving as boilerplate structures.
    *   **Naming:** Template filenames MUST be prefixed with `tpl-` (e.g., `tpl-canonical-frontmatter.md`, `tpl-standard-definition.md`).

## 4. Tooling and Automation Directory

*   **`/tools/`**
    *   **Purpose:** This directory contains scripts and tooling used for validation, indexing, building, or other automation tasks related to the knowledge base.
    *   **Sub-directories:** May include `linter/`, `indexer/`, `builder/`, `validators/` for organization.
    *   **Examples:** `linter/kb_linter.py`, `indexer/generate_index.py`.

## 5. Other Key Directories (Illustrative - To Be Expanded)

*   **`/master-knowledge-base/assets/`**
    *   **Purpose:** For storing static assets like images, diagrams, or other binary files referenced in documents.
*   **`/dist/` or `/build/` (outside `master-knowledge-base/`, typically gitignored)**
    *   **Purpose:** Output directory for generated views, compiled sites, or other build artifacts.

This document will be updated as the directory structure evolves.
