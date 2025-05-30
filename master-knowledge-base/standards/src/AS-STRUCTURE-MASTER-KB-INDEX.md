---
title: "Standard: Master Knowledge Base Directory and Index Structure"
standard_id: "AS-STRUCTURE-MASTER-KB-INDEX"
aliases: ["Master KB Index", "KB Directory File"]
tags:
  - status/draft
  - criticality/P1-High
  - content-type/technical-standard
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "Master KB Directory and Index"
related-standards: ["CS-POLICY-KB-IDENTIFICATION", "AS-KB-DIRECTORY-STRUCTURE"]
version: '1.0.0'
date-created: "2024-07-15T12:00:00Z"
date-modified: "2025-05-30T12:00:00Z"
primary_domain: "AS"
sub_domain: "STRUCTURE"
scope_application: "Defines the structure for the master directory housing all KBs and the requirements for the `kb-directory.md` master index file."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["KB discovery", "Repository organization", "Automated KB listing", "Inter-KB navigation"]
change_log_url: "./AS-STRUCTURE-MASTER-KB-INDEX-changelog.md"
---
# Standard: Master Knowledge Base Directory and Index Structure (AS-STRUCTURE-MASTER-KB-INDEX)

This standard defines the structural requirements for the master directory that houses all Knowledge Bases (KBs) and the specific requirements for the `kb-directory.md` master index file.

## 1. Rules for Master Directory and Index

### Rule 1.1: Single Master Directory (Derived from U-ARCH-002, Rule 2.1)
All individual Knowledge Bases (KBs) MUST reside within a single, master top-level directory in the repository.
*   **Example:** `/digital-brain-vault/`
*   **Notes:** The specific name of this master directory (e.g., `digital-brain-vault`, `knowledge-bases`) can be chosen as per project preference, but its singular existence is mandatory. This directory is typically the root for all KB content. Refer to [[AS-KB-DIRECTORY-STRUCTURE]] for how this fits into the broader repository structure.

### Rule 1.2: Master Index File (`kb-directory.md`) Existence (Derived from U-ARCH-002, Rule 2.3)
A master index file, named `kb-directory.md`, MUST reside directly within the master top-level directory.
*   **Example:** `/digital-brain-vault/kb-directory.md`
*   **Notes:** This file serves as the central directory or "yellow pages" for all KBs within the repository. Its naming MUST be exactly `kb-directory.md`.

### Rule 1.3: Content Requirements for `kb-directory.md` (Derived from U-ARCH-002, Rule 2.4)
The `kb-directory.md` file MUST:
    a.  List all active Knowledge Bases within the repository.
    b.  Provide a concise (typically 1-3 sentences) description of the primary scope and purpose of each listed KB.
    c.  Include a direct link to the `root.md` file of each listed KB.
*   **Notes:**
    *   Links MUST use the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]].
    *   The order of KBs listed in `kb-directory.md` should be logical, potentially alphabetical or grouped by a strategic theme.

## 2. Illustrative Example

### Snippet from `/digital-brain-vault/kb-directory.md`

```markdown
# Knowledge Base Directory

This directory provides an overview and access points to all active Knowledge Bases.

## Available Knowledge Bases

- **[Research Methodology KB](./research-methodology-kb/root.md)**: Focuses on research design, data collection, analysis, and open science practices for generating complex workflows. Excludes funding and ethics.
- **[Prompt Engineering KB](./prompt-engineering-kb/root.md)**: Covers principles, techniques, and frameworks for designing effective prompts for Large Language Models, including prompt construction, optimization, and management.
- **[Standards Development KB](./standards-kb/root.md)**: Contains all standards, policies, and guidelines for creating, managing, and governing content within the knowledge ecosystem.
```
*(Note: The example links above are illustrative path-based links. Per [[SF-LINKS-INTERNAL-SYNTAX]], these should ideally be `[[STANDARD_ID]]` or `[[FILENAME_ID_PLACEHOLDER]]` links if the KBs themselves or their root files have resolvable IDs, or be relative paths as shown if direct file linking is intended here.)*

## 3. Cross-References
- [[CS-POLICY-KB-IDENTIFICATION]] - Policy for unique KB identification and naming.
- [[AS-KB-DIRECTORY-STRUCTURE]] - Defines the broader repository and `master-knowledge-base` directory structures.
- [[SF-LINKS-INTERNAL-SYNTAX]] - Internal Linking Syntax Standard.
- [[SF-CONVENTIONS-NAMING]] - File and Folder Naming Conventions (relevant for KB folder names).

---
*This standard (AS-STRUCTURE-MASTER-KB-INDEX) is based on rules 2.1, 2.3, and 2.4 previously defined in U-ARCH-002 from COL-ARCH-UNIVERSAL.md.*
