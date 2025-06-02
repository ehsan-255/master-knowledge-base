import yaml
import re
from datetime import datetime, timezone

# Load schema and vocabulary files (content already available from previous turns)
schema_content = """---
title: 'Standard: Frontmatter Schema Definition'
standard_id: MT-SCHEMA-FRONTMATTER
aliases:
  - Frontmatter Schema
  - Metadata Schema for Frontmatter
tags:
  - status/draft
  - criticality/p0-critical
  - content-type/standard-definition
  - topic/metadata
  - topic/frontmatter
  - topic/schema
kb-id: standards
info-type: standard-definition
primary-topic: Defines the comprehensive schema for YAML frontmatter, including all
  keys, their order, data types, validation rules, and controlled vocabularies.
related-standards:
  - SF-SYNTAX-YAML-FRONTMATTER
  - SF-FORMATTING-FILE-HYGIENE
  - MT-REGISTRY-TAG-GLOSSARY
  - AS-STRUCTURE-TEMPLATES-DIRECTORY
  - QM-VALIDATION-METADATA
version: 0.1.0
date-created: '2025-05-29T15:40:18Z'
date-modified: '2025-05-30T12:00:00Z'
primary_domain: MT
sub_domain: FRONTMATTER
scope_application: Applies to the YAML frontmatter of all Markdown documents in all
  knowledge bases.
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Metadata integrity
  - Content validation
  - Authoring consistency
  - Automated processing
  - Interoperability
change_log_url: ./MT-SCHEMA-FRONTMATTER-CHANGELOG.MD
---
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
"""

domain_codes_content = """
registry_id: "DOMAIN"
title: "Primary Domain of Concern"
version: "0.1.0-draft"
entries:
  - id: "AS"
    preferred_label: "Architecture & Structure"
    description: "Rules defining directory structure, modularity, and single‑source build patterns."
  - id: "CS"
    preferred_label: "Content & Semantics"
    description: "Standards governing meaning, metadata keys, and controlled vocabularies."
  - id: "MT"
    preferred_label: "Metadata & Tagging"
    description: "Rules for metadata schemas and tagging mechanisms."
  - id: "SF"
    preferred_label: "Syntax & Formatting"
    description: "Constraints on markdown syntax and formatting rules."
  - id: "OM"
    preferred_label: "Operational Management"
    description: "Automation, deployment, and operational processes."
  - id: "GM"
    preferred_label: "Governance & Meta‑Standards"
    description: "Policies, decision records, and governance standards."
  - id: "UA"
    preferred_label: "Utility & Assets"
    description: "Reusable assets, utilities, and ancillary resources."
  - id: "QM"
    preferred_label: "Quality & Metrics"
    description: "Quality criteria, metrics definition, and validation."
"""

subdomain_registry_content = """
# master-knowledge-base/standards/registry/subdomain_registry.yaml
# Defines SUB_DOMAIN_CODEs for each DOMAIN_CODE

AS: # Architectural Standards
  - code: STRUCTURE
    name: Structural Standards
    description: Standards related to the overall organization and structure of knowledge bases.
  - code: INDEXING
    name: Indexing and Mapping
    description: Standards for creating and managing indexes, maps, and tables of contents.
  - code: SCHEMA
    name: Schema Definitions (Architectural)
    description: Standards defining schemas for architectural components or document types.

CS: # Content Standards
  - code: POLICY
    name: Content Policies
    description: Policies governing the creation, style, and lifecycle of content.
  - code: PROFILING
    name: Content Profiling
    description: Standards for conditionalizing or targeting content to specific audiences or conditions.

MT: # Metadata & Tagging Standards
  - code: FRONTMATTER
    name: Frontmatter Metadata
    description: Standards for metadata included in the frontmatter of documents.
  - code: TAGGING
    name: Tagging Standards
    description: Standards and glossaries for applying tags.
  - code: REGISTRY
    name: Registry Management
    description: Standards related to the creation and maintenance of controlled vocabularies.


SF: # Syntax & Formatting Standards
  - code: MARKDOWN
    name: Markdown Syntax
    description: Standards for the use of Markdown syntax elements.
  - code: LINKS
    name: Linking Syntax
    description: Standards for internal and external linking.
  - code: TRANSCLUSION
    name: Transclusion Syntax
    description: Standards for transcluding content.
  - code: CALLOUTS
    name: Callout/Admonition Syntax
    description: Standards for callouts, admonitions, and similar block elements.
  - code: CONDITIONAL
    name: Conditional Text Syntax
    description: Standards for syntax used in conditional text rendering.


OM: # Operational & Management Standards (Placeholder - refine as needed)
  - code: LIFECYCLE
    name: Lifecycle Management
    description: Standards related to content lifecycle, versioning, and governance.
  - code: AUTOMATION
    name: Automation Standards
    description: Standards related to automated processes, workflows, and tooling integration.

GM: # General & Miscellaneous Standards
  - code: CONVENTIONS
    name: Naming and ID Conventions
    description: General naming conventions and identifier rules.
  - code: GUIDE
    name: Guidance Documents
    description: General guides and instructional materials for using the KB and standards.
  - code: GLOSSARY
    name: Glossaries
    description: General glossaries and term definitions.


UA: # User & Audience Standards (Placeholder - refine as needed)
  - code: ACCESSIBILITY
    name: Accessibility Standards
    description: Standards for ensuring content accessibility.
  - code: KEYDEFS
    name: Key Definitions
    description: Global key definitions.
  - code: SCHEMAS
    name: Schema Definitions (Utility & Assets)
    description: Standards defining schemas for utility or asset-related data structures.


QM: # Quality Management Standards (Placeholder - refine as needed)
  - code: VALIDATION
    name: Validation and Linting
    description: Standards and rules for content validation and linting.

# Add other domain codes (e.g., OM, GM, UA, QM) and their sub-domains as they become clearer.
"""

info_types_content = """standard-definition
policy-document
guide-document
glossary-document
template-document
registry-document
schema-document
navigation-document
chapter-document
key-definition-set
kb-definition-map
how-to-guide
tutorial-document
troubleshooting-guide
reference-document
architecture-overview
design-specification
meeting-notes
report-document
process-definition
role-definition
service-definition
api-specification
data-model-definition
security-standard
compliance-guideline
collection-document
mandate-document
changelog
"""

criticality_levels_content = """
# master-knowledge-base/standards/registry/criticality_levels.yaml
# Defines controlled vocabulary for 'Criticality' metadata and tags.

- level: P0-Critical
  tag: criticality/P0-Critical
  description: Standard or policy that, if not followed, can lead to severe operational disruption, data loss, security vulnerabilities, or major compliance failures. Highest priority for adherence and monitoring.

- level: P1-High
  tag: criticality/P1-High
  description: Standard or policy that, if not followed, can lead to significant operational inefficiencies, data integrity issues, or notable compliance gaps. Important for maintaining system stability and quality.

- level: P2-Medium
  tag: criticality/P2-Medium
  description: Standard or policy that, if not followed, may lead to minor operational issues, inconsistencies, or deviations from best practices. Recommended for good practice and consistency.

- level: P3-Low
  tag: criticality/P3-Low
  description: Standard or policy that provides guidance or recommendations that are beneficial but not strictly mandatory for core operations or compliance. Adherence is encouraged.
"""

