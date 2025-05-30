---
title: "Master Knowledge Base Index"
standard_id: "AS-INDEX-KB-MASTER" # This is the ID of this specific index document
aliases: ["KB Directory", "Knowledge Base Master List", "Index of KBs"]
tags: ["status/live", "criticality/P0-Critical", "content-type/navigation-document", "topic/indexing", "topic/architecture", "kb-master-index"]
kb-id: "kb-id/global" # This file is global, indexing multiple KBs
info-type: "navigation-document"
primary-topic: "Provides a master directory and entry points to all active Knowledge Bases (KBs) within the ecosystem."
related-standards: ["AS-STRUCTURE-MASTER-KB-INDEX", "AS-ROOT-STANDARDS-KB"] # Links to the standard defining this type of file, and the root of the standards KB.
version: "1.0.0" # Initial version
date-created: "2025-05-29T16:10:25Z"
date-modified: "2025-05-30T00:00:00Z" # Updated to current date
primary_domain: "AS"
sub_domain: "INDEXING" # Changed from STRUCTURE
scope_application: "Serves as the primary navigational entry point to all distinct Knowledge Bases."
criticality: "P0-Critical" # Essential for navigating the entire KB ecosystem.
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["KB navigation", "Content discoverability", "User orientation", "Onboarding"]
change_log_url: "./AS-INDEX-KB-MASTER-changelog.md" # Assuming changelog is in the same directory
---

# Master Knowledge Base Index

This document provides a centralized directory to all active Knowledge Bases (KBs) within this ecosystem. For the standard defining how this index file should be structured, see `[[AS-STRUCTURE-MASTER-KB-INDEX]]`.

## Available Knowledge Bases

Below is a list of currently available Knowledge Bases. Each KB is a self-contained unit focused on a specific domain or purpose.

1.  **Standards Knowledge Base**
    *   **Description:** Contains all standards, policies, guidelines, and supporting documentation for creating, managing, and governing content within the entire knowledge ecosystem. This is the meta-KB that defines how other KBs operate.
    *   **Entry Point:** `[[AS-ROOT-STANDARDS-KB]]`
    *   **Primary Folder:** `/master-knowledge-base/standards/`

2.  **LLM Content Generation Cookbook KB**
    *   **Description:** Provides practical recipes, prompt templates, and best practices for using Large Language Models (LLMs) to assist with content creation, analysis, and other knowledge work.
    *   **Entry Point:** `[[TODO-LLM-COOKBOOK-ROOT-ID]]` (Link to the root file of the LLM Cookbook KB once its ID is known or it's created)
    *   **Primary Folder:** `/master-knowledge-base/llm-content-generation-cookbook/` (Assumed path)

3.  **Research Methodology KB**
    *   **Description:** Focuses on research design, data collection, analysis, and open science practices for generating complex workflows.
    *   **Entry Point:** `[[TODO-RESEARCH-METHODOLOGY-ROOT-ID]]` (Link to the root file of the Research Methodology KB once its ID is known or it's created)
    *   **Primary Folder:** `/master-knowledge-base/research-methodology-kb/` (Assumed path)

> [!TODO] This index needs to be kept up-to-date as new Knowledge Bases are added or existing ones are retired. Links to the entry points (`root.md` or equivalent `AS-ROOT-*-KB.md` files) of each KB must be accurate. Placeholder links like `[[TODO-LLM-COOKBOOK-ROOT-ID]]` need to be resolved.

---
This master index is crucial for navigating the multi-KB environment.
