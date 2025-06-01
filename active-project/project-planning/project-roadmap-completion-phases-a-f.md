---
title: Refactoring Completion Roadmap (Phases A-F)
standard_id: project-roadmap-completion-phases-a-f
aliases: [Completion Roadmap, Phase A-F Roadmap]
tags: [status/active, info-type/project-roadmap, topic/project-planning]
kb-id: project-governance
info-type: project-roadmap
primary-topic: The detailed execution plan for completing the knowledge base refactoring (Phases A-F).
related-standards: ['project-roadmap-original-high-level', 'project-instructions-phase-b-cleanup']
version: '1.3.0'
date-created: '2025-05-30T00:00:00Z'
date-modified: '2025-05-31T09:33:00Z'
primary_domain: PROJECT
sub_domain: PLANNING
scope_application: Detailed operational roadmap for refactoring completion.
criticality: p0-critical
lifecycle_gatekeeper: N/A
impact_areas: [project-execution, phase-management]
change_log_url: N/A
---

## Refactoring Completion Roadmap

**Document ID:** `GM-ROADMAP-REFACTORING-COMPLETION`
**Version:** `1.3.0`
**Date:** `2025-05-30`

### 0. Preamble

This roadmap outlines the definitive, sequential steps required to complete the refactoring of the knowledge base standards. The goal is to achieve a fully operational, validated, and documented system where all standards, guides, tools, and related artifacts are in their final state and location at the repository root.

### Phase A: Metadata & Content Finalization

**Goal:** Ensure all active atomic source documents have complete and accurate metadata according to the new schema, and that content is correctly allocated between Standard Definition and Policy/Guideline documents. Ensure all legacy documents are correctly marked for future archival.

*   **Step A.1: Systematic Frontmatter Enrichment for All Active Atomic Documents**
    *   **Task A.1.1:** Identify all active atomic standard, policy, and guide documents located in `/master-knowledge-base/standards/src/`.
    *   **Task A.1.2:** For each identified active document:
        *   Verify or assign its unique `standard_id` (matching filename, adhering to `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$` regex).
        *   Update its YAML frontmatter to precisely match the full schema defined in `[[MT-SCHEMA-FRONTMATTER]]`, ensuring all mandatory keys are present and in the correct order.
        *   Populate `primary_domain`, `sub_domain`, `scope_application`, `criticality`, `lifecycle_gatekeeper`, `impact_areas`, and `change_log_url` with accurate values.
        *   Ensure `date-created` and `date-modified` use the full ISO-8601 date-time format with "Z" (e.g., `2025-05-27T15:42:00Z`).
        *   Validate `info-type`, `primary_domain`, `sub_domain`, `criticality`, `lifecycle_gatekeeper`, and `tags` against their respective controlled vocabularies in `/master-knowledge-base/standards/registry/`.
        *   Ensure `version` is a quoted string and reflects the document's current state.
    *   **Deliverable:** All atomic standard, policy, and guide documents in `/master-knowledge-base/standards/src/` have fully populated and validated frontmatter.

*   **Step A.2: Systematic Deprecation Marking of Legacy Files**
    *   **Task A.2.1:** Identify all superseded `COL-*.md`, `U-*.md`, and `M-*.md` files in their original locations (e.g., the old `/standards/` directory at the repository root, or any other legacy paths).
    *   **Task A.2.2:** For each identified superseded file:
        *   Ensure its `status` tag in the frontmatter is set to `status/deprecated`.
        *   Add or verify a prominent deprecation notice at the top of the document body, clearly stating it is superseded and linking to its new replacement(s) in `/master-knowledge-base/standards/src/` using `[[STANDARD_ID]]` links.
        *   Update its `date-modified` field to the current date/time of this action.
        *   Increment its `version` field to reflect this deprecation update.
    *   **Deliverable:** All identified legacy standard files are correctly marked as deprecated with appropriate notices and links, ready for archival in Phase F.

