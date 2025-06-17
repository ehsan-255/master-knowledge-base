#!/usr/bin/env python3
"""
Universal kb_id Strategy Implementation

Implementation of Phase 4: Universal kb_id Strategy Implementation
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module implements the universal kb_id strategy replacing problematic 
standard_id scope issues with a comprehensive identification system.
"""

import os
import re
import yaml
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalKbIdMigrator:
    """
    Universal kb_id Strategy Migrator.
    
    Implements comprehensive kb_id strategy to replace problematic standard_id 
    scope issues while maintaining proper field constraints per document type.
    """
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Document type configurations
        self.document_type_configs = self._initialize_document_type_configs()
        
        # ID generation patterns
        self.id_patterns = self._initialize_id_patterns()
        
        # Migration statistics
        self.migration_stats = {
            'files_processed': 0,
            'corrections_applied': 0,
            'kb_ids_generated': 0,
            'standard_ids_removed': 0,
            'standard_ids_added': 0,
            'errors_encountered': []
        }
    
    def execute_scope_corrections(self, dry_run: bool = True) -> Dict[str, Any]:
        """
        Implement universal kb_id strategy across repository.
        
        Args:
            dry_run: If True, only analyze changes without applying them
            
        Returns:
            Migration results with detailed change report
        """
        self.logger.info(f"Starting universal kb_id migration (dry_run={dry_run})")
        
        corrections_applied = []
        
        # Scan all markdown files in the repository
        markdown_files = list(self.repo_path.rglob("*.md"))
        self.logger.info(f"Found {len(markdown_files)} markdown files to process")
        
        for md_file in markdown_files:
            try:
                file_corrections = self._process_single_file(md_file, dry_run)
                if file_corrections:
                    # Add file path to each correction for reporting
                    for correction in file_corrections:
                        correction['file_path'] = str(md_file)
                    corrections_applied.extend(file_corrections)
                    
            except Exception as e:
                error_msg = f"Error processing {md_file}: {e}"
                self.logger.error(error_msg)
                self.migration_stats['errors_encountered'].append(error_msg)
        
        # Generate comprehensive report
        migration_report = self._generate_migration_report(corrections_applied, dry_run)
        
        return migration_report
    
    def _process_single_file(self, md_file: Path, dry_run: bool) -> List[Dict[str, Any]]:
        """Process a single markdown file for kb_id corrections."""
        self.migration_stats['files_processed'] += 1
        
        try:
            # Read file content
            content = md_file.read_text(encoding='utf-8')
            
            # Extract frontmatter
            frontmatter = self._extract_frontmatter(content)
            if not frontmatter:
                return []  # No frontmatter to process
            
            # Determine document type
            info_type = frontmatter.get('info-type', self._infer_info_type(content, md_file))
            
            # Calculate required corrections
            corrections = self._calculate_required_corrections(frontmatter, info_type, md_file)
            
            # Apply corrections if not dry run
            if corrections and not dry_run:
                self._apply_corrections(md_file, corrections)
            
            return corrections
            
        except Exception as e:
            self.logger.warning(f"Could not process {md_file}: {e}")
            return []
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract YAML frontmatter from document content."""
        try:
            if content.startswith('---\n'):
                end_marker = content.find('\n---\n', 4)
                if end_marker != -1:
                    frontmatter_yaml = content[4:end_marker]
                    return yaml.safe_load(frontmatter_yaml)
            return None
        except Exception as e:
            self.logger.warning(f"Could not parse frontmatter: {e}")
            return None
    
    def _infer_info_type(self, content: str, file_path: Path) -> str:
        """Infer info-type from content and file path."""
        content_lower = content.lower()
        path_str = str(file_path).lower()
        
        # Path-based inference
        if '/standards/' in path_str and any(word in content_lower for word in ['standard', 'compliance']):
            return 'standard-definition'
        elif 'policy' in path_str or 'policy' in content_lower:
            return 'policy-document'
        elif '/reports/' in path_str or 'report' in content_lower:
            return 'technical-report'
        elif 'meeting' in content_lower or 'attendees' in content_lower:
            return 'meeting-notes'
        else:
            return 'general-document'
    
    def _calculate_required_corrections(self, frontmatter: Dict[str, Any], 
                                      info_type: str, file_path: Path) -> List[Dict[str, Any]]:
        """Calculate what corrections are needed for this document."""
        corrections = []
        
        # Get configuration for this document type
        config = self.document_type_configs.get(info_type, self.document_type_configs['general-document'])
        
        # 1. Ensure kb_id exists for ALL documents (universal requirement)
        if 'kb-id' not in frontmatter:
            kb_id = self._generate_kb_id(file_path, frontmatter, info_type)
            corrections.append({
                'type': 'add_field',
                'field': 'kb-id',
                'value': kb_id,
                'reason': 'Universal kb-id requirement for all documents'
            })
            self.migration_stats['kb_ids_generated'] += 1
        
        # 2. Remove standard_id from non-standard documents
        if info_type in config['forbidden_standard_id']:
            if 'standard_id' in frontmatter:
                corrections.append({
                    'type': 'remove_field',
                    'field': 'standard_id',
                    'old_value': frontmatter['standard_id'],
                    'reason': f'{info_type} documents must not have standard_id field'
                })
                self.migration_stats['standard_ids_removed'] += 1
        
        # 3. Add standard_id to standard documents if missing
        elif info_type in config['requires_standard_id']:
            if 'standard_id' not in frontmatter:
                standard_id = self._generate_standard_id(file_path, frontmatter, info_type)
                corrections.append({
                    'type': 'add_field',
                    'field': 'standard_id',
                    'value': standard_id,
                    'reason': f'{info_type} documents require standard_id field'
                })
                self.migration_stats['standard_ids_added'] += 1
        
        # 4. Update info-type if missing or incorrect
        if frontmatter.get('info-type') != info_type:
            corrections.append({
                'type': 'update_field',
                'field': 'info-type',
                'old_value': frontmatter.get('info-type'),
                'new_value': info_type,
                'reason': f'Correct info-type classification based on content analysis'
            })
        
        # 5. Add missing mandatory fields
        for mandatory_field in config['mandatory_fields']:
            if mandatory_field not in frontmatter:
                default_value = self._generate_default_value(mandatory_field, info_type, file_path)
                corrections.append({
                    'type': 'add_field',
                    'field': mandatory_field,
                    'value': default_value,
                    'reason': f'Mandatory field for {info_type} documents'
                })
        
        # 6. Validate existing standard_id pattern if present
        if 'standard_id' in frontmatter and info_type in config['requires_standard_id']:
            if not self._validate_standard_id_pattern(frontmatter['standard_id']):
                new_standard_id = self._generate_standard_id(file_path, frontmatter, info_type)
                corrections.append({
                    'type': 'update_field',
                    'field': 'standard_id',
                    'old_value': frontmatter['standard_id'],
                    'new_value': new_standard_id,
                    'reason': 'Invalid standard_id pattern, regenerating with correct format'
                })
        
        return corrections
    
    def _generate_kb_id(self, file_path: Path, frontmatter: Dict[str, Any], info_type: str) -> str:
        """Generate universal kb_id for any document type."""
        # Use consistent format: PREFIX-TYPE-IDENTIFIER-TIMESTAMP
        
        # Generate prefix based on document type
        type_prefixes = {
            'general-document': 'DOC',
            'standard-definition': 'STD',
            'policy-document': 'POL',
            'technical-report': 'RPT',
            'meeting-notes': 'MTG'
        }
        
        prefix = type_prefixes.get(info_type, 'DOC')
        
        # Generate identifier from file name or title
        identifier = self._generate_identifier_from_content(file_path, frontmatter)
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        
        # Combine into final kb_id
        kb_id = f"{prefix}-{identifier}-{timestamp}"
        
        return kb_id
    
    def _generate_standard_id(self, file_path: Path, frontmatter: Dict[str, Any], info_type: str) -> str:
        """Generate standard_id for standard/policy documents."""
        # Format: XX-CATEGORY-IDENTIFIER
        
        # Type prefix
        type_prefix = 'ST' if info_type == 'standard-definition' else 'PL'
        
        # Category based on file path or content
        category = self._determine_standard_category(file_path, frontmatter)
        
        # Generate identifier
        identifier = self._generate_identifier_from_content(file_path, frontmatter)
        
        # Combine into standard_id
        standard_id = f"{type_prefix}-{category}-{identifier}"
        
        return standard_id
    
    def _generate_identifier_from_content(self, file_path: Path, frontmatter: Dict[str, Any]) -> str:
        """Generate identifier from file name or title."""
        # Try to use title first
        title = frontmatter.get('title', '')
        if title:
            # Convert title to identifier
            identifier = re.sub(r'[^A-Za-z0-9\-]', '', title.replace(' ', '-')).upper()
            if len(identifier) > 20:
                identifier = identifier[:20]
            if identifier:
                return identifier
        
        # Fallback to file name
        file_name = file_path.stem.upper().replace(' ', '-').replace('_', '-')
        identifier = re.sub(r'[^A-Za-z0-9\-]', '', file_name)
        
        if len(identifier) > 20:
            identifier = identifier[:20]
        
        return identifier if identifier else 'AUTO'
    
    def _determine_standard_category(self, file_path: Path, frontmatter: Dict[str, Any]) -> str:
        """Determine category for standard_id generation."""
        path_str = str(file_path).lower()
        
        # Category mapping based on common patterns
        if 'security' in path_str:
            return 'SEC'
        elif 'compliance' in path_str:
            return 'COMP'
        elif 'policy' in path_str:
            return 'POLICY'
        elif 'process' in path_str:
            return 'PROC'
        elif 'data' in path_str:
            return 'DATA'
        else:
            return 'GEN'  # General category
    
    def _generate_default_value(self, field: str, info_type: str, file_path: Path) -> Any:
        """Generate default value for a mandatory field."""
        defaults = {
            'title': file_path.stem.replace('_', ' ').replace('-', ' ').title(),
            'version': '1.0.0',
            'date-created': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'date-modified': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'criticality': 'P2-Standard',
            'lifecycle_gatekeeper': 'Technical-Review',
            'tags': [info_type.replace('-', '_')],
            'scope_application': 'repository'
        }
        
        return defaults.get(field, f'auto-generated-{field}')
    
    def _validate_standard_id_pattern(self, standard_id: str) -> bool:
        """Validate standard_id follows correct pattern."""
        pattern = r'^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$'
        return bool(re.match(pattern, standard_id))
    
    def _apply_corrections(self, file_path: Path, corrections: List[Dict[str, Any]]):
        """Apply corrections to a file."""
        try:
            # Read current content
            content = file_path.read_text(encoding='utf-8')
            
            # Extract frontmatter
            frontmatter = self._extract_frontmatter(content)
            if not frontmatter:
                frontmatter = {}
            
            # Apply each correction
            for correction in corrections:
                if correction['type'] == 'add_field':
                    frontmatter[correction['field']] = correction['value']
                elif correction['type'] == 'remove_field':
                    frontmatter.pop(correction['field'], None)
                elif correction['type'] == 'update_field':
                    frontmatter[correction['field']] = correction['new_value']
            
            # Reconstruct content with updated frontmatter
            updated_content = self._reconstruct_content_with_frontmatter(content, frontmatter)
            
            # Write back to file
            file_path.write_text(updated_content, encoding='utf-8')
            
            self.migration_stats['corrections_applied'] += len(corrections)
            self.logger.info(f"Applied {len(corrections)} corrections to {file_path}")
            
        except Exception as e:
            error_msg = f"Failed to apply corrections to {file_path}: {e}"
            self.logger.error(error_msg)
            self.migration_stats['errors_encountered'].append(error_msg)
    
    def _reconstruct_content_with_frontmatter(self, original_content: str, 
                                            frontmatter: Dict[str, Any]) -> str:
        """Reconstruct content with updated frontmatter."""
        # Generate YAML for frontmatter
        frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        
        # Remove existing frontmatter from content
        if original_content.startswith('---\n'):
            end_marker = original_content.find('\n---\n', 4)
            if end_marker != -1:
                body_content = original_content[end_marker + 5:]
            else:
                body_content = original_content
        else:
            body_content = original_content
        
        # Reconstruct with new frontmatter
        new_content = f"---\n{frontmatter_yaml}---\n\n{body_content.lstrip()}"
        
        return new_content
    
    def _generate_migration_report(self, corrections_applied: List[Dict[str, Any]], 
                                 dry_run: bool) -> Dict[str, Any]:
        """Generate comprehensive migration report."""
        report = {
            'migration_summary': {
                'dry_run': dry_run,
                'timestamp': datetime.now().isoformat(),
                'total_files_processed': self.migration_stats['files_processed'],
                'total_corrections_needed': len(corrections_applied),
                'corrections_applied': self.migration_stats['corrections_applied'],
                'success_rate': (
                    (self.migration_stats['corrections_applied'] / len(corrections_applied) * 100)
                    if corrections_applied else 100
                )
            },
            'field_statistics': {
                'kb_ids_generated': self.migration_stats['kb_ids_generated'],
                'standard_ids_added': self.migration_stats['standard_ids_added'],
                'standard_ids_removed': self.migration_stats['standard_ids_removed']
            },
            'corrections_by_type': self._group_corrections_by_type(corrections_applied),
            'corrections_by_file': self._group_corrections_by_file(corrections_applied),
            'errors_encountered': self.migration_stats['errors_encountered'],
            'validation_status': 'READY_FOR_EXECUTION' if dry_run else 'EXECUTED'
        }
        
        return report
    
    def _group_corrections_by_type(self, corrections: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group corrections by type for statistics."""
        type_counts = {}
        for correction in corrections:
            correction_type = correction.get('type', 'unknown')
            type_counts[correction_type] = type_counts.get(correction_type, 0) + 1
        return type_counts
    
    def _group_corrections_by_file(self, corrections: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group corrections by file for detailed reporting."""
        file_corrections = {}
        for correction in corrections:
            file_path = correction.get('file_path', 'unknown')
            if file_path not in file_corrections:
                file_corrections[file_path] = []
            file_corrections[file_path].append(correction)
        return file_corrections
    
    def _initialize_document_type_configs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize document type configurations."""
        return {
            'general-document': {
                'mandatory_fields': ['title', 'info-type', 'kb-id'],
                'forbidden_standard_id': ['general-document'],
                'requires_standard_id': []
            },
            'standard-definition': {
                'mandatory_fields': ['title', 'info-type', 'standard_id', 'version', 'kb-id'],
                'forbidden_standard_id': [],
                'requires_standard_id': ['standard-definition']
            },
            'policy-document': {
                'mandatory_fields': ['title', 'info-type', 'standard_id', 'version', 'kb-id'],
                'forbidden_standard_id': [],
                'requires_standard_id': ['policy-document']
            },
            'technical-report': {
                'mandatory_fields': ['title', 'info-type', 'version', 'kb-id'],
                'forbidden_standard_id': ['technical-report'],
                'requires_standard_id': []
            },
            'meeting-notes': {
                'mandatory_fields': ['title', 'info-type', 'kb-id'],
                'forbidden_standard_id': ['meeting-notes'],
                'requires_standard_id': []
            }
        }
    
    def _initialize_id_patterns(self) -> Dict[str, str]:
        """Initialize ID generation patterns."""
        return {
            'kb_id': r'^[A-Z0-9\-]+$',
            'standard_id': r'^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$'
        }
    
    def save_migration_report(self, report: Dict[str, Any], output_path: str = None) -> str:
        """Save migration report to file."""
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M')
            output_path = f"tools/reports/kb-id-migration-report-{timestamp}.json"
        
        # Ensure reports directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"Migration report saved to: {output_path}")
        return output_path


def execute_kb_id_migration(dry_run: bool = True, repo_path: str = ".") -> Dict[str, Any]:
    """
    Execute universal kb_id migration process.
    
    Args:
        dry_run: If True, analyze changes without applying them
        repo_path: Path to repository root
        
    Returns:
        Migration report
    """
    migrator = UniversalKbIdMigrator(repo_path)
    
    # Execute migration
    report = migrator.execute_scope_corrections(dry_run=dry_run)
    
    # Save report
    report_path = migrator.save_migration_report(report)
    report['report_path'] = report_path
    
    return report


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal kb_id Strategy Migration")
    parser.add_argument('--execute', action='store_true', 
                       help='Execute migration (default is dry-run)')
    parser.add_argument('--repo-path', default='.', 
                       help='Path to repository root')
    parser.add_argument('--output', 
                       help='Output path for migration report')
    
    args = parser.parse_args()
    
    # Execute migration
    dry_run = not args.execute
    
    print(f"Starting universal kb_id migration (dry_run={dry_run})")
    
    migrator = UniversalKbIdMigrator(args.repo_path)
    report = migrator.execute_scope_corrections(dry_run=dry_run)
    
    # Save report
    report_path = migrator.save_migration_report(report, args.output)
    
    print(f"\nMigration {'analysis' if dry_run else 'execution'} complete!")
    print(f"Report saved to: {report_path}")
    print(f"Files processed: {report['migration_summary']['total_files_processed']}")
    print(f"Corrections needed: {report['migration_summary']['total_corrections_needed']}")
    
    if dry_run:
        print(f"\nTo execute migration, run with --execute flag")
    else:
        print(f"Corrections applied: {report['migration_summary']['corrections_applied']}")
        print(f"Success rate: {report['migration_summary']['success_rate']:.1f}%")