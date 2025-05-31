---
title: 'Policy: Standards Deprecation Process'
standard_id: OM-POLICY-STANDARDS-DEPRECATION
aliases:
- Deprecation Policy
- Standards Retirement
tags:
- status/draft
- criticality/p2-medium
- content-type/policy-document
kb-id: standards
info-type: policy-document
primary-topic: Standards Deprecation Process
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: OM
sub_domain: LIFECYCLE
scope_application: Defines the process and criteria for deprecating standards within the knowledge base.
criticality: p2-medium
lifecycle_gatekeeper: Governance-Board-Approval
impact_areas:
- Standards lifecycle
- Change management
- Documentation integrity
change_log_url: ./OM-POLICY-STANDARDS-DEPRECATION-changelog.md
---
# Policy: Deprecation of Standards (OM-POLICY-STANDARDS-DEPRECATION)

## 1. Policy Statement

This policy outlines the mandatory procedures for deprecating standards that are superseded, no longer relevant, or outdated. The primary goals are to maintain historical context, clearly communicate the status of standards to all users, and ensure the knowledge base remains current and reliable.

## 2. Core Deprecation Requirements

### Rule 2.1: Preservation through Deprecation (Derived from U-DEPRECATION-001, Rule 1.1)
When a standard is superseded by a new standard or is deemed no longer relevant, it MUST be formally marked as deprecated rather than being deleted outright.
*   **Rationale:** Preserving deprecated standards maintains historical context, allowing users to understand past decisions, track the evolution of practices, and avoid re-solving past issues. It is also crucial for any existing systems or content that might still reference the older standard during a transition period.

### Rule 2.2: Update Frontmatter Status (Derived from U-DEPRECATION-001, Rule 1.2)
The YAML frontmatter of a deprecated standard MUST be updated to reflect its new status. Specifically, its `status/*` tag MUST be changed to `status/deprecated`.
*   **Guidance:** The `status/archived` tag may be used if the standard is not only deprecated but also moved to a separate archive location and is no longer considered part of the active, albeit deprecated, set of standards. The choice between `status/deprecated` (still in place but not active) and `status/archived` (moved and inactive) should be applied consistently based on the archiving strategy (see Rule 2.4).
*   **Reference:** The list of valid status tags is maintained in [[MT-REGISTRY-TAG-GLOSSARY]].
*   **Version Update:** The `version` of the standard should be incremented (typically a MINOR or PATCH update, e.g., from `1.2.0` to `1.3.0` or `1.2.1`) and `date-modified` updated to reflect the deprecation event, as per [[OM-VERSIONING-CHANGELOGS]].

### Rule 2.3: Prominent Deprecation Notice (Derived from U-DEPRECATION-001, Rule 1.3)
The body of a deprecated standard document MUST be prefaced with a prominent and clear "DEPRECATED" notice. This notice MUST:
    a.  Clearly state that the standard is deprecated.
    b.  State the reason for deprecation (e.g., "superseded by...", "no longer applicable due to technology changes...").
    c.  Link directly to any replacing standard(s) if applicable.
*   **Example using a standard callout format (syntax defined in [[SF-CALLOUTS-SYNTAX]]):**
    ```markdown
    > [!WARNING] DEPRECATED: This Standard is No Longer Active
    > **Reason for Deprecation:** This standard has been superseded by `[[XX-REPLACEMENT-STANDARD-ID]]`.
    > **Effective Date:** YYYY-MM-DD
    > Please refer to the new standard for current guidelines. This document is retained for historical purposes only.
    ```
*   **Rationale:** This ensures that any user accessing the deprecated standard is immediately aware of its status and is directed to current information if available.

### Rule 2.4: Archival Strategy (Derived from U-DEPRECATION-001, Rule 1.4)
Deprecated standards SHOULD be moved to a designated "archive" section or folder within the Standards KB structure after a suitable notice period or as part of a regular archival process.
*   **Guidance:**
    *   The specific location (e.g., `/master-knowledge-base/standards/archive/`) should be standardized.
    *   The "notice period" before archival might vary depending on the standard's impact.
    *   Even when archived, the deprecated status and notice within the document should remain.
    *   Links to the archived standard from other documents may need to be updated or marked as pointing to an archived resource.
*   **Rationale:** Archiving helps keep the active sections of the knowledge base current and focused, while still preserving deprecated materials for reference.

## 3. Rationale for Deprecation Policy

A formal deprecation policy is essential for:

*   **Maintaining Relevance:** Ensures the active knowledge base primarily contains current and applicable standards.
*   **Clear Communication:** Provides unambiguous information to users about the status of standards.
*   **Historical Context:** Preserves the evolution of standards and organizational knowledge.
*   **Orderly Transition:** Allows for smoother transitions when standards are updated or replaced.
*   **Avoiding Confusion:** Prevents users from mistakenly applying outdated or irrelevant standards.

## 4. Scope of Application

This policy applies to all standard documents within the knowledge base ecosystem that are subject to lifecycle changes, including supersession or obsolescence.

## 5. Cross-References
- [[MT-REGISTRY-TAG-GLOSSARY]] - For the `status/deprecated` and `status/archived` tags.
- [[SF-CALLOUTS-SYNTAX]] - For the syntax of the deprecation notice callout.
- [[OM-VERSIONING-CHANGELOGS]] - For versioning changes related to deprecation.
- [[OM-POLICY-STANDARDS-GOVERNANCE]] - As the decision to deprecate a standard is a governance action.

---
*This policy (OM-POLICY-STANDARDS-DEPRECATION) is based on rules 1.1 through 1.4 previously defined in U-DEPRECATION-001 from COL-GOVERNANCE-UNIVERSAL.md.*
