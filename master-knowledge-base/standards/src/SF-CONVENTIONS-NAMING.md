---
title: "Standard: File and ID Naming Conventions"
standard_id: "SF-CONVENTIONS-NAMING"
aliases: ["Naming Conventions", "File Naming", "ID Conventions"]
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "File and ID Naming Conventions"
related-standards: []
version: '1.0.0'
date-created: "2025-05-29T13:24:53Z"
date-modified: "2025-05-30T18:00:00Z"
primary_domain: "SF"
sub_domain: "MARKDOWN"
scope_application: "Defines the naming conventions for files, standard IDs, and other identifiers in the knowledge base."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["File organization", "Standard identification", "System consistency"]
change_log_url: "./SF-CONVENTIONS-NAMING-changelog.md"
---

# Standard: File and Folder Naming Conventions (SF-CONVENTIONS-NAMING)

This standard defines the mandatory naming conventions for all files and folders within the knowledge base repository. Adherence to these conventions is critical for maintaining an organized structure, facilitating automated processing, ensuring link integrity, and providing a consistent experience for authors and users.

## 1. General Principles

### Rule 1.1: Descriptive and Concise Names (Derived from U-FORMAT-NAMING-001, Rule 1.8)
All file and folder names MUST be descriptive and concise, clearly indicating the primary content or purpose of the item.

## 2. Folder Naming Conventions

### Rule 2.1: Case and Separator (Derived from U-FORMAT-NAMING-001, Rule 1.1)
All folder names MUST be in **all lowercase kebab-case**.
*   **Example:** `part-i-foundations/`, `kb-specific-standards/`, `src/`, `registry/`
*   **Notes:** Words are separated by single hyphens. No spaces or other special characters (except hyphens) are permitted.

## 3. File Naming Conventions

### Rule 3.1: Atomic Standard Document Files (Primary Naming Standard)
This rule defines the primary naming convention for atomic standard definition, policy, and guide documents, particularly those located within the `/master-knowledge-base/standards/src/` directory.

*   **Syntax:** `{DOMAIN_CODE}-{SUB_DOMAIN_CODE}-{PRIMARY_TOPIC_KEYWORD}-{OPTIONAL_SECONDARY_TOPICS*}.md`
    *   **`DOMAIN_CODE`**: A 2-letter uppercase code representing the primary domain (e.g., `AS`, `CS`, `SF`).
    *   **`SUB_DOMAIN_CODE`**: A 2-6 letter uppercase code for the sub-domain (e.g., `STRUCTURE`, `POLICY`, `CONVENTIONS`).
    *   **`PRIMARY_TOPIC_KEYWORD`**: An uppercase, concise keyword (or hyphenated multi-word keyword) indicating the main subject (e.g., `KB-ROOT`, `NAMING`, `LAYERED-INFORMATION`).
    *   **`OPTIONAL_SECONDARY_TOPICS*`**: Optional, hyphenated uppercase keywords for further specification.
*   **Filename and `standard_id` Equivalence:** The filename (excluding the `.md` extension) for these atomic standard documents MUST be **identical** to their `standard_id` frontmatter value.
*   **Example:**
    *   `standard_id: SF-CONVENTIONS-NAMING` results in filename: `SF-CONVENTIONS-NAMING.md`
    *   `standard_id: AS-STRUCTURE-KB-ROOT` results in filename: `AS-STRUCTURE-KB-ROOT.md`
*   **Notes:** This convention supersedes and refines the previous Rule 1.2 from U-FORMAT-NAMING-001 for these specific types of documents. The structure of the `standard_id` itself (and thus the filename) is further detailed in [[MT-SCHEMA-FRONTMATTER]].

