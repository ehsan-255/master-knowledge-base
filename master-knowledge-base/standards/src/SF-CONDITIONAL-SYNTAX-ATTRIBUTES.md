---
title: 'Standard: Syntax for Conditional Attributes in IF Callouts'
standard_id: SF-CONDITIONAL-SYNTAX-ATTRIBUTES
aliases:
  - Conditional Syntax
  - IF Callout Condition Syntax
tags:
  - status/draft
  - criticality/p2-medium
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Conditional Attribute Syntax
related-standards:
  - SF-CALLOUTS-SYNTAX
  - CS-CONTENT-PROFILING-POLICY
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-05-30T12:00:00Z'
primary_domain: SF
sub_domain: CONDITIONAL
scope_application: Defines the syntax for the condition string used within `[!IF condition]`
  callout blocks (as defined in SF-CALLOUTS-SYNTAX).
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Content profiling logic
  - Automated content filtering
  - Authoring consistency for conditional text
change_log_url: ./changelog.md
---
# Standard: Syntax for Conditional Attributes in IF Callouts (SF-CONDITIONAL-SYNTAX-ATTRIBUTES)

## 1. Standard Statement

This standard defines the specific syntax for the `condition` string used within `[!IF condition]` callout blocks. The general syntax for callouts, including the `[!IF ...]` type, is defined in [[SF-CALLOUTS-SYNTAX]]. This document focuses solely on the structure and format of the `condition` part itself. Adherence to this syntax is crucial for consistent parsing and application of content profiling rules.

The actual list of permissible attributes and their corresponding values for use in conditions is defined and managed by the [[CS-CONTENT-PROFILING-POLICY]].

## 2. Core Syntax Rules for Condition Strings

### Rule 2.1: Condition Format (`attribute=value` pairs) (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rule 1.2 - part)
The condition string within an `[!IF condition]` callout MUST consist of one or more `attribute=value` pairs.
*   **Syntax:** `attribute=value`
*   **Example:** `audience=expert`
*   **Rationale:** This simple key-value format allows for clear and parsable conditions.

### Rule 2.2: Multiple Conditions (AND logic) (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rule 1.2 - part)
Multiple `attribute=value` pairs within a single `[!IF condition]` block can be combined using the keyword `AND`.
*   **Case Insensitivity:** The `AND` keyword is case-insensitive (i.e., `AND`, `and`, `And` are all acceptable, but `AND` is preferred for consistency).
*   **Syntax:** `attribute1=value1 AND attribute2=value2`
*   **Example:** `audience=expert AND platform=linux`
*   **Rationale:** Allows for more granular control over content visibility by combining multiple profiling criteria.

### Rule 2.3: `OR` Logic Not Supported in Single Block (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rule 1.2 - part)
`OR` logic is NOT directly supported within a single `[!IF condition]` block.
*   **Guidance:** If `OR` logic is required (e.g., show content if `audience=expert OR audience=developer`), this MUST be achieved by using separate `[!IF ...]` blocks for each condition.
    ```markdown
    > [!IF audience=expert]
    > This content is for experts.

    > [!IF audience=developer]
    > This content is for developers. 
    > (Note: If the content is identical, it would be duplicated here. This highlights a limitation.)
    ```
*   **Rationale:** Keeps the condition parsing logic simple. Complex boolean expressions are difficult to manage and parse reliably within this syntax.

### Rule 2.4: No Spaces in Attributes or Values; Value Formatting (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rule 1.3)
Attribute names and their assigned values MUST NOT contain spaces.
*   **Attribute Names:** SHOULD be concise and descriptive (e.g., `audience`, `platform`, `feature-flag`).
*   **Values:**
    *   Values also MUST NOT contain spaces.
    *   If a value consists of multiple words, it SHOULD be formatted using **kebab-case** (e.g., `expert-user`, `early-adopter-preview`).
*   **Assignment:** The equals sign (`=`) MUST NOT be surrounded by spaces.
    *   **Correct:** `audience=expert-user`
    *   **Incorrect:** `audience = expert-user`, `audience=expert user`
*   **Rationale:** Ensures simple and unambiguous parsing of the condition string.

## 3. Valid Condition String Examples

*   `audience=expert`
*   `platform=windows`
*   `feature-flag=new-dashboard AND audience=internal-tester`
*   `version=v2.1 AND audience=all` (assuming `all` is a defined value for `audience`)
*   `os=macos AND display-mode=dark`

## 4. Management of Attributes and Values

The list of approved profiling attributes (e.g., `audience`, `platform`) and their permissible values (e.g., `expert`, `novice` for `audience`) is defined and managed by the [[CS-CONTENT-PROFILING-POLICY]]. This standard only defines the syntax for how these attribute-value pairs are expressed within a condition string.

## 5. Importance of Consistent Condition Syntax

*   **Reliable Parsing:** Ensures that tools designed to process conditional content can reliably parse and interpret the conditions.
*   **Authoring Clarity:** Provides a clear and unambiguous way for authors to specify conditions.
*   **Maintainability:** Standardized syntax makes it easier to review, update, and manage conditional blocks across the knowledge base.

## 6. Scope of Application

This standard applies to the condition string within all `[!IF condition]` callout blocks used in Markdown documents across the knowledge base.

## 7. Cross-References
- [[SF-CALLOUTS-SYNTAX]] - Defines the general syntax for callout blocks, including the `[!IF ...]` type.
- [[CS-CONTENT-PROFILING-POLICY]] - Defines the approved list of profiling attributes and their values, and the overall policy for content profiling.

---
*This standard (SF-CONDITIONAL-SYNTAX-ATTRIBUTES) is based on rules 1.2 and 1.3 previously defined in M-CONDITIONAL-TEXT-SYNTAX-001.*
