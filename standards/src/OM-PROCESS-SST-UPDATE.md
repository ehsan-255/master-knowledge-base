# OM-PROCESS-SST-UPDATE: JSON-LD SST Update Workflow

| Field                 | Value                                      |
|-----------------------|--------------------------------------------|
| **Standard ID**       | OM-PROCESS-SST-UPDATE                      |
| **Title**             | JSON-LD SST Update Workflow                |
| **Version**           | 1.0.0                                      |
| **Status**            | Draft                                      |
| **Date Created**      | [CURRENT_DATE_YMD]T00:00:00Z               |
| **Date Modified**     | [CURRENT_DATE_YMD]T00:00:00Z               |
| **Primary Domain**    | OM (Operational Management)                |
| **Criticality**       | P1-High                                    |
| **Lifecycle Gatekeeper**| Editorial-Board-Approval                 |
| **Info Type**         | process-definition                         |
| **Scope/Application** | Governs all changes to core JSON-LD SSTs.  |
| **Primary Topic**     | Formal process for updating JSON-LD SSTs.  |

---

## 1. Introduction and Scope

This standard defines the formal process for proposing, reviewing, applying, and validating changes to the core JSON-LD Single Source of Truth (SST) files within the knowledge base system. Adherence to this process is mandatory to ensure the integrity, consistency, and stability of the knowledge graph.

**Covered SSTs**:
*   `standards/registry/schema-registry.jsonld`
*   `standards/registry/master-index.jsonld`
*   `standards/registry/contexts/*.jsonld` (all context files)
*   `standards/registry/shacl-shapes.ttl`
*   Any other file designated as a core JSON-LD SST.

## 2. Roles and Responsibilities

*   **Change Proposer**: Any authorized team member (e.g., Architect, Developer) or designated AI agent can propose changes to the SSTs.
*   **Change Reviewer(s)**: A designated governance body, lead architect, or relevant subject matter experts are responsible for reviewing proposed changes.
*   **Change Implementer**: The individual or AI agent responsible for applying the approved change to the SST files.
*   **Change Approver**: The entity (e.g., Lead Architect, Governance Board) with final authority to approve the merge of applied changes.

## 3. Change Proposal: The YAML Change Request Manifest

All proposed changes to SSTs (excluding entirely new documents managed by other processes) must be described in a YAML "Change Request Manifest" file.

### 3.1 Generating a Base Manifest

For updating existing entities, a base YAML representation can be generated using the `tools/view_generator.py` script:
```bash
python tools/view_generator.py --id <target_entity_@id> --type yaml --output <request_name>.yaml
```
This generated file should then be modified to reflect the proposed changes. For new entities or complex changes, the manifest may be authored from scratch following the format below.

### 3.2 YAML Manifest Format

The YAML Change Request Manifest must adhere to the following structure:

```yaml
# Unique identifier for this change request (e.g., CR-YYYYMMDD-001)
change_request_id: "CR-..."

# The @id of the SST entity being modified or the parent entity if adding/removing elements.
# Examples: "kb:schema-registry", "kb:doc-some-standard", "kb:field-some-field"
target_id: "string"

# Type of operation being performed.
# Allowed values: "update_properties", "add_element", "remove_element", "replace_content"
operation: "string"

# Detailed specification of the change. Structure depends on 'operation'.
payload:
  # Used for "update_properties"
  changes:
    - property: "kb:propertyName"  # Full property URI (e.g., kb:description)
      new_value: "object | string | number | array" # The new value for the property
      old_value: "object | string | number | array" # Optional: Current value for verification

  # Used for "add_element"
  parent_property: "kb:collectionName" # e.g., kb:fieldDefinitions, kb:documents
  element_data: {} # Full JSON-LD object for the new element

  # Used for "remove_element"
  # parent_property: "kb:collectionName" (optional if target_id is the element itself)
  element_id_or_criteria: {} # @id of the element to remove, or a query/criteria object

  # Used for "replace_content" (e.g., for shacl-shapes.ttl or context files)
  new_content: |
    Full new text content of the file.

# Mandatory: Explanation of why this change is needed.
justification: "string"

# Name or ID of the entity (human or AI) proposing the change.
proposer: "string"

# Timestamp (ISO 8601) when the change request was generated.
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
```

### 3.3 Examples

#### Example 1: Updating a Property
```yaml
change_request_id: "CR-20240115-001"
target_id: "kb:field-title"
operation: "update_properties"
payload:
  changes:
    - property: "kb:description"
      new_value: "The official title of the document, now with more clarity."
      old_value: "The official title of the document"
justification: "Improve clarity of the title field description."
proposer: "ArchitectX"
timestamp: "2024-01-15T10:00:00Z"
```

#### Example 2: Adding a New Field Definition
```yaml
change_request_id: "CR-20240115-002"
target_id: "kb:schema-registry" # Target is the registry itself
operation: "add_element"
payload:
  parent_property: "kb:fieldDefinitions"
  element_data:
    "@type": "kb:FieldDefinition"
    "@id": "kb:field-new-custom-field"
    "kb:fieldName": "new-custom-field"
    "kb:description": "A new custom field for specific needs."
    "kb:mandatory": false
    "kb:dataType": "string"
justification: "Requirement for a new optional custom field."
proposer: "DeveloperY"
timestamp: "2024-01-15T11:00:00Z"
```

