---
title: "Standard: Primary Topic Keyword Strategy"
standard_id: "MT-STRATEGY-PRIMARY-TOPIC-KEYWORD"
aliases:
  - "Primary Topic Strategy"
  - "Topic Keywords"
tags:
  - status/draft
  - criticality/p2-medium
  - content-type/technical-standard
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "Primary Topic Keyword Strategy"
related-standards: ["MT-SCHEMA-FRONTMATTER"]
version: '1.0.0'
date-created: "2025-05-29T13:24:53Z"
date-modified: "2025-05-30T18:00:00Z"
primary_domain: "MT"
sub_domain: "FRONTMATTER"
scope_application: "Defines the strategy for selecting and formatting primary topic keywords in frontmatter."
criticality: "P2-Medium"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Content categorization", "Search optimization", "Metadata consistency"]
change_log_url: "./MT-STRATEGY-PRIMARY-TOPIC-KEYWORD-changelog.md"
---
# Standard: Primary Topic Keyword Strategy

## 1. Standard Statement

This standard defines the strategy and provides guidelines for selecting, formatting, and utilizing the `primary-topic` keyword within the YAML frontmatter of Markdown documents. The `primary-topic` key is defined in `[[MT-SCHEMA-FRONTMATTER]]`.

The primary purpose of the `primary-topic` field is to offer a concise, human-readable, and machine-processable keyword or short phrase that encapsulates the core subject of the document. This enhances content discovery, improves metadata consistency, aids in automated indexing, and boosts overall searchability.

## 2. Purpose of the `primary-topic` Key

The `primary-topic` key serves several functions:

*   **Enhanced Discoverability:** Provides a quick understanding of the document's core subject without needing to parse the full title or content.
*   **Improved Search:** Acts as a primary keyword for search engines and internal search tools.
*   **Content Grouping:** Can be used by automation to group related documents or suggest connections.
*   **Disambiguation:** Helps differentiate documents with similar titles or broad subjects by specifying a focused topic.
*   **Consistency:** Ensures a standardized approach to defining the main subject across documents.

## 3. Guidelines for Selecting and Formatting `primary-topic`

### 3.1. Conciseness and Clarity
*   The `primary-topic` SHOULD be a short, clear keyword or phrase, typically between 1 to 5 words.
*   It MUST be easily understandable and accurately reflect the main subject of the document.
*   Avoid jargon where possible, unless the jargon itself is the topic.

### 3.2. Relationship to Title and `standard_id`
*   **For Standards and Policies:**
    *   If the document has a `standard_id` (e.g., `AS-STRUCTURE-KB-ROOT`, `CS-POLICY-KB-ROOT`), the `primary-topic` can often be derived from the descriptive part of the `standard_id`.
    *   To ensure differentiation, especially for related concepts (like a standard defining a structure vs. a policy for that structure), the `primary-topic` should clearly reflect the document's specific intent.
        *   Example for `standard_id: AS-STRUCTURE-KB-ROOT` (`info-type: standard-definition`): `primary-topic: "Knowledge Base Root Structure"`
        *   Example for `standard_id: CS-POLICY-KB-ROOT` (`info-type: policy-document`): `primary-topic: "Policy for Knowledge Base Root"`
    *   It MAY be a slightly more descriptive version of the `standard_id`'s core concept if the `standard_id` is very terse.
*   **For Other Documents:**
    *   The `primary-topic` should generally be a condensed version or the most significant keyword from the `title`.
    *   It should capture the essence of the `title` in fewer words.

### 3.3. Formatting
*   The `primary-topic` is a string value.
*   While `MT-SCHEMA-FRONTMATTER` does not mandate a specific case, **Title Case** or **Sentence case** is recommended for readability. Consistency within a knowledge base or domain is encouraged. Kebab-case is NOT typically used for `primary-topic`.
    *   Example (Title Case): `"Knowledge Base Root Structure"`
    *   Example (Sentence case): `"Knowledge base root structure"`

### 3.4. Uniqueness and Specificity
*   While not strictly unique like a `standard_id`, the `primary-topic` should be specific enough to be useful for filtering and searching.
*   Avoid overly generic terms if more specific alternatives that still accurately represent the content are available. For example, instead of `"Documentation"`, prefer `"Style Guide Documentation"` if that's more accurate.

## 4. Examples

1.  **Standard Document:**
    *   `title: "Standard: Knowledge Base Root Structure Definition"`
    *   `standard_id: "AS-STRUCTURE-KB-ROOT"`
    *   `info-type: "standard-definition"`
    *   `primary-topic: "Knowledge Base Root Structure"`

2.  **Policy Document:**
    *   `title: "Policy: Content Review and Approval for KB Root"`
    *   `standard_id: "CS-POLICY-KB-ROOT-REVIEW"`
    *   `info-type: "policy-document"`
    *   `primary-topic: "Policy for KB Root Review"`

3.  **Guide Document:**
    *   `title: "Comprehensive Guide to Using the Advanced Search Feature"`
    *   `info-type: "guide-document"`
    *   `primary-topic: "Advanced Search Guide"`

4.  **Glossary Term Definition (if `primary-topic` were used, though less common for this `info-type`):**
    *   `title: "Glossary Definition: Epistemology"`
    *   `info-type: "glossary-document"` (or a more granular `key-definition-set`)
    *   `primary-topic: "Epistemology Definition"`

## 5. Scope of Application
This strategy applies to the `primary-topic` field in the YAML frontmatter of all relevant documents across all knowledge bases where this field is mandated or utilized, as per `[[MT-SCHEMA-FRONTMATTER]]`.
