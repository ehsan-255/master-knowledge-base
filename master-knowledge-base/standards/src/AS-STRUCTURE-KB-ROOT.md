---
title: "Standard: Knowledge Base Root Structure"
standard_id: "AS-STRUCTURE-KB-ROOT"
aliases: ["KB Root Structure", "Root File Organization"]
tags:
  - status/draft
  - criticality/P1-High
  - content-type/technical-standard
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "KB Root Structure"
related-standards: ["CS-POLICY-KB-ROOT", "AS-KB-DIRECTORY-STRUCTURE"]
version: '1.0.0'
date-created: "2024-07-15T12:00:00Z"
date-modified: "2025-05-30T16:00:00Z"
primary_domain: "AS"
sub_domain: "STRUCTURE"
scope_application: "Defines the mandatory structure for the root level of any Knowledge Base (KB), including the root file and organization of top-level sections ('Parts')."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["KB navigability", "Authoring consistency", "Automated processing", "Build system"]
change_log_url: "./AS-STRUCTURE-KB-ROOT-changelog.md"
---
# Standard: Knowledge Base Root Structure (AS-STRUCTURE-KB-ROOT)

This standard defines the mandatory structure for the root level of any Knowledge Base (KB), including the root file (`root.md`) and the organization of its top-level sections, referred to as "Parts."

## 1. Rules for KB Root Structure

### Rule 1.1: Designated Primary Folder
Each Knowledge Base (KB) MUST have a designated primary folder.
*   **Example:** `prompt-engineering-kb/`
*   **Notes:** Folder naming MUST adhere to [[SF-CONVENTIONS-NAMING]].

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
*   **Notes:** Folder naming MUST adhere to [[SF-CONVENTIONS-NAMING]]. The decision criterion for "larger" versus "smaller" is further discussed in [[CS-POLICY-KB-ROOT]].

### Rule 1.5: Top-Level "Parts" in Smaller KBs (`root.md` Sections)
For **smaller or moderately sized KBs**, top-level "Parts" (primary sections) MUST be major H1 sections (often rendered as H2 in the context of the `root.md` document itself, following the main H1 title of `root.md`) directly within the `root.md` file. Content for these Parts can be nested directly or linked to subordinate files within the same primary KB folder.
*   **Example (Heading in `root.md`):** `## Part I: Core Methods`
*   **Notes:** The decision criterion for "smaller" versus "larger" is further discussed in [[CS-POLICY-KB-ROOT]].

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

## 3. Cross-References
- [[CS-POLICY-KB-ROOT]] - Policy for consistent application of KB root structures.
- [[AS-KB-DIRECTORY-STRUCTURE]] - Defines overall repository and master knowledge base directory structures.
- [[SF-CONVENTIONS-NAMING]] - File and Folder Naming Conventions.
- [[SF-LINKS-INTERNAL-SYNTAX]] - Internal Linking Syntax Standard.
- [[AS-STRUCTURE-KB-PART]] - Primary KB Section ("Part") Structure.

---
*This standard (AS-STRUCTURE-KB-ROOT) is based on rules 1.1-1.5 previously defined in U-ARCH-001 from COL-ARCH-UNIVERSAL.md.*
