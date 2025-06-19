---
title: "LLM Implementation Prompt: Ultimate Frontmatter Enhancement Guideline"
info-type: technical-prompt
version: 1.0.0
date-created: '2025-01-01T00:00:00Z'
date-modified: '2025-01-01T00:00:00Z'
tags:
- content-type/technical-prompt
- criticality/p0-critical
- domain/automation-implementation
kb-id: LLM-PROMPT-ULT-FMNT-ENH-IMPL
primary-topic: frontmatter-enhancement-implementation
scope_application: master-knowledge-base
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: [standards-infrastructure, automation, validation]
---

# LLM IMPLEMENTATION PROMPT: ULTIMATE FRONTMATTER ENHANCEMENT GUIDELINE

**Target Implementation:** `ultimate-frontmatter-enhancement-guideline-20250617-0312.md`  
**Implementation Approach:** Complete execution of all phases as specified  
**Success Criteria:** 100% automation with zero manual fallbacks  

---

## EXECUTION DIRECTIVE

You are tasked with implementing the **complete specifications** contained in `ultimate-frontmatter-enhancement-guideline-20250617-0312.md`. This document contains comprehensive, step-by-step implementation instructions for a sophisticated frontmatter enhancement system.

### CRITICAL IMPLEMENTATION REQUIREMENTS

**YOU MUST FOLLOW THESE NON-NEGOTIABLE RULES:**

1. **TREAT THE GUIDELINE AS EXECUTABLE SPECIFICATIONS** - Every code snippet, class definition, and implementation step in the guideline is a direct instruction to be implemented exactly as specified.

2. **IMPLEMENT ALL FIVE PHASES SEQUENTIALLY** - Do not skip phases or implement out of order:
   - Phase 1: Robust Document Type Analysis Methodology
   - Phase 2: Detailed SHACL-to-Markdown Generator Implementation  
   - Phase 3: Comprehensive Scribe LLM Integration Enhancement
   - Phase 4: Universal kb_id Strategy Implementation
   - Phase 5: Controlled CI/CD Setup (Disabled Until Approval)

3. **100% AUTOMATION REQUIREMENT** - No manual fallbacks allowed. Every component must have deterministic success guarantees.

4. **LEVERAGE EXISTING INFRASTRUCTURE** - Enhance the existing sophisticated SHACL/JSON-LD/Scribe systems, do not replace them.

5. **REPOSITORY WORK ETHIC COMPLIANCE** - Follow all repository guidelines:
   - Work exclusively on feature branches (never commit to main)
   - Use sequential planning (no time-based planning)
   - Log all operations to `./tools/reports/`
   - Activate conda-kb environment before operations
   - Archive (never delete) any existing files

---

## IMPLEMENTATION EXECUTION PLAN

### PHASE 1: DOCUMENT TYPE ANALYSIS METHODOLOGY

**Primary Target:** `tools/analysis/document_type_analyzer.py`

**Implementation Requirements:**
- Create the `UniversalDocumentTypeAnalyzer` class exactly as specified in the guideline
- Implement all methods: `analyze_on_demand()`, `_analyze_content_patterns()`, `_analyze_structural_patterns()`, `_analyze_metadata_patterns()`, `_analyze_path_patterns()`, `generate_kb_import_profile()`
- Create the CLI interface: `tools/analysis/analyze_document_types.py`
- Implement automated profile generation functions
- **Success Criteria:** Analyzer can process current repository AND scale for future KB imports

### PHASE 2: SHACL-TO-MARKDOWN GENERATOR

**Primary Target:** `tools/builder/shacl_parser.py`, `tools/builder/profile_categorizer.py`, `tools/builder/markdown_template_generator.py`

**Implementation Requirements:**
- Create `SHACLParser` class with `extract_validation_rules()` method implementing all 7 sub-steps
- Create `ProfileCategorizer` class with profile hierarchy generation
- Create `MarkdownTemplateGenerator` class with concise documentation generation (target <180 lines)
- Create `AutoDocumentationWorkflow` class for complete generation cycle
- **Success Criteria:** Automatically generates `MT-SCHEMA-FRONTMATTER.md` from SHACL shapes with <180 lines

### PHASE 3: SCRIBE LLM INTEGRATION

**Primary Target:** `tools/scribe/integrations/llm_integration.py`, `tools/scribe/prompts/schema_constraint_prompts.py`, `tools/scribe/validation/llm_shacl_validator.py`

**Implementation Requirements:**
- Create `LLMSchemaIntegration` class with schema-constrained generation
- Create `SchemaConstraintPromptEngine` class with SHACL-to-prompt conversion
- Create `LLMSHACLValidator` class with validation retry loop (max 5 attempts + deterministic fallback)
- Create `LLMErrorHandler` class for comprehensive error handling
- Create `EnhancedFrontmatterAction` class integrating with existing Scribe workflow
- **Success Criteria:** 100% success rate in generating valid frontmatter with SHACL compliance

### PHASE 4: UNIVERSAL KB_ID STRATEGY

**Primary Target:** `standards/registry/shacl-shapes.ttl`, `tools/refactoring-scripts/universal_kb_id_migration.py`

**Implementation Requirements:**
- Update SHACL shapes with universal kb_id requirements and field scope corrections
- Create `UniversalKbIdMigrator` class for repository-wide scope corrections
- Implement field scope logic: kb_id mandatory for ALL, standard_id only for standards
- **Success Criteria:** Zero field scope violations across repository, 100% kb_id coverage

### PHASE 5: CONTROLLED CI/CD SETUP

