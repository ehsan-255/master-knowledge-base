---

title: 'Standard: Citation Formatting Guidelines'
standard_id: SF-FORMATTING-CITATIONS
aliases:
- Citations
- Reference Formatting
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Citation Formatting Guidelines
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the formatting standards for citations and references in
  knowledge base documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Citation consistency
- Reference formatting
- Academic standards
---
# Standard: Citing External Sources (APA 7th Edition) (SF-FORMATTING-CITATIONS)

## 1. Standard Statement

This standard **MANDATES** the exclusive requirements for citing external sources within all Knowledge Base documents. Proper attribution is **CRITICAL** for maintaining academic integrity, ensuring content verifiability, respecting intellectual property, and providing users with pathways to source material.

## 2. Core Citation Rules

### Rule 2.1: Requirement for Attribution
Any claims, direct quotations, specific data points, or paraphrased information derived from external, published, or citable sources **MUST** be clearly attributed.
*   **Rationale:** Upholds academic/professional integrity and allows verification.

### Rule 2.2: Adopted Citation Style (APA 7th Edition)
The **7th Edition of the Publication Manual of the American Psychological Association (APA)** is the **MANDATORY** citation style for all Knowledge Base documents. This style **MUST** be used consistently for both in-text citations and the "References" list.
*   **Rationale:** Ensures uniformity, predictability, and clarity in referencing.

### Rule 2.3: In-Text Citations
In-text citations **MUST** be used within the text body to indicate the source at the point of presentation. Follow APA 7th Edition guidelines for author-date citations.
*   **Example (Paraphrase):** ...as research has shown (Smith, 2023).
*   **Example (Direct Quote):** Smith (2023) stated, "the results were conclusive" (p. 45).
*   **Rationale:** Provides immediate attribution and aids full reference lookup.

### Rule 2.4: "References" Section
A dedicated section titled "References," formatted as an H2 heading, **MUST** be included at the end of any document containing citations. This section **MUST** list all sources cited in-text, conforming fully to APA 7th Edition formatting. Entries **MUST** be listed alphabetically by the first author's last name.
*   **Example:**
    ```markdown
    ## References
    Smith, J. A. (2023). *The Art of Referencing*. Publisher Name.
    Jones, P., & Adams, B. K. (2022). Citing sources in the digital age. *Journal of Scholarly Communication*, *15*(2), 112-130. https://doi.org/xxxx/xxxx
    ```
*   **Rationale:** Provides complete bibliographic information for source consultation.

### Rule 2.5: Citing Online Sources
When citing online sources, a direct and stable hyperlink (URL or DOI) **MUST** be included in the "References" list entry. Retrieval dates are generally **NOT** required for stable online sources (e.g., journal articles with DOIs).
*   **Example (URL in References):** Author, A. A. (Year). *Title of work*. Site Name. https://xxxx
*   **Rationale:** Facilitates direct access to online sources.

## 3. Importance of Strict Citation Formatting

*   **Academic and Professional Integrity:** Acknowledges work and avoids plagiarism.
*   **Verifiability:** Allows readers to verify information.
*   **Building Trust:** Demonstrates rigor and credibility.
*   **Legal Compliance:** Respects copyright/intellectual property.
*   **Supporting Further Research:** Provides foundation for others.

## 4. Scope of Application

This standard applies to **ALL** documents within any Knowledge Base that incorporate information from external sources. Adherence to these rules is **MANDATORY** for all content creators, automated systems, and tooling interacting with KB Markdown files.

## 5. Cross-References
*   [[SF-LINKS-INTERNAL-SYNTAX]]

---
*This standard (SF-FORMATTING-CITATIONS) has been revised to mandate strict APA 7th Edition citation formatting, including specific rules for in-text citations, references section, and online sources, ensuring academic integrity and verifiability.*
