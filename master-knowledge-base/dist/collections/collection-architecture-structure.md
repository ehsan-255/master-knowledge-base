---
title: "Architecture & Structure Standards"
description: "A collection of key standards related to overall knowledge base architecture, information structure, and schema definitions from the AS (Architecture & Structure) domain."
date_generated: "2025-06-04T22:19:33.618643+00:00"
source_collection_definition_id: "coll_as_arch_structure"
number_of_standards: 15
tags: ["content-type/collection-document", "status/published", "topic/derived-view"] 
info-type: "collection-document" 
# Consider adding a standard_id for the collection itself, e.g.:
# standard_id: "COLL-COLL-AS-ARCH-STRUCTURE" 
---

## Table of Contents
- [Master Knowledge Base Index (`AS-INDEX-KB-MASTER`)](#master-knowledge-base-index-as-index-kb-master)
- [Knowledge Base Directory Structure Standard (`AS-KB-DIRECTORY-STRUCTURE`)](#knowledge-base-directory-structure-standard-as-kb-directory-structure)
- [Standards Knowledge Base Definition Map (`AS-MAP-STANDARDS-KB`)](#standards-knowledge-base-definition-map-as-map-standards-kb)
- [Standards Knowledge Base Root (`AS-ROOT-STANDARDS-KB`)](#standards-knowledge-base-root-as-root-standards-kb)
- [Standard: Content Schema for Concept Definitions (`AS-SCHEMA-CONCEPT-DEFINITION`)](#standard-content-schema-for-concept-definitions-as-schema-concept-definition)
- [Standard: Content Schema for Methodology/Technique Descriptions (`AS-SCHEMA-METHODOLOGY-DESCRIPTION`)](#standard-content-schema-for-methodologytechnique-descriptions-as-schema-methodology-description)
- [Standard: Reference Document Schema (`AS-SCHEMA-REFERENCE`)](#standard-reference-document-schema-as-schema-reference)
- [Standard: Relationship Table (Reltable) Definition (`AS-SCHEMA-RELTABLE-DEFINITION`)](#standard-relationship-table-reltable-definition-as-schema-reltable-definition)
- [Standard: Task Document Schema (`AS-SCHEMA-TASK`)](#standard-task-document-schema-as-schema-task)
- [Standard: Asset Organization and Naming (`AS-STRUCTURE-ASSET-ORGANIZATION`)](#standard-asset-organization-and-naming-as-structure-asset-organization)
- [Standard: Content Document (Chapter) Internal Structure (`AS-STRUCTURE-DOC-CHAPTER`)](#standard-content-document-chapter-internal-structure-as-structure-doc-chapter)
- [Standard: Knowledge Base Part Structure and Overview (`AS-STRUCTURE-KB-PART`)](#standard-knowledge-base-part-structure-and-overview-as-structure-kb-part)
- [Standard: Knowledge Base Root Structure (`AS-STRUCTURE-KB-ROOT`)](#standard-knowledge-base-root-structure-as-structure-kb-root)
- [Standard: Master Knowledge Base Directory and Index Structure (`AS-STRUCTURE-MASTER-KB-INDEX`)](#standard-master-knowledge-base-directory-and-index-structure-as-structure-master-kb-index)
- [Standard: Templates Directory Structure and Usage (`AS-STRUCTURE-TEMPLATES-DIRECTORY`)](#standard-templates-directory-structure-and-usage-as-structure-templates-directory)


## Master Knowledge Base Index (AS-INDEX-KB-MASTER)

# Master Knowledge Base Index

This document provides a centralized directory to all active Knowledge Bases (KBs) within this ecosystem. For the standard defining how this index file should be structured, see `[[AS-STRUCTURE-MASTER-KB-INDEX]]`.

## Available Knowledge Bases

Below is a list of currently available Knowledge Bases. Each KB is a self-contained unit focused on a specific domain or purpose.

1.  **Standards Knowledge Base**
    *   **Description:** Contains all standards, policies, guidelines, and supporting documentation for creating, managing, and governing content within the entire knowledge ecosystem. This is the meta-KB that defines how other KBs operate.
    *   **Entry Point:** `[Standards Knowledge Base Root](#standards-knowledge-base-root-as-root-standards-kb)`
    *   **Primary Folder:** `/master-knowledge-base/standards/`

2.  **LLM Content Generation Cookbook KB**
    *   **Description:** Provides practical recipes, prompt templates, and best practices for using Large Language Models (LLMs) to assist with content creation, analysis, and other knowledge work.
    *   **Entry Point:** `[[TODO-LLM-COOKBOOK-ROOT-ID]]` (Link to the root file of the LLM Cookbook KB once its ID is known or it's created)
    *   **Primary Folder:** `/master-knowledge-base/llm-content-generation-cookbook/` (Assumed path)

3.  **Research Methodology KB**
    *   **Description:** Focuses on research design, data collection, analysis, and open science practices for generating complex workflows.
    *   **Entry Point:** `[[TODO-RESEARCH-METHODOLOGY-ROOT-ID]]` (Link to the root file of the Research Methodology KB once its ID is known or it's created)
    *   **Primary Folder:** `/master-knowledge-base/research-methodology-kb/` (Assumed path)

> [!TODO] This index needs to be kept up-to-date as new Knowledge Bases are added or existing ones are retired. Links to the entry points (`root.md` or equivalent `AS-ROOT-*-KB.md` files) of each KB must be accurate. Placeholder links like `[[TODO-LLM-COOKBOOK-ROOT-ID]]` need to be resolved.

---
This master index is crucial for navigating the multi-KB environment.

---

## Knowledge Base Directory Structure Standard (AS-KB-DIRECTORY-STRUCTURE)

# AS-KB-DIRECTORY-STRUCTURE: Knowledge Base Directory Structure Standard

## 1. Overview

This standard defines the official directory structure for the master knowledge base. A consistent directory structure is crucial for organization, navigability, and automation.

## 2. Top-Level Organization

The primary content and operational files for the knowledge base are organized under a root directory named `master-knowledge-base/`.

## 3. Core Directories for Standards Development

Within `master-knowledge-base/standards/`, the following specialized directories are used:

*   **`/master-knowledge-base/standards/src/` (Task 0.4.1)**
    *   **Purpose:** This is the primary Layer 1 directory for all atomic standard documents (Standard Definitions, Policy Documents, Guide Documents, etc.).
    *   **Content:** Individual Markdown files (`.md`) representing single, atomic standards.
    *   **Naming:** Files in this directory MUST follow the [[GM-CONVENTIONS-NAMING#Atomic File Naming Convention|File Naming Convention]] (Note: Link to be updated once actual naming convention doc ID is set).

*   **`/master-knowledge-base/standards/registry/` (Task 0.4.2)**
    *   **Purpose:** This directory houses all controlled vocabulary manifests and registry definition files.
    *   **Content:** YAML files (`.yaml`) or Markdown files (`.md`) that define terms, codes, and their meanings for various metadata fields (e.g., domain codes, status tags, criticality levels).
    *   **Examples:** `domain_codes.yaml`, `tag-glossary-definition.md`.

*   **`/master-knowledge-base/standards/templates/` (Task 0.4.3)**
    *   **Purpose:** This directory contains standard templates for creating new documents.
    *   **Content:** Markdown files (`.md`) serving as boilerplate structures.
    *   **Naming:** Template filenames MUST be prefixed with `tpl-` (e.g., `tpl-canonical-frontmatter.md`, `tpl-standard-definition.md`).

## 4. Tooling and Automation Directory

*   **`/master-knowledge-base/tools/`**
    *   **Purpose:** This directory contains scripts and tooling used for validation, indexing, building, or other automation tasks related to the knowledge base.
    *   **Sub-directories:** May include `linter/`, `indexer/`, `builder/`, `validators/` for organization.
    *   **Examples:** `linter/kb_linter.py`, `indexer/generate_index.py`.

## 5. Other Key Directories (Illustrative - To Be Expanded)

*   **`/master-knowledge-base/assets/`**
    *   **Purpose:** For storing static assets like images, diagrams, or other binary files referenced in documents.
*   **`/dist/` or `/build/` (outside `master-knowledge-base/`, typically gitignored)**
    *   **Purpose:** Output directory for generated views, compiled sites, or other build artifacts.

This document will be updated as the directory structure evolves.

---

## Standards Knowledge Base Definition Map (AS-MAP-STANDARDS-KB)

# Standards Knowledge Base Definition Map (AS-MAP-STANDARDS-KB)

## 1. Standard Statement

This document defines the logical structure, primary parts (categories), and overall organization of the Standards Knowledge Base (KB) itself. It serves as a high-level map to help users navigate and understand the layout and content of the standards documentation.

The Standards KB is the authoritative source for all standards, policies, and guidelines governing the creation, management, and use of all knowledge bases within the ecosystem.

> [!TODO] The content of this document, particularly the `parts` structure in the frontmatter and the detailed descriptions below, needs to be fully populated and aligned with the actual organization of standards within the `/master-knowledge-base/standards/src/` directory. The current content is a high-level placeholder based on primary domains.

## 2. Purpose

The purpose of this KB Definition Map is to:
-   Provide a clear and organized overview of the Standards KB.
-   Define the main logical sections ("Parts") of the Standards KB.
-   Facilitate navigation and discovery of relevant standards.
-   Serve as a reference for authors contributing to the Standards KB.

## 3. Structure of the Standards Knowledge Base

The Standards Knowledge Base is organized into logical "Parts," primarily aligned with the `primary_domain` codes used in `standard_id`s. Each part groups related standards.

*(The detailed structure, including links to overview documents for each part and key standards within each part, would be elaborated here. The frontmatter `kb_definition` field provides a conceptual outline of this structure.)*

### Example Part Outline (derived from frontmatter `kb_definition`):

#### Part 1: Architecture and Structure (AS)
-   **Overview:** Standards defining the overall organization of knowledge bases, individual documents, and metadata structures.
-   **Key Documents:** (List or link to key `AS-*` standards, e.g., `[[AS-STRUCTURE-KB-ROOT]]`, `[[AS-STRUCTURE-DOC-CHAPTER]]`, `[[MT-SCHEMA-FRONTMATTER]]` (as it defines a core structure), etc.)

#### Part 2: Content Style and Policies (CS)
-   **Overview:** Standards and policies related to content authoring, tone, language, presentation, and accessibility.
-   **Key Documents:** (List or link to key `CS-*` standards)

#### Part 3: General Management and Meta (GM)
-   **Overview:** Guidance documents, glossaries, and policies for overall KB management, user onboarding, and understanding the standards ecosystem.
-   **Key Documents:** (List or link to key `GM-*` standards, e.g., `[[GM-GUIDE-KB-USAGE]]`, `[[GM-GLOSSARY-STANDARDS-TERMS]]`)

#### Part 4: Metadata, Tagging, and Registries (MT)
-   **Overview:** Standards for document metadata (frontmatter), tagging strategies, keyref systems, and the governance of controlled vocabularies (registries).
-   **Key Documents:** (List or link to key `MT-*` standards, e.g., `[[MT-SCHEMA-FRONTMATTER]]`, `[[MT-TAGGING-STRATEGY-POLICY]]`, `[[MT-REGISTRY-TAG-GLOSSARY]]`)

#### Part 5: Operational Management and Lifecycles (OM)
-   **Overview:** Policies and procedures for the operational aspects of standards and content, including governance, versioning, deprecation, and publishing pipelines.
-   **Key Documents:** (List or link to key `OM-*` standards, e.g., `[[OM-POLICY-STANDARDS-GOVERNANCE]]`, `[[OM-OVERVIEW-PUBLISHING-PIPELINE]]`)

#### Part 6: Quality, Metrics, and Validation (QM)
-   **Overview:** Standards and procedures related to ensuring content quality, defining metrics, and validating metadata and content against defined rules.
-   **Key Documents:** (List or link to key `QM-*` standards, e.g., `[[QM-VALIDATION-METADATA]]`)

#### Part 7: Syntax, Formatting, and Conventions (SF)
-   **Overview:** Specific rules for Markdown syntax, file formatting, naming conventions, and other presentational aspects of content.
-   **Key Documents:** (List or link to key `SF-*` standards, e.g., `[[SF-FORMATTING-MARKDOWN-GENERAL]]`, `[[GM-CONVENTIONS-NAMING]]`)

#### Part 8: Utility, Assets, and Automation (UA)
-   **Overview:** Standards for supporting utilities (like keyrefs), management of assets (like images), and schemas for automation processes (like LLM I/O).
-   **Key Documents:** (List or link to key `UA-*` standards, e.g., `[[UA-KEYDEFS-GLOBAL]]`, `[[UA-SCHEMA-LLM-IO]]`)

## 4. Navigation
-   The primary entry point for the Standards KB is typically its `root.md` file.
-   The master directory of all KBs is `[[AS-STRUCTURE-MASTER-KB-INDEX]]`.

This map helps provide a structured view into the comprehensive set of standards governing the knowledge ecosystem.

---

## Standards Knowledge Base Root (AS-ROOT-STANDARDS-KB)

# Standards Knowledge Base Root (AS-ROOT-STANDARDS-KB)

Welcome to the Standards Knowledge Base (KB). This document serves as the main entry point and master table of contents for all standards, policies, guidelines, and supporting documentation related to the knowledge management ecosystem.

The purpose of this KB is to ensure consistency, quality, and interoperability across all managed knowledge domains. For a conceptual map of how this KB is organized, please refer to `[Standards Knowledge Base Definition Map](#standards-knowledge-base-definition-map-as-map-standards-kb)`.

## Master Table of Contents

The following sections categorize and link to the core documents that define our knowledge management standards.

### 1. Foundational Concepts
    - [[CONCEPT-HYPOTHESIS-TESTING|Concept: Hypothesis Testing]]
    - [[CONCEPT-P-VALUE|Concept: P-Value]]
    - [[CONCEPT-CORE-RESEARCH-METHODOLOGY|Concept: Core Research Methodology]]

### 2. Architecture and Structure (AS Domain)
    - [Knowledge Base Directory Structure Standard](#knowledge-base-directory-structure-standard-as-kb-directory-structure)
    - [Standard: Content Schema for Concept Definitions](#standard-content-schema-for-concept-definitions-as-schema-concept-definition)
    - [Standard: Content Schema for Methodology/Technique Descriptions](#standard-content-schema-for-methodologytechnique-descriptions-as-schema-methodology-description)
    - [Standard: Relationship Table (Reltable) Definition](#standard-relationship-table-reltable-definition-as-schema-reltable-definition)
    - [[AS-STRUCTURE-ASSET-ORGANIZATION|Standard: Asset Organization and Naming]]
    - [[AS-STRUCTURE-DOC-CHAPTER|Standard: Content Document (Chapter) Internal Structure]]
    - [[AS-STRUCTURE-KB-PART|Standard: Knowledge Base Part Structure and Overview]]
    - [[AS-STRUCTURE-KB-ROOT|Standard: Knowledge Base Root Structure]]
    - [[AS-STRUCTURE-MASTER-KB-INDEX|Standard: Master Knowledge Base Directory and Index Structure]]
    - [[AS-STRUCTURE-TEMPLATES-DIRECTORY|Standard: Templates Directory Structure and Usage]]

### 3. Content, Style, and Policy (CS Domain)
    - [[CS-ADMONITIONS-POLICY|Policy: Usage of Admonitions and Callouts]]
    - [[CS-CONTENT-PROFILING-POLICY|Policy: Content Profiling and Conditional Text]]
    - [[CS-LINKING-INTERNAL-POLICY|Policy: Internal Knowledge Base Linking Strategy]]
    - [[CS-MODULARITY-TRANSCLUSION-POLICY|Policy: Content Modularity and Use of Transclusion]]
    - [[CS-POLICY-ACCESSIBILITY|Policy: Content Accessibility]]
    - [[CS-POLICY-DIGITAL-ABSTRACTION|Policy: Translating Non-Digital Concepts for Digital Workflows]]
    - [[CS-POLICY-DOC-CHAPTER-CONTENT|Policy: Content Organization and Heading Usage in Chapters]]
    - [[CS-POLICY-KB-IDENTIFICATION|Policy: Unique Knowledge Base Identification and Naming]]
    - [[CS-POLICY-KB-PART-CONTENT|Policy: Content Organization within Knowledge Base Parts]]
    - [[CS-POLICY-KB-ROOT|Policy: Consistent Application of Knowledge Base Root Structure]]
    - [[CS-POLICY-LAYERED-INFORMATION|Policy: Layered Information Presentation and Progressive Disclosure]]

### 4. Metadata, Tagging, and Registries (MT Domain)
    - [[MT-SCHEMA-FRONTMATTER|Standard: Frontmatter Schema Definition]]

### 5. Syntax, Formatting, and Conventions (SF Domain)
    - [[SF-CALLOUTS-SYNTAX|Standard: Callout and Admonition Syntax]]
    - [[SF-LINKS-INTERNAL-SYNTAX|Internal Linking Syntax Standard]]

### 6. Operational Management and Lifecycles (OM Domain)
    - (No standards currently listed for this domain from the processed set)

### 7. Quality, Metrics, and Validation (QM Domain)
    - (No standards currently listed for this domain from the processed set)

### 8. Utility, Assets, and Automation (UA Domain)
    - [[GUIDE-FEATURE-ADVANCED-SETTINGS|Guide: Feature Advanced Settings]]

---
This root document helps navigate the comprehensive set of standards that govern our knowledge ecosystem.
For navigating all KBs, see `[Master Knowledge Base Index](#master-knowledge-base-index-as-index-kb-master)` (once created/confirmed).

---

## Standard: Content Schema for Concept Definitions (AS-SCHEMA-CONCEPT-DEFINITION)

# Standard: Content Schema for Concept Definitions (AS-SCHEMA-CONCEPT-DEFINITION)

This standard defines the mandatory content structure (schema) for documents whose primary purpose is to define a core concept or term. Adherence to this schema ensures that concepts are explained clearly, consistently, and comprehensively.

## 1. Scope and Applicability (Derived from U-SCHEMA-CONCEPT-001, Rule 1.1)

This schema MUST be applied to all documents that primarily define a core concept or term.
*   **Example Application:** A document defining `statistical-significance.md` or `machine-learning-bias.md`.

## 2. Mandatory Document Structure

Documents following this schema MUST adhere to the general internal structure for "Chapters" as defined in [[AS-STRUCTURE-DOC-CHAPTER]]. This includes:

### Rule 2.1: H1 Title (Derived from U-SCHEMA-CONCEPT-001, Rule 1.2)
The H1 title of the document MUST be the specific name of the concept or term being defined.
*   **Example:** `# Statistical Significance`

### Rule 2.2: Introductory Abstract (Derived from U-SCHEMA-CONCEPT-001, Rule 1.3)
An introductory abstract that summarizes the concept's meaning and significance MUST be included immediately after the H1 title.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for details on abstract content.

### Rule 2.3: Table of Contents (ToC) (Derived from U-SCHEMA-CONCEPT-001, Rule 1.4)
A Table of Contents (ToC) MUST follow the abstract, linking to all H2 sections and significant H3 sections.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for ToC requirements.

## 3. Required Sections (H2 Level) (Derived from U-SCHEMA-CONCEPT-001, Rule 1.5)

The following H2 sections MUST be included in the document, at a minimum, and should appear in a logical order similar to that presented below:

1.  **`## Definition`** (Derived from U-SCHEMA-CONCEPT-001, Rule 1.6)
    *   This section MUST provide a clear, concise, and unambiguous definition of the concept or term.
    *   It should be easily understandable and serve as the primary explanation.
2.  **`## Key Characteristics / Principles`**
    *   Describe the essential features, attributes, properties, or underlying principles that define or govern the concept.
3.  **`## Importance / Relevance`**
    *   Explain why the concept is important, its significance in relevant domains, or its practical relevance.
4.  **`## Common Misconceptions`** (If Applicable)
    *   Address any common misunderstandings, myths, or incorrect interpretations related to the concept. This section is optional if no common misconceptions are known.
5.  **`## Practical Examples / Applications`** (Derived from U-SCHEMA-CONCEPT-001, Rule 1.7)
    *   This section MUST illustrate the concept in use through practical examples, applications, or case studies.
    *   Examples should be clear and help solidify understanding.

*   **Note:** Other H2 sections can be added as needed to fully explain the concept.

## 4. Illustrative Example (Partial H2 Outline)

For a document named `statistical-significance.md`:
```markdown
# Statistical Significance
(Abstract: This document defines statistical significance, explaining its role in hypothesis testing...)
(Table of Contents: ...)

## Definition
Statistical significance refers to the likelihood that an observed result or relationship in a dataset is not due to random chance...

## Key Characteristics / Principles
- Based on hypothesis testing (null and alternative hypotheses).
- Involves calculating a p-value.
- Threshold for significance (alpha level, e.g., 0.05).
- Does not imply practical significance or importance of the effect.

## Importance / Relevance
- Crucial for drawing valid conclusions from research data.
- Widely used in scientific research, A/B testing, quality control, etc.
- Helps in making data-driven decisions.

## Common Misconceptions
- That statistical significance implies a large or important effect.
- That a non-significant result proves the null hypothesis is true.

## Practical Examples / Applications
### Example 1: A/B Testing
A website tests two versions of a button (A and B). Version B gets a 5% higher click-through rate. Statistical significance testing determines if this 5% difference is likely real or due to chance...

### Example 2: Medical Trials
A new drug is tested against a placebo. Statistical significance helps determine if the observed improvement in patients taking the drug is a real effect of the drug...

## Summary
(Summary of statistical significance...)

## See Also
- [[CONCEPT-HYPOTHESIS-TESTING]]
- [[CONCEPT-P-VALUE]]
```

## 5. Cross-References
- [[AS-STRUCTURE-DOC-CHAPTER]] - For general chapter structure requirements (H1, abstract, ToC, summary, see also).

---
*This standard (AS-SCHEMA-CONCEPT-DEFINITION) is based on rules 1.1 through 1.7 previously defined in U-SCHEMA-CONCEPT-001 from COL-CONTENT-UNIVERSAL.md.*

---

## Standard: Content Schema for Methodology/Technique Descriptions (AS-SCHEMA-METHODOLOGY-DESCRIPTION)

# Standard: Content Schema for Methodology/Technique Descriptions (AS-SCHEMA-METHODOLOGY-DESCRIPTION)

This standard defines the mandatory content structure (schema) for documents whose primary purpose is to describe a specific methodology, technique, or detailed process. Adherence to this schema ensures consistency, clarity, and comprehensive coverage of essential aspects.

## 1. Scope and Applicability (Derived from U-SCHEMA-METHOD-001, Rule 1.1)

This schema MUST be applied to all documents that describe a specific methodology, technique, or detailed process. This typically includes "how-to" type content that outlines a systematic approach to achieving a particular outcome.

*   **Example Application:** A document detailing the steps for `systematic-literature-review.md` or `troubleshooting-network-latency.md`.

## 2. Mandatory Document Structure

Documents following this schema MUST adhere to the general internal structure for "Chapters" as defined in [[AS-STRUCTURE-DOC-CHAPTER]]. This includes:

### Rule 2.1: H1 Title (Derived from U-SCHEMA-METHOD-001, Rule 1.2)
The H1 title of the document MUST be the specific name of the methodology or technique being described.
*   **Example:** `# Systematic Literature Review`

### Rule 2.2: Introductory Abstract (Derived from U-SCHEMA-METHOD-001, Rule 1.3)
An introductory abstract that summarizes the method, its purpose, and key outcomes MUST be included immediately after the H1 title.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for details on abstract content.

### Rule 2.3: Table of Contents (ToC) (Derived from U-SCHEMA-METHOD-001, Rule 1.4)
A Table of Contents (ToC) MUST follow the abstract, linking to all H2 sections and significant H3 sections.
*   **Reference:** See [[AS-STRUCTURE-DOC-CHAPTER]] for ToC requirements.

## 3. Required Sections (H2 Level) (Derived from U-SCHEMA-METHOD-001, Rule 1.5)

The following H2 sections MUST be included in the document, at a minimum, and should appear in a logical order similar to that presented below:

1.  **`## Purpose`**
    *   Clearly state the primary goal or objective of the methodology/technique. What problem does it solve or what outcome does it achieve?
2.  **`## Core Principles`**
    *   Outline the fundamental concepts, assumptions, or guiding philosophies that underpin the methodology/technique.
3.  **`## When to Use / Not Use`** (Applicability)
    *   Describe the specific contexts, situations, or conditions under which this methodology/technique is most effective or appropriate.
    *   Conversely, describe situations where it might be unsuitable or less effective than alternatives.
4.  **`## Key Steps`** (or **`## Process`**)
    *   This is a critical section detailing the actual execution of the methodology/technique. See "Detailed Requirements for 'Key Steps' / 'Process' Section" below.
5.  **`## Advantages`**
    *   List the primary benefits, strengths, or positive outcomes of using this methodology/technique.
6.  **`## Limitations`**
    *   Describe any known drawbacks, constraints, potential challenges, or areas where the methodology/technique might fall short.
7.  **`## Variations/Alternatives`** (Optional but Recommended)
    *   Discuss common variations of the methodology/technique or briefly mention well-known alternatives if applicable.

## 4. Detailed Requirements for "Key Steps" / "Process" Section

### Rule 4.1: Actionable and Sequenced Steps (Derived from U-SCHEMA-METHOD-001, Rule 1.6)
The "Key Steps" (or "Process") section MUST detail actionable steps in a clear, logical sequence.
*   **Guidance:** Use numbered lists or clearly demarcated H3 headings for each step to ensure sequence is apparent. Steps should be described with enough detail to be understandable and executable by the target audience.

### Rule 4.2: Inputs and Outputs per Step (Derived from U-SCHEMA-METHOD-001, Rule 1.7)
For each "Key Step" described, where applicable, clearly specify:
    a.  **Inputs:** What information, resources, or pre-conditions are required *before* this step can be performed?
    b.  **Outputs/Deliverables:** What tangible results, documents, decisions, or states are produced *by* completing this step?
*   **Example (within an H3 for a step):**
    ```markdown
    ### Step 1: Define Research Question
    **Inputs:** Initial research problem, preliminary literature scan.
    **Outputs:** Focused, answerable research question (e.g., using PICO framework).

    (Detailed actions for defining the research question...)
    ```
*   **Rationale:** Specifying inputs and outputs aids in understanding the flow of the process, supports decomposability for workflow automation, and clarifies dependencies between steps.

## 5. Illustrative Example (Partial H2 Outline)

For a document named `systematic-literature-review.md`:
```markdown
# Systematic Literature Review
(Abstract: This document outlines the process for conducting a systematic literature review...)
(Table of Contents: ...)

## Purpose
To identify, appraise, and synthesize all relevant studies on a particular topic to answer a predefined research question.

## Core Principles
- Transparency in methodology
- Reproducibility of search and selection
- Rigorous critical appraisal of evidence
- Comprehensive and unbiased synthesis

## When to Use / Not Use
**Use when:**
- Answering specific, focused research questions.
- Summarizing the current state of evidence on a mature topic.
- Identifying gaps in current research.
**Not Use when:**
- Broad exploratory research is needed.
- The topic is very new with little existing literature.
- A quick overview is sufficient (consider a scoping review instead).

## Key Steps
### Step 1: Formulate the Research Question (e.g., PICO)
**Inputs:** Initial research problem description, understanding of target domain.
**Outputs:** A clear, focused, and answerable research question.
(Detailed actions on how to formulate the question...)

### Step 2: Develop and Register the Review Protocol
**Inputs:** Formulated research question.
**Outputs:** A documented review protocol outlining the search strategy, inclusion/exclusion criteria, data extraction plan, and analysis methods.
(Detailed actions...)

### Step 3: Execute Search Strategy
(Details...)

## Advantages
- Minimizes bias compared to traditional narrative reviews.
- Provides a comprehensive summary of available evidence.
- Can form the basis for evidence-based guidelines.

## Limitations
- Can be very time-consuming and resource-intensive.
- Quality depends heavily on the quality of included studies.
- May not be suitable for all research questions or types of evidence.

## Variations/Alternatives
- Scoping Reviews
- Rapid Reviews
- Meta-analyses (often a component of systematic reviews)

## Summary
(Summary of the systematic literature review process...)

## See Also
- [[CS-POLICY-LAYERED-INFORMATION]]
- [[AS-STRUCTURE-DOC-CHAPTER]]
```

## 6. Cross-References
- [[AS-STRUCTURE-DOC-CHAPTER]] - For general chapter structure requirements (H1, abstract, ToC, summary, see also).
- [[CS-POLICY-LAYERED-INFORMATION]] - For principles of presenting information from general to specific.

---
*This standard (AS-SCHEMA-METHODOLOGY-DESCRIPTION) is based on rules 1.1 through 1.7 previously defined in U-SCHEMA-METHOD-001 from COL-CONTENT-UNIVERSAL.md.*

---

## Standard: Reference Document Schema (AS-SCHEMA-REFERENCE)

# Standard: Reference Document Schema (AS-SCHEMA-REFERENCE)

## 1. Standard Statement

This standard defines the mandatory and recommended structure for creating **Reference Documents**. Reference documents provide detailed, factual information about specific technical elements such as Application Programming Interface (API) endpoints, command-line interface (CLI) commands, programming language functions or classes, configuration parameters, or data structure definitions.

Adherence to this schema ensures that reference documentation is consistent, comprehensive, predictable, and easy for users (especially developers and technical staff) to navigate and understand. This schema builds upon the general document structure defined in `[[AS-STRUCTURE-DOC-CHAPTER]]`.

## 2. Purpose of Reference Documents

Reference documents are intended to be lookup resources. Users consult them to find:
-   The exact syntax or signature of an element.
-   The purpose and behavior of parameters or options.
-   Expected return values or outcomes.
-   Examples of correct usage.
-   Details of potential errors or exceptions.
-   Other relevant technical details.

They are distinct from tutorials (which teach how to do something step-by-step) or guides (which explain concepts or best practices).

## 3. Core Structure of a Reference Document

A reference document, after the standard frontmatter and H1 title (which should clearly name the element being referenced, e.g., "Command: `git commit`" or "Function: `calculate_average()`"), MUST generally follow this sequence of H2 sections. Some sections are optional depending on the nature of the element being documented.

### 3.1. Element Overview / Description (Mandatory)
   - **Heading:** `## Overview` or `## Description`
   - **Content:** A brief summary (1-3 sentences) explaining what the element is and its primary purpose. This may be similar to the abstract section mentioned in `[[AS-STRUCTURE-DOC-CHAPTER]]` but focused specifically on the element.

### 3.2. Syntax / Signature (Conditional - Mandatory if applicable)
   - **Heading:** `## Syntax` (for commands, code structures) or `## Signature` (for functions, methods, API endpoints)
   - **Content:** The formal definition of how to use or call the element.
     - For commands: Show the command and its parameters, using conventions for optional/required parts.
     - For functions/methods: Show the function signature, including parameter names, types, and return type.
     - For API endpoints: Show the HTTP method, URL pattern, and any path/query parameters.
   - **Example:**
     ```
     ## Syntax
     my_command [--option-a <value>] <required_argument>
     ```
     ```
     ## Signature
     function calculate_sum(a: number, b: number): number
     ```

### 3.3. Parameters / Arguments / Options (Conditional - Mandatory if applicable)
   - **Heading:** `## Parameters`, `## Arguments`, or `## Options` (choose the most appropriate for the element type)
   - **Content:** A detailed list or table describing each parameter, argument, or option. For each item, provide:
     - **Name:** The exact name of the parameter/argument.
     - **Data Type:** (If applicable, e.g., string, integer, boolean, list).
     - **Description:** Explanation of its purpose and effect.
     - **Required/Optional:** Whether it must be provided.
     - **Default Value:** (If applicable and one exists).
     - **Allowed Values/Range:** (If applicable, e.g., for enums or specific value sets).
   - **Format:** Use a definition list, bulleted list with nested details, or a table for clarity.

### 3.4. Return Values / Output (Conditional - Mandatory if applicable)
   - **Heading:** `## Return Values` (for functions/methods) or `## Output` (for commands)
   - **Content:** Description of what the function/method returns or what the command outputs upon successful execution.
     - Specify data types and structure if complex.
     - For commands, describe standard output, standard error, and exit codes if relevant.

### 3.5. Examples (Highly Recommended, Mandatory for many use cases)
   - **Heading:** `## Examples`
   - **Content:** One or more practical examples of how to use the element.
     - Examples should be concise, correct, and illustrative of common use cases.
     - Use code blocks with appropriate language identifiers.
     - Briefly explain what each example does and why it's relevant.

### 3.6. Error Handling / Exceptions (Conditional - Recommended if applicable)
   - **Heading:** `## Error Handling` or `## Exceptions`
   - **Content:** Description of common errors, exceptions, or non-zero exit codes.
     - Explain what might cause them and how to resolve them.
     - This section is crucial for user troubleshooting.

### 3.7. Attributes / Properties (Conditional - If the element has readable/settable properties)
   - **Heading:** `## Attributes` or `## Properties`
   - **Content:** Similar to Parameters, listing properties of an object or resource. For each:
     - Name, Data Type, Read/Write status, Description.

### 3.8. Configuration Details (Conditional - For elements that are configured)
   - **Heading:** `## Configuration`
   - **Content:** Details on how to configure the element, perhaps referencing configuration files or specific settings.

### 3.9. Usage Notes / Remarks (Optional)
   - **Heading:** `## Usage Notes` or `## Remarks`
   - **Content:** Additional important information, best practices, limitations, or edge cases that don't fit neatly into other sections.

### 3.10. Related Elements / See Also (Highly Recommended)
   - **Heading:** `## Related Elements` or `## See Also`
   - **Content:** Links to other relevant reference documents, guides, or standards.
     - Example: A command reference might link to related commands or a conceptual guide explaining its purpose.

## 4. General Guidelines
- **Clarity and Precision:** Use unambiguous language. Define terms where necessary.
- **Completeness:** Strive to cover all aspects a user would need to know to use the element effectively.
- **Atomicity:** Each reference document should ideally focus on a single element (e.g., one command, one function). Complex elements with sub-commands might have a main page linking to sub-pages.
- **Code Blocks:** Use Markdown code blocks with correct language identifiers for syntax, examples, and code snippets.
- **Consistency:** Maintain consistent terminology and formatting across all reference documents.

## 5. Scope of Application
This schema applies to all documents intended to provide detailed reference information for technical elements within the knowledge base ecosystem. It is particularly relevant for software documentation, API guides, and system administration manuals.

---

## Standard: Relationship Table (Reltable) Definition (AS-SCHEMA-RELTABLE-DEFINITION)

# Standard: Relationship Table (Reltable) Definition (AS-SCHEMA-RELTABLE-DEFINITION)

> [!TODO] This standard's content has been migrated from `U-RELTABLE-DEFINITION-001`. However, the overall concept of Reltables, their precise implementation details (especially the defined relationship types and their YAML structure), and their integration with other architectural and schema standards require further review and refinement. The relationship types listed are initial suggestions and need validation against broader use cases and semantic consistency.

This document defines the standard structure for "Relationship Tables" (reltables). Reltables are used to explicitly define typed, non-hierarchical relationships between topics within the knowledge base, enhancing semantic understanding and navigation.

## Table of Contents
- [[#Standard: Reltable Structure and Usage (AS-SCHEMA-RELTABLE-DEFINITION)]]
- [[#Defined Relationship Types (Initial Set)]]

## Standard: Reltable Structure and Usage (AS-SCHEMA-RELTABLE-DEFINITION)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `AS-SCHEMA-RELTABLE-DEFINITION`       |
| Standard Name   | Relationship Table Definition         |
| Standard Category | Interlinking & Semantics              |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Relationship tables MUST be defined within the YAML frontmatter of "map" files (e.g., `root.md`, `_overview.md` for a KB Part) or in dedicated `_reltable.md` files. They use a top-level key `reltable:`. | See Illustrative Example.                                    | Centralizes relationship definitions for a given scope.                      |
| 1.2    | The `reltable:` key MUST contain a list of relationship entries. Each entry is an object.                                                       | `reltable:
  - topic: ...
  - topic: ...`                  | Each object defines relationships *from* a specific source topic.            |
| 1.3    | Each relationship entry object MUST have a `topic:` key, whose value is the path (from `master-knowledge-base` root) to the source topic file (e.g., `master-knowledge-base/standards/src/AS-STRUCTURE-KB-ROOT.md`). | `topic: master-knowledge-base/standards/src/AS-STRUCTURE-KB-ROOT.md`                             | Identifies the "from" side of the relationships. Link should be to new ID format if possible, or remain path based for now. This example uses path. |
| 1.4    | Each entry MAY contain one or more relationship type keys (e.g., `prerequisites:`, `relatedConcepts:`, `supportingTasks:`). These keys are defined in this standard (see "Defined Relationship Types"). | `prerequisites:
  - link: ...`                              | Defines the nature of the link.                                              |
| 1.5    | Each relationship type key (e.g., `prerequisites:`) MUST contain a list of target topic objects.                                                | `relatedConcepts:
  - link: master-knowledge-base/concepts/conceptA.md
    displayText: "Concept A Overview"` | Allows multiple targets for a given relationship type.                       |
| 1.6    | Each target topic object MUST have a `link:` key, whose value is the path (from `master-knowledge-base` root) to the target topic file. It MAY have an optional `displayText:` key for custom link text. | `link: master-knowledge-base/tasks/taskB.md
displayText: "How to Perform Task B"` | Links SHOULD eventually resolve to standard `[[TARGET_ID]]` syntax if the target is a standard. For other content, path-based links may be necessary. This example uses path. |
| 1.7    | Relationship types SHOULD be directional (e.g., "A is prerequisite for B" implies B has A as a prerequisite). Processing tools (e.g., DataviewJS) can infer reciprocal links. | N/A                                                          | Simplifies definition; tools handle bidirectionality if needed.              |

## Defined Relationship Types (Initial Set)

| Relationship Type         | Definition                                                                 | Directionality         | Example YAML Structure (within a `reltable` entry)                                                                 |
|--------------------------|----------------------------------------------------------------------------|-----------------------|--------------------------------------------------------------------------------------------------------------------|
| `isPrerequisiteFor`      | Indicates that the source is a required prerequisite for the target.        | Source → Target        | topic: path/to/source-topic.md
  isPrerequisiteFor:
    - link: path/to/target-topic.md |
| `isConceptualBasisFor`   | Indicates that the source provides the conceptual foundation for the target.| Source → Target        | topic: path/to/source-concept.md
  isConceptualBasisFor:
    - link: path/to/target-methodology.md |
| `isExampleOf`            | Indicates that the source is an example instance of the target concept.     | Source → Target        | topic: path/to/example-instance.md
  isExampleOf:
    - link: path/to/general-concept.md |
| `isAlternativeTo`        | Indicates that the source is an alternative to the target (peer relationship).| Bidirectional         | topic: path/to/method-a.md
  isAlternativeTo:
    - link: path/to/method-b.md |
| `referencesSpecification`| Indicates that the source references a formal specification or standard.    | Source → Target        | topic: path/to/implementation-guide.md
  referencesSpecification:
    - link: path/to/spec-document.md |
| `deepensUnderstandingOf` | Indicates that the source provides additional depth or detail for the target.| Source → Target        | topic: path/to/advanced-topic.md
  deepensUnderstandingOf:
    - link: path/to/introductory-topic.md |

This list can be expanded via the governance process (e.g., reference to a future `[[OM-POLICY-STANDARDS-GOVERNANCE]]` standard).

**Illustrative Examples (Overall):**

YAML snippet within `some-kb/part-1/_overview.md`:
```yaml
reltable:
  - topic: master-knowledge-base/some-kb/part-1/01-main-concept.md # Path based example
    relatedConcepts:
      - link: master-knowledge-base/some-kb/shared/supporting-concept-x.md
        displayText: "Understanding Concept X"
    supportingTasks:
      - link: master-knowledge-base/some-kb/part-1/tasks/how-to-use-main-concept.md
  - topic: master-knowledge-base/some-kb/part-1/tasks/how-to-use-main-concept.md
    prerequisites:
      - link: master-knowledge-base/some-kb/part-1/01-main-concept.md
    referenceMaterial:
      - link: master-knowledge-base/some-kb/references/main-concept-api.md
```

**Cross-References to Other Standard IDs:**
- [[AS-STRUCTURE-KB-ROOT]] (Placeholder for U-ARCH-001)
- [[SF-LINKS-INTERNAL-SYNTAX]] (Placeholder for O-USAGE-LINKS-001)
- [[SF-SYNTAX-YAML-FRONTMATTER]] (Placeholder for M-SYNTAX-YAML-001)

---

## Standard: Task Document Schema (AS-SCHEMA-TASK)

# Standard: Task Document Schema (AS-SCHEMA-TASK)

## 1. Standard Statement

This standard defines the mandatory and recommended structure for creating **Task-Oriented Documents**. These documents guide users through a sequence of steps to achieve a specific goal. Examples include tutorials, how-to guides, standard operating procedures (SOPs), troubleshooting procedures, and installation instructions.

Adherence to this schema ensures that task documentation is clear, actionable, consistent, and easy for users to follow, leading to higher success rates and reduced errors. This schema builds upon the general document structure defined in `[[AS-STRUCTURE-DOC-CHAPTER]]`.

## 2. Purpose of Task Documents

Task documents are instructional. Users consult them to:
-   Understand how to perform a specific operation or procedure.
-   Learn the steps required to achieve a desired outcome.
-   Troubleshoot issues by following a defined process.
-   Ensure compliance with standard procedures.

They are distinct from reference documents (which describe *what* something is) or conceptual guides (which explain *why* something is).

## 3. Core Structure of a Task Document

A task document, after the standard frontmatter and H1 title (which should clearly state the task, e.g., "How to Install the Foobar Application" or "Procedure for Monthly Server Maintenance"), MUST generally follow this sequence of H2 sections. Some sections are optional depending on the complexity and nature of the task.

### 3.1. Goal / Purpose (Mandatory)
   - **Heading:** `## Goal`, `## Purpose`, or `## Objective`
   - **Content:** Clearly state the overall goal or desired outcome of completing the task (1-2 sentences). Briefly explain why this task is performed.

### 3.2. Prerequisites (Conditional - Recommended if applicable)
   - **Heading:** `## Prerequisites`
   - **Content:** List any conditions that must be met, skills required, or configurations needed before starting the task.
     - Use a bulleted or numbered list.
     - Example: "User must have administrator privileges," "Software version X.Y.Z must be installed," "[Standard: Content Schema for Concept Definitions](#standard-content-schema-for-concept-definitions-as-schema-concept-definition) on Topic Z must be understood."

### 3.3. Materials / Tools / Software Required (Conditional - Recommended if applicable)
   - **Heading:** `## Materials Required`, `## Tools Needed`, or `## Software Requirements`
   - **Content:** List any specific hardware, software, tools, parts, or information needed to perform the task.
     - Use a bulleted list.
     - Specify versions if important.

### 3.4. Safety Warnings / Important Notices (Conditional - Highly Recommended if applicable)
   - **Heading:** `## Safety Warnings`, `## Important Notices`, or `## Caution`
   - **Content:** Highlight any potential risks, safety precautions, data loss warnings, or critical information the user MUST be aware of before proceeding.
     - Use callouts (e.g., `[!WARNING]`, `[!CAUTION]`) for emphasis, as defined in `[[SF-CALLOUTS-SYNTAX]]`.

### 3.5. Steps / Procedure (Mandatory)
   - **Heading:** `## Steps`, `## Procedure`, or `## Instructions`
   - **Content:** The core of the document. Present the actions in a clear, sequential order.
     - **Numbered Lists:** Steps MUST be presented as a numbered list (see `[[SF-SYNTAX-LISTS]]`).
     - **Action-Oriented:** Start each step with a clear action verb (e.g., "Open," "Navigate," "Enter," "Verify").
     - **Granularity:** Break down complex actions into manageable sub-steps (nested numbered or bulleted lists).
     - **Clarity:** Each step should be unambiguous and concise.
     - **Conditional Steps:** Clearly indicate if a step is optional or depends on a previous choice (e.g., "If you selected Option A in Step 3, proceed to Step 4a; otherwise, skip to Step 5.").
     - **User Interface Elements:** Use bold text or backticks for UI elements like button names (`**Save**`), menu items (`File > Open`), or field labels (``Username``).
     - **Screenshots/Diagrams:** Optionally include screenshots or diagrams (see `[[SF-SYNTAX-IMAGES]]` and `[[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]]`) after a step if they significantly aid understanding. They should supplement, not replace, clear textual instructions.

### 3.6. Expected Results / Verification (Highly Recommended)
   - **Heading:** `## Expected Results` or `## Verification`
   - **Content:** Describe what the user should observe or be able to do after completing the steps, or a specific sub-set of steps.
     - This helps users confirm they have performed the task correctly.
     - Example: "The system will display a 'Configuration Saved Successfully' message." or "You should now be able to log in to the application."

### 3.7. Troubleshooting / Common Issues (Conditional - Recommended for complex tasks)
   - **Heading:** `## Troubleshooting` or `## Common Issues`
   - **Content:** List potential problems users might encounter, their causes, and solutions.
     - Use a problem/solution format, perhaps with bullet points or sub-headings.

### 3.8. Conclusion / Next Steps (Optional)
   - **Heading:** `## Conclusion` or `## Next Steps`
   - **Content:** Briefly summarize what was achieved. If applicable, suggest what the user might do next or point to related tasks or information.

### 3.9. See Also (Optional)
   - **Heading:** `## See Also`
   - **Content:** Links to related reference documents, conceptual guides, or other relevant tasks.

## 4. General Guidelines
- **Audience Focus:** Write for the intended audience, considering their technical proficiency.
- **Testing:** Whenever possible, procedures should be tested by someone other than the author to ensure clarity and accuracy.
- **Consistency:** Use consistent terminology, formatting, and level of detail across all task documents.
- **Modularity:** If a task is very long or has distinct sub-tasks that can be performed independently, consider breaking it into multiple, linked task documents.

## 5. Scope of Application
This schema applies to all documents that provide step-by-step instructions for users to achieve a specific outcome. This includes, but is not limited to, software installation guides, configuration procedures, user manual tasks, troubleshooting guides, and standard operating procedures.

---

## Standard: Asset Organization and Naming (AS-STRUCTURE-ASSET-ORGANIZATION)

# Standard: Asset Organization and Naming (AS-STRUCTURE-ASSET-ORGANIZATION)

## 1. Standard Statement

This standard defines the requirements for organizing, categorizing, naming, and formatting non-Markdown assets (such as images, diagrams, PDFs, and separate code snippets) within any Knowledge Base (KB). Proper asset organization is crucial for maintaining a clean repository, ensuring assets are discoverable, and facilitating link integrity.

## 2. Asset Directory Structure

### Rule 2.1: Top-Level `assets` Folder (Derived from U-ASSETS-001, Rule 1.1)
All non-Markdown assets associated with a specific Knowledge Base MUST reside in a dedicated top-level folder named `assets` directly within that KB's primary folder.
*   **Example:** If a KB's primary folder is `my-awesome-kb/`, then all its assets MUST be placed within `my-awesome-kb/assets/`.
*   **Rationale:** Centralizes all non-Markdown resources for a KB, making them easy to locate and manage. This is consistent with the overall KB directory structure outlined in [Knowledge Base Directory Structure Standard](#knowledge-base-directory-structure-standard-as-kb-directory-structure).

## 3. Asset Categorization

### Rule 3.1: Sub-folders for Categorization (Derived from U-ASSETS-001, Rule 1.2)
Within the `assets` folder, sub-folders SHOULD be used to categorize assets based on their type or purpose.
*   **Recommended Sub-folder Names:**
    *   `images/` (for PNG, JPG/JPEG, SVG, GIF files)
    *   `diagrams/` (specifically for flowchart, architecture, or other diagrammatic SVGs or PNGs, if differentiation from general images is useful)
    *   `pdfs/` (for PDF documents)
    *   `code-snippets/` (for external code files like `.py`, `.js`, `.sql` that are referenced or meant to be downloadable, not for embedded code in Markdown)
    *   Other categories as needed (e.g., `data/` for CSV files, `audio/` for audio clips).
*   **Example:** `my-awesome-kb/assets/images/user-interface-screenshot.png`, `my-awesome-kb/assets/pdfs/annual-report-2023.pdf`
*   **Folder Naming:** Sub-folder names MUST adhere to the folder naming conventions defined in [[GM-CONVENTIONS-NAMING]] (all lowercase kebab-case).
*   **Rationale:** Categorization improves the organization of the `assets` folder, making it easier to find and manage specific types of assets, especially in KBs with many assets.

## 4. Asset File Naming

### Rule 4.1: Descriptive Kebab-Case Names (Derived from U-ASSETS-001, Rule 1.3)
Asset file names MUST be descriptive of the asset's content or purpose and MUST adhere to the general file naming conventions (all lowercase kebab-case) defined in [[GM-CONVENTIONS-NAMING]].
*   **Example:** `q1-sales-report.pdf`, `user-flow-diagram.svg`, `api-request-example.py`
*   **Avoid:** Generic names like `image1.png`, `document.pdf`, or names with spaces or special characters (other than hyphens).
*   **Rationale:** Descriptive names make assets easier to identify and manage. Consistent kebab-casing ensures cross-platform compatibility and predictability.

## 5. Permitted Image Formats and Preferences

### Rule 5.1: Approved Image Formats (Derived from U-ASSETS-001, Rule 1.4)
The following image formats are permitted for use within the knowledge base:
*   `png` (Portable Network Graphics)
*   `svg` (Scalable Vector Graphics)
*   `jpg` or `jpeg` (Joint Photographic Experts Group)
*   `gif` (Graphics Interchange Format - primarily for simple animations if necessary)

### Rule 5.2: Format Preferences (Derived from U-ASSETS-001, Rule 1.4)
*   **Diagrams, Screenshots, Icons:** `svg` or `png` ARE PREFERRED due to their lossless quality and scalability (for SVG).
    *   `svg` is ideal for vector graphics that need to scale perfectly.
    *   `png` is suitable for raster graphics where transparency or sharp detail is needed (e.g., screenshots with text).
*   **Photographic Images:** `jpg` / `jpeg` is generally preferred for photographic images due to its ability to achieve good compression ratios for such content.
*   **Rationale:** Choosing appropriate image formats ensures a balance of visual quality, file size, and scalability, contributing to better performance and user experience. Using `svg` where possible for diagrams and icons allows for better rendering on high-resolution displays and when zoomed.

## 6. Importance of Asset Organization

*   **Maintainability:** A well-organized `assets` folder makes it easier to update or remove assets without breaking links or causing confusion.
*   **Discoverability:** Logical categorization and descriptive naming help authors and maintainers find existing assets for reuse or reference.
*   **Consistency:** Standardized organization and naming create a more professional and predictable repository structure.
*   **Reduced Clutter:** Prevents the root or content directories from being cluttered with media files.
*   **Build Process Efficiency:** Predictable asset locations can simplify automated build processes or static site generation.

## 7. Scope of Application

This standard applies to all non-Markdown files that are part of a Knowledge Base and are stored within its designated `assets` folder.

## 8. Cross-References
- [[GM-CONVENTIONS-NAMING]] - For general file and folder naming conventions.
- [[SF-ACCESSIBILITY-IMAGE-ALT-TEXT]] - For requirements related to the accessibility of images.
- [Knowledge Base Directory Structure Standard](#knowledge-base-directory-structure-standard-as-kb-directory-structure) - For the overall KB directory structure, including the location of the KB-specific `assets` folder.

---
*This standard (AS-STRUCTURE-ASSET-ORGANIZATION) is based on rules 1.1 through 1.4 previously defined in U-ASSETS-001 from COL-LINKING-UNIVERSAL.md.*

---

## Standard: Content Document (Chapter) Internal Structure (AS-STRUCTURE-DOC-CHAPTER)

# Standard: Content Document (Chapter) Internal Structure (AS-STRUCTURE-DOC-CHAPTER)

This standard defines the mandatory internal structure for primary content documents, typically referred to as "Chapters." Adherence ensures consistency, readability, and supports automated processing.

## 1. Rules for Chapter Structure

### Rule 1.1: Single H1 Heading (Derived from U-STRUC-002, Rule 2.1)
Every "Chapter" document MUST begin with an H1 heading, which serves as the document title. This MUST be the only H1 heading within the document.
*   **Example:** `# My Chapter Title`
*   **Notes:** This rule is fundamental for semantic structure and document parsing. Adherence to [[SF-SYNTAX-HEADINGS]] is required.

### Rule 1.2: Topic Abstract (Derived from U-STRUC-002, Rule 2.2)
An introductory "Topic Abstract," typically 1-3 paragraphs long, MUST immediately follow the H1 heading.
*   **Content:** The abstract should summarize the document's purpose, scope, and key takeaways.
*   **Notes:** This provides readers with a quick overview before they delve into the details.

### Rule 1.3: Table of Contents (ToC) (Derived from U-STRUC-002, Rule 2.3)
A Table of Contents (ToC) MUST follow the Topic Abstract. This ToC should link to all H2 sections and, where appropriate, significant H3 sections within the document.
*   **Example:**
    ```markdown
    ## Table of Contents
    - [Section 1 Title](#section-1-title)
    - [Section 2 Title](#section-2-title)
      - [Subsection 2.1 Title](#subsection-21-title)
    ```
*   **Notes:**
    *   Manual creation of the ToC or the use of a user's chosen authoring tool/plugin is acceptable. The key is the presence and accuracy of the ToC.
    *   Links MUST use the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]].

### Rule 1.4: Concluding "Summary" Section (Derived from U-STRUC-002, Rule 2.6)
A concluding section, typically titled "Summary" and formatted as an H2 heading, MUST be included at the end of the main content.
*   **Example:** `## Summary`
*   **Content:** This section should briefly reiterate the main points or key takeaways of the document.

### Rule 1.5: "See Also" Section (Derived from U-STRUC-002, Rule 2.7)
If relevant cross-references exist, a section titled "See Also" and formatted as an H2 heading MUST be included after the "Summary" section.
*   **Example:**
    ```markdown
    ## See Also
    - [[AS-STRUCTURE-KB-PART]]
    - [[EXAMPLE-STANDARD-ID]]
    ```
*   **Content:** This section should contain a list of links to related documents, standards, or sections that provide further context or information.
*   **Notes:** Links MUST use the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]]. If no relevant cross-references exist, this section may be omitted.

## 2. Illustrative Example

### Partial structure of a Chapter document (e.g., `01-introduction.md`):

```markdown
# Introduction to Research Methodology

This chapter introduces the core concepts of research methodology, outlining its importance and the foundational elements required for conducting systematic investigation. Key takeaways include understanding different research paradigms and the role of ethics in research.

## Table of Contents
- [What is Research?](#what-is-research)
- [Importance of Methodology](#importance-of-methodology)
- [Types of Research](#types-of-research)

## What is Research?
Research is a systematic investigation into and study of materials and sources in order to establish facts and reach new conclusions.
### Defining Research
The definition of research can vary across disciplines...

## Importance of Methodology
A sound methodology is crucial for the validity and reliability of research findings...

## Types of Research
Research can be broadly categorized into qualitative and quantitative approaches...

## Summary
This chapter provided an overview of research methodology, defined key terms, and highlighted the importance of a structured approach to investigation.

## See Also
- [[CS-POLICY-DOC-CHAPTER-CONTENT]]
- [[CONCEPT-CORE-RESEARCH-METHODOLOGY]]
```

## 3. Cross-References
- [[CS-POLICY-DOC-CHAPTER-CONTENT]] - Policy for content organization and heading usage within Chapters.
- [[SF-SYNTAX-HEADINGS]] - Standard for Markdown Heading Syntax.
- [[SF-LINKS-INTERNAL-SYNTAX]] - Standard for Internal Linking Syntax.
- [[GM-CONVENTIONS-NAMING]] - File and Folder Naming Conventions (if relevant to chapter file naming).

---
*This standard (AS-STRUCTURE-DOC-CHAPTER) is based on rules 2.1, 2.2, 2.3, 2.6, and 2.7 previously defined in U-STRUC-002 from COL-ARCH-UNIVERSAL.md.*

---

## Standard: Knowledge Base Part Structure and Overview (AS-STRUCTURE-KB-PART)

# Standard: Knowledge Base Part Structure and Overview (AS-STRUCTURE-KB-PART)

This standard defines the structural requirements for "Parts" (top-level primary sections) within a Knowledge Base (KB). It focuses on the mandatory overview that must introduce each Part, ensuring clarity and navigability.

## 1. Rules for "Part" Structure and Overview

### Rule 1.1: Mandatory Part Overview (Derived from U-STRUC-001, Rule 1.1)
Each "Part" (top-level primary section of a KB) MUST be fronted by an overview.
*   **Notes:** This overview serves as an entry point to the Part, guiding the user.

### Rule 1.2: Overview Location for Sub-folder Parts (Derived from U-STRUC-001, Rule 1.2)
If "Parts" are implemented as sub-folders (typically for larger KBs, as defined in [[AS-STRUCTURE-KB-ROOT]]), the overview content MUST reside in an `_overview.md` file located directly within that Part's folder.
*   **Example:** `research-methodology-kb/part-i-foundations/_overview.md`
*   **Notes:** The filename `_overview.md` is mandatory and MUST adhere to naming conventions in [[GM-CONVENTIONS-NAMING]].

### Rule 1.3: Overview Location for `root.md` Section Parts (Derived from U-STRUC-001, Rule 1.3)
If "Parts" are implemented as major H1 sections within the `root.md` file (typically for smaller KBs, as defined in [[AS-STRUCTURE-KB-ROOT]]), the overview content and links to its "Chapters" MUST directly follow the Part's H1 heading in `root.md`.
*   **Example (Structure within `root.md`):**
    ```markdown
    # Main KB Title

    ## Part I: First Major Section (H1 in this context)
    This part covers the foundational concepts... (This is the overview text)

    ### Chapters in this Part: (This is the ToC to chapters)
    - [Chapter 1: Introduction](./01-introduction.md)
    - [Chapter 2: Core Ideas](./02-core-ideas.md)
    ```
*   **Notes:** This ensures the overview is immediately accessible under the Part's heading.

### Rule 1.4: Content Requirements for Part Overview (Derived from U-STRUC-001, Rule 1.4)
The overview content for each Part (whether in `_overview.md` or within `root.md`) MUST:
    a.  Briefly explain the Part's scope, purpose, and the topics it covers.
    b.  Include a linked Table of Contents (ToC) to its main sub-sections, referred to as "Chapters."
*   **Notes:**
    *   Links in the ToC MUST use the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]].
    *   The overview text should be concise, typically 1-3 paragraphs.

## 2. Illustrative Example

### Snippet from `_overview.md` (for a Part implemented as a sub-folder)

File: `/research-methodology-kb/part-i-foundations/_overview.md`
```markdown
# Part I: Foundations of Research Methodology

This part lays the groundwork for understanding the core principles and initial stages of conducting formal research. It covers fundamental concepts, ethical considerations, and the importance of robust methodology.

## Chapters in this Part:
- [Chapter 1: Introduction to Research Methodology](./01-introduction-to-research-methodology.md)
- [Chapter 2: Core Concept of Research](./02-core-concept-of-research.md)
- [Chapter 3: Ethical Considerations in Research](./03-ethical-considerations.md)
```
*(Note: The example links above are illustrative path-based links. Per [[SF-LINKS-INTERNAL-SYNTAX]], these should ideally be `[[STANDARD_ID]]` or `[[FILENAME_ID_PLACEHOLDER]]` links once target IDs are defined and resolvable.)*

## 3. Cross-References
- [[CS-POLICY-KB-PART-CONTENT]] - Policy for content organization within KB Parts.
- [[AS-STRUCTURE-KB-ROOT]] - Defines the overall structure for KB root files and how Parts are organized.
- [[GM-CONVENTIONS-NAMING]] - File and Folder Naming Conventions (relevant for `_overview.md` and Part folder names).
- [[SF-LINKS-INTERNAL-SYNTAX]] - Internal Linking Syntax Standard.
- [[AS-STRUCTURE-DOC-CHAPTER]] - Standard for Content Document ("Chapter") Internal Structure.

---
*This standard (AS-STRUCTURE-KB-PART) is based on rules 1.1, 1.2, 1.3, and 1.4 previously defined in U-STRUC-001 from COL-ARCH-UNIVERSAL.md.*

---

## Standard: Knowledge Base Root Structure (AS-STRUCTURE-KB-ROOT)

# Standard: Knowledge Base Root Structure (AS-STRUCTURE-KB-ROOT)

This standard defines the mandatory structure for the root level of any Knowledge Base (KB), including the root file (`root.md`) and the organization of its top-level sections, referred to as "Parts."

## 1. Rules for KB Root Structure

### Rule 1.1: Designated Primary Folder
Each Knowledge Base (KB) MUST have a designated primary folder.
*   **Example:** `prompt-engineering-kb/`
*   **Notes:** Folder naming MUST adhere to [[GM-CONVENTIONS-NAMING]].

### Rule 1.2: Root Document (`root.md`)
Within this primary folder, a root document named `root.md` MUST exist.
*   **Example:** `prompt-engineering-kb/root.md`
*   **Notes:** This file serves as the main entry point and master index for the KB.

### Rule 1.3: Master Table of Contents (ToC) in `root.md`
The `root.md` file MUST contain a master Table of Contents (ToC) that links to all top-level primary sections ("Parts") of that KB.
*   **Notes:** Links MUST use the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]].

### Rule 1.4: Top-Level "Parts" in Larger KBs (Sub-folders)
For **larger KBs**, top-level "Parts" (primary sections) MUST be implemented as distinct sub-folders within the primary KB folder. Each such sub-folder represents one "Part".
*   **Example:** `research-methodology-kb/part-i-foundations/`
*   **Notes:** Folder naming MUST adhere to [[GM-CONVENTIONS-NAMING]]. The decision criterion for "larger" versus "smaller" is further discussed in [[CS-POLICY-KB-ROOT]].

### Rule 1.5: Top-Level "Parts" in Smaller KBs (`root.md` Sections)
For **smaller or moderately sized KBs**, top-level "Parts" (primary sections) MUST be major H1 sections (often rendered as H2 in the context of the `root.md` document itself, following the main H1 title of `root.md`) directly within the `root.md` file. Content for these Parts can be nested directly or linked to subordinate files within the same primary KB folder.
*   **Example (Heading in `root.md`):** `## Part I: Core Methods`
*   **Notes:** The decision criterion for "smaller" versus "larger" is further discussed in [[CS-POLICY-KB-ROOT]].

## 2. Illustrative Examples

### Example `root.md` for a Larger KB (Linking to Part Sub-folders)

```markdown
# Research Methodology Knowledge Base - Master Index

This knowledge base provides comprehensive guidance on research methodologies...

## Master Table of Contents

### Part I: Foundations of Research Methodology
- [Overview of Foundations](./part-i-foundations-of-research-methodology/_overview.md)
- [Introduction to Research Methodology](./part-i-foundations-of-research-methodology/01-introduction-to-research-methodology.md)
- [Core Concepts in Research](./part-i-foundations-of-research-methodology/02-core-concepts-in-research.md)

### Part II: Key Processes in Research
- [Overview of Key Processes](./part-ii-key-processes-in-research/_overview.md)
- [Data Collection Techniques](./part-ii-key-processes-in-research/01-data-collection-techniques.md)

### Part III: Advanced Topics
- [Overview of Advanced Topics](./part-iii-advanced-topics/_overview.md)
```
*(Note: The example links above are illustrative path-based links. Per [[SF-LINKS-INTERNAL-SYNTAX]], these should ideally be `[[STANDARD_ID]]` or `[[FILENAME_ID_PLACEHOLDER]]` links once target IDs are defined and resolvable.)*

## 3. Cross-References
- [[CS-POLICY-KB-ROOT]] - Policy for consistent application of KB root structures.
- [Knowledge Base Directory Structure Standard](#knowledge-base-directory-structure-standard-as-kb-directory-structure) - Defines overall repository and master knowledge base directory structures.
- [[GM-CONVENTIONS-NAMING]] - File and Folder Naming Conventions.
- [[SF-LINKS-INTERNAL-SYNTAX]] - Internal Linking Syntax Standard.
- [[AS-STRUCTURE-KB-PART]] - Primary KB Section ("Part") Structure.

---
*This standard (AS-STRUCTURE-KB-ROOT) is based on rules 1.1-1.5 previously defined in U-ARCH-001 from COL-ARCH-UNIVERSAL.md.*

---

## Standard: Master Knowledge Base Directory and Index Structure (AS-STRUCTURE-MASTER-KB-INDEX)

# Standard: Master Knowledge Base Directory and Index Structure (AS-STRUCTURE-MASTER-KB-INDEX)

This standard defines the structural requirements for the master directory that houses all Knowledge Bases (KBs) and the specific requirements for the `kb-directory.md` master index file.

## 1. Rules for Master Directory and Index

### Rule 1.1: Single Master Directory (Derived from U-ARCH-002, Rule 2.1)
All individual Knowledge Bases (KBs) MUST reside within a single, master top-level directory in the repository.
*   **Example:** `/digital-brain-vault/`
*   **Notes:** The specific name of this master directory (e.g., `digital-brain-vault`, `knowledge-bases`) can be chosen as per project preference, but its singular existence is mandatory. This directory is typically the root for all KB content. Refer to [Knowledge Base Directory Structure Standard](#knowledge-base-directory-structure-standard-as-kb-directory-structure) for how this fits into the broader repository structure.

### Rule 1.2: Master Index File (`kb-directory.md`) Existence (Derived from U-ARCH-002, Rule 2.3)
A master index file, named `kb-directory.md`, MUST reside directly within the master top-level directory.
*   **Example:** `/digital-brain-vault/kb-directory.md`
*   **Notes:** This file serves as the central directory or "yellow pages" for all KBs within the repository. Its naming MUST be exactly `kb-directory.md`.

### Rule 1.3: Content Requirements for `kb-directory.md` (Derived from U-ARCH-002, Rule 2.4)
The `kb-directory.md` file MUST:
    a.  List all active Knowledge Bases within the repository.
    b.  Provide a concise (typically 1-3 sentences) description of the primary scope and purpose of each listed KB.
    c.  Include a direct link to the `root.md` file of each listed KB.
*   **Notes:**
    *   Links MUST use the syntax defined in [[SF-LINKS-INTERNAL-SYNTAX]].
    *   The order of KBs listed in `kb-directory.md` should be logical, potentially alphabetical or grouped by a strategic theme.

## 2. Illustrative Example

### Snippet from `/digital-brain-vault/kb-directory.md`

```markdown
# Knowledge Base Directory

This directory provides an overview and access points to all active Knowledge Bases.

## Available Knowledge Bases

- **[Research Methodology KB](./research-methodology-kb/root.md)**: Focuses on research design, data collection, analysis, and open science practices for generating complex workflows. Excludes funding and ethics.
- **[Prompt Engineering KB](./prompt-engineering-kb/root.md)**: Covers principles, techniques, and frameworks for designing effective prompts for Large Language Models, including prompt construction, optimization, and management.
- **[Standards Development KB](./standards-kb/root.md)**: Contains all standards, policies, and guidelines for creating, managing, and governing content within the knowledge ecosystem.
```
*(Note: The example links above are illustrative path-based links. Per [[SF-LINKS-INTERNAL-SYNTAX]], these should ideally be `[[STANDARD_ID]]` or `[[FILENAME_ID_PLACEHOLDER]]` links if the KBs themselves or their root files have resolvable IDs, or be relative paths as shown if direct file linking is intended here.)*

## 3. Cross-References
- [[CS-POLICY-KB-IDENTIFICATION]] - Policy for unique KB identification and naming.
- [Knowledge Base Directory Structure Standard](#knowledge-base-directory-structure-standard-as-kb-directory-structure) - Defines the broader repository and `master-knowledge-base` directory structures.
- [[SF-LINKS-INTERNAL-SYNTAX]] - Internal Linking Syntax Standard.
- [[GM-CONVENTIONS-NAMING]] - File and Folder Naming Conventions (relevant for KB folder names).

---
*This standard (AS-STRUCTURE-MASTER-KB-INDEX) is based on rules 2.1, 2.3, and 2.4 previously defined in U-ARCH-002 from COL-ARCH-UNIVERSAL.md.*

---

## Standard: Templates Directory Structure and Usage (AS-STRUCTURE-TEMPLATES-DIRECTORY)

# Standard: Templates Directory Structure and Usage (AS-STRUCTURE-TEMPLATES-DIRECTORY)

## 1. Standard Statement

This standard defines the requirements for the creation, maintenance, and content of a dedicated directory for standard document templates. Utilizing a centralized templates directory promotes authoring efficiency, ensures consistency in document structure, and aids in the correct application of content schemas.

## 2. Core Requirements for the Templates Directory

### Rule 2.1: Dedicated Templates Directory (Derived from U-TEMPLATES-DIR-001, Rule 1.1, adapted)
A dedicated directory for housing standard document templates MUST be maintained at the following path: `/master-knowledge-base/standards/templates/`.
*   **Rationale:** Centralizes templates for easy discovery and consistent application across the knowledge base. This specific path aligns with the established directory structure for standards-related resources (see [Knowledge Base Directory Structure Standard](#knowledge-base-directory-structure-standard-as-kb-directory-structure)).
*   **Notes:** This directory was established in Phase 0 (Task 0.4.3).

### Rule 2.2: Content of the Templates Directory (Derived from U-TEMPLATES-DIR-001, Rule 1.2)
The `/master-knowledge-base/standards/templates/` directory MUST contain Markdown template files (`.md`) for common standard document types. These templates are intended to:
    a.  Pre-fill the basic structure of a new document according to relevant `AS-SCHEMA-*` (Architectural Standard - Schema) documents, such as [Standard: Content Schema for Methodology/Technique Descriptions](#standard-content-schema-for-methodologytechnique-descriptions-as-schema-methodology-description) and [Standard: Content Schema for Concept Definitions](#standard-content-schema-for-concept-definitions-as-schema-concept-definition).
    b.  Include placeholder content or comments to guide authors on filling out various sections.
    c.  May also include utility templates, such as a canonical frontmatter template (e.g., [[UA-TPL-CANONICAL-FRONTMATTER]], which was created in Phase 0, Task 0.4.3).

*   **Examples of Templates:**
    *   `tpl-standard-definition.md`
    *   `tpl-policy-document.md`
    *   `tpl-methodology-schema.md` (based on [Standard: Content Schema for Methodology/Technique Descriptions](#standard-content-schema-for-methodologytechnique-descriptions-as-schema-methodology-description))
    *   `tpl-concept-schema.md` (based on [Standard: Content Schema for Concept Definitions](#standard-content-schema-for-concept-definitions-as-schema-concept-definition))
    *   `[[UA-TPL-CANONICAL-FRONTMATTER]]`

### Rule 2.3: Template Naming Convention
All template filenames within the `/master-knowledge-base/standards/templates/` directory MUST be prefixed with `tpl-`.
*   **Example:** `tpl-standard-definition.md`, `tpl-canonical-frontmatter.md`.
*   **Rationale:** Clearly identifies files as templates and allows for easy programmatic identification or filtering. This convention was established in Phase 0 (Task 0.4.3).

## 3. Importance of Standardized Templates

*   **Efficiency:** Authors can create new standards-compliant documents more quickly by starting from a template.
*   **Consistency:** Ensures that all documents of a particular type share a common structure and include all mandatory sections and frontmatter fields.
*   **Accuracy:** Helps authors adhere to specific content schemas and frontmatter rules, reducing errors.
*   **Ease of Onboarding:** New contributors can more easily understand expected document structures by referring to or using templates.

## 4. Scope of Application

This standard applies to the management of the templates directory and the creation of new templates. Authors creating new standard documents are strongly encouraged to use these templates.

## 5. Cross-References
- [Knowledge Base Directory Structure Standard](#knowledge-base-directory-structure-standard-as-kb-directory-structure) - Defines the overall location of the `/master-knowledge-base/standards/templates/` directory.
- [Standard: Content Schema for Methodology/Technique Descriptions](#standard-content-schema-for-methodologytechnique-descriptions-as-schema-methodology-description) - An example of a schema for which a template should exist.
- [Standard: Content Schema for Concept Definitions](#standard-content-schema-for-concept-definitions-as-schema-concept-definition) - Another example of a schema for which a template should exist.
- [[UA-TPL-CANONICAL-FRONTMATTER]] - Reference to the existing canonical frontmatter template. (Note: This is a direct reference to a template file, not a standard. It's included as it's a key example of a utility template.)

---
*This standard (AS-STRUCTURE-TEMPLATES-DIRECTORY) is based on rules 1.1 and 1.2 previously defined in U-TEMPLATES-DIR-001 from COL-GOVERNANCE-UNIVERSAL.md, adapting them for the new directory structure and emphasizing established naming conventions.*