**Primary Target:** `.pre-commit-config.yaml`, `.github/workflows/frontmatter-validation.yml`, `tools/validation/on_demand_validator.py`

**Implementation Requirements:**
- Create pre-commit configuration (commented out by default)
- Create GitHub Actions workflow (feature-flagged, disabled by default)
- Create `OnDemandValidator` class for immediate validation capabilities
- **Success Criteria:** CI/CD infrastructure ready but inactive until approval

---

## TECHNICAL IMPLEMENTATION GUIDELINES

### CODE QUALITY REQUIREMENTS

1. **Follow Python Best Practices:**
   - Type hints for all function signatures
   - Comprehensive docstrings with step-by-step explanations
   - Error handling for all possible failure modes
   - Logging to `tools/reports/` for all operations

2. **SHACL/RDF Integration:**
   - Use existing `rdflib` infrastructure
   - Parse existing `standards/registry/shacl-shapes.ttl`
   - Leverage existing graph validator patterns
   - Maintain compatibility with existing JSON-LD contexts

3. **Scribe System Integration:**
   - Inherit from existing `BaseAction` class
   - Follow existing Scribe patterns and interfaces
   - Integrate with existing action registration system
   - Maintain compatibility with existing engine architecture

### VALIDATION AND TESTING

1. **Implement Built-in Validation:**
   - Every component must validate its own outputs
   - SHACL validation integration mandatory
   - Comprehensive error reporting and logging

2. **Success Metrics Verification:**
   - Line count verification for generated documentation
   - SHACL compliance verification for all generated frontmatter
   - Repository-wide validation sweep
   - Performance metrics logging

### FILE ORGANIZATION

**Create these new files exactly as specified:**
```
tools/analysis/
├── document_type_analyzer.py
└── analyze_document_types.py

tools/builder/
├── shacl_parser.py
├── profile_categorizer.py
├── markdown_template_generator.py
└── auto_doc_workflow.py

tools/scribe/integrations/
└── llm_integration.py

tools/scribe/prompts/
└── schema_constraint_prompts.py

tools/scribe/validation/
└── llm_shacl_validator.py

tools/scribe/error_handling/
└── llm_error_handler.py

tools/scribe/actions/
└── enhanced_frontmatter_action.py

tools/refactoring-scripts/
└── universal_kb_id_migration.py

tools/validation/
└── on_demand_validator.py

.github/workflows/
└── frontmatter-validation.yml

.pre-commit-config.yaml (if doesn't exist)
```

---

## EXECUTION WORKFLOW

### STEP 1: ENVIRONMENT PREPARATION
```bash
# Activate conda environment
conda activate conda-kb

# Create feature branch
git checkout -b feature/ultimate-frontmatter-enhancement

# Generate current repository state
python repo_tree.py
```

### STEP 2: SEQUENTIAL IMPLEMENTATION
1. Implement Phase 1 (Document Type Analysis)
2. Test Phase 1 thoroughly
3. Implement Phase 2 (SHACL-to-Markdown Generator)
4. Test Phase 2 thoroughly
5. Implement Phase 3 (Scribe LLM Integration)
6. Test Phase 3 thoroughly
7. Implement Phase 4 (Universal kb_id Strategy)
8. Test Phase 4 thoroughly
9. Implement Phase 5 (Controlled CI/CD Setup)
10. Final validation and testing

### STEP 3: VALIDATION AND REPORTING
```bash
# Run comprehensive validation
python tools/validation/on_demand_validator.py --full-repository

# Generate implementation report
python tools/analysis/analyze_document_types.py --post-implementation-analysis

# Log all results to tools/reports/
```

---

## SUCCESS VERIFICATION CHECKLIST

**YOU MUST VERIFY ALL OF THESE BEFORE CONSIDERING IMPLEMENTATION COMPLETE:**

- [ ] `UniversalDocumentTypeAnalyzer` can analyze current repository
- [ ] `UniversalDocumentTypeAnalyzer` can generate KB import profiles
- [ ] SHACL parser extracts all validation rules correctly
- [ ] Markdown generator produces documentation under 180 lines
- [ ] LLM integration achieves 100% success rate with retry loop
- [ ] Universal kb_id strategy eliminates all field scope violations
- [ ] CI/CD infrastructure exists but remains disabled
- [ ] All generated code follows existing repository patterns
- [ ] All operations log to `tools/reports/`
- [ ] Repository-wide SHACL validation passes 100%
- [ ] No manual fallbacks required anywhere in the system

---

## CRITICAL REMINDERS

1. **THIS IS NOT A PLANNING EXERCISE** - The guideline contains complete implementation specifications. Execute them exactly as written.

2. **100% AUTOMATION IS MANDATORY** - Any component that might require manual intervention must have a deterministic fallback.

3. **LEVERAGE EXISTING SOPHISTICATION** - The repository already has advanced SHACL/JSON-LD/Scribe infrastructure. Enhance it, don't replace it.

4. **SEQUENTIAL EXECUTION ONLY** - Complete each phase fully before moving to the next. No parallel development or time-based planning.

5. **COMPREHENSIVE LOGGING** - Every operation, every decision, every generated artifact must be logged to `tools/reports/` with timestamps.

---

## FINAL DIRECTIVE

**EXECUTE THE ULTIMATE FRONTMATTER ENHANCEMENT GUIDELINE COMPLETELY AND EXACTLY AS SPECIFIED. NO SHORTCUTS, NO COMPROMISES, NO EXCEPTIONS.**

The guideline represents months of analysis and design work. Your task is implementation, not interpretation. Follow the specifications precisely to achieve the sophisticated automation system described.

**BEGIN IMPLEMENTATION IMMEDIATELY.** 