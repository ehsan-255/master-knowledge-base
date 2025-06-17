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
## Standards Refactoring Summary (2025-05-29)

This note summarizes the investigation and refactoring of several standalone schema and governance standards.

**Files Newly Created:**

1.  **`AS-SCHEMA-REFERENCE.md`** (`standard_id: AS-SCHEMA-REFERENCE`):
    *   Created as `U-SCHEMA-REFERENCE-001.md` was not found.
    *   Defines the standard structure for reference documents (e.g., API docs, command references).
    *   Location: `/master-knowledge-base/standards/src/AS-SCHEMA-REFERENCE.md`.

2.  **`AS-SCHEMA-TASK.md`** (`standard_id: AS-SCHEMA-TASK`):
    *   Created as `U-SCHEMA-TASK-001.md` was not found.
    *   Defines the standard structure for task-oriented documents (e.g., tutorials, SOPs).
    *   Location: `/master-knowledge-base/standards/src/AS-SCHEMA-TASK.md`.

3.  **`QM-VALIDATION-METADATA.md`** (`standard_id: QM-VALIDATION-METADATA`):
    *   Created as `U-VALIDATION-METADATA-001.md` was not found.
    *   Defines procedures for validating document metadata against `MT-SCHEMA-FRONTMATTER.md`.
    *   Used `sub_domain: METRICS` for `QM` as `VALIDATION` was not in the registry. Noted for potential registry update.
    *   Location: `/master-knowledge-base/standards/src/QM-VALIDATION-METADATA.md`.

**Files Refactored (Moved & Updated):**

1.  **`GM-REGISTRY-GOVERNANCE.md`** (`standard_id: GM-REGISTRY-GOVERNANCE`):
    *   Content moved from `master-knowledge-base/standards/U-REGISTRIES-GOV-001.md`.
    *   Frontmatter fully populated according to `MT-SCHEMA-FRONTMATTER.md`.
    *   Used `sub_domain: POLICY` for `GM` as `GOVERNANCE` was not in the registry.
    *   Old file `U-REGISTRIES-GOV-001.md` deleted.
    *   Location: `/master-knowledge-base/standards/src/GM-REGISTRY-GOVERNANCE.md`.

**Files Not Found and Not Created (Action Deferred or Not Required by This Task):**
*   N/A for this specific set of tasks (all investigated items were either created or refactored).

**Verification Notes:**
*   The frontmatter for all new/refactored files was created in accordance with `MT-SCHEMA-FRONTMATTER.md`.
*   `date-created` and `date-modified` for new/updated files set to `2025-05-29T15:49:24Z`.

**Immediate Next Step (as per original plan for this subtask):**
*   Update `GM-GUIDE-KB-USAGE.md` (and potentially `GM-GUIDE-STANDARDS-BY-TASK.md`) with the new Standard IDs for `U-SCHEMA-REFERENCE-001` and `U-SCHEMA-TASK-001` (which are now `AS-SCHEMA-REFERENCE` and `AS-SCHEMA-TASK` respectively).

---
**Update Summary (2025-05-29T15:53:52Z):**

Following the refactoring/creation of schema and governance standards:

1.  **Updated `GM-GUIDE-KB-USAGE.md`**:
    *   Replaced `[[U-SCHEMA-REFERENCE-001]]` with `[[AS-SCHEMA-REFERENCE]]`.
    *   Replaced `[[U-SCHEMA-TASK-001]]` with `[[AS-SCHEMA-TASK]]`.
    *   `date-modified` updated to `2025-05-29T15:53:52Z`.

2.  **Updated `MT-SCHEMA-FRONTMATTER.md`**:
    *   Added `[[QM-VALIDATION-METADATA]]` to its `related-standards` list.
    *   `date-modified` updated to `2025-05-29T15:53:52Z`.

**Immediate Next Step:**
*   Proceed to "Refactor Other Remaining Standalone Standards (Roadmap Step 2.2)".

---
**Update Summary (2025-05-29T15:55:50Z):**

Investigation and refactoring of further standalone standards:

1.  **`UA-SCHEMA-LLM-IO.md` (`standard_id: UA-SCHEMA-LLM-IO`)**:
    *   Created at `/master-knowledge-base/standards/src/UA-SCHEMA-LLM-IO.md` as `LLM-AUTOMATION-IO-SCHEMA-001.md` was not found.
    *   Defines standard I/O data structures for LLM automation scripts.
    *   `primary_domain: UA`, `sub_domain: AUTOMATION`.

