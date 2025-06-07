---
title: 'Standard: HTML Comment Syntax for TODO Items'
standard_id: SF-SYNTAX-COMMENT-TODO
aliases:
  - TODO Comment Syntax
  - HTML TODO Standard
tags:
  - status/draft
  - content-type/standard-definition
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
date-modified: '2025-05-30T12:00:00Z'
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
---
# Standard: HTML Comment Syntax for TODO Items (SF-SYNTAX-COMMENT-TODO)

This document defines the standard HTML comment-based syntax for marking "TODO" items or pending actions directly within content documents. This method ensures TODOs are visible in the raw source and are machine-parseable but do not render in standard Markdown views.

## 2. Core Syntax Rules

### Rule 2.1: HTML Comment Delimiters
TODO items using this syntax MUST be enclosed within standard HTML comment delimiters: `<!--` and `-->`.
*   **Rationale:** Ensures the content does not render in standard Markdown or HTML views.

### Rule 2.2: TODO Keyword
The comment MUST begin with the uppercase keyword `TODO:` immediately following the opening comment delimiter `<!--`.
*   **Syntax:** `<!-- TODO: ... -->`
*   **Rationale:** Provides a clear, machine-parseable identifier for TODO items.

### Rule 2.3: Date of Creation (Optional but Recommended)
If a date is included, it SHOULD represent the date the TODO was created or last significantly updated, formatted as `YYYY-MM-DD`. This date SHOULD appear immediately after `TODO:`.
*   **Syntax:** `<!-- TODO: YYYY-MM-DD ... -->`
*   **Example:** `<!-- TODO: 2024-05-30 ... -->`
*   **Rationale:** Helps in tracking the age and relevance of TODO items.

### Rule 2.4: Assignee (Optional)
An assignee for the TODO item MAY be specified using an `@username` format. If included, it SHOULD follow the date (if present) or the `TODO:` keyword.
*   **Syntax (with date):** `<!-- TODO: YYYY-MM-DD @username ... -->`
*   **Syntax (without date):** `<!-- TODO: @username ... -->`
*   **Example:** `<!-- TODO: 2024-05-30 @generalteam: Review this section -->`
*   **Rationale:** Allows for clear assignment of responsibility for addressing the TODO item.

### Rule 2.5: Description
A clear and concise description of the task or pending action MUST follow the keyword, date (if any), and assignee (if any).
*   **Syntax:** `<!-- TODO: [YYYY-MM-DD] [@username] Description of the task. -->`
*   **Example:** `<!-- TODO: 2024-06-15 @jdoe: Verify the accuracy of the statistics in this section. -->`
*   **Rationale:** Provides necessary context for anyone addressing the TODO item.

### Rule 2.6: Placement
HTML comment TODOs can be placed inline within text (though they will still be on their own line in raw Markdown for the comment structure) or on their own line between blocks of text.
*   **Guidance:** For longer TODO descriptions or multiple TODOs, placing them on separate lines between paragraphs or other content blocks is recommended for raw text readability.
*   **Example (between paragraphs):**
    ```markdown
    This is a paragraph.

    <!-- TODO: 2024-05-30 @team: Add a diagram to illustrate this concept. -->

    This is another paragraph.
    ```
*   **Rationale:** Flexible placement allows authors to associate TODOs with specific content areas.

### Rule 2.7: Multi-line Descriptions
The description part of the TODO item can span multiple lines within the HTML comment block. However, the `TODO:`, date, and assignee (if present) should ideally be on the first line for easier parsing.
*   **Example:**
    ```markdown
    <!-- TODO: 2024-05-30 @feedback_crew
    Review this entire section for clarity and technical accuracy.
    Ensure it aligns with the latest product updates released in Q2.
    Consider adding more examples for novice users.
    -->
    ```
*   **Rationale:** Allows for more detailed TODO descriptions when necessary.

## 3. Importance of Standardized HTML Comment TODOs

*   **Non-Rendering:** Ensures that TODO items do not appear in the final published or rendered output, keeping the content clean for consumers.
*   **Machine-Parseable:** The consistent `<!-- TODO: ... -->` format allows scripts or tools to easily find, extract, and report on all TODO items across the knowledge base.
*   **Source Visibility:** TODOs are clearly visible to authors and editors when viewing the raw Markdown source.
*   **Task Tracking:** Facilitates tracking of pending work, assignments, and deadlines directly within the content.
*   **Content Maintenance:** Aids in identifying areas that require updates, verification, or further development.

## 4. Alternative (Visible) TODOs

For TODO items that *should* be visible in the rendered output (e.g., as a note to readers that a section is incomplete), the callout syntax defined in [[SF-CALLOUTS-SYNTAX]] (e.g., `> [!TODO] This section is under construction.`) SHOULD be used instead. This standard (SF-SYNTAX-COMMENT-TODO) is specifically for non-rendering, source-visible TODOs.

## 5. Cross-References
- [[SF-CALLOUTS-SYNTAX]] - For the syntax of visible `[!TODO]` callouts.
- [[UA-KEYDEFS-GLOBAL]] - (Potentially) for defining standard assignee usernames if a controlled list is desired.

---
*This standard (SF-SYNTAX-COMMENT-TODO) is based on rules 1.1 through 1.7 previously defined in M-SYNTAX-TODO-001 from COL-SYNTAX-MARKDOWN.md, focusing on the HTML comment syntax for TODOs.*