*   **Step A.3: Full Standard Definition vs. Policy Document Content Review & Refinement**
    *   **Task A.3.1:** Identify all pairs of "Standard Definition" (`info-type: standard-definition`) and corresponding "Policy Document" (`info-type: policy-document`) files within `/master-knowledge-base/standards/src/`, as well as standalone documents of these types.
    *   **Task A.3.2:** For each document/pair:
        *   Rigorously review the body content to ensure strict adherence to the "HOW/WHERE" (Standard Definition) vs. "WHAT/WHEN/WHY" (Policy Document) separation principle.
        *   Migrate any misplaced content to the correct document.
        *   Refine wording for clarity, precision, and conciseness according to `[[CS-POLICY-TONE-LANGUAGE]]`.
        *   Ensure all internal links within the body use the `[[STANDARD_ID]]` format.
        *   Verify that `related-standards` in the frontmatter accurately link corresponding Standard/Policy pairs and other relevant documents.
    *   **Deliverable:** Content within all standard and policy documents in `/master-knowledge-base/standards/src/` is correctly allocated and refined.

*   **Step A.4: Resolve Unmapped Placeholders & Populate Navigational Files**
    *   **Task A.4.1:** Review the list of "Unresolved/Unmapped Placeholders" (from `master-knowledge-base-main/note.md`). Investigate each placeholder found in files within `/master-knowledge-base/`.
        *   Determine the correct target `STANDARD_ID`.
        *   Update the link in the source file to `[[CORRECT_STANDARD_ID]]`.
        *   If a target standard does not yet exist and is required, create a stub file in `/master-knowledge-base/standards/src/` with minimal frontmatter (including a new `standard_id`) and a `[!TODO]` callout for content, then link to its new `STANDARD_ID`.
    *   **Task A.4.2:** Fully populate the Table of Contents in `[[AS-ROOT-STANDARDS-KB]]` (located in `/master-knowledge-base/standards/src/`) with `[[STANDARD_ID]]` links to all key atomic standards, policies, and guides, organized by domain or theme.
    *   **Task A.4.3:** Fully populate the list of Knowledge Bases in `[[AS-INDEX-KB-MASTER]]` (located in `/master-knowledge-base/`) with accurate descriptions and `[[STANDARD_ID]]` links to the root files of all defined Knowledge Bases.
    *   **Deliverable:** All known placeholder links within `/master-knowledge-base/` resolved. Core navigational documents (`AS-ROOT-STANDARDS-KB`, `AS-INDEX-KB-MASTER`) are fully populated and functional relative to the `/master-knowledge-base/` structure.

*   **Exit Criteria for Phase A:**
    *   All active atomic documents in `/master-knowledge-base/standards/src/` have frontmatter fully compliant with `[[MT-SCHEMA-FRONTMATTER]]`.
    *   All identified legacy standard files are correctly marked as deprecated.
    *   Systematic review of Standard/Policy content separation completed and necessary corrections made within `/master-knowledge-base/standards/src/`.
    *   All identified placeholder links within `/master-knowledge-base/` are resolved.
    *   Core navigational documents within `/master-knowledge-base/` are fully populated with correct links relative to that structure.
    *   A script run report (from locally executed tools) confirms initial validation status.

---

### Phase B: Linter & Indexer Productionization & Initial Source Validation (within `/master-knowledge-base/`)

**Goal:** Transition prototype linter and indexer scripts to production-ready tools and perform an initial comprehensive validation of all refactored source content *within its current `/master-knowledge-base/` location*.