lifecycle_gatekeepers_content = """
# master-knowledge-base/standards/registry/lifecycle_gatekeepers.yaml
# Defines controlled vocabulary for 'Lifecycle_Gatekeeper' metadata.

- gatekeeper: Architect-Review
  name: Architect Review
  description: Requires review and approval from a designated system/solution architect or architectural body.

- gatekeeper: SME-Consensus
  name: Subject Matter Expert (SME) Consensus
  description: Requires consensus agreement from a defined group of subject matter experts.

- gatekeeper: Automated-Validation
  name: Automated Validation
  description: Requires passing automated checks, linters, or validation scripts.

- gatekeeper: Peer-Review
  name: Peer Review
  description: Requires review and feedback from peers or team members.

- gatekeeper: Editorial-Board-Approval
  name: Editorial Board Approval
  description: Requires approval from a designated editorial board or governance committee.

- gatekeeper: No-Formal-Gatekeeper
  name: No Formal Gatekeeper
  description: Does not require a formal gatekeeper for progression; may rely on author discretion or informal review.
"""

tag_categories_content = """status/
kb-id/
content-type/
topic/
criticality/
lifecycle_gatekeeper/
# Add other major topic categories if they become common, e.g.
# project/
# team/
# technology/
"""

tag_glossary_content = """---
title: Master Tag Glossary and Registry
standard_id: MT-REGISTRY-TAG-GLOSSARY
aliases:
- Tag Glossary
- Controlled Vocabulary for Tags
tags:
- kb-id/standards
- content-type/registry-document
- content-type/glossary-document
- status/draft
- topic/tagging
- topic/metadata
- topic/registry
kb-id: kb-id/standards
info-type: registry-document
primary-topic: Defines all official tags, their meanings, hierarchy, and usage guidelines. Serves as the master registry for tags.
related-standards:
- MT-TAGGING-STRATEGY-POLICY
- GM-REGISTRY-GOVERNANCE
- MT-SCHEMA-FRONTMATTER
version: 1.0.0
date-created: '2025-05-15T00:00:00Z'
date-modified: '2025-05-29T16:04:35Z'
primary_domain: MT
sub_domain: REGISTRY
scope_application: Applies to all knowledge bases and documents for tag usage and frontmatter validation.
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Metadata consistency
- Content discoverability
- Automation
- Search accuracy
change_log_url: ./MT-REGISTRY-TAG-GLOSSARY-CHANGELOG.MD
---

# Master Tag Glossary and Registry (MT-REGISTRY-TAG-GLOSSARY)

This document defines all official tags used across knowledge bases, their intended meaning, hierarchy, and usage guidelines. It serves as the master registry for tags. Refer to `[[MT-TAGGING-STRATEGY-POLICY]]` for the core tagging strategy and `[[GM-REGISTRY-GOVERNANCE]]` for how this registry is managed. This glossary is referenced by `[[MT-SCHEMA-FRONTMATTER]]` for validating tags in document frontmatter.

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
"""

