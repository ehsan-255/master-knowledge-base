---
title: 'Collection: Universal Governance and Support Standards'
aliases:
- Universal Governance Standards
- COL-GOVERNANCE-UNIVERSAL
tags:
- content-type/standards-collection
- kb-id/standards
- status/deprecated
- topic/governance
- topic/support-docs
kb-id: standards
info-type: standards-collection
primary-topic: 'DEPRECATED: Collection of universal standards for versioning, governance, deprecation, onboarding, glossaries, templates, and file hygiene.'
related-standards:
- OM-VERSIONING-CHANGELOGS
- OM-POLICY-STANDARDS-GOVERNANCE
- OM-POLICY-STANDARDS-DEPRECATION
- GM-MANDATE-KB-USAGE-GUIDE
- GM-MANDATE-STANDARDS-GLOSSARY
- AS-STRUCTURE-TEMPLATES-DIRECTORY
- SF-FORMATTING-FILE-HYGIENE
version: 0.4.0
date-created: '2025-05-15'
date-modified: '2025-06-01T23:50:44Z'
---
**DEPRECATED:** This collection document is superseded by the new atomic standards architecture. Relevant content has been refactored into individual standard, policy, and guide documents located in `/master-knowledge-base/standards/src/`. Please refer to `[[AS-ROOT-STANDARDS-KB]]` for an overview of the new standards or consult `[[GM-GUIDE-KB-USAGE]]`.

# Universal Governance and Support Standards

This document outlines universal standards related to the versioning of standards, governance processes for updating them, deprecation policies, and supporting documentation like onboarding guides, glossaries, and template directories.

## Table of Contents