*   **Step B.1: Productionize Linter (`kb_linter.py`)**
    *   **Task B.1.1:** Fully implement all specified checks in `/master-knowledge-base/tools/linter/kb_linter.py`. This includes dynamic loading of all controlled vocabularies from `/master-knowledge-base/standards/registry/` files, strict enforcement of key order, validation of `standard_id` uniqueness and regex, ISO-8601 date formats, `change_log_url` checks, and file hygiene checks.
    *   **Task B.1.2:** Configure the linter to `error` on path-based internal links.
    *   **Task B.1.3:** Implement robust error handling, clear reporting with severity levels (`info`, `warning`, `error`), and accurate line number reporting.
    *   **Task B.1.4:** Write unit tests for key linting functions.
    *   **Task B.1.5:** Document final CLI usage and configuration options in `/master-knowledge-base/tools/linter/README.md`.
    *   **Deliverable:** Production-ready `kb_linter.py` script, configured to operate on paths within `/master-knowledge-base/`.

*   **Step B.2: Productionize Indexer (`generate_index.py`)**
    *   **Task B.2.1:** Fully implement robust Markdown parsing and frontmatter extraction in `/master-knowledge-base/tools/indexer/generate_index.py`.
    *   **Task B.2.2:** Ensure the script correctly derives `status` from tags and handles all fields required by `/master-knowledge-base/tools/indexer/standards_index.schema.json`. Filepaths in the index will be relative to the repository root (e.g., `master-knowledge-base/standards/src/FILE.md`).
    *   **Task B.2.3:** Implement comprehensive error handling for file operations and parsing.
    *   **Task B.2.4:** Ensure `schemaVersion` is correctly included in `standards_index.json`.
    *   **Task B.2.5:** Write unit tests for key indexing functions.
    *   **Task B.2.6:** Document final CLI usage in `/master-knowledge-base/tools/indexer/README.md`.
    *   **Deliverable:** Production-ready `generate_index.py` script, configured to operate on paths within `/master-knowledge-base/`.

*   **Step B.3: Initial Full Validation of Source Content (within `/master-knowledge-base/`)**
    *   **Task B.3.1:** Execute the productionized `generate_index.py` on the `/master-knowledge-base/standards/src/` directory. Verify the output `standards_index.json` (e.g., in `/master-knowledge-base/dist/standards_index.json`) against its schema and for completeness.
    *   **Task B.3.2:** Execute the productionized `kb_linter.py` on all Markdown files in `/master-knowledge-base/standards/src/` and other relevant source directories within `/master-knowledge-base/`.
    *   **Task B.3.3:** Address ALL `error` level issues reported by the linter by correcting the source files.
    *   **Task B.3.4:** Review and address all `warning` level issues reported by the linter by correcting the source files or confirming the warning is acceptable.
    *   **Deliverable:** All source Markdown files within `/master-knowledge-base/` pass the linter with zero errors. `standards_index.json` (with paths relative to `/master-knowledge-base/`) is complete and valid.

*   **Exit Criteria for Phase B:**
    *   `kb_linter.py` and `generate_index.py` are production-ready, tested, and documented for operation within `/master-knowledge-base/`.
    *   All source Markdown files within `/master-knowledge-base/standards/src/` (and other key areas within `/master-knowledge-base/`) pass the linter with zero errors.
    *   A complete and valid `standards_index.json` reflecting the `/master-knowledge-base/` structure is generated.
    *   A script run report confirms linter and indexer success on source files within `/master-knowledge-base/`.

---

### Phase C: Template, Collection Builder, Link Finalization & Initial CI/CD (within `/master-knowledge-base/`)

**Goal:** Finalize document templates, implement the "Multi-View" aspect by productionizing the collection builder (operating on `/master-knowledge-base/` content), ensure all internal links are robust, and set up initial CI/CD.

*   **Step C.1: Finalize Document Template Creation**
    *   **Task C.1.1:** Create `/master-knowledge-base/standards/templates/tpl-standard-definition.md`.
    *   **Task C.1.2:** Create `/master-knowledge-base/standards/templates/tpl-policy-document.md`.
    *   **Task C.1.3:** Update `/master-knowledge-base/standards/templates/README.md`.
    *   **Deliverable:** Completed set of core document templates in `/master-knowledge-base/standards/templates/`.

