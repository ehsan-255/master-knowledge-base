## PROPOSAL o3

1. Field Inventory & Source-Map  
 a. Run a scripted scan of every `.md` file’s YAML front-matter → collect all keys, sample values, file paths → write `tools/reports/frontmatter-field-inventory-<timestamp>.csv`.  
 b. Tag each key with earliest authoritative standard (if any).

2. Vocabulary & Context Definition  
 a. For each key, decide URI: reuse Dublin Core/SKOS/FOAF where possible; otherwise define `kb:` namespace entry.  
 b. Update `standards/registry/contexts/fields.jsonld` (and `base.jsonld` if needed).  
 c. Version the context with SemVer (`v1.0.0` → `v1.1.0`, etc.).

3. Design SHACL Profile-Based Universal Schema  
 a. Identify canonical `info-type` values (e.g., `standard-definition`, `guide`, `meeting-notes`, `scratch`).  
 b. In `standards/registry/shacl-shapes.ttl`, create one `shacl:NodeShape` per info-type.  
 c. Within each shape, declare:  
  • mandatory keys (`shacl:minCount 1`)  
  • optional keys (`shacl:minCount 0`)  
  • forbidden keys (`shacl:maxCount 0`)  
  • regex/datatype constraints (`shacl:pattern`, `shacl:datatype`)  
 d. Add meta‐shape enforcing that *every* document carries minimal universal keys (`title`, `info-type`, `kb-id`, `date-modified`, etc.).

4. Front-Matter → RDF Conversion & Validation Engine  
 a. Create `tools/validators/frontmatter_validator.py` that:  
  5. parses YAML front-matter (PyYAML),  
  6. expands via the JSON-LD context into an RDF graph (rdflib),  
  7. validates against `shacl-shapes.ttl` (pyshacl),  
  8. emits pass/fail plus detailed violations to `tools/reports/validation-<timestamp>.log` (machine-readable + human summary).  
 b. Support `--dry-run`, `--subset <glob>`, and `--fix-simple` flags.

9. Front-Matter Generator CLI  
 a. Add `tools/frontmatter-management/generate_frontmatter.py`: given `--info-type` (and optional interactive prompts/LLM later), output a compliant YAML header using the appropriate SHACL shape.  
 b. Integrate with document skeleton scripts so new files start valid.

10. Bulk Migration Automation  
 a. Write `tools/migration/migrate_frontmatter.py` that iterates over the repo, calls the validator, auto-fills missing mandatory keys with sensible placeholders, records actions, and writes a patch set.  
 b. Always run `--dry-run` first; store diff summary in `tools/reports/`.  
 c. After manual review, run live mode to commit changes.

11. Continuous Integration & Pre-Commit Enforcement  
 a. Add a pre-commit hook (`.pre-commit-config.yaml`) that invokes `frontmatter_validator.py --subset staged`.  
 b. Create a GitHub Action workflow executing full validation on every PR; block merge on errors; upload log artifact to workflow run.

12. Refactor Human-Readable Schema Doc  
 a. Generate concise `MT-SCHEMA-FRONTMATTER.md` directly from SHACL shapes via a script (`tools/build/generate_schema_md.py`) → guarantees ≤ 180 lines; place long examples in `examples/`.  
 b. Add “DO NOT EDIT – generated” notice.

13. Standards for Enforcement, Exceptions, and Tooling  
 a. Author new standard `OM-COMPLIANCE-FRONTMATTER-ENFORCEMENT.md` defining mandatory use, penalties for non-compliance, and exception request workflow.  
 b. Create `OM-AUTOMATED-VALIDATION.md` mandating CI/pre-commit checks and referencing the validator.  
 c. Update existing standards to replace “SHOULD” with “MUST” where front-matter is concerned.

14. Documentation & Developer Enablement  
 a. Update repo `README.md` and developer guides to include quick-start commands: generator, validator, migration script.  
 b. Publish a cheat-sheet table mapping keys → purpose → URI.  
 c. Conduct spot-check walkthroughs; store findings in `tools/reports/frontmatter-spotcheck-<timestamp>.md`.

15. Feedback & Iteration Loop  
 a. After first full-repo validation passes, schedule monthly validator runs via CI to detect drift.  
 b. Maintain changelog in `standards/registry/contexts/fields.jsonld` and `shacl-shapes.ttl`, using SemVer tags.  
 c. When breaking changes occur, provide migration scripts + bump major version.

