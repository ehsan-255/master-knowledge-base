---
title: 'Standard: Image Syntax'
standard_id: SF-SYNTAX-IMAGES
aliases:
- Images
- Image Embedding
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Image Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for embedding images in knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Image display
- Content presentation
- Accessibility
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown Syntax for Images (SF-SYNTAX-IMAGES)

## 1. Standard Statement

This standard **MANDATES** the exclusive Markdown syntax for embedding images within all Knowledge Base documents. Correct and consistent image syntax is **CRITICAL** for displaying visual content, ensuring accessibility through alternative text, and integrating with asset organization practices.

## 2. Core Image Syntax Rule

The standard Markdown syntax for embedding an image is: `![Alt text](URL "Optional title")`

Each component **MUST** adhere to the following requirements:

### Rule 2.1: Image Marker (`!`)
An image link **MUST** be prefixed with an exclamation mark (`!`).
*   **Rationale:** Distinguishes an embedded image from a regular hyperlink in Markdown.

### Rule 2.2: Alternative Text (`Alt text`)
Alternative text (alt text) **MUST** be enclosed in square brackets (`[]`).
*   **Mandatory:** Alt text is **MANDATORY** for all informational images.
*   **Purpose:** Provides a textual description of the image for users who cannot see it (e.g., screen readers, image load failure).
*   **Guidelines:** Refer to [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]] for comprehensive alt text guidelines.
*   **Example:** `![Architectural diagram showing user authentication flow]`
*   **Rationale:** Essential for accessibility (WCAG compliance) and provides context when images are unavailable.

### Rule 2.3: URL/Path to Image
The URL or path to the image file **MUST** be enclosed in parentheses (`()`).
*   **Content:** This **MUST** be either:
    *   A relative path to an internal image file.
    *   An absolute URL to an externally hosted image.
*   **Asset Organization:** For internal images, the path **MUST** adhere to [[AS-STRUCTURE-ASSET-ORGANIZATION]] conventions (e.g., `assets/images/`).
*   **Example (Relative Path):** `(./assets/images/my-diagram.png)`
*   **Example (Absolute URL):** `(https://example.com/path/to/image.jpg)`
*   **Rationale:** Specifies the source for image display by the Markdown renderer.

### Rule 2.4: Optional Title (`"Optional title"`)
An optional title for the image **MAY** be included in quotes after the URL/path, separated by a space.
*   **Usage:** This is **NOT** a substitute for alt text. Critical information **MUST** be in alt text or the main document body, not solely in a tooltip.
*   **Example:** `![Server Rack Diagram](./assets/images/server-rack.png "Server Rack Configuration - Q3")`
*   **Rationale:** Provides supplementary, non-essential information. Support and presentation vary across renderers.

### Rule 2.5: Purely Decorative Images
As per [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]], purely decorative images that add no informational value **MUST** use empty alt text: `alt=""`.
*   **Example:** `![](./assets/images/decorative-border.png)`

## 3. Importance of Strict Image Syntax

*   **Visual Content Display:** Enables crucial embedding and display of visual aids.
*   **Accessibility:** Mandatory alt text ensures content access for visually impaired users.
*   **Contextual Understanding:** Alt text provides context if images fail to load.
*   **Maintainability:** Consistent syntax and clear paths simplify maintenance.
*   **SEO:** Alt text contributes to search engine optimization.

## 4. Scope of Application

This standard applies to **ALL** Markdown documents within the Knowledge Base repository where images are embedded. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 5. Cross-References
*   [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]
*   [[AS-STRUCTURE-ASSET-ORGANIZATION]]

---
*This standard (SF-SYNTAX-IMAGES) has been revised to mandate a strict, singular syntax for image embedding, emphasizing accessibility and integration with asset organization standards.*
