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
## Definitive Sequential Instructions for Project File Organization and Archival

**Overall Strategy:**

- **Active Project Documents:** Documents that are "live" (including high-level roadmaps, designs, and active guidelines, even if not frequently edited) will be moved from `_temp/` or the root directory into a new top-level active-project/ structure (e.g., active-project/project-planning/, active-project/project-governance/, active-project/project-design/, active-project/project-guidelines/).
    - **Naming:** These files will use descriptive kebab-case.md names.
    - **Frontmatter:** They **MUST** receive complete YAML frontmatter according to the schema in mt-schema-frontmatter.md. Fields not directly applicable (e.g., standard_id in the formal sense, primary_domain if not a standard) should use "N/A" or a project-specific convention (details below). New info-type values will be proposed.
- **Archived Files:** Files that are truly superseded, temporary, or historical notes will be moved to a top-level archive/ directory, further organized by date and category.
    - **Naming:** Archived files will be named archived-original-descriptive-name-20250531.md (using kebab-case for the original/descriptive part).
    - **Frontmatter:** Archived files do _not_ require new full frontmatter.
- **Link Integrity:** Links within archived documents will not be updated. The /archive/ path should be excluded from link-checking processes.

---

### **Section 0: Preparation - Create New Directory Structures**

Instruction 0.1: Create Core Project Documentation and Archive Directories

* Action: At the root of the repository, create the following new top-level directories if they do not already exist:

* active-project/
* active-project/project-planning/
* active-project/project-governance/
* active-project/project-design/
* active-project/project-guidelines/
* active-project/project-reports/
* archive/

* Rationale: Establishes the standardized locations for active project documentation and archived materials.

---

### **Section 1: Managing Progress Records and Working Notes**

**Goal:** Consolidate progress tracking into the root progress.md and archive redundant notes after extracting essential information.

Instruction 1.1: Maintain and Structure the Authoritative progress.md

* File(s): progress.md (at repository root)

* Action: This file remains at the repository root. Ensure its content is structured as you've defined:

1. Top Section: High-level summary of the overall project/goal/progress.
2. Middle Section: Summary of near-past progress.
3. Main Section: Detailed descriptions of the current progress.

* Frontmatter: Add complete frontmatter to this progress.md file.

* Example Frontmatter:

yaml
---
title: Project Refactoring Progress Report
standard_id: project-progress-master
aliases: [Refactoring Progress, KB Progress Tracker]
tags: [status/active, info-type/project-report, topic/project-management]
kb-id: project-governance
info-type: project-report
primary-topic: Live tracking document for the knowledge base refactoring project.
related-standards: ['gm-roadmap-refactoring-completion-v1']
version: '1.0.0'
date-created: 'YYYY-MM-DDTHH:MM:SSZ'
date-modified: '20250531THH:MM:SSZ'
primary_domain: PROJECT
sub_domain: MANAGEMENT
scope_application: Internal project tracking for the refactoring effort.
criticality: p1-high
lifecycle_gatekeeper: N/A
impact_areas: [project-visibility, planning]
change_log_url: N/A
---

* Rationale: Provides a clear, layered view of project progress for all stakeholders, with standardized metadata.

Instruction 1.2: Consolidate and Archive Other Progress/Note Files

* File(s):

* commit-message-phase-b.txt (at repository root)
* temp/note.md
* temp/end-of-session-summary.md
* temp/roadmap-progress.md
* master-knowledge-base/note.md

* Actions:

1. Review each file for critical information not yet in progress.md or other formal documents. Consolidate as needed into progress.md.
2. Create the target archive directory: archive/project-notes-and-progress-20250531/
3. Move these files into the new archive directory.
4. Rename them as follows:

* archived-root-commit-message-phase-b-20250531.txt
* archived-temp-note-20250531.md
* archived-temp-end-of-session-summary-20250531.md
* archived-temp-roadmap-progress-20250531.md
* archived-mkb-note-20250531.md

* Rationale: Centralizes active progress tracking while preserving detailed historical notes.

---

### **Section 2: Managing Linter and Other Reports**

**Goal:** Archive historical point-in-time reports to reduce clutter.

Instruction 2.1: Archive Historical Linter Reports

* File(s): All historical linter report files at the repository root (e.g., linter-final-check.md, linter-report-updated.md, linter-report-final-vX.md series, linter-report-baseline.md, etc.).

* Actions:

1. Create the target archive directory: archive/old-reports-20250531/
2. Move all such historical reports into this directory.
3. Rename them for clarity, e.g., archived-linter-final-check-20250531.md.

