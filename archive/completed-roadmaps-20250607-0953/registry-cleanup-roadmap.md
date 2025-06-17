---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:13Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: archive
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# REGISTRY CLEANUP EXECUTION ROADMAP

>**THE "*🚨 MANDATORY* ROADMAP PROGRESS MANAGEMENT PROTOCOL" *MUST* BE FOLLOWED AND UPDATED AT ALL TIMES TO ENSURE THE PROGRESS IS ACTIVELY TRACKED AND WORK CAN BE RESUMED FROM THE SAME POINT WITHOUT CAUSING ANY CONFUSION AND REDUNDANCY, THE PROGRESS MUST BE UPDATED CONTINUOUSLY WITHOUT ANY EXCEPTION**

>**UPDATE THE CHECKLIST CONTINUOUSLY AT ALL TIMES WITHOUT ANY EXCEPTION**

**🚨 CRITICAL**: This plan must be actively managed and continuously updated throughout all execution stages. The structure and protocols are mandatory for successful project completion.

---

⬜ ## PROJECT OVERVIEW

**Purpose**: Complete the registry consolidation cleanup phase by fixing broken references to archived YAML files, updating scripts and generator tools, and ensuring all documentation and tooling functions correctly with the new consolidated registry structure.

**Scope**: Update remaining scripts, fix documentation references, update generator tools in builder and repo-tree utilities, update test files, and perform comprehensive validation to ensure system integrity.

**Outcome**: Fully functional system with no broken references to archived files, all scripts and tools working with consolidated registry sources, and complete documentation consistency.

---

⬜ ## PHASE 1: Script Reference Updates

Update all scripts that still reference archived YAML files to use the new consolidated registry sources.

---

⬜ **🏁 PHASE 1 EXIT CONDITIONS**: All scripts updated to use consolidated registry sources
⬜ **CONDITION 1**: refactor_criticality_field.py updated to use mt-schema-frontmatter.yaml
⬜ **CONDITION 2**: generate_naming_configs.py updated to use consolidated sources
⬜ **CONDITION 3**: All test files updated to use new registry structure
⬜ **CONDITION 4**: All scripts tested and verified to function correctly

---

⬜ ### STEP 1.1: Update refactor_criticality_field.py

Update the criticality field refactor script to load data from the consolidated mt-schema-frontmatter.yaml instead of the archived criticality_levels.yaml.

---

⬜ **🏁 STEP 1.1 EXIT CONDITIONS**: Script successfully updated and tested
⬜ **CONDITION 1**: Script modified to load from mt-schema-frontmatter.yaml controlled_vocabularies section
⬜ **CONDITION 2**: Script tested with dry-run to verify functionality
⬜ **CONDITION 3**: Documentation updated to reflect new data source

---

⬜ #### TASK 1.1.1: Modify YAML Loading Logic
🎬 Update the script to load criticality levels from master-knowledge-base/standards/registry/mt-schema-frontmatter.yaml controlled_vocabularies.criticality section instead of criticality_levels.yaml

⬜ #### TASK 1.1.2: Update File Path References
🎬 Change all file path references from criticality_levels.yaml to mt-schema-frontmatter.yaml and update the data extraction logic to navigate the controlled_vocabularies structure

⬜ #### TASK 1.1.3: Test Script Functionality
🎬 Execute the script with --dry-run flag to verify it correctly loads and processes criticality data from the new consolidated source

---

⬜ ### STEP 1.2: Update generate_naming_configs.py

Update the naming configuration generator to use consolidated registry sources instead of archived domain_codes.yaml.

---

⬜ **🏁 STEP 1.2 EXIT CONDITIONS**: Script successfully updated and tested
⬜ **CONDITION 1**: Script modified to use consolidated registry sources
⬜ **CONDITION 2**: Script tested to verify correct configuration generation
⬜ **CONDITION 3**: Generated configurations validated for accuracy

---

⬜ #### TASK 1.2.1: Identify Current Dependencies
🎬 Analyze generate_naming_configs.py to identify all references to domain_codes.yaml and other archived files

