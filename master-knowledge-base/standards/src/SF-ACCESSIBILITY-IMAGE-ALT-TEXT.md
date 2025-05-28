---
title: "Standard: Image Accessibility and Alternative Text"
standard_id: "SF-ACCESSIBILITY-IMAGE-ALT-TEXT"
aliases: ["Alt Text Standard", "Image Alt Text"]
tags:
  - status/draft
  - criticality/P1-High # Accessibility is a high priority
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Image Alt Text" # As per prompt
related-standards: ["CS-POLICY-ACCESSIBILITY_ID_PLACEHOLDER", "SF-SYNTAX-MARKDOWN-IMAGES_ID_PLACEHOLDER"] # Placeholder for image syntax
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "ACCESSIBILITY" # As per prompt
scope_application: "Defines the requirements for providing alternative text (alt text) for images within all knowledge base documents to ensure accessibility."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review" # Accessibility standards often require architectural or editorial review
impact_areas: ["Accessibility (WCAG compliance)", "User experience for visually impaired users", "SEO (image search)", "Content understanding when images fail to load"]
change_log_url: "./SF-ACCESSIBILITY-IMAGE-ALT-TEXT-changelog.md" # Placeholder
---

# Standard: Image Accessibility and Alternative Text (SF-ACCESSIBILITY-IMAGE-ALT-TEXT)

## 1. Standard Statement

This standard mandates the use of descriptive alternative text (alt text) for all informational images embedded within knowledge base documents. Proper alt text is crucial for web accessibility, ensuring that content is understandable by users with visual impairments (e.g., those using screen readers) and when images fail to load.

## 2. Core Requirements for Alt Text

### Rule 2.1: Mandatory Alt Text for Informational Images (Derived from U-ACCESSIBILITY-001, Rule 1.1)
All images embedded in content that convey information relevant to understanding the content MUST include descriptive alternative text.
*   **Syntax:** Alt text is provided using the standard Markdown image syntax: `![Alt text description here](path/to/image.png "Optional Title")`
    *   The "Optional Title" part of the Markdown syntax (hover text) is not a replacement for alt text and should be used sparingly, if at all, as its accessibility support varies. Primary focus MUST be on the alt text.
*   **Reference:** The specific Markdown syntax for images should align with a general Markdown syntax standard, if available (e.g., [[SF-SYNTAX-MARKDOWN-IMAGES_ID_PLACEHOLDER]]).
*   **Rationale:** Alt text provides a textual alternative to visual information, making image content accessible to screen readers and search engines, and providing context if images are disabled or fail to load.

### Rule 2.2: Concise and Sufficiently Descriptive Alt Text (Derived from U-ACCESSIBILITY-001, Rule 1.2)
Alternative text MUST be concise yet sufficiently descriptive to convey the meaning, purpose, or essential information of the image within the context of the surrounding content.
*   **Avoid Generic Terms:** Generic alt text such as "image," "picture," "graphic," or the image filename is unacceptable as it provides no useful information.
*   **Context is Key:** The description should reflect what is important about the image in its specific context. The same image might have different appropriate alt text depending on how it's used.
*   **Conciseness:** Aim for brevity while capturing the essence of the image. Screen readers will read the entire alt text.
*   **Rationale:** Meaningful alt text ensures that users relying on it gain equivalent understanding to those who can see the image.

### Rule 2.3: Handling Decorative Images (Derived from U-ACCESSIBILITY-001, Rule 1.2 guidance)
If an image is purely decorative and provides no informational value (e.g., a stylistic border or abstract background pattern), it SHOULD be implemented in a way that assistive technologies can ignore it.
*   **Guidance:** For purely decorative images, using an empty alt text (`alt=""`) is the preferred method in Markdown: `![](path/to/decorative-image.png)`.
*   **Caution:** This practice should be used sparingly and only when the image genuinely adds no information relevant to the content. If in doubt, provide descriptive alt text.
*   **Rationale:** Prevents screen readers from announcing non-informative image details, which can be distracting and add cognitive load for users.

## 3. Examples of Alt Text

### Good Alt Text:
*   `![Bar chart showing a 25% increase in Q2 sales compared to Q1, with Q2 sales at $50,000.](./assets/images/q2-sales-chart.png)` (For a chart conveying specific data)
*   `![Logo of the ACME Corporation: a stylized blue phoenix rising from flames.](./assets/images/acme-logo.png)` (Describing a logo)
*   `![User interface for the login screen, showing fields for username and password, and a 'Login' button.](./assets/images/login-screen.png)` (Describing a UI screenshot)
*   `![Flowchart illustrating the five steps of the content approval process, starting with 'Draft Creation' and ending with 'Publication'.](./assets/images/approval-process.png)` (Describing a flowchart's purpose and general structure)

### Bad Alt Text (to be avoided):
*   `![image.png](./assets/images/image.png)`
*   `![Chart](./assets/images/q2-sales-chart.png)`
*   `![Picture of a screen](./assets/images/login-screen.png)`
*   `![ ](./assets/images/logo.png)` (Empty alt text for an informational image)

## 4. Importance of Alt Text

*   **Accessibility for Visually Impaired Users:** Screen readers announce alt text, enabling users with visual impairments to understand the content and purpose of images.
*   **Context when Images Fail to Load:** If an image cannot be displayed (e.g., due to a broken link, slow connection, or user settings), the alt text is shown in its place, providing context.
*   **Search Engine Optimization (SEO):** Search engines use alt text to understand image content, which can improve search result relevance.
*   **Usability for All:** Clear alt text can benefit all users by providing additional context or information about an image, especially for complex visuals.

## 5. Scope of Application

This standard applies to all images (e.g., PNG, JPG, SVG, GIF) embedded within any Markdown document in the knowledge base.

## 6. Cross-References
- [[CS-POLICY-ACCESSIBILITY_ID_PLACEHOLDER]] - The overarching policy on content accessibility.
- [[SF-SYNTAX-MARKDOWN-IMAGES_ID_PLACEHOLDER]] - (If it exists) Standard defining the precise Markdown syntax for images. If not, refer to a general Markdown syntax guide.

---
*This standard (SF-ACCESSIBILITY-IMAGE-ALT-TEXT) is based on rules 1.1 and 1.2 previously defined in U-ACCESSIBILITY-001 from COL-LINKING-UNIVERSAL.md.*
```
