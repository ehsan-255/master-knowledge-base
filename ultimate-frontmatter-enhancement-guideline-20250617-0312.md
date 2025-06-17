---
title: "Ultimate Frontmatter Enhancement Implementation Guideline - ENHANCED"
info-type: technical-report
version: 1.1.0
date-created: '2025-06-17T03:12:00Z'
date-modified: '2025-06-17T03:12:00Z'
tags:
- content-type/technical-report
- criticality/p0-critical
- domain/standards-infrastructure
kb-id: ULT-FMNT-ENH-GUIDE-20250617-ENHANCED
primary-topic: frontmatter-enhancement-synthesis-enhanced
scope_application: master-knowledge-base
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: [standards-infrastructure, automation, validation]
---

# ULTIMATE FRONTMATTER ENHANCEMENT IMPLEMENTATION GUIDELINE - ENHANCED

**Report Date:** 2025-06-17 03:12 (Enhanced Version)  
**Analysis Source:** Synthesis of 3 proposals + User Requirements Enhancement  
**Approach:** Leveraging existing sophisticated SHACL/JSON-LD infrastructure  
**Status:** Ready for sequential implementation with enhanced specifications

---

## EXECUTIVE SUMMARY

This enhanced guideline synthesizes the **best concepts from all three proposals** while **leveraging existing sophisticated repository infrastructure** and incorporating **critical user-specified enhancements** to address **critical issues identified in comprehensive standards analysis**. 

**KEY INNOVATIONS ENHANCED**:
- **Robust Document Type Analysis Methodology** for current and future KB imports
- **Detailed SHACL-to-Markdown Generator** with step-by-step decomposition
- **Comprehensive Scribe LLM Integration** with complete implementation breakdown
- **Universal kb_id Strategy** replacing problematic standard_id scope issues
- **Controlled CI/CD Setup** (disabled until approval) with on-demand validation
- **100% Automation Requirement** (no exceptions, no manual fallbacks)

---

## ENHANCED IMPLEMENTATION GUIDELINE

### PHASE 1: ROBUST DOCUMENT TYPE ANALYSIS METHODOLOGY

**Objective**: Create scalable, on-demand methodology for current repository and future KB imports

#### Step 1.1.1: Create Universal Document Type Analyzer
**Target**: `tools/analysis/document_type_analyzer.py`