⬜ #### TASK 1.2.2: Update Data Source References
🎬 Modify the script to load domain codes from mt-schema-frontmatter.yaml controlled_vocabularies section instead of domain_codes.yaml

⬜ #### TASK 1.2.3: Test Configuration Generation
🎬 Execute the script to verify it generates correct naming configurations using the consolidated data sources

---

⬜ ### STEP 1.3: Update Test Files

Update all test files that create or reference archived YAML files to use the new consolidated registry structure.

---

⬜ **🏁 STEP 1.3 EXIT CONDITIONS**: All test files updated and passing
⬜ **CONDITION 1**: test_kb_linter.py updated to create consolidated YAML structure
⬜ **CONDITION 2**: All test files execute successfully
⬜ **CONDITION 3**: Test coverage maintained for new registry structure

---

⬜ #### TASK 1.3.1: Update test_kb_linter.py
🎬 Modify test_kb_linter.py to create mt-schema-frontmatter.yaml and mt-registry-tag-glossary.yaml instead of individual archived YAML files

⬜ #### TASK 1.3.2: Update Test Data Structure
🎬 Ensure test data matches the consolidated YAML structure with controlled_vocabularies sections

⬜ #### TASK 1.3.3: Execute Test Suite
🎬 Run all tests to verify they pass with the updated registry structure

---

⬜ ## PHASE 2: Documentation Reference Updates

Update all manually written documentation that contains broken references to archived YAML files.

---

⬜ **🏁 PHASE 2 EXIT CONDITIONS**: All documentation references updated and validated
⬜ **CONDITION 1**: Template files updated to reference consolidated sources
⬜ **CONDITION 2**: Standards documentation updated with correct references
⬜ **CONDITION 3**: All wiki-links validated and functional
⬜ **CONDITION 4**: Documentation consistency verified

---

⬜ ### STEP 2.1: Update Template Files

Update template files that reference archived YAML files to point to consolidated sources.

---

⬜ **🏁 STEP 2.1 EXIT CONDITIONS**: All template files updated with correct references
⬜ **CONDITION 1**: UA-TPL-CANONICAL-FRONTMATTER.md updated
⬜ **CONDITION 2**: All template references validated
⬜ **CONDITION 3**: Template functionality verified

---

⬜ #### TASK 2.1.1: Update Canonical Frontmatter Template
🎬 Update UA-TPL-CANONICAL-FRONTMATTER.md to reference mt-schema-frontmatter.yaml instead of domain_codes.yaml and subdomain_registry.yaml

⬜ #### TASK 2.1.2: Verify Template References
🎬 Check all template files for any remaining references to archived YAML files and update them to point to consolidated sources

---

⬜ ### STEP 2.2: Update Standards Documentation

Update standards documentation files that contain broken wiki-links to archived files.

---

⬜ **🏁 STEP 2.2 EXIT CONDITIONS**: All standards documentation updated
⬜ **CONDITION 1**: QM-VALIDATION-METADATA.md updated
⬜ **CONDITION 2**: GM-REGISTRY-GOVERNANCE.md updated
⬜ **CONDITION 3**: GM-GLOSSARY-STANDARDS-TERMS.md updated
⬜ **CONDITION 4**: GM-CONVENTIONS-NAMING.md updated
⬜ **CONDITION 5**: AS-KB-DIRECTORY-STRUCTURE.md updated

---

⬜ #### TASK 2.2.1: Update Validation Metadata Documentation
🎬 Update QM-VALIDATION-METADATA.md to reference mt-schema-frontmatter.yaml instead of archived domain_codes.yaml and subdomain_registry.yaml

⬜ #### TASK 2.2.2: Update Registry Governance Documentation
🎬 Update GM-REGISTRY-GOVERNANCE.md to reference consolidated registry sources instead of archived files

⬜ #### TASK 2.2.3: Update Glossary Documentation
🎬 Update GM-GLOSSARY-STANDARDS-TERMS.md to reference consolidated sources for domain and subdomain definitions

