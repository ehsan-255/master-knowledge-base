---
title: Master Analysis Report - Active Project Organization Initiative
id: -apo-initiative-master-analysis-report
kb: active-project-organization-initiative
file_type: master_analysis_report
source_path: active-project/-active-project-organization-initiative-active/master-analysis-report.md
description: Core document defining the structure, workflow, and standards for active
  projects. Originally active-project-organization.md.
status: active
linked_documents:
- master-roadmap.md
- master-progress.md
standard_id: -apo-initiative-master-analysis-report
aliases:
- APO Analysis
- Project Org Standards
tags:
- content-type/policy-document
- criticality/p1-high
- kb-id/global
- status/active
- topic/gm
- topic/project_mgmt
kb-id: active-project-organization-initiative
info-type: policy-document
primary-topic: Defines the organizational standards for active projects.
related-standards: []
version: 1.0.1
date-created: YYYY-MM-DDTHH:MM:SSZ
date-modified: '2025-06-17T02:29:13Z'
primary_domain: GM
sub_domain: PROJECT_MGMT
scope_application: All projects within the active-project directory.
criticality: P1-High
lifecycle_gatekeeper: TBD
impact_areas:
- project-structure
- repository-organization
- workflow-standardization
change_log_url: TBD
maturity: Medium
lifecycle_stage: Draft
target_audience:
- all_contributors
- project_managers
project_phase: Definition
task_type: Standards Definition
jira_issue: TBD
history_summary: Original content from active-project-organization.md. Parent folder
  renamed to '-active-project-organization-initiative-active'.
key_takeaways:
- Defines folder structure, naming conventions, and lifecycle for projects.
next_steps:
- Refine templates and explore automation opportunities.
---
This is the project to re-organize projects in this repo. The `active-project/README.md` is going to be the central explanatory document. Templates and the main archive are external to the `active-project/` directory as you can see in the repo.



