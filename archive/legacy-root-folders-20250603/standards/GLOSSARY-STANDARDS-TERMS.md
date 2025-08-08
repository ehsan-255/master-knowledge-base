---
title: Glossary of Standards Terminology - DEPRECATED
aliases:
- Standards Glossary
- Terminology for Standards
tags:
- content-type/standards-glossary
- content-type/standards-guide
- criticality/p0-critical
- kb-id/standards
- status/deprecated
- topic/glossary
- topic/standards-governance
kb-id: standards
info-type: standards-glossary
primary-topic: Defines key terms used within the Universal Knowledge Base Standards
  documents themselves to ensure consistent understanding.
related-standards:
- GM-GLOSSARY-STANDARDS-TERMS
version: 0.2.0
date-created: '2025-05-22T00:00:00Z'
date-modified: '2025-06-17T02:29:13Z'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: [[GM-GLOSSARY-STANDARDS-TERMS]].

> [!WARNING] DEPRECATED: This Document is No Longer Active
> **Reason for Deprecation:** This document has been superseded by [[GM-GLOSSARY-STANDARDS-TERMS]].
> Please refer to the new glossary for current definitions. This document is retained for historical purposes only.

# Glossary of Standards Terminology

This glossary defines key terms as they are used within the Universal Knowledge Base Standards documents.

## A
-   **Atomic Content:** Content that is self-contained, focused on a single topic or idea, and can be understood with minimal external context, facilitating reuse and modularity.

## F
-   **Frontmatter (YAML):** A block of metadata in YAML format at the beginning of a Markdown document, enclosed by triple hyphens (`---`), used to define properties of the document.

## I
-   **info-type:** A YAML frontmatter key specifying the precise structural or processing classification of a document, using kebab-case values (e.g., `standard-document`, `kb-definition-map`). Critical for automation.

## K
-   **Kebab-case:** A naming convention where words are written in lowercase and separated by hyphens (e.g., `my-file-name`).
-   **Keyref (Key-Based Referencing):** A system using placeholders (e.g., `{{key.productName}}`) in source documents that are replaced with centrally defined values during a rendering process.

## M
-   **Monolith:** A single, large document compiled from multiple smaller source documents, often for ease of distribution or comprehensive review.

## R
-   **Rendered Document:** A version of a knowledge base document that has had all dynamic placeholders (like keyrefs and conditional content) resolved. This is the consumable version.

## S
-   **Schema (Content Schema):** A predefined structure or template that dictates the mandatory and optional sections, headings, and metadata for a specific type of content document.
-   **Source Document:** The primary, editable version of a knowledge base document, which may contain placeholders for dynamic content.

*(This glossary will be expanded as more terms are identified.)*
