---
title: "Guide: Knowledge Base Usage and Standards"
standard_id: "GM-GUIDE-KB-USAGE"
aliases: ["KB Onboarding Guide", "How to Use This KB", "KB Usage Guide"]
tags:
  - status/draft
  - content-type/guide-document
  - topic/onboarding
  - topic/standards-governance
  - topic/user-documentation
  - topic/knowledge-management
  - topic/content-authoring
kb-id: "standards"
info-type: "guide-document"
primary-topic: "Comprehensive guide for users on how to navigate, understand, apply, and contribute to the knowledge base system and its standards."
related-standards: [
    "GM-MANDATE-KB-USAGE-GUIDE", 
    "AS-INDEX-KB-MASTER", 
    "SF-CONVENTIONS-NAMING", 
    "AS-STRUCTURE-KB-ROOT", 
    "AS-STRUCTURE-KB-PART", 
    "CS-POLICY-PART-OVERVIEW", 
    "AS-STRUCTURE-DOC-CHAPTER", 
    "AS-ROOT-STANDARDS-KB", 
    "AS-STRUCTURE-TEMPLATES-DIRECTORY",
    "CS-TOC-POLICY", 
    "SF-TOC-SYNTAX", 
    "SF-LINKS-INTERNAL-SYNTAX", 
    "MT-TAGGING-STRATEGY-POLICY", 
    "MT-REGISTRY-TAG-GLOSSARY",
    "MT-SCHEMA-FRONTMATTER",
    "CS-POLICY-TONE-LANGUAGE",
    "SF-SYNTAX-HEADINGS",
    "SF-SYNTAX-LISTS",
    "SF-SYNTAX-LINKS-GENERAL",
    "UA-KEYDEFS-GLOBAL",
    "SF-SYNTAX-KEYREF",
    "MT-KEYREF-MANAGEMENT",
    "CS-CONTENT-PROFILING-POLICY",
    "SF-CONDITIONAL-SYNTAX-ATTRIBUTES",
    "AS-SCHEMA-METHODOLOGY-DESCRIPTION",
    "AS-SCHEMA-CONCEPT-DEFINITION",
    "AS-SCHEMA-REFERENCE",
    "AS-SCHEMA-TASK",
    "CS-LINKING-INTERNAL-POLICY",
    "MT-TAGS-IMPLEMENTATION",
    "SF-TRANSCLUSION-SYNTAX",
    "CS-MODULARITY-TRANSCLUSION-POLICY",
    "SF-CALLOUTS-SYNTAX",
    "CS-ADMONITIONS-POLICY",
    "OM-POLICY-STANDARDS-GOVERNANCE",
    "OM-VERSIONING-CHANGELOGS",
    "OM-POLICY-STANDARDS-DEPRECATION",
    "GM-GLOSSARY-STANDARDS-TERMS",
    "GM-GUIDE-STANDARDS-BY-TASK"
    ]
version: "0.1.0"
date-created: "2025-05-29T11:51:19Z" # Placeholder
date-modified: "2025-05-29T15:53:52Z"
primary_domain: "GM"
sub_domain: "GUIDE"
scope_application: "Provides guidance for all users and contributors on utilizing the knowledge base and its standards."
criticality: "P1-High"
lifecycle_gatekeeper: "Editorial-Board-Approval"
impact_areas: ["User Onboarding", "Standards Adoption", "KB Navigation", "Contribution Process"]
change_log_url: "./GM-GUIDE-KB-USAGE-changelog.md"
---

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
-   Refer to [[AS-ROOT-STANDARDS-KB]] for more details on this model.

## 2. Getting Started

### 2.1 Navigating the Knowledge Bases
-   **Master KB Directory:** Start at `[[AS-INDEX-KB-MASTER]]` to see a list of all available knowledge bases, their descriptions, and links to their main entry points.
-   **KB Root Files:** Each individual KB (e.g., "Standards KB," "LLM Cookbook KB") has a `root.md` file (e.g., `[[AS-ROOT-STANDARDS-KB]]`) that serves as its master table of contents and entry point.
-   **Part Overview Files:** Larger KBs are divided into "Parts." Each Part typically has an `_overview.md` file that provides a table of contents for the chapters within that part.

### 2.2 Finding Relevant Standards
-   **Standards KB Root:** The `[[AS-ROOT-STANDARDS-KB]]` provides a master table of contents for all universal and specific standards.
-   **Task-Based Guide:** For a task-oriented view, consult the `[[GM-GUIDE-STANDARDS-BY-TASK]]`.
-   **Search:** Utilize your Markdown editor's search functionality (e.g., Obsidian search) to find standards by ID (e.g., `AS-STRUCTURE-DOC-CHAPTER`) or keywords.

## 3. Core Authoring Workflow (Tutorial Style)

This section guides you through creating a typical content document.