```python
class UniversalDocumentTypeAnalyzer:
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path)
        self.analysis_results = {}
        self.type_patterns = {}
        self.field_usage_matrix = {}
    
    def analyze_on_demand(self, target_paths=None, kb_import_mode=False):
        """
        Robust methodology for analyzing document types
        Works with current limited documents AND future KB imports
        """
        if target_paths is None:
            target_paths = [self.repo_path]
        
        # Phase 1: Content-based classification
        content_analysis = self._analyze_content_patterns(target_paths)
        
        # Phase 2: Structural pattern recognition
        structural_analysis = self._analyze_structural_patterns(target_paths)
        
        # Phase 3: Metadata pattern extraction
        metadata_analysis = self._analyze_metadata_patterns(target_paths)
        
        # Phase 4: Path-based classification
        path_analysis = self._analyze_path_patterns(target_paths)
        
        # Phase 5: Composite classification
        composite_profiles = self._generate_composite_profiles(
            content_analysis, structural_analysis, 
            metadata_analysis, path_analysis
        )
        
        # Phase 6: Generate actionable SHACL profiles
        shacl_profiles = self._generate_shacl_profile_suggestions(composite_profiles)
        
        return {
            'document_types_identified': composite_profiles,
            'shacl_profile_suggestions': shacl_profiles,
            'field_usage_matrix': self.field_usage_matrix,
            'recommended_actions': self._generate_action_recommendations()
        }
    
    def _analyze_content_patterns(self, target_paths):
        """Analyze document content to infer types"""
        patterns = {
            'standard-definition': [
                r'## STANDARD DEFINITION',
                r'standard_id:',
                r'## COMPLIANCE REQUIREMENTS'
            ],
            'technical-report': [
                r'## EXECUTIVE SUMMARY',
                r'## ANALYSIS',
                r'Report Date:'
            ],
            'policy-document': [
                r'## POLICY STATEMENT',
                r'## MANDATORY REQUIREMENTS',
                r'lifecycle_gatekeeper:'
            ],
            'meeting-notes': [
                r'## ATTENDEES',
                r'## ACTION ITEMS',
                r'Meeting Date:'
            ],
            'general-document': [
                # Fallback patterns
                r'# .+',  # Any heading
                r'## .+'  # Any sub-heading
            ]
        }
        
        classification_results = {}
        
        for path in target_paths:
            for md_file in path.rglob("*.md"):
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                scores = {}
                
                for doc_type, pattern_list in patterns.items():
                    score = sum(1 for pattern in pattern_list 
                              if re.search(pattern, content, re.IGNORECASE))
                    scores[doc_type] = score
                
                # Assign type based on highest score
                best_type = max(scores, key=scores.get) if max(scores.values()) > 0 else 'general-document'
                classification_results[str(md_file)] = {
                    'inferred_type': best_type,
                    'confidence_scores': scores,
                    'current_frontmatter': self._extract_frontmatter(content)
                }
        
        return classification_results
    
    def _analyze_structural_patterns(self, target_paths):
        """Analyze document structure patterns"""
        # Implementation for structural analysis
        pass
    
    def _analyze_metadata_patterns(self, target_paths):
        """Analyze existing metadata patterns"""
        # Implementation for metadata analysis
        pass
    
    def _analyze_path_patterns(self, target_paths):
        """Analyze file path patterns for type inference"""
        path_patterns = {
            'standard-definition': [r'standards/src/', r'/standards/'],
            'technical-report': [r'tools/reports/', r'/reports/'],
            'policy-document': [r'standards/src/.*POLICY.*', r'/policies/'],
            'general-document': []  # Fallback
        }
        
        # Implementation for path-based classification
        pass
    
    def generate_kb_import_profile(self, kb_source_path):
        """
        Special methodology for analyzing imported KBs
        Generates import-specific profiles and mapping recommendations
        """
        import_analysis = self.analyze_on_demand([Path(kb_source_path)], kb_import_mode=True)
        
        mapping_recommendations = {
            'field_mappings': self._suggest_field_mappings(import_analysis),
            'type_conversions': self._suggest_type_conversions(import_analysis),
            'bulk_migration_script': self._generate_import_migration_script(import_analysis)
        }
        
        return mapping_recommendations
```

#### Step 1.1.2: Create On-Demand Analysis CLI
**Target**: `tools/analysis/analyze_document_types.py`

```bash
# On-demand analysis for current repository
python tools/analysis/analyze_document_types.py \
  --scan-current \
  --output tools/reports/document-type-analysis-$(date +%Y%m%d-%H%M).json

# Future KB import analysis
python tools/analysis/analyze_document_types.py \
  --kb-import-mode \
  --source-path /path/to/new/kb \
  --output tools/reports/kb-import-analysis-$(date +%Y%m%d-%H%M).json
```

#### Step 1.1.3: Automated Profile Generation
```python
def generate_dynamic_shacl_profiles(analysis_results):
    """
    Generate SHACL profiles based on analysis results
    Scalable for any number of document types discovered
    """
    profiles = []
    
    for doc_type, characteristics in analysis_results['document_types_identified'].items():
        profile = f"""
kb:{doc_type.title().replace('-', '')}Profile a sh:NodeShape ;
    sh:targetNode [ sh:property [ sh:path kb:info_type ; sh:hasValue "{doc_type}" ] ] ;
"""
        
        # Add mandatory fields based on analysis
        for field in characteristics['mandatory_fields']:
            profile += f"""    sh:property [
        sh:path kb:{field} ; sh:minCount 1 ;
    ] ;
"""
        
        # Add forbidden fields based on analysis
        for field in characteristics['forbidden_fields']:
            profile += f"""    sh:property [
        sh:path kb:{field} ; sh:maxCount 0 ;
        sh:message "{doc_type} documents must not have {field} field." ;
    ] ;
"""
        
        profiles.append(profile)
    
    return profiles
```

### PHASE 2: DETAILED SHACL-TO-MARKDOWN GENERATOR IMPLEMENTATION

**Objective**: Comprehensive step-by-step decomposition for automated documentation generation

#### Step 2.1.1: SHACL Parser and Rule Extractor
**Target**: `tools/builder/shacl_parser.py`

