---
title: "Standard: Asset Organization and Naming"
standard_id: "AS-STRUCTURE-ASSET-ORGANIZATION"
aliases: ["Asset Management Standard", "Static File Organization"]
tags:
  - status/draft
  - criticality/P2-Medium # Important for organized repositories
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Asset File Organization" # As per prompt
related-standards: ["SF-CONVENTIONS-NAMING_ID_PLACEHOLDER", "SF-ACCESSIBILITY-IMAGE-ALT-TEXT_ID_PLACEHOLDER", "AS-KB-DIRECTORY-STRUCTURE_ID_PLACEHOLDER"]
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "AS" # Architectural Standard
sub_domain: "STRUCTURE" # As per prompt
scope_application: "Defines the standards for organizing, naming, and formatting non-Markdown assets (e.g., images, diagrams, PDFs, code snippets) within any Knowledge Base."
criticality: "P2-Medium"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Repository cleanliness", "Asset discoverability", "Link integrity for assets", "Authoring consistency", "Build processes"]
change_log_url: "./AS-STRUCTURE-ASSET-ORGANIZATION-changelog.md" # Placeholder
---

# Standard: Asset Organization and Naming (AS-STRUCTURE-ASSET-ORGANIZATION)

## 1. Standard Statement

This standard defines the requirements for organizing, categorizing, naming, and formatting non-Markdown assets (such as images, diagrams, PDFs, and separate code snippets) within any Knowledge Base (KB). Proper asset organization is crucial for maintaining a clean repository, ensuring assets are discoverable, and facilitating link integrity.

## 2. Asset Directory Structure

### Rule 2.1: Top-Level `assets` Folder (Derived from U-ASSETS-001, Rule 1.1)
All non-Markdown assets associated with a specific Knowledge Base MUST reside in a dedicated top-level folder named `assets` directly within that KB's primary folder.
*   **Example:** If a KB's primary folder is `my-awesome-kb/`, then all its assets MUST be placed within `my-awesome-kb/assets/`.
*   **Rationale:** Centralizes all non-Markdown resources for a KB, making them easy to locate and manage. This is consistent with the overall KB directory structure outlined in [[AS-KB-DIRECTORY-STRUCTURE_ID_PLACEHOLDER]].

## 3. Asset Categorization

### Rule 3.1: Sub-folders for Categorization (Derived from U-ASSETS-001, Rule 1.2)
Within the `assets` folder, sub-folders SHOULD be used to categorize assets based on their type or purpose.
*   **Recommended Sub-folder Names:**
    *   `images/` (for PNG, JPG/JPEG, SVG, GIF files)
    *   `diagrams/` (specifically for flowchart, architecture, or other diagrammatic SVGs or PNGs, if differentiation from general images is useful)
    *   `pdfs/` (for PDF documents)
    *   `code-snippets/` (for external code files like `.py`, `.js`, `.sql` that are referenced or meant to be downloadable, not for embedded code in Markdown)
    *   Other categories as needed (e.g., `data/` for CSV files, `audio/` for audio clips).
*   **Example:** `my-awesome-kb/assets/images/user-interface-screenshot.png`, `my-awesome-kb/assets/pdfs/annual-report-2023.pdf`
*   **Folder Naming:** Sub-folder names MUST adhere to the folder naming conventions defined in [[SF-CONVENTIONS-NAMING_ID_PLACEHOLDER]] (all lowercase kebab-case).
*   **Rationale:** Categorization improves the organization of the `assets` folder, making it easier to find and manage specific types of assets, especially in KBs with many assets.

## 4. Asset File Naming

### Rule 4.1: Descriptive Kebab-Case Names (Derived from U-ASSETS-001, Rule 1.3)
Asset file names MUST be descriptive of the asset's content or purpose and MUST adhere to the general file naming conventions (all lowercase kebab-case) defined in [[SF-CONVENTIONS-NAMING_ID_PLACEHOLDER]].
*   **Example:** `q1-sales-report.pdf`, `user-flow-diagram.svg`, `api-request-example.py`
*   **Avoid:** Generic names like `image1.png`, `document.pdf`, or names with spaces or special characters (other than hyphens).
*   **Rationale:** Descriptive names make assets easier to identify and manage. Consistent kebab-casing ensures cross-platform compatibility and predictability.

## 5. Permitted Image Formats and Preferences

### Rule 5.1: Approved Image Formats (Derived from U-ASSETS-001, Rule 1.4)
The following image formats are permitted for use within the knowledge base:
*   `png` (Portable Network Graphics)
*   `svg` (Scalable Vector Graphics)
*   `jpg` or `jpeg` (Joint Photographic Experts Group)
*   `gif` (Graphics Interchange Format - primarily for simple animations if necessary)

### Rule 5.2: Format Preferences (Derived from U-ASSETS-001, Rule 1.4)
*   **Diagrams, Screenshots, Icons:** `svg` or `png` ARE PREFERRED due to their lossless quality and scalability (for SVG).
    *   `svg` is ideal for vector graphics that need to scale perfectly.
    *   `png` is suitable for raster graphics where transparency or sharp detail is needed (e.g., screenshots with text).
*   **Photographic Images:** `jpg` / `jpeg` is generally preferred for photographic images due to its ability to achieve good compression ratios for such content.
*   **Rationale:** Choosing appropriate image formats ensures a balance of visual quality, file size, and scalability, contributing to better performance and user experience. Using `svg` where possible for diagrams and icons allows for better rendering on high-resolution displays and when zoomed.

## 6. Importance of Asset Organization

*   **Maintainability:** A well-organized `assets` folder makes it easier to update or remove assets without breaking links or causing confusion.
*   **Discoverability:** Logical categorization and descriptive naming help authors and maintainers find existing assets for reuse or reference.
*   **Consistency:** Standardized organization and naming create a more professional and predictable repository structure.
*   **Reduced Clutter:** Prevents the root or content directories from being cluttered with media files.
*   **Build Process Efficiency:** Predictable asset locations can simplify automated build processes or static site generation.

## 7. Scope of Application

This standard applies to all non-Markdown files that are part of a Knowledge Base and are stored within its designated `assets` folder.

## 8. Cross-References
- [[SF-CONVENTIONS-NAMING_ID_PLACEHOLDER]] - For general file and folder naming conventions.
- [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT_ID_PLACEHOLDER]] - For requirements related to the accessibility of images.
- [[AS-KB-DIRECTORY-STRUCTURE_ID_PLACEHOLDER]] - For the overall KB directory structure, including the location of the KB-specific `assets` folder.

---
*This standard (AS-STRUCTURE-ASSET-ORGANIZATION) is based on rules 1.1 through 1.4 previously defined in U-ASSETS-001 from COL-LINKING-UNIVERSAL.md.*
```
