---
title: 'Guide: Task-Based Navigation of Knowledge Base Standards'
standard_id: GM-GUIDE-STANDARDS-BY-TASK
aliases:
  - Standards by Task Guide
  - Task-Oriented Standards
tags:
  - status/draft
  - content-type/guide-document
  - topic/standards-governance
  - topic/workflow
  - topic/knowledge-management
  - topic/content-authoring
  - topic/navigation
kb-id: standards
info-type: guide-document
primary-topic: Task-oriented guide to Knowledge Base Standards, categorizing them
  by common activities and priority to help users find relevant standards.
related-standards:
  - GM-GUIDE-KB-USAGE
  - AS-STRUCTURE-MASTER-KB-INDEX
  - CS-POLICY-KB-IDENTIFICATION
  - AS-STRUCTURE-KB-ROOT
  - CS-POLICY-KB-ROOT
  - SF-CONVENTIONS-NAMING
  - SF-SYNTAX-YAML-FRONTMATTER
  - MT-SCHEMA-FRONTMATTER
  - MT-TAGGING-STRATEGY-POLICY
  - MT-TAGS-IMPLEMENTATION
  - CS-POLICY-SCOPE-INCLUSION
  - CS-POLICY-SCOPE-EXCLUSION
  - AS-KB-DIRECTORY-STRUCTURE
  - AS-STRUCTURE-KB-PART
  - CS-POLICY-KB-PART-CONTENT
  - CS-POLICY-PART-OVERVIEW
  - SF-SYNTAX-HEADINGS
  - SF-SYNTAX-LINKS-GENERAL
  - SF-LINKS-INTERNAL-SYNTAX
  - GM-MANDATE-KB-USAGE-GUIDE
  - AS-STRUCTURE-TEMPLATES-DIRECTORY
  - GM-MANDATE-STANDARDS-GLOSSARY
  - GM-GLOSSARY-STANDARDS-TERMS
  - AS-STRUCTURE-DOC-CHAPTER
  - CS-POLICY-DOC-CHAPTER-CONTENT
  - CS-POLICY-TONE-LANGUAGE
  - AS-SCHEMA-METHODOLOGY-DESCRIPTION
  - AS-SCHEMA-CONCEPT-DEFINITION
  - SF-FORMATTING-FILE-HYGIENE
  - SF-SYNTAX-KEYREF
  - SF-CONDITIONAL-SYNTAX-ATTRIBUTES
  - CS-CONTENT-PROFILING-POLICY
  - CS-LINKING-INTERNAL-POLICY
  - CS-MODULARITY-TRANSCLUSION-POLICY
  - SF-TRANSCLUSION-SYNTAX
  - CS-POLICY-ACCESSIBILITY
  - SF-ACCESSIBILITY-IMAGE-ALT-TEXT
  - SF-SYNTAX-LISTS
  - SF-SYNTAX-CODE
  - SF-SYNTAX-TABLES
  - SF-FORMATTING-CITATIONS
  - CS-POLICY-LAYERED-INFORMATION
  - CS-TOC-POLICY
  - SF-TOC-SYNTAX
  - SF-SYNTAX-EMPHASIS
  - SF-SYNTAX-BLOCKQUOTES
  - SF-SYNTAX-IMAGES
  - SF-SYNTAX-ESCAPING-CHARACTERS
  - SF-SYNTAX-DEFINITION-LISTS
  - SF-SYNTAX-FOOTNOTES
  - SF-SYNTAX-MATH-EQUATIONS
  - SF-SYNTAX-DIAGRAMS-MERMAID
  - AS-STRUCTURE-ASSET-ORGANIZATION
  - OM-POLICY-STANDARDS-GOVERNANCE
  - MT-REGISTRY-TAG-GLOSSARY
  - MT-KEYREF-MANAGEMENT
  - UA-KEYDEFS-GLOBAL
  - OM-VERSIONING-CHANGELOGS
  - OM-POLICY-STANDARDS-DEPRECATION
  - SF-CALLOUTS-SYNTAX
  - U-SCHEMA-REFERENCE-001
  - U-SCHEMA-TASK-001
version: 0.1.0
date-created: '2025-05-29T11:58:48Z'
date-modified: '2025-05-30T12:00:00Z'
primary_domain: GM
sub_domain: GUIDE
scope_application: Provides a task-based approach to navigating and applying the refactored
  knowledge base standards.
criticality: P2-Medium
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
  - User Onboarding
  - Standards Adoption
  - Workflow Efficiency
change_log_url: ./changelog.md
---
# Guide: Task-Based Navigation of Knowledge Base Standards (GM-GUIDE-STANDARDS-BY-TASK)

This document provides a task-oriented view of the Universal Knowledge Base Standards. It categorizes standards based on common knowledge base management activities and assigns a priority ranking (P1-P3) to each standard within the context of that specific task. This approach aims to help users focus on the most relevant standards for the job at hand, complementing the master priority ranking.

**Priority Definitions within Tasks:**
-   **P1 (Task-Critical):** Essential to perform this task correctly and in line with core principles.
-   **P2 (Task-Recommended):** Strongly advised for producing high-quality, maintainable output for this task.
-   **P3 (Task-Beneficial):** Good practice; enhances the output or process for this task but might be flexible.

## Table of Contents