2.  **`U-METADATA-SLUG-KEY-001.md`**:
    *   Not found. Its purpose was determined to be unclear or likely covered by existing standards (`SF-CONVENTIONS-NAMING.md`, `MT-SCHEMA-FRONTMATTER.md`).
    *   No new file created; considered superseded or not needed at this time.

3.  **`OM-OVERVIEW-PUBLISHING-PIPELINE.md` (`standard_id: OM-OVERVIEW-PUBLISHING-PIPELINE`)**:
    *   Created at `/master-knowledge-base/standards/src/OM-OVERVIEW-PUBLISHING-PIPELINE.md` as `U-PUBLISHING-PIPELINE-OVERVIEW-001.md` was not found.
    *   Provides a high-level overview of the KB publishing pipeline.
    *   `primary_domain: OM`, `sub_domain: OVERVIEW`. Noted `OVERVIEW` for potential addition to `OM` in `subdomain_registry.yaml`.

4.  **`AS-SCHEMA-RELTABLE-DEFINITION.md` (`standard_id: AS-SCHEMA-RELTABLE-DEFINITION`)**:
    *   Created at `/master-knowledge-base/standards/src/AS-SCHEMA-RELTABLE-DEFINITION.md` as `U-RELTABLE-DEFINITION-001.md` was not found.
    *   Defines a schema for "Reltables" (relational table-like data). Contains a TODO for further content definition.
    *   `primary_domain: AS`, `sub_domain: SCHEMA`.

All new files include full frontmatter per `MT-SCHEMA-FRONTMATTER.md`, with `date-created` and `date-modified` set to `2025-05-29T15:55:50Z`.

---
**Placeholder Resolution Summary (2025-05-29T15:55:50Z):**

1.  **`HYPOTHESIS-TESTING_ID_PLACEHOLDER`** in `AS-SCHEMA-CONCEPT-DEFINITION.md`:
    *   Action: Replaced with illustrative `[[CONCEPT-HYPOTHESIS-TESTING]]` as it's in an example's "See Also" section.
2.  **`P-VALUE_ID_PLACEHOLDER`** in `AS-SCHEMA-CONCEPT-DEFINITION.md`:
    *   Action: Replaced with illustrative `[[CONCEPT-P-VALUE]]` as it's in an example's "See Also" section.
3.  **`ANOTHER-RELEVANT-STANDARD_ID_PLACEHOLDER`** in `AS-STRUCTURE-DOC-CHAPTER.md`:
    *   Action: Replaced with illustrative `[[EXAMPLE-STANDARD-ID]]` as it's in an example "See Also" section.
4.  **`CORE-CONCEPT-RESEARCH_ID_PLACEHOLDER`** in `AS-STRUCTURE-DOC-CHAPTER.md`:
    *   Action: Replaced with illustrative `[[CONCEPT-CORE-RESEARCH-METHODOLOGY]]` as it's in an example "See Also" section.
5.  **`FILENAME_ID_PLACEHOLDER`** in comments within `AS-STRUCTURE-KB-PART.md`, `AS-STRUCTURE-KB-ROOT.md`, `AS-STRUCTURE-MASTER-KB-INDEX.md`:
    *   Action: Verified these are in comments explaining link formats. Clarified related comments by removing "(to be updated with actual ID)" for already valid links. No change to the `FILENAME_ID_PLACEHOLDER` text itself as it's meta-commentary.
6.  **`Advanced Settings Guide_ID_PLACEHOLDER`** in `CS-CONTENT-PROFILING-POLICY.md`:
    *   Action: Replaced with illustrative `[[GUIDE-FEATURE-ADVANCED-SETTINGS]]` as it's in an example showing a link to a more detailed guide.
7.  **`NEW-STANDARD-ID_PLACEHOLDER`** in `OM-POLICY-STANDARDS-DEPRECATION.md`:
    *   Action: Replaced with illustrative `[[XX-REPLACEMENT-STANDARD-ID]]` as it's in an example deprecation notice.

---
**Update Summary (2025-05-29T16:04:35Z):**

Refactored Glossary and Definition Files (Roadmap Step 2.3):

1.  **`GM-GLOSSARY-STANDARDS-TERMS.md` (`standard_id: GM-GLOSSARY-STANDARDS-TERMS`)**:
    *   Created at `/master-knowledge-base/standards/src/GM-GLOSSARY-STANDARDS-TERMS.md` as it was not found.
    *   Populated with initial structure and example terms related to existing standards.
    *   `primary_domain: GM`, `sub_domain: GLOSSARY`.

