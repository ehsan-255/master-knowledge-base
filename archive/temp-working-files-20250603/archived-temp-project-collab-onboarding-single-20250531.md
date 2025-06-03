# Project Collaboration & Onboarding Guide (Single Contributor Model)

## 1. Introduction

### 1.1 Purpose of This Guide
This document establishes the standardized workflow, decision-making process, documentation structure, and onboarding procedures for the "Knowledge Base Standards Refactoring" project. Its purpose is to ensure clarity, consistency, and efficiency for the individual contributor, whether returning after an absence or engaging with the project for the first time.

### 1.2 Project Goal Overview
The primary objective of this project is to refactor the existing knowledge base standards into a more granular, atomic, metadata-rich, and automation-centric architecture. This transformation aims to improve maintainability, discoverability, machine-processability (including for LLM interactions), and overall governance of the standards ecosystem.

## 2. Roles and Responsibilities

In this project, a single individual (hereafter referred to as "the Contributor") assumes all technical and analytical responsibilities previously distributed among multiple team members. Ehsan serves as the Project Lead and Facilitator.

- **Ehsan (Project Lead & Facilitator):**
    - Oversees the project, approves decisions, and ensures alignment with strategic objectives.
    - Acts as the central communication hub, relaying tasks, drafts, and feedback.
    - Operates the Executing LLM for precise, scripted file system operations.
    - May execute smaller, well-defined file modifications directly.

- **The Contributor (Technical Analyst, Architect, and Automation Engineer):**
    - Proposes immediate next steps or tasks for the project.
    - Drafts technical solutions, new or refactored standard definitions, automation specifications, and detailed execution plans for approved steps.
    - Conducts critical self-review of technical drafts, plans, and standard definitions.
    - Ensures precision, adherence to standards, and automation readiness.
    - Designs and engineers prompts for the Executing LLM and performs all technical analysis and architectural work.

- **Executing LLM (Automation Tool):**
    - A Large Language Model capable of performing precise, pre-defined file system operations (create, modify, rename files/folders) on the project repository.
    - Operates solely based on explicit, unambiguous prompts provided by Ehsan or the Contributor. It does not make independent decisions.

## 3. Workflow

The project follows a structured, iterative process designed for clarity and consensus between the Contributor and Ehsan:

1. **Step Definition & Task Assignment:**
    - The Contributor defines and proposes the immediate next project step or task.
    - Ehsan reviews the proposal. If approved, Ehsan relays the defined step/task back to the Contributor for execution.

2. **Drafting & Technical Design:**
    - The Contributor analyzes the assigned step/task and drafts the necessary technical solution, which may include:
        - New or modified standard documents.
        - Updates to registry files or templates.
        - Specifications for automation scripts.
        - Detailed plans for content refactoring.
    - The Contributor submits the draft to Ehsan for initial review and alignment.

3. **Review, Iteration & Consensus:**
    - Ehsan performs a thorough review of the Contributor’s draft.
    - Ehsan provides feedback, which the Contributor addresses by revising drafts as needed.
    - This iterative loop continues, with Ehsan facilitating communication and ensuring all perspectives are considered, until consensus is reached on the solution.
    - During collaboration, Ehsan and the Contributor must critically review each other's responses and are expected to push back if a response appears inaccurate, incomplete, or unclear. Responses should only be accepted when they are accurate, comprehensive, and on point.
    - Once common ground has been reached, the Contributor must clearly notify Ehsan that consensus has been achieved and provide the exact final results and/or specify the actions required for implementation or saving the results of the loop.
    - All finalized decisions and progress must be produced in a "text-block" so Ehsan can save it in roadmap-progress.md.

4. **Finalization & Execution Preparation:**
    - Once consensus is reached, the Contributor fine-tunes the approved approach into precise, executable instructions, including:
        - Finalizing the content of new/modified files.
        - Engineering granular, unambiguous prompts for tasks to be performed by the Executing LLM.
    - The Contributor submits the finalized plan and/or prompts to Ehsan for final approval before execution.

5. **Execution:**
    - For tasks designated for the Executing LLM, Ehsan uses the approved prompts to direct the LLM's file system operations.
    - For smaller, clearly defined modifications, Ehsan may execute them directly, based on the finalized plan.

