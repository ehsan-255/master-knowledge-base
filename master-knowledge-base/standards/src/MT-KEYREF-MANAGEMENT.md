---
title: "Standard: Key Definition Management and Storage"
standard_id: "MT-KEYREF-MANAGEMENT"
aliases: ["Keyref Management", "Key Definition Standard", "U-KEYREF-MANAGEMENT-001"]
tags:
  - status/draft
  - content-type/standard-definition
  - topic/keyref
  - topic/metadata-management
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "Defines the storage, structure, and management process for global key definitions used in key-based referencing (keyrefs)."
related-standards: ["SF-SYNTAX-KEYREF", "SF-SYNTAX-YAML-FRONTMATTER", "UA-KEYDEFS-GLOBAL"]
version: '1.0.0'
date-created: "2025-05-30T12:00:00Z"
date-modified: "2025-05-30T21:00:00Z"
primary_domain: "MT"
sub_domain: "REGISTRY"
scope_application: "Governs the management of the central _key_definitions.md file (identified as [[UA-KEYDEFS-GLOBAL]]) and the structure of its content."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Content consistency", "Maintainability", "Automation (keyref resolution)", "Authoring workflow"]
change_log_url: "./MT-KEYREF-MANAGEMENT-changelog.md"
---
# Standard: Key Definition Management and Storage (MT-KEYREF-MANAGEMENT)

This document defines the universal standard for how and where key-based referencing (keyref) definitions are stored and managed. This ensures a single source of truth for all reusable key values, primarily through the `_key_definitions.md` file (see [[UA-KEYDEFS-GLOBAL]]).

## 2. Core Rules

### Rule 2.1: Centralized Key Definition File
All globally reusable key definitions MUST be stored in a single, dedicated file named `_key_definitions.md` located in the root of the `master-knowledge-base` directory. This file is identified by the standard [[UA-KEYDEFS-GLOBAL]].
*   **Rationale:** Centralizes key definitions for easy management, global access, and single-source-of-truth.

### Rule 2.2: Storage within YAML Frontmatter
Key definitions within `_key_definitions.md` MUST be stored within its YAML frontmatter, under a top-level dictionary key named `keys:`. Syntax MUST adhere to [[SF-SYNTAX-YAML-FRONTMATTER]].
*   **Rationale:** Using YAML frontmatter allows for structured data storage that is easily parsable by automated tools and aligns with existing metadata practices.

### Rule 2.3: Key Naming and Value Types
Each key under `keys:` MUST be a string representing the key name (e.g., `productName`). Key names SHOULD follow camelCase convention and are case-sensitive. Values can be strings, numbers, or booleans. Complex objects or lists are discouraged for simple keyrefs.
*   **Example Key Names:** `productName`, `companyFullName`, `apiVersion`, `supportEmail`
*   **Rationale:** Consistent naming conventions improve readability and predictability. Simple value types ensure straightforward replacement by resolver scripts.

### Rule 2.4: Documentation in Markdown Body
The Markdown body of `_key_definitions.md` ([[UA-KEYDEFS-GLOBAL]]) SHOULD be used to document the purpose, scope, and usage guidelines for the defined keys, or to categorize them.
*   **Example:**
    ```markdown
    # Key Definitions Documentation

    This document's frontmatter contains all globally defined keys for use in key-based referencing.

    ## Product Related Keys
    -   `productName`: The official full name of the primary product.
    -   `productVersion`: The current major.minor version of the product.

    ## Company Related Keys
    -   `companyFullName`: The full legal name of the company.
    ```
*   **Rationale:** Provides context and guidance for authors using the keys, improving understanding and appropriate usage.

### Rule 2.5: Update Propagation
Changes to `_key_definitions.md` ([[UA-KEYDEFS-GLOBAL]]) (adding, modifying, or removing keys) MUST trigger appropriate update processes for any rendered or compiled content (e.g., re-run of a 'Resolver Script') to ensure consistency.
*   **Rationale:** Ensures that all content consuming keyrefs reflects the latest definitions, maintaining accuracy across the knowledge base.

## 3. Illustrative Examples (Overall)

### Example: `_key_definitions.md` (File: `master-knowledge-base/_key_definitions.md`)

```yaml
---
# This is the frontmatter of _key_definitions.md ([[UA-KEYDEFS-GLOBAL]])
# It contains the actual key-value pairs.
keys:
  productName: "InnovateSphere Suite"
  productVersion: "3.5"
  companyFullName: "Innovatech Global Solutions, Inc."
  supportEmail: "support@innovatech.com"
  copyrightYear: 2024
  isBetaFeature: false
  featureNameXYZ: "Quantum Entanglement Dashboard"
  docsPortalURL: "https://docs.innovatech.com"
---

# Key Definitions Documentation

This file serves as the central repository for globally defined text variables (keyrefs)
used throughout the knowledge base.

## Key Categories

### Product Information
*   **productName**: The official full name of our flagship product.
    *   *Usage*: Use wherever the full product name is required.
*   **productVersion**: The current public release version of the product.
    *   *Usage*: For referring to the current version in documentation.

### Company Information
*   **companyFullName**: The full legal name of the company.
    *   *Usage*: For official documents, legal disclaimers.
*   **supportEmail**: The primary email address for customer support.
    *   *Usage*: In contact sections, troubleshooting guides.

### Feature Specific
*   **featureNameXYZ**: Official name for the 'Quantum Entanglement Dashboard' feature.
    *   *Usage*: When referring to this specific feature.

### URLs
*   **docsPortalURL**: The main URL for the documentation portal.
    *   *Usage*: For linking back to the main portal page.

### Miscellaneous
*   **copyrightYear**: The current year for copyright notices.
    *   *Usage*: In footers or legal sections.
*   **isBetaFeature**: A boolean flag that might be used by a resolver script for conditional text related to beta features.
    *   *Usage*: `{{key.isBetaFeature}}` might be used in conditional logic.

```

## 4. Importance

*   **Single Source of Truth:** Centralizes reusable text snippets, preventing inconsistencies.
*   **Ease of Update:** Changes to common terms (e.g., product name, year) require editing only one file.
*   **Accuracy:** Reduces typos and variations that can occur with manual repetition.
*   **Automation:** Enables scripts to reliably parse and use these definitions for various purposes (e.g., content generation, validation).

## 5. Cross-References
- [[SF-SYNTAX-KEYREF]] - Defines the syntax for *using* keyrefs in content (e.g., `{{key.yourKeyName}}`).
- [[SF-SYNTAX-YAML-FRONTMATTER]] - Defines the YAML syntax used within the `_key_definitions.md` file.
- [[UA-KEYDEFS-GLOBAL]] - The standard identifier for the `_key_definitions.md` file itself.

---
*This standard (MT-KEYREF-MANAGEMENT) is based on rules previously defined in U-KEYREF-MANAGEMENT-001.*
