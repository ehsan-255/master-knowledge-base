---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:12Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: active-project
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# Active Projects: **MANDATORY** Workflow and Organization

**THIS DOCUMENT ESTABLISHES THE NON-NEGOTIABLE STANDARDIZED STRUCTURE AND WORKFLOW FOR ALL PROJECTS MANAGED WITHIN THE `active-project/` DIRECTORY. ADHERENCE TO THESE GUIDELINES IS ABSOLUTELY MANDATORY FOR MAINTAINING CLARITY AND EFFICIENCY.**

## **CORE PRINCIPLES — ABSOLUTE COMPLIANCE REQUIRED**

*   **ITERATIVE WORKFLOW**: Projects **MUST** be broken down into iterative sub-tasks, managed in levels (`l[n]`) and turns (`t[n]`).
*   **SINGLE SOURCE OF TRUTH**: Each project and sub-task **WILL** have dedicated analysis, roadmap, and progress files.
*   **STATUS TRACKING**: Folder names **MUST** include status suffixes to clearly indicate the current state of a project or sub-task.

## **MASTER PROJECT DOCUMENTS — MANDATORY IMPLEMENTATION**

### **MASTER-ANALYSIS-REPORT — PRIMARY BLUEPRINT**

>**THE `master-analysis-report` IS THE PRIMARY BLUEPRINT FOR THE PROJECT, PROVIDING A COMPREHENSIVE OVERVIEW THAT INCLUDES THE PROJECT'S OBJECTIVES, SUCCESS CRITERIA, RATIONALE, AFFECTED DOMAINS, AND AN OVERARCHING STRATEGY FOR ACHIEVING ITS GOALS.**

**CRITICAL SPECIFICATIONS:**
- **PROVIDES** a high-level, 30,000-foot view with sufficient granularity to enable the creation of individual sub-tasks without ambiguity about requirements
- **SERVES** as the foundational document from which all other project documentation derives
- **CONTAINS** comprehensive project definition, scope boundaries, success metrics, and strategic approach

**DETAILED GUIDELINES:** [Master Analysis Report Creation Guide](./master-analysis-report-creation-guide.md)

### **MASTER-ROADMAP — EXECUTION SEQUENCE AUTHORITY**

>**THE `master-roadmap` DERIVES FROM THE `master-analysis-report` AND SPECIFIES THE MANDATORY SEQUENCE IN WHICH ALL PROJECT TASKS MUST BE EXECUTED TO ACHIEVE COMPLETION.**

**CRITICAL SPECIFICATIONS:**
- **OUTLINES** various high-level steps, each of which **WILL** be treated as an independent job or project requiring its own `analysis-report` and `roadmap`
- **WORK DECOMPOSITION** begins with identifying the largest segments of work and progresses incrementally to smaller, actionable units
- **THE SMALLEST GRANULAR TASK** must be executable within a single sprint and **MUST** follow the format in `active-project/roadmap-template`
- **DECOMPOSITION STRUCTURE**: Uses "sub-levels" (`sl[n]`) for hierarchical task breakdown

**EXCEPTION FOR MINOR PROJECTS:** Minor projects may not require a separate `master-roadmap`. In such cases, direct task execution via the `active-project/roadmap-template` alone **WILL** suffice, and this scenario **MUST** be explicitly documented.

**DETAILED GUIDELINES:** [Master Roadmap Development Guide](./master-roadmap-development-guide.md)

### **MASTER-PROGRESS — CENTRALIZED PROGRESS AUTHORITY**

>**THE `master-progress` IS DISTINCT FROM THE `active-project/roadmap-progress-tracker-template.md` AND `active-project/roadmap-checklist-template.md`. WHILE THE LATTER TWO FOCUS ON ROADMAP-SPECIFIC PROGRESS, THE `master-progress` TRACKS OVERALL PROJECT PROGRESS, MAJOR CHANGES, DECISIONS, DEVIATIONS FROM THE `master-analysis-report` OR `master-roadmap`, AND JUSTIFICATIONS FOR SUCH CHANGES.**

