---

title: 'Standard: YAML Frontmatter Syntax'
standard_id: SF-SYNTAX-YAML-FRONTMATTER
aliases:
- YAML Frontmatter
- Frontmatter Syntax
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: YAML Frontmatter Syntax
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating YAML frontmatter in knowledge base
  documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Frontmatter syntax
- Metadata structure
- Document parsing
---
# Standard: Markdown YAML Frontmatter Syntax (SF-SYNTAX-YAML-FRONTMATTER)

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax for YAML frontmatter in all Knowledge Base documents. Adherence is **CRITICAL** for reliable metadata parsing, content validation, authoring consistency, and interoperability with tooling.

While this standard governs the *syntax* of the YAML block, the *schema and content rules* (e.g., allowed keys, value formats, mandatory fields) are defined in [[MT-SCHEMA-FRONTMATTER]]. File encoding (UTF-8 without BOM) and line endings (LF) are governed by [[SF-FORMATTING-FILE-HYGIENE]].

## 2. Core YAML Syntax Rules for Frontmatter

### Rule 2.1: Delimiters and Placement
A single YAML frontmatter block, enclosed by triple hyphens (`---`) on the line immediately before and after the YAML content, **MUST** be present at the very beginning of every Markdown document.
*   **Requirement:** No content, blank lines, or whitespace are permitted before the opening `---` delimiter. The document **MUST** start with this delimiter on line 1.
*   **Example:**
    ```yaml
    ---
    title: My Document
    ---
    # Markdown content starts here
    ```
*   **Rationale:** Ensures consistent and unambiguous detection of the frontmatter block by parsers and other tools.

### Rule 2.2: Key Naming Convention (kebab-case)
All keys within the YAML frontmatter block **MUST** use **kebab-case** (all lowercase words separated by single hyphens).
*   **Example (Correct):** `date-created: 2023-10-28`, `primary-topic: "Example Topic"`
*   **Example (Incorrect):** `date_created: 2023-10-28`, `PrimaryTopic: "Example Topic"`
*   **Rationale:** Enforces a single, consistent style for all YAML keys, simplifying parsing and improving readability. This is also mandated by [[MT-SCHEMA-FRONTMATTER]].

### Rule 2.3: Appropriate Data Types
Values for YAML keys **MUST** use appropriate YAML data types (e.g., string, number, boolean, list, dictionary/map).
*   **Strings:** Strings do not typically require quotes. However, quotes (preferably single quotes for consistency, unless double quotes are needed for specific character escaping) **MUST** be used if the string:
    *   Contains special characters that could be misinterpreted by the YAML parser (e.g., colons, hashes, brackets, leading/trailing whitespace that is significant).
    *   Is a number, boolean, or null-like value that should be treated as a string (e.g., `version: '1.0'`, `status: 'true'`).
*   **Numbers:** `version: 1.0` (float), `count: 15` (integer).
*   **Booleans:** `draft: true`, `is-archived: false`.
*   **Nulls:** `not-applicable: null` (use `null` explicitly, not empty strings if null is intended).
*   **Rationale:** Correct data typing is essential for reliable parsing and processing of metadata. [[MT-SCHEMA-FRONTMATTER]] specifies expected data types.

### Rule 2.4: List Syntax (Block Style)
Lists (arrays) in YAML frontmatter **MUST** use the block list syntax, where each item is preceded by a hyphen and a space (`- `).
*   **Example (Correct):**
    ```yaml
    tags:
      - standards
      - metadata
      - yaml
    ```
*   **Incorrect (Inline Style PROHIBITED):**
    ```yaml
    tags: [standards, metadata, yaml]
    ```
*   **Rationale:** Block list syntax is generally more readable for multi-item lists and is the mandated style for consistency.

### Rule 2.5: No Non-YAML Metadata
HTML comments (e.g., `<!-- comment -->`), or any other non-YAML content or comments, **MUST NOT** be used within the YAML frontmatter block.
*   **Rationale:** The frontmatter block is exclusively for machine-readable YAML metadata. Comments or other content can break parsers. YAML's own comment syntax (`# comment`) should be used if comments are necessary, though generally discouraged for standardized metadata fields.

## 3. Illustrative Example of Correct Frontmatter Syntax

```yaml
---
title: 'Example Standard Document'
standard_id: 'SF-EXAMPLE-DOC-001'
aliases:
  - Example Alias One
  - Example Alias Two
tags:
  - topic/example
  - status/draft
  - content-type/standard-definition
version: '0.1.0'
date-created: '2024-07-15T10:00:00Z'
is-experimental: true
complexity-score: 3
contact-person: null
---

# Document Content Starts Here

This section illustrates the start of the Markdown content, immediately following the closing `---` delimiter of the frontmatter block.
```

## 4. Scope of Application

This standard applies to the YAML frontmatter block of all Markdown documents within the Knowledge Base repository. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 5. Cross-References
*   [[MT-SCHEMA-FRONTMATTER]]
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-YAML-FRONTMATTER) is based on rules 1.1 through 1.5 previously defined in M-SYNTAX-YAML-001 from COL-SYNTAX-MARKDOWN.md.*
