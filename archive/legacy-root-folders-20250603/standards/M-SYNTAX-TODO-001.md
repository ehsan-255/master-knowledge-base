---
title: 'Standard: Markdown Syntax for TODO Items (M-SYNTAX-TODO-001) - DEPRECATED'
tags:
- content-type/standard-document
- criticality/p0-critical
- kb-id/global
- kb-id/standards
- standards-kb/markdown
- status/deprecated
- syntax-rules
- utility-standards
date-created: 2025-05-19
date-modified: '2025-06-17T02:29:13Z'
version: 0.2.0
info-type: standard-document
primary-topic: Defines the Markdown syntax for marking TODO items within documents.
related-standards:
- O-USAGE-CALLOUTS-001
aliases:
- TODO Syntax
- Task Tracking Markdown
kb-id: archive
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: [[SF-SYNTAX-TODO]].

# Standard: Markdown Syntax for TODO Items (M-SYNTAX-TODO-001)

This document defines the standard Markdown syntax for marking "TODO" items or pending actions directly within content documents. This allows for discoverable and consistently formatted action items.

## Table of Contents
- [[#Standard: TODO Item Syntax (M-SYNTAX-TODO-001)]]

## Standard: TODO Item Syntax (M-SYNTAX-TODO-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-SYNTAX-TODO-001`                   |
| Standard Name   | TODO Item Syntax                      |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | TODO items MUST be formatted as HTML comments to prevent rendering in standard Markdown views, while remaining machine-parseable and visible in the raw source. | `<!-- TODO [YYYY-MM-DD Assignee/System]: Description of the task. -->` | Ensures TODOs don't clutter published output but are clear in source.        |
| 1.2    | The TODO comment MUST start with `TODO`. This keyword is case-sensitive.                                                                        | `<!-- TODO ... -->`                                          | Allows for easy searching (`grep`, etc.).                                    |
| 1.3    | The TODO comment SHOULD include the date of creation in `YYYY-MM-DD` format, enclosed in square brackets.                                        | `<!-- TODO [2025-05-19 ...]: ... -->`                        | Helps track age of TODO items.                                               |
| 1.4    | The TODO comment SHOULD include an assignee (username, team name, or "System" for automated tasks) after the date, separated by a space, still within the square brackets. | `<!-- TODO [2025-05-19 Ehsan]: Review this section. -->`     | Clarifies responsibility.                                                    |
| 1.5    | A colon (`:`) MUST follow the closing square bracket `]` and precede the descriptive text of the TODO item.                                     | `<!-- TODO [...]: Actual task description. -->`              | Standard delimiter.                                                          |
| 1.6    | The description of the TODO item SHOULD be concise yet clear enough to understand the pending action.                                           | `<!-- TODO [2025-05-20 Jim]: Verify all links in See Also. -->` | Actionable description.                                                      |
| 1.7    | TODO items SHOULD be placed on their own line or immediately preceding/following the content block they refer to.                               | N/A                                                          | Contextual placement.                                                        |
| 1.8    | (Alternative/Obsidian-Specific) For TODOs that should be visually distinct *within Obsidian*, an Obsidian `[!TODO]` callout MAY be used IN ADDITION TO or INSTEAD OF the HTML comment for high-visibility items. If used instead, scripts searching for TODOs must also parse this callout format. | `> [!TODO] Review Section X\n> Details about what needs review.` | This is an Obsidian-specific rendering. The HTML comment is more portable for scripts. Choose one primary method for scripting. |

**Illustrative Examples (Overall):**

Standard HTML Comment TODO:
```markdown
Some paragraph text.
<!-- TODO [2025-05-21 UserX]: Expand this section with more examples. -->
Another paragraph.
```

Obsidian Callout TODO (if chosen as an alternative or supplement):
```markdown
> [!TODO] Update Statistics
> The statistics in this table need to be refreshed with Q2 data.
> Assigned: UserY, Due: 2025-06-15
```
*(Note: If using callouts for scripted TODO tracking, the script needs to parse this specific callout format.)*

**Cross-References to Other Standard IDs:** [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Callout Usage (O-USAGE-CALLOUTS-001)|O-USAGE-CALLOUTS-001]] (if using callout alternative).