2.  **`MT-REGISTRY-TAG-GLOSSARY.md` (formerly `tag-glossary-definition.md`)**:
    *   Located at `/master-knowledge-base/standards/registry/tag-glossary-definition.md`.
    *   Frontmatter updated: added `standard_id: MT-REGISTRY-TAG-GLOSSARY`, `primary_domain: MT`, `sub_domain: REGISTRY`, `kb-id: kb-id/standards`. `info-type` changed to `registry-document`. Version reset to `1.0.0`. `date-modified` updated. `related-standards` and introduction text updated.
    *   File path remains in `/registry/` for now.

3.  **`UA-KEYDEFS-GLOBAL.md` (`standard_id: UA-KEYDEFS-GLOBAL`)**:
    *   Created at `/master-knowledge-base/standards/src/UA-KEYDEFS-GLOBAL.md` as `_key_definitions.md` was not found in `master-knowledge-base/`.
    *   Populated with structure for key definitions (actual keys in frontmatter) and a TODO for full content. Includes example keys.
    *   `primary_domain: UA`, `sub_domain: KEYDEFS`.

4.  **`AS-MAP-STANDARDS-KB.md` (`standard_id: AS-MAP-STANDARDS-KB`)**:
    *   Created at `/master-knowledge-base/standards/src/AS-MAP-STANDARDS-KB.md` as `_kb_definition.md` for Standards KB was not found.
    *   Populated with basic structure for a KB definition map and a TODO for full content.
    *   `primary_domain: AS`, `sub_domain: STRUCTURE` (noting `MAP` or `INDEXING` might be better future subdomains for AS).

All new/updated files use `date-created` (if new) and `date-modified` as `2025-05-29T16:04:35Z`.

---
**Update Summary (2025-05-29T16:10:25Z):**

Refactored Root and Navigational Files (Roadmap Step 2.4):

1.  **`AS-ROOT-STANDARDS-KB.md` (`standard_id: AS-ROOT-STANDARDS-KB`)**:
    *   Created in `/master-knowledge-base/standards/src/` as `master-knowledge-base/standards/root.md` was not found.
    *   Populated with full frontmatter (`info-type: navigation-document`, `primary_domain: AS`, `sub_domain: STRUCTURE`) and a basic Table of Contents structure with TODOs.
    *   `date-created`/`modified`: `2025-05-29T16:10:25Z`.

2.  **`AS-INDEX-KB-MASTER.md` (`standard_id: AS-INDEX-KB-MASTER`)**:
    *   Created at `/master-knowledge-base/AS-INDEX-KB-MASTER.md` as `master-knowledge-base/kb-directory.md` was not found.
    *   Populated with full frontmatter (`info-type: navigation-document`, `primary_domain: AS`, `sub_domain: STRUCTURE` - noting `INDEXING` for future) and placeholder content listing known KBs with TODOs for links.
    *   `date-created`/`modified`: `2025-05-29T16:10:25Z`.

---
**Phase 2, Step 6: Systematic Governance Review Preparation (2025-05-29T16:10:25Z):**

**Identified Standard/Policy Pairs:**
*   `AS-STRUCTURE-KB-ROOT.md` (Structure) and `CS-POLICY-KB-ROOT.md` (Policy)
*   `AS-STRUCTURE-KB-PART.md` (Structure) and `CS-POLICY-KB-PART-CONTENT.md` / `CS-POLICY-PART-OVERVIEW.md` (Policy)
*   `AS-STRUCTURE-DOC-CHAPTER.md` (Structure) and `CS-POLICY-DOC-CHAPTER-CONTENT.md` (Policy)
*   `SF-LINKS-INTERNAL-SYNTAX.md` (Syntax) and `CS-LINKING-INTERNAL-POLICY.md` (Policy)
*   `SF-CALLOUTS-SYNTAX.md` (Syntax for general callouts) and `CS-ADMONITIONS-POLICY.md` (Policy on using admonition-type callouts).
*   `SF-CONDITIONAL-SYNTAX-ATTRIBUTES.md` (Syntax for conditional attributes) and `CS-CONTENT-PROFILING-POLICY.md` (Policy on content profiling).
*   `SF-TRANSCLUSION-SYNTAX.md` (Syntax) and `CS-MODULARITY-TRANSCLUSION-POLICY.md` (Policy)
*   `SF-ACCESSIBILITY-IMAGE-ALT-TEXT.md` (Syntax/Implementation) and `CS-POLICY-ACCESSIBILITY.md` (Broader Policy)
*   `SF-TOC-SYNTAX.md` (Syntax) and `CS-TOC-POLICY.md` (Policy)
*   `MT-TAGS-IMPLEMENTATION.md` (Implementation/Syntax) and `MT-TAGGING-STRATEGY-POLICY.md` (Policy)
*   `MT-KEYREF-MANAGEMENT.md` (Management/Operational Policy) related to `UA-KEYDEFS-GLOBAL.md` (Definitions) and `SF-SYNTAX-KEYREF.md` (Syntax).
*   `GM-REGISTRY-GOVERNANCE.md` (Policy) related to specific registries like `MT-REGISTRY-TAG-GLOSSARY.md`.

