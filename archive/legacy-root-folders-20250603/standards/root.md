---
title: Universal Knowledge Base Standards - Overview - DEPRECATED
aliases:
- Standards KB Root
- KB Standards Overview
- UKBS Root
tags:
- content-type/standard-overview-document
- criticality/p0-critical
- kb-id/standards
- status/deprecated
- topic/meta-structure
- topic/standards-governance
kb-id: standards
info-type: standard-overview-document
primary-topic: Root entry point and guide to Universal KB Standards, outlining purpose,
  meta-structure for standard definitions, and master Table of Contents.
related-standards:
- AS-ROOT-STANDARDS-KB
version: 1.3.0
date-created: '2025-05-15T00:00:00Z'
date-modified: '2025-06-17T02:29:13Z'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: [[AS-ROOT-STANDARDS-KB]].

> [!WARNING] DEPRECATED: This Document is No Longer Active
> **Reason for Deprecation:** This document has been superseded by [[AS-ROOT-STANDARDS-KB]], which serves as the main entry point for the Standards Knowledge Base.
> Please refer to the new root document for navigation and current information. This document is retained for historical purposes only.

# Universal Knowledge Base Standards - Root

This document serves as the entry point and guide to the Universal Knowledge Base Standards. It outlines the overall purpose, the meta-structure used for defining each standard, and provides a master Table of Contents for navigating the core standards documents.

## II. Meta-Structure for Standard Definitions

Each standard defined below adheres to the following structure:

A heading (H3 or lower) indicates the start of a standard definition. Immediately following this heading, a Markdown table provides metadata for the standard:

| Metadata        | Value                                                                                                                                                                                             |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Standard ID     | A unique identifier (e.g., `U-ARCH-001`, `M-SYNTAX-LISTS-001`). Prefixes: `U-` (Universal), `M-` (Markdown Syntax), `O-` (Obsidian Usage). KB-Specific prefixes are defined per KB (e.g., `R-` for Research). |
| Standard Name   | A concise, descriptive name.                                                                                                                                                                      |
| Standard Category | The broader area this standard falls under.                                                                                                                                                       |

Following the metadata table, the standard's details are provided:

**Rule/Guideline Statement(s):** Presented in a table.

| Rule # | Statement of Rule                                                        | Example (if illustrative)                    | Notes / Further Specification (if any)          |
| :----- | :----------------------------------------------------------------------- | :------------------------------------------- | :---------------------------------------------- |
| X.Y    | Concrete, actionable rule...                                             | `example-of-application`                     | Clarification or detail...                      |

**Illustrative Examples (Overall):** Broader examples demonstrating the standard in context, if not covered sufficiently by the rules table.