- [[#Standard: Versioning and Changelogs for Standard Files (U-VERSIONING-001)]]
- [[#Standard: Governance - Proposing and Updating Standards (U-GOVERNANCE-001)]]
- [[#Standard: Deprecation Policy for Standards (U-DEPRECATION-001)]]
- [[#Standard: "How to Use These Standards" Guide (U-ONBOARDING-001)]]
- [[#Standard: Glossary for the Standards Document (U-GLOSSARY-001)]]
- [[#Standard: Templates Directory (U-TEMPLATES-DIR-001)]]
- [[#Standard: File Hygiene (U-FILEHYGIENE-001)]]

## Standard: Versioning and Changelogs for Standard Files (U-VERSIONING-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-VERSIONING-001`                    |
| Standard Name   | Versioning and Changelogs for Standard Files |
| Standard Category | Governance & Versioning                |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Each individual standard definition file (e.g., `U-ARCH-001.md` if fully refactored) or compiled standards document (e.g., `01-...md`) MUST include `version` and `date-modified` keys in its YAML frontmatter. | `version: 1.1`<br>`date-modified: 2024-07-15`             | `date-created` is also mandatory per [[05-Markdown-Syntax-Conventions#Standard: Markdown YAML Frontmatter (M-SYNTAX-YAML-001)|M-SYNTAX-YAML-001]]. |
| 1.2    | The `version` key MUST use semantic versioning (e.g., MAJOR.MINOR.PATCH like `1.0.0`, `1.1.0`, `2.0.0`). Increment appropriately with changes.    | Initial draft: `0.1`. First final: `1.0.0`. Minor fix: `1.0.1`. |                                                                              |
| 1.3    | A "Changelog" section (H2 or H3, depending on context within the standard file/document) MUST be maintained within each standard definition file or at the end of compiled standards documents. | `### Changelog\n- 2024-07-15 (v1.1): Clarified Rule X.Y.` | Lists version, date, and brief description of changes.                     |

**Cross-References to Other Standard IDs:** [[COL-SYNTAX-MARKDOWN#Standard: Markdown YAML Frontmatter (M-SYNTAX-YAML-001)|M-SYNTAX-YAML-001]]

## Standard: Governance - Proposing and Updating Standards (U-GOVERNANCE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-GOVERNANCE-001`                    |
| Standard Name   | Governance - Proposing and Updating Standards |
| Standard Category | Governance & Versioning                |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                                  | Example (if illustrative)                               | Notes / Further Specification (if any)                                       |
| :----- | :------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ | :--------------------------------------------------------------------------- |
| 1.1    | A defined process for proposing new standards or changes to existing standards MUST be documented (e.g., within the `U-ONBOARDING-001` guide or a dedicated governance note). | "Submit proposal via issue tracker..."          | This standard mandates that such a process *exists* and is documented.     |
| 1.2    | Proposed changes MUST undergo a review process before being incorporated into the official standards.                                                | N/A                                                     | The nature of the review (e.g., peer, SME) should be part of the documented process. |
| 1.3    | The `tag-glossary.md` and any master Table of Contents documents MUST be updated promptly when standards are added, modified, or deprecated.        | New standard added -> update ToCs.                      | Maintains consistency.                                                       |

**Cross-References to Other Standard IDs:** [[COL-GOVERNANCE-UNIVERSAL#Standard: "How to Use These Standards" Guide (U-ONBOARDING-001)|U-ONBOARDING-001]], [[COL-LINKING-UNIVERSAL#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]]

## Standard: Deprecation Policy for Standards (U-DEPRECATION-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-DEPRECATION-001`                   |
| Standard Name   | Deprecation Policy for Standards      |
| Standard Category | Governance & Versioning                |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | When a standard is superseded or no longer relevant, it MUST be marked as deprecated rather than deleted outright, to maintain historical context. | N/A                                                          |                                                                              |
| 1.2    | Deprecated standards MUST have their `status/*` tag in YAML frontmatter changed to `status/deprecated` or `status/archived`.                      | `tags:\n  - status/deprecated`                               | Per [[03-Universal-Linking-Metadata-And-Utility#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]].                                                 |
| 1.3    | The body of a deprecated standard MUST be prefaced with a clear "DEPRECATED" notice, stating the reason for deprecation and linking to any replacing standard(s). | `> [!WARNING] DEPRECATED\n> This standard is superseded by [[Standards/U-NEW-STANDARD|U-NEW-STANDARD]]. Reason: ...` | Uses Obsidian callout syntax (see [[06-Obsidian-Usage-Conventions#Standard: Obsidian Callout Usage (O-USAGE-CALLOUTS-001)|O-USAGE-CALLOUTS-001]]). |
| 1.4    | Deprecated standards SHOULD be moved to a designated "archive" section or folder within the Standards KB structure after a notice period.         | `Standards/Archive/U-OLD-STANDARD.md`                        |                                                                              |

**Cross-References to Other Standard IDs:** [[COL-LINKING-UNIVERSAL#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]], [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Callout Usage (O-USAGE-CALLOUTS-001)|O-USAGE-CALLOUTS-001]]

## Standard: "How to Use These Standards" Guide (U-ONBOARDING-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-ONBOARDING-001`                    |
| Standard Name   | "How to Use These Standards" Guide   |
| Standard Category | Support & Onboarding                   |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                               | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ | :--------------------------------------------------------------------------- |
| 1.1    | A dedicated document titled 'Guide: Knowledge Base Usage and Standards' (filename: `GUIDE-KB-USAGE-AND-STANDARDS.md`) MUST exist within the `./master-knowledge-base/Standards/` directory.                            | This standard defines its existence.                    | This file is the primary onboarding and usage guide for the Standards KB. |
| 1.2    | This guide MUST explain the purpose of the standards, how to navigate them (e.g., using the `kb-directory.md` and ToCs), and how to find specific rules, now pointing to the comprehensive onboarding guide. | N/A                                                     | See [[Standards/GUIDE-KB-USAGE-AND-STANDARDS|Guide: Knowledge Base Usage and Standards (U-ONBOARDING-001)]]. |
| 1.3    | It MUST briefly outline the process for proposing changes or asking for clarifications (linking to `U-GOVERNANCE-001` details).                 | "For proposals, see [[U-GOVERNANCE-001|Governance Process]]." |                                                                              |
| 1.4    | It SHOULD include a pointer to the `tag-glossary.md` and any templates directory.                                                               | "Refer to the [[tag-glossary-definition.md|Tag Glossary]]."         |                                                                              |

**Cross-References to Other Standard IDs:** [[COL-GOVERNANCE-UNIVERSAL#Standard: Governance - Proposing and Updating Standards (U-GOVERNANCE-001)|U-GOVERNANCE-001]], [[../tag-glossary-definition|Tag Glossary]]

## Standard: Glossary for the Standards Document (U-GLOSSARY-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-GLOSSARY-001`                      |
| Standard Name   | Glossary for the Standards Document   |
| Standard Category | Support & Onboarding                   |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                               | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ | :--------------------------------------------------------------------------- |
| 1.1    | A glossary defining key terms used *within the standards documents themselves* (e.g., "monolith," "atomic," "schema," "kebab-case") MUST be maintained in the file `./master-knowledge-base/Standards/GLOSSARY-STANDARDS-TERMS.md`. | "Kebab-case: A naming convention..."                  | This is distinct from `tag-glossary.md`. Could be a section in `00-...md` or its own file. |
| 1.2    | Terms in the glossary MUST be clearly defined.                                                                                                  | N/A                                                     |                                                                              |

**Cross-References to Other Standard IDs:** [[root|Standards Overview]]

## Standard: Templates Directory (U-TEMPLATES-DIR-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-TEMPLATES-DIR-001`                 |
| Standard Name   | Templates Directory                   |
| Standard Category | Support & Onboarding                   |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                               | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ | :--------------------------------------------------------------------------- |
| 1.1    | A dedicated `/templates/` folder SHOULD be maintained within the master top-level directory (`/master-knowledge-base/templates/`) or within each relevant KB. | `/master-knowledge-base/templates/chapter-template.md` | Location depends on whether templates are universal or KB-specific. Universal preferred if applicable. |
| 1.2    | This folder MUST contain Markdown template files for common document types (e.g., "Chapter," "Methodology Description," "Concept Definition") that pre-fill structure according to relevant `U-SCHEMA-...` standards. It MAY also contain utility templates, such as a canonical frontmatter template. | A template file with H2s from `U-SCHEMA-METHOD-001`.<br/>`canonical-frontmatter-template.md` | Users copy these to start new documents or ensure metadata consistency.      |

**Cross-References to Other Standard IDs:** [[COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Methodology/Technique Descriptions" (U-SCHEMA-METHOD-001)|U-SCHEMA-METHOD-001]], [[COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Concept Definitions" (U-SCHEMA-CONCEPT-001)|U-SCHEMA-CONCEPT-001]]

## Standard: File Hygiene (U-FILEHYGIENE-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-FILEHYGIENE-001`                   |
| Standard Name   | File Hygiene                          |
| Standard Category | Support & Onboarding                   |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                               | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ | :--------------------------------------------------------------------------- |
| 1.1    | All Markdown files MUST use LF (Unix-style) line endings.                                                                                       | N/A                                                     | Most modern editors can be configured for this. Prevents issues in Git.    |
| 1.2    | Trailing whitespace at the end of lines MUST be removed.                                                                                        | N/A                                                     | Editors often have settings to auto-remove this.                           |
| 1.3    | Files MUST end with a single newline character at the End-Of-File (EOF).                                                                        | N/A                                                     | POSIX standard; some tools expect this.                                      |

**Cross-References to Other Standard IDs:** [[COL-SYNTAX-MARKDOWN#Standard: Markdown General Formatting (M-SYNTAX-GENERAL-001)|M-SYNTAX-GENERAL-001]]