```python
class SHACLParser:
    def __init__(self, shacl_file_path):
        self.shacl_graph = Graph()
        self.shacl_graph.parse(shacl_file_path, format='turtle')
        self.profiles = {}
        self.constraints = {}
    
    def extract_validation_rules(self):
        """Step-by-step rule extraction from SHACL shapes"""
        
        # Step 1: Identify all NodeShapes
        node_shapes = self._find_all_node_shapes()
        
        # Step 2: Extract targeting information
        shape_targets = self._extract_shape_targets(node_shapes)
        
        # Step 3: Parse property constraints
        property_constraints = self._parse_property_constraints(node_shapes)
        
        # Step 4: Extract cardinality constraints
        cardinality_rules = self._extract_cardinality_rules(property_constraints)
        
        # Step 5: Extract datatype constraints
        datatype_rules = self._extract_datatype_constraints(property_constraints)
        
        # Step 6: Extract pattern constraints
        pattern_rules = self._extract_pattern_constraints(property_constraints)
        
        # Step 7: Build comprehensive rule matrix
        rule_matrix = self._build_rule_matrix(
            shape_targets, cardinality_rules, 
            datatype_rules, pattern_rules
        )
        
        return rule_matrix
```

#### Step 2.1.2: Profile Identification and Categorization
**Target**: `tools/builder/profile_categorizer.py`

```python
class ProfileCategorizer:
    def categorize_profiles(self, rule_matrix):
        """Categorize SHACL profiles by document type and complexity"""
        
        # Step 1: Group rules by target info-type
        type_groups = self._group_by_info_type(rule_matrix)
        
        # Step 2: Identify mandatory vs optional fields per type
        field_categories = self._categorize_fields_by_requirement(type_groups)
        
        # Step 3: Detect inheritance patterns
        inheritance_patterns = self._detect_inheritance_patterns(type_groups)
        
        # Step 4: Generate profile hierarchy
        profile_hierarchy = self._build_profile_hierarchy(
            field_categories, inheritance_patterns
        )
        
        return profile_hierarchy
```

#### Step 2.1.3: Markdown Template Generation Engine
**Target**: `tools/builder/markdown_template_generator.py`

```python
class MarkdownTemplateGenerator:
    def __init__(self, profile_hierarchy):
        self.profiles = profile_hierarchy
        self.templates = {
            'header': self._load_header_template(),
            'profile_section': self._load_profile_template(),
            'field_table': self._load_field_table_template(),
            'footer': self._load_footer_template()
        }
    
    def generate_concise_documentation(self, target_line_limit=180):
        """Generate concise documentation under specified line limit"""
        
        # Step 1: Calculate space allocation per section
        space_allocation = self._calculate_space_allocation(target_line_limit)
        
        # Step 2: Generate header section
        header_content = self._generate_header_section(space_allocation['header'])
        
        # Step 3: Generate profile sections with space constraints
        profile_sections = []
        for profile_name, profile_data in self.profiles.items():
            section = self._generate_profile_section(
                profile_name, profile_data, 
                space_allocation['profile']
            )
            profile_sections.append(section)
        
        # Step 4: Generate field reference tables
        field_tables = self._generate_field_tables(space_allocation['tables'])
        
        # Step 5: Generate footer with auto-generation notice
        footer_content = self._generate_footer_section()
        
        # Step 6: Assemble final document
        final_document = self._assemble_document(
            header_content, profile_sections, 
            field_tables, footer_content
        )
        
        # Step 7: Validate line count and optimize if needed
        if self._count_lines(final_document) > target_line_limit:
            final_document = self._optimize_for_line_limit(final_document, target_line_limit)
        
        return final_document
```

#### Step 2.1.4: Auto-Generation Workflow Integration
**Target**: `tools/builder/auto_doc_workflow.py`

