---
title: Phase B Completion Roadmap - Detailed Sequential Instructions
standard_id: project-roadmap-phase-b-completion
aliases: [Phase B Roadmap, Phase B Instructions]
tags: [status/active, info-type/project-roadmap, topic/project-planning, project-phase/phase-b]
kb-id: project-governance
info-type: project-roadmap
primary-topic: Detailed sequential instructions for genuinely completing Phase B of the refactoring project.
related-standards: ['project-roadmap-completion-phases-a-f', 'project-report-phase-b-analysis']
version: '1.0.0'
date-created: '2025-05-31T00:00:00Z'
date-modified: '2025-05-31T09:33:00Z'
primary_domain: PROJECT
sub_domain: PLANNING
scope_application: Specific guidance for Phase B completion activities.
criticality: p0-critical
lifecycle_gatekeeper: N/A
impact_areas: [phase-management, tool-productionization, data-validation]
change_log_url: N/A
---

## Detailed Sequential Instructions for Phase B Completion

**Overall Goal:** To genuinely complete Phase B by ensuring all tools are production-ready, all source content passes validation with zero errors, and all Phase B exit criteria as defined in the "Refactoring Completion Roadmap" (`_temp/refactoring-completion-roadmap.md`) are met.

**Preparatory Step: Familiarization (For the implementer)**

- **Action:** Before starting, review the "Refactoring Completion Roadmap" (`_temp/refactoring-completion-roadmap.md`) to understand the precise goals and exit criteria for Phase B.
- **Action:** Review the "Standard: Frontmatter Schema Definition" (`master-knowledge-base/standards/src/MT-SCHEMA-FRONTMATTER.md`) as this is the primary standard against which content and tools are validated.
- **Action:** Review the "Internal Linking Syntax Standard" (`master-knowledge-base/standards/src/SF-LINKS-INTERNAL-SYNTAX.md`) for rules regarding internal links.

---

### **Step 1: Establish a Definitive Error Baseline**

**Purpose:** To get an accurate, current understanding of all issues using the latest tool configurations and repository state. This will be the ground truth for subsequent fixes.

Instruction 1.1: Verify and Update Key Registry Files

* Action: Ensure registry files used by the linter are accurate and complete.

* File(s)/Folder(s) Involved:

* master-knowledge-base/standards/registry/subdomain_registry.yaml: Verify it contains all valid sub_domain codes for each primary_domain, particularly AS/SCHEMA and UA/SCHEMAS which were noted as updated in commit_message_phase_b.txt.

