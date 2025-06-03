# Project Collaboration & Onboarding Guide

## 1. Introduction

### 1.1 Purpose of This Guide
This document outlines the standardized collaboration model, decision-making processes, documentation structure, and onboarding procedures for the "Knowledge Base Standards Refactoring" project. Its purpose is to ensure clarity, consistency, and efficiency for all team members, whether new to the project or returning after a period of absence.

### 1.2 Project Goal Overview
The overarching goal of this project is to refactor the existing knowledge base standards into a more granular, atomic, metadata-rich, and automation-centric architecture. This will enhance maintainability, discoverability, machine-processability (including for LLM interactions), and overall governance of the standards ecosystem.

## 2. Core Team & Conceptual Roles

This project relies on a close-knit team with distinct conceptual roles, working in synergy:

*   **Ehsan (Project Lead & Facilitator):**
    *   Oversees the project, approves decisions, and ensures alignment with strategic objectives.
    *   Acts as the central communication hub, relaying tasks, drafts, and feedback between team members.
    *   Operates the "Executing LLM" for precise, scripted file system operations.
    *   May execute smaller, well-defined file modifications directly.
*   **Jim (Senior Knowledge & Automation Engineer):**
    *   Specializes in structured authoring, RDF/OWL, LLM-driven pipelines, and information architecture.
    *   Primarily responsible for drafting technical solutions, new/refactored standard definitions, automation specifications, and detailed execution plans for approved steps.
    *   Focuses on ensuring precision, adherence to standards, and automation readiness.
*   **Jack (Senior Analyst/Architect - Conceptual):**
    *   Primarily responsible for proposing the immediate next steps or tasks for the project.
    *   Conducts critical reviews of technical drafts, plans, and standard definitions proposed by Jim.
    *   Collaborates on solution design and ensures architectural integrity.
*   **Executing LLM (Automation Tool):**
    *   A Large Language Model with capabilities to perform precise, pre-defined file system operations (create, modify, rename files/folders) on the project repository.
    *   Operates solely based on explicit, unambiguous prompts engineered by the team (Jim, Jack, Ehsan). It does not make independent decisions.

## 3. Collaboration Workflow

Our collaboration follows a structured, iterative process designed for clarity and consensus:

1.  **Step Definition & Task Assignment:**
    *   **Proposal (Jack):** Jack defines and proposes the immediate next project step or task.
    *   **Approval & Relay (Ehsan):** Ehsan reviews Jack's proposal. If approved, Ehsan relays the defined step/task to Jim.

2.  **Drafting & Technical Design:**
    *   **Drafting (Jim):** Jim analyzes the assigned step/task and drafts the necessary technical solution. This may include:
        *   New or modified standard documents.
        *   Updates to registry files or templates.
        *   Specifications for automation scripts.
        *   Detailed plans for content refactoring.
    *   **Initial Review & Relay (Ehsan):** Jim submits the draft to Ehsan. Ehsan conducts an initial review for alignment and clarity, then relays the draft to Jack.

3.  **Review, Iteration & Consensus:**
    *   **Technical Review (Jack):** Jack performs a thorough technical review of Jim's draft.
    *   **Feedback Loop (Jack <-> Jim, via Ehsan):**
        *   Jack provides feedback to Ehsan, who relays it to Jim.
        *   Jim addresses the feedback and submits revised drafts to Ehsan.
        *   This iterative loop continues, with Ehsan facilitating communication and ensuring all perspectives are considered, until Jim and Jack reach a common ground and mutual agreement on the solution.
        *   **NOTE:** Jack and Jim may write their responses directly to each other, not to Ehsan. By passing along their responses, Ehsan gives implicit approval.
    *   **Critical Review & Pushback:**  
        During collaboration, Jack and Jim must review each other's responses critically and are expected to push back if a response appears inaccurate, incomplete, or unclear. Responses should only be accepted when they are accurate, comprehensive, and on point.
    *   **Consensus Notification & Final Results:**  
        After each collaboration loop, and once common ground has been reached, Jack and Jim must clearly notify Ehsan that consensus has been achieved. At this point, Jim must provide the exact final results and/or specify the actions required for implementation or saving the results of the loop.  
        **All finalized decisions and progress must be produced in a "text-block" so Ehsan can save it in roadmap-progress.md.**

4.  **Finalization & Execution Preparation:**
    *   **Fine-tuning (Jim):** Once consensus is reached, Jim fine-tunes the approved approach into precise, executable instructions. This includes:
        *   Finalizing the content of new/modified files.
        *   Engineering granular, unambiguous prompts for tasks to be performed by the Executing LLM.
    *   **Execution Approval (Ehsan):** Jim submits the finalized plan and/or prompts to Ehsan for final approval before execution.

5.  **Execution:**
    *   **LLM Operations (Ehsan + Executing LLM):** For tasks designated for the Executing LLM, Ehsan uses the approved prompts to direct the LLM's file system operations.
    *   **Direct Operations (Ehsan):** For smaller, clearly defined modifications, Ehsan may execute them directly, based on the finalized plan.

