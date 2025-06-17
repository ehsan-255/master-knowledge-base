#!/usr/bin/env python3
"""
Auto-Generation Workflow Integration

Implementation of Phase 2: Step 2.1.4 - Auto-Generation Workflow Integration
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module provides complete workflow for auto-generating MT-SCHEMA-FRONTMATTER.md
with validation, backup, and comprehensive change reporting.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
import hashlib

# Import the Phase 2 components we've built
from shacl_parser import SHACLParser
from profile_categorizer import ProfileCategorizer
from markdown_template_generator import MarkdownTemplateGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentationValidator:
    """Validator for generated documentation quality and consistency."""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def validate_generated_docs(self, documentation: str) -> Dict[str, Any]:
        """Validate generated documentation against quality criteria."""
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'quality_metrics': {},
            'compliance_checks': {}
        }
        
        # Check basic structure
        structure_check = self._validate_document_structure(documentation)
        validation_result['compliance_checks']['structure'] = structure_check
        
        # Check content quality
        quality_check = self._validate_content_quality(documentation)
        validation_result['quality_metrics'] = quality_check
        
        # Check for required sections
        sections_check = self._validate_required_sections(documentation)
        validation_result['compliance_checks']['required_sections'] = sections_check
        
        # Check for auto-generation markers
        auto_gen_check = self._validate_auto_generation_markers(documentation)
        validation_result['compliance_checks']['auto_generation'] = auto_gen_check
        
        # Aggregate validation status
        if not structure_check['valid'] or not sections_check['valid'] or not auto_gen_check['valid']:
            validation_result['is_valid'] = False
        
        # Collect warnings and errors
        for check_name, check_result in validation_result['compliance_checks'].items():
            if check_result.get('warnings'):
                validation_result['warnings'].extend(check_result['warnings'])
            if check_result.get('errors'):
                validation_result['errors'].extend(check_result['errors'])
        
        self.logger.info(f"Documentation validation complete. Valid: {validation_result['is_valid']}")
        if validation_result['warnings']:
            self.logger.warning(f"Validation warnings: {len(validation_result['warnings'])}")
        if validation_result['errors']:
            self.logger.error(f"Validation errors: {len(validation_result['errors'])}")
        
        return validation_result
    
    def _validate_document_structure(self, documentation: str) -> Dict[str, Any]:
        """Validate basic document structure."""
        lines = documentation.split('\n')
        
        result = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'structure_metrics': {}
        }
        
        # Check frontmatter
        if not documentation.startswith('---'):
            result['errors'].append("Document must start with YAML frontmatter")
            result['valid'] = False
        
        # Check for main title
        has_main_title = any(line.startswith('# ') for line in lines)
        if not has_main_title:
            result['errors'].append("Document must have a main title (# heading)")
            result['valid'] = False
        
        # Count heading levels
        heading_counts = {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0}
        for line in lines:
            if line.startswith('# '):
                heading_counts['h1'] += 1
            elif line.startswith('## '):
                heading_counts['h2'] += 1
            elif line.startswith('### '):
                heading_counts['h3'] += 1
            elif line.startswith('#### '):
                heading_counts['h4'] += 1
        
        result['structure_metrics'] = {
            'total_lines': len(lines),
            'heading_distribution': heading_counts,
            'has_tables': '|' in documentation,
            'has_code_blocks': '`' in documentation
        }
        
        # Validate heading hierarchy
        if heading_counts['h1'] != 1:
            result['warnings'].append(f"Expected exactly 1 H1 heading, found {heading_counts['h1']}")
        
        if heading_counts['h2'] == 0:
            result['warnings'].append("No H2 headings found - document may lack structure")
        
        return result
    
    def _validate_content_quality(self, documentation: str) -> Dict[str, Any]:
        """Validate content quality metrics."""
        words = documentation.split()
        lines = documentation.split('\n')
        
        quality_metrics = {
            'word_count': len(words),
            'line_count': len(lines),
            'avg_words_per_line': len(words) / max(len(lines), 1),
            'empty_line_ratio': sum(1 for line in lines if line.strip() == '') / len(lines),
            'has_sufficient_content': len(words) > 100,
            'content_density': 'high' if len(words) / len(lines) > 5 else 'medium' if len(words) / len(lines) > 2 else 'low'
        }
        
        return quality_metrics
    
    def _validate_required_sections(self, documentation: str) -> Dict[str, Any]:
        """Validate presence of required sections."""
        required_sections = [
            'Auto-Generation Notice',
            'Field Reference',
            # Add more required sections as needed
        ]
        
        result = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'missing_sections': [],
            'found_sections': []
        }
        
        for section in required_sections:
            if section in documentation:
                result['found_sections'].append(section)
            else:
                result['missing_sections'].append(section)
                result['warnings'].append(f"Missing required section: {section}")
        
        return result
    
    def _validate_auto_generation_markers(self, documentation: str) -> Dict[str, Any]:
        """Validate auto-generation markers are present."""
        result = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check for auto-generated marker in frontmatter
        if 'auto-generated: true' not in documentation:
            result['errors'].append("Missing 'auto-generated: true' marker in frontmatter")
            result['valid'] = False
        
        # Check for generation timestamp
        if 'Generated:' not in documentation:
            result['warnings'].append("Missing generation timestamp")
        
        # Check for warning about manual editing
        if 'Do not edit this file manually' not in documentation:
            result['warnings'].append("Missing manual editing warning")
        
        return result


class AutoDocumentationWorkflow:
    """
    Complete Auto-Documentation Workflow for SHACL-to-Markdown generation.
    
    Provides end-to-end workflow for generating MT-SCHEMA-FRONTMATTER.md from 
    SHACL shapes with validation, backup, and change reporting.
    """
    
    def __init__(self, shacl_file_path: str = 'standards/registry/shacl-shapes.ttl',
                 target_file_path: str = 'standards/src/MT-SCHEMA-FRONTMATTER.md'):
        self.shacl_file_path = Path(shacl_file_path)
        self.target_file_path = Path(target_file_path)
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        
        # Initialize logger
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Initialize components
        self.validator = DocumentationValidator()
    
    def execute_full_generation_cycle(self) -> Dict[str, Any]:
        """
        Complete workflow for auto-generating MT-SCHEMA-FRONTMATTER.md.
        
        Returns comprehensive results including success status, file paths,
        validation results, and change reports.
        """
        self.logger.info("Starting full auto-documentation generation cycle")
        
        try:
            # Step 1: Parse current SHACL shapes
            self.logger.info("Step 1: Parsing SHACL shapes...")
            parser = SHACLParser(str(self.shacl_file_path))
            rule_matrix = parser.extract_validation_rules()
            
            if not rule_matrix:
                return self._create_failure_result("No SHACL rules found to process")
            
            # Step 2: Categorize profiles
            self.logger.info("Step 2: Categorizing profiles...")
            categorizer = ProfileCategorizer()
            profile_hierarchy = categorizer.categorize_profiles(rule_matrix)
            
            # Step 3: Generate markdown documentation
            self.logger.info("Step 3: Generating markdown documentation...")
            generator = MarkdownTemplateGenerator(profile_hierarchy)
            documentation = generator.generate_concise_documentation(target_line_limit=180)
            
            # Step 4: Validate against existing documentation
            self.logger.info("Step 4: Validating generated documentation...")
            validation_result = self.validator.validate_generated_docs(documentation)
            
            if not validation_result['is_valid']:
                self.logger.error("Generated documentation failed validation")
                return self._create_failure_result("Documentation validation failed", {
                    'validation_result': validation_result,
                    'generated_content': documentation
                })
            
            # Step 5: Create backup of existing documentation
            self.logger.info("Step 5: Creating backup of existing documentation...")
            backup_path = self._backup_existing_documentation()
            
            # Step 6: Write generated documentation
            self.logger.info("Step 6: Writing generated documentation...")
            self._write_generated_documentation(documentation)
            
            # Step 7: Generate change report
            self.logger.info("Step 7: Generating change report...")
            change_report = self._generate_change_report(validation_result, backup_path)
            
            # Step 8: Generate generation metadata
            generation_stats = generator.get_generation_stats(documentation)
            
            success_result = {
                'success': True,
                'timestamp': self.timestamp,
                'documentation_path': str(self.target_file_path),
                'backup_path': str(backup_path) if backup_path else None,
                'line_count': generator._count_lines(documentation),
                'validation_result': validation_result,
                'change_report': change_report,
                'generation_stats': generation_stats,
                'source_analysis': {
                    'shacl_shapes_found': len(rule_matrix),
                    'profile_categories': len(profile_hierarchy.get('document_type_profiles', {})),
                    'total_constraints': sum(
                        data.get('complexity_metrics', {}).get('total_constraints', 0)
                        for data in profile_hierarchy.get('document_type_profiles', {}).values()
                    )
                }
            }
            
            self.logger.info("Auto-documentation generation completed successfully")
            return success_result
            
        except Exception as e:
            self.logger.error(f"Auto-documentation generation failed: {e}")
            return self._create_failure_result(f"Generation failed: {e}")
    
    def _backup_existing_documentation(self) -> Optional[Path]:
        """Create backup of existing documentation file."""
        if not self.target_file_path.exists():
            self.logger.info("No existing documentation file to backup")
            return None
        
        backup_dir = Path("tools/reports/documentation-backups")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        backup_filename = f"MT-SCHEMA-FRONTMATTER-backup-{self.timestamp}.md"
        backup_path = backup_dir / backup_filename
        
        try:
            shutil.copy2(self.target_file_path, backup_path)
            self.logger.info(f"Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return None
    
    def _write_generated_documentation(self, documentation: str):
        """Write generated documentation to target file."""
        try:
            # Ensure target directory exists
            self.target_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write documentation
            with open(self.target_file_path, 'w', encoding='utf-8') as f:
                f.write(documentation)
            
            self.logger.info(f"Documentation written to: {self.target_file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to write documentation: {e}")
            raise
    
    def _generate_change_report(self, validation_result: Dict[str, Any], 
                               backup_path: Optional[Path]) -> Dict[str, Any]:
        """Generate comprehensive change report."""
        change_report = {
            'generation_timestamp': self.timestamp,
            'changes_detected': False,
            'content_comparison': {},
            'validation_summary': {
                'is_valid': validation_result['is_valid'],
                'warning_count': len(validation_result['warnings']),
                'error_count': len(validation_result['errors'])
            },
            'file_operations': {
                'backup_created': backup_path is not None,
                'backup_path': str(backup_path) if backup_path else None,
                'target_file_updated': True
            }
        }
        
        # Compare with backup if available
        if backup_path and backup_path.exists():
            try:
                # Read backup content
                with open(backup_path, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                
                # Read new content
                with open(self.target_file_path, 'r', encoding='utf-8') as f:
                    new_content = f.read()
                
                # Compare content
                content_comparison = self._compare_documentation_content(backup_content, new_content)
                change_report['content_comparison'] = content_comparison
                change_report['changes_detected'] = content_comparison['has_changes']
                
            except Exception as e:
                self.logger.warning(f"Failed to compare content: {e}")
                change_report['content_comparison'] = {'error': str(e)}
        
        # Save change report
        self._save_change_report(change_report)
        
        return change_report
    
    def _compare_documentation_content(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """Compare old and new documentation content."""
        comparison = {
            'has_changes': old_content != new_content,
            'content_hash_old': hashlib.md5(old_content.encode()).hexdigest(),
            'content_hash_new': hashlib.md5(new_content.encode()).hexdigest(),
            'size_change': len(new_content) - len(old_content),
            'line_count_change': len(new_content.split('\n')) - len(old_content.split('\n')),
            'structural_changes': {}
        }
        
        if comparison['has_changes']:
            # Analyze structural changes
            old_lines = old_content.split('\n')
            new_lines = new_content.split('\n')
            
            # Count headings
            old_headings = [line for line in old_lines if line.startswith('#')]
            new_headings = [line for line in new_lines if line.startswith('#')]
            
            comparison['structural_changes'] = {
                'heading_count_change': len(new_headings) - len(old_headings),
                'headings_added': [h for h in new_headings if h not in old_headings],
                'headings_removed': [h for h in old_headings if h not in new_headings]
            }
        
        return comparison
    
    def _save_change_report(self, change_report: Dict[str, Any]):
        """Save change report to file."""
        reports_dir = Path("tools/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_filename = f"auto-doc-change-report-{self.timestamp}.json"
        report_path = reports_dir / report_filename
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(change_report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Change report saved: {report_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save change report: {e}")
    
    def _create_failure_result(self, error_message: str, additional_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Create standardized failure result."""
        result = {
            'success': False,
            'timestamp': self.timestamp,
            'error': error_message,
            'documentation_path': str(self.target_file_path),
            'line_count': 0
        }
        
        if additional_data:
            result.update(additional_data)
        
        return result
    
    def dry_run(self) -> Dict[str, Any]:
        """Execute a dry run without writing files."""
        self.logger.info("Starting dry run of auto-documentation generation")
        
        try:
            # Parse SHACL shapes
            parser = SHACLParser(str(self.shacl_file_path))
            rule_matrix = parser.extract_validation_rules()
            
            # Categorize profiles
            categorizer = ProfileCategorizer()
            profile_hierarchy = categorizer.categorize_profiles(rule_matrix)
            
            # Generate documentation
            generator = MarkdownTemplateGenerator(profile_hierarchy)
            documentation = generator.generate_concise_documentation(target_line_limit=180)
            
            # Validate
            validation_result = self.validator.validate_generated_docs(documentation)
            
            # Get stats
            generation_stats = generator.get_generation_stats(documentation)
            
            dry_run_result = {
                'success': True,
                'dry_run': True,
                'timestamp': self.timestamp,
                'would_write_to': str(self.target_file_path),
                'line_count': generator._count_lines(documentation),
                'validation_result': validation_result,
                'generation_stats': generation_stats,
                'preview': documentation[:500] + "..." if len(documentation) > 500 else documentation
            }
            
            self.logger.info("Dry run completed successfully")
            return dry_run_result
            
        except Exception as e:
            self.logger.error(f"Dry run failed: {e}")
            return self._create_failure_result(f"Dry run failed: {e}")
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status and component health."""
        status = {
            'workflow_ready': True,
            'components_status': {},
            'file_status': {},
            'last_generation': None
        }
        
        # Check SHACL file
        status['file_status']['shacl_shapes'] = {
            'exists': self.shacl_file_path.exists(),
            'path': str(self.shacl_file_path),
            'size': self.shacl_file_path.stat().st_size if self.shacl_file_path.exists() else 0
        }
        
        # Check target directory
        status['file_status']['target_directory'] = {
            'exists': self.target_file_path.parent.exists(),
            'path': str(self.target_file_path.parent),
            'writable': True  # Assume writable for now
        }
        
        # Check existing target file
        status['file_status']['target_file'] = {
            'exists': self.target_file_path.exists(),
            'path': str(self.target_file_path),
            'size': self.target_file_path.stat().st_size if self.target_file_path.exists() else 0,
            'last_modified': self.target_file_path.stat().st_mtime if self.target_file_path.exists() else None
        }
        
        # Test component initialization
        try:
            parser = SHACLParser(str(self.shacl_file_path))
            status['components_status']['shacl_parser'] = {'ready': True}
        except Exception as e:
            status['components_status']['shacl_parser'] = {'ready': False, 'error': str(e)}
            status['workflow_ready'] = False
        
        try:
            categorizer = ProfileCategorizer()
            status['components_status']['profile_categorizer'] = {'ready': True}
        except Exception as e:
            status['components_status']['profile_categorizer'] = {'ready': False, 'error': str(e)}
            status['workflow_ready'] = False
        
        return status


if __name__ == "__main__":
    # Example usage for testing
    workflow = AutoDocumentationWorkflow()
    
    # Check workflow status
    status = workflow.get_workflow_status()
    print(f"Workflow Status: {status}")
    
    # Execute dry run
    dry_run_result = workflow.dry_run()
    print(f"Dry Run Result: {dry_run_result['success']}")
    
    # Execute full generation if dry run successful
    if dry_run_result['success']:
        result = workflow.execute_full_generation_cycle()
        print(f"Full Generation Result: {result['success']}")
        if result['success']:
            print(f"Documentation updated: {result['documentation_path']}")
            print(f"Line count: {result['line_count']}")
    else:
        print("Dry run failed, skipping full generation")