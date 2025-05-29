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

**Immediate Next Step:**
*   Finalize Template Files & Link Style Enforcement (Roadmap Phase 3, Step 7).
