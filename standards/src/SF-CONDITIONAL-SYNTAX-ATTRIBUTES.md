---

title: 'Standard: Syntax for Conditional Attributes in IF Callouts'
standard_id: SF-CONDITIONAL-SYNTAX-ATTRIBUTES
aliases:
- Conditional Syntax
- IF Callout Condition Syntax
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p2-medium
- kb-id/standards
- status/active
- topic/conditional
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Conditional Attribute Syntax
related-standards:
- SF-CALLOUTS-SYNTAX
- CS-CONTENT-PROFILING-POLICY
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-18T03:45:00Z'
primary_domain: SF
sub_domain: CONDITIONAL
scope_application: Defines the syntax for the condition string used within `[!IF condition]` callout blocks.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content profiling logic
- Automated content filtering
- Authoring consistency for conditional text
---
# Standard: Syntax for Conditional Attributes in IF Callouts (SF-CONDITIONAL-SYNTAX-ATTRIBUTES)

## 1. Standard Statement

This standard **MANDATES** the specific syntax for the `condition` string used within `[!IF condition]` callout blocks. The general syntax for callouts is defined in [[SF-CALLOUTS-SYNTAX]]. The list of permissible attributes and values is defined in [[CS-CONTENT-PROFILING-POLICY]].

## 2. Core Syntax Rules for Condition Strings

### Rule 2.1: Condition Format
The condition string **MUST** consist of one or more `attribute=value` pairs.
*   **Syntax:** `attribute=value`
*   **Example:** `audience=expert`

### Rule 2.2: Multiple Conditions (AND Logic)
Multiple `attribute=value` pairs can be combined using the keyword `AND`.
*   **Case Insensitivity:** The `AND` keyword is case-insensitive (`AND`, `and`, `And` are acceptable, but `AND` is preferred).
*   **Syntax:** `attribute1=value1 AND attribute2=value2`
*   **Example:** `audience=expert AND platform=linux`

### Rule 2.3: OR Logic Not Supported
`OR` logic is **NOT** supported within a single `[!IF condition]` block.
*   **Alternative:** Use separate `[!IF ...]` blocks for each condition when OR logic is required.
    ```markdown
    > [!IF audience=expert]
    > This content is for experts.

    > [!IF audience=developer]
    > This content is for developers.
    ```

### Rule 2.4: Attribute and Value Formatting
*   **No Spaces:** Attribute names and values **MUST NOT** contain spaces
*   **Values:** Multi-word values **SHOULD** use **kebab-case** (e.g., `expert-user`, `early-adopter-preview`)
*   **Assignment:** The equals sign (`=`) **MUST NOT** be surrounded by spaces
*   **Correct:** `audience=expert-user`
*   **Prohibited:** `audience = expert-user`, `audience=expert user`

## 3. Valid Condition String Examples

*   `audience=expert`
*   `platform=windows`
*   `feature-flag=new-dashboard AND audience=internal-tester`
*   `version=v2.1 AND audience=all`
*   `os=macos AND display-mode=dark`

## 4. Management of Attributes and Values

The list of approved profiling attributes (e.g., `audience`, `platform`) and their permissible values (e.g., `expert`, `novice`) is defined and managed by [[CS-CONTENT-PROFILING-POLICY]].

## 5. Scope of Application

This standard applies to the condition string within **ALL** `[!IF condition]` callout blocks used in Markdown documents across the Knowledge Base.

## 6. Cross-References
- [[SF-CALLOUTS-SYNTAX]]
- [[CS-CONTENT-PROFILING-POLICY]]

---
*This standard (SF-CONDITIONAL-SYNTAX-ATTRIBUTES) establishes precise syntax requirements for conditional attributes, ensuring reliable parsing and consistent authoring for content profiling.*
