---
title: 'Policy: Content Profiling and Conditional Text'
standard_id: CS-CONTENT-PROFILING-POLICY
aliases:
- Conditional Text Policy
- Content Profiling Strategy
- Audience Targeting
tags:
- status/draft
- criticality/p2-medium
- content-type/policy-document
kb-id: standards
info-type: policy-document
primary-topic: Content Profiling Strategy
related-standards:
- SF-CALLOUTS-SYNTAX
- SF-CONDITIONAL-SYNTAX-ATTRIBUTES
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-01T23:30:16Z'
primary_domain: CS
sub_domain: POLICY
scope_application: Governs the strategy, implementation, and management of content profiling and conditional text display within knowledge base documents.
criticality: P2-Medium
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
- Personalized content delivery
- Content relevance
- Authoring complexity
- Maintenance of profiled content
- User experience
---

# Policy: Content Profiling and Conditional Text (CS-CONTENT-PROFILING-POLICY)

## 1. Policy Statement

This policy governs the strategy for content profiling and the implementation of conditional text within knowledge base documents. Content profiling allows for tailoring content to specific audiences, platforms, feature versions, or other defined contexts. This is achieved using conditional text blocks, which display content only when specified conditions are met.

## 2. Purpose of Content Profiling

Content profiling and conditional text serve several key purposes:
*   **Targeted Information:** Delivering information that is most relevant to a specific user group or situation (e.g., novice vs. expert users, different operating systems).
*   **Reduced Clutter:** Hiding information that is not relevant to a particular context, making documents less overwhelming and easier to navigate.
*   **Single-Sourcing (with Variation):** Managing variations of information within a single document, reducing duplication and simplifying updates for common content.
*   **Phased Rollout:** Allowing documentation for new or beta features to be present but hidden until the feature is generally available.

## 3. Implementation of Conditional Text

### Rule 3.1: Use of `[!IF condition]` Callouts (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rule 1.1)
Conditional text blocks MUST be implemented using the `[!IF condition]` callout syntax as defined in [[SF-CALLOUTS-SYNTAX]].
*   **Syntax Reminder:** `> [!IF condition]`
*   **Rationale:** Provides a standardized and visually distinct way to mark conditional content.

### Rule 3.2: Condition String Syntax
The `condition` string within the `[!IF condition]` callout MUST adhere to the syntax defined in [[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]].
*   **Syntax Reminder:** Conditions are `attribute=value` pairs, combinable with `AND` (case-insensitive). `OR` logic requires separate blocks. Attribute names and values must not contain spaces; values should use kebab-case for multiple words.
*   **Rationale:** Ensures conditions are parsable and consistently interpreted.

### Rule 3.3: Content Indentation and Structure (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rules 1.4 & 1.5)
All content that is conditional upon the `IF` statement MUST be correctly indented under the callout, following standard callout content rules as specified in [[SF-CALLOUTS-SYNTAX]].
*   **Guidance:** Conditional blocks can span multiple paragraphs, lists, or other Markdown elements, as long as each line of the conditional content starts with the callout marker (`> `) and appropriate indentation for nested elements within the callout.
*   **Rationale:** Ensures correct rendering and association of content with its condition.

### Rule 3.4: Blank Lines Around Conditional Blocks (Derived from M-CONDITIONAL-TEXT-SYNTAX-001, Rule 1.6)
A blank line SHOULD precede and follow a conditional block for readability, unless it is immediately followed by another related conditional block (e.g., a series of mutually exclusive conditions). This aligns with [[SF-FORMATTING-FILE-HYGIENE]].
*   **Rationale:** Improves visual separation and parsing reliability.

## 4. Profiling Attributes and Values (Authoritative Source)

This policy document is the authoritative source for defining and managing the permissible profiling attributes and their corresponding values. This replaces any previous documents like `U-PROFILING-ATTRIBUTES-001.md`.

### Rule 4.1: Initial List of Approved Attributes and Values
The following attributes and example values are initially approved for use. Values SHOULD be in kebab-case if multi-word.