**CRITICAL SPECIFICATIONS:**
- **MAINTAINS** a single `master-progress` document at the project's highest level, consolidating all progress metrics, changes, and insights into one centralized resource
- **TRACKS** overall project progress, major changes, decisions, deviations, and justifications
- **AFTER** a roadmap reaches its lowest level of decomposition and tasks are assigned using `active-project/roadmap-template`, progress at this granular level **MUST** be tracked in `active-project/roadmap-progress-tracker-template.md`

## **FOLDER AND FILE NAMING CONVENTIONS — STRICT ADHERENCE REQUIRED**

### **Project & Sub-level Folder Naming:**

*   **Project Folders**: `-[project-name]-initiative-[status-suffix]`
    *   Example: `-project-alpha-initiative-active`, `-project-beta-initiative-completed`
*   **Sub-task Folders (Iterative Levels)**: `l[level]-sl[sub-level]-[descriptive-name]-[status-suffix]`
    *   Example: `l2-sl1-fix-authentication-module-active`
    *   These **MUST** be nested within their parent project or parent sub-task folder.

### **File Naming (within project and l[n]-t[n] folders):**

*   **Master Project Files (at project `...-initiative-[status]` level):**
    *   `master-analysis-report.md`
    *   `master-roadmap.md`
    *   `master-progress.md`
*   **Sub-task Files (within `l[n]-sl[n]-...-[status]` folders):**
    *   `l[n]-sl[n]-analysis-report.md`
    *   `l[n]-sl[n]-roadmap.md`
    *   `l[n]-sl[n]-progress.md`

### **Status Suffixes (kebab-case) — MANDATORY APPLICATION:**

Applied to project and sub-task folders:

*   `-active`
*   `-completed`
*   `-blocked`
*   `-planned`
*   `-on-hold`

### **Branch Naming Convention — STRICT COMPLIANCE**

When working on any task related to `active-project/`, branches **MUST** be named according to the following pattern:

`[folder-name-minus-status]-YYYYMMDD-HHMM`

Where:
*   `[folder-name-minus-status]` is the full name of the project initiative folder (e.g., `my-new-project-initiative`) or the sub-task folder (e.g., `l2-sl1-some-feature`) with its status suffix (e.g., `-active`, `-completed`, `-planned`) removed.
*   `YYYYMMDD-HHMM` is the current date and time when the branch is created.

**MANDATORY EXAMPLES:**
*   If working on tasks for a project initiative folder named `active-project/my-new-project-initiative-planned/`, a branch name **MUST** be: `my-new-project-initiative-20240716-1430`.
*   If working on a sub-task in `active-project/my-new-project-initiative-active/l2-sl1-some-feature-active/`, a branch name **MUST** be: `l2-sl1-some-feature-20240716-1430`.

## Overall Directory Structure Visualized

The following diagram illustrates the typical structure for active projects and their sub-levels:

```
active-project/
├── README.md
│
├── project-guidelines/                     # UTILITY: Universal project guidelines.
│   └── [guideline-topic]-guideline.md      # Example: work-ethic-guideline.md
│
├── -[project-alpha-name]-initiative-[status]/ # PROJECT LEVEL CONTAINER
│   │
│   ├── master-progress.md                  # L1: Overall Project Alpha Progress
│   │
│   ├── master-analysis-report.md           # L1: Project Definition Analysis
│   ├── master-roadmap.md                   # L1: Project Definition Roadmap
│   │
│   ├── l2-sl1-[descriptive-name]-[status]/    # L2, SL1: First sub-task from L1 roadmap
│   │   │
│   │   ├── l2-sl1-progress.md               # L2-SL1 Progress File
│   │   │
│   │   ├── l2-sl1-analysis-report.md        # L2-SL1 Analysis
│   │   └── l2-sl1-roadmap.md                # L2-SL1 Roadmap
│   │   │
│   │   ├── l3-sl1-[descriptive-name]-[status]/ # L3, SL1: First sub-task from L2-SL1 roadmap
│   │   │   │
│   │   │   ├── l3-sl1-progress.md           # L3-SL1 Progress File
│   │   │   │
│   │   │   ├── l3-sl1-analysis-report.md    # L3-SL1 Analysis
│   │   │   └── l3-sl1-roadmap.md            # L3-SL1 Roadmap
│   │   │   └── ... (Can nest further to L4, etc.)
│   │   │
│   │   └── l3-sl2-[descriptive-name]-[status]/ # L3, SL2: Second sub-task from L2-SL1 roadmap
│   │       │
│   │       ├── l3-sl2-progress.md
│   │       ├── l3-sl2-analysis-report.md
│   │       └── l3-sl2-roadmap.md
│   │
│   └── l2-sl2-[descriptive-name]-[status]/    # L2, SL2: Second sub-task from L1 roadmap
│       │
│       ├── l2-sl2-progress.md
│       ├── l2-sl2-analysis-report.md
│       └── l2-sl2-roadmap.md
│       └── ...
│
└── -[project-beta-name]-initiative-[status]/ # Another top-level project.
    └── ...
```

## **PROJECT LIFECYCLE — MANDATORY EXECUTION SEQUENCE**

### **1. Initiating a New Project — STRICT PROTOCOL:**

1.  **CREATE** a new folder: `active-project/-[project-name]-initiative-planned/`.
2.  **GENERATE** `master-analysis-report.md` and `master-roadmap.md` using the linked templates.
3.  **CREATE** `master-progress.md`.
4.  **PRE-POPULATE PLANNED PHASES**: Based on the `master-roadmap.md`, create a sub-folder for each major phase of work (e.g., `l2-sl1-[phase-one-name]-planned/`, `l2-sl2-[phase-two-name]-planned/`, etc.). These folders **MUST** receive the `-planned` status suffix.
5.  **ALL FILES MUST HAVE** full frontmatter (see frontmatter template).
6.  **WHEN WORK BEGINS** on the first phase, follow the sub-level activation protocol below.

### **2. Managing Sub-level Lifecycles — MANDATORY PROCESS:**

This section covers activating a planned task or spawning a new one for unforeseen complications. In all cases, only one `l[n]-sl[n]` sub-task can be `-active` within a parent project at any given time.

**A. Activating a Planned Task:**
1.  The parent project folder (e.g., `-[project-name]-initiative-active/` or `...-planned/`) **MUST BE RENAMED** to append/update its status to `-blocked`.
2.  The target sub-folder (e.g., `l[child-level]-sl[x]-...-planned/`) **MUST BE RENAMED** from `-planned` to `-active`.
3.  **RE-EVALUATE AND UPDATE PLANS**: Before generating documents, the plan for this newly activated phase **MUST** be re-evaluated. Any learnings, new decisions, or changes from previously completed sub-tasks **MUST** be incorporated. The `analysis-report` and `roadmap` created in the next step must reflect the *current* state of understanding, not just the initial plan.
4.  This now `-active` sub-folder **MUST RECEIVE** its own `analysis-report`, `roadmap`, and `progress` files, reflecting the re-evaluated plan.

**B. Spawning a New (Unplanned) Task:**
This occurs when a roadmap encounters a significant complication requiring a dedicated sub-task.
1.  The parent folder (e.g., `-[project-name]-initiative-active/`) **MUST BE RENAMED** to append/update its status to `-blocked`.
2.  A **NEW** sub-folder `l[child-level]-sl[x]-[complication-descriptive-name]-active/` **MUST BE CREATED INSIDE** the now `-blocked` parent folder.
3.  This new sub-folder **MUST RECEIVE** its own `analysis-report`, `roadmap`, and `progress` files.

### **3. Completing Sub-levels & Returning to Parent Control — MANDATORY SEQUENCE:**