*   **Step C.2: Productionize Collection Builder (`generate_collections.py`)**
    *   **Task C.2.1:** Fully implement the logic in `/master-knowledge-base/tools/builder/generate_collections.py`.
    *   **Task C.2.2:** Implement comprehensive error handling and logging.
    *   **Task C.2.3:** Write unit tests for key collection building functions.
    *   **Task C.2.4:** Document final CLI usage in `/master-knowledge-base/tools/builder/README.md`.
    *   **Task C.2.5:** Ensure generated collection files are output to `/master-knowledge-base/dist/collections/`. This directory (`/master-knowledge-base/dist/`) MUST be added to the project's `.gitignore` file.
    *   **Deliverable:** Production-ready `generate_collections.py` script.

*   **Step C.3: Systematic Link Style Enforcement & Validation (within `/master-knowledge-base/`)**
    *   **Task C.3.1:** Confirm the linter (`kb_linter.py`) is strictly enforcing `[[STANDARD_ID]]` link styles (errors on any path-based internal links).
    *   **Task C.3.2:** Run the linter on all source Markdown files within `/master-knowledge-base/`. Fix any remaining path-based links.
    *   **Task C.3.3:** Use the `standards_index.json` to validate that all `[[STANDARD_ID]]` links in source documents resolve to an existing `standard_id` in the index. Fix any broken links.
    *   **Deliverable:** All internal links in source documents within `/master-knowledge-base/` use `[[STANDARD_ID]]` style and are validated.

*   **Step C.4: Implement Initial CI/CD Pipeline (for `/master-knowledge-base/` context)**
    *   **Task C.4.1:** Implement the CI workflow (e.g., GitHub Actions YAML file in `.github/workflows/`) to automatically run the linter, indexer, and collection builder on relevant triggers (e.g., push to main, pull request), operating on the `/master-knowledge-base/` paths.
    *   **Task C.4.2:** Ensure CI workflow correctly reports errors/warnings and build status, and fails the build on linter errors.
    *   **Deliverable:** Integrated and tested CI/CD pipeline for automated checks and builds within the `/master-knowledge-base/` context.

*   **Exit Criteria for Phase C:**
    *   All core templates are finalized and documented.
    *   `generate_collections.py` is production-ready.
    *   All internal links in source documents within `/master-knowledge-base/` use `[[STANDARD_ID]]` style and are validated.
    *   Linter passes with zero errors on all source files within `/master-knowledge-base/`.
    *   The `/master-knowledge-base/dist/` directory is added to `.gitignore`.
    *   Initial CI/CD pipeline is operational for the `/master-knowledge-base/` context and its report confirms successful link validation and collection generation.

---

### Phase D: System-Wide Validation (within `/master-knowledge-base/`) & Documentation Finalization

**Goal:** Conduct comprehensive system validation of content within `/master-knowledge-base/`, including derived views, and finalize all supporting documentation for operational use.

*   **Step D.1: Execute Full System Validation Plan (within `/master-knowledge-base/`)**
    *   **Task D.1.1:** Run all productionized tools (`kb_linter.py`, `generate_index.py`, `generate_collections.py`) in sequence via the CI/CD pipeline or manually.
    *   **Task D.1.2:** Validate all source files in `/master-knowledge-base/standards/src/` using the final linter. Address any remaining issues.
    *   **Task D.1.3:** Generate all derived collection views into `/master-knowledge-base/dist/collections/`. Meticulously validate their content accuracy, structural integrity (ToCs), and internal/external link resolution.
    *   **Task D.1.4:** Test key navigational pathways starting from `[[AS-INDEX-KB-MASTER]]` (in `/master-knowledge-base/`) through `[[AS-ROOT-STANDARDS-KB]]` (in `/master-knowledge-base/standards/src/`) and into generated collection views and sample atomic standards.
    *   **Deliverable:** Fully validated source content and generated derived views, all within the `/master-knowledge-base/` structure.

