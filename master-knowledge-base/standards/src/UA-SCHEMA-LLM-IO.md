---
title: 'Schema: LLM Input/Output Data Structures'
standard_id: UA-SCHEMA-LLM-IO
aliases:
  - LLM IO Schema
  - LLM Data Schema
tags:
  - status/draft
  - criticality/p1-high
  - content-type/schema-document
  - topic/llm
  - topic/automation
  - topic/schemas
  - topic/data-interchange
  - kb-id/standards
kb-id: standards
info-type: schema-document
primary-topic: LLM Input/Output Data Structures
related-standards: []
version: 1.0.0
date-created: '2025-05-29T13:24:53Z'
date-modified: '2025-05-30T18:00:00Z'
primary_domain: UA
sub_domain: KEYDEFS
scope_application: Defines the data structures and schemas for LLM input and output
  in automated workflows.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - LLM integration
  - Data consistency
  - Automation reliability
change_log_url: ./UA-SCHEMA-LLM-IO-CHANGELOG.MD
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
-   `