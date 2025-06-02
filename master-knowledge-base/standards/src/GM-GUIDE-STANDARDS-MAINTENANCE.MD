---
title: 'Guide: Standards Development & Maintenance Workflow'
standard_id: GM-GUIDE-STANDARDS-MAINTENANCE
aliases:
  - Standards Maintenance Guide
  - KB Development Workflow
tags:
  - status/draft
  - content-type/guide-document
  - topic/governance
  - topic/workflow
kb-id: kb-id/standards
info-type: guide-document
primary-topic: 'Provides guidelines for creating, updating, and maintaining standards documents and using the supporting toolchain.'
related-standards:
  - MT-SCHEMA-FRONTMATTER
  - OM-DOC-TOOLS-LINTER-README
  - OM-DOC-TOOLS-INDEXER-README
  - OM-DOC-TOOLS-BUILDER-README
  - GM-GUIDE-KB-USAGE
  - GM-GUIDE-STANDARDS-BY-TASK
version: '0.1.0'
date-created: '2025-06-02T00:00:00Z' # Replace with current date
date-modified: '2025-06-02T00:00:00Z' # Replace with current date
primary_domain: GM
sub_domain: GUIDE
scope_application: 'Contributors and maintainers of the Standards KB.'
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - standards-development
  - content-quality
  - tool-usage
change_log_url: https://example.com/placeholder-changelog-url # Or ./GM-GUIDE-STANDARDS-MAINTENANCE-CHANGELOG.MD if a changelog is created
---

# Guide: Standards Development & Maintenance Workflow (GM-GUIDE-STANDARDS-MAINTENANCE)

## 1. Introduction

This guide provides a comprehensive overview of the workflow for creating, updating, and maintaining standards documents within the Standards Knowledge Base (KB). It also covers the use of supporting tools to ensure content quality and consistency. Adhering to this workflow is crucial for all contributors and maintainers.

## 2. Key Principles

-   **Atomicity:** Standards should be broken down into the smallest reasonable, self-contained units.
-   **Standard vs. Policy:**
    -   **Standards** define *how* to do something or *what* something should be (e.g., schema definitions, syntax rules, structural requirements). They are often technical or procedural.
    -   **Policies** define *what* is allowed or required, *why* it's important, and *when/where* it applies (e.g., rules for content style, linking strategies, governance processes). They often state rules and rationale.
-   **`[[STANDARD_ID]]` Linking:** All internal links to other standards or documents within the knowledge base ecosystem MUST use the `[[STANDARD_ID]]` or `[[STANDARD_ID|display text]]` format. Path-based links (e.g., `[[../file.md]]`) are not permitted in the body content.

## 3. Adding a New Standard or Policy

### 3.1. Choosing a `standard_id` and Filename
-   Select a concise, descriptive `standard_id` adhering to the format `DOMAIN-TYPE-SUBJECT` (e.g., `AS-SCHEMA-NEW-THING`, `CS-POLICY-CONTENT-STYLE`). Refer to `[[SF-CONVENTIONS-NAMING]]`.
-   The filename MUST match the `standard_id` (e.g., `CS-POLICY-CONTENT-STYLE.MD`).

### 3.2. Using Templates
-   Start with the appropriate template from the `master-knowledge-base/standards/templates/` directory:
    -   For standard definitions: `[[UA-TPL-STANDARD-DEFINITION]]`
    -   For policy documents: `[[UA-TPL-POLICY-DOCUMENT]]`
    -   For base frontmatter: `[[UA-TPL-CANONICAL-FRONTMATTER]]`
-   Copy the chosen template to the relevant `src` directory (usually `master-knowledge-base/standards/src/`) and rename it to your new `STANDARD_ID.MD`.

### 3.3. Filling out Frontmatter
-   Carefully complete all mandatory frontmatter fields. Refer to `[[MT-SCHEMA-FRONTMATTER]]` for detailed descriptions of each field and controlled vocabularies.
-   Pay close attention to `primary_domain`, `sub_domain`, `info-type`, `criticality`, and `status`.

### 3.4. Writing Content
-   Follow the structure provided by the template.
-   Ensure clarity, precision, and adherence to any relevant style guides (e.g., `[[CS-POLICY-TONE-LANGUAGE]]`).

