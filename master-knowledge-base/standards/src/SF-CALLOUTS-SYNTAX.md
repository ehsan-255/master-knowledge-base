---
title: "Standard: Callout and Admonition Syntax"
standard_id: "SF-CALLOUTS-SYNTAX"
aliases: ["Callouts", "Admonitions", "Alert Boxes"]
tags:
  - status/draft
  - criticality/p2-medium
  - content-type/technical-standard
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "Callout and Admonition Syntax"
related-standards: []
version: '1.0.0'
date-created: "2025-05-29T13:24:53Z"
date-modified: "2025-05-30T18:00:00Z"
primary_domain: "SF"
sub_domain: "CALLOUTS"
scope_application: "Defines the syntax and usage rules for callouts, admonitions, and alert boxes in knowledge base documents."
criticality: "P2-Medium"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Content presentation", "User attention", "Information hierarchy"]
change_log_url: "./SF-CALLOUTS-SYNTAX-changelog.md"
---
# Standard: Callout/Admonition Block Syntax (SF-CALLOUTS-SYNTAX)

## 1. Standard Statement

This standard defines a generalized Markdown syntax for creating callout or admonition blocks. These blocks are used to highlight specific types of information, such as notes, warnings, tips, or examples, setting them apart from the main narrative flow. The syntax builds upon the standard Markdown blockquote format.

While this standard defines the *syntax*, the policy governing *when and how to use* specific callout types is defined in [[CS-ADMONITIONS-POLICY]]. Adherence to [[SF-FORMATTING-FILE-HYGIENE]] regarding blank lines around block elements is also important.

## 2. Core Callout Syntax Rule

### Rule 2.1: Callout Block Structure
Callout/admonition blocks MUST be constructed as an extension of the standard Markdown blockquote syntax.
*   **Syntax:**
    ```markdown
    > [!TYPE] Optional Title
    > Callout content goes here.
    > It can span multiple lines.
    >
    > - And can include other Markdown elements like lists,
    > - provided they are correctly indented within the blockquote.
    ```
*   **Components:**
    1.  **Blockquote Marker (`>`):** Each line of the callout block MUST begin with the blockquote marker (`>`) followed by a space, as defined in [[SF-SYNTAX-BLOCKQUOTES]].
    2.  **Type Specifier (`[!TYPE]`):** The first line of the callout block, immediately after the `> `, MUST contain a type specifier enclosed in square brackets and prefixed with an exclamation mark: `[!TYPE]`.
        *   **`TYPE`**: A keyword indicating the nature of the callout. This keyword MUST be uppercase. See "Recommended `TYPE` Keywords" below.
    3.  **Optional Title:** An optional title for the callout MAY follow the `[!TYPE]` specifier on the same line, separated by a space.
    4.  **Content:** The content of the callout begins on the line immediately following the type specifier line, or on the same line after the optional title if space permits and is readable. All content lines MUST also be prefixed with `> `.
*   **Blank Lines:** A blank line MUST precede and follow the entire callout block.

### Rule 2.2: Recommended `TYPE` Keywords
The following uppercase keywords ARE recommended for the `[!TYPE]` specifier to ensure consistency and semantic meaning. Their specific usage is governed by [[CS-ADMONITIONS-POLICY]].

*   **`NOTE`**: For general supplementary information or side comments.
*   **`IMPORTANT`**: For information that users must not overlook.
*   **`WARNING`**: For potential dangers, pitfalls, or critical cautionary advice.
*   **`TIP`**: For helpful hints, suggestions, or best practices.
*   **`QUESTION`**: For posing questions related to the content, or for FAQs. (Also `FAQ`)
*   **`ERROR`**: For highlighting error messages or incorrect outcomes.
*   **`SUCCESS`**: For indicating successful outcomes or positive confirmations. (Also `INFO`, `HELP`)
*   **`EXAMPLE`**: For designating examples. (Also `DEMO`)
*   **`QUOTE`**: For text quoted from external sources, distinct from a standard blockquote if specific styling is desired.
*   **`ABSTRACT`**: For summaries or abstracts at the beginning of a section. (Also `SUMMARY`, `TLDR`)
*   **`TODO`**: For highlighting to-do items or pending tasks within the document (primarily for editorial/authoring purposes, may be stripped in final output).
*   **`IF`**: For conditional text presentation logic (if supported by tooling, this indicates a block whose rendering may depend on certain conditions).

*   **Extensibility:** While these are recommended, specific projects or KBs MAY define additional custom types if necessary, but these MUST be documented in a local supplement to [[CS-ADMONITIONS-POLICY]]. Over-proliferation of types is discouraged.

## 3. Illustrative Examples

### Example 3.1: Note with Title
```markdown
> [!NOTE] Important Considerations
> This is a note with a title.
> It provides supplementary information that readers might find useful.
```

### Example 3.2: Warning without Title
```markdown
> [!WARNING]
> Proceed with caution. Incorrect configuration can lead to data loss.
```

### Example 3.3: Tip with Multi-line Content
```markdown
> [!TIP]
> To improve performance, consider the following:
> - Index your database tables.
> - Use a caching layer for frequently accessed data.
```

### Example 3.4: TODO item
```markdown
> [!TODO]
> - Finalize the examples for Section 4.
> - Get review from SME on accuracy of definitions.
```

## 4. Rendering and Tooling Dependency

The visual appearance (e.g., color, icon) of callout/admonition blocks is determined by the CSS and JavaScript of the Markdown rendering environment (e.g., static site generator theme, authoring tool previewer).
*   **Semantic Intent:** This standard defines the syntax to convey the *semantic intent* of the callout.
*   **Fallback:** If a specific `[!TYPE]` is not recognized by a renderer, it SHOULD gracefully fall back to rendering as a standard Markdown blockquote. The `[!TYPE] Optional Title` line will still be visible as the first line of the blockquote.

## 5. Importance of Standardized Callout Syntax

*   **Semantic Highlighting:** Allows authors to give semantic meaning to certain blocks of text, indicating their special importance or nature.
*   **Improved Readability:** When rendered with distinct styling, callouts help break up text and draw attention to key information.
*   **Authoring Consistency:** Provides a uniform syntax for authors to create these highlighted blocks.
*   **Potential for Automation:** Standardized syntax can be targeted by automation tools for indexing, summarization, or conditional processing.

## 6. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where callout or admonition blocks are used to highlight information.

## 7. Cross-References
- [[CS-ADMONITIONS-POLICY]] - Policy on when and how to use specific callout types.
- [[SF-SYNTAX-BLOCKQUOTES]] - Defines the base blockquote syntax upon which callouts are built.
- [[SF-FORMATTING-FILE-HYGIENE]] - For rules on blank lines around block elements.

---
*This standard (SF-CALLOUTS-SYNTAX) generalizes the Obsidian callout syntax to provide a tool-agnostic method for declaring admonition blocks in Markdown, building upon standard blockquote syntax.*