### Rule 3.2: General Content Files (Non-Standard Definitions) (Derived from U-FORMAT-NAMING-001, Rule 1.3)
For general content files (e.g., chapters within a KB part, supplementary documents not defining a formal standard), filenames (excluding the `.md` extension) MUST be descriptive and in **all lowercase kebab-case**.
*   **Numerical Prefixes:** Numerical prefixes (e.g., `00-`, `01-`) MAY be used for sequencing if desired.
*   **Example:** `01-introduction-to-research.md`, `llm-capabilities-overview.md`, `glossary-of-terms.md`
*   **Notes:** This applies to typical content articles within various knowledge bases.

### Rule 3.3: Collection/Grouping Documents (Derived from U-FORMAT-NAMING-001, Rule 1.4)
Files that group related individual standard definitions or discuss a category (often found within the standards knowledge base itself) MUST use the following pattern: `COL-{SUBJECT}-{DESCRIPTOR}.md`.
*   **`COL-` prefix:** Literal and uppercase.
*   **`{SUBJECT}` and `{DESCRIPTOR}`:** Uppercase, concise, hyphenated keywords.
*   **Example:** `COL-ARCH-UNIVERSAL.md`, `COL-SYNTAX-MARKDOWN.md`
*   **Notes:** This structured naming helps identify documents that serve as collections or high-level groupings.

### Rule 3.4: Guide Documents (Derived from U-FORMAT-NAMING-001, Rule 1.5)
Files that provide guidance on using items, processes, or standards MUST use the following pattern: `GUIDE-{TASK_OR_SUBJECT}.md`.
*   **`GUIDE-` prefix:** Literal and uppercase.
*   **`{TASK_OR_SUBJECT}`:** Uppercase, concise, hyphenated keywords.
*   **Example:** `GUIDE-STANDARDS-SUBMISSION-PROCESS.md`, `GUIDE-USING-THE-INDEXER.md`

### Rule 3.5: Script Files and Their Documentation (Derived from U-FORMAT-NAMING-001, Rule 1.7)
*   **Script Files:** Script basenames (e.g., for `.py`, `.sh` files) SHOULD use **snake_case** and reside in appropriate subdirectories within `/master-knowledge-base/tools/` (e.g., `linter/kb_linter.py`).
*   **User Guides for Scripts:** User-facing guides for scripts SHOULD follow the `GUIDE-` pattern (see Rule 3.4) and may reside in a `docs/` subdirectory near the script (e.g., `/master-knowledge-base/tools/linter/docs/GUIDE-KB-LINTER-USAGE.md`).
*   **Technical Documentation for Scripts:** Detailed technical or developer documentation for scripts SHOULD also reside in a `docs/` subdirectory and may use a pattern like `DOC-{SCRIPT_NAME}-{ASPECT}.md` (e.g., `/master-knowledge-base/tools/linter/docs/DOC-KB-LINTER-ARCHITECTURE.md`).

### Rule 3.6: Reserved Names for Structural Files (Derived from U-FORMAT-NAMING-001, Rule 1.6)
Certain filenames are reserved for specific structural purposes and MUST be used exactly as specified (all lowercase kebab-case where applicable).
*   **Examples:** `root.md`, `_overview.md`, `_kb_definition.md`, `_key_definitions.md`, `kb-directory.md`, `tag-glossary-definition.md`, `tpl-canonical-frontmatter.md`.
*   **Notes:** Adherence to these reserved names is crucial for architectural consistency and proper functioning of automated tools. Refer to specific standards defining these files for their exact locations and purposes.

## 4. Cross-References
- [[MT-SCHEMA-FRONTMATTER]] - Defines the structure of `standard_id`, which is integral to standard document naming.
- [[SF-LINKS-INTERNAL-SYNTAX]] - Relevant for how names might be used in links.

---
*This standard (SF-CONVENTIONS-NAMING) is based on rules 1.1 through 1.8 previously defined in U-FORMAT-NAMING-001 from COL-ARCH-UNIVERSAL.md, with Rule 1.2 significantly refined by the new atomic standard document naming convention (Rule 3.1 here).*
```
