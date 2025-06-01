---
title: Standards Categorization Scheme Design Document
standard_id: project-design-standards-categorization-scheme
tags: [status/informational-reference, info-type/project-design-document, topic/project-architecture]
kb-id: project-governance
info-type: project-design-document
primary-topic: Design framework for categorizing and organizing standards within the knowledge base system.
related-standards: ['project-design-multi-view-architecture']
version: '1.0.0'
date-created: '2025-05-29T00:00:00Z'
date-modified: '2025-05-31T09:33:00Z'
primary_domain: PROJECT
sub_domain: DESIGN
scope_application: Overall structural design for the standards system.
criticality: p1-high
lifecycle_gatekeeper: N/A
impact_areas: [system-architecture, content-organization]
change_log_url: N/A
---

## Universal Standards Categorization Scheme: Final Framework

This document outlines the definitive, multi-dimensional categorization scheme for organizing and managing any collection of standards. The framework is designed to ensure clarity, discoverability, maintainability, and robust governance, supporting both human understanding and automated processing.

### Core Principle

The scheme is built upon a **single primary organizational axis**—the "Domains of Concern"—which dictates the main grouping of standards into logical collections. Complementing this, **secondary classificational axes**, such as "Scope of Application" and other essential metadata fields, are applied as facets to each standard. This structure facilitates a clear primary "home" for each standard while enabling rich, multi-dimensional querying and analysis without creating an overly complex physical hierarchy.

---

### 1. Primary Categorization: Domains of Concern

Each standard is categorized under one primary "Domain of Concern." These domains represent distinct functional or conceptual areas within a standards ecosystem. The defined domains are:

1.  **Architecture & Structure (AS)**
    *   **Definition:** Governs the macro and micro-level organization of information systems, knowledge bases, documents, and navigational pathways. Includes file/folder structures, system component relationships, and overall structural integrity.
2.  **Content & Semantics (CS)**
    *   **Definition:** Pertains to the substance, meaning, type, and creation guidelines for informational content. Includes content schemas, templates, writing style, content policies (inclusion/exclusion), and citation practices.
3.  **Metadata & Tagging (MT)**
    *   **Definition:** Focuses on descriptive data about content and system elements. Includes frontmatter definitions, tagging strategies, controlled vocabularies for metadata fields, and content profiling attributes.
4.  **Syntax & Formatting (SF)**
    *   **Definition:** Defines the rules for notation, markup languages, visual presentation, and file-level formatting. Includes specific syntax for Markdown, code, diagrams, and general file hygiene.
5.  **Operational Management (OM)**
    *   **Definition:** Addresses the processes, tools, and automation involved in the lifecycle management, validation, and deployment of content *according to standards*. Includes build pipelines, publishing workflows, validation scripts, tool-specific conventions, and LLM integration workflows.
6.  **Governance & Meta-Standards (GM)**
    *   **Definition:** Concerns the creation, maintenance, evolution, and oversight of the *standards system itself*. Includes policies and processes for proposing, reviewing, writing, versioning, and deprecating standards, as well as support documentation (onboarding, glossaries) for the standards framework.
7.  **Utility & Assets (UA)**
    *   **Definition:** Covers supporting elements and general utilities that enhance the knowledge system or its content. Includes management of non-document assets (images, files) and accessibility guidelines.
8.  **Quality & Metrics (QM)**
    *   **Definition:** Focuses on defining, measuring, and ensuring the quality and effectiveness of content and adherence to standards. Includes linting rules, compliance checks, performance indicators, and testing criteria.

---

### 2. Secondary Categorization: Scope of Application (Facet)

Each standard is further characterized by its "Scope of Application," indicating the level at which it primarily exerts its influence. This is applied as a metadata facet.

1.  **System-Level:** Applies to the entire knowledge management system or multiple knowledge bases.
2.  **KnowledgeBase-Level (KB-Level):** Applies to an entire individual knowledge base.
3.  **Document-Level:** Applies to individual content documents or notes.
4.  **Element-Level:** Applies to specific parts or elements within a document (e.g., a heading, a link).