⬜ #### TASK 2.2.4: Update Naming Conventions Documentation
🎬 Update GM-CONVENTIONS-NAMING.md to reference consolidated registry sources instead of archived files

⬜ #### TASK 2.2.5: Update Directory Structure Documentation
🎬 Update AS-KB-DIRECTORY-STRUCTURE.md to reference consolidated registry sources in examples

---

⬜ ## PHASE 3: Generator Tool Updates

Update generator tools in builder and repo-tree utilities to work with consolidated registry structure.

---

⬜ **🏁 PHASE 3 EXIT CONDITIONS**: All generator tools updated and functional
⬜ **CONDITION 1**: Builder tools updated to use consolidated sources
⬜ **CONDITION 2**: Repo-tree tools updated to reflect current structure
⬜ **CONDITION 3**: Generated files validated for accuracy
⬜ **CONDITION 4**: All generator tools tested successfully

---

⬜ ### STEP 3.1: Update Builder Tools

Update tools in master-knowledge-base/tools/builder to use consolidated registry sources for generating collection documents.

---

⬜ **🏁 STEP 3.1 EXIT CONDITIONS**: Builder tools updated and generating correct output
⬜ **CONDITION 1**: All builder scripts identified and analyzed
⬜ **CONDITION 2**: Scripts updated to use consolidated sources
⬜ **CONDITION 3**: Generated collection documents validated

---

⬜ #### TASK 3.1.1: Analyze Builder Tool Dependencies
🎬 Examine all scripts in master-knowledge-base/tools/builder to identify references to archived YAML files

⬜ #### TASK 3.1.2: Update Builder Data Sources
🎬 Modify builder tools to load data from mt-schema-frontmatter.yaml and mt-registry-tag-glossary.yaml instead of archived files

⬜ #### TASK 3.1.3: Test Collection Generation
🎬 Execute builder tools to generate collection documents and verify they contain correct references to consolidated sources

---

⬜ ### STEP 3.2: Update Repo-Tree Tools

Update tools in master-knowledge-base/tools/utilities/repo-tree to reflect the current repository structure without archived files.

---

⬜ **🏁 STEP 3.2 EXIT CONDITIONS**: Repo-tree tools updated and generating accurate structure
⬜ **CONDITION 1**: Repo-tree generator analyzed and updated
⬜ **CONDITION 2**: Generated repo-tree.md reflects current structure
⬜ **CONDITION 3**: Archive directory properly represented

---

⬜ #### TASK 3.2.1: Analyze Repo-Tree Generator
🎬 Examine the repo-tree generation tool to understand how it scans and represents the repository structure

⬜ #### TASK 3.2.2: Update Structure Representation
🎬 Ensure the repo-tree generator correctly represents the current registry structure with consolidated files and archive directory

⬜ #### TASK 3.2.3: Generate Updated Repository Tree
🎬 Execute the repo-tree generator to create an updated repo-tree.md that accurately reflects the post-consolidation structure

---

⬜ ## PHASE 4: Testing and Validation

Perform comprehensive testing and validation to ensure all systems function correctly with the consolidated registry structure.

---

⬜ **🏁 PHASE 4 EXIT CONDITIONS**: Complete system validation successful
⬜ **CONDITION 1**: All scripts execute successfully
⬜ **CONDITION 2**: All generator tools produce correct output
⬜ **CONDITION 3**: Documentation links validated
⬜ **CONDITION 4**: Linter validation passes
⬜ **CONDITION 5**: End-to-end system test successful

---

⬜ ### STEP 4.1: Script Validation Testing

Execute all updated scripts to verify they function correctly with consolidated registry sources.

---

⬜ **🏁 STEP 4.1 EXIT CONDITIONS**: All scripts validated and functional
⬜ **CONDITION 1**: refactor_criticality_field.py tested successfully
⬜ **CONDITION 2**: generate_naming_configs.py tested successfully
⬜ **CONDITION 3**: All test suites pass
⬜ **CONDITION 4**: No errors or warnings in script execution

