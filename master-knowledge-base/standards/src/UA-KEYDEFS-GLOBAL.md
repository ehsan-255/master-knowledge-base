---
title: Global Key Definitions Set
standard_id: UA-KEYDEFS-GLOBAL
aliases:
- Key Definitions
- Global Keys
- Keyref Definitions
tags:
- status/draft
- criticality/p0-critical
- content-type/key-definition-set
- topic/keyrefs
- topic/structured-data
- kb-id/global
- kb-id/standards
kb-id: standards
info-type: key-definition-set
primary-topic: Defines the centrally managed set of global keys and their corresponding text expansions for use with the keyref system across all knowledge bases.
related-standards:
- MT-KEYREF-MANAGEMENT
- SF-SYNTAX-KEYREF
- GM-REGISTRY-GOVERNANCE
version: 0.1.0
date-created: '2025-05-29T16:04:35Z'
date-modified: '2025-05-30T16:00:00Z'
primary_domain: UA
sub_domain: KEYDEFS
scope_application: Applies to all knowledge bases and documents utilizing key-based references (keyrefs) for content reuse and standardization.
criticality: p0-critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content reuse
- Maintainability
- Consistency
- Reducing redundancy
- Single-sourcing of terms
change_log_url: ./UA-KEYDEFS-GLOBAL-changelog.md
keys:
  placeholder-key: This is an example placeholder value. Replace with actual keys.
  product-name-alpha: Project AlphaX
  company-name-full: Global Knowledge Systems Inc.
  support-email: support@globalknowledge.example.com
---
# Global Key Definitions Set (UA-KEYDEFS-GLOBAL)

## 1. Standard Statement

This document serves as the central, authoritative registry for all global key definitions used by the key-based reference (keyref) system. Keyrefs (`{{key.name}}`) allow for consistent reuse of common terms, phrases, URLs, or other text snippets across all knowledge base documents.

The management and governance of these key definitions are outlined in `[[MT-KEYREF-MANAGEMENT]]`. The syntax for using keyrefs in Markdown documents is defined in `[[SF-SYNTAX-KEYREF]]`.

## 2. Purpose

The purpose of this global key definition set is to:
-   Ensure consistency for frequently used terms and phrases.
-   Simplify updates: change a term once in this file, and it updates everywhere it's referenced.
-   Reduce errors from manual typing or copy-pasting.
-   Promote single-sourcing of critical information snippets.

## 3. Key Definitions

The actual key definitions are stored within the YAML frontmatter of *this* document, under the `keys:` dictionary. Each entry in the `keys:` dictionary consists of a key name (e.g., `product-name-official`) and its corresponding text expansion (value).

**Example Structure in Frontmatter:**
```yaml
keys:
  key-name-1: "Text expansion for key 1."
  key-name-2: "Another piece of text for key 2. Can include spaces and punctuation."
  contact-phone: "+1-800-555-0123"
```

> [!TODO] The initial set of keys needs to be populated based on common terms and phrases identified across the knowledge bases. This document currently contains placeholder examples in its frontmatter. These should be replaced with actual, agreed-upon global keys.

### 3.1. Naming Conventions for Keys
- Keys SHOULD be descriptive and use lowercase letters, numbers, and hyphens (kebab-case).
- Avoid overly generic names to prevent conflicts. Consider prefixing with a relevant domain if applicable (e.g., `support-contact-email` vs. just `email`).

## 4. Adding or Modifying Keys

Proposals for adding new keys or modifying existing key values MUST follow the governance process outlined in `[[MT-KEYREF-MANAGEMENT]]` and `[[GM-REGISTRY-GOVERNANCE]]`. This typically involves a review and approval process to ensure keys are necessary, well-defined, and do not conflict.

## 5. Usage in Documents

To use a key in a Markdown document, insert the keyref using the syntax `{{key.your-key-name}}`, as defined in `[[SF-SYNTAX-KEYREF]]`. The build/rendering process will replace this placeholder with the corresponding text from this document's frontmatter.

## 6. Scope of Application

These global key definitions are intended for use across all knowledge bases and documents within the ecosystem that support the keyref mechanism.
