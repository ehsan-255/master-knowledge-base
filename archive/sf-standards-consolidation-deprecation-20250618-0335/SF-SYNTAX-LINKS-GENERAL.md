---
title: 'Standard: General Markdown Link Syntax'
standard_id: SF-SYNTAX-LINKS-GENERAL
aliases:
- Markdown Link Syntax
- External Links
- Relative Links
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/global
- status/draft
- topic/links
- topic/sf
kb-id: ''
info-type: standard-definition
primary-topic: General Markdown Link Syntax
related-standards:
- SF-LINKS-INTERNAL-SYNTAX
- CS-LINKING-INTERNAL-POLICY
- AS-STRUCTURE-ASSET-ORGANIZATION
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: LINKS
scope_application: Defines the general Markdown syntax for creating external links
  and relative path internal links to non-standard documents or assets. Complements
  SF-LINKS-INTERNAL-SYNTAX for standard-to-standard linking.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Link integrity
- Readability
- Authoring consistency
- Interoperability with Markdown parsers
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: General Markdown Link Syntax (SF-SYNTAX-LINKS-GENERAL)

## 1. Standard Statement

This standard **MANDATES** the general Markdown syntax for creating hyperlinks, primarily focusing on external links and internal links using relative paths (e.g., to assets or non-standard documents). It complements [[SF-LINKS-INTERNAL-SYNTAX]], which specifically governs `[[STANDARD_ID]]` syntax for linking between standard documents. Adherence to these syntactical rules is **CRITICAL** for link integrity, readability, and consistent parsing.

## 2. Core Link Syntax Rules

### Rule 2.1: External Links
External links (**MUST** link to resources outside the Knowledge Base, typically on the internet) **MUST** use the standard Markdown inline link format: `[Link Display Text](URL)`.
*   **`Link Display Text`**: The human-readable text displayed for the link. This text **MUST** be descriptive of the link's destination or purpose.
*   **`URL`**: The full Uniform Resource Locator (URL) for the external resource (e.g., `https://www.example.com/somepage.html`). URLs **MUST** generally include the scheme (e.g., `http://`, `https://`).
*   **Example:**
    ```markdown
    Visit the [Official W3C Website](https://www.w3.org/).
    Refer to the [MDN guidelines](https://developer.mozilla.org/en-US/docs/Web/HTML).
    ```
*   **Rationale:** This is the universally recognized Markdown syntax for external links, ensuring maximum compatibility and understandability.

### Rule 2.2: Internal Links (Relative Paths for Non-Standard Documents/Assets)
Internal links to non-standard documents (e.g., supplementary materials not governed by a `standard_id`) or to assets (e.g., images, PDFs) within the Knowledge Base repository **MUST** use relative path Markdown inline link syntax: `[Link Display Text](./path/to/file.ext)` or `[Link Display Text](../path/to/file.ext)`.
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
*   **Important Distinction for Standard Documents:** For linking *between standard documents* (i.e., documents with a `standard_id`), the mandatory convention is `[[STANDARD_ID]]` as defined in [[SF-LINKS-INTERNAL-SYNTAX]]. The relative path method described here is **PROHIBITED** for linking standard documents to each other.
*   **Rationale:** Relative paths provide a robust way to link to local files, ensuring links remain valid as long as relative positions are maintained.

### Rule 2.3: Prohibition of Reference-Style Links
Reference-style links **MUST NOT** be used for creating any type of hyperlink (internal or external).
*   **Prohibited Example (Reference-Style):**
    ```markdown
    This is an [example][1] of a reference-style link.

    [1]: https://www.example.com/ "Optional Title"
    ```
*   **Rationale:** Inline links are generally more readable and easier to maintain. Prohibiting reference-style links ensures a single, consistent linking method.

### Rule 2.4: Autolinks for URLs and Email Addresses
To display a raw URL or email address as a clickable link, it **MUST** be enclosed in angle brackets (`< >`).
*   **Example (URL):** `<https://www.example.com>`
*   **Example (Email):** `<contact@example.com>`
*   **Rationale:** This is the standard Markdown syntax for creating autolinks, ensuring URLs and email addresses are correctly parsed and interactive.

## 3. Link Display Text (General Mandate)

Link display text **MUST** clearly indicate the content or purpose of the link's destination. Generic text like "click here" or "more info" is **PROHIBITED**.

## 4. Importance of Strict Link Syntax

*   **Functionality:** Ensures links work as intended across different Markdown renderers.
*   **Readability:** Clear and consistent link syntax improves the readability of both raw Markdown and rendered content.
*   **Maintainability:** Standardized link formats are easier to manage, update, and validate with automated tools.
*   **Accessibility:** Descriptive link text is crucial for users relying on assistive technologies.

## 5. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository when creating external links or internal links to non-standard documents or assets using relative paths. For linking between standard documents, [[SF-LINKS-INTERNAL-SYNTAX]] **MUST** be followed.

## 6. Cross-References
*   [[SF-LINKS-INTERNAL-SYNTAX]]
*   [[CS-LINKING-INTERNAL-POLICY]]
*   [[AS-STRUCTURE-ASSET-ORGANIZATION]]

---
*This standard (SF-SYNTAX-LINKS-GENERAL) has been revised to mandate strict, singular syntax for general Markdown links, including external links and relative path internal links. It explicitly prohibits reference-style links and mandates descriptive link text.*
```
