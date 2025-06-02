---
title: 'Standard: Content Schema for Methodology/Technique Descriptions'
standard_id: AS-SCHEMA-METHODOLOGY-DESCRIPTION
aliases:
- Methodology Schema
- Technique Description Schema
tags:
- status/draft
- criticality/p1-high
- content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Schema for Methodology/Technique Descriptions
related-standards:
- AS-STRUCTURE-DOC-CHAPTER
- CS-POLICY-LAYERED-INFORMATION
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-01T23:21:22Z'
primary_domain: AS
sub_domain: SCHEMA
scope_application: Defines the mandatory content structure (schema) for documents that describe specific methodologies, techniques, or detailed processes.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content consistency
- Authoring efficiency
- User understanding of complex processes
- Information reusability
change_log_url: ./changelog.md
---

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
