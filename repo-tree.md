# Repository Tree Structure

**Generated**: 2025-06-17 11:26:37  
**Script**: `tools/utilities/repo-tree/main_repo_tree.py`  
**Output**: Automated repository structure overview  

---

## Repository Structure

```
📁 master-knowledge-base
🏗️ active-project
│   🦮 project-guidelines
│   │   📄 project-reminders.md
│   │   📄 project-work-ethic-guidelines.md
│   📄 README.md
│   📄 current-state.md
│   📄 master-analysis-report-creation-guide.md
│   📄 master-roadmap-development-guide.md
│   📄 roadmap-checklist-template.md
│   📄 roadmap-progress-tracker-template.md
│   📄 roadmap-template.md
🗃️ archive ALWAYS ARCHIVE HERE
📁 change-requests
⚖️ standards
│   🔠 registry
│   │   📁 contexts
│   ⚖️ src
│   │   📄 AS-KB-DIRECTORY-STRUCTURE.md
│   │   📄 AS-MAP-STANDARDS-KB.md
│   │   📄 AS-ROOT-STANDARDS-KB.md
│   │   📄 AS-SCHEMA-CONCEPT-DEFINITION.md
│   │   📄 AS-SCHEMA-METHODOLOGY-DESCRIPTION.md
│   │   📄 AS-SCHEMA-REFERENCE.md
│   │   📄 AS-SCHEMA-RELTABLE-DEFINITION.md
│   │   📄 AS-SCHEMA-TASK.md
│   │   📄 AS-STRUCTURE-ASSET-ORGANIZATION.md
│   │   📄 AS-STRUCTURE-DOC-CHAPTER.md
│   │   📄 AS-STRUCTURE-KB-PART.md
│   │   📄 AS-STRUCTURE-KB-ROOT.md
│   │   📄 AS-STRUCTURE-MASTER-KB-INDEX.md
│   │   📄 AS-STRUCTURE-TEMPLATES-DIRECTORY.md
│   │   📄 CS-ADMONITIONS-POLICY.md
│   │   📄 CS-CONTENT-PROFILING-POLICY.md
│   │   📄 CS-LINKING-INTERNAL-POLICY.md
│   │   📄 CS-MODULARITY-TRANSCLUSION-POLICY.md
│   │   📄 CS-POLICY-ACCESSIBILITY.md
│   │   📄 CS-POLICY-DIGITAL-ABSTRACTION.md
│   │   📄 CS-POLICY-KB-IDENTIFICATION.md
│   │   📄 CS-POLICY-KB-PART-CONTENT.md
│   │   📄 CS-POLICY-LAYERED-INFORMATION.md
│   │   📄 CS-POLICY-PART-OVERVIEW.md
│   │   📄 CS-POLICY-SCOPE-EXCLUSION.md
│   │   📄 CS-POLICY-SCOPE-INCLUSION.md
│   │   📄 CS-POLICY-TONE-LANGUAGE.md
│   │   📄 CS-TOC-POLICY.md
│   │   📄 GM-CONVENTIONS-NAMING.md
│   │   📄 GM-GLOSSARY-STANDARDS-TERMS.md
│   │   📄 GM-GUIDE-KB-USAGE.md
│   │   📄 GM-MANDATE-KB-USAGE-GUIDE.md
│   │   📄 GM-MANDATE-STANDARDS-GLOSSARY.md
│   │   📄 GM-REGISTRY-GOVERNANCE.md
│   │   📄 MT-KEYREF-MANAGEMENT.md
│   │   📄 MT-REGISTRY-TAG-GLOSSARY.md
│   │   📄 MT-SCHEMA-FRONTMATTER.md
│   │   📄 MT-STRATEGY-PRIMARY-TOPIC-KEYWORD.md
│   │   📄 MT-TAGGING-STRATEGY-POLICY.md
│   │   📄 MT-TAGS-IMPLEMENTATION.md
│   │   📄 OM-AUTOMATION-LLM-IO-SCHEMAS.md
│   │   📄 OM-AUTOMATION-LLM-PROMPT-LIBRARY.md
│   │   📄 OM-OVERVIEW-PUBLISHING-PIPELINE.md
│   │   📄 OM-POLICY-STANDARDS-DEPRECATION.md
│   │   📄 OM-POLICY-STANDARDS-GOVERNANCE.md
│   │   📄 OM-PROCESS-SST-UPDATE.md
│   │   📄 OM-VERSIONING-CHANGELOGS.md
│   │   📄 QM-VALIDATION-METADATA.md
│   │   📄 SF-ACCESSIBILITY-IMAGE-ALT-TEXT.md
│   │   📄 SF-CALLOUTS-SYNTAX.md
│   │   📄 SF-CONDITIONAL-SYNTAX-ATTRIBUTES.md
│   │   📄 SF-FORMATTING-CITATIONS.md
│   │   📄 SF-FORMATTING-FILE-HYGIENE.md
│   │   📄 SF-FORMATTING-MARKDOWN-GENERAL.md
│   │   📄 SF-LINKS-INTERNAL-SYNTAX.md
│   │   📄 SF-SYNTAX-BLOCKQUOTES.md
│   │   📄 SF-SYNTAX-CODE.md
│   │   📄 SF-SYNTAX-COMMENT-TODO.md
│   │   📄 SF-SYNTAX-DEFINITION-LISTS.md
│   │   📄 SF-SYNTAX-DIAGRAMS-MERMAID.md
│   │   📄 SF-SYNTAX-EMPHASIS.md
│   │   📄 SF-SYNTAX-ESCAPING-CHARACTERS.md
│   │   📄 SF-SYNTAX-FOOTNOTES.md
│   │   📄 SF-SYNTAX-HEADINGS.md
│   │   📄 SF-SYNTAX-IMAGES.md
│   │   📄 SF-SYNTAX-KEYREF.md
│   │   📄 SF-SYNTAX-LINKS-GENERAL.md
│   │   📄 SF-SYNTAX-LISTS.md
│   │   📄 SF-SYNTAX-MATH-EQUATIONS.md
│   │   📄 SF-SYNTAX-TABLES.md
│   │   📄 SF-SYNTAX-YAML-FRONTMATTER.md
│   │   📄 SF-TOC-SYNTAX.md
│   │   📄 SF-TRANSCLUSION-SYNTAX.md
│   │   📄 UA-KEYDEFS-GLOBAL.md
│   │   📄 UA-SCHEMA-LLM-IO.md
│   🧬 templates
│   │   📄 UA-TPL-CANONICAL-FRONTMATTER.md
│   │   📄 UA-TPL-CHANGELOG-DOCUMENT.md
│   📄 README.md
│   📄 changelog.md
🧪 test-environment ALWAYS SETUP AND EXECUTE TESTS HERE (INCLUDING THEIR OUTPUT; DIFFERENT FROM TOOLS!)
│   💾 backup
│   │   📄 no-frontmatter.md
│   │   📄 sample1.md
│   │   📄 sample2.md
│   📁 scribe-tests
│   │   📄 manual_test_security_manager.py
│   │   📄 simulated_24h_soak_test.py
│   │   📄 simulated_soak_test.py
│   │   📄 soak_test.py
│   │   📄 test_atomic_write.py
│   │   📄 test_circuit_breaker_enhancement.py
│   │   📄 test_end_to_end_traceability.py
│   │   📄 test_event_id_traceability.py
│   │   📄 test_exit_conditions_1_1.py
│   │   📄 test_full_pipeline.py
│   │   📄 test_health_endpoint.py
│   │   📄 test_integration.py
│   │   📄 test_phase4_verification.py
│   │   📄 test_quarantine_logic.py
│   │   📄 test_queue_backpressure.py
│   │   📄 test_security_manager.py
│   │   📄 test_simple_traceability.py
│   │   📄 test_step_1_2_exit_conditions.py
│   │   📄 test_step_2_1_exit_conditions.py
│   │   📄 test_watcher.py
│   │   📄 test_worker.py
│   │   📄 verify_step_1_2.py
│   📁 test-documents
│   │   📄 CamelCaseFile.md
│   │   📄 comprehensive-test.md
│   │   📄 file-with-links.md
│   │   📄 frontmatter-field-violations.md
│   │   📄 locked-test.md
│   │   📄 simple-test.md
│   │   📄 test-uppercase.md
│   │   📄 uppercase-extension-test.md
│   📁 tool-tests-consolidated-20250607-0942
│   │   📁 indexer-tests
│   │   │   📄 test_generate_index.py
│   │   📁 linter-tests
│   │       📄 test_kb_linter.py
│   📁 validator-tests
│   │   📁 test-data
│   │       📄 conforming-shacl-doc.md
│   │       📄 violating-shacl-doc.md
│   📄 README.md
│   📄 naming-enforcer-test-files.md
│   📄 run_all_tests.py
│   📄 safety-test-suite.py
│   📄 test-results-20250607-091041.json
│   📄 test-summary-20250607-091041.md
│   📄 test-todos.json
🔧 tools
│   📁 file-format-utils
│   │   📄 add_readme_frontmatter.py
│   │   📄 crlf_to_lf_converter.py
│   📁 frontmatter-management
│   │   📄 date_time_manager.py
│   │   📄 frontmatter_organizer.py
│   🔧 indexer
│   │   📄 OM-SPEC-STANDARDS-INDEX-JSONLD.md
│   │   📄 generate_index.py
│   │   📄 standards_index.schema.json
│   🔧 linter
│   │   📄 kb_linter.py
│   📁 naming-enforcer
│   │   📄 .namingignore
│   │   📄 .naminginclude
│   │   📄 generate_naming_configs.py
│   │   📄 naming_enforcer.py
│   │   📄 naming_exceptions.json
│   │   📄 protected-names.json
│   │   📄 recover_backup.py
│   🔧 refactoring-scripts
│   │   📄 refactor_criticality_field.py
│   │   📄 refactor_ids_filenames.py
│   │   📄 refactor_tag_casing.py
│   📁 scribe
│   │   📁 actions
│   │   │   📄 __init__.py
│   │   │   📄 base.py
│   │   │   📄 base_action.py
│   │   │   📄 graph_validation_action.py
│   │   │   📄 naming_enforcement_action.py
│   │   │   📄 reconciliation_action.py
│   │   │   📄 run_command_action.py
│   │   │   📄 view_generation_action.py
│   │   📁 config
│   │   │   📄 config.json
│   │   │   📄 config.schema.json
│   │   │   📄 sst-update-workflow.json
│   │   📁 core
│   │   │   📄 __init__.py
│   │   │   📄 action_dispatcher.py
│   │   │   📄 atomic_write.py
│   │   │   📄 circuit_breaker.py
│   │   │   📄 config_manager.py
│   │   │   📄 health_server.py
│   │   │   📄 logging_config.py
│   │   │   📄 plugin_loader.py
│   │   │   📄 rule_processor.py
│   │   │   📄 security_manager.py
│   │   📄 README.md
│   │   📄 __init__.py
│   │   📄 engine.py
│   │   📄 pyproject.toml
│   │   📄 requirements.txt
│   │   📄 watcher.py
│   │   📄 worker.py
│   🔧 utilities
│   │   📁 repo-tree
│   │   │   📄 .subtreeignore
│   │   │   📄 .treeaddtext
│   │   │   📄 .treeicon
│   │   │   📄 .treeignore
│   │   │   📄 main_repo_tree.py
│   │   📄 README-repo-tree.md
│   │   📄 todo_tracker.py
│   🔧 validators
│   │   📄 graph_validator.py
│   │   📄 validate_registry.py
│   📄 README.md
│   📄 archive-logger.ps1
│   📄 changelog.md
│   📄 view_generator.py
📄 .cursorignore
📄 .cursorrules
📄 AS-INDEX-KB-MASTER.md
📄 README.md
📄 comprehensive-standards-analysis-remaining-tasks-20250616-2101.md
📄 frontmatter-analysis.md
📄 frontmatter-enhancements.md
📄 repo-tree.md
📄 repo_tree.py
📄 ultimate-frontmatter-enhancement-guideline-20250617-0312.md
```

---

## Legend

- ⚖️ **Source Content Directory**
- ⛔ **Node.js Dependencies Directory**
- ❌ **INCORRECT LOCATION (ARCHIVE CONTENT AND DELETE THIS FOLDER)**
- 🏗️ **Active Project Management**
- 💡 **Sample Content**
- 💾 **Backup Storage Directory**
- 📁 **Standard Directory**
- 📄 **File**
- 📊 **Generated Reports Directory**
- 📚 **Documentation**
- 🔠 **Data Registry Directory**
- 🔧 **Code Refactoring**
- 🗂️ **Temporary Files Directory**
- 🗃️ **Archive Storage**
- 🦮 **Project Guidelines Documentation**
- 🧪 **Testing Environment**
- 🧬 **Template Files Directory**

---

## Configuration Files

- **`.treeignore`**: Folders to completely exclude from tree
- **`.subtreeignore`**: Folders to show but not expand contents  
- **`.treeaddtext`**: Annotations for specific folders/files
- **`.treeicon`**: Icons and legend descriptions (format: `path|icon|description`)

**Configuration Location**: `tools/utilities/repo-tree/`
