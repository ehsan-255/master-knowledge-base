---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:15Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: archive
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
## CONTRIBUTOR_GUIDE.md Updates Log (Manual Integration Required)

This file contains updates that were intended for `CONTRIBUTOR_GUIDE.md`. Due to issues accessing or reliably updating `CONTRIBUTOR_GUIDE.md` directly, these notes should be manually reviewed and integrated into it at a later stage.

### Decision ID DECISION_002: Refactor KB Standards

**Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment (In Progress)**

-   **Step 1.1: Process `standards/COL-ARCH-UNIVERSAL.md`**
    -   **Overall:** All concepts (U-ARCH-001, U-ARCH-002, U-STRUC-001, U-STRUC-002, U-DETAIL-LEVEL-001, U-FORMAT-NAMING-001) from `COL-ARCH-UNIVERSAL.md` have been processed. The primary finding is that most of these concepts had already been refactore_into_atomic_standards_in `/master-knowledge-base/standards/src/`. Verification of these existing files against the original collection content has been completed.
    -   **Concept U-ARCH-001 (KB Root Structure and Top-Level Part Organization):**
        -   Verified that this concept has already been decomposed into the following atomic standards in `/master-knowledge-base/standards/src/`:
            - `AS-STRUCTURE-KB-ROOT.md` (covers structural definitions)
            - `CS-POLICY-KB-ROOT.md` (covers related policies and guidelines)
        -   The content of these existing files aligns with the requirements for decomposing U-ARCH-001.
    -   **Concept U-ARCH-002 (Master KB Directory and Unique KB Identification):**
        -   Verified that this concept has already been decomposed into the following atomic standards in `/master-knowledge-base/standards/src/`:
            - `AS-STRUCTURE-MASTER-KB-INDEX.md` (defines the structure of the master KB directory and the `kb-directory.md` file)
            - `CS-POLICY-KB-IDENTIFICATION.md` (defines policies for unique KB folder naming and consistent identity declaration in `root.md`)
        -   The content of these existing files aligns with the requirements for decomposing U-ARCH-002.
    -   **Concept U-STRUC-001 (Primary KB Section ("Part") Structure):**
        -   Verified that this concept has already been decomposed and its requirements are met by the following existing atomic standards in `/master-knowledge-base/standards/src/`:
            - `AS-STRUCTURE-KB-PART.md`
            - `CS-POLICY-KB-PART-CONTENT.md`
            - `CS-POLICY-PART-OVERVIEW.md`
        -   The content of these existing files aligns with the requirements for decomposing U-STRUC-001.
        -   Note: The potential `AS-STRUCTURE-PART-OVERVIEW.md` mentioned in roadmap task 1.7.3 seems consolidated into `AS-STRUCTURE-KB-PART.md` for now.
    -   **Concept U-STRUC-002 (Content Document ("Chapter") Internal Structure):**
        -   Verified that this concept has been largely decomposed into the existing atomic standards:
            - `AS-STRUCTURE-DOC-CHAPTER.md`
            - `CS-POLICY-DOC-CHAPTER-CONTENT.md`
            - `CS-TOC-POLICY.md`
        -   The content of these existing files aligns well with the requirements for decomposing U-STRUC-002.
        -   **Action from Roadmap Task 1.7.2 (ToC):** Created new standard `/master-knowledge-base/standards/src/SF-TOC-SYNTAX.md` (ID: `SF-TOC-SYNTAX`) to define the Markdown syntax for Tables of Contents. Updated `master-knowledge-base/standards/src/CS-TOC-POLICY.md` to replace placeholder `[[SF-TOC-SYNTAX_ID_PLACEHOLDER]]` with a direct link `[[SF-TOC-SYNTAX]]`.
    -   **Concept U-DETAIL-LEVEL-001 (Layered Information Presentation):**
        -   Verified that this concept has already been fully decomposed into the existing atomic standard `/master-knowledge-base/standards/src/CS-POLICY-LAYERED-INFORMATION.md`.
    -   **Concept U-FORMAT-NAMING-001 (File and Folder Naming Conventions):**
        -   Verified that this concept has already been comprehensively refactored into the existing atomic standard `/master-knowledge-base/standards/src/SF-CONVENTIONS-NAMING.md`.
    -   **Task 1.1.2 (Mark `COL-ARCH-UNIVERSAL.md` for deprecation):** Verified that `standards/COL-ARCH-UNIVERSAL.md` is already comprehensively marked as deprecated.

