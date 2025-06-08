---
title: 'Standard: Content Schema for "Task Topics" (U-SCHEMA-TASK-001) - DEPRECATED'
tags:
- content-type/standard-document
- content-type/task-topic
- kb-id/standards
- schemas
- standards-kb/universal
- status/deprecated
date-created: '2025-05-19T00:00:00Z'
date-modified: '2025-06-02T05:51:59Z'
version: 0.2.0
info-type: standard-document
primary-topic: Defines the structure for step-by-step procedural task documents
related-standards:
- AS-SCHEMA-TASK
aliases:
- Task Topic Schema
- Procedural Content Schema
---
**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: [[AS-SCHEMA-TASK]].

> [!WARNING] DEPRECATED: This Standard is No Longer Active
> **Reason for Deprecation:** This standard has been superseded by [[AS-SCHEMA-TASK]].
> Please refer to the new standard for current guidelines. This document is retained for historical purposes only.

# Standard: Content Schema for "Task Topics" (U-SCHEMA-TASK-001)

This document details the universal standard schema for "Task Topics." Task topics provide step-by-step instructions to guide a user in accomplishing a specific goal. They are action-oriented and focus on "how-to."

## Table of Contents
- [[#Standard: Schema Definition for Task Topics (U-SCHEMA-TASK-001)]]
- [[#Core Sections]]
- [[#Optional Sections]]

## Standard: Schema Definition for Task Topics (U-SCHEMA-TASK-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-SCHEMA-TASK-001`                   |
| Standard Name   | Content Schema for "Task Topics"      |
| Standard Category | Content Templates & Schemas           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Documents classified with `content-type: task-topic` in their YAML frontmatter MUST adhere to this schema.                                      | File: `how-to-install-plugin.md` with `content-type: task-topic` | Ensures consistency for instructional content.                               |
| 1.2    | The H1 title MUST clearly state the task the user will accomplish, typically starting with a verb (e.g., "How to Install X," "Configuring Y," "Creating Z"). | `# How to Reset Your Password`                               | Action-oriented and clear.                                                   |
| 1.3    | An introductory abstract (per `U-STRUC-002`) MUST briefly state the purpose of the task and what the user will achieve by completing it.        | "This guide explains the steps to reset your forgotten password." | Sets user expectations.                                                      |
| 1.4    | A Table of Contents (per `U-STRUC-002`) MUST be included, linking to all H2 sections, especially "Prerequisites" and "Steps."                  | `- [[#Prerequisites]]\n- [[#Steps]]`                         | Essential for navigating task instructions.                                  |

## Core Sections

The following H2 sections are typically MANDATORY for a Task Topic:

-   **`## Prerequisites` (Optional but Highly Recommended)**
    *   Lists any conditions, tools, permissions, or prior knowledge required before starting the task.
    *   Use a bulleted list. If no prerequisites, state "None."
    *   Example: `- Administrator access required.\n- [[concepts/understanding-widgets|Understanding Widgets]] concept reviewed.`

-   **`## Steps`**
    *   This is the primary section containing the ordered, step-by-step instructions.
    *   Steps MUST be presented as an ordered list (`1.`, `2.`, etc.).
    *   Each step SHOULD begin with an action verb.
    *   Sub-steps or choices within a step MAY use nested ordered lists or bullet points.
    *   Screenshots or code blocks can be embedded within steps for clarity.
    *   Example:
        ```markdown
        ## Steps

        1.  **Navigate** to the Settings menu.
            *   From the main dashboard, click your profile icon.
            *   Select "Settings" from the dropdown.
        2.  **Locate** the "Security" section.
        3.  **Click** the "Reset Password" button.
            *   A confirmation dialog will appear.
        4.  **Enter** your new password in both fields.
            `YourNewPassword123!`
        5.  **Click** "Save Changes."
        ```

-   **`## Expected Result` / `## Verification` (Optional but Highly Recommended)**
    *   Describes what the user should see or be able to do after successfully completing the task.
    *   Helps the user confirm they performed the task correctly.
    *   Example: "Your password is now reset. You should be able to log in with the new credentials."

## Optional Sections

-   **`## Context` / `## Before You Begin`**: Provides broader context or important considerations not fitting into Prerequisites.
-   **`## Troubleshooting` / `## Common Issues`**: Addresses potential problems users might encounter and their solutions.
-   **`## Next Steps`**: Suggests related tasks or further actions the user might take.
-   **`## Summary`** (per `U-STRUC-002`)
-   **`## See Also`** (per `U-STRUC-002`)

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]], [[COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Methodology/Technique Descriptions" (U-SCHEMA-METHOD-001)|U-SCHEMA-METHOD-001]] 