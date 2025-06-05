# Registry Consolidation Execution Plan

## Phase 1: Content Analysis and YAML Structure Design

### 1.1 Analyze Current Registry Files
- ⬜ Subtask 1.1.1: Document complete inventory of all registry files and their content structure
- ⬜ Subtask 1.1.2: Map content relationships between files (dependencies, cross-references)
- ⬜ Subtask 1.1.3: Identify which content belongs in mt-registry-tag-glossary.yaml vs mt-schema-frontmatter.yaml

### 1.2 Design mt-registry-tag-glossary.yaml Structure
- ⬜ Subtask 1.2.1: Define YAML schema for tag categories, hierarchies, and definitions
- ⬜ Subtask 1.2.2: Design structure for tag prefixes, usage guidelines, and relationships
- ⬜ Subtask 1.2.3: Plan metadata and generation tracking sections

### 1.3 Design mt-schema-frontmatter.yaml Updates
- ⬜ Subtask 1.3.1: Plan integration of criticality_levels.yaml content into controlled_vocabularies
- ⬜ Subtask 1.3.2: Plan integration of lifecycle_gatekeepers.yaml content into controlled_vocabularies
- ⬜ Subtask 1.3.3: Plan integration of domain_codes.yaml and subdomain_registry.yaml content
- ⬜ Subtask 1.3.4: Plan integration of maturity_levels.yaml and audience_types.yaml content

## Phase 2: Create New YAML Structures

### 2.1 Create mt-registry-tag-glossary.yaml
- ⬜ Subtask 2.1.1: Extract tag definitions from MT-REGISTRY-TAG-GLOSSARY.md into YAML structure
- ⬜ Subtask 2.1.2: Organize tag categories with proper hierarchy and metadata
- ⬜ Subtask 2.1.3: Add generation metadata and source tracking information

### 2.2 Update mt-schema-frontmatter.yaml
- ⬜ Subtask 2.2.1: Integrate criticality levels into controlled_vocabularies section
- ⬜ Subtask 2.2.2: Integrate lifecycle gatekeepers into controlled_vocabularies section  
- ⬜ Subtask 2.2.3: Integrate domain codes and subdomain mappings into controlled_vocabularies section
- ⬜ Subtask 2.2.4: Integrate maturity levels and audience types into controlled_vocabularies section
- ⬜ Subtask 2.2.5: Update external_vocabularies references to point to consolidated sources

### 2.3 Validate New YAML Structures
- ⬜ Subtask 2.3.1: Verify YAML syntax is valid for both new files
- ⬜ Subtask 2.3.2: Cross-check that all original content is preserved in new structure
- ⬜ Subtask 2.3.3: Verify no content duplication or conflicts exist

## Phase 3: Update Generation Scripts

### 3.1 Update generate_frontmatter_registry.py
- ⬜ Subtask 3.1.1: Modify script to load consolidated controlled vocabularies from mt-schema-frontmatter.yaml
- ⬜ Subtask 3.1.2: Update script to load tag categories from mt-registry-tag-glossary.yaml
- ⬜ Subtask 3.1.3: Remove dependencies on deprecated YAML files (criticality_levels.yaml, etc.)
- ⬜ Subtask 3.1.4: Update generation logic for all .txt files to use consolidated sources

### 3.2 Update generate_schema_docs.py
- ⬜ Subtask 3.2.1: Modify script to read from consolidated YAML sources
- ⬜ Subtask 3.2.2: Update MD generation logic to populate sections from mt-registry-tag-glossary.yaml
- ⬜ Subtask 3.2.3: Ensure proper cross-references between generated documents

### 3.3 Test Updated Scripts
- ⬜ Subtask 3.3.1: Run dry-run tests of all updated scripts to verify functionality
- ⬜ Subtask 3.3.2: Compare generated output against previous versions for accuracy
- ⬜ Subtask 3.3.3: Validate that all expected files are generated correctly

## Phase 4: Update Validation and Linting

### 4.1 Update Linter Configuration
- ⬜ Subtask 4.1.1: Modify kb_linter.py to read controlled vocabularies from consolidated sources
- ⬜ Subtask 4.1.2: Update validation logic to use mt-schema-frontmatter.yaml for all controlled vocabulary checks
- ⬜ Subtask 4.1.3: Update tag validation to use mt-registry-tag-glossary.yaml

### 4.2 Update Other Validation Scripts
- ⬜ Subtask 4.2.1: Identify all scripts that reference deprecated YAML files
- ⬜ Subtask 4.2.2: Update each script to use consolidated sources
- ⬜ Subtask 4.2.3: Test validation accuracy with consolidated sources

### 4.3 Verify Validation Integrity
- ⬜ Subtask 4.3.1: Run comprehensive linting on existing documents to ensure no regressions
- ⬜ Subtask 4.3.2: Verify all controlled vocabulary validations work correctly
- ⬜ Subtask 4.3.3: Test edge cases and error conditions

## Phase 5: Migration and Cleanup

### 5.1 Move MT-REGISTRY-TAG-GLOSSARY.md to standards/src
- ⬜ Subtask 5.1.1: Move MT-REGISTRY-TAG-GLOSSARY.md from registry/ to src/ directory
- ⬜ Subtask 5.1.2: Update any internal references to the moved file
- ⬜ Subtask 5.1.3: Verify file accessibility and link integrity

### 5.2 Archive Deprecated Files
- ⬜ Subtask 5.2.1: Create timestamped archive directory for deprecated registry files
- ⬜ Subtask 5.2.2: Move all deprecated YAML files to archive with proper documentation
- ⬜ Subtask 5.2.3: Archive all deprecated generated .txt files

### 5.3 Final System Testing
- ⬜ Subtask 5.3.1: Run complete generation pipeline with live mode to test end-to-end
- ⬜ Subtask 5.3.2: Run comprehensive linting on entire repository to verify system integrity
- ⬜ Subtask 5.3.3: Generate completion report documenting all changes and new architecture

---

## Status Legend
- ⬜ Not started
- 🔄 In progress / Started
- ✅ Completed

## ⚠️ MANDATORY EXECUTION PROTOCOL

### 🔒 Sequential Execution Requirements
- **PHASES**: Must be completed in strict sequential order (1 → 2 → 3...)
- **TASKS**: Within each phase, tasks must be completed sequentially (1.1 → 1.2 → 1.3...)
- **SUBTASKS**: Within each task, subtasks must be completed sequentially (1.1.1 → 1.1.2 → 1.1.3...)

### 🚫 Blocking Conditions
- **NO PARALLEL EXECUTION** - Only one item may be worked on at a time
- **100% COMPLETION REQUIRED** - Next item cannot begin until current item is 100% complete
- **ZERO TOLERANCE FOR PARTIAL COMPLETION** - Any incomplete task blocks all subsequent work

### 🛑 Failure Protocol
**IF ANY TASK CANNOT BE 100% COMPLETED:**
1. **IMMEDIATELY ABORT** all execution
2. **GENERATE CONCISE REPORT** containing:
   - Failed task identification
   - Specific blocking issue(s)
   - Current completion status
   - Required resolution steps
3. **NO PROGRESSION** until blocking issue is resolved

### 📋 Progress Tracking
- Mark each item with appropriate status indicator
- Update status only upon 100% completion
- Document any dependencies or blocking issues immediately