### Decision ID DECISION_002: Refactor KB Standards (Continued)

**Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment (In Progress)**

-   **Step 1.2: Process `standards/COL-CONTENT-UNIVERSAL.md`**
    -   **Overall:** All concepts (U-SCHEMA-METHOD-001, U-SCHEMA-CONCEPT-001, U-TONE-LANG-001, U-SCOPE-INCLUDE-001, U-SCOPE-EXCLUDE-001, U-ABSTR-DIGITAL-001) from `COL-CONTENT-UNIVERSAL.md` have been processed.
    -   The collection file `standards/COL-CONTENT-UNIVERSAL.md` is already marked as deprecated and correctly lists its atomic replacements.
    -   Verification confirmed that the following atomic standards exist in `/master-knowledge-base/standards/src/` and accurately reflect the content of their corresponding concepts from the collection file:
        -   `AS-SCHEMA-METHODOLOGY-DESCRIPTION.md` (from U-SCHEMA-METHOD-001)
        -   `AS-SCHEMA-CONCEPT-DEFINITION.md` (from U-SCHEMA-CONCEPT-001)
        -   `CS-POLICY-TONE-LANGUAGE.md` (from U-TONE-LANG-001)
        -   `CS-POLICY-SCOPE-INCLUSION.md` (from U-SCOPE-INCLUDE-001)
        -   `CS-POLICY-SCOPE-EXCLUSION.md` (from U-SCOPE-EXCLUDE-001)
        -   `CS-POLICY-DIGITAL-ABSTRACTION.md` (from U-ABSTR-DIGITAL-001)
    -   No new file creation or modifications were needed for these standards as part of this step.
-   **Step 1.7 (Specific Merging/Refactoring Decisions) - Task 1.7.7 (Conditional Text):**
    -   Verified that the requirements for conditional text syntax and policy are met by existing files:
        -   `master-knowledge-base/standards/src/SF-CALLOUTS-SYNTAX.md` correctly lists `IF` as a callout type.
        -   `master-knowledge-base/standards/src/SF-CONDITIONAL-SYNTAX-ATTRIBUTES.md` defines the `attribute=value` syntax for conditions.
        -   `master-knowledge-base/standards/src/CS-CONTENT-PROFILING-POLICY.md` establishes the policy for content profiling, lists approved attributes/values, and explicitly states it supersedes the older `U-PROFILING-ATTRIBUTES-001.md` (which was not found, as expected).
    -   No new file creation or modifications were needed for this task as it appears to have been completed previously.

### Decision ID DECISION_002: Refactor KB Standards (Continued)

**Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment (In Progress)**

-   **Step 1.2: Process `standards/COL-CONTENT-UNIVERSAL.md` (Continued)**
    -   **Task 1.2.2 (Mark `COL-CONTENT-UNIVERSAL.md` for deprecation):**
        -   Verified that `standards/COL-CONTENT-UNIVERSAL.md` is already comprehensively marked as deprecated. This includes appropriate frontmatter updates (status, primary-topic, related-standards, version) and a clear deprecation notice at the top of the document body.
        -   No further modifications were needed to deprecate this file.
-   **Step 1.3: Process `standards/COL-GOVERNANCE-UNIVERSAL.md`**
    -   **Overall:** All concepts (U-VERSIONING-001, U-GOVERNANCE-001, U-DEPRECATION-001, U-ONBOARDING-001, U-GLOSSARY-001, U-TEMPLATES-DIR-001, U-FILEHYGIENE-001) from `COL-GOVERNANCE-UNIVERSAL.md` have been processed.
    -   The collection file `standards/COL-GOVERNANCE-UNIVERSAL.md` is already marked as deprecated and correctly lists its atomic replacements.
    -   Verification confirmed that the following atomic standards exist in `/master-knowledge-base/standards/src/` and accurately reflect the content of their corresponding concepts from the collection file:
        -   `OM-VERSIONING-CHANGELOGS.md` (from U-VERSIONING-001)
        -   `OM-POLICY-STANDARDS-GOVERNANCE.md` (from U-GOVERNANCE-001)
        -   `OM-POLICY-STANDARDS-DEPRECATION.md` (from U-DEPRECATION-001)
        -   `GM-MANDATE-KB-USAGE-GUIDE.md` (mandate derived from U-ONBOARDING-001)
        -   `GM-MANDATE-STANDARDS-GLOSSARY.md` (mandate derived from U-GLOSSARY-001)
        -   `AS-STRUCTURE-TEMPLATES-DIRECTORY.md` (from U-TEMPLATES-DIR-001)
        -   `SF-FORMATTING-FILE-HYGIENE.md` (from U-FILEHYGIENE-001)
    -   No new file creation or modifications were needed for these specific standards as part of this step.
    -   **Note:** The actual guide document (`GM-GUIDE-KB-USAGE.md`) and glossary document (`GM-GLOSSARY-STANDARDS-TERMS.md`) are covered by later roadmap tasks (1.8.1 and 2.3.1 respectively) and will involve renaming/moving and updating existing files from the root `standards/` directory.