6.  **Verification & Closure:**
    *   **Collective Review (Jim, Jack, Ehsan):** All team members review the outcome of the executed step to ensure it meets the requirements and quality standards.
    *   **Documentation & Progress Update:** All finalized decisions and progress must be produced in a "text-block" so Ehsan can save it in roadmap-progress.md. Relevant project documents (e.g., Roadmap, roadmap-progress.md) are updated as needed.
>**IMPORTANT:** *JIM & JACK* ARE NOT TAKING ANY ACTIONS BUT ONLY TO HELP IN ANALYSIS AND DECISION MAKING; THEREFORE, EVERY NECESSARY ACTION AT THE END OF ANY COLLABORATION LOOP WHICH IS REQUIRED TO EXECUTE THE DECISIONS MADE THROUGHOUT THAT LOOP, MUST BE CLEARLY AND CONCISELY PROVIDED TO *EHSAN*.

**Guiding Principles for Collaboration:**
*   **Clarity & Precision:** All communications, definitions, and especially prompts for the Executing LLM, must be unambiguous.
*   **Iterative Refinement:** Solutions are developed through cycles of drafting, review, and feedback.
*   **Consensus-Driven:** Decisions on technical approaches and standard content aim for agreement between Jim and Jack, with Ehsan facilitating and providing final approval.
*   **Documented Decisions:** Key decisions, clarifications, and rationale are captured in "text-blocks" for Ehsan to save in roadmap-progress.md to maintain a project memory.

## 4. Understanding Project Documentation

The project relies on a suite of interconnected documents. Understanding their purpose and interrelations is key:

*   **Core Architectural Documents:**
    *   `Standards Categorization Scheme.md`: Defines the high-level organization of all standards.
    *   `Single-Source Multi-View Standards Architecture.md`: Explains the model of atomic source files and derived views.
*   **Planning & Tracking Documents:**
    *   `Refactor Roadmap.md`: Outlines the overall plan, phases, steps, and tasks.
    *   `roadmap-progress.md`: Tracks major pending tasks, issues, and records finalized decisions and progress.
*   **Interaction Logs & Q&A:**
    *   `end-of-session-summary.md` and `roadmap-progress.md` (if available): Records of session summaries, finalized decisions, clarifications, and progress that shape project decisions. These are vital for understanding the "why" behind certain choices.

**Reading Strategy:**
1.  **Context First:** Start with this `Project Collaboration & Onboarding Guide`, then the `Refactor Roadmap.md`, `Standards Categorization Scheme.md`, and `Single-Source Multi-View Standards Architecture.md`.
2.  **Review Session Summaries & Progress:** For historical context or clarification on past decisions, review `end-of-session-summary.md` and `roadmap-progress.md` (if available).
3.  **Examine Frontmatter:** The YAML frontmatter of every document provides crucial metadata (version, status, primary topic).

## 5. Getting Started / Re-engaging with Work

Whether you are new to the project or returning after some time, follow these steps to get up to speed:

1.  **Read this Guide:** Thoroughly read and understand this `Project Collaboration & Onboarding Guide.md`.
2.  **Review Core Architecture & Roadmap:**
    *   Familiarize yourself with the `Standards Categorization Scheme.md` and `Single-Source Multi-View Standards Architecture.md`.
    *   Read the main `Refactor Roadmap.md` to understand the overall project lifecycle.
3.  **Understand the Current Phase:**
    *   Identify the currently active phase by consulting with Ehsan or checking the latest project updates.
4.  **Catch Up on Recent Decisions:**
    *   Review the most recent entries in `end-of-session-summary.md` and `roadmap-progress.md` (if available) to understand the latest discussions, clarifications, and decisions.
5.  **Identify Current Tasks:**
    *   Ehsan will assign or relay specific tasks based on the current phase and priorities.
6.  **Locate Relevant Documentation:**
    *   Use the project's directory structure (outlined in this guide and the roadmap) to find relevant standards, registries, or templates.
    *   Once available, the `standards_index.json` will be a key tool for locating specific standards by ID or keyword.
7.  **Ask Clarifying Questions:**
    *   If any aspect of the project, current tasks, or documentation is unclear, proactively seek clarification from Ehsan, who will facilitate discussions with Jim and/or Jack as needed.

## 6. Conclusion

This project's success hinges on meticulous planning, clear communication, and consistent adherence to our defined processes and standards. By following this guide, all team members can contribute effectively towards our shared goal of creating a robust, maintainable, and highly functional standards ecosystem.

---

> **IMPORTANT:**  
> At the end of each session, **Jim** will produce a summary of what happened in the session and specify where the next session should begin. **Jack** will then review this summary and either approve it or propose additions/modifications as needed. Ehsan will save the summary in `end-of-session-summary.md`

---

**End of integrated changes.**