```
active-project/
├── README.md                               # Root README: THE SINGLE SOURCE OF TRUTH. Explains:
│                                           #   - Overall iterative workflow for projects and their l[n]-t[n] sub-tasks.
│                                           #   - Project & Sub-level Folder Naming within active-project/:
│                                           #     - [project-name]-initiative-[status-suffix]
│                                           #       (e.g., project-alpha-initiative-active, project-beta-initiative-completed).
│                                           #     - l[level]-t[turn]-[descriptive-name]-[status-suffix] for iterative sub-tasks
│                                           #       (e.g., l2-t1-fix-authentication-module-active).
│                                           #   - File Naming within project and l[n]-t[n] folders:
│                                           #     - master-analysis-report.md, master-roadmap.md (at project [-initiative-status] level).
│                                           #     - l[n]-t[n]-analysis-report.md, l[n]-t[n]-roadmap.md (within l[n]-t[n]-...-[status] folders).
│                                           #     - master-progress.md (at project level), l[n]-t[n]-progress.md (within l[n]-t[n] folders).
│                                           #   - Status Suffixes usage (kebab-case): -active, -completed, -blocked-by-sub-task, -planned, -on-hold.
│                                           #     (Applied to [project-name]-initiative-[status] folders and l[n]-t[n]-...-[status] sub-task folders).
│                                           #   - Initiating a New Project:
│                                           #     1. Create a new folder: active-project/[project-name]-initiative-planned/.
│                                           #     2. Inside, create master-analysis-report.md and master-roadmap.md using the linked templates.
│                                           #     3. Create master-progress.md.
│                                           #     4. All files MUST have full frontmatter (see frontmatter template).
│                                           #     5. When work begins, rename folder to [project-name]-initiative-active/.
│                                           #   - Spawning a New l[n]-t[n] Sub-level (e.g., L2 from L1 master-roadmap, or L3 from an L2 l[2]-t[x]-roadmap):
│                                           #     1. The parent folder (e.g., [project-name]-initiative-active/ or l[n]-t[m]-...-active/)
│                                           #        is RENAMED to append/update status to -blocked-by-sub-task.
│                                           #     2. A NEW sub-folder l[child-level]-t1-[complication-descriptive-name]-active/ is created
│                                           #        INSIDE the now -blocked-by-sub-task parent folder.
│                                           #        (child-level is parent-level + 1; t1 for the first turn/attempt at this new child-level).
│                                           #     3. This new sub-folder gets its l[child-level]-t1-analysis-report.md, -roadmap.md, and -progress.md.
│                                           #   - Completing Sub-levels & Returning to Parent Control:
│                                           #     1. The active l[child-level]-t1-...-active/ folder is RENAMED to -completed.
│                                           #     2. Its l[child-level]-t1-progress.md content (summary of commits/actions) is summarized
│                                           #        and APPENDED to its parent folder's progress.md file.
│                                           #     3. The parent folder (e.g., ...-blocked-by-sub-task/) is RENAMED back to -active.
│                                           #     4. Work on the parent folder's roadmap is resumed or updated based on sub-task outcome.
│                                           #   - Progress File Management:
│                                           #     - Each master-progress.md and l[n]-t[n]-progress.md is populated by appending commit messages or concise task updates.
│                                           #     - Upon an l[n]-t[n] task completion, its progress file is summarized into its parent progress file.
│                                           #   - Archival Process:
│                                           #     - Individual l[n]-t[n]-...-completed/ sub-task folders REMAIN within their parent project structure
│                                           #       in active-project/ until the ENTIRE [project-name]-initiative-... project is completed.
│                                           #     - Once a [project-name]-initiative-[status]/ is marked -completed, its WHOLE FOLDER
│                                           #       (containing all its master files and all nested l[n]-t[n]-...-completed/ sub-folders)
│                                           #       is MOVED from active-project/ to the CENTRALIZED, EXTERNAL archive/ directory.
│                                           #       (External archive location, e.g., ../archive/ or defined at repo root like /archive/).
│                                           #   - Links to Document Templates (these templates are located externally, e.g., in standards/templates/):
│                                           #     - Analysis Report Template: [Link to standards/templates/analysis-report-template.md]
│                                           #     - Roadmap Template: [Link to standards/templates/roadmap-template.md]
│                                           #     - Frontmatter Template: [Link to standards/templates/frontmatter-template.md]
│                                           #   - Links to all relevant universal project-guidelines/ (e.g., work ethic, further naming details).
│
├── project-guidelines/                     # UTILITY: Universal guidelines applicable to all project work. Referenced by root README.
│   └── [guideline-topic]-guideline.md      # Example: work-ethic-guideline.md, file-naming-details-guideline.md
│
├── [project-alpha-name]-initiative-[status]/ # PROJECT LEVEL CONTAINER (e.g., -active, -completed, -planned, -on-hold)
│   │                                       # This entire folder, with all its contents, moves to the external archive/ upon final project completion.
│   ├── master-progress.md                  # Overall progress for Project Alpha. Updated by summarizing l2-tx-progress.md files.
│   │
│   ├── master-analysis-report.md           # LEVEL 1 (Project Definition): Defines/justifies the entire Project Alpha.
│   ├── master-roadmap.md                   # LEVEL 1 (Project Definition): Master plan for Project Alpha.
│   │                                       # If THIS roadmap is blocked by a complication, this project folder status becomes e.g., -blocked-by-l2-task,
│   │                                       # and an l2-t1-...-active/ folder is created below.
│   │
│   ├── l2-t1-[P1-complication-descriptive-name]-[status]/ # LEVEL 2, TURN 1 (Addresses 1st complication from L1 master-roadmap)
│   │   │                                                # (Status: e.g., -active, -completed, -blocked-by-l3-task)
│   │   ├── l2-t1-progress.md               # Progress for this L2-T1 effort. Upon L2-T1 completion, summarized & appended to master-progress.md.
│   │   │
│   │   ├── l2-t1-analysis-report.md        # Analysis for THIS L2-T1 sub-task/complication.
│   │   └── l2-t1-roadmap.md                # Execution plan for THIS L2-T1 sub-task/complication.
│   │   │                                   # If THIS L2-T1 roadmap is blocked, its folder becomes -blocked-by-l3-task,
│   │   │                                   # and an l3-t1-...-active/ folder is created inside here.
│   │   │
│   │   ├── l3-t1-[P1.1-sub-complication-descriptive-name]-[status]/ # LEVEL 3, TURN 1 (Addresses 1st complication from L2-T1 roadmap)
│   │   │   │                                                       # (Status: e.g., -active, -completed)
│   │   │   ├── l3-t1-progress.md           # Progress for L3-T1. Summarized to l2-t1-progress.md on completion.
│   │   │   │
│   │   │   ├── l3-t1-analysis-report.md    # Analysis for THIS L3-T1 sub-task.
│   │   │   └── l3-t1-roadmap.md            # Execution plan for THIS L3-T1 sub-task.
│   │   │   └── (Can nest further: l4-t1-...-[status]/ if this L3-T1 roadmap gets complicated)
│   │   │
│   │   └── l3-t2-[P1.2-sub-complication-descriptive-name]-[status]/ # LEVEL 3, TURN 2 (If L2-T1 roadmap, after L3-T1 completed,
│   │       │                                                       #  hits a *new, distinct* complication).
│   │       ├── l3-t2-progress.md
│   │       ├── l3-t2-analysis-report.md
│   │       └── l3-t2-roadmap.md
│   │
│   └── l2-t2-[P2-complication-descriptive-name]-[status]/ # LEVEL 2, TURN 2 (Addresses 2nd distinct complication from L1 master-roadmap,
│       │                                                #  AFTER l2-t1-...-completed was finished, and master-roadmap work resumed, then hit another snag).
│       ├── l2-t2-progress.md
│       ├── l2-t2-analysis-report.md
│       └── l2-t2-roadmap.md
│       └── ... (Can have its own l3-tx... sub-levels if it gets complicated)
│
└── [project-beta-name]-initiative-[status]/ # Another top-level project, structured identically.
    └── ...

# Note on External Locations (NOT part of this 'active-project/' tree):
# - Centralized Templates: Assumed to be at a path like 'standards/templates/'.
#   The root active-project/README.md will contain direct links to these template files.
# - Centralized Archive: Assumed to be a directory SIBLING to 'active-project/' or at the repository root,
#   e.g., '../archive/' or '/archive/'. Completed '[project-name]-initiative-completed/' FOLDERS are MOVED here.
```