-   **Step 1.3: Process `standards/COL-GOVERNANCE-UNIVERSAL.md` (Continued)**
    -   **Review of Roadmap Step 1.7 (Specific Merging/Refactoring Decisions):**
        -   No specific tasks from Roadmap Step 1.7 were found to directly overlap with or require further action based on the concepts within `COL-GOVERNANCE-UNIVERSAL.md`. The refactoring of this collection's concepts into their atomic counterparts (e.g., `OM-VERSIONING-CHANGELOGS`, `OM-POLICY-STANDARDS-GOVERNANCE`, etc.) was direct and did not involve complex merges with other old standards that are covered by Step 1.7.
    -   **Task 1.3.2 (Mark `COL-GOVERNANCE-UNIVERSAL.md` for deprecation):**
        -   Verified that `standards/COL-GOVERNANCE-UNIVERSAL.md` is already comprehensively marked as deprecated. This includes appropriate frontmatter updates (status, primary-topic, related-standards, version) and a clear deprecation notice at the top of the document body listing its atomic replacements.
        -   No further modifications were needed to deprecate this file.

### Decision ID DECISION_002: Refactor KB Standards (Continued)

**Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment (In Progress)**

-   **Step 1.4: Process `standards/COL-LINKING-UNIVERSAL.md`**
    -   **Overall:** All concepts (U-INTERLINK-001, U-TAG-001, U-CITE-001, U-MODULAR-001, U-ACCESSIBILITY-001, U-ASSETS-001) from `COL-LINKING-UNIVERSAL.md` have been processed.
    -   The collection file `standards/COL-LINKING-UNIVERSAL.md` is already marked as deprecated and correctly lists its atomic replacements.
    -   Verification confirmed that the following atomic standards exist in `/master-knowledge-base/standards/src/` and accurately reflect the content of their corresponding concepts from the collection file, with tool-specific references appropriately generalized:
        -   `SF-LINKS-INTERNAL-SYNTAX.md` and `CS-LINKING-INTERNAL-POLICY.md` (from U-INTERLINK-001)
        -   `MT-TAGS-IMPLEMENTATION.md` and `MT-TAGGING-STRATEGY-POLICY.md` (from U-TAG-001)
        -   `SF-FORMATTING-CITATIONS.md` (from U-CITE-001)
        -   `SF-TRANSCLUSION-SYNTAX.md` and `CS-MODULARITY-TRANSCLUSION-POLICY.md` (from U-MODULAR-001)
        -   `SF-ACCESSIBILITY-IMAGE-ALT-TEXT.md` and `CS-POLICY-ACCESSIBILITY.md` (from U-ACCESSIBILITY-001)
        -   `AS-STRUCTURE-ASSET-ORGANIZATION.md` (from U-ASSETS-001)
    -   No new file creation or modifications were needed for these standards as part of this step.
