---
title: "Standard: General Markdown Link Syntax"
standard_id: "SF-SYNTAX-LINKS-GENERAL"
aliases: ["Markdown Link Syntax", "External Links", "Relative Links"]
tags:
  - status/draft
  - criticality/P1-High # Correct link syntax is fundamental
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "General Markdown Link Syntax" # As per prompt
related-standards: ["SF-LINKS-INTERNAL-SYNTAX", "CS-LINKING-INTERNAL-POLICY", "AS-STRUCTURE-ASSET-ORGANIZATION"]
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "SYNTAX" # As per prompt
scope_application: "Defines the general Markdown syntax for creating external links and relative path internal links to non-standard documents or assets. Complements SF-LINKS-INTERNAL-SYNTAX for standard-to-standard linking."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Link integrity", "Readability", "Authoring consistency", "Interoperability with Markdown parsers"]
change_log_url: "./SF-SYNTAX-LINKS-GENERAL-changelog.md" # Placeholder
---

# Standard: General Markdown Link Syntax (SF-SYNTAX-LINKS-GENERAL)

## 1. Standard Statement

This standard defines the general Markdown syntax for creating hyperlinks, primarily focusing on external links and internal links using relative paths (e.g., to assets or non-standard documents). It complements [[SF-LINKS-INTERNAL-SYNTAX]], which specifically governs the `[[STANDARD_ID]]` syntax for linking between standard documents. Adherence to these syntactical rules is essential for link integrity, readability, and consistent parsing.

## 2. Core Link Syntax Rules

### Rule 2.1: External Links (Derived from M-SYNTAX-LINKS-001, Rule 1.2)
External links (links to resources outside the current knowledge base, typically on the internet) MUST use the standard Markdown inline link format: `[Link Display Text](URL)`.
*   **`Link Display Text`**: The human-readable text that will be displayed for the link. This text SHOULD be descriptive of the link's destination or purpose.
*   **`URL`**: The full Uniform Resource Locator (URL) for the external resource (e.g., `https://www.example.com/somepage.html`). URLs should generally include the scheme (e.g., `http://`, `https://`).
*   **Example:**
    ```markdown
    For more information, visit the [Official W3C Website](https://www.w3.org/).
    Refer to the [guidelines on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML).
    ```
*   **Rationale:** This is the universally recognized Markdown syntax for external links, ensuring maximum compatibility and understandability.

### Rule 2.2: Internal Links (Relative Paths for Non-Standard Documents/Assets) (Adapted from M-SYNTAX-LINKS-001, Rule 1.1)
Internal links to non-standard documents (e.g., supplementary materials not governed by a `standard_id`) or to assets (e.g., images, PDFs) within the knowledge base repository MUST use relative path Markdown inline link syntax: `[Link Display Text](./path/to/file.ext)` or `[Link Display Text](../path/to/file.ext)`.
*   **`Link Display Text`**: Descriptive text for the link.
*   **`./path/to/file.ext` or `../path/to/file.ext`**: The relative path from the current document to the target file.
*   **Example (Linking to an asset):**
    ```markdown
    See the [project overview diagram](./assets/images/project-overview.png).
    Download the [annual report](./assets/pdfs/annual-report-2023.pdf).
    ```
*   **Example (Linking to a non-standard supplementary document):**
    ```markdown
    Refer to the [detailed setup guide](./supplementary-docs/detailed-setup.md).
    ```
*   **Important Distinction for Standard Documents:** For linking *between standard documents* (i.e., documents that have a `standard_id`), the mandatory convention is `[[STANDARD_ID]]` as defined in [[SF-LINKS-INTERNAL-SYNTAX]]. The relative path method described here is NOT for linking standard documents to each other.
*   **Rationale:** Relative paths provide a robust way to link to local files within the repository structure, ensuring links remain valid as long as the relative positions of files are maintained.

### Rule 2.3: Prohibition of Reference-Style Links (Derived from M-SYNTAX-LINKS-001, Rule 1.3)
Reference-style links MUST NOT be used for creating any type of hyperlink (internal or external).
*   **Incorrect Example (Reference-Style):**
    ```markdown
    This is an [example][1] of a reference-style link.

    [1]: https://www.example.com/ "Optional Title"
    ```
*   **Rationale:** Inline links, where the URL is directly specified with the link text, are generally more readable and easier to maintain within the context of the document. Prohibiting reference-style links ensures a single, consistent linking method.

### Rule 2.4: Autolinks for URLs and Email Addresses (Derived from M-SYNTAX-LINKS-001, Rule 1.4)
To display a raw URL or email address as a clickable link, it MUST be enclosed in angle brackets (`< >`).
*   **Example (URL):** `<https://www.example.com>` will render as a clickable link to `https://www.example.com`.
*   **Example (Email):** `<contact@example.com>` will render as a clickable `mailto:` link.
*   **Rationale:** This is the standard Markdown syntax for creating autolinks, ensuring that URLs and email addresses are correctly parsed and made interactive.

## 3. Link Display Text (General Guidance)

While [[SF-LINKS-INTERNAL-SYNTAX]] provides specific guidance on display text for `[[STANDARD_ID]]` links (Rule 1.5 from M-SYNTAX-LINKS-001 regarding no escaping pipes for `[[STANDARD_ID|Display Text]]` is best suited there), the general principle of descriptive link text applies to all links created using the syntax in this standard:
*   Link display text SHOULD clearly indicate the content or purpose of the link's destination.
*   Avoid generic link text like "click here" or "more info."

## 4. Importance of Correct Link Syntax

*   **Functionality:** Ensures links work as intended across different Markdown renderers.
*   **Readability:** Clear and consistent link syntax improves the readability of both raw Markdown and rendered content.
*   **Maintainability:** Standardized link formats are easier to manage, update, and validate, especially with automated tools.
*   **Accessibility:** Descriptive link text (Rule 2.1, 2.2) is crucial for users relying on assistive technologies.

## 5. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository when creating external links or internal links to non-standard documents or assets using relative paths. For linking between standard documents, [[SF-LINKS-INTERNAL-SYNTAX]] MUST be followed.

## 6. Cross-References
- [[SF-LINKS-INTERNAL-SYNTAX]] - Defines the mandatory `[[STANDARD_ID]]` syntax for linking between standard documents.
- [[CS-LINKING-INTERNAL-POLICY]] - Outlines the strategy and best practices for internal linking.
- [[AS-STRUCTURE-ASSET-ORGANIZATION]] - For guidance on organizing and linking to assets.

---
*This standard (SF-SYNTAX-LINKS-GENERAL) is based on rules 1.1 (partially), 1.2, 1.3, and 1.4 previously defined in M-SYNTAX-LINKS-001 from COL-SYNTAX-MARKDOWN.md. It clarifies the use of relative path Markdown links for non-standard documents/assets and defers standard-to-standard linking to [[SF-LINKS-INTERNAL-SYNTAX]]. Rule 1.5 regarding pipe escaping is primarily relevant to the wikilink/STANDARD_ID syntax.*
```