**Sampled Pair Review Findings:**

1.  **`AS-STRUCTURE-DOC-CHAPTER.md` vs. `CS-POLICY-DOC-CHAPTER-CONTENT.md`**:
    *   Review: Good separation. `AS-STRUCTURE-DOC-CHAPTER` defines the structural skeleton (HOW/WHERE). `CS-POLICY-DOC-CHAPTER-CONTENT` defines rules for content within that skeleton, like heading usage for sub-topics (WHAT/WHEN/WHY). No immediate misallocations noted.

2.  **`SF-LINKS-INTERNAL-SYNTAX.md` vs. `CS-LINKING-INTERNAL-POLICY.md`**:
    *   Review: Excellent separation. `SF-LINKS-INTERNAL-SYNTAX` details the "HOW" (syntax of `[[ID]]`, aliases, heading links). `CS-LINKING-INTERNAL-POLICY` details the "WHAT, WHEN, WHY" (use links extensively, descriptive text, "See Also" sections, contextual relevance). No misallocations noted.

3.  **`MT-TAGS-IMPLEMENTATION.md` vs. `MT-TAGGING-STRATEGY-POLICY.md`**:
    *   Review: Good separation. `MT-TAGS-IMPLEMENTATION` focuses on "HOW/WHERE" (YAML syntax, kebab-case, hierarchy, reference to glossary). `MT-TAGGING-STRATEGY-POLICY` focuses on "WHAT, WHEN, WHY" (mandatory tag categories, conformance to glossary, rationale).
    *   Update: Both files correctly updated to reference `[[MT-SCHEMA-FRONTMATTER]]` instead of the old `[[U-METADATA-FRONTMATTER-RULES-001]]`. `date-modified` fields updated to `2025-05-29T16:10:25Z`.

**Recommendation:**
A human reviewer should systematically go through all identified Standard/Policy pairs and other standalone standards (especially those in `AS`, `SF`, `MT` vs. `CS`, `OM`, `GM` domains) to ensure adherence to the Standard Definition (HOW/WHERE) vs. Policy Document (WHAT/WHEN/WHY) separation principle. Particular attention should be paid to ensuring policy documents articulate mandates and rationale, while definition documents focus on technical specifications and syntax.

---
**Update Summary (2025-05-29T16:30:41Z):**

Finalized Template Files & Created README (Roadmap Task 3.1.1 & 3.1.2):

1.  **`tpl-canonical-frontmatter.md`**:
    *   Reviewed content. Internal links in comments (e.g., to `[[MT-REGISTRY-TAG-GLOSSARY]]`, `[[domain_codes.yaml]]`) are appropriate for their purpose.
    *   Alignment with `[[MT-SCHEMA-FRONTMATTER]]` re-verified.
    *   `date-modified` updated to `2025-05-29T16:30:41Z`.

2.  **`/master-knowledge-base/standards/templates/README.md`**:
    *   Created this new file.
    *   Content explains the purpose of the templates directory, lists available templates (currently `tpl-canonical-frontmatter.md`), describes their purpose, and notes they should be kept aligned with core standards.

**Note on Link Style Enforcement (Roadmap Task 3.2.1):**
*   A full, systematic scan and enforcement of `[[STANDARD_ID]]` link styles across all documents will be more effectively performed once linting tools (Roadmap Step 8) are further developed or as part of a final system validation phase (Roadmap Step 10). Current refactoring efforts focus on updating known incorrect links and using the correct style in new/refactored documents.

---
**Update Summary (2025-05-29T16:30:41Z):**

Develop Specifications and Python Skeletons for Linter and Indexer Tools (Roadmap Task 0.5):

1.  **Linter - `kb_linter.py` & `README.md`**:
    *   `/master-knowledge-base/tools/linter/kb_linter.py`: Overwritten with specified skeleton code including specifications for checks (frontmatter, file hygiene, key validation, link styles, etc.) and basic function structure.
    *   `/master-knowledge-base/tools/linter/README.md`: Created, explaining the linter's purpose, planned features, and usage.

2.  **Indexer - `generate_index.py` & `README.md`**:
    *   `/master-knowledge-base/tools/indexer/generate_index.py`: Overwritten with specified skeleton code including specifications for metadata extraction (standard_id, title, domain, status, etc.) and outputting `standards_index.json`.
    *   `/master-knowledge-base/tools/indexer/README.md`: Created, explaining the indexer's purpose.