-   **Step 1.4: Process `standards/COL-LINKING-UNIVERSAL.md` (Continued)**
    -   **Review of Roadmap Step 1.7 (Specific Merging/Refactoring Decisions) in context of COL-LINKING-UNIVERSAL and related concepts:**
        -   Task 1.7.1 (Internal Linking): Verified `SF-LINKS-INTERNAL-SYNTAX.md` and `CS-LINKING-INTERNAL-POLICY.md` correctly refactor U-INTERLINK-001.
        -   Task 1.7.2 (ToC): `SF-TOC-SYNTAX.md` was created and `CS-TOC-POLICY.md` verified (related to U-STRUC-002 from COL-ARCH-UNIVERSAL).
        -   Task 1.7.3 (Part Overview): `AS-STRUCTURE-KB-PART.md` and `CS-POLICY-PART-OVERVIEW.md` verified (related to U-STRUC-001 from COL-ARCH-UNIVERSAL).
        -   Task 1.7.4 (Transclusion): Verified `SF-TRANSCLUSION-SYNTAX.md` and `CS-MODULARITY-TRANSCLUSION-POLICY.md` correctly refactor U-MODULAR-001.
        -   Task 1.7.5 (Callouts): Verified `SF-CALLOUTS-SYNTAX.md` and `CS-ADMONITIONS-POLICY.md` correctly implement requirements, generalizing from O-USAGE-CALLOUTS-001.
        -   Task 1.7.6 (Tagging): Verified `MT-TAGS-IMPLEMENTATION.md` and `MT-TAGGING-STRATEGY-POLICY.md` correctly refactor U-TAG-001.
        -   Task 1.7.7 (Conditional Text): Verified `SF-CALLOUTS-SYNTAX.md` (includes IF type), `SF-CONDITIONAL-SYNTAX-ATTRIBUTES.md`, and `CS-CONTENT-PROFILING-POLICY.md` correctly implement requirements.
        -   All sub-tasks of Roadmap Step 1.7 appear to be addressed by existing (and now verified or created) atomic standards.
    -   **Task 1.4.2 (Mark `COL-LINKING-UNIVERSAL.md` for deprecation):**
        -   Verified that `standards/COL-LINKING-UNIVERSAL.md` is already comprehensively marked as deprecated. This includes appropriate frontmatter updates (status, primary-topic, related-standards, version) and a clear deprecation notice at the top of the document body listing its atomic replacements.
        -   No further modifications were needed to deprecate this file.

### Decision ID DECISION_002: Refactor KB Standards (Continued)

**Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment (In Progress)**

-   **Step 1.5: Process `standards/COL-SYNTAX-MARKDOWN.md`**
    -   **Overall:** All 15 concepts (M-SYNTAX-YAML-001 through M-SYNTAX-DIAGRAMS-001) from `COL-SYNTAX-MARKDOWN.md` have been processed.
    -   The collection file `standards/COL-SYNTAX-MARKDOWN.md` is already marked as deprecated and correctly lists its atomic replacements (generally `SF-SYNTAX-*` or `SF-FORMATTING-*` files).
    -   Verification confirmed that corresponding atomic standards for all 15 concepts exist in `/master-knowledge-base/standards/src/` and accurately reflect the content of their source concepts from the collection file. The specific files verified are:
        -   `SF-SYNTAX-YAML-FRONTMATTER.md`
        -   `SF-SYNTAX-HEADINGS.md`
        -   `SF-SYNTAX-LISTS.md`
        -   `SF-SYNTAX-LINKS-GENERAL.md` (covering general link syntax aspects from M-SYNTAX-LINKS-001)
        -   `SF-SYNTAX-EMPHASIS.md`
        -   `SF-SYNTAX-BLOCKQUOTES.md`
        -   `SF-SYNTAX-CODE.md`
        -   `SF-SYNTAX-TABLES.md`
        -   `SF-FORMATTING-MARKDOWN-GENERAL.md`
        -   `SF-SYNTAX-IMAGES.md`
        -   `SF-SYNTAX-ESCAPING-CHARACTERS.md`
        -   `SF-SYNTAX-DEFINITION-LISTS.md`
        -   `SF-SYNTAX-FOOTNOTES.md`
        -   `SF-SYNTAX-MATH-EQUATIONS.md`
        -   `SF-SYNTAX-DIAGRAMS-MERMAID.md`
    -   No new file creation or modifications were needed for these standards as part of this step, as they were found to be pre-existing and correctly refactored.
-   **Step 1.5: Process `standards/COL-SYNTAX-MARKDOWN.md` (Continued)**
    -   **Task 1.5.2 (Mark `COL-SYNTAX-MARKDOWN.md` for deprecation):**
        -   Verified that `standards/COL-SYNTAX-MARKDOWN.md` is already comprehensively marked as deprecated. This includes appropriate frontmatter updates (status, primary-topic, related-standards, version) and a clear deprecation notice at the top of the document body listing its atomic replacements.
        -   No further modifications were needed to deprecate this file.

### Decision ID DECISION_002: Refactor KB Standards (Continued)

**Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment (In Progress)**

