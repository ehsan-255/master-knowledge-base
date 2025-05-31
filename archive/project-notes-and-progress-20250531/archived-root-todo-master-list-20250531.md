---
title: 'Master TODO List'
aliases: ['KB TODOs', 'Project Tasks']
tags:
  - kb-id/global
  - content-type/utility-document 
  - status/live 
  - topic/project-management
kb-id: global
info-type: todo-master-list 
primary-topic: 'A centralized list for tracking pending tasks, issues, and planned enhancements for the knowledge base system and its standards.'
related-standards: ['M-SYNTAX-TODO-001']
version: '0.1.0'
date-created: '2025-05-22'
date-modified: '2025-05-22'
---

# Master TODO List

This document tracks all major pending tasks, issues, and planned enhancements for the knowledge base system. In-document TODOs (using `<!-- TODO ... -->` comments) should be periodically summarized or referenced here for broader visibility and prioritization.

## Categories

### Standards Development & Refinement
-   Priority: High | Status: Pending | Assignee: Jim | Task: Vault-Wide Enforcement of Quoted `version` Strings.
    -   *Details: Systematically update all `.md` files to ensure `version` key values are quoted strings. Scripting deferred; manual/semi-manual updates can proceed.*
    -   *Source: General requirement from previous reviews.*

### Content Population & Completion
-   Priority: Medium | Status: Pending | Assignee: Ehsan/Jim | Task: Further Populate LLM Cookbook with 10 core recipes.
    -   *Details: Draft content for the 10 recipes identified in planning phase.*
    -   *Source: Planning document.*

### Automation Design & Foundation (No Scripting Yet)
-   Priority: High | Status: Pending | Assignee: Jim | Task: Foundational Design for Resolver Script.
    -   *Details: Document WHAT, WHY, HOW (conceptual) for the resolver script.*
    -   *Source: Planning document.*
-   Priority: High | Status: Pending | Assignee: Jim | Task: Foundational Design for Automated Validation/Linting.
    -   *Details: Document WHAT, WHY, HOW (conceptual) for the validation/linting system.*
    -   *Source: Planning document.*
-   Priority: Medium | Status: Pending | Assignee: Jim | Task: Foundational Design for `kb-directory.md` Generation.
    -   *Details: Document WHAT, WHY, HOW (conceptual) for `kb-directory.md` automation.*
    -   *Source: Planning document.*
-   Priority: Medium | Status: Pending | Assignee: Jim | Task: Foundational Design for `tag-glossary.md` Automation.
    -   *Details: Document WHAT, WHY, HOW (conceptual) for `tag-glossary.md` management assistance.*
    -   *Source: Planning document.*
-   Priority: Medium | Status: Pending | Assignee: Jim | Task: Foundational Design for `generate_slug` refinement in link converter.
    -   *Details: Document WHAT, WHY, HOW (conceptual) for improving slug generation logic.*
    -   *Source: Planning document.*

### Deferred Tasks (Explicitly Not In Current Scope)
-   Task: Rework `assemble-monolith.py` Script.
-   Task: Update `update_frontmatter.py` Script.
-   Task: Update `resolver_script.py` `ACTIVE_PROFILE` (beyond initial conceptual design for configurability).
-   Task: Document Scripts in `scripts/docs/` (beyond initial file creation).
-   Task: Populate placeholder content in `scripts/docs/GUIDE-ASSEMBLY-SCRIPT-RUN.md` and `scripts/docs/DOC-ASSEMBLY-SCRIPT-LOGIC.md`.

*(Add more tasks here as they are identified from in-document TODOs or planning sessions.)* 