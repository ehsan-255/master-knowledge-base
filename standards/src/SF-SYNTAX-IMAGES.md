---
title: 'Standard: Image Syntax'
standard_id: SF-SYNTAX-IMAGES
aliases:
  - Images
  - Image Embedding
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Image Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for embedding images in knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Image display
  - Content presentation
  - Accessibility
---
# Standard: Markdown Syntax for Images (SF-SYNTAX-IMAGES)

## 1. Standard Statement

This standard defines the mandatory Markdown syntax for embedding images within all knowledge base documents. Correct and consistent image syntax is essential for displaying visual content, ensuring accessibility through alternative text, and integrating with asset organization practices.

## 2. Core Image Syntax Rule

The standard Markdown syntax for embedding an image is:

`![Alt text](URL "Optional title")`

Each component of this syntax has a specific purpose and requirement:

### Rule 2.1: Image Marker (`!`)
An image link is prefixed with an exclamation mark (`!`).
*   **Syntax:** The `!` character distinguishes an image link (which embeds the image) from a regular Markdown link (which creates a hyperlink).
*   **Rationale:** Standard Markdown differentiator for embedded images versus textual links.

### Rule 2.2: Alternative Text (`Alt text`)
Alternative text (alt text) is enclosed in square brackets (`[]`).
*   **Requirement:** Alt text is **mandatory** for all informational images.
*   **Purpose:** Provides a textual description of the image for users who cannot see it (e.g., users with screen readers, or if the image fails to load). It is critical for accessibility.
*   **Detailed Guidelines:** For comprehensive rules on how to write effective and descriptive alt text, refer to [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]].
*   **Example:** `![Architectural diagram showing user authentication flow]`
*   **Rationale:** Essential for accessibility (WCAG compliance) and provides context when images are unavailable.

### Rule 2.3: URL/Path to Image
The URL or path to the image file is enclosed in parentheses (`()`).
*   **Content:** This can be:
    *   A relative path to an image file stored within the knowledge base repository (preferred for internal assets).
    *   An absolute URL to an image hosted externally.
*   **Asset Organization:** For images stored internally, the path SHOULD adhere to the conventions defined in [[AS-STRUCTURE-ASSET-ORGANIZATION]] (e.g., pointing to a file within the `assets/images/` directory of the respective KB).
*   **Example (Relative Path):** `(./assets/images/my-diagram.png)`
*   **Example (Absolute URL):** `(https://example.com/path/to/image.jpg)`
*   **Rationale:** Specifies the source from which the browser or Markdown renderer should fetch and display the image.

### Rule 2.4: Optional Title (`"Optional title"`)
An optional title for the image can be included in quotes after the URL/path, separated by a space.
*   **Behavior:** Many Markdown renderers display this title as a tooltip when the user hovers their mouse over the image.
*   **Usage:** Use sparingly. It is NOT a substitute for alt text. Important information should be in the alt text or the main document body, not solely in a tooltip.
*   **Example:** `![Server Rack Diagram](./assets/images/server-rack.png "Server Rack Configuration - Q3")`
*   **Rationale:** Can provide supplementary, non-essential information. Its support and presentation vary across renderers, making it less reliable for critical information compared to alt text.

## 3. Complete Examples

### Example 3.1: Image with Alt Text and Relative Path (Preferred for Internal Assets)
```markdown
![Flowchart of the content lifecycle process, starting with 'Draft' and ending with 'Archive'.](./assets/diagrams/content-lifecycle.svg)
```

### Example 3.2: Image with Alt Text, Relative Path, and Optional Title
```markdown
![User interface screenshot of the main dashboard.](./assets/images/dashboard-screenshot.png "Main Dashboard - Version 2.1")
```

### Example 3.3: Image with Alt Text and Absolute URL (for External Images)
```markdown
![Logo of the World Wide Web Consortium (W3C).](https://www.w3.org/Icons/w3c_home.png "W3C Home Page Logo")
```

### Example 3.4: Purely Decorative Image (Use Sparingly)
As per [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]], if an image is purely decorative and adds no informational value:
```markdown
![](./assets/images/decorative-border.png) 
```
*(Note: The alt text is empty: `alt=""`)*

## 4. Importance of Correct Image Syntax

*   **Visual Content Display:** Enables the embedding and display of visual aids which are crucial for understanding many topics.
*   **Accessibility:** Mandatory alt text ensures content is accessible to users with visual impairments.
*   **Contextual Understanding:** Alt text provides context if images fail to load or are disabled.
*   **Maintainability:** Consistent syntax and clear paths (especially relative paths to organized assets) make maintenance easier.
*   **SEO:** Alt text can contribute to search engine optimization by describing image content to crawlers.

## 5. Scope of Application

This standard applies to all Markdown documents within the knowledge base repository where images are embedded.

## 6. Cross-References
- [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]] - For detailed guidelines on writing effective alternative text.
- [[AS-STRUCTURE-ASSET-ORGANIZATION]] - For rules on storing and organizing image files and other assets.

---
*This standard (SF-SYNTAX-IMAGES) is based on common Markdown image syntax conventions and emphasizes integration with accessibility and asset organization standards.*
