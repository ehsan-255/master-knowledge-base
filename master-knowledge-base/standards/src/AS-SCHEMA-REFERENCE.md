---
title: 'Standard: Reference Document Schema'
standard_id: AS-SCHEMA-REFERENCE
aliases:
  - Schema for Reference Topics
  - Reference Topic Structure
tags:
  - status/draft
  - criticality/p1-high
  - content-type/schema-document
  - topic/schemas
  - topic/documentation-standards
  - kb-id/standards
kb-id: standards
info-type: schema-document
primary-topic: Defines the standard structure and core elements for reference documents,
  typically used for detailing APIs, commands, functions, or configuration parameters.
related-standards:
  - MT-SCHEMA-FRONTMATTER
  - AS-STRUCTURE-DOC-CHAPTER
  - SF-SYNTAX-HEADINGS
version: 0.1.0
date-created: '2025-05-29T15:49:24Z'
date-modified: '2025-05-30T12:00:00Z'
primary_domain: AS
sub_domain: SCHEMA
scope_application: Applies to all documents categorized as 'reference topics' or intended
  to provide detailed specifications for technical elements like APIs, commands, functions,
  tags, or parameters.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - Technical documentation consistency
  - Developer experience
  - API documentation
  - Automated parsing of reference material
change_log_url: ./changelog.md
---
# Standard: Reference Document Schema (AS-SCHEMA-REFERENCE)

## 1. Standard Statement

This standard defines the mandatory and recommended structure for creating **Reference Documents**. Reference documents provide detailed, factual information about specific technical elements such as Application Programming Interface (API) endpoints, command-line interface (CLI) commands, programming language functions or classes, configuration parameters, or data structure definitions.

Adherence to this schema ensures that reference documentation is consistent, comprehensive, predictable, and easy for users (especially developers and technical staff) to navigate and understand. This schema builds upon the general document structure defined in `[[AS-STRUCTURE-DOC-CHAPTER]]`.

## 2. Purpose of Reference Documents

Reference documents are intended to be lookup resources. Users consult them to find:
-   The exact syntax or signature of an element.
-   The purpose and behavior of parameters or options.
-   Expected return values or outcomes.
-   Examples of correct usage.
-   Details of potential errors or exceptions.
-   Other relevant technical details.

They are distinct from tutorials (which teach how to do something step-by-step) or guides (which explain concepts or best practices).

## 3. Core Structure of a Reference Document

A reference document, after the standard frontmatter and H1 title (which should clearly name the element being referenced, e.g., "Command: `git commit`" or "Function: `calculate_average()`"), MUST generally follow this sequence of H2 sections. Some sections are optional depending on the nature of the element being documented.

### 3.1. Element Overview / Description (Mandatory)
   - **Heading:** `## Overview` or `## Description`
   - **Content:** A brief summary (1-3 sentences) explaining what the element is and its primary purpose. This may be similar to the abstract section mentioned in `[[AS-STRUCTURE-DOC-CHAPTER]]` but focused specifically on the element.

### 3.2. Syntax / Signature (Conditional - Mandatory if applicable)
   - **Heading:** `## Syntax` (for commands, code structures) or `## Signature` (for functions, methods, API endpoints)
   - **Content:** The formal definition of how to use or call the element.
     - For commands: Show the command and its parameters, using conventions for optional/required parts.
     - For functions/methods: Show the function signature, including parameter names, types, and return type.
     - For API endpoints: Show the HTTP method, URL pattern, and any path/query parameters.
   - **Example:**
     ```
     ## Syntax
     my_command [--option-a <value>] <required_argument>
     ```
     ```
     ## Signature
     function calculate_sum(a: number, b: number): number
     ```

### 3.3. Parameters / Arguments / Options (Conditional - Mandatory if applicable)
   - **Heading:** `## Parameters`, `## Arguments`, or `## Options` (choose the most appropriate for the element type)
   - **Content:** A detailed list or table describing each parameter, argument, or option. For each item, provide:
     - **Name:** The exact name of the parameter/argument.
     - **Data Type:** (If applicable, e.g., string, integer, boolean, list).
     - **Description:** Explanation of its purpose and effect.
     - **Required/Optional:** Whether it must be provided.
     - **Default Value:** (If applicable and one exists).
     - **Allowed Values/Range:** (If applicable, e.g., for enums or specific value sets).
   - **Format:** Use a definition list, bulleted list with nested details, or a table for clarity.

### 3.4. Return Values / Output (Conditional - Mandatory if applicable)
   - **Heading:** `## Return Values` (for functions/methods) or `## Output` (for commands)
   - **Content:** Description of what the function/method returns or what the command outputs upon successful execution.
     - Specify data types and structure if complex.
     - For commands, describe standard output, standard error, and exit codes if relevant.

### 3.5. Examples (Highly Recommended, Mandatory for many use cases)
   - **Heading:** `## Examples`
   - **Content:** One or more practical examples of how to use the element.
     - Examples should be concise, correct, and illustrative of common use cases.
     - Use code blocks with appropriate language identifiers.
     - Briefly explain what each example does and why it's relevant.

### 3.6. Error Handling / Exceptions (Conditional - Recommended if applicable)
   - **Heading:** `## Error Handling` or `## Exceptions`
   - **Content:** Description of common errors, exceptions, or non-zero exit codes.
     - Explain what might cause them and how to resolve them.
     - This section is crucial for user troubleshooting.

### 3.7. Attributes / Properties (Conditional - If the element has readable/settable properties)
   - **Heading:** `## Attributes` or `## Properties`
   - **Content:** Similar to Parameters, listing properties of an object or resource. For each:
     - Name, Data Type, Read/Write status, Description.

### 3.8. Configuration Details (Conditional - For elements that are configured)
   - **Heading:** `## Configuration`
   - **Content:** Details on how to configure the element, perhaps referencing configuration files or specific settings.

### 3.9. Usage Notes / Remarks (Optional)
   - **Heading:** `## Usage Notes` or `## Remarks`
   - **Content:** Additional important information, best practices, limitations, or edge cases that don't fit neatly into other sections.

### 3.10. Related Elements / See Also (Highly Recommended)
   - **Heading:** `## Related Elements` or `## See Also`
   - **Content:** Links to other relevant reference documents, guides, or standards.
     - Example: A command reference might link to related commands or a conceptual guide explaining its purpose.

## 4. General Guidelines
- **Clarity and Precision:** Use unambiguous language. Define terms where necessary.
- **Completeness:** Strive to cover all aspects a user would need to know to use the element effectively.
- **Atomicity:** Each reference document should ideally focus on a single element (e.g., one command, one function). Complex elements with sub-commands might have a main page linking to sub-pages.
- **Code Blocks:** Use Markdown code blocks with correct language identifiers for syntax, examples, and code snippets.
- **Consistency:** Maintain consistent terminology and formatting across all reference documents.

## 5. Scope of Application
This schema applies to all documents intended to provide detailed reference information for technical elements within the knowledge base ecosystem. It is particularly relevant for software documentation, API guides, and system administration manuals.
