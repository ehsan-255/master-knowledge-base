---
title: 'Guide: Knowledge Base Usage and Standards'
aliases:
- KB Onboarding Guide
- How to Use This KB
- U-ONBOARDING-001 Guide
tags:
- content-type/standards-guide
- criticality/p0-critical
- kb-id/standards
- status/deprecated
- topic/onboarding
- topic/standards-governance
- topic/user-documentation
kb-id: standards
info-type: standards-guide
primary-topic: Comprehensive guide for users on how to navigate, understand, apply,
  and contribute to the knowledge base system and its standards.
related-standards:
- U-ONBOARDING-001
- U-METADATA-FRONTMATTER-RULES-001
- U-TAG-001
version: 0.2.0
date-created: '2025-05-22'
date-modified: '2025-06-17T02:29:13Z'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: [[GM-GUIDE-KB-USAGE]].

# Guide: Knowledge Base Usage and Standards

This guide provides comprehensive information for all users on how to effectively navigate, understand, apply, and contribute to this knowledge base (KB) system and its underlying standards. Adherence to these guidelines ensures consistency, quality, and maintainability of our collective knowledge.

## 1. Introduction

### 1.1 Purpose of This Guide
This guide serves as the primary onboarding resource for new users and a reference for all contributors. It explains the structure of our knowledge base ecosystem, the core standards governing content creation and management, and the tools and processes designed to support your work.

### 1.2 Importance of Standards in the KB Ecosystem
Standardization is crucial for:
-   **Consistency:** Ensuring all content has a predictable structure and style.
-   **Quality:** Maintaining accuracy, clarity, and completeness.
-   **Discoverability:** Enabling users to find information easily through standardized metadata and linking.
-   **Maintainability:** Simplifying updates and revisions across the KB.
-   **Automation:** Allowing scripts and tools to process and manage content reliably.

### 1.3 Overview of the KB's Operational Model (Source-and-Render)
Our KB system utilizes a "Source-and-Render" model.
-   **Source Documents (`./master-knowledge-base/`):** This is where all content is authored and edited. These files may contain placeholders like keyrefs (`{{key.name}}`) and conditional text markers (`> [!IF ...]`).
-   **Rendered Documents (`./master-knowledge-base-rendered/`):** A "Resolver Script" processes source documents to produce fully populated, "rendered" versions. These are primarily for consumption by humans (for a consistent view) and by LLMs (which require fully resolved text).
-   Refer to [[root|Universal Knowledge Base Standards - Overview]] for more details on this model.

## 2. Getting Started

### 2.1 Navigating the Knowledge Bases
-   **Master KB Directory:** Start at `[[master-knowledge-base/kb-directory|KB Directory]]` to see a list of all available knowledge bases, their descriptions, and links to their main entry points.
-   **KB Root Files:** Each individual KB (e.g., "Standards KB," "LLM Cookbook KB") has a `root.md` file (e.g., `[[Standards/root|Standards KB Root]]`) that serves as its master table of contents and entry point.
-   **Part Overview Files:** Larger KBs are divided into "Parts." Each Part typically has an `_overview.md` file (e.g., `[[Standards/KB-Specific-Standards/_overview|KB-Specific Standards Overview]]`) that provides a table of contents for the chapters within that part.

### 2.2 Finding Relevant Standards
-   **Standards KB Root:** The `[[Standards/root|Standards KB Root]]` provides a master table of contents for all universal and specific standards.
-   **Task-Based Guide:** For a task-oriented view, consult the `[[Standards/GUIDE-TASK-BASED|Task-Based Guide to Knowledge Base Standards]]`.
-   **Search:** Utilize your Markdown editor's search functionality (e.g., Obsidian search) to find standards by ID (e.g., `U-STRUC-002`) or keywords.

## 3. Core Authoring Workflow (Tutorial Style)

This section guides you through creating a typical content document.

### 3.1 Creating a New Content Document
1.  **Choose a Template (Recommended):** Navigate to the `[[master-knowledge-base/templates|Templates Directory]]` and copy an appropriate template (e.g., `[[master-knowledge-base/templates/chapter-template|Chapter Template]]`) to your target KB location.
2.  **File Naming:** Name your new file according to `[[Standards/COL-ARCH-UNIVERSAL#Standard: File and Folder Naming Conventions (U-FORMAT-NAMING-001)|U-FORMAT-NAMING-001]]` (lowercase kebab-case, descriptive, optional numerical prefix for sequencing).
3.  **Initial Frontmatter:** Populate all 10 canonical YAML frontmatter keys as defined in `[[Standards/U-METADATA-FRONTMATTER-RULES-001|Frontmatter Structure and Content Rules]]`. Pay close attention to `title`, `kb-id`, `content-type` tag, `info-type`, `status/draft` tag, and `topic/*` tags.