- [Task 1: Setting Up a Brand New Knowledge Base (KB)](#task-1-setting-up-a-brand-new-knowledge-base-kb)
- [Task 2: Authoring a New Content Document](#task-2-authoring-a-new-content-document)
- [Task 3: Editing/Revising an Existing Content Document](#task-3-editingrevising-an-existing-content-document)
- [Task 4: Using an LLM for Content Generation/Assistance](#task-4-using-an-llm-for-content-generationassistance)
- [Task 5: General KB Maintenance & Governance (Vault/System Level)](#task-5-general-kb-maintenance--governance-vaultsystem-level)
- [Task 6: Working within Obsidian (Specific Features & Enhancements)](#task-6-working-within-obsidian-specific-features--enhancements)
- [Task 7: Ensuring Basic Markdown Portability & Readability](#task-7-ensuring-basic-markdown-portability--readability)

## Task 1: Setting Up a Brand New Knowledge Base (KB)

*Focus: Overall structure, foundational files for a new, distinct KB.*

### P1 (Task-Critical)

-   `[[AS-STRUCTURE-KB-ROOT]]`: KB Root Structure & Top-Level Part Organization.
    * Defines the initial skeleton (primary folder, `root.md`, "Parts") of the new KB.
    * *Task Priority Rationale*: Foundational for the KB's basic architecture and initial content discovery.
    * See also: `[[CS-POLICY-KB-ROOT]]`
-   `[[AS-STRUCTURE-MASTER-KB-INDEX]]`: Master KB Directory & Unique KB Identification.
    * Ensures the new KB fits into the overall system with unique naming and `kb-directory.md` listing.
    * *Task Priority Rationale*: Essential for managing multiple KBs and ensuring top-level discoverability.
    * See also: `[[CS-POLICY-KB-IDENTIFICATION]]`
-   `[[SF-CONVENTIONS-NAMING]]`: File & Folder Naming Conventions.
    * Governs kebab-case, descriptive names, and reserved names for all initial files/folders.
    * *Task Priority Rationale*: Critical for machine readability, consistent linking, and preventing errors from the outset.
-   `[[SF-SYNTAX-YAML-FRONTMATTER]]`: Markdown YAML Frontmatter.
    * Mandates YAML structure for `root.md` and any initial overview files.
    * *Task Priority Rationale*: Essential for metadata processing and tooling for foundational KB files.
-   `[[MT-SCHEMA-FRONTMATTER]]`: Frontmatter Structure and Content Rules.
    * Defines the canonical list of keys, order, and population rules for all frontmatter.
    * *Task Priority Rationale*: Critical for ensuring consistent and valid metadata from the outset.
-   `[[MT-TAGGING-STRATEGY-POLICY]]`: Core Tagging Strategy.
    * Requires correct structural tags (e.g., `kb-root`, `kb-id/*`) for `root.md` and `_overview.md` files.
    * *Task Priority Rationale*: Foundational for identifying KB structure and type from the beginning.
    * See also: `[[MT-TAGS-IMPLEMENTATION]]`
-   `[[CS-POLICY-SCOPE-INCLUSION]]`: Universal Principles for Content Inclusion.
    * Defines what the new KB will cover based on relevance and verifiability.
    * *Task Priority Rationale*: Core to defining the KB's purpose and boundaries.
-   `[[CS-POLICY-SCOPE-EXCLUSION]]`: Universal Principles for Content Exclusion.
    * Defines what the new KB will *not* cover (illegal, PII, etc.).
    * *Task Priority Rationale*: Critical for legal, ethical, and focus considerations from inception.
-   KB-Specific Scope Rules (e.g., `R-SCOPE-EXCLUDE-001` for a Research KB):
    * Defines specific content exclusions tailored to the new KB's domain.
    * *Task Priority Rationale*: Must be defined or considered early to ensure the KB's specific focus.
-   `[[AS-KB-DIRECTORY-STRUCTURE]]`:
    * Defines the dual source-and-render directory model for maintainable authoring and LLM-ready output.
    * *Task Priority Rationale*: Ensures the KB is set up for automation, maintainability, and LLM integration from the start.

### P2 (Task-Recommended)

-   `[[AS-STRUCTURE-KB-PART]]`: Primary KB Section ("Part") Structure.
    * Guides creation of initial `_overview.md` files if using sub-folders for "Parts".
    * *Task Priority Rationale*: Important for clear navigation and understanding of major KB sections.
    * See also: `[[CS-POLICY-KB-PART-CONTENT]]`, `[[CS-POLICY-PART-OVERVIEW]]`
-   `[[SF-SYNTAX-HEADINGS]]`: Markdown for Headings.
    * Governs heading structure within `root.md` and `_overview.md`.
    * *Task Priority Rationale*: Ensures structural integrity of foundational overview documents.
-   `[[SF-SYNTAX-LINKS-GENERAL]]`: Markdown for Links.
    * For creating links from `root.md` to "Parts" or overview documents.
    * *Task Priority Rationale*: Enables navigation within the initial KB structure.
    * See also: `[[SF-LINKS-INTERNAL-SYNTAX]]`
-   `[[GM-MANDATE-KB-USAGE-GUIDE]]`: "How to Use These Standards" Guide.
    * Refers to the main guide for understanding the overall standards framework.
    * *Task Priority Rationale*: Reviewing this is key before starting a new KB to ensure general compliance.
-   `[[AS-STRUCTURE-TEMPLATES-DIRECTORY]]`: Templates Directory.
    * Consider if base templates need creation for this new KB or if universal ones suffice.
    * *Task Priority Rationale*: Planning for templates early can save time and ensure consistency later.

### P3 (Task-Beneficial)

-   `[[GM-MANDATE-STANDARDS-GLOSSARY]]`: Glossary for the Standards Document. (Access via `[[GM-GLOSSARY-STANDARDS-TERMS]]`)
    * Helps in understanding specific terminology used within the standards themselves.
    * *Task Priority Rationale*: Useful for correctly interpreting standards during setup.
-   `[[CS-POLICY-PART-OVERVIEW]]` (related to O-USAGE-FOLDERS-NOTES-001): Obsidian Folder Notes for Part Overviews (if using Obsidian).
    * Setting up folder notes for `_overview.md` files if "Parts" are folders.
    * *Task Priority Rationale*: Enhances navigation in Obsidian if it's the chosen tool.

## Task 2: Authoring a New Content Document
*(Focus: Creating a single, new piece of content (e.g., Chapter, Concept, Methodology) within an existing KB)*

### P1 (Task-Critical)

-   `[[SF-CONVENTIONS-NAMING]]`: File & Folder Naming Conventions.
    * Governs the name of the new content file.
    * *Task Priority Rationale*: Ensures consistent and machine-readable file identification.
-   `[[SF-SYNTAX-YAML-FRONTMATTER]]`: Markdown YAML Frontmatter.
    * All new content files require correctly structured YAML for metadata.
    * *Task Priority Rationale*: Essential for metadata processing, discoverability, and status tracking.
-   `[[MT-SCHEMA-FRONTMATTER]]`: Frontmatter Structure and Content Rules.
    * Ensures the new document's frontmatter adheres to the canonical structure and rules.
    * *Task Priority Rationale*: Foundational for metadata consistency and validity.
-   `[[MT-TAGGING-STRATEGY-POLICY]]`: Core Tagging Strategy.
    * Mandates `topic/*`, `status/*`, `content-type/*`, and `kb-id/*` tags.
    * *Task Priority Rationale*: Critical for categorization, filtering, and managing the content lifecycle.
    * See also: `[[MT-TAGS-IMPLEMENTATION]]`
-   `[[AS-STRUCTURE-DOC-CHAPTER]]`: Content Document ("Chapter") Internal Structure.
    * Defines the fundamental layout (H1, abstract, ToC, sections, summary, "See Also").
    * *Task Priority Rationale*: Ensures consistent, predictable, and usable structure for all core content.
    * See also: `[[CS-POLICY-DOC-CHAPTER-CONTENT]]`
-   `[[SF-SYNTAX-HEADINGS]]`: Markdown for Headings.
    * Governs the use of H1-H6 for structuring the document content.
    * *Task Priority Rationale*: Fundamental for document organization, readability, and ToC generation.
-   `[[CS-POLICY-TONE-LANGUAGE]]`: Clarity, Objectivity, and Consistency in Language.
    * Dictates the writing style, terminology use, and acronym definition.
    * *Task Priority Rationale*: Essential for clear, unambiguous, and trustworthy content.
-   Applicable Schema Standards (e.g., `[[AS-SCHEMA-METHODOLOGY-DESCRIPTION]]` or `[[AS-SCHEMA-CONCEPT-DEFINITION]]`):
    * If the document is a methodology or concept, its specific schema must be followed.
    * *Task Priority Rationale*: Ensures specialized content types are structured comprehensively and consistently.
-   `[[SF-SYNTAX-LINKS-GENERAL]]`: Markdown for Links (Internal and External).
    * Governs the syntax for any internal or external links within the document.
    * *Task Priority Rationale*: Correct link syntax is vital for navigation and information integrity.
    * See also: `[[SF-LINKS-INTERNAL-SYNTAX]]`
-   `[[SF-FORMATTING-FILE-HYGIENE]]`: File Hygiene.
    * Ensures LF line endings, no trailing whitespace, and single newline at EOF for the new file.
    * *Task Priority Rationale*: Critical for cross-platform compatibility and version control.
-   `[[SF-SYNTAX-KEYREF]]`:
    * Defines the syntax for key-based referencing (keyrefs) in content.
    * *Task Priority Rationale*: Ensures authors use keyrefs correctly for maintainability and automation.
-   `[[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]]`:
    * Defines the syntax for conditional text blocks for profiling and selective publishing.
    * *Task Priority Rationale*: Enables authors to mark content for different audiences/platforms.
    * See also: `[[CS-CONTENT-PROFILING-POLICY]]`

### P2 (Task-Recommended)

-   `[[CS-LINKING-INTERNAL-POLICY]]`: Internal Knowledge Base Linking.
    * Encourages actively linking to related concepts, methods, and sections.
    * *Task Priority Rationale*: Key to creating a connected web of knowledge, enhancing discoverability.
    * See also: `[[SF-LINKS-INTERNAL-SYNTAX]]`
-   `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`: Designing for Content Modularity.
    * Promotes writing atomic content and considering transclusion over duplication.
    * *Task Priority Rationale*: Important for maintainability, reusability, and avoiding redundancy.
    * See also: `[[SF-TRANSCLUSION-SYNTAX]]`
-   `[[CS-POLICY-ACCESSIBILITY]]`: Image Accessibility and Alt Text.
    * Requires descriptive alt text if images are included in the document.
    * *Task Priority Rationale*: Crucial for users with disabilities and beneficial for machine understanding.
    * See also: `[[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]`
-   `[[SF-SYNTAX-LISTS]]`: Markdown for Lists (Ordered and Unordered).
    * Governs formatting of lists if they are used in the document.
    * *Task Priority Rationale*: Ensures consistent list rendering and readability for steps or itemizations.
-   `[[SF-SYNTAX-CODE]]`: Markdown for Code (Inline and Blocks).
    * Governs formatting of code snippets if included.
    * *Task Priority Rationale*: Essential for correctly displaying and understanding code examples.
-   `[[SF-SYNTAX-TABLES]]`: Markdown for Tables.
    * Governs formatting of tables if they are used.
    * *Task Priority Rationale*: Ensures tables are rendered correctly and are parsable.
-   `[[SF-FORMATTING-CITATIONS]]`: Citing External Sources.
    * Requires APA 7th for attribution if external sources are referenced.
    * *Task Priority Rationale*: Vital for credibility and avoiding plagiarism in factual or research-based content.
-   `[[CS-POLICY-LAYERED-INFORMATION]]`: Layered Information Presentation.
    * Guides how to structure information from general to specific within the document.
    * *Task Priority Rationale*: Significantly improves readability and user comprehension flow.
-   `[[SF-LINKS-INTERNAL-SYNTAX]]` (related to O-USAGE-LINKS-001): Obsidian Internal Linking Conventions (if using Obsidian).
    * Mandates Wikilink format for internal links within Obsidian.
    * *Task Priority Rationale*: Ensures proper link functionality and graph view in Obsidian.
-   `[[CS-TOC-POLICY]]` (related to O-USAGE-TOC-MANDATE-001): Obsidian Table of Contents Mandate (if using Obsidian & plugin for ToC).
    * Recommends using an Obsidian plugin for generating the document's ToC.
    * *Task Priority Rationale*: Facilitates accurate and maintainable ToCs as per `[[AS-STRUCTURE-DOC-CHAPTER]]`.
    * See also: `[[SF-TOC-SYNTAX]]`

### P3 (Task-Beneficial)

-   `[[SF-SYNTAX-EMPHASIS]]`: Markdown for Emphasis (Bold, Italic).
    * Provides rules for consistent styling of bold and italic text.
    * *Task Priority Rationale*: Enhances readability through consistent text highlighting.
-   `[[SF-SYNTAX-BLOCKQUOTES]]`: Markdown for Blockquotes.
    * Provides rules for consistent formatting of quoted text.
    * *Task Priority Rationale*: Ensures clear visual separation for quoted material.
-   `[[SF-SYNTAX-IMAGES]]`: Markdown for Images.
    * Covers the basic syntax for embedding images (alt text covered by `[[CS-POLICY-ACCESSIBILITY]]` and `[[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]`).
    * *Task Priority Rationale*: Basic syntax is usually straightforward; main concern is alt text.
-   `[[SF-SYNTAX-ESCAPING-CHARACTERS]]`: Escaping Special Markdown Characters.
    * Details how to display literal Markdown characters if needed.
    * *Task Priority Rationale*: Important for specific cases, like documenting Markdown itself.
-   `[[SF-SYNTAX-DEFINITION-LISTS]]`: Markdown for Definition Lists.
    * Syntax for creating definition lists, if applicable to content.
    * *Task Priority Rationale*: Useful for glossary-like sections if supported by the rendering environment.
-   `[[SF-SYNTAX-FOOTNOTES]]`: Markdown for Footnotes.
    * Syntax for adding footnotes, if applicable.
    * *Task Priority Rationale*: Provides a standard way to add supplementary notes.
-   `[[SF-SYNTAX-MATH-EQUATIONS]]`: Markdown for Math Equations.
    * Syntax for LaTeX math equations, if applicable.
    * *Task Priority Rationale*: Essential if mathematical notation is required.
-   `[[SF-SYNTAX-DIAGRAMS-MERMAID]]`: Markdown for Diagrams (Mermaid).
    * Syntax for embedding Mermaid diagrams, if applicable.
    * *Task Priority Rationale*: Provides a standard for text-based diagramming.
-   `[[AS-STRUCTURE-ASSET-ORGANIZATION]]`: Asset Organization.
    * If adding new assets like images, they should be placed in the correct `assets` subfolder.
    * *Task Priority Rationale*: Keeps non-Markdown files organized within the KB.
-   `[[SF-TRANSCLUSION-SYNTAX]]` (related to O-USAGE-TRANSCLUSION-001): Obsidian Content Embedding (Transclusion) (if using Obsidian).
    * Syntax for embedding content from other notes in Obsidian.
    * *Task Priority Rationale*: Useful for reusability if content exists elsewhere that can be embedded.
    * See also: `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`

## Task 3: Editing/Revising an Existing Content Document
*(Focus: Modifying existing content, ensuring continued standards compliance and updating relevant metadata)*

### P1 (Task-Critical)

-   `[[SF-CONVENTIONS-NAMING]]`: File & Folder Naming Conventions.
    * Ensures the existing file name remains compliant or is updated if its core subject changes significantly.
    * *Task Priority Rationale*: Maintains consistent and machine-readable file identification.
-   `[[SF-SYNTAX-YAML-FRONTMATTER]]`: Markdown YAML Frontmatter.
    * Requires updating `date-modified`, and potentially `version` and the `status/*` tag based on edits.
    * *Task Priority Rationale*: Keeps metadata accurate, reflecting the current state and history of the document.
-   `[[MT-TAGGING-STRATEGY-POLICY]]`: Core Tagging Strategy.
    * Verify and update `topic/*`, `status/*`, and `content-type/*` tags if the revision changes scope or status.
    * *Task Priority Rationale*: Ensures continued accurate categorization and lifecycle tracking.
    * See also: `[[MT-TAGS-IMPLEMENTATION]]`
-   `[[AS-STRUCTURE-DOC-CHAPTER]]`: Content Document ("Chapter") Internal Structure.
    * Ensures revisions maintain the standard document layout (H1, abstract, ToC, sections, etc.).
    * *Task Priority Rationale*: Guarantees the document remains consistent, predictable, and usable after edits.
    * See also: `[[CS-POLICY-DOC-CHAPTER-CONTENT]]`
-   `[[SF-SYNTAX-HEADINGS]]`: Markdown for Headings.
    * Ensures heading hierarchy and formatting remain correct after changes.
    * *Task Priority Rationale*: Maintains document organization, readability, and ToC integrity.
-   `[[CS-POLICY-TONE-LANGUAGE]]`: Clarity, Objectivity, and Consistency in Language.
    * Ensures new or modified text adheres to the established writing style.
    * *Task Priority Rationale*: Maintains the overall quality and clarity of the content.
-   Applicable Schema Standards (e.g., `[[AS-SCHEMA-METHODOLOGY-DESCRIPTION]]` or `[[AS-SCHEMA-CONCEPT-DEFINITION]]`):
    * Ensures the document continues to adhere to its defined content schema after revisions.
    * *Task Priority Rationale*: Preserves the comprehensive and consistent structure of specialized content types.
-   `[[SF-SYNTAX-LINKS-GENERAL]]`: Markdown for Links (Internal and External).
    * Verify existing links and ensure new links use correct syntax.
    * *Task Priority Rationale*: Prevents broken links and ensures information integrity.
    * See also: `[[SF-LINKS-INTERNAL-SYNTAX]]`
-   `[[SF-FORMATTING-FILE-HYGIENE]]`: File Hygiene.
    * Re-check LF line endings, trailing whitespace, and EOF newline after edits.
    * *Task Priority Rationale*: Maintains file integrity for compatibility and version control.
-   `[[OM-VERSIONING-CHANGELOGS]]`: Versioning and Changelogs for Standard Files (if applying to content docs).
    * Update version number in YAML and add entry to changelog for significant revisions.
    * *Task Priority Rationale*: Tracks evolution of content, especially for important documents.
-   `[[SF-SYNTAX-KEYREF]]`:
    * If edits involve keyrefs, ensures continued correct usage and maintainability.
    * *Task Priority Rationale*: Maintains automation compatibility and content integrity.
-   `[[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]]`:
    * If edits involve conditional text, ensures correct profiling and selective publishing.
    * *Task Priority Rationale*: Maintains content targeting and filtering capabilities.
    * See also: `[[CS-CONTENT-PROFILING-POLICY]]`

### P2 (Task-Recommended)

-   `[[CS-LINKING-INTERNAL-POLICY]]`: Internal Knowledge Base Linking.
    * Review if new links to other documents are now relevant, or if existing links need updating/removal.
    * *Task Priority Rationale*: Keeps the document well-connected within the KB's information web.
    * See also: `[[SF-LINKS-INTERNAL-SYNTAX]]`
-   `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`: Designing for Content Modularity.
    * Assess if edits allow for sections to be abstracted for transclusion, or if duplicated content can now be replaced by an embed.
    * *Task Priority Rationale*: Improves maintainability and reduces redundancy as content evolves.
    * See also: `[[SF-TRANSCLUSION-SYNTAX]]`
-   `[[CS-POLICY-ACCESSIBILITY]]`: Image Accessibility and Alt Text.
    * If images are added or changed, ensure descriptive alt text is provided or updated.
    * *Task Priority Rationale*: Maintains accessibility for all users.
    * See also: `[[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]`
-   `[[SF-SYNTAX-LISTS]]`: Markdown for Lists (Ordered and Unordered).
    * Ensure any new or modified lists adhere to formatting standards.
    * *Task Priority Rationale*: Maintains consistent list rendering and readability.
-   `[[SF-SYNTAX-CODE]]`: Markdown for Code (Inline and Blocks).
    * Ensure new or modified code snippets are correctly formatted.
    * *Task Priority Rationale*: Ensures clarity and correctness of code examples.
-   `[[SF-SYNTAX-TABLES]]`: Markdown for Tables.
    * Ensure new or modified tables are correctly formatted.
    * *Task Priority Rationale*: Maintains correct rendering and parsability of tabular data.
-   `[[SF-FORMATTING-CITATIONS]]`: Citing External Sources.
    * If new claims are added or sources changed, update citations and references accordingly.
    * *Task Priority Rationale*: Upholds academic integrity and source verifiability.
-   `[[CS-POLICY-LAYERED-INFORMATION]]`: Layered Information Presentation.
    * Ensure the flow from general to specific information remains logical after edits.
    * *Task Priority Rationale*: Maintains user comprehension and document readability.
-   `[[SF-LINKS-INTERNAL-SYNTAX]]` (related to O-USAGE-LINKS-001): Obsidian Internal Linking Conventions (if using Obsidian).
    * Ensure wikilinks are used/updated correctly for internal navigation in Obsidian.
    * *Task Priority Rationale*: Maintains link functionality within the Obsidian environment.
-   `[[CS-TOC-POLICY]]` (related to O-USAGE-TOC-MANDATE-001): Obsidian Table of Contents Mandate (if using Obsidian & plugin for ToC).
    * Regenerate or update the ToC if section headings have changed.
    * *Task Priority Rationale*: Ensures the ToC accurately reflects the revised document structure.
    * See also: `[[SF-TOC-SYNTAX]]`

### P3 (Task-Beneficial)

-   `[[SF-SYNTAX-EMPHASIS]]`: Markdown for Emphasis (Bold, Italic).
    * Check consistency of any new emphasis styling.
    * *Task Priority Rationale*: Minor textual enhancements for readability.
-   `[[SF-SYNTAX-BLOCKQUOTES]]`: Markdown for Blockquotes.
    * Check formatting of any new blockquotes.
    * *Task Priority Rationale*: Ensures visual consistency for quoted text.
-   `[[SF-SYNTAX-IMAGES]]`: Markdown for Images.
    * Verify syntax for any new images.
    * *Task Priority Rationale*: Basic syntax check.
-   `[[AS-STRUCTURE-ASSET-ORGANIZATION]]`: Asset Organization.
    * If assets are changed or added, ensure they are correctly located.
    * *Task Priority Rationale*: Keeps associated files organized.
-   `[[SF-TRANSCLUSION-SYNTAX]]` (related to O-USAGE-TRANSCLUSION-001): Obsidian Content Embedding (Transclusion) (if using Obsidian).
    * If content is transcluded, ensure source and embed syntax are still correct.
    * *Task Priority Rationale*: Verifies functionality of embedded content.
    * See also: `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`

## Task 4: Using an LLM for Content Generation/Assistance
*(Focus: Ensuring LLM outputs align with standards, leveraging the LLM Cookbook, and performing necessary human oversight)*

### P1 (Task-Critical)

-   Relevant `LCGC-SCHEMA-RECIPE-001` (or other cookbook recipes from `llm-content-generation-cookbook-kb`):
    * Use the correct, standardized recipe for the specific content generation task.
    * *Task Priority Rationale*: Maximizes the chance of the LLM producing standards-compliant initial drafts.
-   `[[SF-SYNTAX-YAML-FRONTMATTER]]`: Markdown YAML Frontmatter.
    * LLM output must be wrapped with or edited to include correct YAML, or prompt LLM to generate it.
    * *Task Priority Rationale*: Essential for metadata; LLMs may not produce this correctly without explicit instruction.
-   `[[MT-TAGGING-STRATEGY-POLICY]]`: Core Tagging Strategy.
    * Ensure LLM output includes or is edited to have correct tags, especially `status/draft`.
    * *Task Priority Rationale*: LLM-generated content needs clear status and categorization.
    * See also: `[[MT-TAGS-IMPLEMENTATION]]`
-   `[[AS-STRUCTURE-DOC-CHAPTER]]`: Content Document ("Chapter") Internal Structure.
    * Guide LLM to produce content matching this structure or heavily edit output to conform.
    * *Task Priority Rationale*: LLM output needs to fit the standard document layout for usability.
    * See also: `[[CS-POLICY-DOC-CHAPTER-CONTENT]]`
-   `[[SF-SYNTAX-HEADINGS]]`: Markdown for Headings.
    * Instruct LLM on heading hierarchy or correct its output.
    * *Task Priority Rationale*: LLMs can be inconsistent with headings; this is vital for structure.
-   `[[CS-POLICY-TONE-LANGUAGE]]`: Clarity, Objectivity, and Consistency in Language.
    * Crucial to prompt the LLM for the desired tone and to review output for objectivity and clarity.
    * *Task Priority Rationale*: LLMs can adopt various tones; standards require a specific one.
-   Applicable Schema Standards (e.g., `[[AS-SCHEMA-METHODOLOGY-DESCRIPTION]]` or `[[AS-SCHEMA-CONCEPT-DEFINITION]]`):
    * Provide the schema structure in the prompt or use a recipe that incorporates it.
    * *Task Priority Rationale*: Ensures specialized content types are structured comprehensively and consistently.
-   `[[SF-SYNTAX-LINKS-GENERAL]]`: Markdown for Links (Internal and External).
    * LLM-generated links (especially internal) need careful verification and syntax correction.
    * *Task Priority Rationale*: LLMs may hallucinate links or use incorrect paths/syntax.
    * See also: `[[SF-LINKS-INTERNAL-SYNTAX]]`
-   `[[SF-FORMATTING-FILE-HYGIENE]]`: File Hygiene.
    * LLM output pasted into files needs to adhere to file hygiene rules.
    * *Task Priority Rationale*: Ensures generated content integrates cleanly.
-   `01-llm-capabilities-and-limitations.md` (from `llm-content-generation-cookbook-kb`):
    * Understand LLM weaknesses (e.g., factual accuracy, adherence to complex rules) before relying on output.
    * *Task Priority Rationale*: Sets realistic expectations and emphasizes the need for human oversight.
-   `03-iterative-refinement-and-evaluation.md` (from `llm-content-generation-cookbook-kb`):
    * Apply iterative refinement and human evaluation to all LLM-generated content.
    * *Task Priority Rationale*: LLM output is a draft, not final; human review against standards is mandatory.
-   `[[LLM-AUTOMATION-IO-SCHEMA-001]]`:
    * Governs the input/output JSON schemas for LLM automation.
    * *Task Priority Rationale*: Ensures LLMs produce and consume structured, standards-compliant data.
-   `[[LLM-PROMPT-LIBRARY-001]]`:
    * Governs the management and use of versioned LLM prompt templates.
    * *Task Priority Rationale*: Ensures LLMs are prompted with tested, standards-aligned templates.
-   `[[SF-SYNTAX-KEYREF]]` and `[[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]]`:
    * LLM prompts should instruct the use of keyrefs and conditional text where appropriate.
    * *Task Priority Rationale*: Maintains maintainability and profiling in LLM-generated content.
    * See also: `[[CS-CONTENT-PROFILING-POLICY]]`

### P2 (Task-Recommended)

-   `[[SF-FORMATTING-CITATIONS]]`: Citing External Sources.
    * Be extremely cautious with LLM-provided sources; verify all facts and citations. LLMs often "hallucinate" references.
    * *Task Priority Rationale*: Critical for maintaining accuracy and credibility; LLMs are unreliable here.
-   `[[CS-LINKING-INTERNAL-POLICY]]`: Internal Knowledge Base Linking.
    * LLMs might suggest conceptual links, but actual file links need human verification and creation.
    * *Task Priority Rationale*: LLMs don't have real-time access to your KB structure for accurate linking.
    * See also: `[[SF-LINKS-INTERNAL-SYNTAX]]`
-   `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`: Designing for Content Modularity.
    * Prompt the LLM to generate content in atomic, self-contained sections where appropriate.
    * *Task Priority Rationale*: Can help LLMs produce more focused and reusable content blocks.
    * See also: `[[SF-TRANSCLUSION-SYNTAX]]`
-   `[[CS-POLICY-ACCESSIBILITY]]`: Image Accessibility and Alt Text.
    * If LLMs are used to generate descriptions for images, these must be reviewed for accuracy and context as alt text.
    * *Task Priority Rationale*: Ensures LLM-assisted alt text is meaningful.
    * See also: `[[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]`
-   `[[SF-SYNTAX-LISTS]]`, `[[SF-SYNTAX-CODE]]`, `[[SF-SYNTAX-TABLES]]`:
    * Review LLM output for correct Markdown formatting of these elements.
    * *Task Priority Rationale*: LLMs can make subtle formatting errors in complex Markdown.

### P3 (Task-Beneficial)

-   Advanced techniques from `llm-content-generation-cookbook-kb/part-iii-advanced-techniques/` (e.g., Personas, Chain-of-Thought):
    * Employ these for more complex or nuanced content generation tasks.
    * *Task Priority Rationale*: Can improve the quality and relevance of LLM output for specific needs.
-   Specific Markdown formatting rules (`[[SF-SYNTAX-EMPHASIS]]`, `[[SF-SYNTAX-BLOCKQUOTES]]`, etc.):
    * LLMs can often get these right with good prompting but may need minor cleanup.
    * *Task Priority Rationale*: Fine-tuning the presentation of LLM-generated text.

## Task 5: General KB Maintenance & Governance (Vault/System Level)
*(Focus: Managing the overall system, standards, tags, multiple KBs, and supporting utilities)*

### P1 (Task-Critical)

-   `[[AS-STRUCTURE-MASTER-KB-INDEX]]`: Master KB Directory & Unique KB Identification.
    * Specifically, keeping `kb-directory.md` accurate as KBs are added or their scope changes.
    * *Task Priority Rationale*: Essential for the central index of all knowledge bases.
    * See also: `[[CS-POLICY-KB-IDENTIFICATION]]`
-   `[[OM-POLICY-STANDARDS-GOVERNANCE]]`: Governance - Proposing and Updating Standards.
    * Following the defined process for any changes to the standards documents themselves.
    * *Task Priority Rationale*: Core to maintaining the integrity and evolution of the entire standards framework.
-   `[[MT-TAGGING-STRATEGY-POLICY]]`: Core Tagging Strategy.
    * Specifically, maintaining the `tag-glossary.md` (linked as `[[MT-REGISTRY-TAG-GLOSSARY]]`) if new global tags are officialized or existing ones change.
    * *Task Priority Rationale*: Keeps the master list of tags and their meanings current.
-   `[[MT-KEYREF-MANAGEMENT]]`:
    * Governs the management and updating of `[[UA-KEYDEFS-GLOBAL]]`.
    * *Task Priority Rationale*: Ensures a single source of truth for keyrefs and triggers automation updates.

### P2 (Task-Recommended)

-   `[[OM-VERSIONING-CHANGELOGS]]`: Versioning and Changelogs for Standard Files.
    * Applying versioning and changelogs to the *Standards Files* themselves when they are updated.
    * *Task Priority Rationale*: Tracks the evolution of the standards framework for clarity and history.
-   `[[OM-POLICY-STANDARDS-DEPRECATION]]`: Deprecation Policy for Standards.
    * Following the correct procedure when a standard is no longer relevant or is superseded.
    * *Task Priority Rationale*: Manages the lifecycle of standards without losing historical context.
-   `assemble-monolith.py` script logic & `standards-assembly-manifest.md`:
    * Ensuring the script and manifest are correct if the monolith standards document needs to be regenerated.
    * *Task Priority Rationale*: Key for producing the consolidated standards document accurately.
-   `[[GM-MANDATE-KB-USAGE-GUIDE]]` (referring to `[[GM-GUIDE-KB-USAGE]]`): "How to Use These Standards" Guide.
    * Keeping this primary guide up-to-date as standards evolve or new insights are gained.
    * *Task Priority Rationale*: Ensures new and existing users have accurate guidance.
-   `[[SF-FORMATTING-FILE-HYGIENE]]`: File Hygiene.
    * Periodically checking or enforcing file hygiene across the vault, especially for standards documents.
    * *Task Priority Rationale*: Maintains technical quality across the entire KB system.
-   `[[CS-CONTENT-PROFILING-POLICY]]` (related to U-PROFILING-ATTRIBUTES-001):
    * Governs the list of profiling attributes and their allowed values.
    * *Task Priority Rationale*: Ensures consistent profiling and filtering across the KB.

### P3 (Task-Beneficial)

-   `[[GM-MANDATE-STANDARDS-GLOSSARY]]` (Access via `[[GM-GLOSSARY-STANDARDS-TERMS]]`): Glossary for the Standards Document.
    * Updating the glossary of terms used within the standards documents if new terms are introduced.
    * *Task Priority Rationale*: Aids clarity and understanding of the standards documentation.
-   Reviewing KB-Specific standards (e.g., `ResearchMethodology-Standards.md`):
    * Ensuring they remain consistent with universal standards or that deviations are justified and documented.
    * *Task Priority Rationale*: Promotes overall coherence across different knowledge bases.
-   `[[AS-STRUCTURE-TEMPLATES-DIRECTORY]]`: Templates Directory.
    * Periodically reviewing and updating document templates to reflect current standards.
    * *Task Priority Rationale*: Ensures templates remain useful and promote standards adherence.

## Task 6: Working within Obsidian (Specific Features & Enhancements)
*(Note: This section details conventions for users of the Obsidian Markdown editor. These conventions are now generalized in the standards. If you use a different editor, these specific features may not apply, but the underlying Markdown standards still do.)*

### P1 (Task-Critical for Obsidian Users)

-   `[[SF-LINKS-INTERNAL-SYNTAX]]`: Obsidian Internal Linking Conventions.
    * Mandates Wikilink format, use of path autocompletion, and handling of pipe characters.
    * *Task Priority Rationale*: Fundamental for creating functional and consistent internal links within Obsidian.
    * See also: `[[CS-LINKING-INTERNAL-POLICY]]`

### P2 (Task-Recommended for Obsidian Users)

-   `[[MT-TAGS-IMPLEMENTATION]]`: Obsidian Tag Implementation.
    * Using tags in YAML (cross-ref `[[MT-TAGGING-STRATEGY-POLICY]]`), using the Tags pane, and Tag Wrangler plugin.
    * *Task Priority Rationale*: Ensures effective use of Obsidian's tagging features for organization and discovery.
-   `[[SF-TRANSCLUSION-SYNTAX]]`: Obsidian Content Embedding (Transclusion).
    * Using `![[...]]` syntax for embedding blocks, sections, or entire notes.
    * *Task Priority Rationale*: Leverages Obsidian's power for modularity and reducing content duplication.
    * See also: `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`
-   `[[CS-TOC-POLICY]]`: Obsidian Table of Contents Mandate.
    * Recommends using an Obsidian community plugin to generate and maintain ToCs in chapter documents.
    * *Task Priority Rationale*: Facilitates accurate and automatically updated ToCs, aligning with `[[AS-STRUCTURE-DOC-CHAPTER]]`.
    * See also: `[[SF-TOC-SYNTAX]]`

### P3 (Task-Beneficial for Obsidian Users)

-   `[[CS-POLICY-PART-OVERVIEW]]`: Obsidian Folder Notes for Part Overviews.
    * Configuring `_overview.md` files as folder notes using a community plugin.
    * *Task Priority Rationale*: Enhances the navigational experience when browsing KB "Parts" structured as folders.
    * See also: `[[AS-STRUCTURE-KB-PART]]`
-   Future Obsidian-specific standards (e.g., Dataview usage from TODO list):
    * Conventions for using other Obsidian plugins or features.
    * *Task Priority Rationale*: Extends standardized practices to more advanced Obsidian functionalities.

## Task 7: Ensuring Basic Markdown Portability & Readability
*(Focus: Core Markdown syntax for broad compatibility if content is used outside a specific advanced editor like Obsidian, or by diverse tools and LLMs)*

### P1 (Task-Critical)

-   `[[SF-SYNTAX-YAML-FRONTMATTER]]`: Markdown YAML Frontmatter.
    * Ensuring a valid YAML block exists, as many systems can parse this for metadata.
    * *Task Priority Rationale*: Key for metadata extraction by various tools.
-   `[[SF-SYNTAX-HEADINGS]]`: Markdown for Headings.
    * ATX style and proper hierarchy are universally understood.
    * *Task Priority Rationale*: Fundamental for document structure recognition by any Markdown parser.
-   `[[SF-SYNTAX-LISTS]]`: Markdown for Lists (Ordered and Unordered).
    * Using basic `-` and `1.` markers ensures wide compatibility.
    * *Task Priority Rationale*: Ensures lists are rendered correctly across most platforms.
-   `[[SF-SYNTAX-LINKS-GENERAL]]`: Markdown for Links (Internal and External).
    * Standard `[text](url)` for external/relative links is universally supported. Wikilinks (`[[SF-LINKS-INTERNAL-SYNTAX]]`) are less portable without specific processing.
    * *Task Priority Rationale*: Guarantees link functionality outside specialized environments.
-   `[[SF-SYNTAX-CODE]]`: Markdown for Code (Inline and Blocks).
    * Backticks for inline and triple-backtick fenced blocks are standard.
    * *Task Priority Rationale*: Ensures code snippets are displayed as intended by most renderers.
-   `[[SF-SYNTAX-TABLES]]`: Markdown for Tables.
    * GitHub Flavored Markdown (GFM) table syntax is widely adopted.
    * *Task Priority Rationale*: Provides a common standard for tabular data rendering.
-   `[[SF-FORMATTING-FILE-HYGIENE]]`: File Hygiene.
    * LF line endings, no trailing whitespace, EOF newline improve cross-system compatibility.
    * *Task Priority Rationale*: Prevents parsing and display issues in different environments.

### P2 (Task-Recommended)

-   `[[SF-SYNTAX-EMPHASIS]]`: Markdown for Emphasis (Bold, Italic).
    * Using `*` or `_` consistently for italics, and `**` or `__` for bold.
    * *Task Priority Rationale*: Basic emphasis is widely supported; consistency aids readability.
-   `[[SF-SYNTAX-BLOCKQUOTES]]`: Markdown for Blockquotes.
    * Standard `>` syntax is universally recognized.
    * *Task Priority Rationale*: Ensures quoted text is visually distinct across platforms.
-   `[[SF-SYNTAX-IMAGES]]`: Markdown for Images.
    * Core `![alt](src)` syntax is universal.
    * *Task Priority Rationale*: Ensures images can be rendered by basic Markdown processors.
-   `[[CS-POLICY-ACCESSIBILITY]]`: Image Accessibility and Alt Text.
    * Alt text within the `![alt text](src)` tag is part of the Markdown standard.
    * *Task Priority Rationale*: Alt text is crucial for accessibility and can be read by many systems.
    * See also: `[[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]`
-   `[[SF-FORMATTING-MARKDOWN-GENERAL]]`: Markdown General Formatting.
    * Single blank lines between paragraphs, no hard line breaks (unless intended).
    * *Task Priority Rationale*: Promotes clean, universally parsable paragraph structure.

### P3 (Task-Beneficial)

-   `[[SF-SYNTAX-ESCAPING-CHARACTERS]]`: Escaping Special Markdown Characters.
    * Using backslashes to display literal Markdown characters.
    * *Task Priority Rationale*: Important for accurately displaying characters that have special meaning in Markdown.
-   `[[SF-SYNTAX-DEFINITION-LISTS]]`: Markdown for Definition Lists.
    * GFM extension; support varies but is common in many modern parsers.
    * *Task Priority Rationale*: Useful if supported, but not a core Markdown feature everywhere.
-   `[[SF-SYNTAX-FOOTNOTES]]`: Markdown for Footnotes.
    * Extended Markdown syntax; support varies but is common in academic/technical contexts.
    * *Task Priority Rationale*: Useful where supported, but content should remain understandable without them.
-   `[[SF-SYNTAX-MATH-EQUATIONS]]`: Markdown for Math Equations.
    * Requires LaTeX support (e.g., MathJax, KaTeX) in the rendering environment.
    * *Task Priority Rationale*: Content may not render as math without specific renderer support.
-   `[[SF-SYNTAX-DIAGRAMS-MERMAID]]`: Markdown for Diagrams (Mermaid).
    * Requires specific Mermaid JavaScript library for rendering.
    * *Task Priority Rationale*: Diagrams will appear as code blocks without Mermaid support.

## 8. Appendix

For further details on the refactoring project that led to this standards structure, please see the [Refactor Roadmap](../../../_temp/Refactor Roadmap.md).
For guidelines on how to contribute to this knowledge base or propose changes to standards, refer to the [CONTRIBUTOR_GUIDE](../../CONTRIBUTOR_GUIDE.md).

---
*This document provides a task-based entry point to the standards knowledge base. It is intended to complement the [[GM-GUIDE-KB-USAGE]].*
*It replaces the older `standards/GUIDE-TASK-BASED.md`.*
*For the overall refactoring project context, refer to [Refactor Roadmap](../../../_temp/Refactor Roadmap.md) .*