3.  **Indexer Schema - `standards_index.schema.json`**:
    *   `/master-knowledge-base/tools/indexer/standards_index.schema.json`: Overwritten with the specified JSON schema defining the structure for `standards_index.json`.

---
**Update Summary (2025-05-29T16:30:41Z):**

Design Specifications and Python Skeleton for Derived "Collection" View Generation (Roadmap Task 4.1):

1.  **Collection View Generator - `generate_collections.py`**:
    *   Created `/master-knowledge-base/tools/builder/generate_collections.py` with Python skeleton code.
    *   Skeleton includes specifications for input (standards index, collection definitions), logic (filtering, content aggregation, ToC generation, link resolution), and output (Markdown collection files).
    *   Basic function structure and example logic/simulation provided.

2.  **README for Builder**:
    *   Created `/master-knowledge-base/tools/builder/README.md`, explaining the purpose, planned features, and conceptual usage of the collection generator.

3.  **Example Collection Definitions**:
    *   Created `/master-knowledge-base/tools/builder/collection_definitions.yaml` with sample definitions for "Architecture & Structure Standards" and "Syntax & Formatting Standards" to guide development.

---
**Phase 4, Step 10: Full System Validation Planning (2025-05-29T16:30:41Z):**

This section outlines the planned process for Full System Validation (Roadmap Task 5.1), which is crucial for ensuring the integrity, consistency, and functionality of the entire refactored knowledge base ecosystem.

**A. Prerequisite Tool Completion:**
The execution of full system validation is contingent upon the production-ready implementation of the following key automation tools:
1.  **`kb_linter.py` (Linter - Roadmap Task 0.5.1):**
    *   Must comprehensively parse all standards in `/master-knowledge-base/standards/src/`.
    *   Must validate frontmatter against all rules in `[[MT-SCHEMA-FRONTMATTER]]` (key presence, order, data types, controlled vocabularies, regex patterns, ISO date formats, `change_log_url` checks).
    *   Must validate YAML syntax against `[[SF-SYNTAX-YAML-FRONTMATTER]]`.
    *   Must validate file hygiene (UTF-8 no BOM, LF line endings) against `[[SF-FORMATTING-FILE-HYGIENE]]`.
    *   Must check for `[[STANDARD_ID]]` link styles and attempt to resolve/flag broken links using `standards_index.json`.
    *   Must check that filenames (sans `.md`) match the `standard_id` field where applicable.
    *   Must generate a comprehensive error/warning report.
2.  **`generate_index.py` (Indexer - Roadmap Task 0.5.2):**
    *   Must be production-ready, accurately parsing all standard documents and generating a complete and correct `standards_index.json` file as per `[[standards_index.schema.json]]`.
3.  **`generate_collections.py` (Collection Builder - Roadmap Task 4.1):**
    *   Must be production-ready, capable of parsing `collection_definitions.yaml` and generating all defined derived collection views with correct content aggregation, Table of Contents, and resolved internal links.

**B. Validation Steps - Source File Validation (Roadmap Task 5.1.1):**
1.  **Generate Index:** Execute the production-ready `generate_index.py` to ensure `standards_index.json` is current and accurate.
2.  **Run Linter:** Execute the production-ready `kb_linter.py` across all Markdown files in `/master-knowledge-base/standards/src/` and any other relevant content directories (e.g., `/master-knowledge-base/standards/registry/` if Markdown files there are to be linted).
3.  **Analyze Linter Report:**
    *   All reported **errors** MUST be investigated and fixed.
    *   All reported **warnings** SHOULD be reviewed and addressed to ensure best practices.
4.  **Manual Spot-Checks:**
    *   Select a diverse sample of 10-15 atomic standards.
    *   Manually review for clarity, correctness of content, and proper adherence to the Standard Definition (HOW/WHERE) vs. Policy (WHAT/WHEN/WHY) separation principle. This follows up on the initial review preparation (Phase 2, Step 6).
    *   Verify that cross-references (`related-standards` and in-text links) are logical and point to the correct current standards.

**C. Validation Steps - Derived View Validation (Roadmap Task 5.1.2):**
1.  **Generate Collections:** Execute the production-ready `generate_collections.py` to build all derived collection views defined in `collection_definitions.yaml`.
2.  **Review Each Collection View:**
    *   **Content Accuracy:** Confirm that the correct set of standards is included in each collection based on its definition.
    *   **Structural Integrity:** Verify that each collection document has a working Table of Contents. Check that content from aggregated standards is presented clearly and in a logical order.
    *   **Link Integrity:**
        *   Links to standards *within the same collection* should function as internal anchor links.
        *   Links to standards *not in the current collection* should either remain as `[[STANDARD_ID]]` (for later processing by a site generator) or be valid relative links to other generated collection files if such a linking scheme is implemented.
    *   **Formatting & Readability:** Spot-check for major formatting issues or problems with readability that might have arisen during aggregation.

