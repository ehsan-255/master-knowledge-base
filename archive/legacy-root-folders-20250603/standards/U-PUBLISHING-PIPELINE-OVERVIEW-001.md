---
title: 'Standard: Publishing Pipeline Overview (U-PUBLISHING-PIPELINE-OVERVIEW-001)
  - DEPRECATED'
tags:
- automation
- content-type/standard-document
- criticality/p0-critical
- kb-id/global
- kb-id/standards
- publishing
- standards-kb/universal
- status/deprecated
- utility-standards
date-created: '2025-05-19T00:00:00Z'
date-modified: '2025-06-17T02:29:13Z'
version: 0.2.0
info-type: standard-document
primary-topic: Describes the conceptual overview of the automated publishing workflow
related-standards:
- OM-OVERVIEW-PUBLISHING-PIPELINE
aliases:
- Publishing Workflow Standard
- KB Export Process
kb-id: archive
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: [[OM-OVERVIEW-PUBLISHING-PIPELINE]].

> [!WARNING] DEPRECATED: This Standard is No Longer Active
> **Reason for Deprecation:** This standard has been superseded by [[OM-OVERVIEW-PUBLISHING-PIPELINE]].
> Please refer to the new standard for current guidelines. This document is retained for historical purposes only.

# Standard: Publishing Pipeline Overview (U-PUBLISHING-PIPELINE-OVERVIEW-001)

This document provides a high-level overview of the intended automated publishing pipeline for the knowledge base system. It outlines the conceptual stages involved in transforming source content into various output formats.

