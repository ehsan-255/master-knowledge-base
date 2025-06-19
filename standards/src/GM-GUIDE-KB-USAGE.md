---
title: 'Guide: Knowledge Base Usage and Standards'
standard_id: GM-GUIDE-KB-USAGE
aliases:
- KB Onboarding Guide
- How to Use This KB
- KB Usage Guide
tags:
- content-type/guide-document
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/content-authoring
- topic/gm
- topic/guide
- topic/knowledge-management
- topic/onboarding
- topic/standards-governance
- topic/user-documentation
kb-id: standards
info-type: guide-document
primary-topic: Quick-start guide for users on how to navigate, understand, apply,
  and contribute to the knowledge base system and its standards.
related-standards:
- AS-ROOT-STANDARDS-KB
- AS-STRUCTURE-DOC-CHAPTER
- MT-SCHEMA-FRONTMATTER
- GM-CONVENTIONS-NAMING
- AS-STRUCTURE-TEMPLATES-DIRECTORY
version: 0.2.0
date-created: '2025-05-29T11:51:19Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: GM
sub_domain: GUIDE
scope_application: Provides quick-start guidance for all users and contributors on
  utilizing the knowledge base and its standards.
criticality: P1-High
lifecycle_gatekeeper: Editorial-Board-Approval
impact_areas:
- User Onboarding
- Standards Adoption
- KB Navigation
- Contribution Process
---
# Guide: Knowledge Base Usage and Standards

Quick-start guide for navigating, understanding, and contributing to this knowledge base (KB) system and its standards.

## 1. Getting Started

### 1.1 Navigation Entry Points
- **Standards KB Root:** Start at [[AS-ROOT-STANDARDS-KB]] for master table of contents
- **Task-Based Guide:** TODO: Create new task-oriented navigation system to replace archived GM-GUIDE-STANDARDS-BY-TASK
- **Search:** Use your editor's search to find standards by ID or keywords

### 1.2 KB Structure Overview
- **Source Documents:** All content is authored in source files with placeholders and metadata
- **Standards Organization:** Standards are organized by domain (AS, CS, GM, MT, OM, QM, SF, UA)
- **Templates:** Available at `standards/templates/` for consistent document creation

## 2. Core Authoring Workflow

### 2.1 Creating New Documents
1. **Use Templates:** Copy from [[AS-STRUCTURE-TEMPLATES-DIRECTORY]] at `standards/templates/`
2. **File Naming:** Follow [[GM-CONVENTIONS-NAMING]] (lowercase kebab-case)
3. **Document Structure:** Apply [[AS-STRUCTURE-DOC-CHAPTER]] (H1, abstract, ToC, sections, summary)

### 2.2 Essential Frontmatter
All documents MUST include canonical YAML frontmatter per [[MT-SCHEMA-FRONTMATTER]]:
- `title` (matches H1)
- `tags` (including `status/draft`, `content-type/*`, `topic/*`)
- `kb-id` (identifies knowledge base)
- `info-type` (processing instruction)
- `version`, `date-created`, `date-modified`

### 2.3 Critical Tags
- **Status:** `status/draft` → `status/active` → `status/deprecated`
- **Content Type:** `content-type/standard-document`, `content-type/guide-document`, etc.
- **Topics:** At least one `topic/*` tag (e.g., `topic/onboarding`)

## 3. Key Standards Reference

### 3.1 Document Structure
- [[AS-STRUCTURE-DOC-CHAPTER]] - Core document structure requirements
- [[AS-ROOT-STANDARDS-KB]] - Standards KB navigation hub
- [[GM-CONVENTIONS-NAMING]] - File and folder naming rules

### 3.2 Content and Syntax
- [[MT-SCHEMA-FRONTMATTER]] - Complete frontmatter schema
- [[SF-SYNTAX-HEADINGS]] - Heading syntax requirements
- [[SF-LINKS-INTERNAL-SYNTAX]] - Internal linking standards

### 3.3 Governance and Quality
- [[OM-POLICY-STANDARDS-GOVERNANCE]] - Standards change process
- [[OM-VERSIONING-CHANGELOGS]] - Version control requirements
- [[GM-GLOSSARY-STANDARDS-TERMS]] - Standards terminology

## 4. Quick Reference

### 4.1 Essential Actions
- **Before Publishing:** Ensure `status/draft` → `status/active` transition
- **Link Standards:** Use `[[STANDARD_ID]]` format for standard references
- **Version Updates:** Increment version number for significant changes
- **Date Updates:** Update `date-modified` when making changes

### 4.2 Common Patterns
- **Standard References:** `[[STANDARD_ID|Display Text]]`
- **Section Links:** `[[STANDARD_ID#Section Title]]`
- **Task Guidance:** TODO: Develop new workflow-specific standards navigation system

---
*This quick-start guide replaces the comprehensive tutorial format. For detailed guidance, consult individual standards referenced above.*
