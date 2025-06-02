---
title: 'Standard: File Hygiene and Formatting'
standard_id: SF-FORMATTING-FILE-HYGIENE
aliases:
  - File Formatting Standard
  - Line Endings
  - UTF-8 Encoding Standard
tags:
  - status/draft
  - criticality/p2-medium
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: File Hygiene and Line Endings
related-standards:
  - '[[MT-SCHEMA-FRONTMATTER]]'
version: 1.0.0
date-created: '2024-07-15T12:00:00Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: All text-based files within the knowledge base repository, especially
  Markdown (.md), YAML (.yaml), JSON (.json), and script files (.py, .sh, etc.).
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Version control consistency
  - Cross-platform compatibility
  - File integrity
  - Readability
  - Automated processing
change_log_url: ./changelog.md
---

# Standard: File Hygiene and Formatting (SF-FORMATTING-FILE-HYGIENE)

## 1. Standard Statement

This standard defines mandatory file hygiene and formatting rules for all text-based files within the knowledge base repository. Adherence to these rules is crucial for ensuring consistency in version control systems, promoting cross-platform compatibility, maintaining file integrity, enhancing readability, and supporting reliable automated processing.

## 2. Core File Hygiene Rules

### Rule 2.1: UTF-8 Encoding (Consistent with [[MT-SCHEMA-FRONTMATTER]])
All text-based files (e.g., `.md`, `.yaml`, `.json`, `.py`) MUST use **UTF-8 (Unicode Transformation Format—8-bit) encoding**.
*   **Byte Order Mark (BOM):** A Byte Order Mark (BOM) MUST NOT be used at the beginning of files.
*   **Rationale:** UTF-8 is a universal character encoding standard that supports a wide range of characters and symbols, ensuring broad compatibility. Avoiding BOM prevents potential issues with some tools and parsers, particularly in Unix-like environments. This rule aligns with the frontmatter encoding specified in [[MT-SCHEMA-FRONTMATTER]].

### Rule 2.2: Line Feed (LF) Line Endings (Derived from U-FILEHYGIENE-001, Rule 1.1)
All text-based files MUST use **Line Feed (LF) line endings (Unix-style)**.
*   **Prohibition:** Carriage Return Line Feed (CRLF) line endings (Windows-style) or Carriage Return (CR) line endings (classic Mac-style) are NOT permitted.
*   **Rationale:** Consistent line endings prevent common issues in version control systems (like Git incorrectly reporting entire files as changed), ensure cross-platform compatibility, and simplify text processing by scripts and tools. Most modern text editors can be configured to enforce LF line endings.

### Rule 2.3: No Trailing Whitespace (Derived from U-FILEHYGIENE-001, Rule 1.2)
Trailing whitespace (spaces or tabs) at the end of any line of text MUST be removed.
*   **Rationale:** Trailing whitespace can cause inconsistencies in diffs, create visual clutter, and sometimes interfere with the behavior of scripts or parsers. Many text editors can be configured to automatically remove trailing whitespace upon saving.

### Rule 2.4: Single Newline at End-Of-File (EOF) (Derived from U-FILEHYGIENE-001, Rule 1.3)
All text-based files MUST end with a single newline character.
*   **Guidance:** This means the last line of the file should have a line ending character, and there should not be multiple blank lines at the very end of the file.
*   **Rationale:** This is a POSIX standard and is expected by many command-line tools and text processing utilities. It ensures that files can be concatenated or processed correctly and prevents some tools from indicating a "missing newline" warning or diff.

## 3. Importance of File Hygiene

Maintaining consistent file hygiene offers several benefits:

*   **Version Control System (VCS) Integrity:** Prevents spurious changes in diffs caused by line ending or whitespace differences, making commit histories cleaner and reviews more focused.
*   **Cross-Platform Compatibility:** Ensures files can be opened and edited consistently across different operating systems (Windows, macOS, Linux).
*   **Improved Readability:** Eliminates distracting visual inconsistencies caused by mixed line endings or unnecessary whitespace.
*   **Reliable Automation:** Scripts and automated tools for parsing, linting, or building content are less likely to fail or produce unexpected results due to inconsistent formatting.
*   **Professionalism:** Adherence to these conventions reflects a professional approach to content and code management.

## 4. Scope of Application

This standard applies to all text-based files committed to the knowledge base repository, with a particular emphasis on:
*   Markdown files (`.md`)
*   YAML files (`.yaml`)
*   JSON files (`.json`)
*   Python scripts (`.py`)
*   Shell scripts (`.sh`, `.bash`)
*   Other configuration or text files (e.g., `.gitignore`, `.editorconfig`)

Binary files (e.g., images, PDFs) are exempt from these specific rules (though their naming conventions are covered elsewhere).

## 5. Tooling and Enforcement

It is highly recommended to configure text editors and Integrated Development Environments (IDEs) to automatically enforce these file hygiene rules (e.g., by setting default line endings to LF, removing trailing whitespace on save, ensuring a final newline). Project-level configuration files like `.editorconfig` can also be used to help standardize these settings across different editors. Automated linters or pre-commit hooks may also be employed to check for and enforce compliance.

## 6. Cross-References
- [[MT-SCHEMA-FRONTMATTER]] - For specific encoding rules related to YAML frontmatter.

---
*This standard (SF-FORMATTING-FILE-HYGIENE) is based on rules 1.1 through 1.3 previously defined in U-FILEHYGIENE-001 from COL-GOVERNANCE-UNIVERSAL.md, and incorporates a general UTF-8 encoding rule.*
```
