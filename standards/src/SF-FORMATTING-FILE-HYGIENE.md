---

title: 'Standard: File Hygiene and Formatting'
standard_id: SF-FORMATTING-FILE-HYGIENE
aliases:
- File Formatting Standard
- Line Endings
- UTF-8 Encoding Standard
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p2-medium
- kb-id/standards
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: File Hygiene and Line Endings
related-standards:
- MT-SCHEMA-FRONTMATTER
- SF-FORMATTING-MARKDOWN-GENERAL
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-06-18T03:15:00Z'
primary_domain: SF
sub_domain: FORMATTING
scope_application: All text-based files within the knowledge base repository.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Version control consistency
- Cross-platform compatibility
- File integrity
- Automated processing
---
# Standard: File Hygiene and Formatting (SF-FORMATTING-FILE-HYGIENE)

## 1. Standard Statement

This standard **MANDATES** file hygiene and formatting rules for all text-based files within the Knowledge Base repository.

## 2. Core File Hygiene Rules

### Rule 2.1: UTF-8 Encoding
All text-based files **MUST** use **UTF-8 encoding**.
*   **Byte Order Mark (BOM):** **MUST NOT** be used at the beginning of files.

### Rule 2.2: Line Feed (LF) Line Endings
All text-based files **MUST** use **Line Feed (LF) line endings (Unix-style)**.
*   **Prohibited:** Carriage Return Line Feed (CRLF) or Carriage Return (CR) line endings.

### Rule 2.3: No Trailing Whitespace
Trailing whitespace (spaces or tabs) at the end of any line **MUST** be removed.

### Rule 2.4: Single Newline at End-Of-File (EOF)
All text-based files **MUST** end with a single newline character.
*   **Guidance:** The last line should have a line ending character, without multiple blank lines at file end.

## 3. Scope of Application

This standard applies to **ALL** text-based files in the Knowledge Base repository, including:
*   Markdown files (`.md`)
*   YAML files (`.yaml`)
*   JSON files (`.json`)
*   Python scripts (`.py`)
*   Shell scripts (`.sh`, `.bash`)
*   Configuration files (`.gitignore`, `.editorconfig`)

Binary files (images, PDFs) are exempt from these rules.

## 4. Tooling and Enforcement

Text editors and IDEs **SHOULD** be configured to automatically enforce these rules. Project-level configuration files (`.editorconfig`) and automated linters **MAY** be used for compliance checking.

## 5. Cross-References
- [[MT-SCHEMA-FRONTMATTER]]
- [[SF-FORMATTING-MARKDOWN-GENERAL]]

---
*This standard (SF-FORMATTING-FILE-HYGIENE) establishes mandatory file hygiene requirements, ensuring consistency and compatibility across the Knowledge Base.*
```
