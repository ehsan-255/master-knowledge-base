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