target_files_content_raw = [
    """---
title: Knowledge Base Directory Structure Standard
standard_id: AS-KB-DIRECTORY-STRUCTURE
aliases:
  - Directory Structure
  - Folder Organization
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Directory Structure
related-standards: []
version: 0.1.0
date-created: '2024-07-15T10:00:00Z'
date-modified: '2025-05-30T21:00:00Z'
primary_domain: AS
sub_domain: STRUCTURE
scope_application: Overall repository and knowledge base file organization.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Authoring workflow
  - Build process
  - Navigation
change_log_url: ./AS-KB-DIRECTORY-STRUCTURE-CHANGELOG.MD
---
# AS-KB-DIRECTORY-STRUCTURE: Knowledge Base Directory Structure Standard

## 1. Overview

This standard defines the official directory structure for the master knowledge base. A consistent directory structure is crucial for organization, navigability, and automation.

## 2. Top-Level Organization

The primary content and operational files for the knowledge base are organized under a root directory named `master-knowledge-base/`.

## 3. Core Directories for Standards Development

Within `master-knowledge-base/standards/`, the following specialized directories are used:

*   **`/master-knowledge-base/standards/src/` (Task 0.4.1)**
    *   **Purpose:** This is the primary Layer 1 directory for all atomic standard documents (Standard Definitions, Policy Documents, Guide Documents, etc.).
    *   **Content:** Individual Markdown files (`.md`) representing single, atomic standards.
    *   **Naming:** Files in this directory MUST follow the [[SF-CONVENTIONS-NAMING#Atomic File Naming Convention|File Naming Convention]] (Note: Link to be updated once actual naming convention doc ID is set).

*   **`/master-knowledge-base/standards/registry/` (Task 0.4.2)**
    *   **Purpose:** This directory houses all controlled vocabulary manifests and registry definition files.
    *   **Content:** YAML files (`.yaml`) or Markdown files (`.md`) that define terms, codes, and their meanings for various metadata fields (e.g., domain codes, status tags, criticality levels).
    *   **Examples:** `domain_codes.yaml`, `tag-glossary-definition.md`.

*   **`/master-knowledge-base/standards/templates/` (Task 0.4.3)**
    *   **Purpose:** This directory contains standard templates for creating new documents.
    *   **Content:** Markdown files (`.md`) serving as boilerplate structures.
    *   **Naming:** Template filenames MUST be prefixed with `tpl-` (e.g., `tpl-canonical-frontmatter.md`, `tpl-standard-definition.md`).

## 4. Tooling and Automation Directory

*   **`/master-knowledge-base/tools/`**
    *   **Purpose:** This directory contains scripts and tooling used for validation, indexing, building, or other automation tasks related to the knowledge base.
    *   **Sub-directories:** May include `linter/`, `indexer/`, `builder/`, `validators/` for organization.
    *   **Examples:** `linter/kb_linter.py`, `indexer/generate_index.py`.

## 5. Other Key Directories (Illustrative - To Be Expanded)

*   **`/master-knowledge-base/assets/`**
    *   **Purpose:** For storing static assets like images, diagrams, or other binary files referenced in documents.
*   **`/dist/` or `/build/` (outside `master-knowledge-base/`, typically gitignored)**
    *   **Purpose:** Output directory for generated views, compiled sites, or other build artifacts.

This document will be updated as the directory structure evolves.
```""",
    """---
title: Standards Knowledge Base Definition Map
standard_id: AS-MAP-STANDARDS-KB
aliases:
  - Standards KB Map
  - Standards KB Structure Definition
tags:
  - status/draft
  - criticality/p1-high
  - content-type/kb-definition-map
  - topic/architecture
  - topic/indexing
  - kb-id/standards
kb-id: standards
info-type: kb-definition-map
primary-topic: Defines the logical structure, parts, and organization of the Standards
  Knowledge Base itself.
related-standards:
  - AS-STRUCTURE-KB-ROOT
  - AS-STRUCTURE-KB-PART
  - MT-SCHEMA-FRONTMATTER
  - AS-STRUCTURE-MASTER-KB-INDEX
version: 0.1.0
date-created: '2025-05-29T16:04:35Z'
date-modified: '2025-05-30T17:00:00Z'
primary_domain: AS
sub_domain: INDEXING
scope_application: Applies specifically to the Standards Knowledge Base, defining
  its internal organization and primary components.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - KB navigation
  - Content organization
  - Discoverability of standards
  - Authoring within the Standards KB
change_log_url: ./AS-MAP-STANDARDS-KB-CHANGELOG.MD
---
# Standards Knowledge Base Definition Map (AS-MAP-STANDARDS-KB)

## 1. Standard Statement

This document defines the logical structure, primary parts (categories), and overall organization of the Standards Knowledge Base (KB) itself. It serves as a high-level map to help users navigate and understand the layout and content of the standards documentation.

The Standards KB is the authoritative source for all standards, policies, and guidelines governing the creation, management, and use of all knowledge bases within the ecosystem.

> [!TODO] The content of this document, particularly the `parts` structure in the frontmatter and the detailed descriptions below, needs to be fully populated and aligned with the actual organization of standards within the `/master-knowledge-base/standards/src/` directory. The current content is a high-level placeholder based on primary domains.

## 2. Purpose

The purpose of this KB Definition Map is to:
-   Provide a clear and organized overview of the Standards KB.
-   Define the main logical sections ("Parts") of the Standards KB.
-   Facilitate navigation and discovery of relevant standards.
-   Serve as a reference for authors contributing to the Standards KB.

## 3. Structure of the Standards Knowledge Base

The Standards Knowledge Base is organized into logical "Parts," primarily aligned with the `primary_domain` codes used in `standard_id`s. Each part groups related standards.

*(The detailed structure, including links to overview documents for each part and key standards within each part, would be elaborated here. The frontmatter `kb_definition` field provides a conceptual outline of this structure.)*

### Example Part Outline (derived from frontmatter `kb_definition`):

#### Part 1: Architecture and Structure (AS)
-   **Overview:** Standards defining the overall organization of knowledge bases, individual documents, and metadata structures.
-   **Key Documents:** (List or link to key `AS-*` standards, e.g., `[[AS-STRUCTURE-KB-ROOT]]`, `[[AS-STRUCTURE-DOC-CHAPTER]]`, `[[MT-SCHEMA-FRONTMATTER]]` (as it defines a core structure), etc.)

#### Part 2: Content Style and Policies (CS)
-   **Overview:** Standards and policies related to content authoring, tone, language, presentation, and accessibility.
-   **Key Documents:** (List or link to key `CS-*` standards)

#### Part 3: General Management and Meta (GM)
-   **Overview:** Guidance documents, glossaries, and policies for overall KB management, user onboarding, and understanding the standards ecosystem.
-   **Key Documents:** (List or link to key `GM-*` standards, e.g., `[[GM-GUIDE-KB-USAGE]]`, `[[GM-GLOSSARY-STANDARDS-TERMS]]`)

#### Part 4: Metadata, Tagging, and Registries (MT)
-   **Overview:** Standards for document metadata (frontmatter), tagging strategies, keyref systems, and the governance of controlled vocabularies (registries).
-   **Key Documents:** (List or link to key `MT-*` standards, e.g., `[[MT-SCHEMA-FRONTMATTER]]`, `[[MT-TAGGING-STRATEGY-POLICY]]`, `[[MT-REGISTRY-TAG-GLOSSARY]]`)

#### Part 5: Operational Management and Lifecycles (OM)
-   **Overview:** Policies and procedures for the operational aspects of standards and content, including governance, versioning, deprecation, and publishing pipelines.
-   **Key Documents:** (List or link to key `OM-*` standards, e.g., `[[OM-POLICY-STANDARDS-GOVERNANCE]]`, `[[OM-OVERVIEW-PUBLISHING-PIPELINE]]`)

#### Part 6: Quality, Metrics, and Validation (QM)
-   **Overview:** Standards and procedures related to ensuring content quality, defining metrics, and validating metadata and content against defined rules.
-   **Key Documents:** (List or link to key `QM-*` standards, e.g., `[[QM-VALIDATION-METADATA]]`)

#### Part 7: Syntax, Formatting, and Conventions (SF)
-   **Overview:** Specific rules for Markdown syntax, file formatting, naming conventions, and other presentational aspects of content.
-   **Key Documents:** (List or link to key `SF-*` standards, e.g., `[[SF-FORMATTING-MARKDOWN-GENERAL]]`, `[[SF-CONVENTIONS-NAMING]]`)

#### Part 8: Utility, Assets, and Automation (UA)
-   **Overview:** Standards for supporting utilities (like keyrefs), management of assets (like images), and schemas for automation processes (like LLM I/O).
-   **Key Documents:** (List or link to key `UA-*` standards, e.g., `[[UA-KEYDEFS-GLOBAL]]`, `[[UA-SCHEMA-LLM-IO]]`)

## 4. Navigation
-   The primary entry point for the Standards KB is typically its `root.md` file.
-   The master directory of all KBs is `[[AS-STRUCTURE-MASTER-KB-INDEX]]`.

This map helps provide a structured view into the comprehensive set of standards governing the knowledge ecosystem.
""",
    """---
title: Standards Knowledge Base Root
standard_id: AS-ROOT-STANDARDS-KB
aliases:
  - Standards KB Main Page
  - Root for Standards KB
  - Standards KB Root
  - Root of Standards KB
tags:
  - status/active
  - criticality/p0-critical
  - content-type/navigation-document
  - topic/architecture
  - kb-id/standards
  - topic/kb-root
kb-id: standards
info-type: standard-definition
primary-topic: Main entry point and master table of contents for the Standards Knowledge
  Base.
related-standards:
  - AS-STRUCTURE-KB-ROOT
  - AS-MAP-STANDARDS-KB
  - AS-STRUCTURE-MASTER-KB-INDEX
version: 0.1.0
date-created: '2025-05-29T16:10:25Z'
date-modified: '2025-05-30T12:00:00Z'
primary_domain: AS
sub_domain: STRUCTURE
scope_application: Serves as the primary navigational hub for the Standards Knowledge
  Base.
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - KB navigation
  - Content discoverability
  - User orientation
change_log_url: ./AS-ROOT-STANDARDS-KB-CHANGELOG.MD
---
# Standards Knowledge Base Root (AS-ROOT-STANDARDS-KB)

Welcome to the Standards Knowledge Base (KB). This document serves as the main entry point and master table of contents for all standards, policies, guidelines, and supporting documentation related to the knowledge management ecosystem.

The purpose of this KB is to ensure consistency, quality, and interoperability across all managed knowledge domains. For a conceptual map of how this KB is organized, please refer to `[[AS-MAP-STANDARDS-KB]]`.

## Master Table of Contents

> [!TODO] This Table of Contents needs to be populated with links to key standards and parts/categories within the Standards KB. The organization should align with `AS-MAP-STANDARDS-KB`.

### 1. Foundational Concepts
-   Overview of the Standards KB and its purpose.
-   `[[GM-GUIDE-KB-USAGE]]`
-   `[[GM-GUIDE-STANDARDS-BY-TASK]]`
-   `[[GM-GLOSSARY-STANDARDS-TERMS]]`
-   `[[GM-MANDATE-STANDARDS-GLOSSARY]]`
-   `[[GM-MANDATE-KB-USAGE-GUIDE]]`

### 2. Architecture and Structure (AS Domain)
-   Overview of `AS` standards.
-   Key Standards:
    -   `[[AS-STRUCTURE-MASTER-KB-INDEX]]` (Defines `kb-directory.md`)
    -   `[[AS-KB-DIRECTORY-STRUCTURE]]` (Overall repo structure)
    -   `[[AS-STRUCTURE-KB-ROOT]]` (This standard, for individual KB roots)
    -   `[[AS-STRUCTURE-KB-PART]]`
    -   `[[AS-STRUCTURE-DOC-CHAPTER]]`
    -   `[[AS-STRUCTURE-ASSET-ORGANIZATION]]`
    -   `[[AS-STRUCTURE-TEMPLATES-DIRECTORY]]`
-   Schema Definitions:
    -   `[[AS-SCHEMA-CONCEPT-DEFINITION]]`
    -   `[[AS-SCHEMA-METHODOLOGY-DESCRIPTION]]`
    -   `[[AS-SCHEMA-REFERENCE]]`
    -   `[[AS-SCHEMA-TASK]]`
    -   `[[AS-SCHEMA-RELTABLE-DEFINITION]]`
-   Mappings and Indexes:
    -   `[[AS-MAP-STANDARDS-KB]]` (Map of this KB)


### 3. Content, Style, and Policy (CS Domain)
-   Overview of `CS` standards.
-   Key Standards:
    -   `[[CS-POLICY-TONE-LANGUAGE]]`
    -   `[[CS-POLICY-ACCESSIBILITY]]`
    -   `[[CS-LINKING-INTERNAL-POLICY]]`
    -   `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`
    -   `[[CS-ADMONITIONS-POLICY]]` (related to `[[SF-CALLOUTS-SYNTAX]]`)
    -   `[[CS-CONTENT-PROFILING-POLICY]]` (related to `[[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]]`)
    -   ... (other CS policies)

### 4. Metadata, Tagging, and Registries (MT Domain)
-   Overview of `MT` standards.
-   Key Standards:
    -   `[[MT-SCHEMA-FRONTMATTER]]`
    -   `[[MT-TAGGING-STRATEGY-POLICY]]`
    -   `[[MT-REGISTRY-TAG-GLOSSARY]]`
    -   `[[MT-KEYREF-MANAGEMENT]]`
    -   `[[MT-STRATEGY-PRIMARY-TOPIC-KEYWORD]]`
    -   `[[MT-TAGS-IMPLEMENTATION]]`

### 5. Syntax, Formatting, and Conventions (SF Domain)
-   Overview of `SF` standards.
-   Key Standards:
    -   `[[SF-CONVENTIONS-NAMING]]`
    -   `[[SF-FORMATTING-FILE-HYGIENE]]`
    -   `[[SF-FORMATTING-MARKDOWN-GENERAL]]`
    -   `[[SF-SYNTAX-YAML-FRONTMATTER]]`
    -   `[[SF-LINKS-INTERNAL-SYNTAX]]`
    -   ... (other SF standards)

### 6. Operational Management and Lifecycles (OM Domain)
-   Overview of `OM` standards.
-   Key Standards:
    -   `[[OM-POLICY-STANDARDS-GOVERNANCE]]`
    -   `[[OM-VERSIONING-CHANGELOGS]]`
    -   `[[OM-POLICY-STANDARDS-DEPRECATION]]`
    -   `[[OM-OVERVIEW-PUBLISHING-PIPELINE]]`

### 7. Quality, Metrics, and Validation (QM Domain)
-   Overview of `QM` standards.
-   Key Standards:
    -   `[[QM-VALIDATION-METADATA]]`

### 8. Utility, Assets, and Automation (UA Domain)
-   Overview of `UA` standards.
-   Key Standards:
    -   `[[UA-KEYDEFS-GLOBAL]]`
    -   `[[UA-SCHEMA-LLM-IO]]`

---
This root document helps navigate the comprehensive set of standards that govern our knowledge ecosystem.
For navigating all KBs, see `[[AS-INDEX-KB-MASTER]]` (once created/confirmed).
""",
    """---
title: 'Standard: Content Schema for Concept Definitions'
standard_id: AS-SCHEMA-CONCEPT-DEFINITION
aliases:
  - Concept Definition Schema
  - Terminology Schema
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Schema for Concept Definitions
related-standards:
  - AS-STRUCTURE-DOC-CHAPTER
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-05-30T12:00:00Z'
primary_domain: AS
sub_domain: STRUCTURE
scope_application: Defines the mandatory content structure (schema) for documents
  that primarily define a core concept or term.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Content consistency
  - Clarity of definitions
  - User understanding of terminology
  - Knowledge base coherence
change_log_url: ./AS-SCHEMA-CONCEPT-DEFINITION-CHANGELOG.MD
---
# Standard: Content Schema for Concept Definitions (AS-SCHEMA-CONCEPT-DEFINITION)

This standard defines the mandatory content structure (schema) for documents whose primary purpose is to define a core concept or term. Adherence to this schema ensures that concepts are explained clearly, consistently, and comprehensively.

## 1. Scope and Applicability (Derived from U-SCHEMA-CONCEPT-001, Rule 1.1)

This schema MUST be applied to all documents that primarily define a core concept or term.
*   **Example Application:** A document defining `statistical-significance.md` or `machine-learning-bias.md`.

## 2. Mandatory Document Structure

Documents following this schema MUST adhere to the general internal structure for "Chapters" as defined in [[AS-STRUCTURE-DOC-CHAPTER]]. This includes:

### Rule 2.1: H1 Title (Derived from U-SCHEMA-CONCEPT-001, Rule 1.2)
The H1 title of the document MUST be the specific name of the concept or term being defined.
*   **Example:** `# Statistical Significance`

### Rule 2.2: Introductory Abstract (Derived from U-SCHEMA-CONCEPT-001, Rule 1.3)
An introductory abstract that summarizes the concept's meaning and significance MUST be included immediately after the H1 title.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for details on abstract content.

### Rule 2.3: Table of Contents (ToC) (Derived from U-SCHEMA-CONCEPT-001, Rule 1.4)
A Table of Contents (ToC) MUST follow the abstract, linking to all H2 sections and significant H3 sections.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for ToC requirements.

## 3. Required Sections (H2 Level) (Derived from U-SCHEMA-CONCEPT-001, Rule 1.5)

The following H2 sections MUST be included in the document, at a minimum, and should appear in a logical order similar to that presented below:

1.  **`## Definition`** (Derived from U-SCHEMA-CONCEPT-001, Rule 1.6)
    *   This section MUST provide a clear, concise, and unambiguous definition of the concept or term.
    *   It should be easily understandable and serve as the primary explanation.
2.  **`## Key Characteristics / Principles`**
    *   Describe the essential features, attributes, properties, or underlying principles that define or govern the concept.
3.  **`## Importance / Relevance`**
    *   Explain why the concept is important, its significance in relevant domains, or its practical relevance.
4.  **`## Common Misconceptions`** (If Applicable)
    *   Address any common misunderstandings, myths, or incorrect interpretations related to the concept. This section is optional if no common misconceptions are known.
5.  **`## Practical Examples / Applications`** (Derived from U-SCHEMA-CONCEPT-001, Rule 1.7)
    *   This section MUST illustrate the concept in use through practical examples, applications, or case studies.
    *   Examples should be clear and help solidify understanding.

*   **Note:** Other H2 sections can be added as needed to fully explain the concept.

## 4. Illustrative Example (Partial H2 Outline)

For a document named `statistical-significance.md`:
```markdown
# Statistical Significance
(Abstract: This document defines statistical significance, explaining its role in hypothesis testing...)
(Table of Contents: ...)

## Definition
Statistical significance refers to the likelihood that an observed result or relationship in a dataset is not due to random chance...

## Key Characteristics / Principles
- Based on hypothesis testing (null and alternative hypotheses).
- Involves calculating a p-value.
- Threshold for significance (alpha level, e.g., 0.05).
- Does not imply practical significance or importance of the effect.

## Importance / Relevance
- Crucial for drawing valid conclusions from research data.
- Widely used in scientific research, A/B testing, quality control, etc.
- Helps in making data-driven decisions.

## Common Misconceptions
- That statistical significance implies a large or important effect.
- That a non-significant result proves the null hypothesis is true.

## Practical Examples / Applications
### Example 1: A/B Testing
A website tests two versions of a button (A and B). Version B gets a 5% higher click-through rate. Statistical significance testing determines if this 5% difference is likely real or due to chance...

### Example 2: Medical Trials
A new drug is tested against a placebo. Statistical significance helps determine if the observed improvement in patients taking the drug is a real effect of the drug...

## Summary
(Summary of statistical significance...)

## See Also
- [[CONCEPT-HYPOTHESIS-TESTING]]
- [[CONCEPT-P-VALUE]]
```

## 5. Cross-References
- [[AS-STRUCTURE-DOC-CHAPTER]] - For general chapter structure requirements (H1, abstract, ToC, summary, see also).

---
*This standard (AS-SCHEMA-CONCEPT-DEFINITION) is based on rules 1.1 through 1.7 previously defined in U-SCHEMA-CONCEPT-001 from COL-CONTENT-UNIVERSAL.md.*
""",
    """---
title: 'Standard: Content Schema for Methodology/Technique Descriptions'
standard_id: AS-SCHEMA-METHODOLOGY-DESCRIPTION
aliases:
  - Methodology Schema
  - Technique Description Schema
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Schema for Methodology/Technique Descriptions
related-standards:
  - AS-STRUCTURE-DOC-CHAPTER
  - CS-POLICY-LAYERED-INFORMATION
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-05-30T22:00:00Z'
primary_domain: AS
sub_domain: SCHEMA
scope_application: Defines the mandatory content structure (schema) for documents
  that describe specific methodologies, techniques, or detailed processes.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Content consistency
  - Authoring efficiency
  - User understanding of complex processes
  - Information reusability
change_log_url: ./AS-SCHEMA-METHODOLOGY-DESCRIPTION-CHANGELOG.MD
---
# Standard: Content Schema for Methodology/Technique Descriptions (AS-SCHEMA-METHODOLOGY-DESCRIPTION)

This standard defines the mandatory content structure (schema) for documents whose primary purpose is to describe a specific methodology, technique, or detailed process. Adherence to this schema ensures consistency, clarity, and comprehensive coverage of essential aspects.

## 1. Scope and Applicability (Derived from U-SCHEMA-METHOD-001, Rule 1.1)

This schema MUST be applied to all documents that describe a specific methodology, technique, or detailed process. This typically includes "how-to" type content that outlines a systematic approach to achieving a particular outcome.

*   **Example Application:** A document detailing the steps for `systematic-literature-review.md` or `troubleshooting-network-latency.md`.

## 2. Mandatory Document Structure

Documents following this schema MUST adhere to the general internal structure for "Chapters" as defined in [[AS-STRUCTURE-DOC-CHAPTER]]. This includes:

### Rule 2.1: H1 Title (Derived from U-SCHEMA-METHOD-001, Rule 1.2)
The H1 title of the document MUST be the specific name of the methodology or technique being described.
*   **Example:** `# Systematic Literature Review`

### Rule 2.2: Introductory Abstract (Derived from U-SCHEMA-METHOD-001, Rule 1.3)
An introductory abstract that summarizes the method, its purpose, and key outcomes MUST be included immediately after the H1 title.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for details on abstract content.

### Rule 2.3: Table of Contents (ToC) (Derived from U-SCHEMA-METHOD-001, Rule 1.4)
A Table of Contents (ToC) MUST follow the abstract, linking to all H2 sections and significant H3 sections.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for ToC requirements.

## 3. Required Sections (H2 Level) (Derived from U-SCHEMA-METHOD-001, Rule 1.5)

The following H2 sections MUST be included in the document, at a minimum, and should appear in a logical order similar to that presented below:

1.  **`## Purpose`**
    *   Clearly state the primary goal or objective of the methodology/technique. What problem does it solve or what outcome does it achieve?
2.  **`## Core Principles`**
    *   Outline the fundamental concepts, assumptions, or guiding philosophies that underpin the methodology/technique.
3.  **`## When to Use / Not Use`** (Applicability)
    *   Describe the specific contexts, situations, or conditions under which this methodology/technique is most effective or appropriate.
    *   Conversely, describe situations where it might be unsuitable or less effective than alternatives.
4.  **`## Key Steps`** (or **`## Process`**)
    *   This is a critical section detailing the actual execution of the methodology/technique. See "Detailed Requirements for 'Key Steps' / 'Process' Section" below.
5.  **`## Advantages`**
    *   List the primary benefits, strengths, or positive outcomes of using this methodology/technique.
6.  **`## Limitations`**
    *   Describe any known drawbacks, constraints, potential challenges, or areas where the methodology/technique might fall short.
7.  **`## Variations/Alternatives`** (Optional but Recommended)
    *   Discuss common variations of the methodology/technique or briefly mention well-known alternatives if applicable.

## 4. Detailed Requirements for "Key Steps" / "Process" Section

### Rule 4.1: Actionable and Sequenced Steps (Derived from U-SCHEMA-METHOD-001, Rule 1.6)
The "Key Steps" (or "Process") section MUST detail actionable steps in a clear, logical sequence.
*   **Guidance:** Use numbered lists or clearly demarcated H3 headings for each step to ensure sequence is apparent. Steps should be described with enough detail to be understandable and executable by the target audience.

### Rule 4.2: Inputs and Outputs per Step (Derived from U-SCHEMA-METHOD-001, Rule 1.7)
For each "Key Step" described, where applicable, clearly specify:
    a.  **Inputs:** What information, resources, or pre-conditions are required *before* this step can be performed?
    b.  **Outputs/Deliverables:** What tangible results, documents, decisions, or states are produced *by* completing this step?
*   **Example (within an H3 for a step):**
    ```markdown
    ### Step 1: Define Research Question
    **Inputs:** Initial research problem, preliminary literature scan.
    **Outputs:** Focused, answerable research question (e.g., using PICO framework).

    (Detailed actions for defining the research question...)
    ```
*   **Rationale:** Specifying inputs and outputs aids in understanding the flow of the process, supports decomposability for workflow automation, and clarifies dependencies between steps.

## 5. Illustrative Example (Partial H2 Outline)

For a document named `systematic-literature-review.md`:
```markdown
# Systematic Literature Review
(Abstract: This document outlines the process for conducting a systematic literature review...)
(Table of Contents: ...)

## Purpose
To identify, appraise, and synthesize all relevant studies on a particular topic to answer a predefined research question.

## Core Principles
- Transparency in methodology
- Reproducibility of search and selection
- Rigorous critical appraisal of evidence
- Comprehensive and unbiased synthesis

## When to Use / Not Use
**Use when:**
- Answering specific, focused research questions.
- Summarizing the current state of evidence on a mature topic.
- Identifying gaps in current research.
**Not Use when:**
- Broad exploratory research is needed.
- The topic is very new with little existing literature.
- A quick overview is sufficient (consider a scoping review instead).

## Key Steps
### Step 1: Formulate the Research Question (e.g., PICO)
**Inputs:** Initial research problem description, understanding of target domain.
**Outputs:** A clear, focused, and answerable research question.
(Detailed actions on how to formulate the question...)

### Step 2: Develop and Register the Review Protocol
**Inputs:** Formulated research question.
**Outputs:** A documented review protocol outlining the search strategy, inclusion/exclusion criteria, data extraction plan, and analysis methods.
(Detailed actions...)

### Step 3: Execute Search Strategy
(Details...)

## Advantages
- Minimizes bias compared to traditional narrative reviews.
- Provides a comprehensive summary of available evidence.
- Can form the basis for evidence-based guidelines.

## Limitations
- Can be very time-consuming and resource-intensive.
- Quality depends heavily on the quality of included studies.
- May not be suitable for all research questions or types of evidence.

## Variations/Alternatives
- Scoping Reviews
- Rapid Reviews
- Meta-analyses (often a component of systematic reviews)

## Summary
(Summary of the systematic literature review process...)

## See Also
- [[CS-POLICY-LAYERED-INFORMATION]]
- [[AS-STRUCTURE-DOC-CHAPTER]]
```

## 6. Cross-References
- [[AS-STRUCTURE-DOC-CHAPTER]] - For general chapter structure requirements (H1, abstract, ToC, summary, see also).
- [[CS-POLICY-LAYERED-INFORMATION]] - For principles of presenting information from general to specific.

---
*This standard (AS-SCHEMA-METHODOLOGY-DESCRIPTION) is based on rules 1.1 through 1.7 previously defined in U-SCHEMA-METHOD-001 from COL-CONTENT-UNIVERSAL.md.*
"""
]