-   **Step 1.6: Process `standards/COL-TOOLING-OBSIDIAN.md`**
    -   **Overall:** All concepts (O-USAGE-LINKS-001, O-USAGE-TAGS-001, O-USAGE-FOLDERS-NOTES-001, O-USAGE-TOC-MANDATE-001, O-USAGE-TRANSCLUSION-001, O-USAGE-CALLOUTS-001, O-USAGE-TOC-PLUGIN-001) from `COL-TOOLING-OBSIDIAN.md` have been processed.
    -   The collection file `standards/COL-TOOLING-OBSIDIAN.md` is already marked as deprecated and correctly lists its generalized atomic replacements.
    -   Verification confirmed that the following atomic standards exist in `/master-knowledge-base/standards/src/` and accurately reflect and generalize the functionalities previously described in an Obsidian-specific context. These include:
        -   `SF-LINKS-INTERNAL-SYNTAX.md` and `CS-LINKING-INTERNAL-POLICY.md` (for linking)
        -   `MT-TAGS-IMPLEMENTATION.md` and `MT-TAGGING-STRATEGY-POLICY.md` (for tagging)
        -   `AS-STRUCTURE-KB-PART.md` and `CS-POLICY-PART-OVERVIEW.md` (for part overviews, generalizing folder notes)
        -   `SF-TOC-SYNTAX.md` and `CS-TOC-POLICY.md` (for table of contents, generalizing plugin usage to recommendations for tools producing standard Markdown)
        -   `SF-TRANSCLUSION-SYNTAX.md` and `CS-MODULARITY-TRANSCLUSION-POLICY.md` (for transclusion, generalizing to ID-based targets)
        -   `SF-CALLOUTS-SYNTAX.md` and `CS-ADMONITIONS-POLICY.md` (for callouts, standardizing the syntax for the KB)
    -   No new file creation or modifications were needed for these standards as part of this step, as they were found to be pre-existing and correctly refactored/generalized.
-   **Step 1.6: Process `standards/COL-TOOLING-OBSIDIAN.md` (Continued)**
    -   **Explicit Re-verification of Roadmap Step 1.7 (Specific Merging/Refactoring Decisions):**
        -   A full review of Roadmap Step 1.7 tasks (1.7.1 through 1.7.7) confirms that all specified atomic standards have been previously verified as existing or were created (i.e., `SF-TOC-SYNTAX.md`).
        -   The concepts from `COL-TOOLING-OBSIDIAN.md` (linking, tagging, folder notes/part overviews, ToC, transclusion, callouts) have been successfully generalized into their respective tool-agnostic atomic standards (SF-LINKS-INTERNAL-SYNTAX, CS-LINKING-INTERNAL-POLICY, MT-TAGS-IMPLEMENTATION, MT-TAGGING-STRATEGY-POLICY, AS-STRUCTURE-KB-PART, CS-POLICY-PART-OVERVIEW, SF-TOC-SYNTAX, CS-TOC-POLICY, SF-TRANSCLUSION-SYNTAX, CS-MODULARITY-TRANSCLUSION-POLICY, SF-CALLOUTS-SYNTAX, CS-ADMONITIONS-POLICY).
        -   No further actions are required for Roadmap Step 1.7 based on the processing of `COL-TOOLING-OBSIDIAN.md` and prior collection files.
    -   **Task 1.6.2 (Mark `COL-TOOLING-OBSIDIAN.md` for deprecation):**
        -   Verified that `standards/COL-TOOLING-OBSIDIAN.md` is already comprehensively marked as deprecated. This includes appropriate frontmatter updates (status, primary-topic, related-standards, version) and a clear deprecation notice at the top of the document body listing its generalized atomic replacements.
        -   No further modifications were needed to deprecate this file.

### Decision ID DECISION_002: Refactor KB Standards (Continued)

**Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment (In Progress)**

-   **Step 1.8: Refactor Guide Documents**
    -   **Task 1.8.1: Refactor `GUIDE-KB-USAGE-AND-STANDARDS.md`**
        -   Created new guide `/master-knowledge-base/standards/src/GM-GUIDE-KB-USAGE.md` (standard_id: `GM-GUIDE-KB-USAGE`).
        -   Populated frontmatter using `tpl-canonical-frontmatter.md` as a base, with `info-type: guide-document`.
        -   Migrated content from `standards/GUIDE-KB-USAGE-AND-STANDARDS.md`.
        -   Thoroughly revised content, updating internal links to use the new `[[STANDARD_ID]]` format, pointing to the refactored atomic standards.
        -   Updated references to the TODO system to align with `SF-CALLOUTS-SYNTAX.md` (`[!TODO]` callouts).
        -   Updated references to glossaries, templates directory, and other key architectural files to their new standard IDs.
        -   Added notes to the "Using Obsidian" section to clarify that these are now generalized standards.