---

### 3. Essential Standard Metadata

Every individual standard MUST possess the following metadata fields, populated accurately:

1.  **Standard ID:** A unique identifier (e.g., `AS-STRUCTURE-KB-ROOT.md`). The Standard ID is keyword-based, not sequential, and is typically constructed from domain, sub-domain, and descriptive keywords.
2.  **Standard Name:** A concise, descriptive name.
3.  **Primary Domain:** The main domain (from Section 1) under which the standard is categorized (e.g., `AS`, `CS`).
4.  **Sub-Domain:** A more granular, controlled classification within the Primary Domain (see Section 4).
5.  **Scope of Application:** The relevant scope (from Section 2) (e.g., `System-Level`, `Document-Level`).
6.  **Version:** The semantic version number of the standard (e.g., `'1.0.0'`).
7.  **Status:** The current lifecycle status (e.g., `Draft`, `Active`, `Deprecated`).
8.  **Date Created:** The date the standard was initially created (`YYYY-MM-DD`).
9.  **Date Modified:** The date the standard was last significantly modified (`YYYY-MM-DD`).
10. **Description/Purpose:** A clear statement of what the standard aims to achieve and its rationale.
11. **Rules/Guidelines:** For "Standard" documents, this section contains the HOW/WHERE (i.e., the specific, actionable rules and the context or location of their application). For "Policy" documents, this section contains the WHAT/WHEN/WHY (i.e., the intent, timing, and rationale for the policy). This distinction is crucial for clarity and governance.
12. **Cross-References:** A list of IDs of other directly related standards.
13. **Additional Facets/Tags:** A list of other relevant keywords or classification tags for enhanced findability, not covered by structured fields.
14. **Criticality:** The enforcement priority of the standard (e.g., `P0` - Critical/Must, `P1` - High/Should, `P2` - Medium/May).
15. **Lifecycle_Gatekeeper:** The defined role, team, or process responsible for approving status transitions for the standard (e.g., "Architect Review", "SME Consensus", "Automated Validation Suite").
16. **Impact_Areas:** A list of other Primary Domains potentially affected by changes to this standard.
17. **Change_Log_URL:** A direct link to the standard's version history, diffs, or relevant discussion threads (e.g., PR link).
18. **Document Type:** The explicit type of rule document (e.g., `standard-definition`, `policy-document`, `guideline-document`). This field captures the nature of the document and enforces the strict separation of "Standards" from "Policies/Guidelines."

---

### 4. Sub-Domain Governance

To ensure consistency and utility for the "Sub-Domain" metadata field:

*   A controlled vocabulary for sub-domains within each Primary Domain MUST be established and maintained (e.g., in a central `subdomain_registry.yaml` or similar manifest).
*   The sub-domain structure SHOULD typically be limited (e.g., a maximum of one or two levels deep from the Primary Domain) to prevent over-complexity.

---

### 5. Supporting Mechanisms for Operationalization

To make this categorization scheme fully operational and to support automation, the following is essential:

*   **Central Standards Index:** A machine-readable manifest (e.g., `standards_index.json`) SHOULD be generated or maintained. This index acts as a single source of truth, listing all standards and their core metadata. It enables:
    *   Automated validation of metadata completeness and correctness.
    *   Generation of dynamic Tables of Contents, dashboards, and reports.
    *   Dependency analysis and impact assessment for changes.
    *   Automated checks in CI/CD pipelines (e.g., blocking merges if mandatory metadata is missing).

---

### 6. Governance and Evolution of the Scheme

This Universal Standards Categorization Scheme itself is subject to governance. The defined domains, scope levels, and metadata fields can be refined or extended based on the evolving needs of the standards ecosystem. Any changes to this scheme MUST follow a formal review and approval process.

### Conclusion

This final framework provides a comprehensive, robust, and adaptable system for categorizing and managing standards. It balances structural clarity with the flexibility needed for diverse knowledge environments, ensuring that standards are not only well-organized but also actively support both human contributors and automated systems.

---