### 3.1 Creating a New Content Document
1.  **Choose a Template (Recommended):** Navigate to the `[[AS-STRUCTURE-TEMPLATES-DIRECTORY]]` and copy an appropriate template (e.g., `[[master-knowledge-base/templates/tpl-chapter-template.md|Chapter Template]]`) to your target KB location. 
2.  **File Naming:** Name your new file according to `[[SF-CONVENTIONS-NAMING]]` (lowercase kebab-case, descriptive, optional numerical prefix for sequencing).
3.  **Initial Frontmatter:** Populate all 10 canonical YAML frontmatter keys as defined in `[[MT-SCHEMA-FRONTMATTER]]`. Pay close attention to `title`, `kb-id`, `content-type` tag, `info-type`, `status/draft` tag, and `topic/*` tags.

### 3.2 Understanding and Applying Document Structure (`AS-STRUCTURE-DOC-CHAPTER`)
All core content documents ("chapters") MUST follow `[[AS-STRUCTURE-DOC-CHAPTER]]`:
-   **Single H1:** The document title, matching the `title:` in frontmatter.
-   **Abstract:** 1-3 paragraphs immediately after H1, summarizing purpose, scope, and takeaways.
-   **Table of Contents (ToC):** Links to all H2 (and significant H3) sections. See [[CS-TOC-POLICY]] and [[SF-TOC-SYNTAX]].
-   **Hierarchical Sections:** Use H2-H6 for content, no skipped levels.
-   **Summary:** A concluding H2 section.
-   **See Also:** An H2 section for links to related content.

### 3.3 Writing with Clarity and Objectivity (`CS-POLICY-TONE-LANGUAGE`)
Adhere to `[[CS-POLICY-TONE-LANGUAGE]]`:
-   Use clear, concise, precise, and unambiguous language.
-   Maintain an objective, academic, and informative tone.
-   Use domain terminology consistently; define acronyms on first use.
-   Prefer active voice.

### 3.4 Essential Markdown Syntax
Consistently use the following Markdown syntax as defined in `[[SF-FORMATTING-MARKDOWN-GENERAL]]`:
-   Headings: `[[SF-SYNTAX-HEADINGS]]` (ATX style, single space, no skipped levels).
-   Lists: `[[SF-SYNTAX-LISTS]]` (hyphen for unordered, `1.` for ordered, 2-space indent for nesting).
-   Links: `[[SF-SYNTAX-LINKS-GENERAL]]` and Obsidian-specific `[[SF-LINKS-INTERNAL-SYNTAX]]`.

## 4. Metadata and Tagging (How-To Style)

### 4.1 Populating Canonical Frontmatter (`MT-SCHEMA-FRONTMATTER`)
Every document requires YAML frontmatter with 10 canonical keys in a specific order. Refer to `[[MT-SCHEMA-FRONTMATTER]]` for detailed rules on each key:
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
-   **`content-type/*` (Tag):** A hierarchical tag for broad categorization, filtering, and navigation (e.g., `content-type/standard-document`). Values from `[[MT-REGISTRY-TAG-GLOSSARY]]`.
-   **`info-type` (YAML Key):** A specific, non-hierarchical kebab-case string mapping to a processing instruction or schema (e.g., `standard-document`). Critical for automation. Vocabulary in `[[MT-SCHEMA-FRONTMATTER]]`.

### 4.3 Applying Tags Effectively (`MT-TAGGING-STRATEGY-POLICY`)
-   Tags are defined in YAML frontmatter under the `tags:` key.
-   All tags use kebab-case. Hierarchy with `/`.
-   Mandatory tag categories:
    -   One `kb-id/{id}` (e.g., `kb-id/standards`)
    -   One `content-type/{type}` (e.g., `content-type/standard-document`)
    -   One `status/{status}` (e.g., `status/draft`)
    -   At least one `topic/{topic}` (e.g., `topic/metadata`)
-   Consult the `[[MT-REGISTRY-TAG-GLOSSARY]]` for official tags and their meanings. Refer to `[[MT-TAGGING-STRATEGY-POLICY]]` for the full strategy.

## 5. Advanced Authoring Features (How-To Style)

### 5.1 Using Keyrefs (`SF-SYNTAX-KEYREF`)
-   Keyrefs allow you to insert reusable text snippets (e.g., product names, URLs) defined in `[[UA-KEYDEFS-GLOBAL]]`.
-   Syntax: `{{key.yourKeyName}}` (e.g., `{{key.productName}}`).
-   Refer to `[[SF-SYNTAX-KEYREF]]` and `[[MT-KEYREF-MANAGEMENT]]`.

### 5.2 Implementing Conditional Content (`SF-CONDITIONAL-SYNTAX-ATTRIBUTES`)
-   Mark text blocks for specific audiences or platforms using Obsidian callouts: `> [!IF attribute=value AND attribute2=value2]`.
-   Attributes and values are defined in `[[CS-CONTENT-PROFILING-POLICY]]`.
-   Example: `> [!IF audience=expert AND platform=linux]`
-   Refer to `[[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]]`.