* Rationale: Keeps the root directory clean. The linter report generated as part of completing Phase B will be the current one until it is also superseded.

---

### **Section 3: Managing Roadmaps, Designs, and Selected temp/ Working Files**

**Goal:** Relocate files from temp/ based on their current status (active roadmap, important reference, or archivable working file), ensuring they get proper naming and full frontmatter if not archived.

Instruction 3.1: Relocate "Highest-Level Live" Original Roadmap

* File(s): temp/refactor-roadmap.md

* User Assessment: Still live and unfinished, highest-level roadmap.

* Actions:

1. New Location: active-project/project-planning/project-roadmap-original-high-level.md
2. Add Complete Frontmatter:

yaml
---
title: Original High-Level Refactoring Roadmap (Phases 0-5)
standard_id: project-roadmap-original
aliases: [Original Project Roadmap, Phase 0-5 Roadmap]
tags: [status/active, info-type/project-roadmap, topic/project-planning, project-phase/legacy]
kb-id: project-governance
info-type: project-roadmap
primary-topic: The initial overall strategic plan for the knowledge base refactoring.
related-standards: ['project-roadmap-completion-phases-a-f']
version: '1.0.0'
date-created: 'YYYY-MM-DDTHH:MM:SSZ'
date-modified: '20250531THH:MM:SSZ'
primary_domain: PROJECT
sub_domain: PLANNING
scope_application: Overall guidance for the multi-year refactoring effort (historical high-level).
criticality: p1-high
lifecycle_gatekeeper: N/A
impact_areas: [project-strategy, historical-context]
change_log_url: N/A
---

* Rationale: Places this key strategic document in an accessible project documentation folder with proper metadata.

Instruction 3.2: Relocate Current "Mid-Level" Roadmap (Phases A-F)

* File(s): temp/refactoring-completion-roadmap.md

* User Assessment: Current live guiding document, mid-level roadmap.

* Actions:

1. New Location: active-project/project-planning/project-roadmap-completion-phases-a-f.md
2. Update/Add Complete Frontmatter:

yaml
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
date-created: '2025-05-30THH:MM:SSZ'
date-modified: '20250531THH:MM:SSZ'
primary_domain: PROJECT
sub_domain: PLANNING
scope_application: Detailed operational roadmap for refactoring completion.
criticality: p0-critical
lifecycle_gatekeeper: N/A
impact_areas: [project-execution, phase-management]
change_log_url: N/A
---

* Guidance: Once this current instruction report is adopted as the primary guide for immediate actions, the status of project-roadmap-completion-phases-a-f.md can be changed to status/superseded-by-instructions or status/active-reference.

* Rationale: Ensures the currently active detailed roadmap is properly located and metadata-rich.

Instruction 3.3: Relocate Key Supporting Reports and Design Documents for Reference

* File(s):

* temp/refactoring-completion-report.md
* temp/standards-categorization-scheme.md
* temp/single-source-multi-view-standards-architecture.md

* User Assessment: Not actively used but handy for reference.

* Actions:

1. New Locations & Names:

* active-project/project-reports/project-report-initial-refactoring-completion.md
* active-project/project-design/project-design-standards-categorization-scheme.md
* active-project/project-design/project-design-multi-view-architecture.md

2. Add Complete Frontmatter to each (example for report):

yaml
---
title: Initial Refactoring Completion Report Analysis
standard_id: project-report-initial-refactoring-completion
tags: [status/informational-reference, info-type/project-report, topic/project-assessment]
kb-id: project-governance
info-type: project-report
primary-topic: Analysis report that informed the Refactoring Completion Roadmap (Phases A-F).
related-standards: ['project-roadmap-completion-phases-a-f']
version: '1.0.0'
date-created: 'YYYY-MM-DDTHH:MM:SSZ'
date-modified: '20250531THH:MM:SSZ'
primary_domain: PROJECT
sub_domain: REPORTS
scope_application: Historical analysis for the refactoring project.
criticality: p2-medium
lifecycle_gatekeeper: N/A
impact_areas: [project-planning, historical-context]
change_log_url: N/A
---

* Adapt frontmatter similarly for the design documents, using info-type: project-design-document and sub_domain: DESIGN.

* Rationale: Preserves these important reference documents in an organized project documentation structure with appropriate metadata.

Instruction 3.4: Archive Other temp/ Working Files

* File(s):

* temp/refactor-prompt.md
* temp/system-prompt-structured-authoring-specialist-custom-schema-v1-4.md
* temp/project-collaboration-and-onboarding-single.md
* temp/project-collaboration-and-onboarding-guide.md

