---
title: 'Standard: Markdown Syntax for Conditional Text (M-CONDITIONAL-TEXT-SYNTAX-001) - DEPRECATED'
tags:
- content-profiling
- content-type/standard-document
- kb-id/standards
- standards-kb/markdown
- status/deprecated
- syntax-rules
date-created: 2025-05-19
date-modified: '2025-06-02T00:39:05Z'
version: 0.2.0
info-type: standard-document
primary-topic: Defines the Markdown syntax for marking conditional text blocks.
related-standards:
- U-PROFILING-ATTRIBUTES-001
- O-USAGE-CALLOUTS-001
aliases:
- Conditional Text Syntax
- Profiling Markdown Syntax
---
**DEPRECATED:** This document is superseded. Superseded by [[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]] and [[CS-CONTENT-PROFILING-POLICY]].

# Standard: Markdown Syntax for Conditional Text (M-CONDITIONAL-TEXT-SYNTAX-001)

This document defines the standard Markdown syntax for marking blocks of text as conditional, intended for content profiling and selective publishing.

## Table of Contents
- [[#Standard: Conditional Text Block Syntax (M-CONDITIONAL-TEXT-SYNTAX-001)]]

## Standard: Conditional Text Block Syntax (M-CONDITIONAL-TEXT-SYNTAX-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `M-CONDITIONAL-TEXT-SYNTAX-001`       |
| Standard Name   | Conditional Text Block Syntax         |
| Standard Category | Markdown Syntax Conventions           |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Conditional text blocks MUST be implemented using Obsidian-style callouts with a specific `[!IF ...]` type. The condition MUST follow the `IF` keyword. | `> [!IF audience=expert]`                                    | Leverages existing callout syntax for easy visual distinction and parsing.   |
| 1.2    | The condition within `[!IF ...]` MUST consist of `attribute=value` pairs. Multiple conditions can be combined using `AND` (case-insensitive). `OR` logic is NOT directly supported in a single `IF` block; use separate blocks. | `> [!IF platform=windows AND audience=admin]`<br/>`> [!IF feature=beta]` | Attributes and values are defined in `U-PROFILING-ATTRIBUTES-001`.           |
| 1.3    | The attribute name and value in the condition MUST NOT contain spaces. Values SHOULD be kebab-case if multi-word.                               | `audience=expert-user` (Correct)<br/>`platform = windows` (Incorrect due to spaces around `=`) | Ensures simple parsing.                                                      |
| 1.4    | The content conditional upon the `IF` statement MUST be indented under the callout, following standard callout content rules.                   | `> [!IF audience=expert]\n> This is expert content.`         | Standard Markdown callout behavior.                                          |
| 1.5    | Conditional blocks can span multiple paragraphs, lists, or other Markdown elements, as long as each line of the conditional content starts with the callout marker `> `. | See Illustrative Example.                                    |                                                                              |
| 1.6    | A blank line SHOULD precede and follow a conditional block for readability, unless it's immediately followed by another related conditional block. | N/A                                                          | Improves visual separation.                                                  |

**Illustrative Examples (Overall):**

```markdown
General introduction text.

> [!IF audience=expert AND platform=linux]
> This section provides advanced troubleshooting tips for Linux experts.
> - Check kernel logs using `dmesg`.
> - Ensure all dependencies are met via `ldd`.

> [!IF audience=novice]
> For beginners, please ensure the application is installed correctly by following the setup wizard.

General concluding text.
```

**Cross-References to Other Standard IDs:** [[../../_backup/master-knowledge-base-backup/standards/U-PROFILING-ATTRIBUTES-001|U-PROFILING-ATTRIBUTES-001]], [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Callout Usage (O-USAGE-CALLOUTS-001)|O-USAGE-CALLOUTS-001]] 