**D. Validation Steps - Navigational Pathway Testing (Roadmap Task 5.1.3):**
1.  **Master Navigation:**
    *   Start from `[[AS-INDEX-KB-MASTER]]`. Verify links to individual Knowledge Base root files (e.g., `[[AS-ROOT-STANDARDS-KB]]`).
2.  **KB-Level Navigation:**
    *   From each KB root file (e.g., `[[AS-ROOT-STANDARDS-KB]]`), test links to its major sections, parts, or collections.
3.  **Collection Navigation:**
    *   Within generated collection views, test the generated Table of Contents links.
4.  **Cross-Standard Linking:**
    *   From a sample of atomic standards, test links in their `related-standards` frontmatter field and a few key in-text `[[STANDARD_ID]]` links to ensure they point to the correct current documents.
5.  **Discoverability:**
    *   Assess if key standards and policies are reasonably discoverable through the main navigational pathways.

**Execution Note:**
The actual *execution* of this Full System Validation is pending the full implementation and stabilization of the `kb_linter.py`, `generate_index.py`, and `generate_collections.py` tools. This plan will guide that future validation effort.

---
**Phase 4, Step 11: Final Peer Review & System Documentation Planning (2025-05-29T16:30:41Z):**

This step outlines the creation of comprehensive workflow documentation and the items to be covered in a final human peer review.

**1. Development and Maintenance Workflow Documentation Outline (Roadmap Task 5.2.2)**
This documentation will guide contributors and maintainers. It should eventually reside in a dedicated guide (e.g., `GM-GUIDE-STANDARDS-MAINTENANCE.md`). The outline includes:
    *   **1. Introduction:**
        *   Purpose of the workflow documentation.
        *   Overview of the Single-Source Multi-View Standards Architecture (referencing `[[AS-KB-DIRECTORY-STRUCTURE]]` and other relevant architectural docs).
    *   **2. Managing Atomic Standards (`/master-knowledge-base/standards/src/`):**
        *   Proposing new standards/policies (ref: `[[OM-POLICY-STANDARDS-GOVERNANCE]]`).
        *   Choosing `standard_id` and filename (ref: `[[SF-CONVENTIONS-NAMING]]`, `[[MT-SCHEMA-FRONTMATTER]]`).
        *   Using templates (ref: `[[AS-STRUCTURE-TEMPLATES-DIRECTORY]]`, `[[tpl-canonical-frontmatter.md]]`).
        *   Populating frontmatter (ref: `[[MT-SCHEMA-FRONTMATTER]]`).
        *   Writing content: Standard Definitions (HOW/WHERE) vs. Policy Documents (WHAT/WHEN/WHY).
        *   Linking to other standards (ref: `[[SF-LINKS-INTERNAL-SYNTAX]]`, `[[CS-LINKING-INTERNAL-POLICY]]`).
        *   Versioning (ref: `[[OM-VERSIONING-CHANGELOGS]]`) and `change_log_url`.
    *   **3. Managing Registries (`/master-knowledge-base/standards/registry/`):**
        *   Process for updating controlled vocabularies (e.g., `[[domain_codes.yaml]]`, `[[MT-REGISTRY-TAG-GLOSSARY]]`).
        *   Referencing `[[GM-REGISTRY-GOVERNANCE]]`.
    *   **4. Using Automation Tools (once fully developed):**
        *   Linter (`kb_linter.py`): Purpose, basic command, interpreting output.
        *   Indexer (`generate_index.py`): Purpose, basic command.
        *   Collection Builder (`generate_collections.py`): Purpose, basic command, managing `collection_definitions.yaml`.
    *   **5. CI/CD Pipeline Overview (if applicable):**
        *   Brief explanation of automated checks during PRs or merges.
    *   **6. Deprecating a Standard:**
        *   Process (ref: `[[OM-POLICY-STANDARDS-DEPRECATION]]`).
    *   **7. Getting Help:**
        *   Links to key architectural documents (e.g., `[[AS-INDEX-KB-MASTER]]`, `[[AS-ROOT-STANDARDS-KB]]`, `[[AS-MAP-STANDARDS-KB]]`).
        *   Contact points or channels.