**Cross-References to Other Standard IDs:** Links to related standards using wikilink format (e.g., [[COL-ARCH-UNIVERSAL#Standard: Master KB Directory and Unique KB Identification (U-ARCH-002)|U-ARCH-002]] or [Link Text to Heading](#heading-id)).

## III. Core Operational Model: Source-and-Render

This knowledge base system employs a "source-and-render" operational model, particularly concerning features like Key-Based Referencing (Keyrefs).

-   **Source Documents:** The primary, editable versions of content are authored with placeholders for dynamic values (e.g., keyrefs like `{{key.productName}}`). These source files reside in the `master-knowledge-base` directory structure. This is the "backend" where all canonical content and logic are maintained.
-   **Rendered Documents:** For consumption by humans (for a consistent view) and by LLMs (which require fully resolved text), a "Resolver Script" processes the source documents and key definitions. This script generates a parallel set of fully populated documents where all placeholders are replaced with their actual values. These rendered documents are stored in a separate `master-knowledge-base-rendered` directory. This is the "frontend" for reading and LLM processing.
-   **Workflow:** Edits are made to source documents. The Resolver Script is run (manually or via automation) to update the rendered documents. Both humans and LLMs primarily consume content from the `master-knowledge-base-rendered` directory for comprehension tasks. LLMs generating new content that should include placeholders will be instructed to use the defined syntax, and their output will be saved to the source directory.

This model ensures that the benefits of maintainability from features like keyrefs are preserved in the source, while providing clean, fully resolved content for all consumers. For detailed guidance on applying standards to specific activities, please refer to the [[GUIDE-TASK-BASED|Task-Based Guide to Knowledge Base Standards]].

## Master Table of Contents for Standards Documents

- [[COL-ARCH-UNIVERSAL|Universal Architecture and Structure Standards]]
- [[COL-CONTENT-UNIVERSAL|Universal Content and Schemas Standards]]
- [[COL-LINKING-UNIVERSAL|Universal Linking, Metadata, and Utility Standards]]
- [[COL-GOVERNANCE-UNIVERSAL|Universal Governance and Support Standards]]
- [[COL-SYNTAX-MARKDOWN|Markdown Syntax Conventions]]
- [[COL-TOOLING-OBSIDIAN|Obsidian Usage Conventions]]
- [[../../_backup/master-knowledge-base-backup/standards/KB-Specific-Standards/_overview|KB-Specific Standards Overview]]
- [[U-KEYREF-SYNTAX-001|Key-Based Referencing Syntax (U-KEYREF-SYNTAX-001)]]
- [[U-KEYREF-MANAGEMENT-001|Key-Based Referencing Management (U-KEYREF-MANAGEMENT-001)]]
- [[M-CONDITIONAL-TEXT-SYNTAX-001|Markdown Syntax for Conditional Text (M-CONDITIONAL-TEXT-SYNTAX-001)]]
- [[../../_backup/master-knowledge-base-backup/standards/U-PROFILING-ATTRIBUTES-001|Profiling Attributes and Values (U-PROFILING-ATTRIBUTES-001)]]
- [[U-SCHEMA-REFERENCE-001|Content Schema for "Reference Topics" (U-SCHEMA-REFERENCE-001)]]
- [[U-SCHEMA-TASK-001|Content Schema for "Task Topics" (U-SCHEMA-TASK-001)]]
- [[U-ARCH-003-Directory-Structure-Source-Render|Directory Structure for Source and Rendered Content (U-ARCH-003)]]
- [[LLM-AUTOMATION-IO-SCHEMA-001|LLM Automation Input/Output Schemas (LLM-AUTOMATION-IO-SCHEMA-001)]]
- [[../../_backup/master-knowledge-base-backup/standards/LLM-PROMPT-LIBRARY-001|LLM Prompt Library Management (LLM-PROMPT-LIBRARY-001)]]
- [[U-RELTABLE-DEFINITION-001|Relationship Table Definition (U-RELTABLE-DEFINITION-001)]]
- [[U-VALIDATION-METADATA-001|Metadata Value Validation (U-VALIDATION-METADATA-001)]]
- [[U-PUBLISHING-PIPELINE-OVERVIEW-001|Publishing Pipeline Overview (U-PUBLISHING-PIPELINE-OVERVIEW-001)]]
- [[M-SYNTAX-TODO-001|Markdown Syntax for TODO Items (M-SYNTAX-TODO-001)]]
- [[U-METADATA-FRONTMATTER-RULES-001|Standard: Frontmatter Structure and Content Rules (U-METADATA-FRONTMATTER-RULES-001)]]
- [[GLOSSARY-STANDARDS-TERMS|Glossary of Standards Terminology]]
- [[../../_backup/master-knowledge-base-backup/standards/O-USAGE-DATAVIEW-001|Obsidian Dataview Usage (O-USAGE-DATAVIEW-001)]]
- [[U-METADATA-SLUG-KEY-001|Slug YAML Key for URLs (U-METADATA-SLUG-KEY-001)]]
- [[GUIDE-KB-USAGE-AND-STANDARDS|Guide: Knowledge Base Usage and Standards (U-ONBOARDING-001)]]

## TODO for Future Standards Development

This section tracks planned additions or enhancements to the standards.

- Max folder nesting depth guideline (for `U-ONBOARDING-001` or `U-ARCH-BESTPRACTICES-001`).
- Linting for standards adherence (long-term consideration).
- Periodic review process for standards (part of `U-GOVERNANCE-001`).
