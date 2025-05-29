## CONTRIBUTOR_GUIDE.md Updates Log (Manual Integration Required)

This file contains updates that were intended for `CONTRIBUTOR_GUIDE.md`. Due to issues accessing or reliably updating `CONTRIBUTOR_GUIDE.md` directly, these notes should be manually reviewed and integrated into it at a later stage.

### Decision ID DECISION_002: Refactor KB Standards

**Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment (In Progress)**

-   **Step 1.1: Process `standards/COL-ARCH-UNIVERSAL.md`**
    -   **Overall:** All concepts (U-ARCH-001, U-ARCH-002, U-STRUC-001, U-STRUC-002, U-DETAIL-LEVEL-001, U-FORMAT-NAMING-001) from `COL-ARCH-UNIVERSAL.md` have been processed. The primary finding is that most of these concepts had already been refactored into atomic standards in `/master-knowledge-base/standards/src/`. Verification of these existing files against the original collection content has been completed.
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