* master-knowledge-base/standards/registry/criticality_levels.txt: Ensure values are lowercase (e.g., p0-critical) as this is used for validating criticality/* tags. This was claimed to be updated in commit_message_phase_b.txt.

* master-knowledge-base/standards/registry/criticality_levels.yaml: Ensure this defines the mixed-case values (e.g., P0-Critical) for the criticality: frontmatter field.

* master-knowledge-base/standards/registry/info_types.txt: Confirm all necessary info-types are present (e.g., changelog was added as per progress.md).

* Other registry files as listed in kb_linter.py's LinterConfig: domain_codes.yaml, lifecycle_gatekeepers.txt, tag_categories.txt.

* Guidance for Understanding: These files in /master-knowledge-base/standards/registry/ define the allowed values (controlled vocabularies) for many frontmatter fields. The linter (kb_linter.py) loads these to validate document metadata. Accuracy here is crucial for correct linting.

* Expected Outcome: All registry files are confirmed to be correct and up-to-date.

Instruction 1.2: Generate a Fresh Standards Index

* Action: Run the indexer script to create an up-to-date standards_index.json.

* File(s)/Folder(s) Involved:

* Indexer Script: master-knowledge-base/tools/indexer/generate_index.py

* Output Index: master-knowledge-base/dist/standards_index.json

* Source Directories: master-knowledge-base/standards/src/, master-knowledge-base/standards/registry/, master-knowledge-base/ (for root files like AS-INDEX-KB-MASTER.md).

* Command Example (run from repository root):

python master-knowledge-base/tools/indexer/generate_index.py --repo-base . --src-dirs master-knowledge-base/standards/src master-knowledge-base/standards/registry master-knowledge-base --output-dir master-knowledge-base/dist

* Guidance for Understanding: The generate_index.py script scans specified source directories, extracts metadata from Markdown files, and creates standards_index.json. This index is used by the linter to validate internal links ([[STANDARD_ID]]). The --src-dirs argument allows specifying multiple locations.

* Expected Outcome: A new standards_index.json is generated without errors and is schema-valid. Note any files the indexer reports as skipped and why.

Instruction 1.3: Perform a Canonical Linter Run

* Action: Run the linter script with its current configuration on all relevant content to get a definitive list of current errors and warnings.

* File(s)/Folder(s) Involved:

* Linter Script: master-knowledge-base/tools/linter/kb_linter.py

* Target Directories: Typically master-knowledge-base/standards/src/ and other relevant source areas like master-knowledge-base/standards/registry/ and root-level standard documents.

* Output Report: e.g., master-knowledge-base/linter_report_current_baseline.md

* Command Example (run from repository root):

python master-knowledge-base/tools/linter/kb_linter.py --repo-base . --directory master-knowledge-base/standards/src --output master-knowledge-base/linter_report_current_baseline.md --fail-on-errors

(Consider linting other directories like registry separately if needed, or enhance linter to accept multiple target dirs).

* Guidance for Understanding: kb_linter.py validates files against defined standards. Ensure it's using the freshly generated index from Instruction 1.2 and the verified registries from Instruction 1.1. The --repo-base . tells the linter where to find its configuration and related files (like the index in dist/ and registries).

* Expected Outcome: A new, comprehensive linter report (linter_report_current_baseline.md) is generated. This report will serve as the checklist for subsequent data correction tasks.

---

### **Step 2: Critical Tooling Enhancements & Corrections**

**Purpose:** To bring `kb_linter.py`, `generate_index.py`, and utility scripts to "production-ready" status by addressing verified deficiencies.

Instruction 2.A: Enhance Linter (kb_linter.py)

* File(s) Involved: master-knowledge-base/tools/linter/kb_linter.py, relevant standards documents (e.g., MT-SCHEMA-FRONTMATTER.md), registry files.

* Sub-Instruction 2.A.1: Implement Unit Tests (Roadmap Task B.1.4)

* Action: Develop a suite of unit tests covering critical linting functions (e.g., standard_id validation, date format checks, vocabulary lookups, key order logic, link parsing, file hygiene checks). Use a standard Python testing framework (e.g., unittest or pytest).

* Guidance: The linter's README explicitly notes this as an ongoing Phase B task. Tests should cover both valid and invalid inputs.

* Expected Outcome: A functional test suite ensuring linter reliability and correctness.

* Sub-Instruction 2.A.2: Finalize Vocabulary Loading (Roadmap Task B.1.1)

* Action: Address the TODO in kb_linter.py regarding "Dynamic Vocabulary Loading Strategy from Markdown" (e.g., for MT-REGISTRY-TAG-GLOSSARY.md). Decide if this is strictly necessary or if all vocabularies can/should reside in easily parsable .txt/.yaml files in the registry. If Markdown parsing is kept, ensure it's robust.

* Guidance: Currently, the linter primarily loads from .txt and .yaml registry files. The MT-SCHEMA-FRONTMATTER.md lists some vocabularies (like for info-type) directly. Ensure consistency in how these are sourced and loaded.

* Expected Outcome: All controlled vocabularies specified in standards are reliably loaded and used by the linter.

* Sub-Instruction 2.A.3: Verify sub_domain Validation Logic

* Action: Review and test the linter's code section that validates sub_domain based on primary_domain against the subdomain_registry.yaml structure.

* Guidance: subdomain_registry.yaml defines subdomains as a list of dictionaries under each primary domain key. The linter code needs to iterate this list correctly. Discrepancies were noted between linter_final_check.md and the registry.

* Expected Outcome: Linter correctly validates sub_domain entries, matching the structure and content of subdomain_registry.yaml.

* Sub-Instruction 2.A.4: Implement Correct criticality Field vs. Tag Validation

* Action: Modify the linter to validate the criticality: frontmatter field against the mixed-case values in master-knowledge-base/standards/registry/criticality_levels.yaml.

* Action: Ensure it continues to validate criticality/* tags within the tags: list against the lowercase values in master-knowledge-base/standards/registry/criticality_levels.txt.

* Guidance: MT-SCHEMA-FRONTMATTER.md is the source of truth. The distinction between field value and tag format needs to be clear in the linter.

* Expected Outcome: Linter accurately validates both the criticality field and criticality/* tags according to their respective defined vocabularies and casing rules.

* Sub-Instruction 2.A.5: Ensure Accurate change_log_url Validation for Changelogs

* Action: Add a specific check: if info-type: changelog, then the change_log_url field MUST be ./SELF_FILENAME.MD (where SELF_FILENAME.MD is the name of the changelog file itself).

* Guidance: This ensures changelogs correctly point to themselves as per best practice.

* Expected Outcome: Linter enforces self-referential change_log_url for changelog documents.

* Sub-Instruction 2.A.6: Refine Key Order Logic and Reporting (Roadmap Task B.1.1, B.1.3)

* Action: Ensure the linter strictly uses the DEFINED_KEY_ORDER from kb_linter.py (which should match MT-SCHEMA-FRONTMATTER.md) as the single source of truth for all document types, including changelogs, unless a separate explicit order for changelogs is defined and justified.

* Guidance: Key order warnings were prevalent in commit_message_phase_b.txt.

* Expected Outcome: Key order validation is consistent and accurate.

Instruction 2.B: Enhance Indexer (generate_index.py)

* File(s) Involved: master-knowledge-base/tools/indexer/generate_index.py, master-knowledge-base/tools/indexer/standards_index.schema.json.

* Sub-Instruction 2.B.1: Implement Unit Tests (Roadmap Task B.2.5)

* Action: Develop a suite of unit tests for metadata extraction, status derivation from tags, and schema compliance logic.

* Guidance: The indexer's README notes this as an ongoing Phase B task.

* Expected Outcome: A functional test suite ensuring indexer reliability.

* Sub-Instruction 2.B.2: Implement Duplicate Entry Prevention/Warning

* Action: Modify the script to ensure each unique filepath results in only one entry. If multiple files are found claiming the same standard_id, the indexer should log this as a critical issue (as this should be caught by the linter eventually) and decide on a consistent handling strategy (e.g., index the first encountered, skip subsequent, or halt with an error).

* Guidance: Report 2 highlighted potential issues with duplicate entries. The current script iterates and appends; explicit checks are needed.

* Expected Outcome: standards_index.json is free from duplicate entries for the same file path, and standard_id collisions are flagged.

* Sub-Instruction 2.B.3: Remove or Conditionalize Excessive Debug Output

* Action: Review the "DEBUG: ..." print statements in generate_index.py. Convert them to use the logging module or make them conditional (e.g., active only with a --verbose flag).

* Guidance: Production-ready tools should not have verbose debug printing by default.

* Expected Outcome: Cleaner console output during normal operation.

Instruction 2.C: Review and Refine Utility Scripts

* File(s) Involved: Scripts in master-knowledge-base/tools/ such as populate_changelog_fm.py, refactor_ids_filenames.py, refactor_criticality_field.py.

* Sub-Instruction 2.C.1: Correct refactor_criticality_field.py Logic

* Action: Modify refactor_criticality_field.py. It currently lowercases the criticality: field value. This should be changed to ensure the field value matches the mixed-case values defined in master-knowledge-base/standards/registry/criticality_levels.yaml (e.g., P0-Critical). The refactor_tag_casing.py correctly handles the lowercase criticality/* tags.

* Guidance: This addresses the ambiguity identified in the "super-super report" regarding criticality field vs. tag casing.

* Expected Outcome: criticality: field values in frontmatter will be mixed-case, aligning with criticality_levels.yaml.

* Sub-Instruction 2.C.2: Perfect Key Order in populate_changelog_fm.py

* Action: Investigate why populate_changelog_fm.py, despite using CHANGELOG_KEY_ORDER (which is identical to DEFINED_KEY_ORDER in the linter), results in key order warnings. Refine its ruamel.yaml dumping logic to ensure strict adherence to the specified key order. Ensure change_log_url is set to ./SELF_FILENAME.MD.

* Guidance: The commit_message_phase_b.txt highlights this as the main source of remaining warnings.

* Expected Outcome: Changelog files generated/updated by this script pass linter key order checks.

* Sub-Instruction 2.C.3: Ensure Robustness of refactor_ids_filenames.py

* Action: Verify that refactor_ids_filenames.py correctly handles the -CHANGELOG suffix (all uppercase) for both standard_id and filename, and is robust for case-only renames on case-insensitive systems (e.g., by renaming to a temporary name first if only case changes).

* Expected Outcome: All standard_ids and corresponding filenames are consistently cased and formatted.

---

### **Step 3: Data Quality and Standards Adherence - Iterative Correction**

**Purpose:** To systematically fix all remaining errors and warnings in the content using the enhanced tools.

Instruction 3.1: Correct Critical Path-Based Link Errors

* Action: Manually edit the specified guide files to correct the 3 path-based link errors identified in commit_message_phase_b.txt. Links to non-standard project documents (e.g., CONTRIBUTOR_GUIDE.md, Refactor Roadmap.md) must use standard Markdown relative link syntax: [Link Text](path/to/file.md). Any malformed [[[[...]]]] links must be fixed.

* File(s) Involved:

* master-knowledge-base/standards/src/GM-GUIDE-KB-USAGE.md

* master-knowledge-base/standards/src/GM-GUIDE-STANDARDS-BY-TASK.md

* Verify the link in master-knowledge-base/standards/src/AS-STRUCTURE-TEMPLATES-DIRECTORY.md to tpl-canonical-frontmatter.md is [[TPL-CANONICAL-FRONTMATTER]] or a valid relative link if it's not a standard.

* Remove/correct invalid backup link in master-knowledge-base/standards/src/OM-AUTOMATION-LLM-IO-SCHEMAS.md.

* Guidance: Phase B requires path-based links to be errors. SF-LINKS-INTERNAL-SYNTAX.md defines the rules.

* Expected Outcome: These specific, known critical link errors are resolved.

Instruction 3.2: Iteratively Fix Remaining Issues from New Baseline Linter Report

* Action: Using the linter_report_current_baseline.md (from Instruction 1.3) and the enhanced tools (from Step 2), systematically address all remaining identified errors and then warnings.

* Guidance & Priorities:

1. Changelog Frontmatter: If the new baseline report still shows changelogs missing frontmatter or having incorrectly formatted standard_ids, re-run the now-corrected populate_changelog_fm.py (with --force if necessary and after dry-run verification) and refactor_ids_filenames.py.

2. standard_id and Filename Mismatches/Casing: Re-run the corrected refactor_ids_filenames.py if needed.

3. criticality Field Values: Re-run the corrected refactor_criticality_field.py to ensure mixed-case values.

4. Key Order Warnings: These should be largely resolved by the fixes to populate_changelog_fm.py. Manually correct any persistent, isolated instances in other files if necessary, adhering to DEFINED_KEY_ORDER in MT-SCHEMA-FRONTMATTER.md.

5. Broken [[STANDARD_ID]] Links: Investigate each. This could be due to:

* Typos in the link.

* The target document not having a standard_id or not being indexed (check indexer skip list).

* The target document's standard_id being incorrect.

Correct the link or the target document's metadata.

6. Other Specific Errors/Warnings: Address based on the linter message, referring to relevant standards documents.

* Process:

1. Make a set of fixes.

2. Re-run generate_index.py.

3. Re-run kb_linter.py.

4. Review the new report. Repeat until all errors are gone and warnings are minimized/understood.

* Expected Outcome: Linter reports zero errors. Warnings are significantly reduced, and any remaining are understood and explicitly accepted if not fixable or deferred.

---

### **Step 4: Final Phase B Verification**

**Purpose:** To formally confirm that all Phase B exit criteria are met.

Instruction 4.1: Confirm Zero Linter Errors

* Action: Perform a final linter run on all source Markdown files within /master-knowledge-base/standards/src/ and other key areas (registry, root standards).

* File(s)/Folder(s) Involved: All relevant source content.

* Expected Outcome: The linter report shows zero errors. This is a critical exit criterion.

Instruction 4.2: Confirm Complete and Valid Index

* Action: Perform a final run of generate_index.py.

* File(s)/Folder(s) Involved: Output master-knowledge-base/dist/standards_index.json.

* Expected Outcome: The standards_index.json is generated, is schema-valid, contains no unintended duplicates, and accurately reflects all intended documents from /master-knowledge-base/ structure.

Instruction 4.3: Verify Tool Readiness

* Action: Confirm linter and indexer have completed unit tests, and their READMEs accurately reflect their production-ready state and CLI usage.

* File(s)/Folder(s) Involved:

* master-knowledge-base/tools/linter/kb_linter.py and its tests.

* master-knowledge-base/tools/linter/README.md.

* master-knowledge-base/tools/indexer/generate_index.py and its tests.

* master-knowledge-base/tools/indexer/README.md.

* Expected Outcome: Tools meet the "production-ready, tested, and documented" criteria.

Instruction 4.4: Update Progress Documentation

* Action: Update progress.md and commit_message_phase_b.txt (or create a new commit message) to accurately reflect the true completion status of Phase B, including final error/warning counts (target: 0 errors). This will be the "script run report."

* Expected Outcome: Clear, accurate documentation of Phase B completion.

---

### **Step 5: Prepare for Phase C**

**Purpose:** To ensure a smooth transition into Phase C by setting up foundational elements that were part of Phase B or are immediate next steps.

Instruction 5.1: Implement Functional CI/CD Checks (Anticipating Phase C Task C.4)

* Action: Modify the GitHub Actions workflow file (.github/workflows/standards_check.yml) to:

1. Uncomment or add steps to actually execute kb_linter.py and generate_index.py.

2. Ensure the workflow uses the correct paths for the scripts and target directories within the /master-knowledge-base/ context.

3. Configure the workflow to fail if kb_linter.py exits with an error status (i.e., if linter errors are found). This aligns with Phase C Task C.4.2.

* Guidance: The current CI file has these steps commented out. Implementing this now, even if perfected in Phase C, helps protect the "perfect slate."

* Expected Outcome: A basic but functional CI pipeline that runs the linter and indexer and fails on linter errors, providing continuous validation.

Instruction 5.2: Draft Scripting Standards Document (Long-Term Improvement)

* Action: Create an initial draft of GM-STANDARDS-SCRIPTING-GUIDELINES.md (new file, e.g., in master-knowledge-base/standards/src/).

* Content Points (as per Report 2):

* Naming Conventions (Python: snake_case.py).

* Error Handling & Exit Codes.

* Logging (Python logging module, levels, key actions, changes, summaries).

* Argument Parsing (argparse, mandatory --dry-run, --verbose).

* Modularity, Comments, Docstrings.

* Dependency Management.

* Mandatory log review and manual spot-checking after script runs.

* Guidance: This document will formalize best practices for all current and future scripts in the project, improving reliability and maintainability.

* Expected Outcome: A draft document outlining scripting standards for the project.

---

By meticulously following these sequential instructions, all known shortcomings from Phase B will be addressed, tools will be genuinely production-ready and tested, data quality will be high, and the project will have a verified "perfect slate" to confidently proceed to Phase C.