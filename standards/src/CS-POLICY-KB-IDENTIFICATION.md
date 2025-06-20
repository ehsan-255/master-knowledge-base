---

title: 'Policy: Unique Knowledge Base Identification and Naming'
standard_id: CS-POLICY-KB-IDENTIFICATION
aliases:
- KB Naming Policy
- Unique KB ID Policy
tags:
- content-type/policy-document
- criticality/p2-medium
- kb-id/standards
- status/draft
- topic/cs
- topic/policy
kb-id: standards
info-type: policy-document
primary-topic: Knowledge Base Identification
related-standards:
- AS-STRUCTURE-MASTER-KB-INDEX
- GM-CONVENTIONS-NAMING
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: CS
sub_domain: POLICY
scope_application: Ensures unique identification and clear naming for all Knowledge
  Bases (KBs) within the repository.
criticality: P2-Medium
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
- KB discoverability
- Repository organization
- Link integrity
- Authoring clarity
---
# Policy: Unique Knowledge Base Identification and Naming (CS-POLICY-KB-IDENTIFICATION)

## 1. Policy Statement

This policy mandates unique identification for each Knowledge Base (KB) through its primary folder name and requires clear articulation of the KB's identity within its root file. These measures are essential for maintaining an organized, navigable, and unambiguous knowledge ecosystem.

## 2. Core Requirements

### Rule 2.1: Globally Unique KB Primary Folder Name (Derived from U-ARCH-002, Rule 2.2)
Each Knowledge Base (KB) primary folder name MUST be globally unique within the master KB directory.
*   **Example:** `research-methodology-kb`, `prompt-engineering-kb`
*   **Notes:**
    *   This primary folder name acts as the de facto unique identifier for the KB at the file system level.
    *   Folder naming conventions (e.g., case, separators) MUST adhere to the global file and folder naming standard: [[GM-CONVENTIONS-NAMING]].
    *   Uniqueness prevents naming conflicts and ambiguity, ensuring that each KB can be distinctly referenced.

### Rule 2.2: Consistent KB Identity in `root.md` (Derived from U-ARCH-002, Rule 2.5)
The `root.md` file of each Knowledge Base MUST clearly state the full name and primary scope of that KB in its introductory content (typically the first paragraph or section after the H1 title). This stated identity MUST align with the KB's entry in the `kb-directory.md` file (as defined in [[AS-STRUCTURE-MASTER-KB-INDEX]]).
*   **Example (Text in `prompt-engineering-kb/root.md`):** "Welcome to the Prompt Engineering Knowledge Base. This KB covers principles, techniques, and frameworks for designing effective prompts for Large Language Models..."
*   **Notes:**
    *   This ensures that users entering a KB via its `root.md` immediately understand its identity and scope.
    *   Consistency with the `kb-directory.md` entry reinforces a single source of truth for KB descriptions.

## 3. Rationale and Importance

Adherence to this policy is critical for:

*   **Preventing Conflicts:** Unique KB folder names prevent technical issues and ambiguity in file paths and automated processes.
*   **Ensuring Clarity:** Consistent and clearly stated KB identity within `root.md` helps users confirm they are in the correct knowledge base and understand its purpose.
*   **Discoverability:** Unique and descriptive names, reflected in both the folder structure and `kb-directory.md`, improve the ability to locate specific KBs.
*   **Link Integrity:** While not directly governing link syntax, unique KB identifiers are foundational for reliable inter-KB linking strategies that might emerge.
*   **Maintainability and Governance:** A clear and unique identification scheme simplifies the management and governance of multiple KBs.

## 4. Scope of Application

This policy applies to all Knowledge Bases developed and maintained within the organization's master KB directory.

## 5. Cross-References
- [[AS-STRUCTURE-MASTER-KB-INDEX]] - Defines the structure of the master KB directory and the `kb-directory.md` index file.
- [[GM-CONVENTIONS-NAMING]] - File and Folder Naming Conventions (to be updated with actual ID).

---
*This policy (CS-POLICY-KB-IDENTIFICATION) is based on rules 2.2 and 2.5 previously defined in U-ARCH-002 from COL-ARCH-UNIVERSAL.md.*
