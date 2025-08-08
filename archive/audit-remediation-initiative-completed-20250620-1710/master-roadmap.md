---
title: 'Master Roadmap: Audit Remediation Initiative'
standard_id: ARI-MASTER-ROADMAP
aliases: [audit-remediation-roadmap]
tags:
- content-type/project-documentation
- criticality/p1-high
- kb-id/audit-remediation-initiative
- status/active
- topic/governance
- topic/remediation
kb-id: audit-remediation-initiative
info-type: roadmap
primary-topic: 'The sequential execution plan for the Audit Remediation Initiative, detailing the five core phases of work.'
related-standards: ['ARI-MASTER-ANALYSIS']
version: 1.0.0
date-created: '2025-06-19T00:00:00Z'
date-modified: '2025-06-19T00:00:00Z'
primary_domain: GOVERNANCE
sub_domain: REMEDIATION
scope_application: 'Repository-wide standards and architectural documents'
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas: ['standards', 'architecture', 'automation']
---
# MASTER ROADMAP - AUDIT REMEDIATION INITIATIVE

## **EXECUTIVE SUMMARY**
This roadmap defines the mandatory execution sequence for the Audit Remediation Initiative. It is derived from the `master-analysis-report.md` and breaks the project into five distinct, sequential phases (P1-P5). Each phase represents a major workstream aimed at resolving a specific issue identified during the audit process. The successful completion of these phases in the specified order is critical to restoring the integrity of the standards repository.

---

## **P1: CORRECT INVALID REFERENCES IN ACTIVE STANDARDS**
- **Objective**: To find and replace all references to obsolete collection documents (`COL-GOVERNANCE-UNIVERSAL.md`, `COL-LINKING-UNIVERSAL.md`) within the 12 affected standards files.
- **Decomposition**:
    - **P1.1**: Develop a script to perform a `grep` search to precisely identify the 12 files and the lines containing the invalid references.
    - **P1.2**: Manually perform a historical analysis to map the old, deprecated rules to their new, atomic standard counterparts. This mapping must be documented in a temporary file.
    - **P1.3**: Develop and execute a Python script that reads the mapping and replaces the invalid reference sentences in the 12 files with corrected text pointing to the new standards.
- **Exit Criteria**:
    - All 12 files are updated.
    - A `grep` search for the obsolete filenames returns zero results in `standards/src/`.
    - A commit is made containing the 12 corrected files.

---

## **P2: SYSTEM-WIDE REMOVAL OF CHANGELOG METADATA**
- **Objective**: To completely remove the `change_log_url` key from the frontmatter of all 68 standards documents where it exists.
- **Decomposition**:
    - **P2.1**: Develop a Python script that can iterate through all `.md` files in `standards/src/`, parse their YAML frontmatter, and remove the line containing `change_log_url:` if it exists.
    - **P2.2**: Perform a dry run of the script, logging all files that will be modified to a report in `tools/reports/`.
    - **P2.3**: Execute the script to perform the file modifications.
- **Exit Criteria**:
    - All 68 files are updated.
    - A `grep` search for `change_log_url:` returns zero results in `standards/src/`.
    - A commit is made containing the 68 corrected files.

---

## **P3: ESTABLISH AND EXECUTE DRAFT PROMOTION PROCESS**
- **Objective**: To create and implement a formal, quality-gated process for reviewing and promoting the 55 standards currently in `draft` status.
- **Decomposition**:
    - **P3.1**: Formalize the "Expert Review Checklist" in a new standard document (`SA-PROCESS-DRAFT-REVIEW`). The checklist must include checks for completeness, link integrity, reference validity, linter compliance, and logical soundness.
    - **P3.2**: Create a master tracking sheet (e.g., a CSV or Markdown table in the project directory) listing all 55 draft files.
    - **P3.3**: Begin the review process for each standard. This is a significant manual effort and will be broken down into sub-tasks for each domain. This roadmap only tracks the setup of the process; the execution will be managed via the `master-progress.md` file.
- **Exit Criteria**:
    - The `SA-PROCESS-DRAFT-REVIEW` standard is created and marked as active.
    - The tracking sheet is created and populated with the 55 files.
    - A plan for tackling the review is documented in `master-progress.md`.

---

## **P4: DEVELOP ARCHITECTURAL SYNCHRONIZATION TOOL**
- **Objective**: To create a new script that automates the updating of the primary architectural documents (`AS-MAP-STANDARDS-KB.md` and `AS-ROOT-STANDARDS-KB.md`).
- **Decomposition**:
    - **P4.1**: Create the new script file: `tools/builder/update_architecture_docs.py`.
    - **P4.2**: Implement logic to read and parse the **correct** master index file path: `standards/registry/master-index.jsonld`.
    - **P4.3**: Implement logic to calculate standard counts by domain and update the `standard_count` fields in `AS-MAP-STANDARDS-KB.md`.
    - **P4.4**: Implement logic to generate markdown navigation link lists and replace the stale lists in `AS-ROOT-STANDARDS-KB.md`.
- **Exit Criteria**:
    - The script is created and successfully runs without errors.
    - The script correctly updates the two architectural documents based on the current index file.
    - The script is integrated into the main build process to run after the indexer.

---

## **P5: CORRECT DOCUMENT TAGGING AND TAXONOMY**
- **Objective**: To align document metadata and navigation with the established architectural principles.
- **Decomposition**:
    - **P5.1**: Manually edit `standards/src/AS-ROOT-STANDARDS-KB.md` to remove the `content-type/standard-definition` tag from its frontmatter.
    - **P5.2**: **(Dependency on P4)** Enhance the `update_architecture_docs.py` script. Add logic to differentiate between standards and `CONCEPT-*` documents when generating navigation for `AS-ROOT-STANDARDS-KB.md`. The script must place concepts under a separate `### Foundational Concepts` heading.
- **Exit Criteria**:
    - The tag is removed from `AS-ROOT-STANDARDS-KB.md`.
    - The new script correctly generates a separate navigation section for concepts.
    - A final commit is made with the updated script and the manually corrected file. 