### 3.2 Understanding and Applying Document Structure (`U-STRUC-002`)
All core content documents ("chapters") MUST follow `[[Standards/COL-ARCH-UNIVERSAL#Standard: Content Document ("Chapter") Internal Structure (U-STRUC-002)|U-STRUC-002]]`:
-   **Single H1:** The document title, matching the `title:` in frontmatter.
-   **Abstract:** 1-3 paragraphs immediately after H1, summarizing purpose, scope, and takeaways.
-   **Table of Contents (ToC):** Links to all H2 (and significant H3) sections.
-   **Hierarchical Sections:** Use H2-H6 for content, no skipped levels.
-   **Summary:** A concluding H2 section.
-   **See Also:** An H2 section for links to related content.

### 3.3 Writing with Clarity and Objectivity (`U-TONE-LANG-001`)
Adhere to `[[Standards/COL-CONTENT-UNIVERSAL#Standard: Clarity, Objectivity, and Consistency in Language (U-TONE-LANG-001)|U-TONE-LANG-001]]`:
-   Use clear, concise, precise, and unambiguous language.
-   Maintain an objective, academic, and informative tone.
-   Use domain terminology consistently; define acronyms on first use.
-   Prefer active voice.

### 3.4 Essential Markdown Syntax
Consistently use the following Markdown syntax as defined in `[[Standards/COL-SYNTAX-MARKDOWN|Markdown Syntax Conventions]]`:
-   Headings: `[[Standards/COL-SYNTAX-MARKDOWN#Standard: Markdown for Headings (M-SYNTAX-HEADINGS-001)|M-SYNTAX-HEADINGS-001]]` (ATX style, single space, no skipped levels).
-   Lists: `[[Standards/COL-SYNTAX-MARKDOWN#Standard: Markdown for Lists (Ordered and Unordered) (M-SYNTAX-LISTS-001)|M-SYNTAX-LISTS-001]]` (hyphen for unordered, `1.` for ordered, 2-space indent for nesting).
-   Links: `[[Standards/COL-SYNTAX-MARKDOWN#Standard: Markdown for Links (Internal and External) (M-SYNTAX-LINKS-001)|M-SYNTAX-LINKS-001]]` and Obsidian-specific `[[Standards/COL-TOOLING-OBSIDIAN#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)|O-USAGE-LINKS-001]]`.

## 4. Metadata and Tagging (How-To Style)

### 4.1 Populating Canonical Frontmatter (`U-METADATA-FRONTMATTER-RULES-001`)
Every document requires YAML frontmatter with 10 canonical keys in a specific order. Refer to `[[Standards/U-METADATA-FRONTMATTER-RULES-001|Frontmatter Structure and Content Rules]]` for detailed rules on each key:
1.  `title`
2.  `aliases`
3.  `tags`
4.  `kb-id`
5.  `info-type` (kebab-case values)
6.  `primary-topic`
7.  `related-standards`
8.  `version` (quoted string, e.g., `'0.1.0'`)
9.  `date-created` (`YYYY-MM-DD`)
10. `date-modified` (`YYYY-MM-DD`)

### 4.2 Understanding `info-type` vs. `content-type`
-   **`content-type/*` (Tag):** A hierarchical tag for broad categorization, filtering, and navigation (e.g., `content-type/standard-document`). Values from `[[master-knowledge-base/tag-glossary-definition|Tag Glossary]]`.
-   **`info-type` (YAML Key):** A specific, non-hierarchical kebab-case string mapping to a processing instruction or schema (e.g., `standard-document`). Critical for automation. Vocabulary in `[[Standards/U-METADATA-FRONTMATTER-RULES-001|U-METADATA-FRONTMATTER-RULES-001]]`.

