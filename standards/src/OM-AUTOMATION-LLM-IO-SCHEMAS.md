---

title: 'Standard: LLM Automation Input/Output Schemas'
standard_id: OM-AUTOMATION-LLM-IO-SCHEMAS
aliases:
- LLM IO Schemas
- LLM Automation Schemas
- LLM Data Schema
tags:
- content-type/standard-definition
- criticality/p1-high
- kb-id/standards
- status/active
- topic/automation
- topic/llm-integration
- topic/om
- topic/schemas
- topic/data-interchange
kb-id: standards
info-type: standard-definition
primary-topic: LLM Automation I/O Schemas
related-standards:
- '[[OM-AUTOMATION-LLM-PROMPT-LIBRARY]]'
- '[[MT-SCHEMA-FRONTMATTER]]'
- '[[GM-CONVENTIONS-NAMING]]'
version: 2.0.0
date-created: '2025-05-19T00:00:00Z'
date-modified: '2025-06-17T14:16:00Z'
primary_domain: OM
sub_domain: AUTOMATION
scope_application: Defines the standard for creating, documenting, and managing JSON schemas used for LLM input/output in automated workflows.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- LLM automation
- Data interchange
- Schema validation
- Workflow integration
- Data consistency
- Automation reliability
---
# Standard: LLM Automation Input/Output Schemas (OM-AUTOMATION-LLM-IO-SCHEMAS)

## 1. Standard Statement

This document defines the standard for creating, documenting, and managing JSON schemas used for structured input to and output from Large Language Models (LLMs) in automated knowledge base workflows. Standardizing these I/O schemas is crucial for ensuring interoperability, maintainability, and reliability of LLM-based automation within the knowledge base ecosystem.

## 2. Purpose and Objectives

The primary purposes of defining standard LLM I/O schemas are:
- **Consistency:** Ensuring all LLM automation components expect and produce data in a predictable format
- **Interoperability:** Allowing different LLM scripts, services, and tools to connect and exchange data seamlessly
- **Maintainability:** Simplifying the development, debugging, and updating of LLM automation scripts by providing clear data contracts
- **Scalability:** Facilitating the expansion of LLM automation capabilities with a common data framework
- **Validation:** Enabling automated validation of data exchanged with LLM components
- **Clarity:** Eliminating ambiguity in LLM task execution through well-defined data structures

## 3. General Principles

- **Format:** Data exchange MUST primarily use JSON. YAML may be acceptable for human-readable configuration inputs but JSON is REQUIRED for API-like interactions
- **Clarity:** Field names MUST be descriptive and unambiguous
- **Versioning:** I/O schemas themselves MUST be versioned when significant changes occur
- **Extensibility:** Schemas MUST allow for optional fields or metadata sections for future enhancements without breaking existing implementations
- **Validation:** All schemas MUST use standard JSON Schema syntax and conventions

## 4. Core Schema Requirements

### 4.1. Mandatory Schema Definition Rules

| Rule # | Statement of Rule | Example | Notes |
| :----- | :---------------- | :------ | :---- |
| 1.1 | For every distinct automated task involving an LLM, separate JSON schemas MUST be defined for the expected input structure provided to the LLM and the expected output structure received from the LLM | Task: "Draft New Topic". Input Schema: `draft_topic_input.json_schema`. Output Schema: `draft_topic_output.json_schema` | Ensures clarity and predictability of LLM interactions |
| 1.2 | All LLM I/O schemas MUST be documented. This documentation MUST include the schema's purpose, a description of each field, data types, and whether fields are required or optional | A Markdown file per schema, or a central schema dictionary | Documentation is crucial for understanding and maintaining the automation |
| 1.3 | Schemas MUST use standard JSON Schema syntax and conventions | `{ "type": "object", "properties": { ... } }` | Promotes interoperability and use of standard validation tools |
| 1.4 | Schemas MUST be versioned. Changes to a schema that are not backward-compatible MUST result in a new version of the schema | `draft_topic_input_v1.0.json_schema`, `draft_topic_input_v1.1.json_schema` | Manages evolution and impact on dependent prompts and scripts |

## 5. Standard Input Schema (Request to LLM Automation)

This section outlines common fields for data sent *to* an LLM automation script/service.

### 5.1. Core Input Fields (Mandatory)