target_filenames = [
    "master-knowledge-base/standards/src/AS-KB-DIRECTORY-STRUCTURE.md",
    "master-knowledge-base/standards/src/AS-MAP-STANDARDS-KB.md",
    "master-knowledge-base/standards/src/AS-ROOT-STANDARDS-KB.md",
    "master-knowledge-base/standards/src/AS-SCHEMA-CONCEPT-DEFINITION.md",
    "master-knowledge-base/standards/src/AS-SCHEMA-METHODOLOGY-DESCRIPTION.md"
]

# --- Helper function to parse frontmatter and body ---
def parse_markdown_file_content(content):
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content # No frontmatter
    frontmatter_str = parts[1]
    body_str = parts[2]
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        return frontmatter, body_str
    except yaml.YAMLError:
        return None, content # Error parsing YAML

# --- Load Vocabularies ---
domain_codes_data = yaml.safe_load(domain_codes_content)
valid_domain_codes = [entry['id'] for entry in domain_codes_data.get('entries', [])]

subdomain_registry_data = yaml.safe_load(subdomain_registry_content)
valid_subdomains = {}
for domain, sub_list in subdomain_registry_data.items():
    if isinstance(sub_list, list):
        valid_subdomains[domain] = [s['code'] for s in sub_list]

valid_info_types = info_types_content.strip().split('\n')

