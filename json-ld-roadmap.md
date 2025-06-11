>THE "*🚨 MANDATORY* ROADMAP PROGRESS MANAGEMENT PROTOCOL" *MUST* BE FOLLOWED AND UPDATED AT ALL TIMES TO ENSURE THE PROGRESS IS ACTIVELY TRACKED AND WORK CAN BE RESUMED FROM THE SAME POINT WITHOUT CAUSING ANY CONFUSION AND REDUNDANCY, THE PROGRESS MUST BE UPDATED CONTINUOUSLY WITHOUT ANY EXCEPTION

>UPDATE THE CHECKLIST CONTINUOUSLY AT ALL TIMES WITHOUT ANY EXCEPTION

# PROJECT EXECUTION ROADMAP

## PROJECT OVERVIEW

**Brief Description:** This project will execute the complete architectural evolution of the knowledge base system, migrating it from a disparate collection of YAML-based Single Sources of Truth (SSTs) to a unified, governed, and fully automated knowledge graph. The new architecture will be built exclusively on JSON-LD as the sole SST, with all tools and workflows refactored to be data-driven from this central graph. The outcome will be a highly resilient, scalable, and AI-native system prepared for advanced automation and reasoning tasks.

---

## PHASE 1: Foundational SST Generation & The Great Deprecation
**Brief Description:** This phase focuses on bootstrapping the new JSON-LD Single Source of Truth from the legacy YAML files. It culminates in the permanent removal of the old SSTs, establishing a clear point of no return and mandating the subsequent refactoring of all tools.

---

### STEP 1.1: Define Core Contexts and Versioning
**Brief Description:** Establish the foundational vocabulary and versioning mechanism for the entire knowledge graph. This step creates the semantic dictionary that all other components will use.

---

#### TASK 1.1.1: Create Directory Structure
- 🎬 Create the `standards/registry/contexts/` directory.

#### TASK 1.1.2: Define Base Context and Versioning
- 🎬 Create the `base.jsonld` file within the new `contexts/` directory.
- 🎬 Populate `base.jsonld` with the core prefixes (`kb:`, `schema:`, `xsd:`, etc.) and define the `kb:schemaVersion` property.
- 🎬 Set the initial `kb:schemaVersion` value to `"1.0.0"`.

---

### STEP 1.2: Build and Execute the Bootstrap Script
**Brief Description:** Develop and run the one-time migration script that will generate the core JSON-LD SSTs from the legacy YAML files.

---

#### TASK 1.2.1: Develop Bootstrap Script
- 🎬 Create a new script named `tools/migration/bootstrap_sst.py`.
- 🎬 Implement logic within the script to read and parse `standards/registry/mt-schema-frontmatter.yaml` and `standards/registry/mt-registry-tag-glossary.yaml`.
- 🎬 Implement the transformation logic to convert the parsed YAML data into the new JSON-LD schema structure.
- 🎬 Implement file-writing logic to output the final `schema-registry.jsonld` and `contexts/fields.jsonld` files.

#### TASK 1.2.2: Execute and Verify
- 🎬 Run the `bootstrap_sst.py` script to generate the JSON-LD files.
- 🎬 Manually inspect the generated `schema-registry.jsonld` and `contexts/fields.jsonld` files to verify their correctness, completeness, and structural integrity against the source YAML.

---

### STEP 1.3: Execute The Great Deprecation
**Brief Description:** Permanently remove the legacy SSTs to enforce the new architecture and eliminate any possibility of tools using outdated sources.

---

#### TASK 1.3.1: Delete Legacy SSTs
- 🎬 Delete the following files from the `standards/registry/` directory:
  - `mt-schema-frontmatter.yaml`
  - `mt-registry-tag-glossary.yaml`
  - All generated `.txt` files (e.g., `info_types.txt`, `criticality_levels.txt`).
  - All other generated `.yaml` files (e.g., `field_order.yaml`, `frontmatter_fields.yaml`).

#### TASK 1.3.2: Archive Bootstrap Script
- 🎬 Move the `bootstrap_sst.py` script to a designated `archive/` directory.

---

**🏁 PHASE 1 EXIT CONDITIONS**: The foundational JSON-LD SSTs are created and are the only remaining source of truth for schema information.
**CONDITION 1**: The `schema-registry.jsonld` and `contexts/*.jsonld` files exist in `standards/registry/` and are populated correctly.
**CONDITION 2**: The `kb:schemaVersion` is present and set to `"1.0.0"` in the schema registry.
**CONDITION 3**: All legacy YAML and derivative `.txt` SST files are confirmed to be deleted from the `standards/registry/` directory.

---

## PHASE 2: Graph Reconciliation & Basic Validation
**Brief Description:** This phase focuses on creating the master inventory of all knowledge nodes as a graph (`master-index.jsonld`) and refactoring the linter into a basic schema validator that consumes the new JSON-LD SST.

---

