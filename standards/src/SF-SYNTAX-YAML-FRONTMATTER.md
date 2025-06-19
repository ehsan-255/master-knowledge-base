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
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: YAML Frontmatter Syntax
related-standards:
- MT-SCHEMA-FRONTMATTER
- SF-FORMATTING-FILE-HYGIENE
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-18T03:10:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the syntax for creating YAML frontmatter in knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Frontmatter syntax
- Metadata structure
- Document parsing
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Markdown YAML Frontmatter Syntax (SF-SYNTAX-YAML-FRONTMATTER)

## 1. Standard Statement

This standard **MANDATES** the exclusive syntax for YAML frontmatter in all Knowledge Base documents. While this standard governs the *syntax* of the YAML block, the *schema and content rules* are defined in [[MT-SCHEMA-FRONTMATTER]]. File encoding and line endings are governed by [[SF-FORMATTING-FILE-HYGIENE]].

## 2. Core YAML Syntax Rules for Frontmatter

### Rule 2.1: Delimiters and Placement
A YAML frontmatter block enclosed by triple hyphens (`---`) **MUST** be present at the very beginning of every Markdown document.
*   **Requirement:** No content, blank lines, or whitespace permitted before the opening `---` delimiter. The document **MUST** start with this delimiter on line 1.
*   **Example:**
    ```yaml
    ---
    title: My Document
    ---
    # Markdown content starts here
    ```

### Rule 2.2: Key Naming Convention (kebab-case)
All keys within the YAML frontmatter block **MUST** use **kebab-case** (lowercase words separated by hyphens).
*   **Correct:** `date-created: 2023-10-28`, `primary-topic: "Example Topic"`
*   **Prohibited:** `date_created: 2023-10-28`, `PrimaryTopic: "Example Topic"`

### Rule 2.3: Appropriate Data Types
Values **MUST** use appropriate YAML data types.
*   **Strings:** Do not typically require quotes. Use quotes if the string:
    *   Contains special characters that could be misinterpreted (colons, hashes, brackets)
    *   Is a number/boolean that should be treated as string (`version: '1.0'`, `status: 'true'`)
*   **Numbers:** `version: 1.0` (float), `count: 15` (integer)
*   **Booleans:** `draft: true`, `is-archived: false`
*   **Nulls:** `not-applicable: null`

### Rule 2.4: List Syntax (Block Style)
Lists **MUST** use block list syntax with hyphens and spaces (`- `).
*   **Correct:**
    ```yaml
    tags:
      - standards
      - metadata
      - yaml
    ```
*   **Prohibited (Inline Style):**
    ```yaml
    tags: [standards, metadata, yaml]
    ```

### Rule 2.5: No Non-YAML Metadata
HTML comments or non-YAML content **MUST NOT** be used within the YAML frontmatter block.

## 3. Complete Example

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

This standard applies to the YAML frontmatter block of **ALL** Markdown documents within the Knowledge Base repository. Adherence is **MANDATORY** for all content creators, automated systems, and tooling.

## 5. Cross-References
*   [[MT-SCHEMA-FRONTMATTER]]
*   [[SF-FORMATTING-FILE-HYGIENE]]

---
*This standard (SF-SYNTAX-YAML-FRONTMATTER) establishes strict YAML frontmatter syntax requirements, ensuring consistent metadata structure across the Knowledge Base.*
