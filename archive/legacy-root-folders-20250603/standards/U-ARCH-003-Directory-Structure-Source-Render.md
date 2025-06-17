---
title: 'Standard: Directory Structure for Source and Rendered Content (U-ARCH-003)
  - DEPRECATED'
tags:
- architecture
- content-type/standard-document
- criticality/p0-critical
- file-system
- kb-id/global
- kb-id/standards
- source-and-render
- standards-kb/universal
- status/deprecated
date-created: 2025-05-19
date-modified: '2025-06-17T02:29:13Z'
version: 0.2.0
info-type: standard-document
primary-topic: Defines the directory structure for managing source and rendered knowledge
  base content.
related-standards:
- U-ARCH-001
- U-ARCH-002
aliases:
- Source-Render Directory Standard
kb-id: archive
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
**DEPRECATED:** This document is superseded. Concepts integrated into [[AS-KB-DIRECTORY-STRUCTURE]] and other architectural standards..

# Standard: Directory Structure for Source and Rendered Content (U-ARCH-003)

This document defines the standard directory structure for managing the "source" (editable, with placeholders) and "rendered" (consumable, fully populated) versions of the knowledge base content, in line with the "source-and-render" operational model.

## Table of Contents
- [[#Standard: Directory Organization (U-ARCH-003)]]

## Standard: Directory Organization (U-ARCH-003)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-ARCH-003`                          |
| Standard Name   | Directory Structure for Source and Rendered Content |
| Standard Category | Overall Knowledge Base Architecture   |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | The primary editable content, containing placeholders (e.g., keyrefs, conditional text markers), MUST reside within the `master-knowledge-base/` directory and its subdirectories. This is the "source" vault. | `master-knowledge-base/Standards/U-ARCH-001.md`              | All authoring and direct modifications occur here.                           |
| 1.2    | A parallel directory named `master-knowledge-base-rendered/` MUST exist at the same level as `master-knowledge-base/`. This directory will store the "rendered" or "consumable" versions of the content. | `../master-knowledge-base-rendered/` (relative to a file inside `master-knowledge-base`) | This directory is populated by the "Resolver Script".                        |
| 1.3    | The internal folder and file structure within `master-knowledge-base-rendered/` MUST mirror the structure of `master-knowledge-base/` exactly. | If source is `master-knowledge-base/KB1/fileA.md`, rendered is `master-knowledge-base-rendered/KB1/fileA.md`. | Ensures consistent paths between source and rendered versions.               |
| 1.4    | Files within `master-knowledge-base-rendered/` are considered build artifacts. They SHOULD NOT be edited directly. All edits MUST occur in the corresponding source files within `master-knowledge-base/`. | N/A                                                          | Edits to rendered files will be overwritten by the Resolver Script.          |
| 1.5    | Both `master-knowledge-base/` and `master-knowledge-base-rendered/` directories MUST be under version control (Git).                            | `git add master-knowledge-base/ master-knowledge-base-rendered/` | Allows tracking of both source and the history of its rendered states.       |
| 1.6    | The "Resolver Script" is responsible for reading from `master-knowledge-base/` and writing to `master-knowledge-base-rendered/`.                 | N/A                                                          | The script ensures synchronization.                                          |

**Cross-References to Other Standard IDs:** [[root#III. Core Operational Model: Source-and-Render|Core Operational Model: Source-and-Render]], [[COL-ARCH-UNIVERSAL#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)|U-ARCH-001]], [[COL-ARCH-UNIVERSAL#Standard: Master KB Directory and Unique KB Identification (U-ARCH-002)|U-ARCH-002]]