criticality_levels_data = yaml.safe_load(criticality_levels_content)
valid_criticality_levels = [entry['level'] for entry in criticality_levels_data]

lifecycle_gatekeepers_data = yaml.safe_load(lifecycle_gatekeepers_content)
valid_lifecycle_gatekeepers = [entry['gatekeeper'] for entry in lifecycle_gatekeepers_data]

tag_glossary_fm, _ = parse_markdown_file_content(tag_glossary_content)
valid_kb_ids_from_glossary = []
valid_tags_from_glossary = {"status": [], "content-type": [], "topic": [], "criticality": [], "lifecycle_gatekeeper": [], "kb-id": []}
if tag_glossary_fm:
    valid_kb_ids_from_glossary = ["kb-id/standards", "kb-id/research-methodology", "kb-id/llm-cookbook", "kb-id/global"] # Manually from example
    tag_lines = tag_glossary_content.splitlines()
    for line in tag_lines:
        line = line.strip()
        for cat in ["status", "content-type", "topic", "criticality", "lifecycle_gatekeeper", "kb-id"]:
            if line.startswith(f"- `{cat}/"):
                try:
                    tag_value = line.split("`")[1]
                    valid_tags_from_glossary[cat].append(tag_value)
                except IndexError:
                    pass # Ignore malformed lines for this simple parser