COMPLETION CRITERIA  
• 100 % of Markdown files pass SHACL validation in CI.  
• `MT-SCHEMA-FRONTMATTER.md` auto-generated and ≤ 180 lines.  
• Pre-commit and GitHub Action block invalid front-matter.  
• All keys mapped in JSON-LD context with resolvable URIs.  
• New enforcement standard merged into main branch.

---

## PROPOSAL SONNET 4

### ENHANCED ARCHITECTURE COMBINING BEST OF BOTH + EXISTING SYSTEMS

**Foundation Principle**: Leverage existing SHACL/JSON-LD infrastructure while preserving sophisticated conditional logic from legacy YAML system.

**Key Innovations Beyond Both Reports:**

1. **Legacy Wisdom Preservation**: Extract conditional validation rules from archived `mt-schema-frontmatter.yaml`
2. **Complete Profile System**: Comprehensive SHACL shapes for each `info-type` with conditional logic
3. **Automated Documentation**: Generate `MT-SCHEMA-FRONTMATTER.md` from SHACL shapes (282→100 lines)
4. **LLM Integration Architecture**: Schema-driven frontmatter generation for automation
5. **Bulk Migration System**: Automated legacy document migration with zero exceptions

---

## ULTIMATE STEP-BY-STEP IMPLEMENTATION GUIDELINE

### PHASE 1: FOUNDATION CONSOLIDATION (Days 1-3)

#### Step 1.1: Archive Legacy Conditional Logic Analysis
```bash
# Extract conditional rules from legacy YAML system
python tools/extract_legacy_conditional_rules.py \
  archive/migration-backup-20250607-133124/master-knowledge-base/standards/registry/mt-schema-frontmatter.yaml \
  > tools/reports/legacy-conditional-rules-analysis.md
```

#### Step 1.2: Enhance SHACL Shapes with Complete Conditional Logic
**Target**: `standards/registry/shacl-shapes.ttl`

```turtle
# Enhanced SHACL shapes with info-type profiles
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix kb: <https://knowledge-base.local/vocab#> .

# Complete profile for standard-definition documents
kb:StandardDefinitionProfile a sh:NodeShape ;
    sh:targetNode [ sh:property [ sh:path kb:info_type ; sh:hasValue "standard-definition" ] ] ;
    sh:property [
        sh:path kb:standard_id ; sh:minCount 1 ;
        sh:pattern "^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\\-]+$" ;
    ] ;
    sh:property [
        sh:path kb:primary_domain ; sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path kb:sub_domain ; sh:minCount 1 ;
    ] .

# Profile for meeting-notes documents  
kb:MeetingNotesProfile a sh:NodeShape ;
    sh:targetNode [ sh:property [ sh:path kb:info_type ; sh:hasValue "meeting-notes" ] ] ;
    sh:property [
        sh:path kb:standard_id ; sh:maxCount 0 ;  # Explicitly disallowed
    ] .
```

#### Step 1.3: Complete JSON-LD Context Enhancement
**Target**: `standards/registry/contexts/fields.jsonld`

```json
{
  "@context": {
    "kb": "https://knowledge-base.local/vocab#",
    "dct": "http://purl.org/dc/terms/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    
    "title": { "@id": "dct:title", "@type": "xsd:string" },
    "standard_id": { "@id": "kb:standard_id", "@type": "xsd:string" },
    "info_type": { "@id": "kb:info_type", "@type": "xsd:string" },
    "date_created": { "@id": "dct:created", "@type": "xsd:dateTime" },
    "date_modified": { "@id": "dct:modified", "@type": "xsd:dateTime" }
  }
}
```

### PHASE 2: AUTOMATED DOCUMENTATION SYSTEM (Days 4-5)

#### Step 2.1: Create SHACL-to-Markdown Generator
**Target**: `tools/generate_schema_docs_from_shacl.py`

```python
# Auto-generate MT-SCHEMA-FRONTMATTER.md from SHACL shapes
def generate_frontmatter_schema_doc(shacl_file, output_file):
    """Generate human-readable schema from SHACL shapes"""
    profiles = parse_shacl_profiles(shacl_file)
    
    markdown_content = []
    for profile_name, rules in profiles.items():
        markdown_content.append(f"## {profile_name} Profile")
        for field, constraints in rules.items():
            mandatory = "Mandatory" if constraints.get('minCount', 0) > 0 else "Optional"
            markdown_content.append(f"### `{field}` - {mandatory}")
    
    write_markdown(output_file, markdown_content)
```