**2. Scope for Final Peer Review (Roadmap Task 5.2.1)**
The final human peer review should encompass a holistic assessment of the refactored system:
    *   **Overall Structure:** Review the organization of atomic standards in `/master-knowledge-base/standards/src/` and registry files in `/master-knowledge-base/standards/registry/`.
    *   **Core Schema Documents:** Thoroughly review `[[MT-SCHEMA-FRONTMATTER]]`, `[[SF-SYNTAX-YAML-FRONTMATTER]]`, and `[[SF-FORMATTING-FILE-HYGIENE]]` for clarity, correctness, and completeness, as they are foundational.
    *   **Standard vs. Policy Separation:** Verify the correct distinction between Standard Definition content (HOW/WHERE) and Policy Document content (WHAT/WHEN/WHY) across a significant sample of paired and standalone documents.
    *   **Content Clarity & Accuracy:** Review the actual content of key standards and policies for accuracy, clarity, and actionable guidance.
    *   **Navigational Integrity:** Review `[[AS-INDEX-KB-MASTER]]`, `[[AS-ROOT-STANDARDS-KB]]`, and `[[AS-MAP-STANDARDS-KB]]` for clarity and correctness of navigation.
    *   **Derived Views (once tools are production-ready):** Review sample generated collection documents for accuracy, completeness, and usability.
    *   **Automation Scripts (once implemented):** Code review of `kb_linter.py`, `generate_index.py`, and `generate_collections.py` for logic, correctness, and efficiency.
    *   **Workflow Documentation:** Review the "Development and Maintenance Workflow Documentation" (outlined above) for clarity, accuracy, and completeness.
    *   **Glossaries:** Review `[[GM-GLOSSARY-STANDARDS-TERMS]]` and `[[MT-REGISTRY-TAG-GLOSSARY]]` for accuracy and completeness.

---
**Update Summary (2025-05-29T16:30:41Z):**

Linter Core Functionality Implemented (Roadmap Task 0.5.1 - Initial):
*Note: This entry reflects the *initial* core functionality as requested in a previous step with the same timestamp. Subsequent steps will enhance this.*

1.  **`kb_linter.py` Enhancements**:
    *   Implemented file reading with `FileNotFoundError` handling.
    *   Added frontmatter parsing using `yaml.safe_load()`, with error handling for missing frontmatter or invalid YAML.
    *   Implemented check for **LF line endings** (warns for CRLF or CR).
    *   Implemented check for **UTF-8 BOM** (warns if BOM is present).
    *   Implemented check for **Mandatory Keys** (currently `title`, `info-type`, `version`, `date-created`, `date-modified`). Adds errors if missing.
    *   Implemented basic **Key Order** check for the specified subset of keys. Adds warnings for deviations.
    *   Implemented **`standard_id` Regex Validation** (`^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`). Adds errors if non-compliant.
    *   Implemented **Date Format Validation** for `date-created` and `date-modified` (ISO-8601 `YYYY-MM-DDTHH:MM:SSZ`). Adds errors if non-compliant.
    *   Reporting includes filepath, message, and line number (approximated for some errors like missing keys or whole-block issues).

2.  **`main()` Function Updated for Testing**:
    *   The `main` function in `kb_linter.py` now lints `MT-SCHEMA-FRONTMATTER.md`, `AS-SCHEMA-CONCEPT-DEFINITION.md`, and a dynamically created `dummy_lint_test.md` file containing known errors to demonstrate linter output.
    *   Results (errors, warnings, infos) are printed to the console for each file.
    *   The dummy file is cleaned up after the run.

---
**Update Summary (2025-05-29T16:30:41Z):**

Indexer Core Functionality Implemented (Roadmap Task 0.5.2):

1.  **`generate_index.py` Enhancements**:
    *   `extract_metadata(filepath, file_content)` function enhanced to parse YAML frontmatter from `file_content`.
    *   Extracts `standard_id`, `title`, `primary_domain`, `sub_domain`, `info-type`, `version`, `status` (derived from tags via new `get_status_from_tags` helper), `filepath` (relative to repo root), and `date-modified`.
    *   Skips files if `standard_id` or `title` are missing, or if other essential fields for indexing logic (like `info-type`, `version`, `date-modified`, `status`) are not found.
    *   `main()` function implements directory traversal for `/master-knowledge-base/standards/src/` using `os.walk()`.
    *   Processes only `.md` files.
    *   Calls `extract_metadata` for each file and appends valid results to the index.
    *   Includes `schemaVersion` and `generatedDate` in the output.
    *   Writes the index to `/master-knowledge-base/dist/standards_index.json`, creating the `/dist/` directory if needed.
    *   Basic error handling for file operations included.

---
**Update Summary (2025-05-29T16:30:41Z):**

