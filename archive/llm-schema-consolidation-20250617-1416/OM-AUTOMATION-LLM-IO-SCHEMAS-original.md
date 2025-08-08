---
title: 'Standard: LLM Automation Input/Output Schemas'
standard_id: OM-AUTOMATION-LLM-IO-SCHEMAS
aliases:
- LLM IO Schemas
- LLM Automation Schemas
tags:
- content-type/standard-definition
- criticality/p2-medium
- kb-id/standards
- status/draft
- topic/automation
- topic/llm-integration
- topic/om
- topic/schemas
kb-id: standards
info-type: standard-definition
primary-topic: LLM Automation I/O Schemas
related-standards:
- '[[OM-AUTOMATION-LLM-PROMPT-LIBRARY]]'
version: 0.1.2
date-created: '2025-05-19T00:00:00Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: OM
sub_domain: AUTOMATION
scope_application: Defines the standard for creating, documenting, and managing JSON
  schemas used for LLM input/output in automated workflows.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- LLM automation
- Data interchange
- Schema validation
- Workflow integration
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: LLM Automation Input/Output Schemas

This document defines the standard for creating, documenting, and managing JSON schemas used for structured input to and output from Large Language Models (LLMs) in automated knowledge base workflows.

## Table of Contents
- [[#Standard: Definition, Documentation, and Management of LLM I/O Schemas (LLM-AUTOMATION-IO-SCHEMA-001)]]
- [[#Schema Repository and Naming]]
- [[#Example Schema Structure (Conceptual)]]

## Standard: Definition, Documentation, and Management of LLM I/O Schemas (LLM-AUTOMATION-IO-SCHEMA-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `LLM-AUTOMATION-IO-SCHEMA-001`        |
| Standard Name   | LLM Automation Input/Output Schemas   |
| Standard Category | LLM Integration & Automation          |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | For every distinct automated task involving an LLM, separate JSON schemas MUST be defined for the expected input structure provided to the LLM and the expected output structure received from the LLM. | Task: "Draft New Topic". Input Schema: `draft_topic_input.json_schema`. Output Schema: `draft_topic_output.json_schema`. | Ensures clarity and predictability of LLM interactions.                      |
| 1.2    | All LLM I/O schemas MUST be documented. This documentation SHOULD include the schema's purpose, a description of each field, data types, and whether fields are required or optional. | A Markdown file per schema, or a central schema dictionary.  | Documentation is crucial for understanding and maintaining the automation.   |
| 1.3    | Schemas MUST use standard JSON Schema syntax and conventions.                                                                                   | `{ "type": "object", "properties": { ... } }`                | Promotes interoperability and use of standard validation tools.              |
| 1.4    | Schemas SHOULD be versioned. Changes to a schema that are not backward-compatible MUST result in a new version of the schema.                   | `draft_topic_input_v1.0.json_schema`, `draft_topic_input_v1.1.json_schema` | Manages evolution and impact on dependent prompts and scripts.             |
| 1.5    | Input schemas for LLMs SHOULD include fields for: `task_id` (unique identifier for the specific job), `contextual_information` (e.g., relevant existing KB content, key definitions), and `task_specific_parameters`. | See Conceptual Example.                                      | Provides necessary context for the LLM.                                      |
| 1.6    | Output schemas from LLMs SHOULD include fields for: `status` (e.g., success, failure_with_reason), `llm_response_data` (the structured payload), and `confidence_score` (if applicable/obtainable). | See Conceptual Example.                                      | Facilitates programmatic handling of LLM responses.                          |
| 1.7    | The `LLM-PROMPT-LIBRARY-001` standard MUST reference the specific version of the input and output schemas that a prompt template is designed for. | Prompt `P-DRAFT-TOPIC-001` uses input schema `draft_topic_input_v1.0` and expects output schema `draft_topic_output_v1.0`. | Ensures alignment between prompts and data structures.                       |

## Schema Repository and Naming

-   A dedicated directory, e.g., `master-knowledge-base/llm-io/llm-io-schemas/`, SHOULD be used to store all JSON schema definition files (`.json_schema` or `.json`).
-   Schema file names SHOULD clearly indicate the task and whether it's an input or output schema, including version (e.g., `task_createContent_input_v1.json`).

## Example Schema Structure (Conceptual)

**Conceptual Input Schema (`llm-io/llm-io-schemas/task_example_input_v1.json_schema`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Example LLM Task Input",
  "description": "Schema for input to an example LLM task.",
  "type": "object",
  "properties": {
    "taskId": { "type": "string", "description": "Unique ID for this task instance." },
    "taskName": { "type": "string", "enum": ["createTopic", "summarizeText", "suggestMetadata"] },
    "sourceContent": { "type": "string", "description": "Main text content to process." },
    "keyDefinitions": { "type": "object", "description": "Relevant key-value pairs from _key_definitions.md." },
    "targetSchemaId": { "type": "string", "description": "ID of the U-SCHEMA-* to adhere to for output." }
  },
  "required": ["taskId", "taskName", "sourceContent"]
}
```

**Conceptual Output Schema (`llm-io/llm-io-schemas/task_example_output_v1.json_schema`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Example LLM Task Output",
  "description": "Schema for output from an example LLM task.",
  "type": "object",
  "properties": {
    "taskId": { "type": "string", "description": "Corresponds to the input taskId." },
    "status": { "type": "string", "enum": ["success", "partial_success", "failure"] },
    "failureReason": { "type": "string", "description": "Details if status is failure." },
    "generatedData": {
      "type": "object",
      "description": "The structured data generated by the LLM, specific to the task."
      // Example: "yamlFrontmatter": { ... }, "markdownBody": "..."
    },
    "llmConfidence": { "type": "number", "minimum": 0, "maximum": 1, "description": "LLM's confidence if available." }
  },
  "required": ["taskId", "status", "generatedData"]
}
```

## Governance and Maintenance

### Proposing New Schemas
- Any team member or stakeholder may propose a new schema by documenting the need and drafting a schema using standard JSON Schema syntax.
- The draft schema is submitted for review by KB architects or the standards committee.
- Upon approval, the schema is versioned and added to the `llm-io/llm-io-schemas/` directory.

### Schema Versioning
- All schema files MUST use SemVer principles in their filenames (e.g., `...input-vMajor.Minor.json_schema`).
- Minor version increments are for backward-compatible changes; major version increments are for breaking changes.
- Deprecated schemas are moved to an `archive/` subfolder within `llm-io/llm-io-schemas/`.

### Schema Documentation
- Each schema file MUST use the `title` and `description` top-level JSON Schema keywords.
- Each property within the schema MUST have a `description` field explaining its purpose, data type, and whether it is required or optional.

## LLM Prompt Meta-Data Structure

*   `prompt_id`: (String) A unique identifier for the prompt (e.g., "KB-ARTICLE-SUMMARIZER-V1").
*   `prompt_name`: (String) A human-readable name for the prompt.
*   `prompt_description`: (String) A brief description of what the prompt does.
*   `prompt_version`: (String) Semantic version of the prompt (e.g., "1.0.2").
*   `tags`: (List of Strings) Keywords for categorization.
*   `variables`: (List of Objects) Describes input variables required by the prompt template.
    *   `var_name`: (String) e.g., "input_text", "tone_style"
    *   `var_type`: (String) e.g., "string", "integer", "boolean"
    *   `var_description`: (String) Explanation of the variable.
    *   `var_required`: (Boolean)
*   `prompt_template_url`: (String) Relative path to the prompt template file (e.g., `./prompts/summarizer_v1.txt`).
*   `model_parameters`: (Object) Key-value pairs for LLM parameters (e.g., `"temperature": 0.7`, `"max_tokens": 500`).
*   `expected_output_description`: (String) Description of the expected output format or structure.
*   `notes`: (String, Optional) Any additional notes or usage instructions.

## 3. Related Standards

- [[OM-AUTOMATION-LLM-PROMPT-LIBRARY]]
- [[MT-SCHEMA-FRONTMATTER]]
- [[GM-CONVENTIONS-NAMING]]
