---
title: Glossary of Standards Terminology
standard_id: GM-GLOSSARY-STANDARDS-TERMS
aliases:
- Standards Glossary
- KB Governance Terms
tags:
- status/draft
- criticality/p1-high
- content-type/glossary-document
- topic/glossary
- topic/standards-governance
- kb-id/standards
kb-id: standards
info-type: glossary-document
primary-topic: Provides definitions for key terms, acronyms, and concepts used throughout the Knowledge Base standards and governance documentation.
related-standards:
- GM-MANDATE-STANDARDS-GLOSSARY
- MT-SCHEMA-FRONTMATTER
version: 0.1.0
date-created: '2025-05-29T16:04:35Z'
date-modified: '2025-05-30T14:00:00Z'
primary_domain: GM
sub_domain: GLOSSARY
scope_application: Applies to all users and contributors of the knowledge base ecosystem to ensure a common understanding of terminology related to standards.
criticality: p1-high
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
- User understanding
- Communication clarity
- Standards adoption
- Onboarding
change_log_url: ./GM-GLOSSARY-STANDARDS-TERMS-changelog.md
---
# Glossary of Standards Terminology (GM-GLOSSARY-STANDARDS-TERMS)

This document provides definitions for key terms, acronyms, and concepts used throughout the Knowledge Base (KB) standards and governance documentation. Its purpose is to establish a shared understanding and ensure clarity in communication.

This glossary is mandated by `[[GM-MANDATE-STANDARDS-GLOSSARY]]`.

## A

Atomic Standard
:   A standard that is focused on a single, specific rule, component, or process, designed to be modular and individually addressable. This promotes clarity, reusability, and ease of maintenance. See also: `[[CS-MODULARITY-TRANSCLUSION-POLICY]]`.

Attribute (Content Profiling)
:   A named characteristic used for content profiling, allowing content to be shown or hidden based on its value. Examples include `audience`, `platform`. See `[[CS-CONTENT-PROFILING-POLICY]]`.

## C

Canonical Frontmatter
:   The set of mandatory and optional metadata keys, their specific order, data types, and validation rules, as defined in the `[[MT-SCHEMA-FRONTMATTER]]` standard, which must be present in the YAML frontmatter of documents.

Conditional Text
:   Content within a document that is displayed or hidden based on predefined conditions, typically using profiling attributes. See `[[CS-CONTENT-PROFILING-POLICY]]` and `[[SF-CONDITIONAL-SYNTAX-ATTRIBUTES]]`.

Controlled Vocabulary
:   A predefined, restricted set of terms or values that must be used for a specific metadata field or tag category to ensure consistency and prevent ambiguity. Examples include values for `info-type`, `criticality`, or specific tag groups like `status/*`. See `[[MT-REGISTRY-TAG-GLOSSARY]]`, `[[GM-REGISTRY-GOVERNANCE]]`.

## F

Frontmatter (YAML)
:   A block of YAML-formatted metadata at the beginning of a Markdown document, delimited by triple hyphens (`---`), used to store information about the document such as its title, ID, tags, dates, etc. See `[[MT-SCHEMA-FRONTMATTER]]` and `[[SF-SYNTAX-YAML-FRONTMATTER]]`.

## I

info-type
:   A mandatory frontmatter key that specifies the type or category of information the document represents (e.g., `standard-definition`, `policy-document`). Its value comes from a controlled vocabulary defined in `[[MT-SCHEMA-FRONTMATTER]]` and is critical for automation.

## K

kb-id (Knowledge Base Identifier)
:   A mandatory frontmatter key whose value is a tag from a controlled vocabulary (see `[[MT-REGISTRY-TAG-GLOSSARY]]`) that identifies which specific Knowledge Base (KB) a document belongs to (e.g., `kb-id/standards`, `kb-id/llm-cookbook`).

Keyref (Key-based Reference)
:   A placeholder (e.g., `{{key.someName}}`) in content that gets replaced by a predefined snippet of text during a rendering or publishing process. Key definitions are managed centrally. See `[[UA-KEYDEFS-GLOBAL]]`, `[[MT-KEYREF-MANAGEMENT]]`, and `[[SF-SYNTAX-KEYREF]]`.

Knowledge Base (KB)
:   A managed collection of information, documents, and resources, typically focused on a specific domain or purpose, and structured according to defined standards.

## P

Primary Domain
:   A two-letter uppercase code (e.g., `AS`, `CS`, `MT`) used in `standard_id` and the `primary_domain` frontmatter field to categorize a standard by its main area of governance. Defined in `[[domain_codes.yaml]]`.

Primary Topic
:   A mandatory frontmatter key (`primary-topic`) holding a concise statement describing the main subject of a document. See `[[MT-STRATEGY-PRIMARY-TOPIC-KEYWORD]]`.

Profiling (Content)
:   The practice of tailoring content for specific contexts, such as different audiences, platforms, or feature versions, often implemented using conditional text. See `[[CS-CONTENT-PROFILING-POLICY]]`.

## R

Registry
:   A formal collection of defined terms, codes, or identifiers that serve as a controlled vocabulary for specific purposes. Examples include the tag glossary or domain code lists. Governed by `[[GM-REGISTRY-GOVERNANCE]]`.

Resolver Script
:   An automated script or process that transforms source documents (which may contain keyrefs, conditional text, etc.) into fully populated, "rendered" documents suitable for consumption by humans or LLMs. Part of the "Source-and-Render" model.

## S

Schema
:   A formal definition of the structure, elements, and rules for a particular type of document or data. Examples include `[[MT-SCHEMA-FRONTMATTER]]` (for frontmatter), `[[AS-SCHEMA-CONCEPT-DEFINITION]]` (for concept documents).

Source-and-Render Model
:   An operational model for the KB where content is authored in "source" documents (e.g., Markdown with special syntax like keyrefs) and then processed by a "resolver script" to produce "rendered" documents for consumption. See `[[AS-KB-DIRECTORY-STRUCTURE]]`.

Standard ID (`standard_id`)
:   A unique, structured identifier assigned to each standard document, following a defined pattern (e.g., `XX-YYYY-ZZZZZ`). See `[[MT-SCHEMA-FRONTMATTER]]` for format rules.

Sub-domain
:   A 2-6 letter uppercase code used in `standard_id` and the `sub_domain` frontmatter field to further categorize a standard within its `primary_domain`. Defined in `[[subdomain_registry.yaml]]`.

## T

Tag
:   A keyword or label, typically in kebab-case, assigned to a document via its frontmatter `tags` field to categorize it, indicate its status, or facilitate discovery. Governed by `[[MT-TAGGING-STRATEGY-POLICY]]` and defined in `[[MT-REGISTRY-TAG-GLOSSARY]]`.

Transclusion
:   The embedding or inclusion of content from one document into another by reference, allowing for content reuse. See `[[CS-MODULARITY-TRANSCLUSION-POLICY]]` and `[[SF-TRANSCLUSION-SYNTAX]]`.

> [!TODO] This glossary is not exhaustive and should be expanded as more terms are standardized or require clarification.