1.  The active `l[child-level]-sl[x]-...-active/` folder **MUST BE RENAMED** to `-completed`.
2.  Its `l[child-level]-sl[x]-progress.md` content (a summary of commits/actions) **MUST BE SUMMARIZED AND APPENDED** to its parent folder's progress file (e.g., `master-progress.md` or `l[parent-level]-sl[m]-progress.md`).
3.  The parent folder (e.g., `...-blocked/`) **MUST BE RENAMED** back to `-active`.
4.  Work on the parent folder's roadmap **MUST BE RESUMED** or updated based on the sub-task's outcome.

### **4. Progress File Management — CONTINUOUS REQUIREMENT:**

*   Each `master-progress.md` and `l[n]-sl[n]-progress.md` **MUST BE POPULATED** by appending commit messages or concise task updates.
*   Upon an `l[n]-sl[n]` task completion, its progress file content **MUST BE SUMMARIZED** into its parent's progress file.

### **5. Archival Process — MANDATORY PROTOCOL:**

*   Individual `l[n]-sl[n]-...-completed/` sub-task folders **MUST REMAIN** within their parent project structure in `active-project/` until the **ENTIRE** `-[project-name]-initiative-...` project is completed.
*   Once a `-[project-name]-initiative-[status]/` is marked `-completed`, its **WHOLE FOLDER** (containing all its master files and all nested `l[n]-sl[n]-...-completed/` sub-folders) **MUST BE MOVED** from `active-project/` to the centralized, external `archive/` directory (located at the repository root).

## **DOCUMENT TEMPLATES — MANDATORY USAGE**

These templates are located in `standards/templates/`:

*   **Analysis Report Template**: [Analysis Report Template](../standards/templates/analysis-report-template.md)
*   **Roadmap Template**: [Roadmap Template](./roadmap-template.md)
*   **Frontmatter Template**: [Frontmatter Template](../standards/templates/tpl-canonical-frontmatter.md)
    *   *Note: This is the canonical frontmatter template that **MUST** be used for all content files.*

## **EXTERNAL DEPENDENCIES AND NOTES**

### **Templates**
Centralized document templates (e.g., for Analysis Reports, Roadmaps, Frontmatter) are located externally in the `standards/templates/` directory. This `active-project/README.md` contains direct relative links to these templates.

### **Archive**
The centralized archive for completed projects is located at the repository root in the `/archive/` directory. Once an entire `-[project-name]-initiative-[status]/` (e.g., `-my-project-initiative-completed/`) is marked as completed, its whole folder, including all master files and nested sub-task folders, **MUST BE MOVED** from `active-project/` to this `/archive/` directory.

## **CURRENT STATE TRACKING — MANDATORY MAINTENANCE**

### **current-state.md — PROJECT PORTFOLIO LOG**

**PURPOSE:** Centralized chronological log tracking **TOP-LEVEL PROJECT STATUS CHANGES ONLY**

**MANDATORY UPDATES:**
1. **PROJECT INITIATION**: Log when new `-[project-name]-initiative-planned/` folders are created
2. **STATUS TRANSITIONS**: Log only when top-level projects change status (`-planned` → `-active` → `-completed`/`-blocked`/`-on-hold`)
3. **COMPLETION SUMMARY**: Brief achievement summary for completed projects

**UPDATE FORMAT:** Always append entries with UTC timestamps. Keep summaries to **1-2 sentences maximum**.

**SCOPE RESTRICTION:** **DO NOT** log sub-task (`l[n]-sl[n]`) status changes - only top-level project initiatives.

---

## **UNIVERSAL PROJECT GUIDELINES — MANDATORY COMPLIANCE**

**REFER TO THE FOLLOWING GUIDELINES FOR UNIVERSAL PRACTICES APPLICABLE TO ALL PROJECT WORK:**

*   [Work Ethic Guidelines](./project-guidelines/project-work-ethic-guidelines.md)
*   [Project Reminders](./project-guidelines/project-reminders.md)
*   *(Add links to other relevant guidelines in `active-project/project-guidelines/` as needed)*