6. **Verification & Closure:**
    - Both Ehsan and the Contributor review the outcome of the executed step to ensure it meets the requirements and quality standards.
    - All finalized decisions and progress must be produced in a "text-block" so Ehsan can save it in roadmap-progress.md. Relevant project documents (e.g., Roadmap, roadmap-progress.md) are updated as needed.

> **IMPORTANT:**  
> The Contributor is responsible for all technical analysis and decision-making, but only Ehsan executes or approves actions. Every necessary action at the end of any collaboration loop which is required to execute the decisions made throughout that loop must be clearly and concisely provided to Ehsan.

**Guiding Principles:**
- **Clarity & Precision:** All communications, definitions, and especially prompts for the Executing LLM, must be unambiguous.
- **Iterative Refinement:** Solutions are developed through cycles of drafting, review, and feedback.
- **Consensus-Driven:** Decisions on technical approaches and standard content are finalized through agreement between the Contributor and Ehsan.
- **Documented Decisions:** Key decisions, clarifications, and rationale are captured in "text-blocks" for Ehsan to save in roadmap-progress.md to maintain a project memory.

## 4. Understanding Project Documentation

The project relies on a suite of interconnected documents. Understanding their purpose and interrelations is key:

- **Core Architectural Documents:**
    - `Standards Categorization Scheme.md`: Defines the high-level organization of all standards.
    - `Single-Source Multi-View Standards Architecture.md`: Explains the model of atomic source files and derived views.
- **Planning & Tracking Documents:**
    - `Refactor Roadmap.md`: Outlines the overall plan, phases, steps, and tasks.
    - `roadmap-progress.md`: Tracks major pending tasks, issues, and records finalized decisions and progress.
- **Interaction Logs & Q&A:**
    - `end-of-session-summary.md` and `roadmap-progress.md` (if available): Records of session summaries, finalized decisions, clarifications, and progress that shape project decisions. These are vital for understanding the "why" behind certain choices.

**Reading Strategy:**
1. **Context First:** Start with this `Project Collaboration & Onboarding Guide`, then the `Refactor Roadmap.md`, `Standards Categorization Scheme.md`, and `Single-Source Multi-View Standards Architecture.md`.
2. **Review Session Summaries & Progress:** For historical context or clarification on past decisions, review `end-of-session-summary.md` and `roadmap-progress.md` (if available).
3. **Examine Frontmatter:** The YAML frontmatter of every document provides crucial metadata (version, status, primary topic).

## 5. Getting Started / Re-engaging with Work

Whether new to the project or returning after some time, the Contributor should follow these steps to get up to speed:

1. **Read this Guide:** Thoroughly read and understand this `Project Collaboration & Onboarding Guide.md`.
2. **Review Core Architecture & Roadmap:**
    - Familiarize oneself with the `Standards Categorization Scheme.md` and `Single-Source Multi-View Standards Architecture.md`.
    - Read the main `Refactor Roadmap.md` to understand the overall project lifecycle.
3. **Understand the Current Phase:**
    - Identify the currently active phase by consulting with Ehsan or checking the latest project updates.
4. **Catch Up on Recent Decisions:**
    - Review the most recent entries in `end-of-session-summary.md` and `roadmap-progress.md` (if available) to understand the latest discussions, clarifications, and decisions.
5. **Identify Current Tasks:**
    - Ehsan will assign or relay specific tasks based on the current phase and priorities.
6. **Locate Relevant Documentation:**
    - Use the project's directory structure (outlined in this guide and the roadmap) to find relevant standards, registries, or templates.
    - Once available, the `standards_index.json` will be a key tool for locating specific standards by ID or keyword.
7. **Ask Clarifying Questions:**
    - If any aspect of the project, current tasks, or documentation is unclear, the Contributor should proactively seek clarification from Ehsan, who will facilitate further discussion as needed.

## 6. Conclusion

The success of this project depends on meticulous planning, clear communication, and consistent adherence to defined processes and standards. By following this guide, the Contributor and Ehsan can work together effectively to create a robust, maintainable, and highly functional standards ecosystem.

---

> **IMPORTANT:**  
> At the end of each session, the Contributor will produce a summary of what happened in the session and specify where the next session should begin. Ehsan will review this summary and either approve it or propose additions/modifications as needed. Ehsan will save the summary in `end-of-session-summary.md`.

---

**End of document.**