## Table of Contents
- [[#Standard: Conceptual Publishing Workflow (U-PUBLISHING-PIPELINE-OVERVIEW-001)]]
- [[#Key Pipeline Stages]]

## Standard: Conceptual Publishing Workflow (U-PUBLISHING-PIPELINE-OVERVIEW-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-PUBLISHING-PIPELINE-OVERVIEW-001`  |
| Standard Name   | Publishing Pipeline Overview          |
| Standard Category | Publishing & Automation               |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | The publishing pipeline MUST operate on the "rendered" content from the `master-knowledge-base-rendered/` directory as its primary input, or directly on "source" content from `master-knowledge-base/` by incorporating the "Resolver Script" logic as its first stage. | Pipeline starts by reading from `master-knowledge-base-rendered/`. | Ensures keyrefs are resolved and potentially other pre-processing is done.   |
| 1.2    | The pipeline SHOULD be scriptable and automatable to allow for consistent and repeatable builds.                                                | A master script (e.g., Python, shell script, `Makefile`) orchestrates all steps. | Reduces manual effort and errors.                                            |
| 1.3    | The pipeline MUST support filtering of content based on profiling attributes defined in YAML frontmatter and conditional text markers (`M-CONDITIONAL-TEXT-SYNTAX-001`) to produce different output variants. | Building a "novice-only" version of the documentation.       | Core requirement for targeted content delivery.                              |
| 1.4    | The pipeline SHOULD support conversion to common output formats such as HTML (for web) and PDF. Other formats MAY be supported as needed.       | Pandoc for conversion to HTML and PDF.                       | Addresses common publishing needs.                                           |
| 1.5    | Internal wikilinks (Obsidian format, paths from root) MUST be converted to standard relative Markdown links or appropriate HTML links during the transformation process for the target output format. | `[[Standards/U-ARCH-001]]` becomes `standards/u-arch-001.html`. | Handled by tools like `export_vault_with_markdown_links.py` logic or Pandoc filters. |
| 1.6    | The pipeline SHOULD allow for the application of custom styling and templates for different output formats.                                     | CSS for HTML, LaTeX templates for PDF.                       | Ensures brand consistency and professional presentation.                     |

## Key Pipeline Stages

1.  **Content Selection & Preparation**
    *   **Purpose:** To identify and gather the necessary source files from `master-knowledge-base/` for a specific build or output.
    *   **Primary Inputs:** Source directory (`master-knowledge-base/`), build configuration (defining scope).
    *   **Core Actions/Processes:** File gathering based on criteria (e.g., specific KB, tags, modification dates).
    *   **Primary Outputs:** A defined set of source files to be processed.
    *   **Example Tooling/Methods (Conceptual):** Python scripts for file system traversal and filtering, manifest files.

2.  **Keyref Resolution**
    *   **Purpose:** To replace all keyref placeholders (e.g., `{{key.productName}}`) in the selected source content with their defined values from `_key_definitions.md`.
    *   **Primary Inputs:** Selected source files, `_key_definitions.md`.
    *   **Core Actions/Processes:** Parsing content for keyref syntax, looking up values, substituting placeholders.
    *   **Primary Outputs:** Source files with all keyrefs resolved.
    *   **Example Tooling/Methods (Conceptual):** Python scripts with regex or dedicated templating libraries.

3.  **Conditional Content Filtering**
    *   **Purpose:** To include or exclude blocks of content based on profiling attributes (e.g., `audience`, `platform`) to tailor the output for specific targets.
    *   **Primary Inputs:** Keyref-resolved content, active build profile (defining attribute values).
    *   **Core Actions/Processes:** Parsing content for conditional markers (e.g., `> [!IF audience=expert]`), evaluating conditions against the profile, removing or keeping content blocks.
    *   **Primary Outputs:** Content filtered according to the active profile.
    *   **Example Tooling/Methods (Conceptual):** Python scripts that parse Markdown and evaluate conditional logic.

4.  **Link Transformation**
    *   **Purpose:** To convert internal Obsidian wikilinks (paths from root) to standard relative Markdown links or appropriate HTML links suitable for the target output format.
    *   **Primary Inputs:** Filtered content with Obsidian wikilinks.
    *   **Core Actions/Processes:** Identifying wikilinks, resolving their target paths relative to the output structure, rewriting link syntax.
    *   **Primary Outputs:** Content with links transformed for the target publishing environment.
    *   **Example Tooling/Methods (Conceptual):** Python scripts (like `export_vault_with_markdown_links.py` logic), Pandoc filters.

5.  **Format Conversion**
    *   **Purpose:** To convert the processed Markdown content into the desired final output format(s) (e.g., HTML, PDF).
    *   **Primary Inputs:** Transformed Markdown content, styling templates (CSS, LaTeX), conversion tool configurations.
    *   **Core Actions/Processes:** Using a conversion engine to render Markdown into the target format, applying styles and templates.
    *   **Primary Outputs:** Files in the target output format (e.g., HTML files, a PDF document).
    *   **Example Tooling/Methods (Conceptual):** Pandoc, static site generators (MkDocs, Hugo, Jekyll), LaTeX engines.

6.  **Output & Deployment**
    *   **Purpose:** To organize the generated output files and, optionally, deploy them to a distribution point.
    *   **Primary Inputs:** Converted files in the target format.
    *   **Core Actions/Processes:** Assembling files into a final directory structure, copying to a web server, committing to a repository for a static site host.
    *   **Primary Outputs:** Published documentation accessible to end-users.
    *   **Example Tooling/Methods (Conceptual):** File system operations (copy, move), `rsync`, Git deployment, CI/CD pipelines.

**Tooling Considerations (Examples):**
-   Python for scripting (Resolver Script, orchestration).
-   Pandoc for format conversion.
-   Static Site Generators (e.g., MkDocs with Material theme, Hugo) for HTML websites.
-   Git for version control of source and potentially rendered output.
-   CI/CD systems (e.g., GitHub Actions) for automating builds.

**Cross-References to Other Standard IDs:** [[U-ARCH-003-Directory-Structure-Source-Render|U-ARCH-003-Directory-Structure-Source-Render]], [[U-KEYREF-SYNTAX-001|U-KEYREF-SYNTAX-001]], [[M-CONDITIONAL-TEXT-SYNTAX-001|M-CONDITIONAL-TEXT-SYNTAX-001]], [[../scripts/export_vault_with_markdown_links.py]]
