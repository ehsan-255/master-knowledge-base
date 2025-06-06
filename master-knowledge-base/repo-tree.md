# Repository Tree Structure

**Generated**: 2025-06-06 16:10:31  
**Script**: `master-knowledge-base/tools/utilities/repo-tree/main_repo_tree.py`  
**Output**: Automated repository structure overview  

---

## Repository Structure

```
📁 master-knowledge-base
✅ archive ALWAYS ARCHIVE HERE
📋 standards
│   📊 registry
│   │   📄 audience_types.yaml
│   │   📄 criticality_levels.txt
│   │   📄 criticality_levels.yaml
│   │   📄 domain_codes.yaml
│   │   📄 field_order.yaml
│   │   📄 frontmatter_fields.yaml
│   │   📄 info_types.txt
│   │   📄 lifecycle_gatekeepers.txt
│   │   📄 lifecycle_gatekeepers.yaml
│   │   📄 maturity_levels.yaml
│   │   📄 MT-REGISTRY-TAG-GLOSSARY.md
│   │   📄 mt-schema-frontmatter.yaml
│   │   📄 registry_schema.yaml
│   │   📄 subdomain_registry.yaml
│   │   📄 tag_categories.txt
│   📝 src
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
│   │   📄 CS-POLICY-DOC-CHAPTER-CONTENT.md
│   │   📄 CS-POLICY-KB-IDENTIFICATION.md
│   │   📄 CS-POLICY-KB-PART-CONTENT.md
│   │   📄 CS-POLICY-KB-ROOT.md
│   │   📄 CS-POLICY-LAYERED-INFORMATION.md
│   │   📄 CS-POLICY-PART-OVERVIEW.md
│   │   📄 CS-POLICY-SCOPE-EXCLUSION.md
│   │   📄 CS-POLICY-SCOPE-INCLUSION.md
│   │   📄 CS-POLICY-TONE-LANGUAGE.md
│   │   📄 CS-TOC-POLICY.md
│   │   📄 GM-CONVENTIONS-NAMING.md
│   │   📄 GM-GLOSSARY-STANDARDS-TERMS.md
│   │   📄 GM-GUIDE-KB-USAGE.md
│   │   📄 GM-GUIDE-STANDARDS-BY-TASK.md
│   │   📄 GM-MANDATE-KB-USAGE-GUIDE.md
│   │   📄 GM-MANDATE-STANDARDS-GLOSSARY.md
│   │   📄 GM-REGISTRY-GOVERNANCE.md
│   │   📄 MT-KEYREF-MANAGEMENT.md
│   │   📄 MT-SCHEMA-FRONTMATTER.md
│   │   📄 MT-STRATEGY-PRIMARY-TOPIC-KEYWORD.md
│   │   📄 MT-TAGGING-STRATEGY-POLICY.md
│   │   📄 MT-TAGS-IMPLEMENTATION.md
│   │   📄 OM-AUTOMATION-LLM-IO-SCHEMAS.md
│   │   📄 OM-AUTOMATION-LLM-PROMPT-LIBRARY.md
│   │   📄 OM-OVERVIEW-PUBLISHING-PIPELINE.md
│   │   📄 OM-POLICY-STANDARDS-DEPRECATION.md
│   │   📄 OM-POLICY-STANDARDS-GOVERNANCE.md
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
│   📄 templates
│   │   📄 UA-TPL-CANONICAL-FRONTMATTER.md
│   │   📄 UA-TPL-CHANGELOG-DOCUMENT.md
│   📄 changelog.md
🔧 tools
│   📁 file-format-utils
│   │   📄 add_readme_frontmatter.py
│   │   📄 crlf_to_lf_converter.py
│   📁 frontmatter-management
│   │   📄 date_time_manager.py
│   │   📄 frontmatter_organizer.py
│   │   📄 generate_frontmatter_registry.py
│   │   📄 generate_schema_docs.py
│   📇 indexer
│   │   ❌ tests NEVER TEST HERE (content must be moved to test-environment folder and this folder must be deleted)
│   │   │   📄 test_generate_index.py
│   │   📄 generate_index.py
│   │   📄 OM-SPEC-STANDARDS-INDEX-JSONLD.md
│   │   📄 standards_index.schema.json
│   🔍 linter
│   │   ❌ tests NEVER TEST HERE (content must be moved to test-environment folder and this folder must be deleted)
│   │   │   📄 test_kb_linter.py
│   │   📄 kb_linter.py
│   📁 naming-enforcer
│   │   📄 .namingignore
│   │   📄 .naminginclude
│   │   📄 generate_naming_configs.py
│   │   📄 naming_enforcer.py
│   │   📄 naming_exceptions.json
│   │   📄 protected-names.json
│   │   📄 recover_backup.py
│   🔄 refactoring-scripts
│   │   📄 refactor_criticality_field.py
│   │   📄 refactor_ids_filenames.py
│   │   📄 refactor_tag_casing.py
│   📋 reports
│   │   📁 backups
│   │   │   📁 fix_violations_20250604_090824
│   │   │   │   📄 AUTOMATIC_FILES.md
│   │   │   │   📄 backup-manifest.json
│   │   │   │   📄 debug_pattern_extraction.py
│   │   │   │   📄 dry_run_preview_20250604_082128_operations.json
│   │   │   │   📄 dry_run_preview_20250604_082149_operations.json
│   │   │   │   📄 dry_run_preview_20250604_083922_operations.json
│   │   │   │   📄 dry_run_preview_20250604_085009_operations.json
│   │   │   │   📄 dry_run_results.txt
│   │   │   │   📄 EXCLUDE_FUNCTIONALITY.md
│   │   │   │   📄 full_repo_scan.txt
│   │   │   │   📄 IMPLEMENTATION_SUMMARY.md
│   │   │   │   📄 INCLUDE_FUNCTIONALITY.md
│   │   │   │   📄 registry-schema.yaml
│   │   │   📁 fix_violations_20250604_092653
│   │   │       📄 backup-manifest.json
│   │   │       📄 current-state.mD
│   │   📄 auto-generation-completion-report-2025-06-05.md
│   │   📄 collection_fixes_implemented_2025-06-04.md
│   │   📄 collection_linter_issue_analysis_2025-06-04.md
│   │   📄 criticality_fix_summary_2025-06-04.md
│   │   📄 exact_linter_errors_2025-06-04-09-57.md
│   │   📄 frontmatter-registry-summary-2025-06-04-20-39-16.md
│   │   📄 frontmatter-registry-summary-2025-06-04-20-39-19.md
│   │   📄 frontmatter-registry-summary-2025-06-04-22-46-12.md
│   │   📄 frontmatter-registry-summary-2025-06-05-02-10-51.md
│   │   📄 frontmatter-registry-summary-2025-06-05-02-10-57.md
│   │   📄 frontmatter-registry-summary-2025-06-05-02-11-08.md
│   │   📄 frontmatter-registry-summary-2025-06-05-02-14-53.md
│   │   📄 frontmatter-registry-summary-2025-06-05-02-33-47.md
│   │   📄 frontmatter-registry-summary-2025-06-05-02-33-52.md
│   │   📄 frontmatter-registry-summary-2025-06-05-02-53-53.md
│   │   📄 frontmatter-registry-summary-2025-06-05-02-55-02.md
│   │   📄 GM-CONVENTIONS-NAMING_preview.md
│   │   📄 legend-configuration-guide-20250606-1516.md
│   │   📄 linter_report.md
│   │   📄 linter_report_criticality_fixed.md
│   │   📄 linter_report_fixed.md
│   │   📄 linter_results_after_fixes.txt
│   │   📄 linter_results_corrected_path.txt
│   │   📄 linter_results_final.txt
│   │   📄 linter_results_final_complete.txt
│   │   📄 linter_results_post_live_run.txt
│   │   📄 linter_results_ultimate_final.txt
│   │   📄 linter_test_auto_generated_files.txt
│   │   📄 MT-SCHEMA-FRONTMATTER_preview.md
│   │   📄 preview-criticality_levels.txt
│   │   📄 preview-field_order.yaml
│   │   📄 preview-frontmatter_fields.yaml
│   │   📄 preview-info_types.txt
│   │   📄 preview-lifecycle_gatekeepers.txt
│   │   📄 preview-tag_categories.txt
│   │   📄 repository-tree-final-cleanup-20250606-1441.md
│   │   📄 repository-tree-generator-configuration-upgrade-20250606-1411.md
│   │   📄 repository-tree-generator-implementation-20250606-1333.md
│   │   📄 roadmap-template-compliance-update-20250606-1301.md
│   │   📄 schema_docs_generation_report_20250604_224621.md
│   │   📄 schema_docs_generation_report_20250604_225007.md
│   │   📄 schema_docs_generation_report_20250605_021500.md
│   │   📄 schema_docs_generation_report_20250605_023537.md
│   🔧 utilities
│   │   📁 repo-tree
│   │   │   📄 .subtreeignore
│   │   │   📄 .treeaddtext
│   │   │   📄 .treeicon
│   │   │   📄 .treeignore
│   │   │   📄 main_repo_tree.py
│   │   📄 README-repository-tree-generator.md
│   │   📄 todo_tracker.py
│   ✅ validators
│   │   📄 validate_registry.py
│   📄 changelog.md
│   📄 README.md
📄 AS-INDEX-KB-MASTER.md
📄 repo-tree.md
```

---

## Legend

- ⛔ **Node.js Dependencies Directory**
- ✅ **Validation Tools Directory**
- ❌ **Test Files (Restricted)**
- 🎯 **Active Project Management**
- 🏗️ **Build System Directory**
- 💡 **Sample Content Directory**
- 💾 **Backup Storage Directory**
- 📁 **Standard Directory**
- 📄 **Template Files Directory**
- 📇 **Content Indexing Directory**
- 📊 **Data Registry Directory**
- 📋 **Project Guidelines Documentation**
- 📚 **Documentation Directory**
- 📝 **Source Content Directory**
- 🔄 **Code Refactoring Directory**
- 🔍 **Code Linting Directory**
- 🔧 **Utility Tools Directory**
- 🗂️ **Temporary Files Directory**

---

## Configuration Files

- **`.treeignore`**: Folders to completely exclude from tree
- **`.subtreeignore`**: Folders to show but not expand contents  
- **`.treeaddtext`**: Annotations for specific folders/files
- **`.treeicon`**: Icons and legend descriptions (format: `path|icon|description`)

**Configuration Location**: `master-knowledge-base/tools/utilities/repo-tree/`