-   **Step 1.8: Refactor Guide Documents (Continued)**
    -   **Task 1.8.2: Refactor `GUIDE-TASK-BAED.md`**
        -   Created new guide `/master-knowledge-base/standards/src/GM-GUIDE-STANDARDS-BY-TASK.md` (standard_id: `GM-GUIDE-STANDARDS-BY-TASK`).
        -   Populated frontmatter using `tpl-canonical-frontmatter.md` as a base, with `info-type: guide-document`.
        -   Migrated content from `standards/GUIDE-TASK-BASED.md`.
        -   Thoroughly revised content, updating internal links from old U-xxx/M-xxx/O-xxx IDs to use the new `[[STANDARD_ID]]` format, pointing to the refactored atomic standards.
        -   Updated the "Working within Obsidian" section to reference generalized standards.
-   **Step 1.8: Refactor Guide Documents (Completed)**
    -   The original guide files `standards/GUIDE-KB-USAGE-AND-STANDARDS.md` and `standards/GUIDE-TASK-BASED.md` have been successfully refactored into `master-knowledge-base/standards/src/GM-GUIDE-KB-USAGE.md` and `master-knowledge-base/standards/src/GM-GUIDE-STANDARDS-BY-TASK.md` respectively.
    -   The original files in the `standards/` directory are now considered superseded and are candidates for deletion or archival in a later cleanup phase. No direct modifications (like adding deprecation notices) will be made to these old files at this time, as their replacements are now the authoritative versions.

## Unresolved/Unmapped Placeholders Encountered During Link Updates (Phase 2.1)

The following placeholder IDs were found in files within `/master-knowledge-base/standards/src/` but were not included in the provided replacement mapping. They have been left unchanged for now and require further investigation:

-   `HYPOTHESIS-TESTING_ID_PLACEHOLDER` (found in `AS-SCHEMA-CONCEPT-DEFINITION.md`)
-   `P-VALUE_ID_PLACEHOLDER` (found in `AS-SCHEMA-CONCEPT-DEFINITION.md`)
-   `ANOTHER-RELEVANT-STANDARD_ID_PLACEHOLDER` (found in `AS-STRUCTURE-DOC-CHAPTER.md`)
-   `CORE-CONCEPT-RESEARCH_ID_PLACEHOLDER` (found in `AS-STRUCTURE-DOC-CHAPTER.md`)
-   `FILENAME_ID_PLACEHOLDER` (found in comments in `AS-STRUCTURE-KB-PART.md`, `AS-STRUCTURE-KB-ROOT.md`, `AS-STRUCTURE-MASTER-KB-INDEX.md` - likely not actual links)
-   `Advanced Settings Guide_ID_PLACEHOLDER` (found in `CS-CONTENT-PROFILING-POLICY.md`)
-   `NEW-STANDARD-ID_PLACEHOLDER` (found in `OM-POLICY-STANDARDS-DEPRECATION.md` example)

### Decision ID DECISION_002: Refactor KB Standards (Continued)

**Phase 2: Governance Review & Standalone Document Refactoring (In Progress)**

-   **Step 2.2: Refactor Existing Standalone Standard Files**
    -   **Processed `standards/U-KEYREF-SYNTAX-001.md`**:
        -   Created new atomic standard `/master-knowledge-base/standards/src/SF-SYNTAX-KEYREF.md` (standard_id: `SF-SYNTAX-KEYREF`).
        -   `info-type` set to `standard-definition`.
        -   Frontmatter populated according to `tpl-canonical-frontmatter.md`.
        -   Content migrated from `U-KEYREF-SYNTAX-001`, defining the `{{key.name}}` syntax, camelCase recommendation for key names, and no whitespace rule.
        -   Cross-references updated to point to anticipated new standard IDs like `[[MT-KEYREF-MANAGEMENT]]` and `[[UA-KEYDEFS-GLOBAL]]`.
### Decision ID DECISION_002: Refactor KB Standards (Continued)

**Phase 2: Standalone Document Refactoring - Part 2 (Continuing Roadmap Step 2.2)**

