---
title: "Standard: Citing External Sources (APA 7th Edition)"
standard_id: "SF-FORMATTING-CITATIONS"
aliases: ["Citation Standard", "APA 7th Edition Citation", "External Source Citation"]
tags:
  - status/draft
  - criticality/P1-High # Proper citation is crucial for academic integrity and verifiability
  - content-type/technical-standard
kb-id: "" # Global standard
info-type: "standard-definition"
primary-topic: "Citation of External Sources" # As per prompt
related-standards: ["SF-LINKS-INTERNAL-SYNTAX"] # For linking syntax in references (though these are external)
version: "1.0.0"
date-created: "2024-07-15T12:00:00Z"
date-modified: "2024-07-15T12:00:00Z"
primary_domain: "SF" # Syntax & Formatting
sub_domain: "FORMATTING" # As per prompt
scope_application: "All documents within the knowledge base that reference, quote, or derive information from external published or citable sources."
criticality: "P1-High"
lifecycle_gatekeeper: "Editorial-Board-Approval" # Citation style is often an editorial decision
impact_areas: ["Academic integrity", "Content verifiability", "User trust", "Legal compliance (copyright)", "Consistency in referencing"]
change_log_url: "./SF-FORMATTING-CITATIONS-changelog.md" # Placeholder
---

# Standard: Citing External Sources (APA 7th Edition) (SF-FORMATTING-CITATIONS)

## 1. Standard Statement

This standard defines the mandatory requirements for citing external sources within all knowledge base documents. Proper attribution of external information is essential for maintaining academic integrity, ensuring content verifiability, respecting intellectual property, and providing users with pathways to source material.

## 2. Requirement for Attribution (Derived from U-CITE-001, Rule 1.1)

Any claims, direct quotations, specific data points, or paraphrased information derived from external published or citable sources MUST be clearly attributed to the original source.
*   **Rationale:** Upholds academic and professional integrity, allows readers to verify information, and gives credit to original authors.

## 3. Adopted Citation Style (APA 7th Edition) (Derived from U-CITE-001, Rule 1.2)

The **7th Edition of the Publication Manual of the American Psychological Association (APA)** IS THE ADOPTED AND MANDATORY CITATION STYLE for all knowledge base documents.
*   **Consistency:** This style MUST be used consistently for both in-text citations and the "References" list across all Knowledge Bases.
*   **Rationale:** Using a single, well-established citation style ensures uniformity, predictability, and clarity in how sources are referenced, making it easier for both authors and readers.

## 4. In-Text Citations (Derived from U-CITE-001, Rule 1.3)

In-text citations MUST be used within the body of the text to indicate the source of specific information at the point where it is presented.
*   **Format:** Follow APA 7th Edition guidelines for author-date citations.
    *   **Example (Paraphrase):** ...as research has shown that this method is effective (Smith, 2023).
    *   **Example (Direct Quote):** Smith (2023) stated, "the results were conclusive" (p. 45).
*   **Rationale:** Provides immediate attribution and allows readers to easily locate the full reference in the "References" section.

## 5. "References" Section (Derived from U-CITE-001, Rule 1.4)

A dedicated section titled "References," formatted as an H2 heading, MUST be included at the end of any document that contains citations.
*   **Content:** This section MUST list all sources cited in-text.
*   **Format:** All entries in the "References" list MUST fully conform to APA 7th Edition formatting guidelines.
*   **Order:** Entries are typically listed alphabetically by the first author's last name.
*   **Example:**
    ```markdown
    ## References
    Smith, J. A. (2023). *The Art of Referencing*. Publisher Name.
    Jones, P., & Adams, B. K. (2022). Citing sources in the digital age. *Journal of Scholarly Communication*, *15*(2), 112-130. https://doi.org/xxxx/xxxx
    ```
*   **Rationale:** Provides readers with the complete bibliographic information needed to locate and consult the original sources.

## 6. Citing Online Sources (Derived from U-CITE-001, Rule 1.5)

When citing online sources, the following specific guidelines apply within the APA 7th Edition framework:
*   **Hyperlinks:** If the source is publicly available online, a direct and stable hyperlink (URL or DOI) MUST be included in the "References" list entry.
    *   **Syntax for links:** Standard Markdown link syntax can be used within the reference entry if desired for active links, e.g., `[https://doi.org/xxxx/xxxx](https://doi.org/xxxx/xxxx)` or simply the URL/DOI text which might be auto-linked by renderers. Adherence to [[SF-LINKS-INTERNAL-SYNTAX]] is for internal links, but general good practice for link clarity applies.
*   **Retrieval Dates:** According to APA 7th Edition, retrieval dates are generally NOT required for most online sources if the content is stable (e.g., journal articles with DOIs, final versions of web pages). However, a retrieval date MAY be included if the source material is expected to change over time and there is no archive URL (e.g., a frequently updated webpage that is not a formal publication).
    *   **Example (with retrieval date, if necessary):** Author, A. A. (Year, Month Day). *Title of work*. Site Name. Retrieved Month Day, Year, from https://xxxx
*   **Rationale:** Facilitates direct access to online sources and addresses the dynamic nature of web content.

## 7. Importance of Proper Citation

*   **Academic and Professional Integrity:** Acknowledges the work of others and avoids plagiarism.
*   **Verifiability:** Allows readers to consult original sources to verify information and explore topics in more depth.
*   **Building Trust:** Demonstrates rigor and credibility, enhancing user trust in the KB content.
*   **Legal Compliance:** Helps respect copyright and intellectual property rights.
*   **Supporting Further Research:** Provides a foundation for others to build upon existing knowledge.

## 8. Scope of Application

This standard applies to all documents within any Knowledge Base that incorporate information from external sources, whether through direct quotation, paraphrase, data presentation, or summarization.

## 9. Cross-References
- [[SF-LINKS-INTERNAL-SYNTAX]] - For general Markdown link syntax (though external links are primarily governed by APA 7th style for the URL/DOI presentation itself).
- Official APA 7th Edition Style and Grammar Guidelines (External Resource).

---
*This standard (SF-FORMATTING-CITATIONS) is based on rules 1.1 through 1.5 previously defined in U-CITE-001 from COL-LINKING-UNIVERSAL.md.*
```