### STEP 2.1: Refactor Indexer into Reconciliation Engine
- 🎬 Completely refactor the script `tools/indexer/generate_index.py`.
- 🎬 Implement logic to first load the existing `master-index.jsonld` file (if it exists).
- 🎬 Implement logic to scan the entire knowledge base for all `.md` files.
- 🎬 Implement the three-way reconciliation logic: ADD new file nodes, UPDATE existing nodes if frontmatter changed, and REMOVE nodes for deleted files.
- 🎬 Ensure the script outputs the updated `master-index.jsonld` file.

### STEP 2.2: Generate the Master Index
- 🎬 Run the newly refactored Reconciliation Engine to produce the first version of `master-index.jsonld`.

### STEP 2.3: Refactor Linter into Graph Validator (Part 1)
- 🎬 Refactor the script `tools/linter/kb_linter.py` into a new tool located at `tools/validators/graph_validator.py`.
- 🎬 Delete all logic related to loading and parsing the old `.txt` and `.yaml` registry files.
- 🎬 Implement logic to first load `schema-registry.jsonld` and check its `kb:schemaVersion` for compatibility, failing with an error if incompatible.
- 🎬 Implement logic to load `master-index.jsonld`.
- 🎬 Implement the core validation loop that iterates through every node in the master index and validates its properties against the rules defined in the schema registry.

---

**🏁 PHASE 2 EXIT CONDITIONS**: The KB's content inventory exists as a queryable graph, and a basic validator can ensure its schema compliance.
**CONDITION 1**: The `master-index.jsonld` file is successfully generated and contains a node for every `.md` file in the KB.
**CONDITION 2**: The new `graph_validator.py` script successfully executes and validates all nodes in `master-index.jsonld` against `schema-registry.jsonld` without errors.

---

## PHASE 3: Relationship Graph & Link Validation
**Brief Description:** This phase enhances the Graph Validator to make the knowledge graph semantically aware by explicitly mapping all relationships between documents and validating their integrity.

---

### STEP 3.1: Enhance Graph Validator for Link Validation
- 🎬 Implement a new function within `graph_validator.py` dedicated to link validation.
- 🎬 This function must iterate through every link property (e.g., `kb:relatedStandards`) on every node in `master-index.jsonld`.
- 🎬 For each link target ID, the function must query `master-index.jsonld` to confirm a node with that `@id` exists.
- 🎬 The function must report a "broken link" error if a target node does not exist.

### STEP 3.2: Enhance Graph Validator for Relationship Generation
- 🎬 Implement a new function within `graph_validator.py` dedicated to relationship graph generation.
- 🎬 This function must scan the full body content of every `.md` file referenced in the master index.
- 🎬 It must use regex to find all `[[STANDARD_ID]]` references within the body text.
- 🎬 It must then generate or update the `relationships.jsonld` file, creating explicit `kb:references` edges between the source and target document nodes.

---

**🏁 PHASE 3 EXIT CONDITIONS**: The knowledge graph is fully connected and all internal links are validated.
**CONDITION 1**: The `graph_validator.py` script can successfully identify and report broken `[[STANDARD_ID]]` links.
**CONDITION 2**: The `relationships.jsonld` file is successfully generated and accurately reflects the cross-references found in the content bodies.

---

## PHASE 4: Advanced Business Rule Validation (SHACL)
**Brief Description:** Implement the final and most powerful layer of validation, capable of enforcing complex, cross-document business rules using SHACL.

---

### STEP 4.1: Create SHACL Shapes File
- 🎬 Create a new file at `standards/registry/shacl-shapes.ttl`.
- 🎬 Define the initial set of critical business rules in SHACL syntax (e.g., rules for `criticality` vs. `lifecycle_gatekeeper`).

### STEP 4.2: Integrate SHACL Engine into Graph Validator
- 🎬 Add a new validation step to `graph_validator.py`.
- 🎬 Integrate a Python SHACL library (e.g., `pyshacl`).
- 🎬 Implement logic to load the knowledge graph by combining `master-index.jsonld` and `relationships.jsonld`.
- 🎬 Implement logic to validate the combined graph against the rules in `shacl-shapes.ttl`.
- 🎬 Ensure any SHACL validation failures are reported as critical errors.

---

**🏁 PHASE 4 EXIT CONDITIONS**: The system can automatically enforce complex business logic across the entire knowledge graph.
**CONDITION 1**: The `shacl-shapes.ttl` file exists and contains at least one valid business rule.
**CONDITION 2**: The `graph_validator.py` script successfully executes the SHACL validation step and reports violations correctly.

---

## PHASE 5: Unifying the Toolchain & Formalizing Workflows
**Brief Description:** Refactor the remaining legacy tools to be data-driven from the JSON-LD SSTs and formally document the critical human/AI update workflow.

---

### STEP 5.1: Refactor the Naming Enforcer
- 🎬 Refactor the script `tools/naming-enforcer/naming_enforcer.py`.
- 🎬 Delete all logic that reads its local `.json` configuration files.
- 🎬 Implement new logic to load `schema-registry.jsonld` and extract naming conventions, which must now be defined as properties within the schema itself.

