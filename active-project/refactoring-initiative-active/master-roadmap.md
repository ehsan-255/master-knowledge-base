---
title: "Master Roadmap - Refactoring Initiative"
id: "refactoring-initiative-master-roadmap"
kb: "refactoring-initiative"
file_type: "master_roadmap"
source_path: "active-project/refactoring-initiative-active/master-roadmap.md"
description: "Original high-level roadmap for the refactoring initiative."
linked_documents: ["master-analysis-report.md", "master-progress.md"]
standard_id: "refactoring-initiative-master-roadmap"
aliases: ["Master Project Roadmap", "Refactoring Main Roadmap"]
tags:
  - status/active
  - criticality/P1-High
  - content-type/roadmap-document
kb-id: "refactoring-initiative"
info-type: "roadmap-document"
primary-topic: "Defines the overall phases and tasks for the refactoring initiative."
related-standards: []
version: "1.0.0"
date-created: "YYYY-MM-DDTHH:MM:SSZ"
date-modified: "YYYY-MM-DDTHH:MM:SSZ"
primary_domain: "PROJECT"
sub_domain: "PLANNING"
scope_application: "Entire refactoring initiative."
criticality: "P1-High"
lifecycle_gatekeeper: "TBD"
impact_areas: ["project-strategy", "historical-context", "phase-planning"]
change_log_url: "TBD"
maturity: "Medium"
lifecycle_stage: "Planning"
target_audience: ["technical_team", "project_managers"]
project_phase: "Overall"
task_type: "Master Planning Document"
jira_issue: "TBD"
history_summary: "Content from project-roadmap-original-high-level.md."
key_takeaways: ["Provides a multi-phase plan for standards refactoring."]
next_steps: ["Execute Phase 0 and subsequent phases as outlined."]
---
## Roadmap: Standards Refactoring

This roadmap outlines the phases, steps, and tasks required to fully refactor the existing standards according to the new architecture and categorization schemes, incorporating all agreed-upon revisions and final clarifications.

### Phase 0: Foundations, Definitions & Initial Tooling (Pre-Refactoring)

**Goal:** Establish all necessary definitions, conventions, foundational metadata structures, and initial automation prototypes before modifying existing content.

*   **Step 0.1: Finalize Naming Conventions & Identifiers**
    *   **Task 0.1.1:** Document the confirmed atomic file naming convention: `{DOMAIN_CODE}-{SUB_DOMAIN_CODE}-{PRIMARY_TOPIC_KEYWORD}-{OPTIONAL_SECONDARY_TOPICS*}.md`.
    *   **Task 0.1.2:** Develop and document the strategy for `PRIMARY_TOPIC_KEYWORD` selection. This includes creating an initial proposal table mapping existing standard concepts (e.g., from `U-ARCH-001`) to their new `PRIMARY_TOPIC_KEYWORD`s, ensuring differentiation for Standard Definition vs. Policy/Guideline files (e.g., `KB-ROOT` for `AS-STRUCTURE-KB-ROOT` and `CS-POLICY-KB-ROOT`).
    *   **Task 0.1.3:** Document the regex for `standard_id` syntax as `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$` (all-caps, numerals, hyphens; no spaces, no underscores) in `U-METADATA-FRONTMATTER-RULES-001.md`.
    *   **Task 0.1.4:** Document in `U-METADATA-FRONTMATTER-RULES-001.md` that filenames (sans `.md`) SHOULD equal the `standard_id` metadata field.