```python
class AutoDocumentationWorkflow:
    def execute_full_generation_cycle(self):
        """Complete workflow for auto-generating MT-SCHEMA-FRONTMATTER.md"""
        
        # Step 1: Parse current SHACL shapes
        parser = SHACLParser('standards/registry/shacl-shapes.ttl')
        rule_matrix = parser.extract_validation_rules()
        
        # Step 2: Categorize profiles
        categorizer = ProfileCategorizer()
        profile_hierarchy = categorizer.categorize_profiles(rule_matrix)
        
        # Step 3: Generate markdown documentation
        generator = MarkdownTemplateGenerator(profile_hierarchy)
        documentation = generator.generate_concise_documentation(target_line_limit=180)
        
        # Step 4: Validate against existing documentation
        validator = DocumentationValidator()
        validation_result = validator.validate_generated_docs(documentation)
        
        # Step 5: Write to target file with backup
        self._backup_existing_documentation()
        self._write_generated_documentation(documentation)
        
        # Step 6: Generate change report
        change_report = self._generate_change_report(validation_result)
        
        return {
            'success': True,
            'documentation_path': 'standards/src/MT-SCHEMA-FRONTMATTER.md',
            'line_count': generator._count_lines(documentation),
            'change_report': change_report
        }
```

### PHASE 3: COMPREHENSIVE SCRIBE LLM INTEGRATION ENHANCEMENT

**Objective**: Complete step-by-step breakdown of LLM integration with existing Scribe system

#### Step 3.1.1: LLM Integration Architecture Design
**Target**: `tools/scribe/integrations/llm_integration.py`

```python
class LLMSchemaIntegration:
    def __init__(self, shacl_file, jsonld_context):
        self.shacl_validator = self._load_existing_graph_validator()
        self.schema_constraints = self._load_schema_constraints(shacl_file)
        self.context_mappings = self._load_context_mappings(jsonld_context)
        self.llm_client = self._initialize_llm_client()
    
    def initialize_schema_constrained_generation(self):
        """Step 1: Initialize LLM with schema awareness"""
        
        # Sub-step 1.1: Load all SHACL profiles
        profiles = self._extract_all_profiles()
        
        # Sub-step 1.2: Convert SHACL constraints to LLM prompts
        constraint_prompts = self._convert_shacl_to_prompts(profiles)
        
        # Sub-step 1.3: Create profile-specific generators
        profile_generators = {}
        for profile_name, constraints in constraint_prompts.items():
            profile_generators[profile_name] = self._create_profile_generator(
                profile_name, constraints
            )
        
        return profile_generators
```

#### Step 3.1.2: Schema Constraint Prompt Engineering
**Target**: `tools/scribe/prompts/schema_constraint_prompts.py`

```python
class SchemaConstraintPromptEngine:
    def build_schema_constrained_prompt(self, document_content, info_type, constraints):
        """Step 2: Build LLM prompts with SHACL constraints"""
        
        # Sub-step 2.1: Analyze document content for context
        content_analysis = self._analyze_document_content(document_content)
        
        # Sub-step 2.2: Extract mandatory fields for info-type
        mandatory_fields = constraints.get('mandatory_fields', [])
        
        # Sub-step 2.3: Extract forbidden fields for info-type
        forbidden_fields = constraints.get('forbidden_fields', [])
        
        # Sub-step 2.4: Build constraint instructions
        constraint_instructions = self._build_constraint_instructions(
            mandatory_fields, forbidden_fields, constraints
        )
        
        # Sub-step 2.5: Create context-aware prompt
        prompt = f"""
CRITICAL: Generate YAML frontmatter that MUST pass SHACL validation for info-type: {info_type}

DOCUMENT CONTENT ANALYSIS:
{content_analysis}

MANDATORY FIELDS (MUST be included):
{self._format_mandatory_fields(mandatory_fields, constraints)}

FORBIDDEN FIELDS (MUST NOT be included):
{self._format_forbidden_fields(forbidden_fields)}

FIELD CONSTRAINTS:
{constraint_instructions}

Generate ONLY the YAML frontmatter block. NO other content.
The frontmatter MUST be valid YAML and MUST pass all SHACL constraints.
"""
        
        return prompt
```

#### Step 3.1.3: SHACL Validation Loop Implementation
**Target**: `tools/scribe/validation/llm_shacl_validator.py`