*   **Step D.2: Finalize System & Workflow Documentation**
    *   **Task D.2.1:** Complete and finalize the "Development and Maintenance Workflow Documentation" (e.g., `GM-GUIDE-STANDARDS-MAINTENANCE.md`), ensuring it accurately reflects all final tools, processes, and directory structures *as they exist within `/master-knowledge-base/`*.
    *   **Task D.2.2:** Review and update `[[GM-GUIDE-KB-USAGE]]` and `[[GM-GUIDE-STANDARDS-BY-TASK]]` for final accuracy and completeness.
    *   **Task D.2.3:** Ensure READMEs for tools in `/master-knowledge-base/tools/` are complete and accurate.
    *   **Deliverable:** Comprehensive and accurate documentation for using and maintaining the standards ecosystem within its `/master-knowledge-base/` structure.

*   **Exit Criteria for Phase D:**
    *   Full system validation completed for content within `/master-knowledge-base/` with all critical issues resolved.
    *   All system, tool, and workflow documentation is finalized reflecting the `/master-knowledge-base/` structure.
    *   CI/CD pipeline is fully operational and tested for the `/master-knowledge-base/` context.

---

### Phase E: Root Relocation & System Finalization

**Goal:** Move the refactored content to the repository root, update all paths and links, perform final validation, and formally conclude the project.

*   **Step E.1: Archive Legacy Root Content**
    *   **Task E.1.1:** Identify all legacy files and folders at the repository root that will be replaced by the contents of `/master-knowledge-base/`.
    *   **Task E.1.2:** Create a dedicated archive directory at the repository root: `/archive/legacy-root-content-YYYYMMDD/` (where YYYYMMDD is the current date).
    *   **Task E.1.3:** Move all identified legacy files and folders from the repository root into this newly created archive directory.
    *   **Deliverable:** Clean repository root, with legacy content archived.

*   **Step E.2: Relocate Refactored Content to Repository Root**
    *   **Task E.2.1:** Move the entire contents of `/master-knowledge-base/` (including `/standards/`, `/tools/`, `AS-INDEX-KB-MASTER.md`, etc.) to the repository root.
        *   Example: `/master-knowledge-base/standards/src/` becomes `/standards/src/`.
        *   Example: `/master-knowledge-base/tools/linter/` becomes `/tools/linter/`.
        *   Example: `/master-knowledge-base/AS-INDEX-KB-MASTER.md` becomes `/AS-INDEX-KB-MASTER.md`.
    *   **Deliverable:** Refactored content now resides at the repository root.

*   **Step E.3: Update Tool Configurations and Internal Paths**
    *   **Task E.3.1:** Modify `kb_linter.py`, `generate_index.py`, `generate_collections.py` (now at `/tools/`) to reflect the new base paths for source files (`/standards/src/`), registries (`/standards/registry/`), templates (`/standards/templates/`), and output directories (e.g., `/dist/`).
    *   **Task E.3.2:** Update any configuration files used by these tools (e.g., `collection_definitions.yaml` now at `/tools/builder/`) if they contain paths that need adjustment.
    *   **Deliverable:** Tools configured to operate correctly from the new root structure.

*   **Step E.4: Regenerate `standards_index.json` at New Root**
    *   **Task E.4.1:** Run the updated `generate_index.py` to create a new `standards_index.json` in `/dist/` with correct filepaths relative to the new repository root.
    *   **Deliverable:** Updated `standards_index.json` reflecting the new root structure. The `/dist/` directory MUST be added to `.gitignore`.

*   **Step E.5: Comprehensive Link Validation and Correction (Script-Assisted)**
    *   **Task E.5.1:** Develop or adapt a script (`/tools/path_corrector/correct_paths.py`) to:
        *   Verify all `[[STANDARD_ID]]` links still resolve correctly using the new index.
        *   Scan all Markdown files (now at the root and in subdirectories like `/standards/src/`) for any remaining relative path links (e.g., `[text](./some/path.md)`, `![alt](../assets/img.png)`) that might have broken due to the move.
        *   Attempt to automatically correct these relative paths based on the known structural change (i.e., removal of the `/master-knowledge-base/` prefix from paths).
    *   **Task E.5.2:** Run this path correction script.
    *   **Task E.5.3:** Manually review and correct any links the script could not automatically fix.
    *   **Deliverable:** All internal links (both `[[STANDARD_ID]]` and relative paths) are validated and correct for the new root structure.

