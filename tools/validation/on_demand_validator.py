#!/usr/bin/env python3
"""
On-Demand Validator

Implementation of Phase 5: Step 5.3 - On-Demand Validation Scripts
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module provides always-available validation without CI/CD integration,
allowing manual validation of frontmatter at any time.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json

# Add tools path for importing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from validators.graph_validator import GraphValidator
except ImportError:
    GraphValidator = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OnDemandValidator:
    """
    Always-available validation without CI/CD integration.
    
    Provides immediate validation capabilities for:
    - Current repository state
    - Specific files
    - Staged Git changes
    - Custom file selections
    """
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Initialize validator if available
        self.graph_validator = None
        if GraphValidator:
            try:
                self.graph_validator = GraphValidator()
            except Exception as e:
                self.logger.warning(f"Could not initialize GraphValidator: {e}")
        
        # Validation statistics
        self.validation_stats = {
            'total_files_checked': 0,
            'valid_files': 0,
            'invalid_files': 0,
            'errors_encountered': [],
            'validation_history': []
        }
    
    def validate_current_repository(self, output_report: bool = True) -> Dict[str, Any]:
        """
        Immediate validation of current repository state.
        
        Args:
            output_report: Whether to generate a detailed report file
            
        Returns:
            Validation results with detailed analysis
        """
        self.logger.info("Starting full repository validation")
        start_time = datetime.now()
        
        # Find all markdown files in repository
        markdown_files = list(self.repo_path.rglob("*.md"))
        self.logger.info(f"Found {len(markdown_files)} markdown files to validate")
        
        # Validate each file
        validation_results = []
        for md_file in markdown_files:
            result = self._validate_single_file(md_file)
            validation_results.append(result)
        
        # Compile comprehensive report
        processing_time = (datetime.now() - start_time).total_seconds()
        report = self._compile_validation_report(validation_results, processing_time)
        
        # Save report if requested
        if output_report:
            report_path = self._save_validation_report(report, "full-repository")
            report['report_path'] = report_path
        
        return report
    
    def validate_specific_files(self, file_paths: List[str], 
                              output_report: bool = True) -> Dict[str, Any]:
        """
        Validate specific files on demand.
        
        Args:
            file_paths: List of file paths to validate
            output_report: Whether to generate a detailed report file
            
        Returns:
            Validation results for specified files
        """
        self.logger.info(f"Validating {len(file_paths)} specific files")
        start_time = datetime.now()
        
        validation_results = []
        for file_path in file_paths:
            path = Path(file_path)
            if path.exists() and path.suffix == '.md':
                result = self._validate_single_file(path)
                validation_results.append(result)
            else:
                validation_results.append({
                    'file_path': str(path),
                    'valid': False,
                    'errors': [f"File not found or not a markdown file: {path}"],
                    'skipped': True
                })
        
        # Compile report
        processing_time = (datetime.now() - start_time).total_seconds()
        report = self._compile_validation_report(validation_results, processing_time)
        
        # Save report if requested
        if output_report:
            report_path = self._save_validation_report(report, "specific-files")
            report['report_path'] = report_path
        
        return report
    
    def validate_staged_changes(self, output_report: bool = True) -> Dict[str, Any]:
        """
        Validate only staged Git changes.
        
        Args:
            output_report: Whether to generate a detailed report file
            
        Returns:
            Validation results for staged markdown files
        """
        self.logger.info("Validating staged Git changes")
        start_time = datetime.now()
        
        # Get staged markdown files
        staged_files = self._get_staged_markdown_files()
        
        if not staged_files:
            self.logger.info("No staged markdown files found")
            return {
                'validation_summary': {
                    'total_files': 0,
                    'valid_files': 0,
                    'invalid_files': 0,
                    'overall_status': 'NO_STAGED_FILES'
                },
                'file_results': [],
                'processing_time': 0
            }
        
        self.logger.info(f"Found {len(staged_files)} staged markdown files")
        
        # Validate staged files
        validation_results = []
        for file_path in staged_files:
            result = self._validate_single_file(Path(file_path))
            validation_results.append(result)
        
        # Compile report
        processing_time = (datetime.now() - start_time).total_seconds()
        report = self._compile_validation_report(validation_results, processing_time)
        
        # Save report if requested
        if output_report:
            report_path = self._save_validation_report(report, "staged-changes")
            report['report_path'] = report_path
        
        return report
    
    def validate_directory(self, directory_path: str, recursive: bool = True,
                         output_report: bool = True) -> Dict[str, Any]:
        """
        Validate all markdown files in a specific directory.
        
        Args:
            directory_path: Directory to validate
            recursive: Whether to search subdirectories
            output_report: Whether to generate a detailed report file
            
        Returns:
            Validation results for directory
        """
        dir_path = Path(directory_path)
        if not dir_path.exists() or not dir_path.is_dir():
            return {
                'error': f"Directory not found: {directory_path}",
                'validation_summary': {'overall_status': 'DIRECTORY_NOT_FOUND'}
            }
        
        self.logger.info(f"Validating directory: {directory_path} (recursive={recursive})")
        start_time = datetime.now()
        
        # Find markdown files in directory
        if recursive:
            markdown_files = list(dir_path.rglob("*.md"))
        else:
            markdown_files = list(dir_path.glob("*.md"))
        
        self.logger.info(f"Found {len(markdown_files)} markdown files in directory")
        
        # Validate files
        validation_results = []
        for md_file in markdown_files:
            result = self._validate_single_file(md_file)
            validation_results.append(result)
        
        # Compile report
        processing_time = (datetime.now() - start_time).total_seconds()
        report = self._compile_validation_report(validation_results, processing_time)
        
        # Save report if requested
        if output_report:
            dir_name = dir_path.name or "root"
            report_path = self._save_validation_report(report, f"directory-{dir_name}")
            report['report_path'] = report_path
        
        return report
    
    def _validate_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Validate a single markdown file."""
        self.validation_stats['total_files_checked'] += 1
        
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Extract frontmatter
            frontmatter = self._extract_frontmatter(content)
            
            if not frontmatter:
                return {
                    'file_path': str(file_path),
                    'valid': False,
                    'errors': ['No frontmatter found'],
                    'warnings': [],
                    'frontmatter': None
                }
            
            # Validate frontmatter
            validation_errors = []
            validation_warnings = []
            
            # Use graph validator if available
            if self.graph_validator:
                try:
                    info_type = frontmatter.get('info-type', 'general-document')
                    validation_result = self.graph_validator.validate_frontmatter_shacl(
                        frontmatter, info_type
                    )
                    
                    if not validation_result.conforms:
                        for violation in getattr(validation_result, 'violations', []):
                            validation_errors.append(str(violation))
                            
                except Exception as e:
                    validation_warnings.append(f"SHACL validation failed: {e}")
            
            # Basic validation checks
            basic_errors = self._perform_basic_validation(frontmatter)
            validation_errors.extend(basic_errors)
            
            # Determine overall validity
            is_valid = len(validation_errors) == 0
            
            if is_valid:
                self.validation_stats['valid_files'] += 1
            else:
                self.validation_stats['invalid_files'] += 1
            
            return {
                'file_path': str(file_path),
                'valid': is_valid,
                'errors': validation_errors,
                'warnings': validation_warnings,
                'frontmatter': frontmatter
            }
            
        except Exception as e:
            error_msg = f"Error validating {file_path}: {e}"
            self.logger.error(error_msg)
            self.validation_stats['errors_encountered'].append(error_msg)
            self.validation_stats['invalid_files'] += 1
            
            return {
                'file_path': str(file_path),
                'valid': False,
                'errors': [error_msg],
                'warnings': [],
                'frontmatter': None
            }
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract YAML frontmatter from markdown content."""
        try:
            import yaml
            
            if content.startswith('---\n'):
                end_marker = content.find('\n---\n', 4)
                if end_marker != -1:
                    frontmatter_yaml = content[4:end_marker]
                    return yaml.safe_load(frontmatter_yaml)
            return None
        except Exception as e:
            self.logger.warning(f"Could not parse frontmatter: {e}")
            return None
    
    def _perform_basic_validation(self, frontmatter: Dict[str, Any]) -> List[str]:
        """Perform basic frontmatter validation checks."""
        errors = []
        
        # Check for required fields
        required_fields = ['title', 'info-type']
        for field in required_fields:
            if field not in frontmatter:
                errors.append(f"Missing required field: {field}")
        
        # Validate info-type values
        valid_info_types = [
            'general-document', 'standard-definition', 'policy-document',
            'technical-report', 'meeting-notes'
        ]
        info_type = frontmatter.get('info-type')
        if info_type and info_type not in valid_info_types:
            errors.append(f"Invalid info-type: {info_type}")
        
        # Validate standard_id pattern if present
        standard_id = frontmatter.get('standard_id')
        if standard_id:
            import re
            pattern = r'^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$'
            if not re.match(pattern, standard_id):
                errors.append(f"Invalid standard_id pattern: {standard_id}")
        
        return errors
    
    def _get_staged_markdown_files(self) -> List[str]:
        """Get list of staged markdown files from Git."""
        try:
            # Run git diff to get staged files
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Filter for markdown files
            staged_files = [
                line.strip() for line in result.stdout.split('\n')
                if line.strip().endswith('.md')
            ]
            
            return staged_files
            
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Could not get staged files: {e}")
            return []
        except FileNotFoundError:
            self.logger.warning("Git not found, cannot check staged files")
            return []
    
    def _compile_validation_report(self, validation_results: List[Dict[str, Any]], 
                                 processing_time: float) -> Dict[str, Any]:
        """Compile comprehensive validation report."""
        total_files = len(validation_results)
        valid_files = sum(1 for r in validation_results if r.get('valid', False))
        invalid_files = total_files - valid_files
        
        # Calculate success rate
        success_rate = (valid_files / total_files * 100) if total_files > 0 else 100
        
        # Group errors by type
        error_types = {}
        for result in validation_results:
            for error in result.get('errors', []):
                error_type = self._classify_error_type(error)
                error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Determine overall status
        if invalid_files == 0:
            overall_status = 'PASS'
        elif valid_files == 0:
            overall_status = 'FAIL'
        else:
            overall_status = 'PARTIAL_PASS'
        
        report = {
            'validation_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_files': total_files,
                'valid_files': valid_files,
                'invalid_files': invalid_files,
                'success_rate': success_rate,
                'overall_status': overall_status,
                'processing_time_seconds': processing_time
            },
            'error_statistics': error_types,
            'file_results': validation_results,
            'validation_configuration': {
                'shacl_validator_available': self.graph_validator is not None,
                'validation_mode': 'on_demand'
            }
        }
        
        return report
    
    def _classify_error_type(self, error_message: str) -> str:
        """Classify error message into categories."""
        error_lower = error_message.lower()
        
        if 'missing required field' in error_lower:
            return 'missing_required_field'
        elif 'invalid' in error_lower and 'pattern' in error_lower:
            return 'pattern_violation'
        elif 'shacl' in error_lower:
            return 'shacl_violation'
        elif 'frontmatter' in error_lower and 'found' not in error_lower:
            return 'frontmatter_missing'
        else:
            return 'other'
    
    def _save_validation_report(self, report: Dict[str, Any], report_type: str) -> str:
        """Save validation report to file."""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        report_filename = f"validation-{report_type}-{timestamp}.json"
        report_path = self.repo_path / "tools" / "reports" / report_filename
        
        # Ensure reports directory exists
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save report
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"Validation report saved to: {report_path}")
        return str(report_path)
    
    def get_validation_statistics(self) -> Dict[str, Any]:
        """Get overall validation statistics."""
        return self.validation_stats.copy()


def main():
    """Command-line interface for on-demand validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="On-Demand Frontmatter Validation")
    parser.add_argument('--mode', choices=['repository', 'staged', 'files', 'directory'],
                       default='repository', help='Validation mode')
    parser.add_argument('--files', nargs='+', help='Specific files to validate')
    parser.add_argument('--directory', help='Directory to validate')
    parser.add_argument('--recursive', action='store_true', 
                       help='Recursive directory search')
    parser.add_argument('--no-report', action='store_true',
                       help='Skip generating report file')
    parser.add_argument('--repo-path', default='.', help='Repository path')
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = OnDemandValidator(args.repo_path)
    
    # Execute validation based on mode
    if args.mode == 'repository':
        print("Validating entire repository...")
        result = validator.validate_current_repository(not args.no_report)
    elif args.mode == 'staged':
        print("Validating staged changes...")
        result = validator.validate_staged_changes(not args.no_report)
    elif args.mode == 'files':
        if not args.files:
            print("Error: --files required for files mode")
            return 1
        print(f"Validating specific files: {args.files}")
        result = validator.validate_specific_files(args.files, not args.no_report)
    elif args.mode == 'directory':
        if not args.directory:
            print("Error: --directory required for directory mode")
            return 1
        print(f"Validating directory: {args.directory}")
        result = validator.validate_directory(args.directory, args.recursive, not args.no_report)
    
    # Print summary
    summary = result['validation_summary']
    print(f"\nValidation Summary:")
    print(f"  Total files: {summary['total_files']}")
    print(f"  Valid files: {summary['valid_files']}")
    print(f"  Invalid files: {summary['invalid_files']}")
    print(f"  Success rate: {summary.get('success_rate', 0):.1f}%")
    print(f"  Overall status: {summary['overall_status']}")
    
    if 'report_path' in result:
        print(f"  Report saved: {result['report_path']}")
    
    # Return appropriate exit code
    return 0 if summary['overall_status'] in ['PASS', 'NO_STAGED_FILES'] else 1


if __name__ == "__main__":
    sys.exit(main())