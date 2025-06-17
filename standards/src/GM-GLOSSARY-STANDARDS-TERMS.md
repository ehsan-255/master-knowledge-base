---
title: Glossary of Standards Terminology
standard_id: GM-GLOSSARY-STANDARDS-TERMS
aliases:
- Standards Glossary
- KB Governance Terms
tags:
- content-type/glossary-document
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/glossary
- topic/gm
- topic/standards-governance
kb-id: standards
info-type: glossary-document
primary-topic: Provides definitions for key terms, acronyms, and concepts used throughout
  the Knowledge Base standards and governance documentation.
related-standards:
- GM-MANDATE-STANDARDS-GLOSSARY
- MT-SCHEMA-FRONTMATTER
version: 0.2.0
date-created: '2025-05-29T16:04:35Z'
date-modified: '2025-06-17T14:16:00Z'
primary_domain: GM
sub_domain: GLOSSARY
scope_application: Applies to all users and contributors of the knowledge base ecosystem
  to ensure a common understanding of terminology related to standards.
criticality: P1-High
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
- User understanding
- Communication clarity
- Standards adoption
- Onboarding
---
# Glossary of Standards Terminology (GM-GLOSSARY-STANDARDS-TERMS)

This document provides definitions for key terms used throughout the Knowledge Base standards and governance documentation. This glossary is mandated by `[[GM-MANDATE-STANDARDS-GLOSSARY]]`.

## A

**Atomic Standard:** A standard focused on a single, specific rule or process, designed to be modular and individually addressable.

**Attribute (Content Profiling):** Named characteristic for content profiling, allowing content to be shown/hidden based on value (e.g., `audience`, `platform`).

## C

**Canonical Frontmatter:** Mandatory and optional metadata keys, order, data types, and validation rules defined in `[[MT-SCHEMA-FRONTMATTER]]`.

**Conditional Text:** Content displayed or hidden based on predefined conditions using profiling attributes.

**Controlled Vocabulary:** Predefined, restricted set of terms for specific metadata fields to ensure consistency (e.g., `info-type`, `criticality`).

## F

**Frontmatter (YAML):** YAML-formatted metadata block at the beginning of Markdown documents, delimited by `---`, containing document information.

## I

**info-type:** Mandatory frontmatter key specifying document category from controlled vocabulary (e.g., `standard-definition`, `policy-document`).

## K

**kb-id:** Mandatory frontmatter key identifying which Knowledge Base a document belongs to (e.g., `kb-id/standards`).

**Keyref:** Placeholder (e.g., `{{key.someName}}`) replaced by predefined text during rendering. Managed by `[[UA-KEYDEFS-GLOBAL]]`.

**Knowledge Base (KB):** Managed collection of information and documents focused on specific domain, structured according to defined standards.

## P

**Primary Domain:** Two-letter uppercase code (e.g., `AS`, `CS`, `MT`) used in `standard_id` for categorizing standards by governance area.

**Primary Topic:** Mandatory frontmatter key (`primary-topic`) with concise statement describing document's main subject.

**Profiling (Content):** Practice of tailoring content for specific contexts using conditional text (audiences, platforms, feature versions).

## R

**Registry:** Formal collection of defined terms, codes, or identifiers serving as controlled vocabulary. Governed by `[[GM-REGISTRY-GOVERNANCE]]`.

**Resolver Script:** Automated process transforming source documents with keyrefs and conditional text into rendered documents.

## S

**Schema:** Formal definition of structure, elements, and rules for document or data types (e.g., `[[MT-SCHEMA-FRONTMATTER]]`).

**Source-and-Render Model:** Operational model where content is authored in source documents then processed by resolver scripts for consumption.

**Standard ID:** Unique, structured identifier for each standard document following pattern `XX-YYYY-ZZZZZ`.

**Sub-domain:** 2-6 letter uppercase code for further categorizing standards within their `primary_domain`.

## T

**Tag:** Kebab-case keyword assigned via frontmatter `tags` field for categorization and discovery. Governed by `[[MT-REGISTRY-TAG-GLOSSARY]]`.

**Transclusion:** Embedding content from one document into another by reference for content reuse.