---

⬜ #### TASK 4.1.1: Test Criticality Field Script
🎬 Execute refactor_criticality_field.py with both dry-run and live modes to verify correct functionality

⬜ #### TASK 4.1.2: Test Naming Config Generator
🎬 Execute generate_naming_configs.py to verify it generates correct configurations from consolidated sources

⬜ #### TASK 4.1.3: Execute Full Test Suite
🎬 Run all unit tests and integration tests to ensure no regressions were introduced

---

⬜ ### STEP 4.2: Generator Tool Validation

Validate that all generator tools produce correct and consistent output.

---

⬜ **🏁 STEP 4.2 EXIT CONDITIONS**: All generator tools validated
⬜ **CONDITION 1**: Collection documents generated correctly
⬜ **CONDITION 2**: Repository tree reflects accurate structure
⬜ **CONDITION 3**: Generated content validated for consistency

---

⬜ #### TASK 4.2.1: Validate Collection Generation
🎬 Execute builder tools and verify generated collection documents contain correct references and no broken links

⬜ #### TASK 4.2.2: Validate Repository Tree Generation
🎬 Execute repo-tree generator and verify the output accurately represents the current repository structure

---

⬜ ### STEP 4.3: System Integration Testing

Perform end-to-end testing to ensure the entire system functions cohesively.

---

⬜ **🏁 STEP 4.3 EXIT CONDITIONS**: Complete system integration validated
⬜ **CONDITION 1**: Linter validation passes on all content
⬜ **CONDITION 2**: All documentation links functional
⬜ **CONDITION 3**: No broken references detected
⬜ **CONDITION 4**: System ready for production use

---

⬜ #### TASK 4.3.1: Execute Comprehensive Linting
🎬 Run kb_linter.py on all content directories to verify no validation errors with consolidated registry structure

⬜ #### TASK 4.3.2: Validate Documentation Links
🎬 Systematically check all documentation for broken links or references to non-existent files

⬜ #### TASK 4.3.3: Perform End-to-End System Test
🎬 Execute a complete workflow from content creation through validation to ensure all components work together correctly

---

⬜ **🏁 PROJECT EXIT CONDITIONS**: Registry cleanup completely successful and system ready for merge
⬜ **CONDITION 1**: All scripts updated and functional with consolidated sources
⬜ **CONDITION 2**: All documentation references corrected and validated
⬜ **CONDITION 3**: All generator tools updated and producing correct output
⬜ **CONDITION 4**: Comprehensive testing completed with zero errors
⬜ **CONDITION 5**: System integration validated and ready for production use

---

## STATUS LEGEND

⬜ **NOT STARTED**
🔄 **IN PROGRESS**
✅ **COMPLETED**
❌ **BLOCKED**

**NOTE:** ***🔄 IN PROGRESS and ❌ BLOCKED statuses must be applied to all the affected parent branches all the way up to the project level***

---

## EXECUTION PROTOCOL

### **SEQUENTIAL PROGRESSION**

- **PHASES**: Must complete 1 → 2 → 3 → 4
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

#### **OPTION A: DIRECT ROADMAP UPDATES** (for shorter roadmaps)
- **UPDATE** status checkboxes continuously in the roadmap
- **ADD** one-liner notes directly to roadmap items for important points
- **MAINTAIN** separate detailed progress tracker document

#### **OPTION B: SEPARATE PROGRESS CHECKLIST** (for longer roadmaps)
- **GENERATE** separate progress checklist file with tree-structure matching roadmap ToC
- **UPDATE** status checkboxes in the separate checklist
- **ADD** one-liner notes to the checklist items (NOT the roadmap)
- **MAINTAIN** separate detailed progress tracker document

### **MANDATORY UPDATES**

1. **STATUS TRACKING**: Update checkboxes continuously (refer to status legend)
2. **ONE-LINER NOTES**: Add important execution points (roadmap OR checklist based on option chosen)
3. **DETAILED PROGRESS**: Update progress tracker document after each completion