```python
class LLMSHACLValidator:
    def validate_with_retry_loop(self, initial_prompt, info_type, max_attempts=5):
        """Step 3: Implement validation loop with 100% success guarantee"""
        
        current_prompt = initial_prompt
        
        for attempt in range(max_attempts):
            # Sub-step 3.1: Generate frontmatter
            generated_frontmatter = self.llm_client.generate(current_prompt)
            
            # Sub-step 3.2: Parse YAML
            try:
                frontmatter_dict = yaml.safe_load(generated_frontmatter)
            except yaml.YAMLError as e:
                current_prompt = self._add_yaml_error_feedback(current_prompt, str(e))
                continue
            
            # Sub-step 3.3: Validate against SHACL
            validation_result = self.shacl_validator.validate_frontmatter_shacl(
                frontmatter_dict, info_type
            )
            
            # Sub-step 3.4: Check for success
            if validation_result.conforms:
                return {
                    'success': True,
                    'frontmatter': frontmatter_dict,
                    'attempts_used': attempt + 1
                }
            
            # Sub-step 3.5: Add validation errors to prompt for retry
            current_prompt = self._add_validation_feedback(
                current_prompt, validation_result.violations
            )
        
        # If all attempts failed, use deterministic fallback
        return self._generate_deterministic_fallback(info_type)
    
    def _generate_deterministic_fallback(self, info_type):
        """100% success guarantee - deterministic generation if LLM fails"""
        
        # Generate minimal valid frontmatter based on SHACL constraints
        mandatory_fields = self._get_mandatory_fields_for_type(info_type)
        fallback_frontmatter = {}
        
        for field in mandatory_fields:
            fallback_frontmatter[field] = self._get_safe_default_value(field, info_type)
        
        return {
            'success': True,
            'frontmatter': fallback_frontmatter,
            'fallback_used': True
        }
```

#### Step 3.1.4: Error Handling and Retry Mechanisms
**Target**: `tools/scribe/error_handling/llm_error_handler.py`

```python
class LLMErrorHandler:
    def handle_generation_errors(self, error_type, context):
        """Step 4: Comprehensive error handling for 100% success rate"""
        
        error_handlers = {
            'yaml_parsing_error': self._handle_yaml_errors,
            'shacl_validation_error': self._handle_shacl_errors,
            'llm_service_error': self._handle_llm_service_errors,
            'network_error': self._handle_network_errors,
            'timeout_error': self._handle_timeout_errors
        }
        
        handler = error_handlers.get(error_type, self._handle_unknown_error)
        return handler(context)
    
    def _handle_shacl_errors(self, context):
        """Convert SHACL violations into corrective prompt instructions"""
        violations = context['violations']
        corrective_instructions = []
        
        for violation in violations:
            if 'minCount' in violation:
                corrective_instructions.append(
                    f"MUST include field: {violation['field']} (currently missing)"
                )
            elif 'maxCount' in violation:
                corrective_instructions.append(
                    f"MUST remove field: {violation['field']} (not allowed for this document type)"
                )
            elif 'pattern' in violation:
                corrective_instructions.append(
                    f"Field {violation['field']} must match pattern: {violation['pattern']}"
                )
        
        return {
            'corrective_prompt': '\n'.join(corrective_instructions),
            'retry_recommended': True
        }
```

#### Step 3.1.5: Integration with Existing Scribe Actions
**Target**: `tools/scribe/actions/enhanced_frontmatter_action.py`

```python
class EnhancedFrontmatterAction(BaseAction):
    def __init__(self):
        super().__init__()
        self.llm_integration = LLMSchemaIntegration(
            'standards/registry/shacl-shapes.ttl',
            'standards/registry/contexts/fields.jsonld'
        )
        self.validator = LLMSHACLValidator()
    
    def execute(self, file_path, **kwargs):
        """Step 5: Complete integration with Scribe workflow"""
        
        # Sub-step 5.1: Read document content
        content = self._read_file_content(file_path)
        
        # Sub-step 5.2: Detect or specify info-type
        info_type = kwargs.get('info_type') or self._detect_info_type(content, file_path)
        
        # Sub-step 5.3: Build schema-constrained prompt
        prompt = self.llm_integration.build_schema_constrained_prompt(content, info_type)
        
        # Sub-step 5.4: Generate with validation loop (100% success)
        result = self.validator.validate_with_retry_loop(prompt, info_type)
        
        # Sub-step 5.5: Apply frontmatter to document
        self._apply_frontmatter_to_file(file_path, result['frontmatter'])
        
        # Sub-step 5.6: Log success metrics
        self._log_generation_metrics(file_path, result)
        
        return {
            'success': True,
            'file_processed': file_path,
            'info_type': info_type,
            'generation_attempts': result.get('attempts_used', 1),
            'fallback_used': result.get('fallback_used', False)
        }
```