# --- Frontmatter Schema Order ---
frontmatter_key_order = [
    'title', 'standard_id', 'aliases', 'tags', 'kb-id', 'info-type',
    'primary-topic', 'related-standards', 'version', 'date-created',
    'date-modified', 'primary_domain', 'sub_domain', 'scope_application',
    'criticality', 'lifecycle_gatekeeper', 'impact_areas', 'change_log_url'
]

standard_id_regex = r"^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$"
target_info_types = ["standard-definition", "policy-document", "guide-document"]
target_statuses = ["status/active", "status/draft"]
current_utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

structured_results = []

for i, file_content_loop_var in enumerate(target_files_content_raw):
    filename_loop_var = target_filenames[i]
    original_fm_loop_var, body_loop_var = parse_markdown_file_content(file_content_loop_var)
    processed_file_notes_loop_var = []

    if not original_fm_loop_var:
        structured_results.append({
            "filename": filename_loop_var, "status": "skipped", "reason": "Could not parse frontmatter.",
            "new_content": None, "notes": [f"{filename_loop_var}: Could not parse frontmatter. Skipping."]
        })
        continue

    current_info_type_loop_var = original_fm_loop_var.get('info-type')
    current_status_tags_loop_var = [tag for tag in original_fm_loop_var.get('tags', []) if tag.startswith("status/")]
    doc_status_loop_var = current_status_tags_loop_var[0] if current_status_tags_loop_var else "unknown"

    if not (doc_status_loop_var in target_statuses and current_info_type_loop_var in target_info_types):
        structured_results.append({
            "filename": filename_loop_var, "status": "skipped",
            "reason": f"Status: '{doc_status_loop_var}', Info-type: '{current_info_type_loop_var}'.",
            "new_content": None,
            "notes": [f"Note: {filename_loop_var} was skipped. Status: '{doc_status_loop_var}', Info-type: '{current_info_type_loop_var}'."]
        })
        continue

    new_fm_loop_var = {}
    standard_id_loop_var = original_fm_loop_var.get('standard_id')
    filename_base_loop_var = filename_loop_var.split('/')[-1].replace('.md', '')

    if standard_id_loop_var:
        if not re.match(standard_id_regex, standard_id_loop_var):
            processed_file_notes_loop_var.append(f"Warning: `standard_id` '{standard_id_loop_var}' does not match regex.")
        if standard_id_loop_var != filename_base_loop_var:
            processed_file_notes_loop_var.append(f"Warning: `standard_id` '{standard_id_loop_var}' does not match filename '{filename_base_loop_var}'.")
    else:
        standard_id_loop_var = "NEEDS_REVIEW_ID"
        processed_file_notes_loop_var.append(f"Warning: Missing mandatory `standard_id`. Added placeholder.")

    new_fm_loop_var['title'] = original_fm_loop_var.get('title', 'NEEDS_REVIEW_TITLE')
    if 'title' not in original_fm_loop_var: processed_file_notes_loop_var.append("Warning: Missing mandatory `title`.")
    new_fm_loop_var['standard_id'] = standard_id_loop_var

    aliases_loop_var = original_fm_loop_var.get('aliases')
    if aliases_loop_var is not None:
      if not isinstance(aliases_loop_var, list):
          aliases_loop_var = [str(aliases_loop_var)]
          processed_file_notes_loop_var.append("Warning: `aliases` was not a list. Converted to list.")
      new_fm_loop_var['aliases'] = [str(a) for a in aliases_loop_var]

    tags_loop_var = original_fm_loop_var.get('tags', [])
    if not isinstance(tags_loop_var, list):
        tags_loop_var = [str(tags_loop_var)]
        processed_file_notes_loop_var.append("Warning: `tags` was not a list. Converted to list.")
    validated_tags_loop_var = []
    has_status_tag_loop_var = False
    has_content_type_tag_loop_var = False
    for tag_val_loop_var in tags_loop_var:
        if not isinstance(tag_val_loop_var, str) or not re.match(r"^[a-z0-9/\._-]+$", tag_val_loop_var): # Relaxed kebab-case for tags like status/active etc.
            processed_file_notes_loop_var.append(f"Warning: Tag '{tag_val_loop_var}' may not be valid kebab-case/path-style. Keeping as is.")
        validated_tags_loop_var.append(tag_val_loop_var)
        if tag_val_loop_var.startswith("status/"):
            has_status_tag_loop_var = True
            if tag_val_loop_var not in valid_tags_from_glossary.get("status", []):
                 processed_file_notes_loop_var.append(f"Warning: Status tag '{tag_val_loop_var}' not in glossary.")
        if tag_val_loop_var.startswith("content-type/"):
            has_content_type_tag_loop_var = True
            simplified_tag_val_loop_var = tag_val_loop_var.replace("content-type/", "")
            if simplified_tag_val_loop_var not in valid_info_types and tag_val_loop_var not in valid_tags_from_glossary.get("content-type",[]):
                 processed_file_notes_loop_var.append(f"Warning: Content-type tag '{tag_val_loop_var}' not in info_types or glossary.")
    if not has_status_tag_loop_var:
        validated_tags_loop_var.append("status/NEEDS_REVIEW")
        processed_file_notes_loop_var.append("Warning: Missing `status/*` tag. Added placeholder.")
    if not has_content_type_tag_loop_var:
        inferred_ct_tag_loop_var = f"content-type/{current_info_type_loop_var}"
        # Check against combined list: info_types (raw) and content-type tags from glossary
        combined_valid_content_tags = valid_info_types + [ct.replace("content-type/","") for ct in valid_tags_from_glossary.get("content-type",[])]
        if current_info_type_loop_var and current_info_type_loop_var in combined_valid_content_tags :
             # It's a valid info-type, so the tag form should be acceptable or added to glossary
            validated_tags_loop_var.append(inferred_ct_tag_loop_var)
            if inferred_ct_tag_loop_var not in valid_tags_from_glossary.get("content-type",[]):
                 processed_file_notes_loop_var.append(f"Note: Inferred content-type tag '{inferred_ct_tag_loop_var}' from info-type; consider adding to glossary if not present.")
        else:
            validated_tags_loop_var.append("content-type/NEEDS_REVIEW")
            processed_file_notes_loop_var.append("Warning: Missing `content-type/*` tag or info-type cannot be mapped to a valid tag. Added placeholder.")
    new_fm_loop_var['tags'] = validated_tags_loop_var
    if 'tags' not in original_fm_loop_var: processed_file_notes_loop_var.append("Warning: Missing mandatory `tags`.")

    kb_id_val_loop_var = original_fm_loop_var.get('kb-id')
    if kb_id_val_loop_var:
        # Use kb-id tags from glossary for validation:
        kb_id_tag_form = f"kb-id/{kb_id_val_loop_var}" if not kb_id_val_loop_var.startswith("kb-id/") else kb_id_val_loop_var
        if kb_id_tag_form not in valid_tags_from_glossary.get("kb-id", []): # Check against kb-id/* tags
             processed_file_notes_loop_var.append(f"Warning: `kb-id` '{kb_id_val_loop_var}' (as tag '{kb_id_tag_form}') not in glossary kb-id tags. Keeping as is.")
        new_fm_loop_var['kb-id'] = kb_id_val_loop_var # Store the raw kb-id, not the tag form
    else:
        new_fm_loop_var['kb-id'] = "NEEDS_REVIEW_KB_ID"
        processed_file_notes_loop_var.append("Warning: Missing mandatory `kb-id`. Added placeholder.")

    info_type_val_loop_var = original_fm_loop_var.get('info-type')
    if info_type_val_loop_var:
        if info_type_val_loop_var not in valid_info_types:
            processed_file_notes_loop_var.append(f"Warning: `info-type` '{info_type_val_loop_var}' not in `info_types.txt`. Keeping as is.")
        new_fm_loop_var['info-type'] = info_type_val_loop_var
    else:
        new_fm_loop_var['info-type'] = "NEEDS_REVIEW_INFO_TYPE"
        processed_file_notes_loop_var.append("Warning: Missing mandatory `info-type`. Added placeholder.")

    new_fm_loop_var['primary-topic'] = original_fm_loop_var.get('primary-topic', 'NEEDS_REVIEW_PRIMARY_TOPIC')
    if 'primary-topic' not in original_fm_loop_var: processed_file_notes_loop_var.append("Warning: Missing mandatory `primary-topic`.")

    related_standards_loop_var = original_fm_loop_var.get('related-standards')
    if related_standards_loop_var is not None:
        if not isinstance(related_standards_loop_var, list):
            related_standards_loop_var = [str(related_standards_loop_var)]
            processed_file_notes_loop_var.append("Warning: `related-standards` was not a list. Converted to list.")
        new_fm_loop_var['related-standards'] = [str(rs) for rs in related_standards_loop_var]

    version_val_loop_var = original_fm_loop_var.get('version')
    if version_val_loop_var is not None:
        new_fm_loop_var['version'] = str(version_val_loop_var)
    else:
        new_fm_loop_var['version'] = "0.0.0" # Placeholder
        processed_file_notes_loop_var.append("Warning: Missing mandatory `version`. Added placeholder '0.0.0'.")

    date_created_val_loop_var = original_fm_loop_var.get('date-created')
    if date_created_val_loop_var:
        try:
            # Attempt to parse, accepting if it's already a datetime object (less likely from raw parse) or string
            if isinstance(date_created_val_loop_var, datetime):
                 new_fm_loop_var['date-created'] = date_created_val_loop_var.strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                datetime.strptime(str(date_created_val_loop_var).replace("Z", "").split('.')[0], '%Y-%m-%dT%H:%M:%S') # Handle potential millis
                new_fm_loop_var['date-created'] = str(date_created_val_loop_var)
        except ValueError:
            processed_file_notes_loop_var.append(f"Warning: `date-created` '{date_created_val_loop_var}' not valid ISO-8601. Keeping as is.")
            new_fm_loop_var['date-created'] = str(date_created_val_loop_var)
    else:
        new_fm_loop_var['date-created'] = "NEEDS_REVIEW_DATE"
        processed_file_notes_loop_var.append("Warning: Missing mandatory `date-created`. Added placeholder.")

    new_fm_loop_var['date-modified'] = current_utc_time

    primary_domain_val_loop_var = original_fm_loop_var.get('primary_domain')
    if primary_domain_val_loop_var:
        if primary_domain_val_loop_var not in valid_domain_codes:
            processed_file_notes_loop_var.append(f"Warning: `primary_domain` '{primary_domain_val_loop_var}' not in `domain_codes.yaml`. Keeping as is.")
        new_fm_loop_var['primary_domain'] = primary_domain_val_loop_var
    else:
        new_fm_loop_var['primary_domain'] = "TBD"
        processed_file_notes_loop_var.append("Warning: Missing mandatory `primary_domain` for this doc type. Added placeholder 'TBD'.")

    sub_domain_val_loop_var = original_fm_loop_var.get('sub_domain')
    current_primary_domain_loop_var = new_fm_loop_var.get('primary_domain', "")
    if sub_domain_val_loop_var:
        if current_primary_domain_loop_var in valid_subdomains:
            if sub_domain_val_loop_var not in valid_subdomains[current_primary_domain_loop_var]:
                processed_file_notes_loop_var.append(f"Warning: `sub_domain` '{sub_domain_val_loop_var}' not valid for primary_domain '{current_primary_domain_loop_var}'. Keeping as is.")
        elif current_primary_domain_loop_var != "TBD": # Only warn if primary domain was supposed to be valid
            processed_file_notes_loop_var.append(f"Warning: Cannot validate `sub_domain` '{sub_domain_val_loop_var}' as primary_domain '{current_primary_domain_loop_var}' is invalid or missing. Keeping as is.")
        new_fm_loop_var['sub_domain'] = sub_domain_val_loop_var
    else:
        new_fm_loop_var['sub_domain'] = "TBD"
        processed_file_notes_loop_var.append("Warning: Missing mandatory `sub_domain` for this doc type. Added placeholder 'TBD'.")

    new_fm_loop_var['scope_application'] = original_fm_loop_var.get('scope_application', 'NEEDS_REVIEW_SCOPE')
    if 'scope_application' not in original_fm_loop_var: processed_file_notes_loop_var.append("Warning: Missing mandatory `scope_application`.")

    criticality_val_loop_var = original_fm_loop_var.get('criticality')
    if criticality_val_loop_var:
        if criticality_val_loop_var not in valid_criticality_levels:
            processed_file_notes_loop_var.append(f"Warning: `criticality` '{criticality_val_loop_var}' not in `criticality_levels.yaml`. Keeping as is.")
        new_fm_loop_var['criticality'] = criticality_val_loop_var
    else:
        new_fm_loop_var['criticality'] = "TBD" # Placeholder
        processed_file_notes_loop_var.append("Warning: Missing mandatory `criticality`. Added placeholder 'TBD'.")

    lifecycle_gatekeeper_val_loop_var = original_fm_loop_var.get('lifecycle_gatekeeper')
    if lifecycle_gatekeeper_val_loop_var:
        if lifecycle_gatekeeper_val_loop_var not in valid_lifecycle_gatekeepers:
            processed_file_notes_loop_var.append(f"Warning: `lifecycle_gatekeeper` '{lifecycle_gatekeeper_val_loop_var}' not in `lifecycle_gatekeepers.yaml`. Keeping as is.")
        new_fm_loop_var['lifecycle_gatekeeper'] = lifecycle_gatekeeper_val_loop_var
    else:
        new_fm_loop_var['lifecycle_gatekeeper'] = "TBD" # Placeholder
        processed_file_notes_loop_var.append("Warning: Missing mandatory `lifecycle_gatekeeper`. Added placeholder 'TBD'.")

    impact_areas_loop_var = original_fm_loop_var.get('impact_areas', []) # Optional in schema, but good to have a default
    if 'impact_areas' not in original_fm_loop_var:
         processed_file_notes_loop_var.append("Warning: Missing mandatory `impact_areas`. Added empty list placeholder.")
         new_fm_loop_var['impact_areas'] = []
    elif not isinstance(impact_areas_loop_var, list):
        impact_areas_loop_var = [str(impact_areas_loop_var)]
        processed_file_notes_loop_var.append("Warning: `impact_areas` was not a list. Converted to list.")
        new_fm_loop_var['impact_areas'] = [str(ia) for ia in impact_areas_loop_var]
    else:
        new_fm_loop_var['impact_areas'] = [str(ia) for ia in impact_areas_loop_var]


    change_log_url_loop_var = original_fm_loop_var.get('change_log_url')
    if change_log_url_loop_var:
        if not str(change_log_url_loop_var).startswith("./"):
             processed_file_notes_loop_var.append(f"Warning: `change_log_url` '{change_log_url_loop_var}' does not start with './'. Keeping as is.")
        new_fm_loop_var['change_log_url'] = str(change_log_url_loop_var)
    else:
        new_fm_loop_var['change_log_url'] = f"./{filename_base_loop_var}-CHANGELOG.MD" # Placeholder
        processed_file_notes_loop_var.append("Warning: Missing mandatory `change_log_url`. Added placeholder based on filename.")

    ordered_fm_loop_var = {key: new_fm_loop_var[key] for key in frontmatter_key_order if key in new_fm_loop_var}
    for key_loop_var in new_fm_loop_var:
        if key_loop_var not in ordered_fm_loop_var: # Should not happen if schema is complete and all keys handled
            ordered_fm_loop_var[key_loop_var] = new_fm_loop_var[key_loop_var]
            processed_file_notes_loop_var.append(f"DevWarning: Key '{key_loop_var}' processed but not in schema order list, appended.")

    new_frontmatter_yaml_loop_var = yaml.dump(ordered_fm_loop_var, sort_keys=False, Dumper=NoAliasDumper, width=1000, allow_unicode=True)
    updated_content_loop_var = f"---\n{new_frontmatter_yaml_loop_var}---\n{body_loop_var}"

    structured_results.append({
        "filename": filename_loop_var, "status": "processed", "new_content": updated_content_loop_var,
        "notes": processed_file_notes_loop_var
    })

# --- Construct final output string for the tool ---
script_stdout_parts = []
for res in structured_results:
    if res["status"] == "processed" and res["new_content"]:
        script_stdout_parts.append(f"--- START OF {res['filename']} ---\n{res['new_content']}\n--- END OF {res['filename']} ---")
    else:
        script_stdout_parts.append(f"--- SKIPPED: {res['filename']} (Reason: {res['reason']}) ---")
    if res["notes"]: # Always include notes if present
        script_stdout_parts.append(f"--- NOTES FOR {res['filename']} ---\n" + "\n".join(res["notes"]) + f"\n--- END OF NOTES FOR {res['filename']} ---")

print("\n\n".join(script_stdout_parts))
