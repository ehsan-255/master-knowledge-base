# Active Projects: Workflow and Organization

This document outlines the standardized structure and workflow for all projects managed within the `active-project/` directory. Adherence to these guidelines is crucial for maintaining clarity and efficiency.

## Core Principles

*   **Iterative Workflow**: Projects are often broken down into iterative sub-tasks, managed in levels (`l[n]`) and turns (`t[n]`).
*   **Single Source of Truth**: Each project and sub-task will have dedicated analysis, roadmap, and progress files.
*   **Status Tracking**: Folder names include status suffixes to clearly indicate the current state of a project or sub-task.

## Folder and File Naming Conventions

### Project & Sub-level Folder Naming:

*   **Project Folders**: `[project-name]-initiative-[status-suffix]`
    *   Example: `project-alpha-initiative-active`, `project-beta-initiative-completed`
*   **Sub-task Folders (Iterative Levels)**: `l[level]-t[turn]-[descriptive-name]-[status-suffix]`
    *   Example: `l2-t1-fix-authentication-module-active`
    *   These are nested within their parent project or parent sub-task folder.

### File Naming (within project and l[n]-t[n] folders):

*   **Master Project Files (at project `...-initiative-[status]` level):**
    *   `master-analysis-report.md`
    *   `master-roadmap.md`
    *   `master-progress.md`
*   **Sub-task Files (within `l[n]-t[n]-...-[status]` folders):**
    *   `l[n]-t[n]-analysis-report.md`
    *   `l[n]-t[n]-roadmap.md`
    *   `l[n]-t[n]-progress.md`

### Status Suffixes (kebab-case):

Applied to project and sub-task folders:

*   `-active`
*   `-completed`
*   `-blocked-by-sub-task`
*   `-planned`
*   `-on-hold`

## Project Lifecycle

### 1. Initiating a New Project:

1.  Create a new folder: `active-project/[project-name]-initiative-planned/`.
2.  Inside, create `master-analysis-report.md` and `master-roadmap.md` using the linked templates.
3.  Create `master-progress.md`.
4.  All files **MUST** have full frontmatter (see frontmatter template).
5.  When work begins, rename the folder to `[project-name]-initiative-active/`.

### 2. Spawning a New l[n]-t[n] Sub-level:

This occurs when a roadmap (either `master-roadmap.md` or an `l[n]-t[m]-roadmap.md`) encounters a significant complication requiring a dedicated sub-task.

1.  The parent folder (e.g., `[project-name]-initiative-active/` or `l[n]-t[m]-...-active/`) is **RENAMED** to append/update its status to `-blocked-by-sub-task`.
2.  A **NEW** sub-folder `l[child-level]-t1-[complication-descriptive-name]-active/` is created **INSIDE** the now `-blocked-by-sub-task` parent folder.
    *   `[child-level]` is `[parent-level] + 1`.
    *   `t1` signifies the first turn/attempt at this new child-level task.
3.  This new sub-folder gets its own:
    *   `l[child-level]-t1-analysis-report.md`
    *   `l[child-level]-t1-roadmap.md`
    *   `l[child-level]-t1-progress.md`
    *   (All using appropriate templates and including frontmatter).

### 3. Completing Sub-levels & Returning to Parent Control:

1.  The active `l[child-level]-t[x]-...-active/` folder is **RENAMED** to `-completed`.
2.  Its `l[child-level]-t[x]-progress.md` content (a summary of commits/actions) is summarized and **APPENDED** to its parent folder's progress file (e.g., `master-progress.md` or `l[parent-level]-t[m]-progress.md`).
3.  The parent folder (e.g., `...-blocked-by-sub-task/`) is **RENAMED** back to `-active`.
4.  Work on the parent folder's roadmap is resumed or updated based on the sub-task's outcome.

### 4. Progress File Management:

*   Each `master-progress.md` and `l[n]-t[n]-progress.md` is populated by appending commit messages or concise task updates.
*   Upon an `l[n]-t[n]` task completion, its progress file content is summarized into its parent's progress file.

### 5. Archival Process:

*   Individual `l[n]-t[n]-...-completed/` sub-task folders **REMAIN** within their parent project structure in `active-project/` until the **ENTIRE** `[project-name]-initiative-...` project is completed.
*   Once a `[project-name]-initiative-[status]/` is marked `-completed`, its **WHOLE FOLDER** (containing all its master files and all nested `l[n]-t[n]-...-completed/` sub-folders) is **MOVED** from `active-project/` to the centralized, external `archive/` directory (located at the repository root).

## Document Templates

These templates are located in `master-knowledge-base/standards/templates/`:

*   **Analysis Report Template**: [Analysis Report Template](../master-knowledge-base/standards/templates/analysis-report-template.md)
*   **Roadmap Template**: [Roadmap Template](../master-knowledge-base/standards/templates/roadmap-template.md)
*   **Frontmatter Template**: [Frontmatter Template](../master-knowledge-base/standards/templates/tpl-canonical-frontmatter.md)
    *   *Note: This is the canonical frontmatter template to be used for all content files.*

## Universal Project Guidelines

Refer to the following guidelines for universal practices applicable to all project work:

*   [Work Ethic Guidelines](./project-guidelines/project-work-ethic-guidelines.md)
*   [Project Reminders](./project-guidelines/project-reminders.md)
*   *(Add links to other relevant guidelines in `active-project/project-guidelines/` as needed)*