Linter Enhancements - Vocabulary, Filename, and Link Validation:

1.  **Vocabulary Loading:**
    *   Added helper `load_yaml_vocab` to load `domain_codes.yaml` and `subdomain_registry.yaml`.
    *   Added helper `load_standards_index` to load `standards_index.json`.
    *   Hardcoded representative lists for `info-type` (from `MT-SCHEMA-FRONTMATTER.md`) and `criticality` values, and `tag_categories` (from `MT-REGISTRY-TAG-GLOSSARY.md`) with TODOs for dynamic parsing.
2.  **Extended Validation Checks in `lint_file`:**
    *   **Controlled Vocabularies:**
        *   `primary_domain`: Validated against loaded `domain_codes_list`.
        *   `sub_domain`: Validated against loaded `subdomain_registry_data` based on `primary_domain`.
        *   `info-type`: Validated against `HARDCODED_INFO_TYPES`.
        *   `criticality`: Validated against `HARDCODED_CRITICALITY_VALUES`.
        *   `tags`: Validated for kebab-case syntax and against `HARDCODED_TAG_CATEGORIES` prefixes.
    *   **`change_log_url` Validity:**
        *   If relative (`./`), checks for file existence.
        *   If absolute (`http(s)://`), checks for basic URL syntax.
    *   **Filename Matches `standard_id`:** If `standard_id` exists, warns if filename base doesn't match.
    *   **Internal Link Style and Existence:**
        *   Scans body content for `[[LINK]]` patterns.
        *   Warns if `LINK` appears to be a path rather than a `STANDARD_ID`.
        *   If `LINK` appears to be a `STANDARD_ID`, checks for its existence in the loaded `standards_index_data`. Warns if not found (potentially broken link).
3.  **`main()` Function Updated:**
    *   Loads vocabularies and index at the start.
    *   `dummy_lint_test.md` updated with test cases for new validation rules.
    *   Linter is called with loaded vocabularies and index.

---
**Update Summary (2025-05-29T16:30:41Z):**

Collection View Generator - Advanced Link Resolution:

1.  **Enhanced `generate_single_collection` function:**
    *   **Identify Included Standard IDs:** Creates a set of `standard_id`s for standards included in the current collection (derived from `filter_standards` result).
    *   **Anchor Generation:** Uses a refined `generate_anchor_for_standard(standard_id)` (using the ID itself for the anchor, making it unique and simple) for H2 headings (`<a id="anchor-id"></a>`) and ToC links.
    *   **Link Processing in Content Body:**
        *   A new `resolve_internal_links(body_content, current_collection_standard_ids, all_standards_map)` function is implemented.
        *   Uses regex `r"\[\[([A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+)(\#[A-Za-z0-9\-]+)?((\|)([^\]]+))?\]\]"` to find `[[STANDARD_ID]]`, `[[STANDARD_ID#anchor]]`, and aliased versions.
        *   If `LINKED_STANDARD_ID` is in `current_collection_standard_ids`:
            *   Replaces with an anchor link `[Display Text](#generated-anchor-for-LINKED_STANDARD_ID)`. The display text is the alias if present, otherwise the title of the target standard (from `all_standards_map`), or finally the `LINKED_STANDARD_ID` itself. Original sub-anchors (e.g., `#section`) are currently dropped for intra-collection links, which now point to the H2 of the standard's section.
        *   If `LINKED_STANDARD_ID` is NOT in the current collection:
            *   The link remains as `[[LINKED_STANDARD_ID#optional-anchor|OptionalAlias]]` or `[[LINKED_STANDARD_ID#optional-anchor]]` or `[[LINKED_STANDARD_ID|OptionalAlias]]` or `[[LINKED_STANDARD_ID]]` for downstream processing.
    *   The `resolve_internal_links` function is called on the body content of each standard before aggregation.
2.  **Refined H2 Heading and ToC Anchors:**
    *   Ensured `generate_anchor_for_standard(standard_id)` is used consistently for H2 `id` attributes and ToC `href` values, using the `standard_id` directly for anchor generation.
3.  **`main()` Function Notes:**
    *   `load_standards_index` updated to return a dictionary keyed by `standard_id` for efficient lookups.
    *   `filter_standards` adapted to work with the standards map.
    *   The `main` function structure is suitable for testing these enhancements assuming the input `standards_index.json` and `collection_definitions.yaml` are appropriately populated with inter-linking standards. (Actual content of these data files is outside this script's direct modification).
    *   Added print statements to log link resolution actions.

**Immediate Next Step:**
*   Testing and Iteration.

[end of master-knowledge-base/note.md]