* User Assessment: To be archived.

* Actions:

1. Create the target archive directory: archive/temp-working-files-20250531/
2. Move these files into this directory.
3. Rename them:

* archived-temp-refactor-prompt-20250531.md
* archived-temp-system-prompt-v1-4-20250531.md
* archived-temp-project-collab-onboarding-single-20250531.md
* archived-temp-project-collab-onboarding-guide-20250531.md

* Rationale: Clears temp/ of superseded working drafts.

---

### **Section 4: Managing Misplaced Files**

**Goal:** Correctly relocate usable templates.

Instruction 4.1: Relocate temp/changelog-template.md as an Active Template

* File(s): temp/changelog-template.md

* User Assessment: It IS a generic, usable template.

* Actions:

1. New Location & Name: master-knowledge-base/standards/templates/tpl-changelog-document.md
2. Review and Update Content: Ensure its content (e.g., frontmatter placeholders, structure) aligns with current standards for changelog documents (see populate_changelog_fm.py for expected fields) and mt-schema-frontmatter.md.

---

### **Section 5: Managing Other Root-Level Utility/Guidance Files**

**Goal:** Relocate or archive root-level files that are not part of the core KB content structure.

Instruction 5.1: Archive todo-master-list.md

* File(s): todo-master-list.md (at repository root)

* User Assessment: To be archived as a redesign is planned.

* Actions:

1. Review for any final critical items that need migration before archival.
2. Create the target archive directory if it doesn't exist: archive/project-notes-and-progress-20250531/
3. New Location & Name: archive/project-notes-and-progress-20250531/archived-root-todo-master-list-20250531.md

* Rationale: Preserves the historical list while acknowledging it's superseded.

Instruction 5.2: Relocate Active Project Guidelines (work-ethic-guidelines.md & reminders.md)

* File(s):

* work-ethic-guidelines.md (at repository root)
* reminders.md (at repository root)

* User Assessment: To be moved to an active project documentation area like active-project/project-guidelines/.

* Actions:

1. New Locations & Names:

* active-project/project-guidelines/project-work-ethic-guidelines.md
* active-project/project-guidelines/project-reminders.md

2. Add Complete Frontmatter to each (example for work-ethic):

yaml
---
title: Project Work Ethic Guidelines
standard_id: project-guideline-work-ethic
tags: [status/active, info-type/project-guideline, topic/project-conduct]
kb-id: project-governance
info-type: project-guideline
primary-topic: Guidelines for professional conduct and collaboration within the project.
version: '1.0.0'
date-created: 'YYYY-MM-DDTHH:MM:SSZ'
date-modified: '20250531THH:MM:SSZ'
primary_domain: PROJECT
sub_domain: GUIDELINES
scope_application: All contributors to this knowledge base project.
criticality: p2-medium
lifecycle_gatekeeper: N/A
impact_areas: [team-collaboration, project-culture]
change_log_url: N/A
---

* Adapt frontmatter similarly for project-reminders.md.

* Rationale: Provides a clear, accessible, and metadata-rich location for active project-level guidance documents.

---

### **Section 6: Implement Archive README**

**Goal:** Explain the archive structure to future users.

Instruction 6.1: Create README for archive/ Directory

* Action: Create a new file: archive/readme.md

* Content:

```markdown
# Repository Archive

This directory contains historical, superseded, or temporary working files related to the Master Knowledge Base project that are no longer in active use but are retained for reference.

## Structure

Files are typically organized into subdirectories named with a `20250531` date suffix indicating when the contents were archived. Common subdirectories include:

* project-notes-and-progress-20250531/: Historical progress reports, commit message drafts, and detailed working notes.
* old-reports-20250531/: Point-in-time reports, such as linter outputs.
* temp-working-files-20250531/: Miscellaneous temporary files from previous work.
* misplaced-files-20250531/: Files that were found in incorrect locations and subsequently archived.
* (Other categories like outdated-roadmaps-and-designs-20250531/ or legacy-root-content-20250531/ may appear here as per project lifecycle phases.)

## Filename Convention for Archived Files

Archived files are typically renamed to archived-original-descriptive-name-20250531.ext to clearly mark their status and retain context.

## Link Integrity

Links within archived documents may be broken as they point to files that might have been moved, renamed, or are also archived. These links are **not** maintained. Automated link checking tools should be configured to ignore paths within this archive/ directory.
```

* **Rationale:** Provides essential clarity on the purpose and organization of archived materials.

---