### 3.5. Creating a Changelog
-   For significant new standards or policies, create a corresponding changelog document.
-   Use the `[[UA-TPL-CHANGELOG-DOCUMENT]]` template.
-   The `standard_id` of the changelog should be `[PARENT_STANDARD_ID]-CHANGELOG` (e.g., `CS-POLICY-CONTENT-STYLE-CHANGELOG`).
-   The `change_log_url` in the parent document's frontmatter should point to this changelog file (e.g., `./CS-POLICY-CONTENT-STYLE-CHANGELOG.MD`).
-   Refer to `[[OM-VERSIONING-CHANGELOGS]]` for versioning and changelog best practices.

## 4. Updating an Existing Standard or Policy

### 4.1. Modifying Content
-   Make necessary changes to the body or frontmatter of the document.

### 4.2. Frontmatter Updates
-   Update the `date-modified` field to the current date.
-   Increment the `version` number according to SemVer principles (see `[[OM-VERSIONING-CHANGELOGS]]`).
    -   Major change (backward-incompatible): Increment MAJOR version (e.g., 1.2.3 to 2.0.0).
    -   Minor change (backward-compatible new feature): Increment MINOR version (e.g., 1.2.3 to 1.3.0).
    -   Patch change (backward-compatible bug fix/typo): Increment PATCH version (e.g., 1.2.3 to 1.2.4).

### 4.3. Changelog Entry
-   Add a new entry to the corresponding changelog document detailing the changes, the date, and the new version number.

## 5. Using Local Tools

These tools are located in `master-knowledge-base/tools/`. Run them from the repository root.

### 5.1. Linter (`kb_linter.py`)
-   Validates documents against schema, style, and link integrity.
-   **Example:** To lint all content in the main `src` directory:
    ```bash
    python master-knowledge-base/tools/linter/kb_linter.py --repo-base . --directory master-knowledge-base/standards/src --fail-on-errors --output master-knowledge-base/tools/reports/linter_report_src_local.md
    ```
-   Review the output report for errors and warnings. See `[[OM-DOC-TOOLS-LINTER-README]]` for more details.

### 5.2. Indexer (`generate_index.py`)
-   Generates the `master-knowledge-base/dist/standards_index.json` file, which is used by the linter for link validation and by other tools.
-   Run this after adding new documents or changing `standard_id`s.
-   **Example (to index all relevant content areas):**
    ```bash
    python master-knowledge-base/tools/indexer/generate_index.py --repo-base . --src-dirs master-knowledge-base/standards/src master-knowledge-base/standards/registry master-knowledge-base/standards/templates master-knowledge-base/tools master-knowledge-base --output-dir master-knowledge-base/dist --log-level INFO
    ```
-   See `[[OM-DOC-TOOLS-INDEXER-README]]` for more details.

### 5.3. Collection Builder (`generate_collections.py`)
-   Generates derived collection views based on definitions in `collection_definitions.yaml`.
-   **Example:**
    ```bash
    python master-knowledge-base/tools/builder/generate_collections.py --repo-base . --log-level INFO
    ```
-   Output is to `master-knowledge-base/dist/collections/`. See `[[OM-DOC-TOOLS-BUILDER-README]]` for more details.

## 6. CI/CD Pipeline Overview

-   The repository includes a GitHub Actions workflow defined in `.github/workflows/standards_check.yml`.
-   This workflow automatically runs on pushes and pull requests to the `main` branch.
-   It performs:
    1.  Dependency installation.
    2.  Standards Linter execution across the entire `master-knowledge-base`.
    3.  Standards Indexer execution.
    4.  JSON Schema validation of the generated index.
    5.  Collection Builder execution.
-   If the linter (with `--fail-on-errors`) or any other crucial script fails, the workflow will fail, preventing merges with errors.
-   Artifacts like the linter report, standards index, and collections are uploaded for review.

## 7. Link Management

-   Always use `[[STANDARD_ID]]` or `[[STANDARD_ID|Optional Display Text]]` for internal links.
-   After creating new documents or modifying links, run the indexer and then the linter.
-   The linter report will identify:
    -   "Potentially broken link" warnings if a `[[STANDARD_ID]]` is not found in the `standards_index.json`.
    -   "Path-based link" errors if direct file paths are used in links.

For general KB usage and navigation, refer to `[[GM-GUIDE-KB-USAGE]]`. For task-specific guidance, see `[[GM-GUIDE-STANDARDS-BY-TASK]]`.
