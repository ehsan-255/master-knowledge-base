---
title: "Standard: LLM Automation Input/Output Schema"
standard_id: "UA-SCHEMA-LLM-IO"
aliases: ["LLM IO Schema", "Schema for LLM Automation Data Exchange"]
tags: ["status/draft", "criticality/P1-High", "content-type/schema-document", "topic/llm", "topic/automation", "topic/schemas", "topic/data-interchange", "kb-id/standards"]
kb-id: "standards"
info-type: "schema-document"
primary-topic: "Defines the standard input and output data structures (schemas) for scripts and services involved in LLM-based content generation and automation."
related-standards: ["MT-SCHEMA-FRONTMATTER", "OM-POLICY-STANDARDS-GOVERNANCE"]
version: '0.1.0'
date-created: "2025-05-29T15:55:50Z"
date-modified: "2025-05-30T12:00:00Z"
primary_domain: "UA"
sub_domain: "AUTOMATION"
scope_application: "Applies to all automated processes and scripts that interact with Large Language Models (LLMs) for tasks such as content generation, analysis, or modification within the knowledge base ecosystem."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["LLM integration", "Automation reliability", "Data consistency", "Developer workflow for LLM scripts"]
change_log_url: "./UA-SCHEMA-LLM-IO-changelog.md"
---
# Standard: LLM Automation Input/Output Schema (UA-SCHEMA-LLM-IO)

## 1. Standard Statement

This standard defines the recommended and mandatory data structures (schemas) for inputs provided to, and outputs received from, Large Language Model (LLM) automation scripts and services. Standardizing these I/O schemas is crucial for ensuring interoperability, maintainability, and reliability of LLM-based automation within the knowledge base ecosystem.

## 2. Purpose

The primary purposes of defining standard LLM I/O schemas are:
-   **Consistency:** Ensuring all LLM automation components expect and produce data in a predictable format.
-   **Interoperability:** Allowing different LLM scripts, services, and tools to connect and exchange data seamlessly.
-   **Maintainability:** Simplifying the development, debugging, and updating of LLM automation scripts by providing clear data contracts.
-   **Scalability:** Facilitating the expansion of LLM automation capabilities with a common data framework.
-   **Validation:** Enabling automated validation of data exchanged with LLM components.

## 3. General Principles

-   **Format:** Data exchange SHOULD primarily use JSON. YAML may be acceptable for human-readable configuration inputs but JSON is preferred for API-like interactions.
-   **Clarity:** Field names should be descriptive and unambiguous.
-   **Versioning:** I/O schemas themselves MAY be versioned if significant changes occur. This standard (`UA-SCHEMA-LLM-IO`) will govern the general structure, and specific schema instances might carry their own versions if needed.
-   **Extensibility:** Schemas should allow for optional fields or metadata sections for future enhancements without breaking existing implementations.

## 4. Standard Input Schema (Request to LLM Automation)

This section outlines common fields for data sent *to* an LLM automation script/service. Specific scripts may require additional or fewer fields.

### 4.1. Core Input Fields
-   `request_id` (String, UUID, Optional): A unique identifier for the request, useful for tracing and logging.
-   `source_document_id` (String, Optional): The `standard_id` or unique path of the document the LLM task pertains to (if any).
-   `task_type` (String, Mandatory): An identifier for the specific LLM task to be performed (e.g., "generate-abstract", "summarize-text", "extract-keywords", "translate-content").
-   `input_text_content` (String, Conditional): The primary text content to be processed by the LLM. Conditional based on `task_type`.
-   `input_data_payload` (Object, Conditional): For tasks requiring more structured input than plain text (e.g., providing context, examples, or specific parameters). The structure of this object would be task-specific.

### 4.2. LLM Configuration Parameters (Optional)
-   `llm_model_preference` (String, Optional): Preferred LLM model to use (e.g., "gpt-4", "claude-3-opus").
-   `temperature` (Float, Optional): LLM temperature setting.
-   `max_tokens` (Integer, Optional): Maximum tokens for the LLM response.
-   `custom_instructions` (String, Optional): Specific instructions or system prompts to guide the LLM for this request, supplementing any default prompts associated with the `task_type`.