*   **Step 0.2: Define Controlled Vocabularies & Registries**
    *   **Task 0.2.1:** Create `/master-knowledge-base/standards/registry/domain_codes.yaml` (or `.md`) defining the `DOMAIN_CODE`s (AS, CS, MT, SF, OM, GM, UA, QM) with their full names and descriptions.
    *   **Task 0.2.2:** Create `/master-knowledge-base/standards/registry/subdomain_registry.yaml` defining the initial set of `SUB_DOMAIN_CODE`s for each `DOMAIN_CODE`, with descriptions.
    *   **Task 0.2.3:** Update `U-METADATA-FRONTMATTER-RULES-001.md` with the finalized controlled vocabulary for the `info-type` metadata field, referencing the list within the document itself.
    *   **Task 0.2.4:** Update `/master-knowledge-base/standards/registry/tag-glossary-definition.md` (confirming this new path) with the finalized controlled vocabulary for `status/*` tags, derived from existing content and refined.
    *   **Task 0.2.5:** Update `/master-knowledge-base/standards/registry/tag-glossary-definition.md` with the finalized controlled vocabulary for `content-type/*` tags, ensuring alignment with `info-type` where appropriate.
    *   **Task 0.2.6:** Define the controlled vocabulary for `Criticality` (e.g., `P0-Critical`, `P1-High`, `P2-Medium`) within `/master-knowledge-base/standards/registry/tag-glossary-definition.md` (e.g., as `criticality/P0-Critical`) or a dedicated `criticality_levels.yaml` in the registry.
    *   **Task 0.2.7:** Define the controlled vocabulary for `Lifecycle_Gatekeeper` (e.g., `Architect-Review`, `SME-Consensus`, `Automated-Validation`) within `/master-knowledge-base/standards/registry/tag-glossary-definition.md` (e.g., as `gatekeeper/Architect-Review`) or a dedicated `gatekeepers.yaml` in the registry.
    *   **Task 0.2.8:** Ensure all vocabulary files in `/master-knowledge-base/standards/registry/` are created and populated.

*   **Step 0.3: Finalize Metadata Schema & Core Documentation Updates**
    *   **Task 0.3.1:** Update `U-METADATA-FRONTMATTER-RULES-001.md` (at its current path, to be renamed/moved in Phase 2) to:
        *   Add the new `standard_id` key (placed directly after `title`), specifying its regex (from Task 0.1.3).
        *   Add new keys: `primary_domain`, `sub_domain`, `scope_application`, `criticality`, `lifecycle_gatekeeper`, `impact_areas`, `change_log_url`.
        *   Define the frontmatter key order: `title`, `standard_id`, `aliases`, `tags`, `kb-id`, `info-type`, `primary-topic`, `related-standards`, `version`, `date-created`, `date-modified`, then the seven new extension keys.
        *   Clarify that filename SHOULD equal `standard_id`.
        *   Specify date fields (`date-created`, `date-modified`) MUST use full ISO-8601 date-time with "Z" (e.g., `2025-05-27T15:42:00Z`).
        *   Specify YAML frontmatter encoding: "UTF-8 (no BOM), LF line endings" for all Markdown files.
        *   Specify `change_log_url` can be relative (starting `./`, linter checks existence) or absolute (linter checks basic syntax).
    *   **Task 0.3.2:** Create `/master-knowledge-base/standards/templates/tpl-canonical-frontmatter.md` including `standard_id`, all other mandatory frontmatter keys, and ISO-8601 date format placeholders.
    *   **Task 0.3.3:** Update `O-USAGE-LINKS-001.md` (currently a section in `COL-TOOLING-OBSIDIAN.md`, to be extracted in Phase 1) to reflect the canonical link style `[[STANDARD_ID]]` and the transitional policy (Phase 0: `warning` for path-based links from linter).

*   **Step 0.4: Plan Directory Structure**
    *   **Task 0.4.1:** Document the target Layer 1 directory for atomic files as `/master-knowledge-base/standards/src/`.
    *   **Task 0.4.2:** Document the target directory for vocabulary manifests as `/master-knowledge-base/standards/registry/`.
    *   **Task 0.4.3:** Document the target directory for templates as `/master-knowledge-base/standards/templates/` with filenames prefixed `tpl-`.

