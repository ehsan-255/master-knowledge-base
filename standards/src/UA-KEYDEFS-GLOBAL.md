---
title: Global Key Definitions Set
standard_id: UA-KEYDEFS-GLOBAL
aliases:
- Key Definitions
- Global Keys
- Keyref Definitions
tags:
- content-type/key-definition-set
- criticality/p0-critical
- kb-id/global
- kb-id/standards
- status/active
- topic/keydefs
- topic/keyrefs
- topic/structured-data
- topic/ua
kb-id: standards
info-type: key-definition-set
primary-topic: Defines the centrally managed set of global keys and their corresponding
  text expansions for use with the keyref system across all knowledge bases.
related-standards:
- MT-KEYREF-MANAGEMENT
- SF-SYNTAX-KEYREF
- GM-REGISTRY-GOVERNANCE
version: 1.0.0
date-created: '2025-05-29T16:04:35Z'
date-modified: '2025-06-17T06:50:00Z'
primary_domain: UA
sub_domain: KEYDEFS
scope_application: Applies to all knowledge bases and documents utilizing key-based
  references (keyrefs) for content reuse and standardization.
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Content reuse
- Maintainability
- Consistency
- Reducing redundancy
- Single-sourcing of terms
change_log_url: 'standards/changelog.md'
keys:
  # Repository Structure Keys
  master-kb-root: "master-knowledge-base"
  standards-dir: "standards/src"
  registry-dir: "standards/registry"
  templates-dir: "standards/templates"
  tools-dir: "tools"
  reports-dir: "tools/reports"
  archive-dir: "archive"
  
  # Change Log Management
  change-log-url: "standards/changelog.md"
  
  # Primary Topics (Common Placeholders)
  primary-topic-standards: "Standards infrastructure and governance"
  primary-topic-metadata: "Document metadata and frontmatter management"
  primary-topic-syntax: "Markdown syntax and formatting standards"
  primary-topic-content: "Content authoring policies and guidelines"
  
  # Scope Applications (Common Values)
  scope-universal: "Applies universally to all knowledge bases and documents"
  scope-standards-kb: "Applies specifically to the Standards Knowledge Base"
  scope-metadata: "Applies to all documents with YAML frontmatter metadata"
  scope-markdown: "Applies to all Markdown documents"
  
  # Common File Paths
  frontmatter-schema: "standards/src/MT-SCHEMA-FRONTMATTER.md"
  kb-usage-guide: "standards/src/GM-GUIDE-KB-USAGE.md"
  naming-conventions: "standards/src/GM-CONVENTIONS-NAMING.md"
  
  # Organization Information
  kb-system-name: "Master Knowledge Base System"
  kb-system-short: "Master Knowledge Base"
  
  # Technical Configuration
  yaml-schema-version: "1.2"
  markdown-flavor: "GitHub Flavored Markdown (GFM)"
  
  # Common Status Values
  status-active: "active"
  status-draft: "draft"
  status-deprecated: "deprecated"
  status-archived: "archived"
  
  # Criticality Levels
  criticality-p0: "P0-Critical"
  criticality-p1: "P1-High"
  criticality-p2: "P2-Medium"
  criticality-p3: "P3-Low"
  
  # Common Domain Prefixes
  domain-as: "Architecture and Structure"
  domain-cs: "Content Style and Policies"
  domain-gm: "General Management"
  domain-mt: "Metadata and Tagging"
  domain-om: "Operational Management"
  domain-qm: "Quality and Validation"
  domain-sf: "Syntax and Formatting"
  domain-ua: "Utilities and Assets"
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

### 3.1. Naming Conventions for Keys
- Keys MUST be descriptive and use lowercase letters, numbers, and hyphens (kebab-case).
- Avoid overly generic names to prevent conflicts. Consider prefixing with a relevant domain if applicable (e.g., `change-log-url` vs. just `url`).
- Keys for common placeholders MUST follow the pattern `missing-{purpose}` for replacement values.

### 3.2. Key Categories

The global keys are organized into the following categories:
- **Repository Structure**: Common directory paths and structure references
- **Change Log Management**: URLs and references for change tracking
- **Primary Topics**: Standard topic descriptions for common use cases
- **Scope Applications**: Standard scope descriptions for different contexts
- **File Paths**: Common file references used across standards
- **Organization Information**: System and organization identifiers
- **Technical Configuration**: Version numbers and technical specifications
- **Status Values**: Standard status lifecycle values
- **Criticality Levels**: Standard criticality classifications
- **Domain Descriptions**: Human-readable descriptions for domain codes

## 4. Adding or Modifying Keys

Proposals for adding new keys or modifying existing key values MUST follow the governance process outlined in `[[MT-KEYREF-MANAGEMENT]]` and `[[GM-REGISTRY-GOVERNANCE]]`. This typically involves a review and approval process to ensure keys are necessary, well-defined, and do not conflict.

## 5. Usage in Documents

To use a key in a Markdown document, insert the keyref using the syntax `{{key.your-key-name}}`, as defined in `[[SF-SYNTAX-KEYREF]]`. The build/rendering process will replace this placeholder with the corresponding text from this document's frontmatter.

## 6. Scope of Application

These global key definitions are intended for use across all knowledge bases and documents within the ecosystem that support the keyref mechanism.
