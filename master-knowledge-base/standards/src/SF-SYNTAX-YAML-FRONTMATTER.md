---
title: "Standard: Markdown YAML Frontmatter Syntax"
standard_id: "SF-SYNTAX-YAML-FRONTMATTER"
aliases: ["YAML Frontmatter Syntax", "Frontmatter Syntax Standard"]
tags:
  - status/draft
  - criticality/P1-High # Correct syntax is essential for parsing
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "YAML Frontmatter Syntax" # As per prompt
related-standards: ["U-METADATA-FRONTMATTER-RULES-001_ID_PLACEHOLDER", "SF-FORMATTING-FILE-HYGIENE_ID_PLACEHOLDER"]
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "SYNTAX" # As per prompt
scope_application: "Defines the mandatory YAML syntax conventions for frontmatter blocks in all Markdown documents within the knowledge base."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Metadata parsing", "Content validation", "Authoring consistency", "Interoperability with tools"]
change_log_url: "./SF-SYNTAX-YAML-FRONTMATTER-changelog.md" # Placeholder
---

# Standard: Markdown YAML Frontmatter Syntax (SF-SYNTAX-YAML-FRONTMATTER)

## 1. Standard Statement

This standard defines the mandatory YAML syntax conventions for frontmatter blocks used in all Markdown documents within the knowledge base. Adherence to these syntax rules is essential for ensuring reliable metadata parsing, supporting content validation, maintaining authoring consistency, and ensuring interoperability with various processing tools.

While this standard governs the *syntax* of the YAML block itself, the *schema and content rules* for the frontmatter (e.g., allowed keys, specific value formats like ISO dates for `date-created`, mandatory fields) are defined in [[MT-SCHEMA-FRONTMATTER]]. File encoding (UTF-8 without BOM) and line endings (LF) are governed by [[SF-FORMATTING-FILE-HYGIENE]].

## 2. Core YAML Syntax Rules for Frontmatter

### Rule 2.1: Delimiters and Placement (Derived from M-SYNTAX-YAML-001, Rule 1.1)
A single YAML frontmatter block, enclosed by triple hyphens (`---`) on the line immediately before and after the YAML content, MUST be present at the very beginning of every Markdown document.
*   **Requirement:** No content, blank lines, or whitespace are permitted before the opening `---` delimiter. The document must start with this delimiter on line 1.
*   **Example:**
    ```yaml
    ---
    # YAML content starts on the next line
    title: My Document
    ---
    # Markdown content starts here
    ```
*   **Rationale:** Ensures consistent and unambiguous detection of the frontmatter block by parsers and other tools.

### Rule 2.2: Key Naming Convention (kebab-case) (Derived from M-SYNTAX-YAML-001, Rule 1.2)
All keys within the YAML frontmatter block MUST use **kebab-case** (all lowercase words separated by single hyphens).
*   **Example (Correct):** `date-created: 2023-10-28`, `primary-topic: "Example Topic"`
*   **Example (Incorrect):** `date_created: 2023-10-28`, `PrimaryTopic: "Example Topic"`
*   **Rationale:** Enforces a single, consistent style for all YAML keys, simplifying parsing and improving readability. This is also mandated by [[U-METADATA-FRONTMATTER-RULES-001_ID_PLACEHOLDER]].

### Rule 2.3: Appropriate Data Types (Derived from M-SYNTAX-YAML-001, Rule 1.3)
Values for YAML keys MUST use appropriate YAML data types (e.g., string, number, boolean, list, dictionary/map).
*   **Strings:** Strings do not typically require quotes. However, quotes (preferably single quotes for consistency, unless double quotes are needed for specific character escaping) MUST be used if the string:
    *   Contains special characters that could be misinterpreted by the YAML parser (e.g., colons, hashes, brackets, leading/trailing whitespace that is significant).
    *   Is a number, boolean, or null-like value that should be treated as a string (e.g., `version: '1.0'`, `status: 'true'`).
*   **Numbers:** `version: 1.0` (interpreted as a float), `count: 15` (interpreted as an integer).
*   **Booleans:** `draft: true`, `is-archived: false`.
*   **Nulls:** `not-applicable: null` (use `null` explicitly, not empty strings if the intent is a null value).
*   **Rationale:** Correct data typing is essential for reliable parsing and subsequent processing of metadata. [[U-METADATA-FRONTMATTER-RULES-001_ID_PLACEHOLDER]] specifies the expected data types for its defined keys.

### Rule 2.4: List Syntax (Block Style) (Derived from M-SYNTAX-YAML-001, Rule 1.4)
Lists (arrays) in YAML frontmatter MUST use the block list syntax, where each item is preceded by a hyphen and a space (`- `).
*   **Example (Correct):**
    ```yaml
    tags:
      - standards
      - metadata
      - yaml
    ```
*   **Incorrect (Inline Style MUST NOT be used):**
    ```yaml
    tags: [standards, metadata, yaml]
    ```
*   **Rationale:** Block list syntax is generally more readable for lists of more than one or two short items and is the mandated style for consistency.

### Rule 2.5: No Non-YAML Metadata (Derived from M-SYNTAX-YAML-001, Rule 1.5)
HTML comments (e.g., `<!-- comment -->`), or any other non-YAML content or comments, MUST NOT be used within the YAML frontmatter block.
*   **Rationale:** The frontmatter block is exclusively for machine-readable YAML metadata. Comments or other content can break parsers or lead to unpredictable behavior. YAML's own comment syntax (`# comment`) should be used if comments are necessary within the frontmatter, though they are generally discouraged for standardized metadata fields.

## 3. Illustrative Example of Correct Frontmatter Syntax

```yaml
---
title: 'Example Standard Document with Correct YAML Syntax'
standard_id: 'SF-EXAMPLE-DOC-001'
aliases:
  - Example Alias One
  - Example Alias Two
tags:
  - topic/example
  - status/draft
  - content-type/standard-definition
version: '0.1.0' # String value, even for numbers, if specified by U-METADATA-FRONTMATTER-RULES-001
date-created: '2024-07-15T10:00:00Z' # ISO-8601 string
is-experimental: true # Boolean
complexity-score: 3 # Number
# This is a valid YAML comment, generally used sparingly.
contact-person: null # Explicit null value
---

# Document Content Starts Here

This section illustrates the start of the Markdown content, immediately following the closing `---` delimiter of the frontmatter block.
```

## 4. Scope of Application

This standard applies to the YAML frontmatter block of all Markdown documents within the knowledge base repository.

## 5. Cross-References
- [[MT-SCHEMA-FRONTMATTER]] - Defines the schema, allowed keys, specific value formats, and overall content rules for frontmatter.
- [[SF-FORMATTING-FILE-HYGIENE]] - Defines file encoding (UTF-8 no BOM) and line ending (LF) requirements applicable to the entire file, including the frontmatter.

---
*This standard (SF-SYNTAX-YAML-FRONTMATTER) is based on rules 1.1 through 1.5 previously defined in M-SYNTAX-YAML-001 from COL-SYNTAX-MARKDOWN.md.*
```
