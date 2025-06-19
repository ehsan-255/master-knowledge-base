---
title: Immediate Remediation Requirements - Investigation & Revised Plan
document_type: execution-plan
date_created: '2025-06-19T00:00:00Z'
author: AI Assistant
scope: Analysis of remediation tasks from comprehensive-standards-analysis-final-20250618-2300.md
status: final
---

# Immediate Remediation Requirements: Investigation & Revised Plan

This document provides a precise, instructional plan for addressing the five critical issues identified in the standards ecosystem. This plan is the output of a deep investigation and supersedes the initial recommendations with fact-based, executable steps.

---

## 1. Invalid References to Obsolete Collection Documents

**A. Analysis Summary:**
The investigation confirms that the two "missing" collection documents (`COL-GOVERNANCE-UNIVERSAL.md` and `COL-LINKING-UNIVERSAL.md`) are not missing but are intentionally **deprecated and archived**. A new, automated system (`tools/builder/generate_collections.py`) now creates dynamic collections. The true issue is that **12 active standards contain invalid references** to rule sets within these obsolete files.

**B. Instructional Plan:**

1.  **Identify Invalid References:**
    *   Execute a `grep` search across the `standards/src/` directory for the strings `COL-GOVERNANCE-UNIVERSAL.md` and `COL-LINKING-UNIVERSAL.md` to confirm the 12 affected files.

2.  **Map Old Rules to New Standards:**
    *   For each of the 12 files, perform a detailed analysis of the broken reference (e.g., `...rules 1.1 through 1.3... from COL-GOVERNANCE-UNIVERSAL.md`).
    *   Manually trace the history of that rule set to identify the corresponding new, atomic standard(s) that now contain this logic.
    *   Create a mapping table: `[Obsolete Rule ID] -> [New Standard ID(s)]`.

3.  **Correct the References:**
    *   Develop a script to iterate through the 12 affected files.
    *   For each file, replace the sentence containing the invalid reference with a corrected sentence that points to the new, appropriate standard(s) based on the mapping from the previous step.

---

## 2. System-Wide Changelog Removal

**A. Analysis Summary:**
The user has mandated the complete removal of all changelog-related artifacts from the standards documents, not just the replacement of placeholders. This affects 71 files containing the `change_log_url` key in their frontmatter.

**B. Instructional Plan:**

1.  **Develop Removal Script:**
    *   Create a script that iterates through all `.md` files in the `standards/src/` directory.
    *   The script must parse the YAML frontmatter of each file.
    *   If the key `change_log_url` exists, the script will remove the entire line containing the key-value pair.
    *   The script will save the modified file.

2.  **Execute and Verify:**
    *   Perform a dry run, logging all files that would be modified.
    *   Execute the script.
    *   Perform a verification `grep` search for `change_log_url:` to ensure no instances remain.

---

## 3. Promotion of Critical Standards from 'Draft' to 'Active'

**A. Analysis Summary:**
Investigation of a sample draft file (`AS-KB-DIRECTORY-STRUCTURE.md`) confirms that documents are in "draft" status due to legitimate incompleteness, including placeholder values, broken links, and sections explicitly marked for expansion. A comprehensive, expert review is mandatory before promotion.

**B. Instructional Plan:**

1.  **Establish Formal Review Checklist:**
    *   Finalize and document a mandatory "Expert Review Checklist" to be applied to each of the 40 draft standards. The checklist must include, at a minimum:
        *   **Completeness:** No placeholder text (e.g., `[MISSING_...]`, `(To Be Expanded)`).
        *   **Link Integrity:** All internal links resolve to an existing, active standard.
        *   **Reference Validity:** No references to deprecated or archived documents.
        *   **Syntactic Correctness:** Document passes all `kb_linter.py` checks.
        *   **Terminological Consistency:** All technical terms align with a master glossary.
        *   **Logical Soundness:** The rules defined are unambiguous and do not conflict with other active standards.

2.  **Execute Review & Remediation:**
    *   Create a tracking sheet listing all 40 draft standards.
    *   For each standard, perform the review and document all findings against the checklist.
    *   Create a work item to remediate every failed checklist item for each document. This is a prerequisite for promotion.

3.  **Promote Remediated Standards:**
    *   Once a standard passes 100% of the checklist items, create a final pull request to change its frontmatter status from `status/draft` to `status/active`.

---

## 4. Synchronization of Architectural Counts and Navigation

**A. Analysis Summary:**
The investigation confirms that the architectural documents (`AS-MAP-STANDARDS-KB.md` and `AS-ROOT-STANDARDS-KB.md`) are out of sync because the **tooling to update them does not exist**. The `tools/indexer/generate_index.py` script creates the necessary data (`master-index.jsonld`), but no process consumes this data to update the logical and presentation layer documents.

**B. Instructional Plan:**

1.  **Develop Architectural Synchronizer Script:**
    *   Create a new script, e.g., `tools/builder/update_architecture_docs.py`.
    *   **Input:** The script will take `dist/master-index.jsonld` as input.
    *   **Logic (AS-MAP-STANDARDS-KB.md):**
        *   Parse the index and group all documents by their `primary_domain`.
        *   Calculate the count of active standards for each domain.
        *   Read `standards/src/AS-MAP-STANDARDS-KB.md`, locate the `standard_count` fields, and update their values with the correct counts.
    *   **Logic (AS-ROOT-STANDARDS-KB.md):**
        *   For each domain, generate a markdown list of links to the active standards within that domain.
        *   Read `standards/src/AS-ROOT-STANDARDS-KB.md`, locate the navigation sections for each domain, and replace the placeholder content (or stale list) with the newly generated list.
    *   **Output:** The script will overwrite the two architectural files with the updated content.

2.  **Integrate into Workflow:**
    *   Incorporate the execution of this new script into the main build/CI process, ensuring it runs immediately after `generate_index.py` completes.

---

## 5. Correction of Tagging and Taxonomy

**A. Analysis Summary:**
A review based on the project's foundational principles of layered architecture confirms the original analysis is **correct**. The `AS-ROOT-STANDARDS-KB.md` (Presentation Layer) should not be tagged as a `standard-definition`. Furthermore, mixing `CONCEPT-*` documents with normative standards in the primary navigation violates the principle of taxonomic separation.

**B. Instructional Plan:**

1.  **Correct Document Tagging:**
    *   Manually edit `standards/src/AS-ROOT-STANDARDS-KB.md`.
    *   Remove the tag `content-type/standard-definition` from its frontmatter.

2.  **Update Synchronizer Logic for Taxonomy:**
    *   In the new `update_architecture_docs.py` script (from item #4), add logic to handle concept documents separately.
    *   When generating navigation for `AS-ROOT-STANDARDS-KB.md`, the script must differentiate between standards and concepts based on the `standard_id` prefix (e.g., `CONCEPT-*`).
    *   The script should place `CONCEPT-*` documents in a distinct `### Foundational Concepts` section, separate from the domain-specific standards lists, to ensure clear separation. 