### 4.3. Output Control
-   `output_format_hint` (String, Optional): A hint to the LLM or script about the desired output format (e.g., "markdown", "json_list", "single_sentence").
-   `requested_schema_version` (String, Optional): If the output data has a versioned schema, the version requested by the client.

## 5. Standard Output Schema (Response from LLM Automation)

This section outlines common fields for data sent *from* an LLM automation script/service.

### 5.1. Core Output Fields
-   `request_id` (String, UUID, Optional): Copied from the input `request_id` for correlation.
-   `response_id` (String, UUID, Mandatory): A unique identifier for this specific response.
-   `status` (String, Mandatory): Indicates the outcome of the LLM task.
    -   Allowed values: `"success"`, `"partial_success"`, `"failure"`, `"error"`.
-   `timestamp` (String, ISO-8601 DateTime, Mandatory): Timestamp of when the response was generated.

### 5.2. Content Output (Conditional on Success)
-   `generated_text_content` (String, Conditional): The primary text output from the LLM if the task was successful and produced text.
-   `generated_data_payload` (Object, Conditional): Structured data output from the LLM if the task was successful and produced structured data. The schema of this object would be task-specific.

### 5.3. Error Details (Conditional on Failure/Error)
-   `error_code` (String, Optional): A specific error code if the task failed or an error occurred.
-   `error_message` (String, Optional): A human-readable description of the error.
-   `error_details` (Object, Optional): Additional structured information about the error.

### 5.4. Metadata and Metrics (Optional)
-   `llm_model_used` (String, Optional): The actual LLM model that processed the request.
-   `tokens_prompt` (Integer, Optional): Number of tokens in the input prompt.
-   `tokens_completion` (Integer, Optional): Number of tokens in the LLM's completion.
-   `processing_time_ms` (Integer, Optional): Time taken to process the request in milliseconds.
-   `confidence_score` (Float, Optional): If applicable, a score indicating the LLM's confidence in its response (0.0 to 1.0).
-   `warnings` (List of Strings, Optional): Any non-critical warnings encountered during processing.

## 6. Schema Validation

-   Both input to and output from LLM automation scripts SHOULD be validated against their defined schemas.
-   JSON Schema or similar schema definition languages can be used for this purpose.
-   Strict validation should be enforced for mandatory fields and data types.

## 7. Examples

### Example 1: Input for "generate-abstract" task

```json
{
  "request_id": "c7a3b9e0-4f1d-4a8a-9c3e-0d7f1b3e4c5d",
  "source_document_id": "AS-STRUCTURE-DOC-CHAPTER",
  "task_type": "generate-abstract",
  "input_text_content": "Long document text here...",
  "llm_model_preference": "claude-3-sonnet",
  "output_format_hint": "single_paragraph_markdown"
}
```

### Example 2: Output for a successful "generate-abstract" task

```json
{
  "request_id": "c7a3b9e0-4f1d-4a8a-9c3e-0d7f1b3e4c5d",
  "response_id": "e1b8c4a2-9d3e-4f1a-8c7b-0a9f8e7d6c5b",
  "status": "success",
  "timestamp": "2025-05-29T16:00:00Z",
  "generated_text_content": "This document defines the standard internal structure for core content documents, known as 'chapters'. It outlines mandatory sections such as an H1 title, abstract, table of contents, hierarchically organized content sections, a summary, and a 'See Also' section for related links, ensuring consistency and usability.",
  "llm_model_used": "claude-3-sonnet-20240229",
  "tokens_prompt": 1500,
  "tokens_completion": 85,
  "processing_time_ms": 3500
}
```

## 8. Scope of Application
This standard applies to all developers and teams creating or maintaining LLM automation scripts and services within the knowledge base ecosystem. It also applies to any system components that invoke these LLM services.