*   **`audience`**: Defines the target audience for the content.
    *   `novice`: Users new to the subject or product.
    *   `intermediate`: Users with some experience but not experts.
    *   `expert`: Users with deep knowledge and experience.
    *   `developer`: Users who are software developers.
    *   `admin`: System administrators or users with administrative privileges.
    *   `internal-only`: For content intended only for internal team members.
*   **`platform`**: Specifies the operating system or platform.
    *   `windows`
    *   `linux`
    *   `macos`
    *   `ios`
    *   `android`
    *   `web` (for web browser based platforms/features)
*   **`feature-version`**: Specifies a version of a feature (distinct from document version).
    *   `v1.0`
    *   `v2.x`
    *   `beta`
    *   `alpha`
*   **`deployment-model`**: Specifies the deployment environment.
    *   `cloud`
    *   `on-premises`
    *   `hybrid`
*   **`access-level`**: Specifies user access or permission levels.
    *   `user`
    *   `premium-user`
    *   `administrator`

### Rule 4.2: Process for Managing Attributes and Values
*   **Proposal:** New attributes or values, or changes to existing ones, MUST be proposed to the designated governance body (e.g., Editorial Board, Standards Committee).
*   **Review:** Proposals will be reviewed for clarity, necessity, potential overlap, and impact on the overall profiling strategy.
*   **Approval & Documentation:** Approved attributes and values will be formally added to this policy document (Rule 4.1). Changes to this section MUST follow the standard versioning and changelog process for this policy document itself, as defined in [[OM-VERSIONING-CHANGELOGS]].
*   **Rationale:** Ensures that the set of profiling attributes and values remains controlled, consistent, and aligned with the evolving needs of the knowledge base.

## 5. Illustrative Examples of Conditional Text Usage

### Example 5.1: Audience-Specific Content
```markdown
General introduction to the feature.

> [!IF audience=expert]
> For expert users, you can further optimize performance by adjusting the following parameters in the configuration file:
> - `max_cache_size`
> - `thread_pool_count`

> [!IF audience=novice]
> If you are new to this feature, we recommend starting with the default settings. You can learn more about configuration in the [[GUIDE-FEATURE-ADVANCED-SETTINGS]].

This concludes the feature description.
```

### Example 5.2: Platform-Specific Instructions
```markdown
To install the software:

> [!IF platform=windows]
> 1. Download the `setup.exe` installer.
> 2. Double-click the installer and follow the on-screen prompts.

> [!IF platform=linux]
> 1. Download the `.tar.gz` archive.
> 2. Extract the archive: `tar -xvzf package.tar.gz`
> 3. Run the installation script: `sudo ./install.sh`

> [!IF platform=macos]
> 1. Download the `.dmg` file.
> 2. Open the `.dmg` and drag the application icon to your Applications folder.
```

## 6. Importance of a Content Profiling Policy

*   **Targeted Communication:** Enables delivery of the right information to the right audience at the right time.
*   **Improved User Experience:** Reduces information overload and makes content more relevant to the user's context.
*   **Maintainability:** While adding complexity, it can help manage variations of content within a single source if used carefully.
*   **Consistency:** Ensures a consistent approach to conditional content across the knowledge base.

## 7. Scope of Application

This policy applies to all content within the knowledge base where conditional text is used for profiling or selective display. All authors and editors MUST adhere to this policy when implementing conditional content.

## 8. Cross-References
- [[SF-CALLOUTS-SYNTAX]] - Defines the general syntax for callout blocks, including the `[!IF ...]` type.
- [[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]] - Defines the specific syntax for the condition string within `[!IF ...]` callouts.
- [[OM-VERSIONING-CHANGELOGS]] - For versioning this policy document when attributes/values are updated.

---
*This policy (CS-CONTENT-PROFILING-POLICY) is based on rules 1.1, 1.4, 1.5, and 1.6 previously defined in M-CONDITIONAL-TEXT-SYNTAX-001. It also establishes itself as the new authoritative source for profiling attributes and values, superseding U-PROFILING-ATTRIBUTES-001.*