### 4.3 Applying Tags Effectively (`U-TAG-001`)
-   Tags are defined in YAML frontmatter under the `tags:` key.
-   All tags use kebab-case. Hierarchy with `/`.
-   Mandatory tag categories:
    -   One `kb-id/{id}` (e.g., `kb-id/standards`)
    -   One `content-type/{type}` (e.g., `content-type/standard-document`)
    -   One `status/{status}` (e.g., `status/draft`)
    -   At least one `topic/{topic}` (e.g., `topic/metadata`)
-   Consult the `[[master-knowledge-base/tag-glossary-definition|Tag Glossary]]` for official tags and their meanings. Refer to `[[Standards/COL-LINKING-UNIVERSAL#Standard: Core Tagging Strategy for KB Content (U-TAG-001)|U-TAG-001]]` for the full strategy.

## 5. Advanced Authoring Features (How-To Style)

### 5.1 Using Keyrefs (`U-KEYREF-SYNTAX-001`)
-   Keyrefs allow you to insert reusable text snippets (e.g., product names, URLs) defined in `[[master-knowledge-base/_key_definitions|Global Key Definitions]]`.
-   Syntax: `{{key.yourKeyName}}` (e.g., `{{key.productName}}`).
-   Refer to `[[Standards/U-KEYREF-SYNTAX-001|Key-Based Referencing Syntax]]` and `[[Standards/U-KEYREF-MANAGEMENT-001|Key-Based Referencing Management]]`.

### 5.2 Implementing Conditional Content (`M-CONDITIONAL-TEXT-SYNTAX-001`)
-   Mark text blocks for specific audiences or platforms using Obsidian callouts: `> [!IF attribute=value AND attribute2=value2]`.
-   Attributes and values are defined in `[[Standards/U-PROFILING-ATTRIBUTES-001|Profiling Attributes and Values]]`.
-   Example: `> [!IF audience=expert AND platform=linux]`
-   Refer to `[[Standards/M-CONDITIONAL-TEXT-SYNTAX-001|Markdown Syntax for Conditional Text]]`.

### 5.3 Working with Specific Content Schemas (`U-SCHEMA-*`)
Certain document types have specific structural requirements defined by `U-SCHEMA-*` standards:
-   Methodology/Technique Descriptions: `[[Standards/COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Methodology/Technique Descriptions" (U-SCHEMA-METHOD-001)|U-SCHEMA-METHOD-001]]`
-   Concept Definitions: `[[Standards/COL-CONTENT-UNIVERSAL#Standard: Content Schema for "Concept Definitions" (U-SCHEMA-CONCEPT-001)|U-SCHEMA-CONCEPT-001]]`
-   Reference Topics: `[[Standards/U-SCHEMA-REFERENCE-001|U-SCHEMA-REFERENCE-001]]`
-   Task Topics: `[[Standards/U-SCHEMA-TASK-001|U-SCHEMA-TASK-001]]`
-   Consult these standards and use templates from `[[master-knowledge-base/templates|Templates Directory]]` when creating such documents.

## 6. Using Obsidian (Obsidian User Specific)

*(Note: This section details conventions for users of the Obsidian Markdown editor. If you use a different editor, these specific features may not apply, but the underlying Markdown standards still do.)*

### 6.1 Obsidian Linking Conventions (`O-USAGE-LINKS-001`)
-   Use Wikilinks: `[[path/from/master-kb-root/to/file#Optional Heading|Optional Display Text]]`.
-   Paths MUST start from the `master-knowledge-base` root (e.g., `[[Standards/U-ARCH-001]]`).
-   Utilize Obsidian's path autocompletion.
-   Refer to `[[Standards/COL-TOOLING-OBSIDIAN#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)|O-USAGE-LINKS-001]]`.

### 6.2 Obsidian Tagging (`O-USAGE-TAGS-001`)
-   Tags are primarily managed in YAML frontmatter.
-   Use Obsidian's "Tags" pane for navigation.
-   The "Tag Wrangler" plugin is recommended for tag management.
-   Refer to `[[Standards/COL-TOOLING-OBSIDIAN#Standard: Obsidian Tag Implementation (O-USAGE-TAGS-001)|O-USAGE-TAGS-001]]`.

### 6.3 Obsidian Content Embedding/Transclusion (`O-USAGE-TRANSCLUSION-001`)
-   Embed content from other notes using `![[filename#^blockID]]` or `![[filename#Section Heading]]`.
-   Use `![[filename]]` for entire notes.
-   Refer to `[[Standards/COL-TOOLING-OBSIDIAN#Standard: Obsidian Content Embedding (Transclusion) (O-USAGE-TRANSCLUSION-001)|O-USAGE-TRANSCLUSION-001]]`.