#### Step 2.2: Integrate with Existing Build Process
```bash
# Add to existing workflow
python tools/generate_schema_docs_from_shacl.py \
  standards/registry/shacl-shapes.ttl \
  standards/src/MT-SCHEMA-FRONTMATTER.md
```

### PHASE 3: LLM INTEGRATION ARCHITECTURE (Days 6-8)

#### Step 3.1: Schema-Driven Frontmatter Generator
**Target**: `tools/frontmatter-management/llm_frontmatter_generator.py`

```python
class LLMFrontmatterGenerator:
    def __init__(self, shacl_file, jsonld_context):
        self.profiles = parse_shacl_profiles(shacl_file)
        self.context = load_jsonld_context(jsonld_context)
    
    def generate_frontmatter(self, document_content, info_type):
        """Generate frontmatter using LLM with schema constraints"""
        profile_rules = self.profiles.get(f"{info_type}Profile", {})
        
        # Create LLM prompt with schema constraints
        prompt = self.build_constrained_prompt(document_content, profile_rules)
        frontmatter = llm_client.generate(prompt)
        
        # Validate against SHACL before returning
        if self.validate_shacl(frontmatter, info_type):
            return frontmatter
        else:
            return self.regenerate_with_corrections(frontmatter, info_type)
```

#### Step 3.2: Integration with Scribe Workflow
**Target**: `tools/scribe/actions/generate_frontmatter.py`

```python
from tools.frontmatter_management.llm_frontmatter_generator import LLMFrontmatterGenerator

class GenerateFrontmatterAction(BaseAction):
    def execute(self, file_path):
        content = read_file(file_path)
        info_type = self.detect_info_type(content)
        
        generator = LLMFrontmatterGenerator(
            "standards/registry/shacl-shapes.ttl",
            "standards/registry/contexts/fields.jsonld"
        )
        
        frontmatter = generator.generate_frontmatter(content, info_type)
        self.prepend_frontmatter(file_path, frontmatter)
```

### PHASE 4: VALIDATION INTEGRATION (Days 9-10)

#### Step 4.1: Enhance Existing Linter with SHACL Validation
**Target**: `tools/linter/kb_linter.py`

```python
from pyshacl import validate

class EnhancedKBLinter:
    def validate_frontmatter_shacl(self, frontmatter_dict, file_path):
        """Validate frontmatter against SHACL shapes"""
        # Convert YAML frontmatter to RDF using JSON-LD context
        rdf_graph = self.yaml_to_rdf(frontmatter_dict)
        
        # Validate against SHACL shapes
        conforms, results_graph, results_text = validate(
            rdf_graph, 
            shacl_graph="standards/registry/shacl-shapes.ttl"
        )
        
        if not conforms:
            self.report_shacl_violations(file_path, results_text)
        
        return conforms
```

#### Step 4.2: Pre-commit Hook Integration
**Target**: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: local
    hooks:
      - id: frontmatter-shacl-validation
        name: Frontmatter SHACL Validation
        entry: python tools/linter/kb_linter.py --shacl-validation
        language: python
        files: '\.md$'
        fail_fast: true
```

### PHASE 5: BULK LEGACY MIGRATION (Days 11-14)

#### Step 5.1: Legacy Document Analysis and Migration Planning
```bash
# Analyze all documents requiring frontmatter migration
python tools/analyze_legacy_documents.py \
  --scan-repository \
  --output tools/reports/legacy-migration-plan.md
```

#### Step 5.2: Automated Bulk Migration
**Target**: `tools/bulk_frontmatter_migration.py`

```python
class BulkFrontmatterMigrator:
    def migrate_repository(self, dry_run=True):
        """Migrate all legacy documents with zero exceptions"""
        documents = self.scan_all_markdown_files()
        
        for doc_path in documents:
            if not self.has_valid_frontmatter(doc_path):
                content = read_file(doc_path)
                info_type = self.classify_document(content, doc_path)
                
                frontmatter = self.generator.generate_frontmatter(content, info_type)
                
                if dry_run:
                    self.log_proposed_changes(doc_path, frontmatter)
                else:
                    self.apply_frontmatter(doc_path, frontmatter)
                    self.validate_result(doc_path)