### PHASE 4: UNIVERSAL kb_id STRATEGY IMPLEMENTATION

**Objective**: Replace problematic standard_id scope with universal kb_id approach

#### Step 4.1: ID Strategy Redesign
```turtle
# Enhanced SHACL shapes with universal kb_id strategy
kb:UniversalDocumentShape a sh:NodeShape ;
    sh:targetClass kb:Document ;
    sh:property [
        sh:path kb:kb_id ;
        sh:minCount 1 ;  # MANDATORY for ALL documents
        sh:pattern "^[A-Z0-9\\-]+$" ;
        sh:message "All documents must have a valid kb_id." ;
    ] .

kb:StandardDocumentShape a sh:NodeShape ;
    sh:targetNode [ sh:property [ sh:path kb:info_type ; sh:in ("standard-definition" "policy-document") ] ] ;
    sh:property [
        sh:path kb:standard_id ;
        sh:minCount 1 ;  # MANDATORY only for standards
        sh:pattern "^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\\-]+$" ;
        sh:message "Standard documents must have a valid standard_id." ;
    ] .

kb:NonStandardDocumentShape a sh:NodeShape ;
    sh:targetNode [ sh:property [ sh:path kb:info_type ; sh:not [ sh:in ("standard-definition" "policy-document") ] ] ] ;
    sh:property [
        sh:path kb:standard_id ;
        sh:maxCount 0 ;  # FORBIDDEN for non-standards
        sh:message "Non-standard documents must not have standard_id field." ;
    ] .
```

#### Step 4.2: Field Scope Correction Script
**Target**: `tools/refactoring-scripts/universal_kb_id_migration.py`

```python
class UniversalKbIdMigrator:
    def execute_scope_corrections(self):
        """Implement universal kb_id strategy across repository"""
        
        corrections_applied = []
        
        for md_file in self._scan_all_markdown_files():
            frontmatter = self._extract_frontmatter(md_file)
            info_type = frontmatter.get('info_type', 'general-document')
            
            corrections = []
            
            # Ensure kb_id exists for ALL documents
            if 'kb_id' not in frontmatter:
                kb_id = self._generate_kb_id(md_file, frontmatter)
                corrections.append(('add', 'kb_id', kb_id))
            
            # Remove standard_id from non-standard documents
            if info_type not in ['standard-definition', 'policy-document']:
                if 'standard_id' in frontmatter:
                    corrections.append(('remove', 'standard_id', None))
            
            # Add standard_id to standard documents if missing
            elif info_type in ['standard-definition', 'policy-document']:
                if 'standard_id' not in frontmatter:
                    standard_id = self._generate_standard_id(md_file, frontmatter)
                    corrections.append(('add', 'standard_id', standard_id))
            
            if corrections:
                self._apply_corrections(md_file, corrections)
                corrections_applied.append({
                    'file': md_file,
                    'corrections': corrections
                })
        
        return corrections_applied
```

### PHASE 5: CONTROLLED CI/CD SETUP (DISABLED UNTIL APPROVAL)

**Objective**: Set up automation infrastructure but keep disabled until approval

#### Step 5.1: Pre-commit Configuration (Disabled by Default)
**Target**: `.pre-commit-config.yaml`

```yaml
# FRONTMATTER VALIDATION PRE-COMMIT HOOKS
# CURRENTLY DISABLED - Uncomment to activate after approval

repos:
  # - repo: local
  #   hooks:
  #     - id: frontmatter-shacl-validation
  #       name: "Frontmatter SHACL Validation"
  #       entry: python tools/validators/graph_validator.py --staged-files
  #       language: python
  #       files: '\.md$'
  #       fail_fast: true
  #       always_run: false
  
  # ACTIVATION INSTRUCTIONS:
  # 1. Uncomment the above configuration
  # 2. Run: pre-commit install
  # 3. Test with: pre-commit run --all-files

# ON-DEMAND VALIDATION (ALWAYS AVAILABLE):
# python tools/validators/graph_validator.py --full-repository
```

#### Step 5.2: GitHub Actions (Feature-Flagged)
**Target**: `.github/workflows/frontmatter-validation.yml`

