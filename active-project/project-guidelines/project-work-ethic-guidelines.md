---
title: Project Work Ethic Guidelines
standard_id: project-guideline-work-ethic
tags: [status/active, info-type/project-guideline, topic/project-conduct]
kb-id: project-governance
info-type: project-guideline
primary-topic: Guidelines for professional conduct and collaboration within the project.
version: '1.0.0'
date-created: '2025-05-25T00:00:00Z'
date-modified: '2025-05-31T09:33:00Z'
primary_domain: PROJECT
sub_domain: GUIDELINES
scope_application: All contributors to this knowledge base project.
criticality: p2-medium
lifecycle_gatekeeper: N/A
impact_areas: [team-collaboration, project-culture]
change_log_url: N/A
---

# Work Ethic & Operational Guidelines for Project Tasks

## 1. Core Principles

**1.1. Ownership & Responsibility:**
    -   Take full ownership of assigned tasks. Do not deflect responsibility or suggest manual work for tasks that can or should be automated or investigated more thoroughly.
    -   Proactively identify and resolve issues within the scope of your abilities and the task at hand.

**1.2. Fact-Based Work - No Assumptions:**
    -   **Never assume.** Always verify information, file states, script behaviors, and the current status of data or standards.
    -   Base decisions and actions on verifiable facts derived from direct investigation (e.g., reading files, running tools, checking configurations) rather than assumptions or outdated information.
    -   If a piece of information is critical and unknown (e.g., a file path), exhaust available tools (file search, code search) to find it. If still unknown, clearly state what is missing and why it blocks progress, rather than making a potentially incorrect assumption to proceed.

**1.3. Precision & Attention to Detail:**
    -   Meticulously check details: regex patterns, file paths, configuration settings, script logic, and linter/tool outputs.
    -   Ensure that automated actions (e.g., script-based file edits) are precise and achieve the intended outcome without unintended side effects. Small errors in patterns or logic can lead to widespread issues.

**1.4. Adherence to Standards:**
    -   Internalize and strictly adhere to all documented project standards (e.g., naming conventions, `standard_id` formats, metadata schemas like `MT-SCHEMA-FRONTMATTER.md`, linking policies, coding guidelines).
    -   Tools (linters, scripts) should be configured to enforce these standards rigorously.
    -   If data conflicts with a standard, the primary approach is to correct the data. If the standard itself is found to be unworkable or outdated, this should be flagged for discussion and formal update, not silently worked around by relaxing tool enforcement.

## 2. Working with Scripts & Automation

**2.1. Importance of Automation:**
    -   Strive to automate repetitive tasks, data correction, validation, and reporting wherever feasible and reliable. This improves efficiency, consistency, and reduces manual error.
    -   Develop robust scripts that are configurable, handle errors gracefully, and provide clear logging.

**2.2. Script Development & Testing Workflow:**
    -   **Dry Runs are Mandatory:** Before running any script that modifies files or data live, ALWAYS perform a dry run (`--dry-run` flag or similar mechanism). Carefully review the dry run output to ensure the script will perform the intended actions correctly and on the correct targets.
    -   **Incremental Application:** For widespread changes, consider running scripts on a small subset of data/files first to verify behavior before a global run.
    -   **Live Run with Caution:** Only proceed with a live run (without `--dry-run`) after a successful and thoroughly reviewed dry run.

**2.3. Logging & Verification:**
    -   **Comprehensive Logging:** All scripts MUST implement comprehensive logging that details:
        -   Files processed.
        -   Actions taken (or that would be taken in a dry run).
        -   Specific changes made (e.g., "changed X to Y in file Z").
        -   Any errors, warnings, or skipped items with clear reasons.
        -   A summary of operations (e.g., total files scanned, files changed).
    -   **Log Review:** Immediately after any script run (dry or live), the output log MUST be thoroughly reviewed to confirm the script behaved as expected and to identify any unexpected outcomes.
    -   **Manual Spot-Checking of Results:** After a live script run that modifies data or files, a significant percentage of the affected items (e.g., 50% or a risk-based sample) MUST be manually checked to verify the accuracy and correctness of the changes. Do not assume the script worked perfectly based solely on a successful exit code or a positive-looking log summary.

## 3. Iterative Problem Solving & Verification

**3.1. Use Current Data:**
    -   Always work from the most recent and up-to-date information. If a linter report is generated, base subsequent actions on *that specific report*.
    -   If data-modifying scripts are run, immediately re-run validation tools (e.g., indexer, linter) to get a fresh assessment of the current state. Do not proceed with further fixes based on an outdated report.

**3.2. Decompose Complex Tasks:**
    -   Break down large or complex tasks into smaller, manageable, and verifiable steps.
    -   Address one category of issue at a time if possible, verify the fix, then move to the next.

**3.3. Investigate, Don't Assume:**
    -   If a tool reports an error or warning that seems incorrect (e.g., a link reported as broken when it seems valid), investigate deeper. This might involve:
        -   Checking the tool's configuration (e.g., regex patterns, input paths).
        -   Verifying the source data directly (e.g., the content of the file being linted).
        -   Adding debug output to tools to understand their internal state or decision-making.

**3.4. Tool Limitations & Asking for Help:**
    -   Understand the limitations of available tools. If a tool is consistently failing to perform a specific type of complex edit or if its internal linter reports phantom errors, document this issue.
    -   If, after thorough investigation and multiple attempts, a problem cannot be resolved with the available tools or expertise, then it is appropriate to clearly articulate the problem, the steps taken, and ask for stakeholder input or assistance.

## 4. Professionalism & Communication

-   Maintain a high standard of work ethic. Avoid shortcuts that compromise quality or adherence to standards.
-   If a mistake is made or a previous approach was flawed, acknowledge it, learn from it, and proactively correct the course of action.
-   Clearly communicate plans, actions taken, results observed, and any remaining issues or dependencies.

By consistently applying these guidelines, team members can contribute to a high-quality, reliable, and maintainable project, fostering a professional and effective work environment. 