```

#### Step 5.3: Zero Exceptions Enforcement
```bash
# Execute bulk migration with comprehensive validation
python tools/bulk_frontmatter_migration.py --execute --validate-all --zero-exceptions

# Verify 100% compliance
python tools/linter/kb_linter.py --full-repository-scan --shacl-validation --fail-on-any-violation
```

### PHASE 6: MONITORING & REFINEMENT (Days 15+)

#### Step 6.1: Automated Quality Monitoring
```bash
# Weekly automated compliance reporting
python tools/generate_frontmatter_compliance_report.py \
  --output tools/reports/weekly-frontmatter-compliance-$(date +%Y%m%d).md
```

#### Step 6.2: Continuous Schema Evolution
```python
# Version-controlled schema updates
class SchemaEvolutionManager:
    def propose_schema_change(self, change_request):
        """Handle schema changes with backward compatibility"""
        # Validate against existing documents
        # Generate migration scripts if needed
        # Update SHACL shapes and JSON-LD context atomically
```

---

## SUCCESS METRICS & VALIDATION

### Quantitative Targets
- **Verbosity Reduction**: MT-SCHEMA-FRONTMATTER.md from 282 to ~100 lines (65% reduction)
- **Validation Coverage**: 100% repository compliance with zero exceptions
- **Automation Rate**: 95%+ frontmatter generation through LLM automation
- **Profile Completeness**: 100% of info-types have dedicated SHACL profiles

### Qualitative Targets  
- **Single Source of Truth**: SHACL shapes as authoritative schema definition
- **Semantic Integration**: Full RDF/OWL compatibility through JSON-LD contexts
- **Developer Experience**: Automated frontmatter generation eliminates manual work
- **Enterprise Compliance**: Mandatory validation enforces strict standards

---

## IMPLEMENTATION TIMELINE

**Total Duration**: 15 days sequential implementation
- **Phase 1-2**: Infrastructure consolidation and automation (5 days)
- **Phase 3-4**: LLM integration and validation (5 days)  
- **Phase 5**: Bulk migration with zero exceptions (4 days)
- **Phase 6**: Ongoing monitoring and refinement (1 day setup)

**Critical Dependencies**: 
1. Conda-kb environment activation
2. Feature branch workflow (never commit to main)
3. `tools/reports/` logging for all operations
4. Sequential task completion (no time-based planning)

This ultimate solution delivers on all user requirements while leveraging the sophisticated infrastructure already in place, making it both technically superior and practically achievable.

---

## PROPOSAL GEMINI

### **Ultimate Step-by-Step Implementation Guideline**

This plan outlines a sequential, five-phase process to design, implement, and enforce a new, unified frontmatter architecture. This initiative directly addresses critical issues outlined in `comprehensive-standards-analysis-remaining-tasks-20250616-2101.md`, specifically sections on "Frontmatter Field Scope Errors" (5.1), "Missing Automated Validation Requirements" (6.2), and "KB-ID Field Ambiguity" (5.3).

---

### **Phase 1: Architectural Definition & Design (The Blueprint)**

*   **Goal:** To create the authoritative, machine-readable definition of the new frontmatter standard.

**Step 1.1: Formalize Document "Profiles"**
-   **Action:** Define a definitive, controlled vocabulary for the `info-type` field.
-   **Details:** Analyze the repository to identify all distinct document categories (e.g., `standard-definition`, `policy`, `guide`, `technical-report`, `meeting-notes`, `general-document`). Each `info-type` will correspond to a validation "profile".
-   **Deliverable:** An updated `standards/registry/controlled-vocabularies/info-types.yaml` (or equivalent) file.

**Step 1.2: Design the Master JSON-LD Context**
-   **Action:** Create the master context file that maps human-friendly frontmatter keys to formal RDF/OWL URIs.
-   **Details:**
    -   Use standard vocabularies (e.g., `dct:` for Dublin Core, `skos:` for tags) where possible to maximize interoperability.
    -   Define a custom `kb:` namespace for repository-specific fields (e.g., `kb:standard_id`, `kb:lifecycle_gatekeeper`).
    -   Specify data types for fields (e.g., `"date-modified": { "@id": "dct:modified", "@type": "xsd:dateTime" }`).
-   **Deliverable:** A finalized `standards/registry/contexts/master.jsonld` file.

**Step 1.3: Author the Authoritative SHACL Schema**
-   **Action:** Build the `shacl-shapes.ttl` file that defines all validation rules.
-   **Details:**
    -   Create a `shacl:NodeShape` for each "profile" defined in Step 1.1 (e.g., `kb:StandardShape`, `kb:GuideShape`).
    -   For each shape, define `shacl:property` constraints for every relevant field, specifying:
        -   Cardinality (`shacl:minCount`, `shacl:maxCount`) to enforce mandatory/optional rules per profile.
        -   Data types (`shacl:datatype`).
        -   Value constraints (e.g., regex `shacl:pattern`, controlled vocabulary `shacl:in`).
-   **Deliverable:** A complete `standards/registry/shacl-shapes.ttl` file that serves as the single source of truth for all frontmatter rules.

**Step 1.4: Formally Deprecate the Legacy Schema Document**
-   **Action:** Update the `MT-SCHEMA-FRONTMATTER.md` standard to mark it as deprecated.
-   **Details:** Add a deprecation notice at the top of the file, explaining that it is being replaced by the new SHACL-based validation system and the forthcoming auto-generated documentation.
-   **Deliverable:** An updated `standards/src/MT-SCHEMA-FRONTMATTER.md` with a clear deprecation warning.

---

### **Phase 2: Core Toolchain Development (The Automation Engine)**

*   **Goal:** To build the automated tools required to generate, validate, and document the new frontmatter standard.

**Step 2.1: Develop the Universal Frontmatter Validator (`frontmatter_validator.py`)**
-   **Action:** Create a new Python script responsible for all frontmatter validation.
-   **Logic:**
    1.  Input: A Markdown file path.
    2.  Extract the YAML frontmatter.
    3.  Load the `master.jsonld` context.
    4.  Use a library (e.g., `pyld`) to convert the frontmatter into an in-memory RDF graph (JSON-LD expansion).
    5.  Load the `shacl-shapes.ttl` schema.
    6.  Use a library (e.g., `pyshacl`) to validate the generated graph against the SHACL shapes. The script must select the correct shape based on the document's `info-type`.
    7.  Output: A clear pass/fail result with detailed error messages if validation fails.
-   **Deliverable:** A robust, well-tested script in `tools/validators/frontmatter_validator.py`.

**Step 2.2: Develop the Frontmatter Generation & Update Tool (`scribe-fm-manager`)**
-   **Action:** Create a CLI tool to assist authors and automate frontmatter creation/updates.
-   **Features:**
    -   `scribe-fm-manager new --info-type <profile>`: Generates a valid, minimal frontmatter block for a new document of a specific type.
    -   `scribe-fm-manager update <file>`: Inspects an existing file's frontmatter, identifies missing mandatory fields for its profile, and interactively (or automatically) adds them.
-   **Deliverable:** A new tool integrated into the Scribe automation engine or as a standalone script in `tools/frontmatter-management/`.

**Step 2.3: Develop the Schema-to-Markdown Documentation Generator**
-   **Action:** Create a script that reads the `shacl-shapes.ttl` file and generates human-readable documentation.
-   **Logic:**
    1.  Parse the SHACL file to extract all Shapes and Property definitions.
    2.  For each profile (Shape), generate a Markdown section detailing its required and optional fields, their data types, and constraints.
    3.  This replaces the manual effort of maintaining `MT-SCHEMA-FRONTMATTER.md`.
-   **Deliverable:** A script in `tools/builder/generate_schema_docs.py` that outputs a new `UA-SCHEMA-FRONTMATTER.md`.

---

### **Phase 3: Integration, Enforcement & Documentation (The Rollout)**

*   **Goal:** To embed the new standard and its toolchain into the repository's daily workflow.

**Step 3.1: Integrate Validator into the CI/CD Pipeline & Pre-Commit Hooks**
-   **Action:** Make validation an unavoidable step in the contribution process.
-   **Details:**
    -   Configure the repository's pre-commit hook framework to run `python tools/validators/frontmatter_validator.py` on all staged `.md` files.
    -   Add a validation step to the main CI/CD pipeline (e.g., GitHub Actions) that performs the same check, failing the build if any document has invalid frontmatter.
-   **Deliverable:** Updated configuration files for pre-commit hooks and CI/CD workflows.

**Step 3.2: Generate and Commit the New Authoritative Documentation**
-   **Action:** Run the documentation generator from Step 2.3 to create the official, human-readable schema.
-   **Details:** Execute `python tools/builder/generate_schema_docs.py` and commit the resulting `standards/src/UA-SCHEMA-FRONTMATTER.md`. This becomes the new "source of truth" for human authors.
-   **Deliverable:** The initial version of the auto-generated `UA-SCHEMA-FRONTMATTER.md`.

**Step 3.3: Update Repository Guidelines**
-   **Action:** Update all relevant project guidelines and standards to refer to the new system.
-   **Details:** Search for and update any documents that mention frontmatter, pointing them to the new `UA-SCHEMA-FRONTMATTER.md` document and the `scribe-fm-manager` tool. This includes `project-work-ethic-guidelines.md` and other onboarding materials.
-   **Deliverable:** A set of commits updating all relevant documentation.

---

### **Phase 4: Full-Scale Legacy Migration (The "Zero-Exception" Mandate)**

*   **Goal:** To update every single existing Markdown document in the repository to conform to the new frontmatter standard.

**Step 4.1: Develop the Bulk Migration Script (`migrate_frontmatter.py`)**
-   **Action:** Create a powerful, idempotent script to perform the migration.
-   **Logic:**
    1.  Recursively scan the entire repository for `.md` files.
    2.  For each file, read its existing frontmatter.
    3.  **Intelligently Map Old to New:** Attempt to map existing fields to the new schema. Infer the `info-type` based on file location or existing metadata where possible; default to `general-document` if unsure.
    4.  **Add Missing Fields:** Add all new mandatory fields for the determined profile, populating them with sensible defaults (e.g., `[AUTO_GENERATED_KB_ID]`, `[MISSING_PRIMARY_TOPIC]`).
    5.  **Overwrite the File:** Write the new, conformant frontmatter back to the file.
-   **Deliverable:** A script in `tools/refactoring-scripts/migrate_frontmatter.py`.

**Step 4.2: Perform and Meticulously Verify Dry-Run**
-   **Action:** Run the migration script in a `--dry-run` mode that logs proposed changes without writing them.
-   **Details:**
    -   The script will generate a comprehensive report (`tools/reports/frontmatter-migration-dry-run-YYYYMMDD-HHMM.log`) detailing every file it would change and the exact diff.
    -   Manually review a significant sample (at least 20%) of the proposed changes across different document types to ensure correctness.
-   **Deliverable:** A clean dry-run report with verification sign-off.

**Step 4.3: Execute Full Migration**
-   **Action:** Run the migration script in live mode.
-   **Details:** Execute the script from Step 4.1. This will be a large, repository-wide change committed in a single, well-documented operation.
-   **Deliverable:** A single commit containing all frontmatter changes across the repository.

**Step 4.4: Final Verification**
-   **Action:** Run the universal validator (Step 2.1) across the entire repository one last time.
-   **Details:** The validator must pass with zero errors.
-   **Deliverable:** A final validation report (`tools/reports/post-migration-validation-YYYYMMDD-HHMM.log`) confirming 100% compliance.

---

### **Phase 5: Governance & Continuous Improvement (The Living Standard)**

*   **Goal:** To establish a formal process for managing and evolving the frontmatter standard over time.

**Step 5.1: Establish a Schema Change Management Process**
-   **Action:** Document the formal procedure for proposing, reviewing, and implementing changes to the frontmatter schema.
-   **Details:** This process will be defined in a new standard (`OM-POLICY-SCHEMA-GOVERNANCE.md`). It will require that all changes are made directly to the `shacl-shapes.ttl` and `master.jsonld` files, followed by re-running the documentation generator. No manual edits to the documentation will be permitted.
-   **Deliverable:** A new governance standard document.

**Step 5.2: Update Onboarding and Training Materials**
-   **Action:** Ensure all developer and author documentation reflects the new, automated, and strictly-enforced frontmatter system.
-   **Details:** This includes updating READMEs, wikis, and any guides related to content creation.
-   **Deliverable:** Updated training and onboarding documents.