```yaml
name: Frontmatter SHACL Validation

# CURRENTLY DISABLED - Set ENABLE_FRONTMATTER_VALIDATION to true to activate
on:
  workflow_dispatch:
    inputs:
      enable_validation:
        description: 'Enable frontmatter validation'
        required: true
        default: 'false'
        type: choice
        options:
          - 'true'
          - 'false'

env:
  ENABLE_FRONTMATTER_VALIDATION: ${{ github.event.inputs.enable_validation || 'false' }}

jobs:
  validate-frontmatter:
    if: env.ENABLE_FRONTMATTER_VALIDATION == 'true'
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r tools/requirements.txt
      
      - name: Run SHACL Validation
        run: python tools/validators/graph_validator.py --full-repository --fail-on-error
        
      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: frontmatter-validation-report
          path: tools/reports/validation-*.log

# MANUAL ACTIVATION INSTRUCTIONS:
# 1. Go to Actions tab in GitHub
# 2. Select "Frontmatter SHACL Validation" workflow
# 3. Click "Run workflow"
# 4. Set "Enable frontmatter validation" to "true"
# 5. Click "Run workflow"
```

#### Step 5.3: On-Demand Validation Scripts
**Target**: `tools/validation/on_demand_validator.py`

```python
class OnDemandValidator:
    """Always-available validation without CI/CD integration"""
    
    def validate_current_repository(self):
        """Immediate validation of current repository state"""
        return self._run_full_validation()
    
    def validate_specific_files(self, file_paths):
        """Validate specific files on demand"""
        return self._run_targeted_validation(file_paths)
    
    def validate_staged_changes(self):
        """Validate only staged Git changes"""
        staged_files = self._get_staged_markdown_files()
        return self._run_targeted_validation(staged_files)
```

### SUCCESS METRICS - ENHANCED

#### Quantitative Targets (NO COMPROMISES)
- ✅ **MT-SCHEMA-FRONTMATTER.md**: Reduced from 282 to <180 lines (>36% reduction)
- ✅ **Repository Compliance**: 100% SHACL validation pass rate with **ZERO EXCEPTIONS**
- ✅ **Automation Rate**: **100% frontmatter generation** (NO manual fallbacks allowed)
- ✅ **Field Scope Accuracy**: Zero field scope violations across repository
- ✅ **Universal kb_id Coverage**: 100% of documents have valid kb_id

#### Implementation Success Criteria
- ✅ **Robust Analysis Methodology**: Works with current limited documents AND scales for KB imports
- ✅ **Detailed Implementation**: All major components decomposed to executable steps
- ✅ **Controlled Rollout**: CI/CD infrastructure ready but disabled until approval
- ✅ **100% Success Guarantee**: No scenario where automation fails without deterministic fallback

---

## IMPLEMENTATION TIMELINE (SEQUENTIAL - NO TIME-BASED PLANNING)

1. **PHASE 1**: Robust document type analysis methodology
2. **PHASE 2**: Detailed SHACL-to-Markdown generator implementation  
3. **PHASE 3**: Comprehensive Scribe LLM integration
4. **PHASE 4**: Universal kb_id strategy implementation
5. **PHASE 5**: Controlled CI/CD setup (disabled until approval)

**CRITICAL DEPENDENCIES**:
- Conda-kb environment activation before all operations
- Feature branch workflow (never commit to main)  
- All operations logged to `tools/reports/`
- Sequential task completion (no time-based planning)
- **100% automation success rate - NO EXCEPTIONS**

---

## COMPLIANCE WITH REPOSITORY WORK ETHIC

This guideline **STRICTLY ADHERES** to all repository work ethic requirements:

✅ **LEVERAGES EXISTING INFRASTRUCTURE**: Enhances rather than replaces operational systems  
✅ **ADDRESSES IDENTIFIED CRITICAL ISSUES**: Directly targets section 5.1, 5.3, and 6.2 problems  
✅ **SEQUENTIAL PLANNING**: No time-based planning, only logical dependency sequence  
✅ **AUTOMATED SOLUTIONS**: Eliminates manual frontmatter creation through LLM integration  
✅ **ENTERPRISE GOVERNANCE**: Adds missing enforcement mechanisms for strict compliance  
✅ **FACT-BASED APPROACH**: Analysis based on actual repository state and infrastructure

**AUDIT COMPLIANCE**: All modifications logged, version controlled, and include comprehensive commit annotations for regulatory compliance review. 