### STEP 5.2: Develop the View Generator
- 🎬 Create a new script named `tools/view_generator.py`.
- 🎬 Implement logic to read the JSON-LD SSTs.
- 🎬 The script must be capable of producing two distinct outputs for a given standard or schema:
  1. A human-readable `.md` file for architect review.
  2. A structured `.yaml` file to serve as an AI-consumable "change request" manifest.

### STEP 5.3: Author the Workflow Standard
- 🎬 Create a new standard document: `OM-PROCESS-SST-UPDATE.md`.
- 🎬 Populate this standard with the formal, step-by-step process for updating the JSON-LD SSTs, including the format of the `.yaml` change request file and mandatory post-change validation steps.

---

**🏁 PHASE 5 EXIT CONDITIONS**: The toolchain is unified, and the human/AI update process is formally governed.
**CONDITION 1**: The Naming Enforcer operates solely based on rules defined in `schema-registry.jsonld`.
**CONDITION 2**: The View Generator can successfully produce both `.md` and `.yaml` views from the SSTs.
**CONDITION 3**: The `OM-PROCESS-SST-UPDATE.md` standard is authored, approved, and published.

---

## PHASE 6: Full Orchestration with Scribe
**Brief Description:** Fully automate the entire knowledge graph maintenance and validation pipeline using the Scribe engine, operationalizing the new architecture.

---

### STEP 6.1: Create Scribe Action Plugins
- 🎬 Refactor the core logic from the new, modular tools (Reconciliation Engine, Graph Validator, Naming Enforcer, View Generator) into distinct `BaseAction` subclasses within the `tools/scribe/actions/` directory.

### STEP 6.2: Define Scribe Workflows
- 🎬 Modify `tools/scribe/config/config.json` to define the end-to-end workflows.
- 🎬 Implement a primary workflow triggered on `.md` file changes that sequences the Scribe actions in the correct order (e.g., Namer → Reconciler → Validator).
- 🎬 Implement a secondary workflow triggered on SST changes that runs the Graph Validator and View Generator.

---

**🏁 PHASE 6 EXIT CONDITIONS**: The knowledge graph is self-maintaining and self-validating via an event-driven pipeline.
**CONDITION 1**: Scribe action plugins exist for all refactored tools.
**CONDITION 2**: The Scribe configuration correctly orchestrates the end-to-end validation and generation pipeline upon file changes.
**CONDITION 3**: A test run of the Scribe workflow completes successfully without manual intervention.

---

**🏁 PROJECT EXIT CONDITIONS**: The knowledge base has been fully migrated to a JSON-LD-native architecture, and all supporting tools and processes have been updated.
**CONDITION 1**: All legacy YAML SSTs and their derivative registry files are confirmed to be removed from the repository.
**CONDITION 2**: All core tools (Graph Validator, Reconciliation Engine, Naming Enforcer, View Generator) are refactored and verifiably driven by the JSON-LD SSTs.
**CONDITION 3**: The Scribe engine successfully orchestrates the entire validation and generation pipeline in an automated, event-driven manner.
**CONDITION 4**: The Human/AI update workflow is documented in a formal standard and is operational.

---

## EXECUTION PROTOCOL

### **SEQUENTIAL PROGRESSION**

- **PHASES**: Must complete 1 → 2 → 3...
- **STEPS**: Must complete 1.1 → 1.2 → 1.3...
- **TASKS**: Must complete 1.1.1 → 1.1.2 → 1.1.3...
- **NO PARALLEL EXECUTION** unless explicitly planned

### **COMPLETION STANDARDS**

- **100% COMPLETION REQUIRED** before advancing
- **ZERO TOLERANCE** for partial completion
- **EXIT CONDITIONS** must be verified and checked off

### **BLOCKED PROGRESS PROTOCOL**
If progress is blocked,

1. **TAKE A STEP BACK**, review and analyze the plan from a different perspective, then craft an alternative strategy and try again. IF resolved, continue, ELSE, GOTO 2
2. **GO BACKWARDS STEP BY STEP**, review and analyze the plan meticulously at each step, and try to identify the flaw in the plan or where the problem was introduced (go back until the previous 100% checkpoint)
2.1 **IF A SOLUTION IS FOUND**, apply and continue
2.2 **ELSE IF NO SOLUTION IS FOUND**, mark the plan as **❌ BLOCKED** and execute the **FAILURE PROTOCOL**

### **FAILURE PROTOCOL**
If progress is blocked,

1. **IMMEDIATELY STOP** all progression
2. **DOCUMENT** blocking issue with specific details
2.1 **ADD** a one-liner note to the plan
2.2 **UPDATE** the progress report with specific details
2.3 **ENSURE** the specific item and all the affected parent branches are marked as **❌ BLOCKED**

## **🚨 MANDATORY** ROADMAP PROGRESS MANAGEMENT PROTOCOL

>**THIS PROTOCOL IS *MANDATORY* AND *MUST* BE FOLLOWED AT ALL TIMES**

### **PROGRESS TRACKING OPTIONS**

#### **PROGRESS CHECKLIST**
- **UPDATE** status checkboxes in the separate checklist
- **ADD** one-liner notes to the checklist items (NOT the roadmap)
- **MAINTAIN** separate detailed progress tracker document

---