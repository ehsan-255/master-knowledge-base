---
title: 'Standard: HTML Comment Syntax for TODO Items'
standard_id: SF-SYNTAX-COMMENT-TODO
aliases:
- TODO Comment Syntax
- HTML TODO Standard
tags:
- content-type/standard-definition
- criticality/p3-low
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
- topic/syntax
- topic/task-management
kb-id: standards
info-type: standard-definition
primary-topic: Defines the standard HTML comment syntax for embedding machine-parseable
  TODO items within Markdown documents that do not render in typical views.
related-standards:
- SF-CALLOUTS-SYNTAX
version: 1.0.0
date-created: '2025-05-30T00:00:00Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Applies to all knowledge base documents where non-rendering, machine-parseable
  TODO items are embedded.
criticality: P3-Low
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Task tracking
- Authoring workflow
- Automated reporting
- Content maintenance
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: HTML Comment Syntax for TODO Items (SF-SYNTAX-COMMENT-TODO)

## 1. Standard Statement

This standard **MANDATES** the exclusive HTML comment-based syntax for marking "TODO" items or pending actions directly within content documents. This method **MUST** ensure TODOs are visible in the raw source and are machine-parseable but do not render in standard Markdown views.

## 2. Core Syntax Rules

### Rule 2.1: HTML Comment Delimiters
TODO items using this syntax **MUST** be enclosed within standard HTML comment delimiters: `<!--` and `-->`.
*   **Rationale:** Ensures content does not render in standard Markdown or HTML views.

### Rule 2.2: TODO Keyword
The comment **MUST** begin with the uppercase keyword `TODO:` immediately following the opening comment delimiter `<!--`.
*   **Syntax:** `<!-- TODO: ... -->`
*   **Rationale:** Provides a clear, machine-parseable identifier for TODO items.

### Rule 2.3: Date of Creation
If a date is included, it **MUST** represent the date the TODO was created or last significantly updated, formatted as `YYYY-MM-DD`. This date **MUST** appear immediately after `TODO:`.
*   **Syntax:** `<!-- TODO: YYYY-MM-DD ... -->`
*   **Example:** `<!-- TODO: 2024-05-30 ... -->`
*   **Rationale:** Helps in tracking the age and relevance of TODO items.

### Rule 2.4: Assignee
An assignee for the TODO item **MUST** be specified using an `@username` format if assigned. If included, it **MUST** follow the date (if present) or the `TODO:` keyword.
*   **Syntax (with date):** `<!-- TODO: YYYY-MM-DD @username ... -->`
*   **Syntax (without date):** `<!-- TODO: @username ... -->`
*   **Example:** `<!-- TODO: 2024-05-30 @generalteam: Review this section -->`
*   **Rationale:** Allows for clear assignment of responsibility.

### Rule 2.5: Description
A clear and concise description of the task or pending action **MUST** follow the keyword, date (if any), and assignee (if any).
*   **Syntax:** `<!-- TODO: [YYYY-MM-DD] [@username] Description of the task. -->`
*   **Example:** `<!-- TODO: 2024-06-15 @jdoe: Verify the accuracy of the statistics in this section. -->`
*   **Rationale:** Provides necessary context for addressing the TODO item.

### Rule 2.6: Placement
HTML comment TODOs **MUST** be placed on their own line between blocks of text for readability in raw Markdown. Inline placement is **PROHIBITED**.
*   **Example:**
    ```markdown
    This is a paragraph.

    <!-- TODO: 2024-05-30 @team: Add a diagram to illustrate this concept. -->

    This is another paragraph.
    ```
*   **Rationale:** Ensures clear association of TODOs with specific content areas and maintains raw text readability.

### Rule 2.7: Multi-line Descriptions
The description part of the TODO item **MAY** span multiple lines within the HTML comment block. However, the `TODO:`, date, and assignee (if present) **MUST** be on the first line for easier parsing.
*   **Example:**
    ```markdown
    <!-- TODO: 2024-05-30 @feedback_crew
    Review this entire section for clarity and technical accuracy.
    Ensure it aligns with the latest product updates released in Q2.
    Consider adding more examples for novice users.
    -->
    ```
*   **Rationale:** Allows for more detailed TODO descriptions when necessary.

## 3. Importance of Strict HTML Comment TODOs

*   **Non-Rendering:** Ensures TODO items do not appear in final published output.
*   **Machine-Parseable:** Consistent format allows tools to find, extract, and report on TODOs.
*   **Source Visibility:** TODOs are clearly visible to authors/editors in raw Markdown.
*   **Task Tracking:** Facilitates tracking pending work, assignments, and deadlines.
*   **Content Maintenance:** Aids in identifying areas requiring updates or development.

## 4. Alternative (Visible) TODOs

For TODO items that **MUST** be visible in the rendered output (e.g., as a note to readers that a section is incomplete), the callout syntax defined in [[SF-CALLOUTS-SYNTAX]] (e.g., `> [!TODO] This section is under construction.`) **MUST** be used instead. This standard (SF-SYNTAX-COMMENT-TODO) is specifically for non-rendering, source-visible TODOs.

## 5. Cross-References
*   [[SF-CALLOUTS-SYNTAX]]
*   [[UA-KEYDEFS-GLOBAL]]

---
*This standard (SF-SYNTAX-COMMENT-TODO) has been revised to mandate a strict, singular syntax for non-rendering, machine-parseable TODO items within HTML comments, ensuring consistency and effective task tracking.*