*   **Step E.6: Final System-Wide Test & Validation (at Root)**
    *   **Task E.6.1:** Re-run the updated linter on all content at its new root locations. Address any new issues.
    *   **Task E.6.2:** Re-generate derived views using the updated collection builder (outputting to `/dist/collections/`). Validate these views.
    *   **Task E.6.3:** Test navigation and key functionalities thoroughly in the new root structure.
    *   **Task E.6.4:** Update the CI/CD pipeline path configurations to operate on the new root structure and test the full pipeline.
    *   **Deliverable:** Fully validated system operating correctly from the repository root, with CI/CD updated.

*   **Step E.7: Update All Project Documentation for Root Structure**
    *   **Task E.7.1:** Ensure all project documentation (this roadmap, `GM-GUIDE-STANDARDS-MAINTENANCE.md`, `GM-GUIDE-KB-USAGE.md`, tool READMEs, etc.) reflects the final root structure in all path examples and descriptions.
    *   **Deliverable:** All project documentation accurately reflects the final system structure.

*   **Exit Criteria for Phase E:**
    *   Legacy root content archived.
    *   Refactored content successfully relocated to the repository root.
    *   All tools and configurations updated for the new root structure.
    *   `standards_index.json` regenerated with correct root-relative paths.
    *   The `/dist/` directory is added to `.gitignore`.
    *   All internal links validated and corrected for the new root structure.
    *   Final system-wide tests pass.
    *   All project documentation updated to reflect the final root structure.
    *   CI/CD pipeline updated and successfully running against the root structure.

---

### Phase F: Final Repository Cleanup & Project Closure

**Goal:** Remove obsolete refactoring artifacts, perform final checks, and formally conclude the refactoring project.

*   **Step F.1: Repository Cleanup**
    *   **Task F.1.1:** Delete the (now empty) `/master-knowledge-base/` directory.
    *   **Task F.1.2:** Identify any remaining superseded `COL-*.md`, `U-*.md`, `M-*.md` files (that were not part of the legacy root content archived in Step E.1, e.g., if they were in deeper old paths). Move these to a dedicated archive directory: `/archive/legacy-standards-v1-YYYYMMDD/` (where YYYYMMDD is the current date).
    *   **Task F.1.3:** Delete the old root `/templates/` directory if it exists and is distinct from `/standards/templates/`.
    *   **Deliverable:** Cleaned repository, containing only final refactored content and necessary structural/registry/template files at their new root locations, with legacy items archived.

*   **Step F.2: Review and Archive Project-Specific Tracking Files**
    *   **Task F.2.1:** Review `master-knowledge-base-main/note.md` for any outstanding actions or decisions not yet incorporated. Integrate any remaining critical information into final documentation.
    *   **Task F.2.2:** Archive `master-knowledge-base-main/note.md` by moving it to `/archive/project-notes/refactor-YYYYMMDD/note.md` (where YYYYMMDD is the current date).
    *   **Deliverable:** Cleaned project directory, with `note.md` archived.

*   **Step F.3: Final Project Review & Sign-off**
    *   **Task F.3.1:** Conduct a final review of the entire refactored standards ecosystem by all key stakeholders.
    *   **Task F.3.2:** Prepare a final Pull Request summarizing the completed refactoring effort, key outcomes, and any recommendations for ongoing maintenance. This PR will include the final state of the repository after all relocations and cleanup.
    *   **Task F.3.3:** Obtain formal sign-off on the completion of the refactoring project upon merging the final PR.
    *   **Deliverable:** Signed-off, fully refactored, validated, and documented standards knowledge base system, operating from the repository root.

---