- `request_id` (String, UUID, Optional): A unique identifier for the request, useful for tracing and logging
- `task_id` (String, Mandatory): Unique identifier for the specific job instance
- `task_type` (String, Mandatory): An identifier for the specific LLM task to be performed (e.g., "generate-abstract", "summarize-text", "extract-keywords", "translate-content")
- `source_document_id` (String, Optional): The `standard_id` or unique path of the document the LLM task pertains to (if any)

### 5.2. Content Input Fields

- `input_text_content` (String, Conditional): The primary text content to be processed by the LLM. Conditional based on `task_type`
- `input_data_payload` (Object, Conditional): For tasks requiring more structured input than plain text (e.g., providing context, examples, or specific parameters)
- `contextual_information` (Object, Optional): Relevant existing KB content, key definitions, and contextual data
- `task_specific_parameters` (Object, Optional): Parameters specific to the task being performed

### 5.3. LLM Configuration Parameters (Optional)

- `llm_model_preference` (String, Optional): Preferred LLM model to use (e.g., "gpt-4", "claude-3-opus")
- `temperature` (Float, Optional): LLM temperature setting
- `max_tokens` (Integer, Optional): Maximum tokens for the LLM response
- `custom_instructions` (String, Optional): Specific instructions or system prompts to guide the LLM for this request

### 5.4. Output Control

- `output_format_hint` (String, Optional): A hint to the LLM or script about the desired output format (e.g., "markdown", "json_list", "single_sentence")
- `requested_schema_version` (String, Optional): If the output data has a versioned schema, the version requested by the client
- `target_schema_id` (String, Optional): ID of the target schema to adhere to for output

## 6. Standard Output Schema (Response from LLM Automation)

This section outlines common fields for data sent *from* an LLM automation script/service.

### 6.1. Core Output Fields (Mandatory)

- `request_id` (String, UUID, Optional): Copied from the input `request_id` for correlation
- `task_id` (String, Mandatory): Corresponds to the input task_id
- `response_id` (String, UUID, Mandatory): A unique identifier for this specific response
- `status` (String, Mandatory): Indicates the outcome of the LLM task
  - Allowed values: `"success"`, `"partial_success"`, `"failure"`, `"error"`

### 6.2. Response Content Fields

- `llm_response_data` (Object, Mandatory): The structured payload containing the LLM's output
- `generated_data` (Object, Conditional): The structured data generated by the LLM, specific to the task
- `failure_reason` (String, Conditional): Details if status is failure or error
- `processing_metadata` (Object, Optional): Information about the processing pipeline

### 6.3. Quality and Confidence Indicators

- `llm_confidence` (Number, Optional): LLM's confidence score if available (0-1 range)
- `validation_status` (String, Optional): Result of automated validation checks
- `quality_metrics` (Object, Optional): Additional quality indicators

## 7. Schema Repository and Naming Conventions

### 7.1. Repository Structure

- A dedicated directory `master-knowledge-base/llm-io/llm-io-schemas/` MUST be used to store all JSON schema definition files
- Schema file names MUST clearly indicate the task and whether it's an input or output schema, including version
- Naming pattern: `task_[taskname]_[input|output]_v[major].[minor].json_schema`

### 7.2. Versioning Strategy

- All schema files MUST use SemVer principles in their filenames
- Minor version increments are for backward-compatible changes
- Major version increments are for breaking changes
- Deprecated schemas MUST be moved to an `archive/` subfolder within `llm-io/llm-io-schemas/`

## 8. Example Schema Structures

