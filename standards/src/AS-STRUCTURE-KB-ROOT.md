---
title: 'Standard: Knowledge Base Root Structure'
standard_id: AS-STRUCTURE-KB-ROOT
aliases:
- KB Root Structure
- Root File Organization
- KB Root Consistency Standard
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/as
- topic/structure
kb-id: standards
info-type: standard-definition
primary-topic: KB Root Structure and Consistent Application
related-standards:
- AS-KB-DIRECTORY-STRUCTURE
- AS-STRUCTURE-KB-PART
- GM-CONVENTIONS-NAMING
- SF-LINKS-INTERNAL-SYNTAX
version: 2.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: AS
sub_domain: STRUCTURE
scope_application: Defines the mandatory structure for the root level of any Knowledge
  Base (KB), including the root file, organization of top-level sections ('Parts'),
  and requirements for consistent application of structural choices.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- KB navigability
- Authoring consistency
- Automated processing
- Build system
- User experience
- Maintainability
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Knowledge Base Root Structure (AS-STRUCTURE-KB-ROOT)

This standard defines the mandatory structure for the root level of any Knowledge Base (KB), including the root file (`root.md`), the organization of its top-level sections ("Parts"), and the requirements for consistent application of structural choices within each KB.

## 1. Rules for KB Root Structure

### Rule 1.1: Designated Primary Folder
Each Knowledge Base (KB) MUST have a designated primary folder.
*   **Example:** `prompt-engineering-kb/`
*   **Notes:** Folder naming MUST adhere to [[GM-CONVENTIONS-NAMING]].

### Rule 1.2: Root Document (`root.md`)
Within this primary folder, a root document named `root.md` MUST exist.
*   **Example:** `prompt-engineering-kb/root.md`
*   **Notes:** This file serves as the main entry point and master index for the KB.

### Rule 1.3: Master Table of Contents (ToC) in `root.md`
The `root.md` file MUST contain a master Table of Contents (ToC) that links to all top-level primary sections ("Parts") of that KB.
*   **Notes:** Links MUST use the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]].

### Rule 1.4: Top-Level "Parts" in Larger KBs (Sub-folders)
For **larger KBs**, top-level "Parts" (primary sections) MUST be implemented as distinct sub-folders within the primary KB folder. Each such sub-folder represents one "Part".
*   **Example:** `research-methodology-kb/part-i-foundations/`
*   **Notes:** Folder naming MUST adhere to [[GM-CONVENTIONS-NAMING]]. The decision criterion for "larger" versus "smaller" is defined in Rule 1.6.

### Rule 1.5: Top-Level "Parts" in Smaller KBs (`root.md` Sections)
For **smaller or moderately sized KBs**, top-level "Parts" (primary sections) MUST be major H1 sections (often rendered as H2 in the context of the `root.md` document itself, following the main H1 title of `root.md`) directly within the `root.md` file. Content for these Parts can be nested directly or linked to subordinate files within the same primary KB folder.
*   **Example (Heading in `root.md`):** `## Part I: Core Methods`
*   **Notes:** The decision criterion for "smaller" versus "larger" is defined in Rule 1.6.

### Rule 1.6: Consistent Structure for "Parts" (Derived from U-ARCH-001, Rule 1.6)
The chosen method for organizing top-level "Parts" — either as distinct sub-folders (for larger KBs) or as major H1 sections within the `root.md` file (for smaller KBs) — MUST be consistently applied throughout a single Knowledge Base.
*   **Guidance:** A KB should not mix these two approaches. For instance, one Part should not be a sub-folder while another Part in the same KB is an H1 section in `root.md`.
*   **Decision Criteria for "Larger" vs. "Smaller" KBs:**
    *   **Number of Top-Level Parts:** If a KB is anticipated to have more than 5-7 top-level Parts, using sub-folders is generally recommended.
    *   **Depth of Content within Parts:** If individual Parts are expected to contain a large number of "Chapters" or deep sub-sections, sub-folders provide better organization from the outset.
    *   **Complexity of `root.md`:** If the `root.md` file becomes excessively long or difficult to manage due to numerous H1 sections and their inline ToCs, transitioning to sub-folders for Parts is advisable.
    *   **Team Size and Collaboration:** Larger teams or more complex collaborative environments may benefit from the clearer separation provided by sub-folders.
*   **Rationale:** 
    *   **User Experience & Navigability:** A consistent structure makes it easier for users to understand, navigate, and predict how content is organized within any given KB.
    *   **Authoring Consistency:** Clear rules on KB structure simplify the authoring process, as contributors do not have to guess how to organize new top-level sections.
    *   **Maintainability:** Uniformity in structure reduces complexity when performing maintenance tasks, refactoring content, or applying batch updates.
    *   **Automation & Tooling:** Automated tools for validation, indexing, or building KB views rely on predictable structures.
    *   **Scalability:** This rule ensures that the chosen option is applied uniformly, supporting clearer growth paths for KBs.

## 2. Illustrative Examples

### Example `root.md` for a Larger KB (Linking to Part Sub-folders)

```markdown
# Research Methodology Knowledge Base - Master Index

This knowledge base provides comprehensive guidance on research methodologies...

## Master Table of Contents

### Part I: Foundations of Research Methodology
- [Overview of Foundations](./part-i-foundations-of-research-methodology/_overview.md)
- [Introduction to Research Methodology](./part-i-foundations-of-research-methodology/01-introduction-to-research-methodology.md)
- [Core Concepts in Research](./part-i-foundations-of-research-methodology/02-core-concepts-in-research.md)

### Part II: Key Processes in Research
- [Overview of Key Processes](./part-ii-key-processes-in-research/_overview.md)
- [Data Collection Techniques](./part-ii-key-processes-in-research/01-data-collection-techniques.md)

### Part III: Advanced Topics
- [Overview of Advanced Topics](./part-iii-advanced-topics/_overview.md)
```
*(Note: The example links above are illustrative path-based links. Per [[SF-LINKS-INTERNAL-SYNTAX]], these should ideally be `[[STANDARD_ID]]` or `[[FILENAME_ID_PLACEHOLDER]]` links once target IDs are defined and resolvable.)*

## 3. Scope of Application

This standard applies to all Knowledge Bases developed and maintained within the organization.

## 4. Cross-References
- [[AS-KB-DIRECTORY-STRUCTURE]] - Defines overall repository and master knowledge base directory structures.
- [[AS-STRUCTURE-KB-PART]] - Primary KB Section ("Part") Structure.
- [[GM-CONVENTIONS-NAMING]] - File and Folder Naming Conventions.
- [[SF-LINKS-INTERNAL-SYNTAX]] - Internal Linking Syntax Standard.

---
*This standard (AS-STRUCTURE-KB-ROOT) consolidates and is based on rules 1.1-1.6 previously defined in U-ARCH-001 from COL-ARCH-UNIVERSAL.md. This version 2.0.0 incorporates consistency requirements previously defined in CS-POLICY-KB-ROOT.*
