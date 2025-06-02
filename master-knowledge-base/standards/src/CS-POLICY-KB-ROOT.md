---
title: 'Policy: Consistent Application of Knowledge Base Root Structure'
standard_id: CS-POLICY-KB-ROOT
aliases:
- KB Root Consistency Policy
tags:
- status/draft
- criticality/p2-medium
- content-type/policy-document
kb-id: standards
info-type: policy-document
primary-topic: KB Root Structure Application Policy
related-standards:
- AS-STRUCTURE-KB-ROOT
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-01T23:34:47Z'
primary_domain: CS
sub_domain: POLICY
scope_application: Ensures consistent application of the KB root structure choices defined in AS-STRUCTURE-KB-ROOT across all Knowledge Bases.
criticality: P2-Medium
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
- User experience
- KB navigability
- Authoring consistency
- Maintainability
change_log_url: ./changelog.md
---

# Policy: Consistent Application of Knowledge Base Root Structure (CS-POLICY-KB-ROOT)

## 1. Policy Statement

This policy mandates the consistent application of structural choices for Knowledge Base (KB) root organization, as defined in standard [[AS-STRUCTURE-KB-ROOT]]. Specifically, it pertains to the organization of top-level "Parts" (primary sections) within a KB.

## 2. Core Requirement

### Rule 2.1: Consistent Structure for "Parts" (Derived from U-ARCH-001, Rule 1.6)
The chosen method for organizing top-level "Parts" — either as distinct sub-folders (for larger KBs) or as major H1 sections within the `root.md` file (for smaller KBs) — MUST be consistently applied throughout a single Knowledge Base.
*   **Reference:** See [[AS-STRUCTURE-KB-ROOT#Rule 1.4: Top-Level "Parts" in Larger KBs (Sub-folders)]] and [[AS-STRUCTURE-KB-ROOT#Rule 1.5: Top-Level "Parts" in Smaller KBs (`root.md` Sections)]].
*   **Guidance:** A KB should not mix these two approaches. For instance, one Part should not be a sub-folder while another Part in the same KB is an H1 section in `root.md`.

## 3. Rationale and Importance

Adherence to this policy is crucial for several reasons:

*   **User Experience & Navigability:** A consistent structure makes it easier for users to understand, navigate, and predict how content is organized within any given KB. Inconsistent structures can lead to confusion and difficulty in locating information.
*   **Authoring Consistency:** Clear rules on KB structure simplify the authoring process, as contributors do not have to guess how to organize new top-level sections.
*   **Maintainability:** Uniformity in structure reduces complexity when performing maintenance tasks, refactoring content, or applying batch updates.
*   **Automation & Tooling:** Automated tools for validation, indexing, or building KB views rely on predictable structures. Inconsistencies can break these tools or lead to incorrect outputs.
*   **Scalability:** While [[AS-STRUCTURE-KB-ROOT]] provides options for different KB sizes, this policy ensures that the chosen option is applied uniformly, supporting clearer growth paths for KBs. If a "smaller" KB grows, a decision to refactor its Part structure to sub-folders should be applied to all Parts.

## 4. Scope of Application

This policy applies to all Knowledge Bases developed and maintained within the organization.

## 5. Decision Criteria for "Larger" vs. "Smaller" KBs

While [[AS-STRUCTURE-KB-ROOT]] outlines the two structural options for Parts based on KB size, the decision to classify a KB as "larger" (requiring sub-folders for Parts) versus "smaller" (allowing H1 sections in `root.md` for Parts) should be guided by the following considerations:

*   **Number of Top-Level Parts:** If a KB is anticipated to have more than 5-7 top-level Parts, using sub-folders is generally recommended.
*   **Depth of Content within Parts:** If individual Parts are expected to contain a large number of "Chapters" or deep sub-sections, sub-folders provide better organization from the outset.
*   **Complexity of `root.md`:** If the `root.md` file becomes excessively long or difficult to manage due to numerous H1 sections and their inline ToCs, transitioning to sub-folders for Parts is advisable.
*   **Team Size and Collaboration:** Larger teams or more complex collaborative environments may benefit from the clearer separation provided by sub-folders.

The final decision rests with the KB owners or architects, but it should be made with long-term scalability and user experience in mind, and once made, applied consistently as per Rule 2.1.

## 6. Cross-References
- [[AS-STRUCTURE-KB-ROOT]] - Defines the technical structure for KB root organization.

---
*This policy (CS-POLICY-KB-ROOT) supports rule 1.6 previously defined in U-ARCH-001 from COL-ARCH-UNIVERSAL.md.*
