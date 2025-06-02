---
title: Project Reminders
standard_id: project-guideline-reminders
tags: [status/active, info-type/project-guideline, topic/project-management]
kb-id: project-governance
info-type: project-guideline
primary-topic: Key reminders and action items for project development and maintenance.
version: '1.0.0'
date-created: '2025-05-25T00:00:00Z'
date-modified: '2025-06-02T00:00:00Z'
primary_domain: PROJECT
sub_domain: GUIDELINES
scope_application: All contributors to this knowledge base project.
criticality: p2-medium
lifecycle_gatekeeper: N/A
impact_areas: [project-management, team-awareness]
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
    *   Development teams must implement a comprehensive naming convention framework with strict enforcement protocols across all project artifacts. The standardized nomenclature system requires kebab-case formatting as the primary convention for all deliverables, with defined exceptions for specific artifact categories.
Script-related components, including executable files, automated test suites, logging outputs, and associated documentation, must utilize snake_case formatting to maintain consistency with scripting language conventions and enhance readability within development environments.
Standard identifiers require ALL-CAPS-KEBAB-CASE formatting to ensure proper distinction and maintain compliance with identification protocols. This formatting standard applies to all metadata elements within frontmatter configurations, including but not limited to `standard_id`, `file_type`, `source_path`, and related parameter specifications.
Quality assurance procedures mandate comprehensive updates to all technical documentation, standards repositories, and knowledge base systems to reflect these naming conventions. Static analysis tools and linting utilities must be configured with strict validation rules to enforce compliance across the entire codebase and prevent deviation from established standards.
The implementation framework requires mandatory adherence to these specifications: snake_case for all scripting components and related artifacts, ALL-CAPS-KEBAB-CASE for standard identifiers, and kebab-case for all remaining project elements. Additional exceptions to this nomenclature framework require formal documentation and approval through established change management processes..
    *   It is necessary to develop and implement updated standards, guidelines, and regulatory frameworks to address the requirements associated with the recently initiated active projects (active-project/) guidelines. These measures should ensure comprehensive oversight, alignment with best practices, and effective governance throughout the project's lifecycle.
    *   It is imperative to establish and deploy revised standards, protocols, and regulatory frameworks that comprehensively address the requirements stipulated within the newly implemented records retention and archival management guidelines (archive/). These governance mechanisms must ensure rigorous oversight, adherence to established archival science best practices, and effective information governance throughout the retention scheduling triggers and the complete records lifecycle management process, from creation through final disposition.

---
## Reminder: Future `OM-AUTOMATION-LLM-PROMPT-LIBRARY` Integration (20250602)

- The standard `OM-AUTOMATION-LLM-PROMPT-LIBRARY` is planned but does not yet exist.
- When this standard is created:
    - Update `[[OM-AUTOMATION-LLM-IO-SCHEMAS]]` to correctly link to it in its `related-standards` and body content if appropriate.
- This reminder was added because a link to it was prematurely removed from `OM-AUTOMATION-LLM-IO-SCHEMAS.MD` after user feedback indicated the prompt library is not yet ready.

---
## Reminder: Missing GM-GUIDE Documents (20250602)

- The following guide documents, expected to be in `master-knowledge-base/standards/src/`, could not be found during the execution of L2-T1 Phase D.2 tasks:
    - `GM-GUIDE-KB-USAGE.MD`
    - `GM-GUIDE-STANDARDS-BY-TASK.MD`
- These files need to be located or recreated and then reviewed/updated as per Task D.2.2 of the L2-T1 roadmap.
- This reminder was added after a subtask reported them as not found during an attempt to review them.

---
## Reminder: Linter Local Test Mode Issue (20250602)

- During L2-T1 execution (Phases C, D, E), the `kb_linter.py` script consistently ran in a "local test mode" when attempting to lint specific directories or files (e.g., `master-knowledge-base/standards/src/`).
- This mode processed dummy files created by the linter itself, instead of the actual target files.
- The cause for this mode triggering or how to disable it is not documented in the linter's README.
- As a result, specific validation of newly created/modified files (like `GM-GUIDE-KB-USAGE.MD`, `GM-GUIDE-STANDARDS-BY-TASK.MD`, and their changelogs) could not be completed.
- While the CI/CD pipeline might run the linter on the entire KB successfully, targeted local linting for development and verification remains problematic.
- This issue needs further investigation to ensure the linter can be reliably used for local validation.