### 6.4 Obsidian Callouts (`O-USAGE-CALLOUTS-001`)
-   Use `> [!TYPE] Optional Title` for admonitions (NOTE, WARNING, TIP, etc.).
-   Use semantically (e.g., `[!WARNING]` for actual warnings).
-   Refer to `[[Standards/COL-TOOLING-OBSIDIAN#Standard: Obsidian Callout Usage (O-USAGE-CALLOUTS-001)|O-USAGE-CALLOUTS-001]]`.

## 7. LLM-Assisted Content Generation (Tutorial/How-To Style)

### 7.1 Introduction to the LLM Content Generation Cookbook
-   The `[[llm-content-generation-cookbook-kb/root|LLM Content Generation Cookbook KB]]` provides recipes and best practices for using Large Language Models (LLMs) to assist with content creation.

### 7.2 How to Use Recipes and Prompt Templates
-   Cookbook recipes (e.g., `[[llm-content-generation-cookbook-kb/part-ii-recipes/01-recipe-methodology-schema|Recipe: Generating a Methodology Description]]`) provide structured prompts.
-   These prompts reference versioned prompt templates from `[[master-knowledge-base/llm-io/llm-prompts|LLM Prompt Library]]` and I/O schemas from `[[master-knowledge-base/llm-io/llm-io-schemas|LLM I/O Schemas]]`.
-   Follow the input variable guidance in each recipe.

### 7.3 Critical Human Review and Validation of LLM Output
-   **LLM output is a DRAFT, not final content.**
-   Always critically review LLM-generated text for:
    -   Factual accuracy (LLMs can "hallucinate").
    -   Adherence to all KB standards (structure, tone, metadata, syntax).
    -   Clarity, coherence, and completeness.
-   Edit LLM output thoroughly before marking content as `status/final`.

## 8. Governance and Contribution (Reference/Explanation Style)

### 8.1 Process for Proposing Changes to Standards (`U-GOVERNANCE-001`)
-   Refer to `[[Standards/COL-GOVERNANCE-UNIVERSAL#Standard: Governance - Proposing and Updating Standards (U-GOVERNANCE-001)|U-GOVERNANCE-001]]` for the documented process on how to propose new standards or suggest modifications to existing ones.

### 8.2 Versioning and Changelogs (`U-VERSIONING-001`)
-   Standards documents (and other key documents) are versioned using semantic versioning (e.g., `version: '1.0.1'`) in their frontmatter.
-   Significant changes are noted in a "Changelog" section within the standard.
-   Refer to `[[Standards/COL-GOVERNANCE-UNIVERSAL#Standard: Versioning and Changelogs for Standard Files (U-VERSIONING-001)|U-VERSIONING-001]]`.

### 8.3 Deprecation Policy (`U-DEPRECATION-001`)
-   Superseded or irrelevant standards are marked as deprecated, not deleted, to maintain historical context.
-   Refer to `[[Standards/COL-GOVERNANCE-UNIVERSAL#Standard: Deprecation Policy for Standards (U-DEPRECATION-001)|U-DEPRECATION-001]]`.

### 8.4 Using the TODO System (`M-SYNTAX-TODO-001`)
-   Mark pending actions or notes for future work directly in documents using HTML comments: `<!-- TODO [YYYY-MM-DD Assignee]: Description. -->`.
-   Refer to `[[Standards/M-SYNTAX-TODO-001|Markdown Syntax for TODO Items]]`.
-   Major TODOs are aggregated in the `[[master-knowledge-base/TODO-MASTER-LIST|Master TODO List]]`.

## 9. Glossaries and Further Help

-   **Standards Terminology:** For definitions of terms used within the standards documents themselves, see `[[Standards/GLOSSARY-STANDARDS-TERMS|Glossary of Standards Terminology]]`.
-   **Tag Glossary:** For definitions of all official tags used in YAML frontmatter, see `[[master-knowledge-base/tag-glossary-definition|Tag Glossary]]`.
-   **Questions:** If you have questions or need clarification, please [Specify Contact Point or Channel, e.g., "reach out on the #kb-standards channel" or "contact Jim"].

---
