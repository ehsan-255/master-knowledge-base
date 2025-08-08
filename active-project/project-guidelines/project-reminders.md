---
title: Project Reminders
standard_id: project-guideline-reminders
tags:
- content-type/project-guideline
- criticality/p2-medium
- info-type/project-guideline
- kb-id/global
- status/active
- topic/guidelines
- topic/project
- topic/project-management
kb-id: project-governance
info-type: project-guideline
primary-topic: Key reminders and action items for project development and maintenance.
version: 1.0.0
date-created: '2025-05-25T00:00:00Z'
date-modified: '2025-06-17T02:29:12Z'
primary_domain: PROJECT
sub_domain: GUIDELINES
scope_application: All contributors to this knowledge base project.
criticality: p2-medium
lifecycle_gatekeeper: N/A
impact_areas:
- project-management
- team-awareness
change_log_url: N/A
---
**Reminders:**

1.  **`CONTRIBUTOR_GUIDE.md`:** Please review/define its purpose, structure, guidelines, and final location. Update the commented-out/corrected links in `GM-GUIDE-STANDARDS-BY-TASK.md` and any other relevant documents.
2.  **`TODO-MASTER-LIST.md`:** Please review/define its purpose, structure, and guidelines for tracking major project TODOs.
3.  **`master_todo_populate.py`:** Please define its purpose (likely to scan for `[!TODO]` callouts in documents and populate `TODO-MASTER-LIST.md`), its responsibilities (how it parses, what it extracts), and usage guidelines. Consider its interaction with the linter (which could also flag TODOs).
4.  **Scripting Standards/Guidelines:** Please initiate, define, and document a new category of standards/guidelines specifically for scripting within this project. This should cover aspects like:
    *   Script naming conventions.
    *   Required error handling and exit codes.
    *   Comprehensive logging practices.
    *   Argument parsing conventions.
    *   Dependency management (e.g., use of `requirements.txt`, conda environments).
    *   Code style and commenting.
5.  **Logging & Review Mandate for Scripts:** Please add to the new scripting guidelines (and any relevant process documentation) that every team member MUST:
    *   Implement comprehensive logging in every script created or modified.
    *   Ensure logs capture key decisions, actions taken, files processed, and any errors or warnings encountered.
    *   Fully review logs immediately after each script run to verify expected behavior.
    *   Manually review a significant percentage of affected files (e.g., 50% or a sample based on risk/impact) to ensure the accuracy of the script and the correctness of the changes reflected in the logs.
6.  **General Standards/Guidelines:** Please edit and document existing standards/guidelines or generate a new category of standards/guidelines to cover the following aspects:
    *   **Naming Convention Standards:** Review existing naming convention standards and update as needed to ensure comprehensive coverage across all project artifacts.
    *   It is necessary to develop and implement updated standards, guidelines, and regulatory frameworks to address the requirements associated with active projects (active-project/) guidelines. 
    *   It is imperative to establish and deploy revised standards, protocols, and regulatory frameworks that comprehensively address the requirements stipulated within the records retention and archival management guidelines (archive/). 

---
## Reminder: Future `OM-AUTOMATION-LLM-PROMPT-LIBRARY` Integration (20250602)

- The standard `OM-AUTOMATION-LLM-PROMPT-LIBRARY` is planned but does not yet exist.
- When this standard is created:
    - Update `[[OM-AUTOMATION-LLM-IO-SCHEMAS]]` to correctly link to it in its `related-standards` and body content if appropriate.
- This reminder was added because a link to it was prematurely removed from `OM-AUTOMATION-LLM-IO-SCHEMAS.MD` after user feedback indicated the prompt library is not yet ready.

---
## Reminder: Populate Placeholder GM-GUIDE Documents (20250602)

- The following guide documents were recreated as placeholders in `standards/src/` during L2-T1 Phase C/D remediation (Agent Jules, 2025-06-02):
    - `GM-GUIDE-KB-USAGE.MD` (and its changelog `GM-GUIDE-KB-USAGE-CHANGELOG.MD`)
    - `GM-GUIDE-STANDARDS-BY-TASK.MD` (and its changelog `GM-GUIDE-STANDARDS-BY-TASK-CHANGELOG.MD`)
- These files currently contain only placeholder content and frontmatter. They need to be populated with actual content as per their intended scope.
- Their `status` tag is `status/draft`.

---