### 5.3 Working with Specific Content Schemas
Certain document types have specific structural requirements defined by their respective schema standards:
-   Methodology/Technique Descriptions: `[[AS-SCHEMA-METHODOLOGY-DESCRIPTION]]`
-   Concept Definitions: `[[AS-SCHEMA-CONCEPT-DEFINITION]]`
-   Reference Topics: `[[AS-SCHEMA-REFERENCE]]`
-   Task Topics: `[[AS-SCHEMA-TASK]]`
-   Consult these standards and use templates from `[[AS-STRUCTURE-TEMPLATES-DIRECTORY]]` when creating such documents.

## 6. Using Obsidian (Obsidian User Specific)

*(Note: This section details conventions for users of the Obsidian Markdown editor. These conventions are now generalized in the standards. If you use a different editor, these specific features may not apply, but the underlying Markdown standards still do.)*

### 6.1 Obsidian Linking Conventions
-   Use Wikilinks: `[[STANDARD_ID|Optional Display Text]]` or `[[path/to/file#Optional Heading|Optional Display Text]]`.
-   Paths SHOULD primarily use `standard_id` for linking to other standards. For non-standard content, relative paths are used.
-   Utilize Obsidian's path autocompletion where helpful.
-   Refer to `[[SF-LINKS-INTERNAL-SYNTAX]]` and `[[CS-LINKING-INTERNAL-POLICY]]`.

### 6.2 Obsidian Tagging
-   Tags are primarily managed in YAML frontmatter.
-   Use Obsidian's "Tags" pane for navigation.
-   The "Tag Wrangler" plugin is recommended for tag management.
-   Refer to `[[MT-TAGS-IMPLEMENTATION]]` and `[[MT-TAGGING-STRATEGY-POLICY]]`.

### 6.3 Obsidian Content Embedding/Transclusion
-   Embed content from other notes using `![[STANDARD_ID#optional_heading]]` or `![[filename#^blockID]]`.
-   Use `![[STANDARD_ID]]` for entire standard documents.
-   Refer to `[[SF-TRANSCLUSION-SYNTAX]]` and `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`.

### 6.4 Obsidian Callouts
-   Use `> [!TYPE] Optional Title` for admonitions (NOTE, WARNING, TIP, etc.).
-   Use semantically (e.g., `[!WARNING]` for actual warnings).
-   Refer to `[[SF-CALLOUTS-SYNTAX]]` and `[[CS-ADMONITIONS-POLICY]]`.

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

### 8.1 Process for Proposing Changes to Standards (`OM-POLICY-STANDARDS-GOVERNANCE`)
-   Refer to `[[OM-POLICY-STANDARDS-GOVERNANCE]]` for the documented process on how to propose new standards or suggest modifications to existing ones.

### 8.2 Versioning and Changelogs (`OM-VERSIONING-CHANGELOGS`)
-   Standards documents (and other key documents) are versioned using semantic versioning (e.g., `version: '1.0.1'`) in their frontmatter.
-   Significant changes are noted in a "Changelog" section within the standard, or in a separate changelog file linked via `change_log_url`.
-   Refer to `[[OM-VERSIONING-CHANGELOGS]]`.

### 8.3 Deprecation Policy (`OM-POLICY-STANDARDS-DEPRECATION`)
-   Superseded or irrelevant standards are marked as deprecated, not deleted, to maintain historical context.
-   Refer to `[[OM-POLICY-STANDARDS-DEPRECATION]]`.

### 8.4 Using the TODO System
-   Mark pending actions or notes for future work directly in documents using the `[!TODO]` callout format as specified in `[[SF-CALLOUTS-SYNTAX]]`.
-   Example: `> [!TODO] This section needs more examples. Due by YYYY-MM-DD, assigned to @username.`
-   Major TODOs may be aggregated in a project-specific `TODO-MASTER-LIST.md` or similar tracking document.

## 9. Glossaries and Further Help

-   **Standards Terminology:** For definitions of terms used within the standards documents themselves, see `[[GM-GLOSSARY-STANDARDS-TERMS]]`.
-   **Tag Glossary:** For definitions of all official tags used in YAML frontmatter, see `[[MT-REGISTRY-TAG-GLOSSARY]]`.
-   **Questions:** If you have questions or need clarification, please [Specify Contact Point or Channel, e.g., "reach out on the #kb-standards channel" or "contact Jim"].

---
*This guide is intended to be the primary onboarding document for all users of the Knowledge Base. It replaces and expands upon the original `GUIDE-KB-USAGE-AND-STANDARDS.md`.*
*Refer to the [[Refactor Roadmap.md]] for the overall refactoring project context.*
*For a task-oriented view of standards, see [[GM-GUIDE-STANDARDS-BY-TASK]].*