-   **Process `standards/M-CONDITIONAL-TEXT-SYNTAX-001.md`**:
    -   Read the file `standards/M-CONDITIONAL-TEXT-SYNTAX-001.md`.
    -   Verified that its content regarding conditional text syntax and usage is fully covered and superseded by the combination of existing atomic standards:
        -   `SF-CALLOUTS-SYNTAX.md` (defines the `[!IF]` callout type)
        -   `SF-CONDITIONAL-SYNTAX-ATTRIBUTES.md` (defines the `attribute=value` syntax for conditions)
        -   `CS-CONTENT-PROFILING-POLICY.md` (defines the overall policy, manages attributes/values, and references the syntax standards; explicitly supersedes `U-PROFILING-ATTRIBUTES-001.md` which was related to `M-CONDITIONAL-TEXT-SYNTAX-001.md`).
    -   No new file creation is needed from `M-CONDITIONAL-TEXT-SYNTAX-001.md` as its rules have been appropriately refactored. This file is now fully superseded.
-   **Process `standards/M-SYNTAX-TODO-001.md`**:
    -   The original standard defined two methods for TODOs: HTML comments and an Obsidian callout alternative.
    -   The `[!TODO]` callout aspect is covered by `SF-CALLOUTS-SYNTAX.md`.
    -   To preserve the distinct HTML comment-based TODO syntax (for non-rendering, script-parsable tasks), created new atomic standard `/master-knowledge-base/standards/src/SF-SYNTAX-COMMENT-TODO.md` (standard_id: `SF-SYNTAX-COMMENT-TODO`).
    -   `info-type` set to `standard-definition`.
    -   Frontmatter populated according to `tpl-canonical-frontmatter.md`.
    -   Content migrated and adapted from `M-SYNTAX-TODO-001` (Rules 1.1-1.7), focusing on the `<!-- TODO ... -->` syntax.
    -   The original `M-SYNTAX-TODO-001.md` is now considered superseded by the combination of `SF-CALLOUTS-SYNTAX.md` (for visible TODOs) and `SF-SYNTAX-COMMENT-TODO.md` (for hidden, scriptable TODOs).
-   **Process `standards/U-ARCH-003-Directory-Structure-Source-Render.md`**:
    -   Read the file `standards/U-ARCH-003-Directory-Structure-Source-Render.md`.
    -   Verified that its content regarding source directory structure (`master-knowledge-base/`) and the concept of a rendered output directory are substantially covered and evolved by the existing atomic standard `master-knowledge-base/standards/src/AS-KB-DIRECTORY-STRUCTURE.md`.
    -   `AS-KB-DIRECTORY-STRUCTURE.md` details the primary `master-knowledge-base/` root and its internal organization (including `/standards/src`, `/standards/registry`, `/standards/templates`, `/tools`, `/assets`). It also proposes a `/dist/` or `/build/` directory (typically gitignored) for generated outputs, which serves a similar purpose to `master-knowledge-base-rendered/` but with a more common build artifact handling approach.
    -   `U-ARCH-003-Directory-Structure-Source-Render.md` is considered superseded by `AS-KB-DIRECTORY-STRUCTURE.md`. No new file creation needed from `U-ARCH-003`.
-   **Process `standards/U-KEYREF-MANAGEMENT-001.md`**:
    -   Created new atomic standard `/master-knowledge-base/standards/src/MT-KEYREF-MANAGEMENT.md` (standard_id: `MT-KEYREF-MANAGEMENT`).
    -   `info-type` set to `standard-definition`.
    -   Frontmatter populated according to `tpl-canonical-frontmatter.md` and specific requirements for this standard (domain MT, subdomain REGISTRY).
    -   Content migrated and adapted from `U-KEYREF-MANAGEMENT-001`, defining storage (`_key_definitions.md` identified as `[[UA-KEYDEFS-GLOBAL]]`), structure (YAML `keys:` dictionary), key naming conventions, documentation within `_key_definitions.md`, and the policy for triggering content resolution upon changes.
    -   Cross-references updated to `[[SF-SYNTAX-KEYREF]]`, `[[SF-SYNTAX-YAML-FRONTMATTER]]`, and `[[UA-KEYDEFS-GLOBAL]]`.
    -   The original `standards/U-KEYREF-MANAGEMENT-001.md` is now considered superseded.

[end of note.md]
