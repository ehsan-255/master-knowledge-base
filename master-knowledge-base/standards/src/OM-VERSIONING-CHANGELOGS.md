---
title: 'Standard: Versioning and Changelogs for Standard Files'
standard_id: OM-VERSIONING-CHANGELOGS
aliases:
  - Standard Versioning
  - Changelog Standard
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Standard File Versioning and Changelogs
related-standards:
  - MT-SCHEMA-FRONTMATTER
version: 2.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-01-11T00:00:00Z'
primary_domain: OM
sub_domain: LIFECYCLE
scope_application: All standard documents and changelog approaches (individual, separate files, and folder-level) within the knowledge base repository.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Standards management
  - Change tracking
  - Historical record keeping
  - User awareness of changes
change_log_url: ./changelog.md
---
# Standard: Versioning and Changelogs for Standard Files (OM-VERSIONING-CHANGELOGS)

This standard defines the mandatory requirements for versioning individual standard documents and maintaining their changelogs. Adherence to these rules ensures that changes to standards are tracked systematically, providing clarity on historical evolution and current validity.

## 1. Frontmatter Versioning Keys (Derived from U-VERSIONING-001, Rule 1.1)

Each individual standard document (including standard definitions, policies, guides, and schemas) MUST include the following keys in its YAML frontmatter, as defined in [[MT-SCHEMA-FRONTMATTER]]:

*   **`version`**: Specifies the current version of the standard document.
*   **`date-created`**: Specifies the date (and time) the standard document was initially created. This value SHOULD NOT change after initial creation.
*   **`date-modified`**: Specifies the date (and time) the standard document was last significantly modified. This MUST be updated upon every substantive change that also warrants a version increment.

*   **Notes:**
    *   The format for `date-created` and `date-modified` MUST be full ISO-8601 date-time format (e.g., `YYYY-MM-DDTHH:MM:SSZ`) as per [[MT-SCHEMA-FRONTMATTER]].
    *   The `version` key value MUST also be enclosed in single quotes in YAML (e.g., `version: '1.0.0'`) as specified in [[MT-SCHEMA-FRONTMATTER]].

## 2. Semantic Versioning (Derived from U-VERSIONING-001, Rule 1.2)

The `version` key for all standard documents MUST use Semantic Versioning 2.0.0 (SemVer). The version number is formatted as MAJOR.MINOR.PATCH (e.g., `1.0.0`, `1.1.0`, `2.0.1`).

*   **Increment MAJOR version (e.g., `1.x.x` to `2.0.0`) when:**
    *   You make incompatible changes (breaking changes) to the standard that require consumers of the standard (e.g., documents, processes, tools) to adapt.
*   **Increment MINOR version (e.g., `x.1.x` to `x.2.0`) when:**
    *   You add functionality or rules in a backwards-compatible manner.
    *   You make significant clarifications or additions that do not break existing compatibility.
*   **Increment PATCH version (e.g., `x.x.1` to `x.x.2`) when:**
    *   You make backwards-compatible bug fixes, correct typos, or make minor editorial improvements that do not alter the substantive meaning or application of the standard.

*   **Initial Drafts:** Typically start at `0.1.0`.
*   **First Final Release:** Typically `1.0.0`.

*   **Example:**
    *   Initial draft: `version: '0.1.0'`
    *   First final release: `version: '1.0.0'`
    *   Minor clarification added: `version: '1.1.0'`
    *   Typo corrected: `version: '1.1.1'`
    *   Breaking change introduced: `version: '2.0.0'`

## 3. Changelog Maintenance (Derived from U-VERSIONING-001, Rule 1.3)

Standard documents MUST maintain human-readable changelog information. The changelog approach SHOULD be selected based on the scope and maturity of the knowledge base:

*   **Location Option 1 (For Isolated Standards):** A dedicated section within the standard document itself, typically an H2 or H3 heading titled "Changelog" or "Revision History" near the end of the document.
*   **Location Option 2 (For Individual Standards):** A separate linked changelog file, referenced by the `change_log_url` frontmatter key as defined in [[MT-SCHEMA-FRONTMATTER]].
*   **Location Option 3 (Recommended for Knowledge Base Collections):** A shared changelog file at the parent folder level that tracks changes affecting multiple related standards. This is the current approach used by this knowledge base, where standards reference `../changelog.md` for comprehensive change tracking.

The changelog MUST record, at a minimum:
*   The **version number**.
*   The **date** of the change (corresponding to `date-modified`).
*   A **brief description** of the changes made for that version.

*   **Example (In-document Changelog Section):**
    ```markdown
    ## Changelog
    ### Version 1.1.0 (2024-07-15)
    - Clarified Rule 2.3 regarding SemVer incrementation.
    - Added examples for PATCH updates.

    ### Version 1.0.0 (2024-06-01)
    - Initial official release of the standard.

    ### Version 0.1.0 (2024-05-10)
    - Initial draft.
    ```

*   **Example (Folder-level Changelog File):**
    ```markdown
    # Standards Changelog
    
    ## Version 1.2.0 (2024-08-15)
    
    ### Added
    - AS-SCHEMA-NEW-DEFINITION: New schema for definition management
    - SF-SYNTAX-ENHANCED-LINKS: Enhanced link syntax support
    
    ### Changed
    - MT-SCHEMA-FRONTMATTER: Updated mandatory keys list
    - CS-POLICY-ACCESSIBILITY: Clarified WCAG compliance requirements
    
    ### Deprecated
    - SF-LEGACY-SYNTAX-OLD: Replaced by SF-SYNTAX-ENHANCED-LINKS
    ```

## 4. Rationale

*   **Traceability:** Semantic versioning and detailed changelogs provide a clear history of how a standard has evolved, making it easier to understand the rationale behind current rules.
*   **Impact Assessment:** When standards change, version numbers help users and maintainers assess the potential impact of adopting a new version.
*   **Communication:** Changelogs communicate the nature of updates to all stakeholders.
*   **Dependency Management:** In automated systems or when standards reference each other, versioning is critical for managing dependencies.
*   **Maintainability:** Folder-level changelogs reduce maintenance overhead when changes affect multiple related standards, preventing changelog duplication and improving change visibility across standard collections.

## 5. Cross-References
- [[MT-SCHEMA-FRONTMATTER]] - Defines the mandatory frontmatter keys (`version`, `date-created`, `date-modified`, `change_log_url`) and their formats.

---
*This standard (OM-VERSIONING-CHANGELOGS) is based on rules 1.1 through 1.3 previously defined in U-VERSIONING-001 from COL-GOVERNANCE-UNIVERSAL.md.*
