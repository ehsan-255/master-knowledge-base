---

title: 'Standard: Markdown Utilities Syntax'
standard_id: SF-UTILITIES-MARKDOWN
aliases:
- Markdown Utilities
- Key References and Escaping
- TODO Comments
- Utility Syntax
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p2-medium
- kb-id/standards
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Markdown Utilities Syntax
related-standards:
- SF-SYNTAX-MARKDOWN-TEXT
- SF-SYNTAX-MARKDOWN-STRUCTURED
- MT-KEYREF-MANAGEMENT
version: 1.0.0
date-created: '2025-06-18T03:00:00Z'
date-modified: '2025-06-18T03:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines utility Markdown syntax for key references, character escaping, and TODO comments.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Key references
- Character handling
- Task tracking
- Content maintenance
---
# Standard: Markdown Utilities Syntax (SF-UTILITIES-MARKDOWN)

## 1. Standard Statement

This standard **MANDATES** utility Markdown syntax for key-based referencing, character escaping, and TODO comments. This consolidated standard ensures universal consistency for utility functions across the Knowledge Base.

## 2. Key Reference Syntax

### Rule 2.1: Placeholder Format
Keyref placeholders **MUST** use double curly braces `{{ }}` enclosing the mandatory prefix `key.` followed by the key name.
*   **Mandatory Syntax:** `{{key.yourKeyName}}`
*   **Example:** `{{key.officialCompanyName}}`

### Rule 2.2: Key Naming Convention
Key names **MUST** follow camelCase convention. The source of truth for key names is [[UA-KEYDEFS-GLOBAL]].
*   **Example:** `{{key.projectStartDate}}`

### Rule 2.3: No Whitespace
Whitespace within the curly braces is **PROHIBITED**.
*   **Correct:** `{{key.yourKeyName}}`
*   **Prohibited:** `{{ key.yourKeyName }}`, `{{key. yourKeyName}}`

## 3. Character Escaping Syntax

### Rule 3.1: Backslash Escaping
To display special Markdown characters literally, a backslash (`\`) **MUST** be placed immediately before the character.
*   **Syntax:** `\CharacterToEscape`
*   **Example:** `\*` displays a literal asterisk

### Rule 3.2: Common Escapable Characters
The following characters **MAY** require escaping when intended for literal display:
*   `\` (Backslash: `\\`)
*   `` ` `` (Backtick: `` \` ``)
*   `*` (Asterisk: `\*`)
*   `_` (Underscore: `\_`)
*   `{ }` (Curly braces: `\{` and `\}`)
*   `[ ]` (Square brackets: `\[` and `\]`)
*   `( )` (Parentheses: `\(` and `\)`)
*   `#` (Hash: `\#` at start of line)
*   `+` `-` `.` (List markers: `\+`, `\-`, `1\.`)
*   `!` (Exclamation: `\!` before `[`)

### Rule 3.3: Escaping Examples
*   **Literal asterisks:** `\*not italic\*` displays: \*not italic\*
*   **Literal hash:** `\#not a heading` displays: \#not a heading
*   **Literal numbering:** `1\. not a list` displays: 1\. not a list

## 4. TODO Comment Syntax

### Rule 4.1: HTML Comment Delimiters
TODO items **MUST** be enclosed within HTML comment delimiters: `<!--` and `-->`.
*   **Basic Syntax:** `<!-- TODO: description -->`

### Rule 4.2: TODO Keyword
Comments **MUST** begin with uppercase `TODO:` immediately following the opening delimiter.
*   **Example:** `<!-- TODO: Review this section -->`

### Rule 4.3: Date Format (Optional)
If included, dates **MUST** be formatted as `YYYY-MM-DD` immediately after `TODO:`.
*   **Example:** `<!-- TODO: 2024-05-30 Update statistics -->`

### Rule 4.4: Assignee Format (Optional)
Assignees **MUST** use `@username` format if specified.
*   **Example:** `<!-- TODO: 2024-05-30 @teamlead: Verify accuracy -->`

### Rule 4.5: TODO Placement
HTML comment TODOs **MUST** be placed on their own line between content blocks.
*   **Example:**
    ```markdown
    This is a paragraph.

    <!-- TODO: 2024-05-30 @reviewer: Add diagram here -->

    This is another paragraph.
    ```

### Rule 4.6: Multi-line TODOs
Multi-line descriptions are **PERMITTED**, but `TODO:`, date, and assignee **MUST** be on the first line.
*   **Example:**
    ```markdown
    <!-- TODO: 2024-05-30 @team
    Review this section for accuracy.
    Add more examples for clarity.
    -->
    ```

## 5. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository. Adherence is **MANDATORY** for all content creators, automated systems, and tooling.

## 6. Cross-References
*   [[SF-SYNTAX-MARKDOWN-TEXT]]
*   [[SF-SYNTAX-MARKDOWN-STRUCTURED]]
*   [[MT-KEYREF-MANAGEMENT]]
*   [[UA-KEYDEFS-GLOBAL]]
*   [[CS-POLICY-TONE-LANGUAGE]]

---
*This standard (SF-UTILITIES-MARKDOWN) consolidates utility Markdown syntax into a comprehensive standard, ensuring universal consistency for the Knowledge Base.* 