### 8.1. Conceptual Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LLM Task Input Schema",
  "description": "Standard schema for LLM task input",
  "type": "object",
  "properties": {
    "request_id": { "type": "string", "format": "uuid", "description": "Unique request identifier" },
    "task_id": { "type": "string", "description": "Unique ID for this task instance" },
    "task_type": { "type": "string", "enum": ["createTopic", "summarizeText", "suggestMetadata"] },
    "source_document_id": { "type": "string", "description": "Source document identifier" },
    "input_text_content": { "type": "string", "description": "Main text content to process" },
    "contextual_information": { "type": "object", "description": "Relevant context data" },
    "task_specific_parameters": { "type": "object", "description": "Task-specific configuration" },
    "llm_model_preference": { "type": "string", "description": "Preferred LLM model" },
    "temperature": { "type": "number", "minimum": 0, "maximum": 2 },
    "max_tokens": { "type": "integer", "minimum": 1 },
    "output_format_hint": { "type": "string", "description": "Desired output format" }
  },
  "required": ["task_id", "task_type"]
}
```

### 8.2. Conceptual Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LLM Task Output Schema",
  "description": "Standard schema for LLM task output",
  "type": "object",
  "properties": {
    "request_id": { "type": "string", "format": "uuid", "description": "Corresponds to input request_id" },
    "task_id": { "type": "string", "description": "Corresponds to the input task_id" },
    "response_id": { "type": "string", "format": "uuid", "description": "Unique response identifier" },
    "status": { "type": "string", "enum": ["success", "partial_success", "failure", "error"] },
    "failure_reason": { "type": "string", "description": "Details if status is failure/error" },
    "llm_response_data": { "type": "object", "description": "The structured LLM output" },
    "generated_data": { "type": "object", "description": "Task-specific generated content" },
    "llm_confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "validation_status": { "type": "string", "description": "Validation check results" },
    "processing_metadata": { "type": "object", "description": "Processing pipeline information" }
  },
  "required": ["task_id", "response_id", "status", "llm_response_data"]
}
```

## 9. LLM Prompt Meta-Data Structure

For integration with prompt libraries, the following metadata structure MUST be used:

- `prompt_id` (String): A unique identifier for the prompt (e.g., "KB-ARTICLE-SUMMARIZER-V1")
- `prompt_name` (String): A human-readable name for the prompt
- `prompt_description` (String): A brief description of what the prompt does
- `prompt_version` (String): Semantic version of the prompt (e.g., "1.0.2")
- `tags` (List of Strings): Keywords for categorization
- `variables` (List of Objects): Describes input variables required by the prompt template
  - `var_name` (String): e.g., "input_text", "tone_style"
  - `var_type` (String): e.g., "string", "integer", "boolean"
  - `var_description` (String): Explanation of the variable
  - `var_required` (Boolean): Whether the variable is mandatory
- `prompt_template_url` (String): Relative path to the prompt template file
- `model_parameters` (Object): Key-value pairs for LLM parameters
- `expected_output_description` (String): Description of the expected output format
- `input_schema_reference` (String): Reference to the input schema version
- `output_schema_reference` (String): Reference to the output schema version
- `notes` (String, Optional): Additional notes or usage instructions

## 10. Governance and Maintenance

### 10.1. Proposing New Schemas

- Any team member or stakeholder may propose a new schema by documenting the need and drafting a schema using standard JSON Schema syntax
- The draft schema MUST be submitted for review by KB architects or the standards committee
- Upon approval, the schema MUST be versioned and added to the `llm-io/llm-io-schemas/` directory

### 10.2. Schema Documentation Requirements

- Each schema file MUST use the `title` and `description` top-level JSON Schema keywords
- Each property within the schema MUST have a `description` field explaining its purpose, data type, and whether it is required or optional
- Cross-references between related schemas MUST be maintained

### 10.3. Integration with Prompt Libraries

- The `OM-AUTOMATION-LLM-PROMPT-LIBRARY` standard MUST reference the specific version of the input and output schemas that a prompt template is designed for
- Example: Prompt `P-DRAFT-TOPIC-001` uses input schema `draft_topic_input_v1.0` and expects output schema `draft_topic_output_v1.0`

## 11. Validation and Compliance

### 11.1. Automated Validation

- All schema files MUST be validated against JSON Schema meta-schema before deployment
- Automated tests MUST verify schema compatibility with existing prompt templates
- CI/CD pipelines MUST include schema validation steps

### 11.2. Compliance Monitoring

- Regular audits MUST be conducted to ensure all LLM automation components use approved schemas
- Non-compliant implementations MUST be flagged for immediate remediation
- Schema usage metrics MUST be tracked for optimization purposes

## 12. Migration Path

### 12.1. Legacy Systems

- Existing LLM automation components have 90 days to adopt the standardized schemas
- Migration scripts MUST be provided for common legacy formats
- Backward compatibility MUST be maintained during the transition period

### 12.2. Deprecation Process

- Deprecated schemas MUST be marked with clear deprecation notices
- Minimum 6-month notice MUST be given before removing deprecated schemas
- Migration guides MUST be provided for all deprecated schemas

---

**Note:** This standard consolidates and supersedes the previous `UA-SCHEMA-LLM-IO` standard, providing a comprehensive and authoritative specification for LLM I/O schemas in the knowledge base ecosystem.