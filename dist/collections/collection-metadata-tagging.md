---
title: "Metadata, Tagging & Registry Standards"
description: "A collection of key standards for document metadata (frontmatter), tagging strategy, key references, and registry management from the MT (Metadata & Tagging) domain."
date_generated: "2025-06-04T22:19:33.653412+00:00"
source_collection_definition_id: "coll_mt_metadata_tagging"
number_of_standards: 6
tags: ["content-type/collection-document", "status/published", "topic/derived-view"] 
info-type: "collection-document" 
# Consider adding a standard_id for the collection itself, e.g.:
# standard_id: "COLL-COLL-MT-METADATA-TAGGING" 
---

## Table of Contents
- [Standard: Key Definition Management and Storage (`MT-KEYREF-MANAGEMENT`)](#standard-key-definition-management-and-storage-mt-keyref-management)
- [Master Tag Glossary and Registry (`MT-REGISTRY-TAG-GLOSSARY`)](#master-tag-glossary-and-registry-mt-registry-tag-glossary)
- [Standard: Frontmatter Schema Definition (`MT-SCHEMA-FRONTMATTER`)](#standard-frontmatter-schema-definition-mt-schema-frontmatter)
- [Standard: Primary Topic Keyword Strategy (`MT-STRATEGY-PRIMARY-TOPIC-KEYWORD`)](#standard-primary-topic-keyword-strategy-mt-strategy-primary-topic-keyword)
- [Policy: Tagging Strategy and Implementation (`MT-TAGGING-STRATEGY-POLICY`)](#policy-tagging-strategy-and-implementation-mt-tagging-strategy-policy)
- [Standard: Tag Implementation Guidelines (`MT-TAGS-IMPLEMENTATION`)](#standard-tag-implementation-guidelines-mt-tags-implementation)


## Standard: Key Definition Management and Storage (MT-KEYREF-MANAGEMENT)

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

---

## Master Tag Glossary and Registry (MT-REGISTRY-TAG-GLOSSARY)

# Master Tag Glossary and Registry (MT-REGISTRY-TAG-GLOSSARY)

This document defines all official tags used across knowledge bases, their intended meaning, hierarchy, and usage guidelines. It serves as the master registry for tags. Refer to `[[MT-TAGGING-STRATEGY-POLICY]]` for the core tagging strategy and `[[GM-REGISTRY-GOVERNANCE]]` for how this registry is managed. This glossary is referenced by `[Standard: Frontmatter Schema Definition](#standard-frontmatter-schema-definition-mt-schema-frontmatter)` for validating tags in document frontmatter.

## Tag Categories

### Status Tags (`status/*`)
- `status/draft`: Content is in initial draft stage, subject to significant change.
- `status/in-review`: Content is under review by subject matter experts or stakeholders.
- `status/approved`: Content has been formally approved and is considered stable.
- `status/published`: Content has been formally published (if applicable to workflow).
- `status/deprecated`: Content is no longer current or recommended for use.
- `status/archived`: Content is preserved for historical reference but is not actively maintained.

### KB Identification Tags (`kb-id/*`)
- `kb-id/standards`: For notes belonging to the Standards KB.
- `kb-id/research-methodology`: For notes belonging to the Research Methodology KB.
- `kb-id/llm-cookbook`: For notes belonging to the LLM Content Generation Cookbook KB.
- `kb-id/global`: For vault-level utility files not specific to one KB.

### Structural Tags
- `kb-master-index`: Applied to `kb-directory.md`.
- `kb-root`: Applied to the `root.md` file of each KB.
- `kb-part-overview`: Applied to `_overview.md` files for Parts within a KB.
- `kb-utility`: Applied to utility documents like this glossary.

### Topic Tags (`topic/*`)
- `topic/metadata`: Documents about metadata standards, structure, or management.
- `topic/governance`: Documents about governance, versioning, or change management.
- `topic/yaml`: Documents about YAML syntax or usage.
- `topic/tagging`: Documents about tagging strategy or tag management.
- `topic/standards-governance`: Documents about standards governance or glossary.
- `topic/architecture`: Documents about KB or file/folder architecture.
- `topic/structure`: Documents about document or section structure.
- `topic/content-guidelines`: Documents about content creation, schemas, or tone.
- `topic/schemas`: Documents about content schemas or templates.
- `topic/markdown`: Documents about Markdown syntax or formatting.
- `topic/syntax`: Documents about syntax rules.
- `topic/obsidian`: Documents about Obsidian-specific usage and conventions.
- `topic/support-docs`: Documents about supporting documentation, onboarding, or guides.
- `topic/llm`: Documents about LLMs, prompt engineering, or automation.
- `topic/content-generation`: Documents about content generation workflows.
- `topic/project-management`: Documents about project management or TODO tracking.
- `topic/research-methodology`: Documents about research methodology KB or standards.
- `topic/glossary`: Documents about glossaries or terminology.
- `topic/utility-standards`: Documents about utility standards or supporting processes.
- `topic/build-process`: Documents about the assembly or build process for the KB.
- `topic/scripting`: Documents outlining scripts or automation logic.
- `topic/linking`: Documents focused on interlinking content.

### Content Type Tags (`content-type/*`)
(Align with `info-type` where sensible, but can be more granular)
- `content-type/technical-standard`: Describes technical rules, specifications.
- `content-type/procedural-guideline`: Outlines steps for a process.
- `content-type/conceptual-explanation`: Explains concepts or principles.
- `content-type/reference-material`: Provides data or information for lookup.
- `content-type/troubleshooting-guide`: Helps resolve issues.
- `content-type/example-code`: Provides code examples.
- `content-type/standard-definition`: For documents that define a standard.
- `content-type/policy-document`: For documents that define a policy.
- `content-type/guide-document`: For documents that provide guidance.
- `content-type/glossary-document`: For documents that define terms (like this one).
- `content-type/template-document`: For documents that serve as templates.
- `content-type/registry-document`: For documents that act as registries.
- `content-type/schema-document`: For documents that define a schema.

### Criticality Tags (`criticality/*`)
(Used for both the `tags` array and as the controlled vocabulary for the `criticality` field)
- `criticality/P0-Critical`: Essential for system operation, core understanding, or carries significant regulatory/compliance implications. Failure to adhere poses immediate and severe risk.
- `criticality/P1-High`: Important for system operation, key processes, or best practices. Failure to adhere poses a high risk of negative impact.
- `criticality/P2-Medium`: Useful for consistency, best practices, or operational efficiency. Failure to adhere may lead to minor issues or inefficiencies.
- `criticality/P3-Low`: Optional or advisory content. Non-adherence is unlikely to cause significant issues.
- `criticality/P4-Informational`: Purely informational content with no direct operational impact.

### Lifecycle Gatekeeper Tags (`lifecycle_gatekeeper/*`)
(Used for both the `tags` array and as the controlled vocabulary for the `lifecycle_gatekeeper` field)
- `lifecycle_gatekeeper/Architect-Review`: Requires review and approval by the architecture review board or designated architects.
- `lifecycle_gatekeeper/Security-Team-Approval`: Requires review and approval by the security team.
- `lifecycle_gatekeeper/Stakeholder-Review`: Requires review and approval by defined business or technical stakeholders.
- `lifecycle_gatekeeper/No-Gatekeeper`: Lifecycle managed by the author or immediate team; no formal external gatekeeper.

### Standards KB Tags (`standards-kb/*`)
- `standards-kb/core`: Core standards and meta-structure documents.
- `standards-kb/universal`: Universal standards applicable to all KBs.
- `standards-kb/kb-specific`: Standards unique to a specific KB.
- `standards-kb/markdown`: Standards related to Markdown syntax and formatting.
- `standards-kb/obsidian`: Standards related to Obsidian-specific usage and conventions.

### Utility & Process Tags
- `utility-standards`: Documents or sections related to utility standards or supporting processes.
- `build-process`: Documents related to the assembly or build process for the KB.
- `scripting`: Documents outlining scripts or automation logic.

### Linking, Metadata, and Content Structure Tags
- `linking`: Standards or documents focused on interlinking content.
- `metadata`: Standards or documents focused on metadata and tagging.
- `governance`: Standards or documents related to governance, versioning, and change management.
- `support-docs`: Supporting documentation, onboarding, and guides.
- `schemas`: Standards or templates for content schemas.
- `syntax-rules`: Rules for Markdown or other syntax.
- `obsidian-usage`: Conventions for using Obsidian features.

### KB-Specific Tags
- `research-methodology`: Used for the Research Methodology KB and related standards.
- `llm-cookbook`: Used for the LLM Content Generation Cookbook KB and related standards.

### Topic Tags (`topic/*`) - Additional from MT-SCHEMA-FRONTMATTER
- `topic/frontmatter`: Documents related to YAML frontmatter.
- `topic/schema`: Documents related to schema definitions.

---

## Standard: Frontmatter Schema Definition (MT-SCHEMA-FRONTMATTER)

# Standard: Frontmatter Schema Definition

## Introduction

This document defines the official schema for YAML frontmatter in all Markdown documents. It specifies the allowed keys, their required order, the data types for their values, their mandatory or optional status, and associated validation rules. 

Adherence to this schema is crucial for maintaining consistency across the knowledge base, enabling automated validation of metadata, and facilitating various automated processing tasks.

For rules regarding the syntax of YAML frontmatter itself (e.g., the use of `---` delimiters), refer to `[[SF-SYNTAX-YAML-FRONTMATTER]]`. For requirements related to file encoding, line endings, and other file hygiene aspects, see `[[SF-FORMATTING-FILE-HYGIENE]]`.

## Overall Structure and Key Order

The YAML frontmatter block MUST contain the following keys in the specified order. This order integrates the original 10 keys and the 7 new extension keys.

1.  `title`
2.  `standard_id` (for standards documents, optional otherwise but recommended if it has a canonical ID)
3.  `aliases`
4.  `tags`
5.  `kb-id`
6.  `info-type`
7.  `primary-topic`
8.  `related-standards`
9.  `version`
10. `date-created`
11. `date-modified`
12. `primary_domain` (for standards documents, optional otherwise)
13. `sub_domain` (for standards documents, optional otherwise)
14. `scope_application`
15. `criticality`
16. `lifecycle_gatekeeper`
17. `impact_areas`
18. `change_log_url`

This order is **mandatory**.

## Detailed Key Definitions

### `title`
*   **Description/Purpose:** The official title of the document.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must not be empty.

### `standard_id`
*   **Description/Purpose:** A unique identifier for a standard document.
*   **Mandatory/Optional:** Mandatory for `info-type` values such as `standard-definition`, `policy-document`. Optional for other document types, but recommended if the document has a canonical identifier.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** MUST follow the regex pattern: `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`. The filename of the document (excluding the `.md` extension) SHOULD be identical to the `standard_id`.

### `aliases`
*   **Description/Purpose:** A list of alternative names or titles by which the document might be known.
*   **Mandatory/Optional:** Optional.
*   **Data Type:** List of Strings.
*   **Validation Rules & Constraints:** None beyond being a list of strings.

### `tags`
*   **Description/Purpose:** A list of keywords or labels used to categorize the document. Tags help in searching, filtering, and understanding the document's context.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** List of Strings.
*   **Validation Rules & Constraints:** All tags MUST be in kebab-case. The list MUST include tags from specific categories, such as `status/*`, `content-type/*`, and `topic/*`. For a comprehensive list of allowed tags and their meanings, refer to `[[MT-REGISTRY-TAG-GLOSSARY]]`.

### `kb-id`
*   **Description/Purpose:** An identifier for the knowledge base this document belongs to.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must be in kebab-case. Value must come from a controlled vocabulary defined in `[[MT-REGISTRY-TAG-GLOSSARY]]` or a dedicated knowledge base registry.

### `info-type`
*   **Description/Purpose:** Specifies the type or category of information the document represents (e.g., a standard, a policy, a guide). This is critical for automation and consistent processing.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must be in kebab-case. The value MUST be one of the predefined values in the Controlled Vocabularies section below.

### `primary-topic`
*   **Description/Purpose:** A concise statement (typically a sentence) describing the main subject or purpose of the document.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must not be empty.

### `related-standards`
*   **Description/Purpose:** A list of other standards that are related to this document.
*   **Mandatory/Optional:** Optional.
*   **Data Type:** List of Strings.
*   **Validation Rules & Constraints:** Each string in the list MUST be a valid `standard_id` of another document or a valid internal link in the format `[[STANDARD_ID]]`.

### `version`
*   **Description/Purpose:** The version number of the document.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Semantic versioning (e.g., `'1.0.0'`, `'0.2.1-alpha'`) is preferred.

### `date-created`
*   **Description/Purpose:** The date and time when the document was originally created.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** MUST be in ISO-8601 date-time format: `YYYY-MM-DDTHH:MM:SSZ`.

### `date-modified`
*   **Description/Purpose:** The date and time when the document was last modified.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** MUST be in ISO-8601 date-time format: `YYYY-MM-DDTHH:MM:SSZ`.

### `primary_domain`
*   **Description/Purpose:** The primary domain code (e.g., "IT", "HR", "MT" for Meta).
*   **Mandatory/Optional:** Mandatory for standards documents; optional otherwise.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must be 2 uppercase letters. The value MUST exist in `[[domain_codes.yaml]]`.

### `sub_domain`
*   **Description/Purpose:** The sub-domain code (e.g., "SECURITY", "NETWORK", "SCHEMA").
*   **Mandatory/Optional:** Mandatory for standards documents; optional otherwise.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must be 2-6 uppercase letters. The value MUST exist in `[[subdomain_registry.yaml]]` for the given `primary_domain`.

### `scope_application`
*   **Description/Purpose:** Defines the scope to which this document applies (e.g., "All backend services", "Frontend components in Project X").
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Must not be empty.

### `criticality`
*   **Description/Purpose:** The criticality level of the document or the standard it defines.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Value MUST come from the controlled vocabulary (e.g., `P0-Critical`, `P1-High`, `P2-Medium`). Refer to `[[MT-REGISTRY-TAG-GLOSSARY]]`.

### `lifecycle_gatekeeper`
*   **Description/Purpose:** Specifies the role or team responsible for approving transitions in the document's lifecycle (e.g., "Architect-Review", "Security-Team-Approval").
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** Value MUST come from a controlled vocabulary. Refer to `[[MT-REGISTRY-TAG-GLOSSARY]]`.

### `impact_areas`
*   **Description/Purpose:** A list of areas or systems that are affected by this document or standard.
*   **Mandatory/Optional:** Mandatory.
*   **Data Type:** List of Strings.
*   **Validation Rules & Constraints:** None beyond being a list of strings.

### `change_log_url`
*   **Description/Purpose:** A URL or relative path pointing to the document's changelog.
*   **Mandatory/Optional:** Mandatory for standards.
*   **Data Type:** String.
*   **Validation Rules & Constraints:** If a relative path, it MUST start with `./`. A linter SHOULD check for the existence of the linked file if it's a relative path.

## Controlled Vocabularies

This section defines or references the controlled vocabularies for specific frontmatter keys.

### `info-type`

The `info-type` key MUST use one of the following string values (all in kebab-case):

*   `standard-definition`
*   `policy-document`
*   `guide-document`
*   `glossary-document`
*   `template-document`
*   `registry-document`
*   `schema-document`
*   `chapter-document`
*   `key-definition-set`
*   `kb-definition-map`
*   `how-to-guide`
*   `tutorial-document`
*   `troubleshooting-guide`
*   `reference-document`
*   `architecture-overview`
*   `design-specification`
*   `meeting-notes`
*   `report-document`
*   `process-definition`
*   `role-definition`
*   `service-definition`
*   `api-specification`
*   `data-model-definition`
*   `security-standard`
*   `compliance-guideline`

### Other Controlled Vocabularies

*   **`tags` (categories and specific tags):** See `[[MT-REGISTRY-TAG-GLOSSARY]]`.
*   **`kb-id`:** See `[[MT-REGISTRY-TAG-GLOSSARY]]` or a dedicated knowledge base registry.
*   **`criticality`:** See `[[MT-REGISTRY-TAG-GLOSSARY]]`.
*   **`lifecycle_gatekeeper`:** See `[[MT-REGISTRY-TAG-GLOSSARY]]`.
*   **`primary_domain`:** Values must exist in `[[domain_codes.yaml]]`.
*   **`sub_domain`:** Values must exist in `[[subdomain_registry.yaml]]` for the specified `primary_domain`.

## Relationship to Filename

For documents that have a `standard_id` (e.g., those with `info-type: standard-definition`), the filename (excluding the `.md` extension) SHOULD exactly match the value of the `standard_id` key. This promotes consistency and predictability in locating standard documents. For example, a document with `standard_id: MT-SCHEMA-FRONTMATTER` should be named `MT-SCHEMA-FRONTMATTER.md`.

---

## Standard: Primary Topic Keyword Strategy (MT-STRATEGY-PRIMARY-TOPIC-KEYWORD)

# Standard: Primary Topic Keyword Strategy

## 1. Standard Statement

This standard defines the strategy and provides guidelines for selecting, formatting, and utilizing the `primary-topic` keyword within the YAML frontmatter of Markdown documents. The `primary-topic` key is defined in `[Standard: Frontmatter Schema Definition](#standard-frontmatter-schema-definition-mt-schema-frontmatter)`.

The primary purpose of the `primary-topic` field is to offer a concise, human-readable, and machine-processable keyword or short phrase that encapsulates the core subject of the document. This enhances content discovery, improves metadata consistency, aids in automated indexing, and boosts overall searchability.

## 2. Purpose of the `primary-topic` Key

The `primary-topic` key serves several functions:

*   **Enhanced Discoverability:** Provides a quick understanding of the document's core subject without needing to parse the full title or content.
*   **Improved Search:** Acts as a primary keyword for search engines and internal search tools.
*   **Content Grouping:** Can be used by automation to group related documents or suggest connections.
*   **Disambiguation:** Helps differentiate documents with similar titles or broad subjects by specifying a focused topic.
*   **Consistency:** Ensures a standardized approach to defining the main subject across documents.

## 3. Guidelines for Selecting and Formatting `primary-topic`

### 3.1. Conciseness and Clarity
*   The `primary-topic` SHOULD be a short, clear keyword or phrase, typically between 1 to 5 words.
*   It MUST be easily understandable and accurately reflect the main subject of the document.
*   Avoid jargon where possible, unless the jargon itself is the topic.

### 3.2. Relationship to Title and `standard_id`
*   **For Standards and Policies:**
    *   If the document has a `standard_id` (e.g., `AS-STRUCTURE-KB-ROOT`, `CS-POLICY-KB-ROOT`), the `primary-topic` can often be derived from the descriptive part of the `standard_id`.
    *   To ensure differentiation, especially for related concepts (like a standard defining a structure vs. a policy for that structure), the `primary-topic` should clearly reflect the document's specific intent.
        *   Example for `standard_id: AS-STRUCTURE-KB-ROOT` (`info-type: standard-definition`): `primary-topic: "Knowledge Base Root Structure"`
        *   Example for `standard_id: CS-POLICY-KB-ROOT` (`info-type: policy-document`): `primary-topic: "Policy for Knowledge Base Root"`
    *   It MAY be a slightly more descriptive version of the `standard_id`'s core concept if the `standard_id` is very terse.
*   **For Other Documents:**
    *   The `primary-topic` should generally be a condensed version or the most significant keyword from the `title`.
    *   It should capture the essence of the `title` in fewer words.

### 3.3. Formatting
*   The `primary-topic` is a string value.
*   While `MT-SCHEMA-FRONTMATTER` does not mandate a specific case, **Title Case** or **Sentence case** is recommended for readability. Consistency within a knowledge base or domain is encouraged. Kebab-case is NOT typically used for `primary-topic`.
    *   Example (Title Case): `"Knowledge Base Root Structure"`
    *   Example (Sentence case): `"Knowledge base root structure"`

### 3.4. Uniqueness and Specificity
*   While not strictly unique like a `standard_id`, the `primary-topic` should be specific enough to be useful for filtering and searching.
*   Avoid overly generic terms if more specific alternatives that still accurately represent the content are available. For example, instead of `"Documentation"`, prefer `"Style Guide Documentation"` if that's more accurate.

## 4. Examples

1.  **Standard Document:**
    *   `title: "Standard: Knowledge Base Root Structure Definition"`
    *   `standard_id: "AS-STRUCTURE-KB-ROOT"`
    *   `info-type: "standard-definition"`
    *   `primary-topic: "Knowledge Base Root Structure"`

2.  **Policy Document:**
    *   `title: "Policy: Content Review and Approval for KB Root"`
    *   `standard_id: "CS-POLICY-KB-ROOT-REVIEW"`
    *   `info-type: "policy-document"`
    *   `primary-topic: "Policy for KB Root Review"`

3.  **Guide Document:**
    *   `title: "Comprehensive Guide to Using the Advanced Search Feature"`
    *   `info-type: "guide-document"`
    *   `primary-topic: "Advanced Search Guide"`

4.  **Glossary Term Definition (if `primary-topic` were used, though less common for this `info-type`):**
    *   `title: "Glossary Definition: Epistemology"`
    *   `info-type: "glossary-document"` (or a more granular `key-definition-set`)
    *   `primary-topic: "Epistemology Definition"`

## 5. Scope of Application
This strategy applies to the `primary-topic` field in the YAML frontmatter of all relevant documents across all knowledge bases where this field is mandated or utilized, as per `[Standard: Frontmatter Schema Definition](#standard-frontmatter-schema-definition-mt-schema-frontmatter)`.

---

## Policy: Tagging Strategy and Implementation (MT-TAGGING-STRATEGY-POLICY)

# Policy: Core Tagging Strategy (MT-TAGGING-STRATEGY-POLICY)

## 1. Policy Statement

This policy defines the core strategy for applying tags to knowledge base documents. It mandates the use of specific tag categories to ensure consistent metadata, enhance content discoverability, support faceted search and filtering, and provide semantic meaning for automated processing. All tags MUST conform to the syntax defined in [Standard: Tag Implementation Guidelines](#standard-tag-implementation-guidelines-mt-tags-implementation) and be defined in the [[MT-REGISTRY-TAG-GLOSSARY]].

## 2. Mandatory Tag Categories and Usage

The following tag categories and their usage rules are mandatory for all relevant documents:

### Rule 2.1: `topic/*` Tag (Derived from U-TAG-001, Rule 1.5)
Every content document (e.g., standards, guides, detailed concepts, methodologies) MUST include at least one `topic/*` tag that accurately reflects its primary subject matter.
*   **Guidance:** Multiple `topic/*` tags are encouraged for interdisciplinary topics to enhance discoverability across different subject areas.
*   **Example:** `topic/architecture`, `topic/metadata/frontmatter`
*   **Rationale:** `topic/*` tags are fundamental for subject-based searching, filtering, and navigation.

### Rule 2.2: `status/*` Tag (Derived from U-TAG-001, Rule 1.6)
Every document MUST include exactly ONE `status/*` tag to indicate its current lifecycle stage.
*   **Guidance:** Valid status values (e.g., `status/draft`, `status/in-review`, `status/approved`, `status/deprecated`) are defined in the [[MT-REGISTRY-TAG-GLOSSARY]].
*   **Example:** `status/draft`
*   **Rationale:** Clearly communicates the maturity and reliability of the document content.

### Rule 2.3: Structural Identification Tags (Derived from U-TAG-001, Rule 1.7)
Specific tags MUST be used to identify key structural documents within the knowledge base ecosystem:
    a.  **`kb-master-index`**: MUST be applied to the master `kb-directory.md` file.
    b.  **`kb-root`**: MUST be applied to the `root.md` file of each individual Knowledge Base.
    c.  **`kb-id/{kb-name}`**: MUST be applied to the `root.md` file of each individual Knowledge Base, where `{kb-name}` is the unique identifier for that KB (e.g., `kb-id/standards-kb`).
    d.  **`kb-part-overview`**: MUST be applied to `_overview.md` files that serve as the overview for a "Part" (major section) within a Knowledge Base.
*   **Rationale:** These tags enable automated identification and processing of key navigational and structural files.

### Rule 2.4: `content-type/*` Tag (Derived from U-TAG-001, Rule 1.8)
Every document MUST include at least one `content-type/*` tag that describes its nature or format.
*   **Guidance:** The controlled vocabulary for the `{type}` part of `content-type/{type}` (e.g., `standard-document`, `policy-document`, `guide-document`) is defined in the `tag-glossary-definition.md` file, referenced as [[MT-REGISTRY-TAG-GLOSSARY]]. This aligns with, but is distinct from, the `info-type` frontmatter key detailed in [Standard: Frontmatter Schema Definition](#standard-frontmatter-schema-definition-mt-schema-frontmatter).
*   **Example:** `content-type/technical-standard`, `content-type/conceptual-explanation`
*   **Rationale:** Allows users and systems to filter content based on its type, facilitating easier access to specific kinds of information.

## 3. Conformance to Tag Glossary (Derived from U-TAG-001, Rule 1.9 - part)

All tag values used in any document's frontmatter (across all categories like `topic/*`, `status/*`, `content-type/*`, `criticality/*`, etc.) MUST strictly conform to a tag explicitly defined in the official Tag Glossary document ([[MT-REGISTRY-TAG-GLOSSARY]]).
*   **Rationale:** Ensures that the tagging system remains controlled, consistent, and meaningful. Prevents the proliferation of ad-hoc or redundant tags, which would degrade the quality and utility of the metadata. The Tag Glossary is the single source of truth for all approved tags.

## 4. Rationale for Tagging Strategy

A robust and consistently applied tagging strategy offers numerous benefits:

*   **Enhanced Discoverability:** Tags provide multiple dimensions for finding relevant content beyond folder structures or titles.
*   **Faceted Search and Filtering:** Allows users to narrow down searches and browse content by combining different tag facets (e.g., find all `status/approved` documents with `topic/security` and `content-type/technical-standard`).
*   **Semantic Meaning:** Adds semantic context to documents, making their purpose and relevance clearer to both humans and machines.
*   **Automation Potential:** Enables automated workflows, such as generating specialized reports, validating content, or managing content lifecycles based on tags.
*   **Improved Knowledge Base Organization:** Complements the structural organization of the KB by providing flexible, metadata-driven views of the content.

## 5. Scope of Application

This policy applies to all documents within the knowledge base ecosystem that utilize YAML frontmatter for metadata. All contributors and maintainers of content are responsible for adhering to this tagging strategy.

## 6. Cross-References
- [Standard: Tag Implementation Guidelines](#standard-tag-implementation-guidelines-mt-tags-implementation) - Defines the syntax and declaration rules for tags.
- [[MT-REGISTRY-TAG-GLOSSARY]] - The official glossary of all approved tags, their hierarchies, and definitions.
- [Standard: Frontmatter Schema Definition](#standard-frontmatter-schema-definition-mt-schema-frontmatter) - Defines the `info-type` key and overall frontmatter structure.

---
*This policy (MT-TAGGING-STRATEGY-POLICY) is based on rules 1.5, 1.6, 1.7, 1.8, and the conformance aspect of 1.9 previously defined in U-TAG-001 from COL-LINKING-UNIVERSAL.md.*

---

## Standard: Tag Implementation Guidelines (MT-TAGS-IMPLEMENTATION)

# Standard: Tag Implementation and Syntax (MT-TAGS-IMPLEMENTATION)

This standard defines the mandatory syntax and declaration rules for all tags used within the YAML frontmatter of knowledge base documents. Adherence to these rules is essential for ensuring metadata consistency, enabling reliable automated processing, and supporting effective content discovery.

## 1. Tag Declaration and Syntax Rules

### Rule 1.1: Declaration in YAML Frontmatter (Derived from U-TAG-001, Rule 1.1)
All tags associated with a document MUST be declared within the YAML frontmatter block at the beginning of the document.
*   **Rationale:** Centralizes metadata, making it easily parsable by automated tools and consistently accessible to authors.
*   **Reference:** General frontmatter structure is defined in [Standard: Frontmatter Schema Definition](#standard-frontmatter-schema-definition-mt-schema-frontmatter).

### Rule 1.2: `tags` Key and Block List Format (Derived from U-TAG-001, Rule 1.2)
Within the YAML frontmatter, tags MUST be listed under a key named exactly `tags`. The value of this key MUST be a block list of strings (each string being a single tag).
*   **Example:**
    ```yaml
    tags:
      - status/draft
      - topic/syntax
      - content-type/standard-definition
    ```
*   **Rationale:** Provides a consistent and machine-readable format for tag declaration.

### Rule 1.3: Kebab-Case for Tag Strings (Derived from U-TAG-001, Rule 1.3)
All tag strings MUST be in **kebab-case** (all lowercase, with words separated by single hyphens).
*   **Example (Correct):** `topic/research-methods`, `content-type/technical-standard`
*   **Example (Incorrect):** `topic/researchMethods`, `ContentType/TechnicalStandard`
*   **Rationale:** Ensures uniformity in tag appearance and simplifies programmatic processing of tags by avoiding case sensitivity issues.

### Rule 1.4: Hierarchical Tag Structure (Derived from U-TAG-001, Rule 1.4)
Tags MAY use forward slashes (`/`) to indicate an internal hierarchy or categorization.
*   **Guidance:**
    *   When used, the hierarchy should be logical and consistently applied (e.g., `category/sub-category/specific-tag`).
    *   Top-level categories (e.g., `topic/`, `status/`, `content-type/`, `criticality/`) should generally come first in the tag string.
*   **Example:** `topic/architecture/directory-structure`, `status/in-review`, `content-type/policy-document`
*   **Rationale:** Hierarchical tags allow for more granular categorization and faceted filtering, improving content organization and discoverability.

## 2. Tag Glossary Requirement (Derived from U-TAG-001, Rule 1.9 - part)

A dedicated Tag Glossary document MUST exist and be maintained. This glossary serves as the single source of truth for all officially recognized tags.
*   **Identification:** This glossary is identified by the standard ID [[MT-REGISTRY-TAG-GLOSSARY]].
*   **Purpose:** The Tag Glossary lists all official tags, defines their intended meaning and scope, and illustrates their correct hierarchy and usage.
*   **Mandate for Conformance:** All tags used in any document's frontmatter MUST conform to a tag defined in the [[MT-REGISTRY-TAG-GLOSSARY]]. The strategic application of these tags is further defined in [[MT-TAGGING-STRATEGY-POLICY]].
*   **Rationale:** Ensures that tags are used consistently and meaningfully across the entire knowledge base, preventing tag proliferation and ambiguity.

## 3. Cross-References
- [Standard: Frontmatter Schema Definition](#standard-frontmatter-schema-definition-mt-schema-frontmatter) - Defines general YAML frontmatter structure and rules.
- [[MT-TAGGING-STRATEGY-POLICY]] - Outlines the strategic application of different tag categories.
- [[MT-REGISTRY-TAG-GLOSSARY]] - The official glossary of all approved tags and their definitions.

---
*This standard (MT-TAGS-IMPLEMENTATION) is based on rules 1.1, 1.2, 1.3, 1.4, and part of 1.9 previously defined in U-TAG-001 from COL-LINKING-UNIVERSAL.md.*