*   **Step 0.5: Initial Automation Development (Prototypes in Python, located in `/master-knowledge-base/tools/`)**
    *   **Task 0.5.1:** Provide specifications, pseudocode, and Python skeletons for a prototype linter (`/tools/linter/kb_linter.py`) supporting severity levels (`info`, `warning`, `error`). The linter must:
        *   Enforce `standard_id` regex and uniqueness across files in `/standards/src/`.
        *   Check for presence of all mandatory frontmatter keys.
        *   Validate `date-created` and `date-modified` against ISO-8601 format.
        *   Validate values against controlled vocabularies loaded from `/standards/registry/` files.
        *   Check YAML encoding (UTF-8 no BOM, LF line endings).
        *   Check `change_log_url` (existence if relative, basic syntax if absolute).
        *   Issue `warning` for path-based internal links.
    *   **Task 0.5.2:** Provide specifications, pseudocode, and Python skeletons for a prototype `standards_index.json` generator (`/tools/indexer/generate_index.py`). The output `standards_index.json` must:
        *   Include a root-level `"schemaVersion": 1`.
        *   Parse all atomic files in `/standards/src/`.
        *   Extract key metadata: `standard_id`, `title`, `primary_domain`, `sub_domain`, `info-type`, `version`, `status` (from tags), filepath, `date-modified`.
    *   **Task 0.5.3:** Create a formal JSON Schema definition (`/tools/indexer/standards_index.schema.json`) for the structure of `standards_index.json`.
    *   **Task 0.5.4:** (Optional, based on Ehsan's confirmation of CI platform, e.g., GitHub Actions) Provide specifications for a basic CI workflow (`.github/workflows/standards_check.yml`) to run the linter and index generator, emitting a Markdown summary report of findings (counts of errors/warnings, index build status).

*   **Exit Criteria for Phase 0:**
    *   All foundational documents (`U-METADATA-FRONTMATTER-RULES-001.md` (updated), `O-USAGE-LINKS-001.md` (updated section placeholder), `tpl-canonical-frontmatter.md`, vocabulary manifests in `/standards/registry/`) are created/updated and committed.
    *   Prototype linter (specs/pseudocode/skeletons) defined, capable of validating `standard_id` (syntax, uniqueness) and other core checks on test files; issues `warning` for path-based links.
    *   Prototype `standards_index.json` generator (specs/pseudocode/skeletons) defined, including `schemaVersion` and its own JSON schema.
    *   (If CI confirmed) CI workflow (specs) defined to emit a summary report.

### Phase 1: Atomic Decomposition, Splitting & Metadata Enrichment

**Goal:** Convert existing "collection" based standards into initial atomic "Standard Definition" AND "Policy/Guideline" files, applying new naming and enriched metadata from the outset.

*   **Step 1.1: Process `master-knowledge-base/standards/COL-ARCH-UNIVERSAL.md`**
    *   **Task 1.1.1:** For each standard concept (U-ARCH-001, U-ARCH-002, U-STRUC-001, U-STRUC-002, U-DETAIL-LEVEL-001, U-FORMAT-NAMING-001) within `COL-ARCH-UNIVERSAL.md`:
        *   Analyze its content to identify "HOW/WHERE" (Standard Definition) vs. "WHAT/WHEN/WHY" (Policy/Guideline) aspects.
        *   Create one or two new atomic Markdown files in `/master-knowledge-base/standards/src/` based on the analysis (e.g., for U-ARCH-001, create `AS-STRUCTURE-KB-ROOT.md` and potentially `CS-POLICY-KB-ROOT.md`).
        *   Apply the new naming convention. Assign a unique `standard_id` (matching filename, adhering to regex from Task 0.1.3) to each new file.
        *   Populate all frontmatter fields for each new file using `tpl-canonical-frontmatter.md` as a base (including ISO-8601 dates, correct `primary_domain`, `sub_domain`, `scope_application`, `criticality`, `lifecycle_gatekeeper`, `impact_areas`, `change_log_url`).
        *   Set `info-type` to `standard-definition` or `policy-document` as appropriate.
        *   Migrate the relevant content (rule statements, examples, cross-references) into the appropriate new file(s).
        *   Update `related-standards` in the frontmatter of the new Standard Definition and Policy Document to link to each other if split from a single concept.
    *   **Task 1.1.2:** Mark `COL-ARCH-UNIVERSAL.md` for future deprecation by adding a deprecation notice at the top of the file.

*   **Step 1.2: Process `master-knowledge-base/standards/COL-CONTENT-UNIVERSAL.md`**
    *   **Task 1.2.1:** Repeat the sub-tasks from Task 1.1.1 for each standard concept (U-SCHEMA-METHOD-001, U-SCHEMA-CONCEPT-001, U-TONE-LANG-001, U-SCOPE-INCLUDE-001, U-SCOPE-EXCLUDE-001, U-ABSTR-DIGITAL-001) within `COL-CONTENT-UNIVERSAL.md`.
    *   **Task 1.2.2:** Mark `COL-CONTENT-UNIVERSAL.md` for future deprecation.

*   **Step 1.3: Process `master-knowledge-base/standards/COL-GOVERNANCE-UNIVERSAL.md`**
    *   **Task 1.3.1:** Repeat Task 1.1.1 for each standard concept (U-VERSIONING-001, U-GOVERNANCE-001, U-DEPRECATION-001, U-ONBOARDING-001, U-GLOSSARY-001, U-TEMPLATES-DIR-001, U-FILEHYGIENE-001) within `COL-GOVERNANCE-UNIVERSAL.md`. Note: `U-ONBOARDING-001` will have `info-type: guide-document`.
    *   **Task 1.3.2:** Mark `COL-GOVERNANCE-UNIVERSAL.md` for future deprecation.

*   **Step 1.4: Process `master-knowledge-base/standards/COL-LINKING-UNIVERSAL.md`**
    *   **Task 1.4.1:** Repeat Task 1.1.1 for each standard concept (U-INTERLINK-001, U-TAG-001, U-CITE-001, U-MODULAR-001, U-ACCESSIBILITY-001, U-ASSETS-001) within `COL-LINKING-UNIVERSAL.md`.
    *   **Task 1.4.2:** Mark `COL-LINKING-UNIVERSAL.md` for future deprecation.

*   **Step 1.5: Process `master-knowledge-base/standards/COL-SYNTAX-MARKDOWN.md`**
    *   **Task 1.5.1:** Repeat Task 1.1.1 for each standard concept (M-SYNTAX-YAML-001, M-SYNTAX-HEADINGS-001, etc.) within `COL-SYNTAX-MARKDOWN.md`.
    *   **Task 1.5.2:** Mark `COL-SYNTAX-MARKDOWN.md` for future deprecation.

*   **Step 1.6: Process `master-knowledge-base/standards/COL-TOOLING-OBSIDIAN.md`**
    *   **Task 1.6.1:** Repeat Task 1.1.1 for each standard concept (O-USAGE-LINKS-001, O-USAGE-TAGS-001, O-USAGE-FOLDERS-NOTES-001, O-USAGE-TOC-MANDATE-001, O-USAGE-TRANSCLUSION-001, O-USAGE-CALLOUTS-001, O-USAGE-TOC-PLUGIN-001) within `COL-TOOLING-OBSIDIAN.md`. This includes extracting `O-USAGE-LINKS-001` into its own atomic file.
    *   **Task 1.6.2:** Mark `COL-TOOLING-OBSIDIAN.md` for future deprecation.

*   **Step 1.7: Implement Specific Merging/Refactoring Decisions (ensuring Standard/Policy split)**
    *   **Task 1.7.1 (Internal Linking):** Create `/standards/src/SF-LINKS-INTERNAL-SYNTAX.md` (`info-type: standard-definition`) and `/standards/src/CS-LINKING-INTERNAL-POLICY.md` (`info-type: policy-document`), populating with full metadata and relevant content from original M-SYNTAX-LINKS-001 and O-USAGE-LINKS-001.
    *   **Task 1.7.2 (ToC):** Create `/standards/src/SF-TOC-STRUCTURE.md` (Standard Def) and `/standards/src/CS-TOC-MANDATE.md` (Policy), populating from U-STRUC-002 and O-USAGE-TOC-MANDATE-001/PLUGIN-001. Remove ToC mandate for atomic standard files.
    *   **Task 1.7.3 (Part Overview/Folder Notes):** Ensure rules for `_overview.md` structure are in an appropriate AS standard (e.g., `AS-STRUCTURE-PART-OVERVIEW.md`) and its mandate in a CS policy (e.g., `CS-POLICY-PART-OVERVIEW.md`). Remove all mentions of Obsidian folder note plugins from standards/policies.
    *   **Task 1.7.4 (Transclusion):** Create `/standards/src/SF-TRANSCLUSION-SYNTAX.md` (Standard Def) and `/standards/src/CS-MODULARITY-TRANSCLUSION-POLICY.md` (Policy) from U-MODULAR-001 and O-USAGE-TRANSCLUSION-001.
    *   **Task 1.7.5 (Callouts):** Create `/standards/src/SF-CALLOUTS-SYNTAX.md` (Standard Def, promoting O-USAGE-CALLOUTS-001) and `/standards/src/CS-ADMONITIONS-POLICY.md` (Policy).
    *   **Task 1.7.6 (Tagging):** Create `/standards/src/MT-TAGS-IMPLEMENTATION.md` (Standard Def) and `/standards/src/MT-TAGGING-STRATEGY-POLICY.md` (Policy) from U-TAG-001.
    *   **Task 1.7.7 (Conditional Text):** Ensure `SF-CALLOUTS-SYNTAX.md` lists `IF` as a type. Create `/standards/src/SF-CONDITIONAL-SYNTAX-ATTRIBUTES.md` (Standard Def for `attribute=value` syntax) and `/standards/src/CS-CONTENT-PROFILING-POLICY.md` (Policy, replacing `U-PROFILING-ATTRIBUTES-001.md`).

*   **Step 1.8: Refactor Guide Documents**
    *   **Task 1.8.1:** For `master-knowledge-base/standards/GUIDE-KB-USAGE-AND-STANDARDS.md`:
        *   Rename to `/master-knowledge-base/standards/src/GM-GUIDE-KB-USAGE.md`.
        *   Assign a unique `standard_id` (e.g., `GM-GUIDE-KB-USAGE`).
        *   Populate its full frontmatter, ensuring `info-type: guide-document`.
        *   Thoroughly revise its content to reflect the new atomic structure, the Standard/Policy split, and link to the new atomic files using `[[STANDARD_ID]]` style.
    *   **Task 1.8.2:** For `master-knowledge-base/standards/GUIDE-TASK-BASED.md`:
        *   Rename to `/master-knowledge-base/standards/src/GM-GUIDE-STANDARDS-BY-TASK.md`.
        *   Assign a unique `standard_id` (e.g., `GM-GUIDE-STANDARDS-BY-TASK`).
        *   Populate its full frontmatter, ensuring `info-type: guide-document`.
        *   Thoroughly revise its content to link to the new atomic files using `[[STANDARD_ID]]` style.

*   **Exit Criteria for Phase 1:**
    *   All standards from original collection files are decomposed into atomic Standard Definition and/or Policy/Guideline files in `/master-knowledge-base/standards/src/`.
    *   All new atomic files have complete and valid frontmatter (ISO dates, `standard_id`, etc.).
    *   Linter (prototype) now configured to `error` on path-based internal links, and passes on all files in `/standards/src/`.
    *   `standards_index.json` (prototype) builds successfully and includes all new atomic files.
    *   Guide documents (`GM-GUIDE-KB-USAGE.md`, `GM-GUIDE-STANDARDS-BY-TASK.md`) are refactored.
    *   Original collection files are marked with deprecation notices.
    *   CI (or script run) emits a summary report.

### Phase 2: Governance Review of Standard/Policy Boundary & Standalone/Utility Document Refactoring

**Goal:** Ensure consistent application of Standard/Policy separation. Refactor all remaining standalone and utility standards-related documents.

*   **Step 2.1: Review Atomic Files from Phase 1 for Standard/Policy Separation**
    *   **Task 2.1.1:** Systematically review each pair of (or standalone) Standard Definition and Policy/Guideline files created in Phase 1.
    *   **Task 2.1.2:** Verify that content is correctly allocated (HOW/WHERE in Standard Definition vs. WHAT/WHEN/WHY in Policy/Guideline).
    *   **Task 2.1.3:** Identify any ambiguities or overlaps. Refine content by moving text, merging, or further splitting files if necessary to ensure clean separation. Update `standard_id`s and filenames if splits occur.
    *   **Task 2.1.4:** Ensure `related-standards` links between corresponding Standard Definition/Policy files are accurate and use `[[STANDARD_ID]]` style.

*   **Step 2.2: Refactor Existing Standalone Standard Files**
    *   **Task 2.2.1:** For each standalone standard file (e.g., `U-KEYREF-SYNTAX-001.md`, `LLM-AUTOMATION-IO-SCHEMA-001.md`, `M-CONDITIONAL-TEXT-SYNTAX-001.md` (if not fully superseded by Task 1.7.7), `M-SYNTAX-TODO-001.md`, `U-ARCH-003-Directory-Structure-Source-Render.md`, `U-KEYREF-MANAGEMENT-001.md`, `U-METADATA-FRONTMATTER-RULES-001.md`, `U-METADATA-SLUG-KEY-001.md` (placeholder), `U-PUBLISHING-PIPELINE-OVERVIEW-001.md`, `U-RELTABLE-DEFINITION-001.md`, `U-SCHEMA-REFERENCE-001.md`, `U-SCHEMA-TASK-001.md`, `U-VALIDATION-METADATA-001.md`):
        *   Move to `/master-knowledge-base/standards/src/`.
        *   Apply the new naming convention and assign a unique `standard_id`.
        *   Analyze and split into "Standard Definition" (HOW/WHERE) and "Policy/Guideline" (WHAT/WHEN/WHY) components if necessary, creating new files in `/standards/src/` with appropriate `standard_id`s and `info-type`.
        *   Enrich metadata to the full set of frontmatter keys for all resulting atomic files.
        *   Ensure all internal links use `[[STANDARD_ID]]` style.

*   **Step 2.3: Refactor Glossary & Definition Files**
    *   **Task 2.3.1 (`master-knowledge-base/standards/GLOSSARY-STANDARDS-TERMS.md`):**
        *   Move to `/master-knowledge-base/standards/src/GM-GLOSSARY-STANDARDS-TERMS.md`.
        *   Assign `standard_id` (e.g., `GM-GLOSSARY-STANDARDS-TERMS`).
        *   Populate full frontmatter, `info-type: glossary-document`.
        *   Review and update terms based on new architecture; ensure links use `[[STANDARD_ID]]`.
    *   **Task 2.3.2 (`master-knowledge-base/tag-glossary-definition.md`):**
        *   Move to `/master-knowledge-base/standards/registry/tag-glossary-definition.md` (as per Phase 0).
        *   Assign `standard_id` (e.g., `MT-REGISTRY-TAG-GLOSSARY`).
        *   Populate full frontmatter, `info-type: tag-glossary-document`.
        *   Verify its content aligns with refactored tagging standards.
    *   **Task 2.3.3 (`master-knowledge-base/_key_definitions.md`):**
        *   Move to `/master-knowledge-base/standards/src/UA-KEYDEFS-GLOBAL.md` (or keep as `_key_definitions.md` in root if scripts rely on fixed path, but assign `standard_id` like `UA-KEYDEFS-GLOBAL`).
        *   Populate full frontmatter, `info-type: key-definition-set`.
    *   **Task 2.3.4 (`master-knowledge-base/standards/_kb_definition.md` for Standards KB):**
        *   Move to `/master-knowledge-base/standards/src/AS-MAP-STANDARDS-KB.md`.
        *   Assign `standard_id` (e.g., `AS-MAP-STANDARDS-KB`).
        *   Populate full frontmatter, `info-type: kb-definition-map`.
        *   Update its `parts:` structure to reference new atomic `[[STANDARD_ID]]`s or planned derived collection views.

*   **Step 2.4: Refactor Root & Navigational Files**
    *   **Task 2.4.1 (`master-knowledge-base/standards/root.md`):**
        *   Move to `/master-knowledge-base/standards/src/AS-ROOT-STANDARDS-KB.md`.
        *   Assign `standard_id` (e.g., `AS-ROOT-STANDARDS-KB`).
        *   Populate full frontmatter.
        *   Completely overhaul its Table of Contents to link to new atomic `[[STANDARD_ID]]`s or (conceptually) to where derived collection views will be.
    *   **Task 2.4.2 (`master-knowledge-base/kb-directory.md`):**
        *   Move to `/master-knowledge-base/src/AS-INDEX-KB-MASTER.md` (or similar top-level src if it's truly global).
        *   Assign `standard_id` (e.g., `AS-INDEX-KB-MASTER`).
        *   Populate full frontmatter.
        *   Update links to use `[[STANDARD_ID]]` if it references specific standards documents.

*   **Exit Criteria for Phase 2:**
    *   All atomic files from Phase 1 reviewed and refined for correct Standard/Policy separation.
    *   All standalone standards, glossaries, definition files, root/navigational files are refactored into `/standards/src/` (or other designated `src` locations), with new naming, `standard_id`, and full metadata.
    *   Linter passes on all files in `/standards/src/` (and other `src` locations).
    *   `standards_index.json` builds successfully and includes all refactored files.
    *   CI (or script run) emits a summary report.

### Phase 3: Template Finalization & Link Style Enforcement

**Goal:** Finalize templates and ensure all internal links strictly use the `[[STANDARD_ID]]` convention.

*   **Step 3.1: Finalize Template Files**
    *   **Task 3.1.1:** For all template files in `/master-knowledge-base/standards/templates/` (e.g., `tpl-canonical-frontmatter.md`, `tpl-standard-definition.md`, `tpl-policy-document.md`, `tpl-chapter.md`, etc.):
        *   Ensure their frontmatter placeholders include `standard_id` and all other new canonical keys.
        *   Ensure any example internal links use `[[PLACEHOLDER_STANDARD_ID]]` format.
    *   **Task 3.1.2:** Create a `README.md` within `/master-knowledge-base/standards/templates/` explaining the purpose of each template and when to use it.

*   **Step 3.2: Enforce `[[STANDARD_ID]]` Link Style Across All Refactored Content**
    *   **Task 3.2.1:** Perform a final verification scan of all Markdown files within `/master-knowledge-base/standards/src/` (and any other `src` directories containing refactored content).
    *   **Task 3.2.2:** Confirm the linter correctly identifies and errors on any remaining path-based internal links. Manually correct any stragglers.

*   **Exit Criteria for Phase 3:**
    *   All templates in `/standards/templates/` are finalized and documented with a README.
    *   All internal links within all refactored source Markdown files strictly use the `[[STANDARD_ID]]` format.
    *   Linter strictly enforces `[[STANDARD_ID]]` links and passes on all refactored source files.
    *   `standards_index.json` (with `schemaVersion`) is stable and reliably maps `standard_id`s to their respective filepaths.
    *   CI (or script run) emits a summary report.

### Phase 4: Design & Implementation of Derived Views & Production Automation

**Goal:** Realize the "Multi-View" aspect by designing and implementing generation of derived collections and production-ready automation tools.

*   **Step 4.1: Design and Implement Derived "Collection" View Generation**
    *   **Task 4.1.1:** Finalize the logic for generating views equivalent to the original "Collection" documents (e.g., a "Universal Architecture Collection"). This includes defining criteria for standard inclusion (e.g., based on `primary_domain` and `sub_domain` from `standards_index.json`).
    *   **Task 4.1.2:** Develop/refine Python script(s) (e.g., in `/tools/builder/`) to generate these derived views.
        *   Scripts will read `standards_index.json` to find relevant source files.
        *   Content from source files will be transcluded or concatenated into the derived view.
        *   Generated ToCs within these views will link to sections of aggregated content.
        *   Output to a `.gitignore`'d directory (e.g., `/dist/collections/` or `/site/collections/`).
        *   Internal links within transcluded content (`[[STANDARD_ID]]`) should resolve to anchors within the same collection view if the target is part of the collection, or to links to other collection views/atomic files if external to the current collection.

*   **Step 4.2: Productionize `standards_index.json` Generation**
    *   **Task 4.2.1:** Ensure the `/tools/indexer/generate_index.py` script is robust, handles all edge cases, and its output `standards_index.json` conforms to `/tools/indexer/standards_index.schema.json`.
    *   **Task 4.2.2:** Ensure `schemaVersion` in `standards_index.json` is correctly managed.

*   **Step 4.3: Productionize Metadata Validation Automation (Linter)**
    *   **Task 4.3.1:** Ensure the `/tools/linter/kb_linter.py` script is robust, covers all validation rules from `U-METADATA-FRONTMATTER-RULES-001.md` and `U-VALIDATION-METADATA-001.md` (once refactored), and uses severity levels effectively.
    *   **Task 4.3.2:** Integrate the linter into the CI/CD pipeline (if established) to run on every commit/PR, blocking merges on `error` severity.

*   **Exit Criteria for Phase 4:**
    *   Scripts for generating derived collection views are functional and produce human-readable, navigable outputs.
    *   `standards_index.json` generation is production-ready and its schema is validated.
    *   Metadata linter is production-ready and integrated (or runnable as a standalone check).
    *   Generated collection views are confirmed to be excluded from version control.
    *   CI (or script run) emits a summary report including counts of atoms/policies and status of derived view generation.

### Phase 5: Final Validation, Review & Documentation

**Goal:** Ensure the entire refactored system is correct, complete, documented, and meets all architectural goals.

*   **Step 5.1: Full System Validation**
    *   **Task 5.1.1:** Perform a comprehensive validation pass on all source files in `/standards/src/` using the production linter.
    *   **Task 5.1.2:** Generate all derived views and meticulously validate their content, structure, and link integrity (both internal to the view and external).
    *   **Task 5.1.3:** Test key navigational pathways in the generated derived views to ensure usability.

*   **Step 5.2: Final Peer Review & System Documentation**
    *   **Task 5.2.1:** Conduct a final peer review of the overall system: source structure in `/standards/src/`, generated derived views, and automation scripts in `/tools/`.
    *   **Task 5.2.2:** Create/update documentation for the development and maintenance workflow:
        *   How to add or update an atomic standard/policy.
        *   How to run the linter and indexer locally.
        *   How to regenerate derived views.
        *   Overview of the CI process (if applicable).
    *   **Task 5.2.3:** Prepare an annotated changelog Pull Request summarizing the entire refactoring effort for team review and merge into the main branch.

*   **Step 5.3: Iteration & Refinement Based on Final Review**
    *   **Task 5.3.1:** Address any critical issues identified during the final validation and peer review.
    *   **Task 5.3.2:** Incorporate feedback into documentation and scripts.

*   **Exit Criteria for Phase 5:**
    *   All source files pass linting with no errors.
    *   All defined derived views generate correctly and are validated.
    *   All process and system documentation is complete and accurate.
    *   Team review of the refactoring PR is completed, and changes are merged.
    *   Final CI (or script run) report indicates full system health and successful build.

---