## 4. Update Process Steps

### Step 4.1: Prepare Change Request
1.  Identify the SST entity to be modified.
2.  If updating an existing entity, generate its current YAML representation using `tools/view_generator.py --id <target_id> --type yaml`.
3.  Create or modify a `.yaml` file according to the Change Request Manifest format specified in Section 3.
4.  Ensure all fields, especially `justification`, are accurately completed.

### Step 4.2: Submit Change Request for Review
1.  Commit the new/updated YAML Change Request Manifest file to a new branch in the Git repository.
2.  Create a Pull Request (PR) targeting the main development branch.
3.  The PR description must include a summary of the change and a link to or inclusion of the YAML manifest content.
4.  Assign relevant reviewers (e.g., Lead Architect, Governance Board members).

### Step 4.3: Review and Approval
1.  Reviewers will assess the proposed change based on:
    *   Accuracy and completeness of the YAML manifest.
    *   Validity of the justification.
    *   Impact on the knowledge graph and downstream systems.
    *   Adherence to existing standards and conventions.
2.  Feedback should be provided via PR comments. Iterations may be needed.
3.  Once all concerns are addressed, the Change Approver gives formal approval on the PR.

### Step 4.4: Apply Change
Once the PR for the YAML manifest is approved (but **not yet merged**):
1.  The Change Implementer (or an authorized AI agent) carefully applies the described changes directly to the target JSON-LD SST file(s) in the same branch.
    *   **Manual Edits**: Extreme care must be taken to maintain valid JSON/JSON-LD/Turtle syntax. Use appropriate editors and linters.
    *   **Automated Edits (Future)**: An AI agent may consume the YAML manifest and use JSON-LD processing libraries to apply changes programmatically.
2.  Commit the modifications to the SST file(s) to the *same branch* as the YAML manifest. The commit message should reference the manifest.

### Step 4.5: Post-Change Validation (Mandatory)
After applying changes to the SSTs, the following validation steps **must** be performed in the branch:
1.  **Run Master Indexer (if applicable)**: If changes could affect document discovery or structure (e.g., adding/removing schema fields that influence indexing), run:
    ```bash
    python tools/indexer/generate_index.py
    ```
2.  **Run Graph Validator**: Execute a full validation suite:
    ```bash
    python tools/validators/graph_validator.py --output-report validation_report.json --log-level INFO
    ```
    Review `validation_report.json`. All schema, link, and SHACL validation errors must be resolved.
3.  **Run Naming Enforcer**: Check for any naming convention violations introduced:
    ```bash
    python tools/naming-enforcer/naming_enforcer.py --scan .
    ```
    Resolve any reported violations.
4.  **Iterate if Validation Fails**: If any validation step fails:
    *   Revert the problematic changes to the SSTs (or fix them directly).
    *   Re-run validation steps.
    *   Commit fixes.
    *   Repeat until all validations pass without critical errors.

### Step 4.6: Commit, Merge, and Archive
1.  Ensure all applied changes (to SSTs and any fixes from validation) and the original YAML manifest are committed to the branch.
2.  The PR (containing the YAML manifest and the applied SST changes) can now be merged into the main development branch by an authorized person.
3.  (Optional) Archive the processed YAML Change Request Manifest to a designated record-keeping location.

### Step 4.7: Update Documentation
*   If the change significantly alters schema or processes, update relevant documentation (e.g., `schema-registry.jsonld` comments, other standards).
*   Update `json-ld-roadmap-progress-tracker.md` or other relevant project logs if the change corresponds to a planned roadmap item.

## 5. Versioning of SSTs

*   **`schema-registry.jsonld`**: The `kb:schemaVersion` property within this file should be incremented according to semantic versioning principles (MAJOR.MINOR.PATCH) upon any non-trivial change:
    *   PATCH: Backwards-compatible fixes or minor additions (e.g., adding an optional field description).
    *   MINOR: Backwards-compatible new features (e.g., adding a new optional field definition, new non-breaking validation rule).
    *   MAJOR: Backwards-incompatible changes (e.g., removing a field, changing a data type, significant structural changes).
*   **`master-index.jsonld`**: Its `kb:version` can be updated (e.g., timestamp-based or incremental) upon each successful regeneration. Its `kb:schemaVersion` should track the version of `schema-registry.jsonld` it is compatible with.
*   **Individual Documents**: `kb:version` in individual Markdown documents should be managed by their respective authors/owners based on content changes.
*   **Context Files / SHACL Shapes**: Versioning of these files can be managed via Git tags or by comments within the files if granular versioning is needed.

## 6. Appendix

### Example: Full Change Request for Removing a Field Definition

```yaml
change_request_id: "CR-20240116-001"
target_id: "kb:schema-registry"
operation: "remove_element"
payload:
  parent_property: "kb:fieldDefinitions"
  element_id_or_criteria:
    "@id": "kb:field-old-custom-field" # ID of the field definition to remove
justification: "Field 'kb:field-old-custom-field' is deprecated and no longer used."
proposer: "AdminUser"
timestamp: "2024-01-16T14:00:00Z"
```
