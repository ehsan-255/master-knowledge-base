---
title: Global Key Definitions
aliases:
  - Keyrefs
  - Key Definitions Store
  - _key_definitions
tags:
  - kb-id/global
  - content-type/key-definition-set
  - status/live
  - topic/automation
  - topic/content-management
standard_id: UA-KEYDEFS-GLOBAL
kb-id: global
info-type: key-definition-set
primary-topic: Central repository for globally reusable key-value pairs (keyrefs) used for content consistency and automation.
primary_domain: UA
sub_domain: KEYDEFS
related-standards:
  - MT-KEYREF-MANAGEMENT
  - SF-SYNTAX-KEYREF
  - MT-SCHEMA-FRONTMATTER
version: 0.2.4
date-created: "2025-05-19T00:00:00Z"
date-modified: "2025-05-30T00:00:00Z"
scope_application: "Global key definitions for use across all knowledge bases to ensure content consistency and support automation."
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas: ["Content consistency", "Automation", "Branding", "Link management"]
change_log_url: ./UA-KEYDEFS-GLOBAL-changelog.md
keys:
  productName: Knowledge Base System X
  productVersionMajor: "1"
  productVersionMinor: "0"
  productVersionPatch: "0"
  productReleaseName: Orion
  officialCompanyName: Ehsan Solutions Inc.
  companyWebsiteUrl: https://www.example.com
  mainDocsUrl: "[[AS-INDEX-KB-MASTER]]"
  supportPageUrl: https://support.example.com
  apiReferenceUrl: "[[AS-SCHEMA-REFERENCE]]"
  betaFeatureDisclaimer: This feature is currently in beta and subject to change.
  confidentialityNotice: This document contains confidential information.
  defaultStatusDraft: status/draft
  defaultKbIdStandards: kb-id/standards
  defaultKbIdCookbook: kb-id/llm-cookbook
---

# Key Definitions (`_key_definitions.md`)

This file serves as the central repository for all globally reusable key-value pairs (keyrefs) used throughout the `master-knowledge-base` and its rendered outputs. It adheres to standard [[MT-KEYREF-MANAGEMENT]].

## Purpose

-   To ensure consistency in terminology, product names, URLs, standard phrases, and other frequently used snippets.
-   To provide a single source of truth for these values, simplifying updates and maintenance.
-   To be consumed by the "Resolver Script" which populates placeholders (e.g., `{{key.productName}}`) in source documents to create rendered documents.
-   To provide context to LLMs for content generation and modification tasks.

## Structure

All keys are defined within the YAML frontmatter of this document, under the `keys:` dictionary. See [[MT-KEYREF-MANAGEMENT]] for structural rules.

## Categories of Keys (Examples)

*(This section documents the types of keys defined in the YAML frontmatter for human understanding)*

### Product Related Keys
-   `productName`: The official name of the primary product.
-   `productVersionMajor`, `productVersionMinor`, `productVersionPatch`: Components of the product version.
-   `productReleaseName`: Codename for the current product release.

### Company/Organization Keys
-   `officialCompanyName`: The full legal name of the company/organization.
-   `companyWebsiteUrl`: The main URL for the company/organization.

### Common URLs
-   `mainDocsUrl`: Link to the main entry point of the documentation.
-   `supportPageUrl`: Link to the primary support page.
-   `apiReferenceUrl`: Link to the main API reference documentation.

### Standard Phrases / Disclaimers
-   `betaFeatureDisclaimer`: Standard text for beta features.
-   `confidentialityNotice`: Standard confidentiality notice.

### Default Values / System Tags
-   `defaultStatusDraft`: Default tag for new draft documents.
-   `defaultKbIdStandards`: Default `kb-id` tag for the Standards KB.
-   `defaultKbIdCookbook`: Default `kb-id` tag for the LLM Cookbook KB.

## Usage

In source Markdown documents, use the syntax `{{key.keyName}}` (defined in [[SF-SYNTAX-KEYREF]]) to insert the value of a key. For example, `{{key.productName}}` will be replaced by "Knowledge Base System X" (or its current value) in the rendered output.

## Maintenance

-   When adding, modifying, or removing keys, ensure this document is updated.
-   After any change to the `keys:` in the YAML frontmatter, the "Resolver Script" MUST be re-run to update all rendered documents across the `master-knowledge-base-rendered/` directory.