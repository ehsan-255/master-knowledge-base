---
title: 'Standard: Task Document Schema'
standard_id: AS-SCHEMA-TASK
aliases:
  - Schema for Task-Oriented Documents
  - Procedural Document Structure
  - How-To Guide Schema
tags:
  - status/draft
  - criticality/p1-high
  - content-type/schema-document
  - topic/schemas
  - topic/documentation-standards
  - topic/procedures
  - kb-id/standards
kb-id: standards
info-type: schema-document
primary-topic: Defines the standard structure and core elements for task-oriented
  documents, such as tutorials, how-to guides, and standard operating procedures (SOPs).
related-standards:
  - MT-SCHEMA-FRONTMATTER
  - AS-STRUCTURE-DOC-CHAPTER
  - SF-SYNTAX-HEADINGS
  - SF-SYNTAX-LISTS
version: 0.1.0
date-created: '2025-05-29T15:49:24Z'
date-modified: '2025-05-30T16:00:00Z'
primary_domain: AS
sub_domain: SCHEMA
scope_application: Applies to all documents designed to guide users through a sequence
  of steps to achieve a specific outcome.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Procedural consistency
  - User training
  - Operational efficiency
  - Task success rates
change_log_url: ./changelog.md
---
# Standard: Task Document Schema (AS-SCHEMA-TASK)

## 1. Standard Statement

This standard defines the mandatory and recommended structure for creating **Task-Oriented Documents**. These documents guide users through a sequence of steps to achieve a specific goal. Examples include tutorials, how-to guides, standard operating procedures (SOPs), troubleshooting procedures, and installation instructions.

Adherence to this schema ensures that task documentation is clear, actionable, consistent, and easy for users to follow, leading to higher success rates and reduced errors. This schema builds upon the general document structure defined in `[[AS-STRUCTURE-DOC-CHAPTER]]`.

## 2. Purpose of Task Documents

Task documents are instructional. Users consult them to:
-   Understand how to perform a specific operation or procedure.
-   Learn the steps required to achieve a desired outcome.
-   Troubleshoot issues by following a defined process.
-   Ensure compliance with standard procedures.

They are distinct from reference documents (which describe *what* something is) or conceptual guides (which explain *why* something is).

## 3. Core Structure of a Task Document

A task document, after the standard frontmatter and H1 title (which should clearly state the task, e.g., "How to Install the Foobar Application" or "Procedure for Monthly Server Maintenance"), MUST generally follow this sequence of H2 sections. Some sections are optional depending on the complexity and nature of the task.

### 3.1. Goal / Purpose (Mandatory)
   - **Heading:** `## Goal`, `## Purpose`, or `## Objective`
   - **Content:** Clearly state the overall goal or desired outcome of completing the task (1-2 sentences). Briefly explain why this task is performed.

### 3.2. Prerequisites (Conditional - Recommended if applicable)
   - **Heading:** `## Prerequisites`
   - **Content:** List any conditions that must be met, skills required, or configurations needed before starting the task.
     - Use a bulleted or numbered list.
     - Example: "User must have administrator privileges," "Software version X.Y.Z must be installed," "[[AS-SCHEMA-CONCEPT-DEFINITION]] on Topic Z must be understood."

### 3.3. Materials / Tools / Software Required (Conditional - Recommended if applicable)
   - **Heading:** `## Materials Required`, `## Tools Needed`, or `## Software Requirements`
   - **Content:** List any specific hardware, software, tools, parts, or information needed to perform the task.
     - Use a bulleted list.
     - Specify versions if important.

### 3.4. Safety Warnings / Important Notices (Conditional - Highly Recommended if applicable)
   - **Heading:** `## Safety Warnings`, `## Important Notices`, or `## Caution`
   - **Content:** Highlight any potential risks, safety precautions, data loss warnings, or critical information the user MUST be aware of before proceeding.
     - Use callouts (e.g., `[!WARNING]`, `[!CAUTION]`) for emphasis, as defined in `[[SF-CALLOUTS-SYNTAX]]`.

### 3.5. Steps / Procedure (Mandatory)
   - **Heading:** `## Steps`, `## Procedure`, or `## Instructions`
   - **Content:** The core of the document. Present the actions in a clear, sequential order.
     - **Numbered Lists:** Steps MUST be presented as a numbered list (see `[[SF-SYNTAX-LISTS]]`).
     - **Action-Oriented:** Start each step with a clear action verb (e.g., "Open," "Navigate," "Enter," "Verify").
     - **Granularity:** Break down complex actions into manageable sub-steps (nested numbered or bulleted lists).
     - **Clarity:** Each step should be unambiguous and concise.
     - **Conditional Steps:** Clearly indicate if a step is optional or depends on a previous choice (e.g., "If you selected Option A in Step 3, proceed to Step 4a; otherwise, skip to Step 5.").
     - **User Interface Elements:** Use bold text or backticks for UI elements like button names (`**Save**`), menu items (`File > Open`), or field labels (``Username``).
     - **Screenshots/Diagrams:** Optionally include screenshots or diagrams (see `[[SF-SYNTAX-IMAGES]]` and `[[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]`) after a step if they significantly aid understanding. They should supplement, not replace, clear textual instructions.

### 3.6. Expected Results / Verification (Highly Recommended)
   - **Heading:** `## Expected Results` or `## Verification`
   - **Content:** Describe what the user should observe or be able to do after completing the steps, or a specific sub-set of steps.
     - This helps users confirm they have performed the task correctly.
     - Example: "The system will display a 'Configuration Saved Successfully' message." or "You should now be able to log in to the application."

### 3.7. Troubleshooting / Common Issues (Conditional - Recommended for complex tasks)
   - **Heading:** `## Troubleshooting` or `## Common Issues`
   - **Content:** List potential problems users might encounter, their causes, and solutions.
     - Use a problem/solution format, perhaps with bullet points or sub-headings.

### 3.8. Conclusion / Next Steps (Optional)
   - **Heading:** `## Conclusion` or `## Next Steps`
   - **Content:** Briefly summarize what was achieved. If applicable, suggest what the user might do next or point to related tasks or information.

### 3.9. See Also (Optional)
   - **Heading:** `## See Also`
   - **Content:** Links to related reference documents, conceptual guides, or other relevant tasks.

## 4. General Guidelines
- **Audience Focus:** Write for the intended audience, considering their technical proficiency.
- **Testing:** Whenever possible, procedures should be tested by someone other than the author to ensure clarity and accuracy.
- **Consistency:** Use consistent terminology, formatting, and level of detail across all task documents.
- **Modularity:** If a task is very long or has distinct sub-tasks that can be performed independently, consider breaking it into multiple, linked task documents.

## 5. Scope of Application
This schema applies to all documents that provide step-by-step instructions for users to achieve a specific outcome. This includes, but is not limited to, software installation guides, configuration procedures, user manual tasks, troubleshooting guides, and standard operating procedures.
