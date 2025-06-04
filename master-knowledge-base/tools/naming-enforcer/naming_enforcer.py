#!/usr/bin/env python3
"""
Naming Convention Enforcer v2.0 - Single Source of Truth
Parses GM-CONVENTIONS-NAMING.md directly for all naming rules and configurations.

This enforcer eliminates JSON configuration files by extracting everything
from the authoritative markdown document.
"""

import os
import sys
import re
import json
import argparse
import shutil
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple, Union
from collections import defaultdict
from datetime import datetime
import yaml
from uuid import uuid4
import fnmatch

@dataclass
class NamingRule:
    """Represents a naming rule extracted from the standard"""
    context: str
    rule_type: str  # 'pattern', 'protected', 'exception'
    pattern: str
    examples: List[str] = field(default_factory=list)
    rationale: str = ""

@dataclass
class NamingViolation:
    path: str
    current_name: str
    suggested_name: str
    violation_type: str
    severity: str
    reason: str
    context: str

@dataclass
class ContentUpdate:
    file_path: str
    line_number: int
    old_text: str
    new_text: str
    context: str
    update_type: str

@dataclass
class RenameOperation:
    old_path: Path
    new_path: Path
    violation_type: str
    content_updates: List[ContentUpdate] = field(default_factory=list)

@dataclass
class OperationLog:
    """Comprehensive operation logging for reversibility"""
    operation_id: str
    timestamp: str
    operation_type: str  # 'rename', 'content_update', 'backup', 'rollback'
    source_path: str
    target_path: str = ""
    old_content: str = ""
    new_content: str = ""
    status: str = "pending"  # 'pending', 'success', 'failed', 'rolled_back'
    error_message: str = ""

@dataclass
class BackupManifest:
    """Manifest for tracking backups and enabling rollback"""
    backup_id: str
    timestamp: str
    operation_description: str
    backed_up_files: List[str] = field(default_factory=list)
    backup_directory: str = ""

@dataclass
class ExcludePattern:
    """Represents an exclusion pattern with metadata"""
    pattern: str
    pattern_type: str  # 'file', 'directory', 'glob', 'regex'
    is_absolute: bool = False
    description: str = ""

@dataclass
class IncludePattern:
    """Represents an inclusion pattern with metadata"""
    pattern: str
    pattern_type: str  # 'file', 'directory', 'glob', 'regex'
    is_absolute: bool = False
    description: str = ""

class ExcludeManager:
    """Manages all exclusion patterns and logic for the naming enforcer"""
    
    def __init__(self):
        self.exclude_patterns: List[ExcludePattern] = []
        self.exclude_files: Set[Path] = set()
        self.exclude_directories: Set[Path] = set()
        self.exclude_globs: List[str] = []
        self.exclude_regexes: List[re.Pattern] = []
        
    def add_exclude_file(self, file_path: Union[str, Path], description: str = ""):
        """Add a single file to exclusions"""
        path = Path(file_path).resolve()
        self.exclude_files.add(path)
        self.exclude_patterns.append(ExcludePattern(
            pattern=str(path),
            pattern_type='file',
            is_absolute=True,
            description=description or f"Excluded file: {path.name}"
        ))
    
    def add_exclude_directory(self, dir_path: Union[str, Path], description: str = ""):
        """Add a single directory to exclusions"""
        path = Path(dir_path).resolve()
        self.exclude_directories.add(path)
        self.exclude_patterns.append(ExcludePattern(
            pattern=str(path),
            pattern_type='directory',
            is_absolute=True,
            description=description or f"Excluded directory: {path.name}"
        ))
    
    def add_exclude_glob(self, glob_pattern: str, description: str = ""):
        """Add a glob pattern to exclusions"""
        self.exclude_globs.append(glob_pattern)
        self.exclude_patterns.append(ExcludePattern(
            pattern=glob_pattern,
            pattern_type='glob',
            is_absolute=False,
            description=description or f"Excluded glob: {glob_pattern}"
        ))
    
    def add_exclude_regex(self, regex_pattern: str, description: str = ""):
        """Add a regex pattern to exclusions"""
        try:
            compiled_regex = re.compile(regex_pattern)
            self.exclude_regexes.append(compiled_regex)
            self.exclude_patterns.append(ExcludePattern(
                pattern=regex_pattern,
                pattern_type='regex',
                is_absolute=False,
                description=description or f"Excluded regex: {regex_pattern}"
            ))
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{regex_pattern}': {e}")
    
    def load_exclude_file(self, exclude_file_path: Union[str, Path]):
        """Load exclusions from a file (one pattern per line)"""
        exclude_file = Path(exclude_file_path)
        if not exclude_file.exists():
            raise FileNotFoundError(f"Exclude file not found: {exclude_file}")
        
        with open(exclude_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Determine pattern type based on content
                if line.startswith('regex:'):
                    pattern = line[6:].strip()
                    self.add_exclude_regex(pattern, f"From {exclude_file.name}:{line_num}")
                elif line.startswith('glob:'):
                    pattern = line[5:].strip()
                    self.add_exclude_glob(pattern, f"From {exclude_file.name}:{line_num}")
                elif '*' in line or '?' in line or '[' in line:
                    # Looks like a glob pattern
                    self.add_exclude_glob(line, f"From {exclude_file.name}:{line_num}")
                else:
                    # Treat as file or directory path
                    path = Path(line)
                    if path.is_absolute() or line.startswith('./') or line.startswith('../'):
                        # Absolute or relative path
                        resolved_path = path.resolve() if path.exists() else path
                        if resolved_path.is_dir() or line.endswith('/'):
                            self.add_exclude_directory(resolved_path, f"From {exclude_file.name}:{line_num}")
                        else:
                            self.add_exclude_file(resolved_path, f"From {exclude_file.name}:{line_num}")
                    else:
                        # Treat as glob pattern for relative paths
                        self.add_exclude_glob(line, f"From {exclude_file.name}:{line_num}")
    
    def is_excluded(self, path: Path) -> bool:
        """Check if a path should be excluded"""
        resolved_path = path.resolve()
        path_str = str(resolved_path)
        relative_path_str = str(path)
        
        # Check exact file matches
        if resolved_path in self.exclude_files:
            return True
        
        # Check if path is within any excluded directory
        for exclude_dir in self.exclude_directories:
            try:
                resolved_path.relative_to(exclude_dir)
                return True  # Path is within excluded directory
            except ValueError:
                continue  # Path is not within this excluded directory
        
        # Check glob patterns against both absolute and relative paths
        for glob_pattern in self.exclude_globs:
            if (fnmatch.fnmatch(path_str, glob_pattern) or 
                fnmatch.fnmatch(relative_path_str, glob_pattern) or
                fnmatch.fnmatch(path.name, glob_pattern)):
                return True
        
        # Check regex patterns
        for regex_pattern in self.exclude_regexes:
            if (regex_pattern.search(path_str) or 
                regex_pattern.search(relative_path_str) or
                regex_pattern.search(path.name)):
                return True
        
        return False
    
    def get_exclusion_summary(self) -> str:
        """Get a summary of all exclusion patterns"""
        if not self.exclude_patterns:
            return "No exclusions configured"
        
        summary = ["Exclusion Summary:"]
        by_type = defaultdict(list)
        
        for pattern in self.exclude_patterns:
            by_type[pattern.pattern_type].append(pattern)
        
        for pattern_type, patterns in by_type.items():
            summary.append(f"  {pattern_type.title()}s ({len(patterns)}):")
            for pattern in patterns[:5]:  # Show first 5
                summary.append(f"    - {pattern.pattern}")
            if len(patterns) > 5:
                summary.append(f"    ... and {len(patterns) - 5} more")
        
        return "\n".join(summary)

class IncludeManager:
    """Manages all inclusion patterns and logic for the naming enforcer"""
    
    def __init__(self):
        self.include_patterns: List[IncludePattern] = []
        self.include_files: Set[Path] = set()
        self.include_directories: Set[Path] = set()
        self.include_globs: List[str] = []
        self.include_regexes: List[re.Pattern] = []
        
    def add_include_file(self, file_path: Union[str, Path], description: str = ""):
        """Add a single file to inclusions"""
        path = Path(file_path).resolve()
        self.include_files.add(path)
        self.include_patterns.append(IncludePattern(
            pattern=str(path),
            pattern_type='file',
            is_absolute=True,
            description=description or f"Included file: {path.name}"
        ))
    
    def add_include_directory(self, dir_path: Union[str, Path], description: str = ""):
        """Add a single directory to inclusions"""
        path = Path(dir_path).resolve()
        self.include_directories.add(path)
        self.include_patterns.append(IncludePattern(
            pattern=str(path),
            pattern_type='directory',
            is_absolute=True,
            description=description or f"Included directory: {path.name}"
        ))
    
    def add_include_glob(self, glob_pattern: str, description: str = ""):
        """Add a glob pattern to inclusions"""
        self.include_globs.append(glob_pattern)
        self.include_patterns.append(IncludePattern(
            pattern=glob_pattern,
            pattern_type='glob',
            is_absolute=False,
            description=description or f"Included glob: {glob_pattern}"
        ))
    
    def add_include_regex(self, regex_pattern: str, description: str = ""):
        """Add a regex pattern to inclusions"""
        try:
            compiled_regex = re.compile(regex_pattern)
            self.include_regexes.append(compiled_regex)
            self.include_patterns.append(IncludePattern(
                pattern=regex_pattern,
                pattern_type='regex',
                is_absolute=False,
                description=description or f"Included regex: {regex_pattern}"
            ))
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{regex_pattern}': {e}")
    
    def load_include_file(self, include_file_path: Union[str, Path]):
        """Load inclusions from a file (one pattern per line)"""
        include_file = Path(include_file_path)
        if not include_file.exists():
            raise FileNotFoundError(f"Include file not found: {include_file}")
        
        with open(include_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Determine pattern type based on content
                if line.startswith('regex:'):
                    pattern = line[6:].strip()
                    self.add_include_regex(pattern, f"From {include_file.name}:{line_num}")
                elif line.startswith('glob:'):
                    pattern = line[5:].strip()
                    self.add_include_glob(pattern, f"From {include_file.name}:{line_num}")
                elif '*' in line or '?' in line or '[' in line:
                    # Looks like a glob pattern
                    self.add_include_glob(line, f"From {include_file.name}:{line_num}")
                else:
                    # Treat as file or directory path
                    path = Path(line)
                    if path.is_absolute() or line.startswith('./') or line.startswith('../'):
                        # Absolute or relative path
                        resolved_path = path.resolve() if path.exists() else path
                        if resolved_path.is_dir() or line.endswith('/'):
                            self.add_include_directory(resolved_path, f"From {include_file.name}:{line_num}")
                        else:
                            self.add_include_file(resolved_path, f"From {include_file.name}:{line_num}")
                    else:
                        # Treat as glob pattern for relative paths
                        self.add_include_glob(line, f"From {include_file.name}:{line_num}")
    
    def is_included(self, path: Path) -> bool:
        """Check if a path should be included"""
        # If no include patterns are configured, include everything by default
        if not self.include_patterns:
            return True
            
        resolved_path = path.resolve()
        path_str = str(resolved_path)
        relative_path_str = str(path)
        
        # Check exact file matches
        if resolved_path in self.include_files:
            return True
        
        # Check if path is within any included directory
        for include_dir in self.include_directories:
            try:
                resolved_path.relative_to(include_dir)
                return True  # Path is within included directory
            except ValueError:
                continue  # Path is not within this included directory
        
        # Check glob patterns against both absolute and relative paths
        for glob_pattern in self.include_globs:
            if (fnmatch.fnmatch(path_str, glob_pattern) or 
                fnmatch.fnmatch(relative_path_str, glob_pattern) or
                fnmatch.fnmatch(path.name, glob_pattern)):
                return True
        
        # Check regex patterns
        for regex_pattern in self.include_regexes:
            if (regex_pattern.search(path_str) or 
                regex_pattern.search(relative_path_str) or
                regex_pattern.search(path.name)):
                return True
        
        return False
    
    def get_inclusion_summary(self) -> str:
        """Get a summary of all inclusion patterns"""
        if not self.include_patterns:
            return "No inclusions configured (processing all files)"
        
        summary = ["Inclusion Summary:"]
        by_type = defaultdict(list)
        
        for pattern in self.include_patterns:
            by_type[pattern.pattern_type].append(pattern)
        
        for pattern_type, patterns in by_type.items():
            summary.append(f"  {pattern_type.title()}s ({len(patterns)}):")
            for pattern in patterns[:5]:  # Show first 5
                summary.append(f"    - {pattern.pattern}")
            if len(patterns) > 5:
                summary.append(f"    ... and {len(patterns) - 5} more")
        
        return "\n".join(summary)

class SafetyLogger:
    """Comprehensive logging system with emergency rollback capabilities"""
    
    def __init__(self, operation_name: str = "naming_enforcer_operation"):
        self.operation_name = operation_name
        self.operation_id = f"{operation_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.logs: List[OperationLog] = []
        self.backup_manifest: Optional[BackupManifest] = None
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup structured logging to files"""
        # Get the repo root by going up from the current script location
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent.parent.parent  # Go up from tools/naming-enforcer to repo root
        log_dir = repo_root / "master-knowledge-base" / "tools" / "reports"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Operation log file
        log_file = log_dir / f"{self.operation_id}.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(self.operation_name)
        self.logger.info(f"Started operation: {self.operation_id}")
    
    def log_operation(self, operation_type: str, source_path: str, target_path: str = "", 
                     old_content: str = "", new_content: str = ""):
        """Log a single operation"""
        op_log = OperationLog(
            operation_id=f"{self.operation_id}_{len(self.logs):04d}",
            timestamp=datetime.now().isoformat(),
            operation_type=operation_type,
            source_path=source_path,
            target_path=target_path,
            old_content=old_content,
            new_content=new_content
        )
        self.logs.append(op_log)
        
        self.logger.info(f"LOG {operation_type}: {source_path} -> {target_path}")
        return op_log
    
    def mark_success(self, operation_log: OperationLog):
        """Mark operation as successful"""
        operation_log.status = "success"
        self.logger.info(f"SUCCESS: {operation_log.operation_id}")
    
    def mark_failed(self, operation_log: OperationLog, error_message: str):
        """Mark operation as failed"""
        operation_log.status = "failed"
        operation_log.error_message = error_message
        self.logger.error(f"FAILED: {operation_log.operation_id} - {error_message}")
    
    def create_backup(self, files_to_backup: List[Path], operation_description: str) -> bool:
        """Create timestamped backup of files before modification"""
        try:
            # Get the repo root by going up from the current script location
            script_dir = Path(__file__).parent
            repo_root = script_dir.parent.parent.parent  # Go up from tools/naming-enforcer to repo root
            backup_dir = repo_root / "master-knowledge-base" / "tools" / "reports" / "backups" / self.operation_id
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            self.backup_manifest = BackupManifest(
                backup_id=self.operation_id,
                timestamp=datetime.now().isoformat(),
                operation_description=operation_description,
                backup_directory=str(backup_dir)
            )
            
            for file_path in files_to_backup:
                if file_path.exists():
                    backup_file = backup_dir / file_path.name
                    shutil.copy2(file_path, backup_file)
                    self.backup_manifest.backed_up_files.append(str(file_path))
                    self.logger.info(f"BACKUP: Backed up: {file_path}")
            
            # Save backup manifest
            manifest_file = backup_dir / "backup-manifest.json"
            with open(manifest_file, 'w') as f:
                json.dump({
                    "backup_id": self.backup_manifest.backup_id,
                    "timestamp": self.backup_manifest.timestamp,
                    "operation_description": self.backup_manifest.operation_description,
                    "backed_up_files": self.backup_manifest.backed_up_files,
                    "backup_directory": self.backup_manifest.backup_directory
                }, f, indent=2)
            
            self.logger.info(f"📦 Created backup: {backup_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"ERROR: Backup failed: {e}")
            return False
    
    def save_operation_log(self):
        """Save complete operation log for rollback capabilities"""
        # Get the repo root by going up from the current script location
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent.parent.parent  # Go up from tools/naming-enforcer to repo root
        log_dir = repo_root / "master-knowledge-base" / "tools" / "reports"
        log_file = log_dir / f"{self.operation_id}_operations.json"
        
        log_data = {
            "operation_id": self.operation_id,
            "timestamp": datetime.now().isoformat(),
            "operation_name": self.operation_name,
            "total_operations": len(self.logs),
            "operations": [
                {
                    "operation_id": log.operation_id,
                    "timestamp": log.timestamp,
                    "operation_type": log.operation_type,
                    "source_path": log.source_path,
                    "target_path": log.target_path,
                    "old_content": log.old_content[:1000] if log.old_content else "",  # Truncate for file size
                    "new_content": log.new_content[:1000] if log.new_content else "",
                    "status": log.status,
                    "error_message": log.error_message
                } for log in self.logs
            ],
            "backup_manifest": {
                "backup_id": self.backup_manifest.backup_id if self.backup_manifest else "",
                "timestamp": self.backup_manifest.timestamp if self.backup_manifest else "",
                "operation_description": self.backup_manifest.operation_description if self.backup_manifest else "",
                "backed_up_files": self.backup_manifest.backed_up_files if self.backup_manifest else [],
                "backup_directory": self.backup_manifest.backup_directory if self.backup_manifest else ""
            } if self.backup_manifest else None
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        self.logger.info(f"SAVED: Saved operation log: {log_file}")
    
    def finalize_operation(self):
        """Finalize logging and provide summary"""
        successes = len([log for log in self.logs if log.status == "success"])
        failures = len([log for log in self.logs if log.status == "failed"])
        
        self.logger.info(f"COMPLETE: Operation complete: {self.operation_id}")
        self.logger.info(f"SUCCESS: Successful operations: {successes}")
        self.logger.info(f"ERROR: Failed operations: {failures}")
        
        self.save_operation_log()
        
        if failures > 0:
            self.logger.warning(f"WARNING: {failures} operations failed - check logs for details")
            self.logger.warning(f"INFO: Use rollback functionality if needed")

class NamingStandardParser:
    """Parse naming standards from the official document"""
    
    def __init__(self, standard_path: str = None):
        if standard_path is None:
            # Get the repo root by going up from the current script location
            script_dir = Path(__file__).parent
            repo_root = script_dir.parent.parent.parent  # Go up from tools/naming-enforcer to repo root
            self.standard_path = repo_root / "master-knowledge-base" / "standards" / "src" / "GM-CONVENTIONS-NAMING.md"
        else:
            self.standard_path = Path(standard_path)
        self.raw_content = ""
        self.rules: Dict[str, List[NamingRule]] = {}
        self.protected_names: Dict[str, Set[str]] = {}
        self.exceptions: Dict[str, List[str]] = {}
        self.patterns: Dict[str, str] = {}
        
        if self.standard_path.exists():
            self.load_and_parse()
        else:
            raise FileNotFoundError(f"Naming standard not found: {self.standard_path}")
    
    def load_and_parse(self):
        """Load and parse the naming standard document"""
        with open(self.standard_path, 'r', encoding='utf-8') as f:
            self.raw_content = f.read()
        
        self.extract_context_patterns()
        self.extract_protected_names()
        self.extract_exceptions()
        self.extract_validation_rules()
    
    def extract_context_patterns(self):
        """Extract naming patterns for different contexts"""
        # Section 1: CONTEXT-SPECIFIC NAMING RULES
        patterns = {
            'kebab-case': r'^[a-z0-9]+(-[a-z0-9]+)*$',
            'kebab-case-with-prefix': r'^-?[a-z0-9]+(-[a-z0-9]+)*$',  # Allow optional leading hyphen for sorting
            'snake_case': r'^[a-z_][a-z0-9_]*$',
            'tool_reports': r'^[a-zA-Z0-9_-]+$',  # Lenient pattern for tool-generated reports
            'PascalCase': r'^[A-Z][a-zA-Z0-9]*$',
            'camelCase': r'^[a-z][a-zA-Z0-9]*$',
            'UPPER_SNAKE_CASE': r'^[A-Z_][A-Z0-9_]*$',
            'DOMAIN-SUBDOMAIN-NAME': r'^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$'  # FIXED: Exact pattern from GM-CONVENTIONS-NAMING.md
        }
        
        # Extract standard ID prefixes from the document
        self.standard_id_prefixes = self.extract_standard_id_prefixes()
        
        # Extract specific contexts from document
        context_mapping = {
            'files_and_directories': 'kebab-case',
            'directories_with_prefix': 'kebab-case-with-prefix',  # For active project directories that start with -
            'python_variables': 'snake_case',
            'python_functions': 'snake_case',
            'python_classes': 'PascalCase',
            'python_constants': 'UPPER_SNAKE_CASE',
            'frontmatter_fields': 'snake_case',
            'json_yaml_keys': 'snake_case',
            'standard_ids': 'DOMAIN-SUBDOMAIN-NAME',
            'tool_reports': 'tool_reports',  # Lenient naming for tool-generated files
            'javascript_variables': 'camelCase',
            'javascript_functions': 'camelCase',
            'javascript_classes': 'PascalCase',
            'javascript_constants': 'UPPER_SNAKE_CASE',
            'tags_metadata': 'kebab-case',
            'key_references': 'camelCase'
        }
        
        # Store patterns with contexts
        for context, pattern_name in context_mapping.items():
            if pattern_name in patterns:
                self.patterns[context] = patterns[pattern_name]
    
    def extract_protected_names(self):
        """Extract protected names from Section 2"""
        # Find Section 2: PROTECTED NAMES
        protected_section_match = re.search(
            r'## 2\. PROTECTED NAMES.*?(?=## 3\.|$)', 
            self.raw_content, 
            re.DOTALL
        )
        
        if not protected_section_match:
            return
        
        protected_content = protected_section_match.group(0)
        
        # Extract different categories of protected names
        categories = {
            'python_variables': r'### 2\.1 Python Variable Dependencies\s*```\s*([^`]+)```',
            'frontmatter_fields': r'### 2\.2 Frontmatter Field Names.*?```\s*([^`]+)```',
            'config_files': r'### 2\.3 Configuration File Names\s*```\s*([^`]+)```',
            'tool_scripts': r'### 2\.4 Tool Script Names\s*```\s*([^`]+)```',
            'json_keys': r'### 2\.5 JSON/YAML Configuration Keys\s*```\s*([^`]+)```',
            'environment_vars': r'### 2\.6 Environment Variables\s*```\s*([^`]+)```'
        }
        
        for category, pattern in categories.items():
            match = re.search(pattern, protected_content, re.DOTALL)
            if match:
                names_text = match.group(1).strip()
                # Better parsing: split by newlines and commas, clean up
                names = []
                for line in names_text.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Split by commas and clean each name
                        line_names = [name.strip().rstrip(',') for name in line.split(',')]
                        names.extend([name for name in line_names if name])
                self.protected_names[category] = set(names)
        
        # Add additional protected files based on standard conventions
        additional_protected_files = {
            'LICENSE', 'README.md', 'CHANGELOG.md', 'Makefile',
            'Dockerfile', '.gitignore', '.eslintrc.js'
        }
        if 'config_files' not in self.protected_names:
            self.protected_names['config_files'] = set()
        self.protected_names['config_files'].update(additional_protected_files)
    
    def extract_exceptions(self):
        """Extract validation exceptions from Section 3 and Section 4.2"""
        # Find Section 3: VALIDATION RULES
        validation_section_match = re.search(
            r'## 3\. VALIDATION RULES.*?(?=## 4\.|$)', 
            self.raw_content, 
            re.DOTALL
        )
        
        if validation_section_match:
            validation_content = validation_section_match.group(0)
            
            # Extract exception patterns
            temp_files_match = re.search(r'Skip validation for files matching `([^`]+)`', validation_content)
            if temp_files_match:
                temp_patterns = [p.strip('`').strip() for p in temp_files_match.group(1).split('`,')]
                self.exceptions['temp_files'] = temp_patterns
            
            system_dirs_match = re.search(r'Exclude `([^`]+)`', validation_content)
            if system_dirs_match:
                system_dirs = [d.strip('`').strip() for d in system_dirs_match.group(1).split('`,')]
                self.exceptions['system_directories'] = system_dirs
        
        # Look for Section 4.2 Naming Exceptions JSON Generation template
        exceptions_template_match = re.search(
            r'### 4\.2 Naming Exceptions JSON Generation.*?```json\s*({.*?})\s*```',
            self.raw_content,
            re.DOTALL
        )
        
        if exceptions_template_match:
            try:
                import json
                template_json = json.loads(exceptions_template_match.group(1))
                
                # Merge with existing exceptions
                if 'directories' in template_json:
                    self.exceptions.setdefault('system_directories', []).extend(template_json['directories'])
                
                if 'files' in template_json:
                    self.exceptions.setdefault('protected_files', []).extend(template_json['files'])
                
                if 'patterns' in template_json:
                    self.exceptions.setdefault('temp_files', []).extend(template_json['patterns'])
                
                # Remove duplicates
                for key in self.exceptions:
                    if isinstance(self.exceptions[key], list):
                        self.exceptions[key] = list(set(self.exceptions[key]))
                        
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Add commonly excluded patterns if not found
        if 'system_directories' not in self.exceptions:
            self.exceptions['system_directories'] = []
        
        common_system_dirs = [
            '__pycache__', 'node_modules', '.git', '.vscode',
            'dist', 'build', 'target', 'bin', 'obj',
            '.obsidian', '.space', 'archive'  # Add Obsidian and archive exclusions
        ]
        self.exceptions['system_directories'].extend(common_system_dirs)
        self.exceptions['system_directories'] = list(set(self.exceptions['system_directories']))
        
        if 'temp_files' not in self.exceptions:
            self.exceptions['temp_files'] = []
        
        common_temp_patterns = [
            '*.min.js', '*.bundle.*', '*.tmp', '*.temp', '*.bak',
            '*.log', '*.pid', '.*'
        ]
        self.exceptions['temp_files'].extend(common_temp_patterns)
        self.exceptions['temp_files'] = list(set(self.exceptions['temp_files']))
    
    def extract_standard_id_prefixes(self):
        """Extract standard ID prefixes from the document examples and references"""
        prefixes = set()
        
        # Extract from Section 1.5 examples
        section_1_5_match = re.search(
            r'### 1\.5 Standard IDs.*?- \*\*Examples\*\*: `([^`]+)`', 
            self.raw_content, 
            re.DOTALL
        )
        if section_1_5_match:
            examples = section_1_5_match.group(1)
            # Extract standard IDs like GM-CONVENTIONS-NAMING, MT-SCHEMA-FRONTMATTER
            standard_ids = re.findall(r'([A-Z]{1,6})-[A-Z0-9-]+', examples)
            prefixes.update(standard_ids)
        
        # Extract from Section 5.1 references
        section_5_1_match = re.search(
            r'### 5\.1 Standards That Must Reference.*?(?=### 5\.2|## 6\.)', 
            self.raw_content, 
            re.DOTALL
        )
        if section_5_1_match:
            references = section_5_1_match.group(0)
            # Extract standard IDs from references like **SF-SYNTAX-YAML-FRONTMATTER**
            standard_ids = re.findall(r'\*\*([A-Z]{1,6})-[A-Z0-9-]+\*\*', references)
            prefixes.update(standard_ids)
        
        # Also scan for any standard_id in frontmatter examples
        frontmatter_examples = re.findall(r'standard_id:\s*([A-Z]{1,6})-[A-Z0-9-]+', self.raw_content)
        prefixes.update(frontmatter_examples)
        
        # Scan entire document for any standard ID patterns to catch all prefixes
        all_standard_ids = re.findall(r'\b([A-Z]{1,6})-[A-Z]{1,15}-[A-Z0-9\-]+\b', self.raw_content)
        prefixes.update(all_standard_ids)
        
        # More aggressive scan for patterns like U-ARCH-003, QM-VALIDATION, etc.
        simple_patterns = re.findall(r'\b([A-Z]{1,6})-[A-Z]+', self.raw_content)
        prefixes.update(simple_patterns)
        
        # Default fallback prefixes if extraction fails
        if not prefixes:
            prefixes = {'SF', 'MT', 'UA', 'AS', 'CS', 'GM', 'OM', 'QM', 'U'}
        
        return sorted(prefixes)
    
    def extract_validation_rules(self):
        """Extract validation hierarchy and rules"""
        # This would extract the validation hierarchy from Section 3.3
        # For now, implementing the basic hierarchy
        self.validation_hierarchy = [
            'protected_names',
            'context_rules',
            'exception_patterns',
            'default_rule'
        ]
    
    def get_naming_pattern(self, context: str) -> Optional[str]:
        """Get regex pattern for a specific context"""
        return self.patterns.get(context)
    
    def is_protected_name(self, name: str, category: str = None) -> bool:
        """Check if a name is protected"""
        if category:
            return name in self.protected_names.get(category, set())
        
        # Check all categories if no specific category given
        for protected_set in self.protected_names.values():
            if name in protected_set:
                return True
        return False
    
    def is_exception(self, path: Path) -> bool:
        """Check if path matches any exception patterns"""
        path_str = str(path).replace('\\', '/')
        
        # Check system directories
        for sys_dir in self.exceptions.get('system_directories', []):
            if sys_dir in path_str:
                return True
        
        # Check protected files
        if path.is_file():
            filename = path.name
            
            # Check protected files list
            for protected_file in self.exceptions.get('protected_files', []):
                if filename == protected_file:
                    return True
            
            # Check if it's in the protected config files
            if filename in self.protected_names.get('config_files', set()):
                return True
            
            # Check temp file patterns
            for pattern in self.exceptions.get('temp_files', []):
                # Handle glob patterns
                if '*' in pattern:
                    if fnmatch.fnmatch(filename, pattern):
                        return True
                elif filename == pattern:
                    return True
        
        # Check if directory name itself is protected
        if path.is_dir():
            dir_name = path.name
            for sys_dir in self.exceptions.get('system_directories', []):
                if dir_name == sys_dir.rstrip('/'):
                    return True
        
        return False

class NamingEnforcerV2:
    """Advanced naming convention enforcer with comprehensive violation detection"""
    
    def __init__(self, standard_path: str = None):
        if standard_path is None:
            # Get the repo root by going up from the current script location
            script_dir = Path(__file__).parent
            repo_root = script_dir.parent.parent.parent  # Go up from tools/naming-enforcer to repo root
            standard_path = str(repo_root / "master-knowledge-base" / "standards" / "src" / "GM-CONVENTIONS-NAMING.md")
        
        self.parser = NamingStandardParser(standard_path)
        self.violations: List[NamingViolation] = []
        self.rename_operations: List[RenameOperation] = []
        self.exclude_manager = ExcludeManager()
        self.include_manager = IncludeManager()
        
        # Load automatic ignore/include files if they exist
        self._load_automatic_files()
        
        # Compiled regex patterns for performance
        self.compiled_patterns = {
            context: re.compile(pattern)
            for context, pattern in self.parser.patterns.items()
        }
    
    def _load_automatic_files(self, scan_directory: Path = None):
        """Load .namingignore and .naminginclude files automatically"""
        # Determine the directory to look for automatic files
        if scan_directory is None:
            scan_directory = Path.cwd()
        else:
            scan_directory = Path(scan_directory)
        
        # Load .namingignore file
        namingignore_file = scan_directory / ".namingignore"
        if namingignore_file.exists():
            try:
                self.exclude_manager.load_exclude_file(namingignore_file)
                print(f"Loaded exclusions from: {namingignore_file}")
            except Exception as e:
                print(f"Warning: Could not load .namingignore file: {e}")
        
        # Load .naminginclude file
        naminginclude_file = scan_directory / ".naminginclude"
        if naminginclude_file.exists():
            try:
                self.include_manager.load_include_file(naminginclude_file)
                print(f"Loaded inclusions from: {naminginclude_file}")
            except Exception as e:
                print(f"Warning: Could not load .naminginclude file: {e}")
    
    def reload_automatic_files(self, scan_directory: Path = None):
        """Reload automatic files for a specific scan directory"""
        # Only reload if scan directory is different from current working directory
        if scan_directory is None:
            scan_directory = Path.cwd()
        else:
            scan_directory = Path(scan_directory)
        
        # Only reload if we're scanning a different directory than where we initially loaded from
        if scan_directory.resolve() != Path.cwd().resolve():
            self._load_automatic_files(scan_directory)
    
    def get_context_for_path(self, path: Path) -> str:
        """Determine the naming context for a given path"""
        path_str = str(path).replace('\\', '/')
        
        # Special context rules based on path
        if '/tools/' in path_str:
            if path.suffix == '.py':
                if path.name.endswith('_test.py') or '/tests/' in path_str:
                    return 'python_variables'  # Use snake_case for test files
                return 'python_variables'  # Scripts use snake_case
            elif path.suffix == '.md' and '/reports/' in path_str:
                return 'tool_reports'  # Tool reports use lenient naming
        
        # Registry files should use snake_case for data consistency
        if '/registry/' in path_str and path.suffix in ['.txt', '.yaml', '.yml']:
            return 'python_variables'  # Registry data files use snake_case
        
        if path.suffix == '.py':
            return 'python_variables'
        
        if path.suffix in ['.js', '.ts']:
            return 'javascript_variables'
        
        # JSON/YAML files are treated as regular files for naming (kebab-case filenames)
        # Only their internal content should use snake_case keys
        
        if path.suffix == '.md':
            # Check if filename matches standard ID pattern using extracted prefixes
            for prefix in self.parser.standard_id_prefixes:
                if path.stem.startswith(f'{prefix}-'):
                    return 'standard_ids'
            return 'files_and_directories'
        
        if path.is_dir():
            # Check if this is an active project directory that starts with hyphen for sorting
            if path.name.startswith('-') and ('active-project' in path_str or 'project' in path.name):
                return 'directories_with_prefix'
            return 'files_and_directories'
        
        return 'files_and_directories'  # Default
    
    def validate_name(self, name: str, context: str) -> Tuple[bool, Optional[str]]:
        """Validate a name against its context rules"""
        # Check if it's a protected name first
        if self.parser.is_protected_name(name):
            return True, None  # Protected names are always valid
        
        # Get the appropriate pattern
        if context not in self.compiled_patterns:
            context = 'files_and_directories'  # Fallback
        
        pattern = self.compiled_patterns[context]
        
        if pattern.match(name):
            return True, None
        
        # Generate suggestion based on context
        suggestion = self.convert_to_context_convention(name, context)
        return False, suggestion
    
    def convert_to_context_convention(self, name: str, context: str) -> str:
        """Convert name to the appropriate convention for the context"""
        if context in ['files_and_directories', 'tags_metadata']:
            return self.to_kebab_case(name)
        elif context == 'directories_with_prefix':
            # For directories that can start with hyphen, preserve the hyphen if it exists
            if name.startswith('-'):
                return '-' + self.to_kebab_case(name[1:])
            return self.to_kebab_case(name)
        elif context == 'tool_reports':
            # Tool reports are already in acceptable format - minimal conversion
            return name
        elif context in ['python_variables', 'python_functions', 'frontmatter_fields', 'json_yaml_keys']:
            return self.to_snake_case(name)
        elif context in ['python_classes', 'javascript_classes']:
            return self.to_pascal_case(name)
        elif context in ['javascript_variables', 'javascript_functions', 'key_references']:
            return self.to_camel_case(name)
        elif context == 'python_constants' or context == 'javascript_constants':
            return self.to_upper_snake_case(name)
        else:
            return self.to_kebab_case(name)  # Default
    
    def to_kebab_case(self, name: str) -> str:
        """Convert to kebab-case"""
        # Handle camelCase and PascalCase
        name = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '-', name)
        # Handle acronyms
        name = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', '-', name)
        # Convert underscores to hyphens
        name = name.replace('_', '-')
        # Clean up multiple hyphens
        name = re.sub(r'-+', '-', name)
        # Remove leading/trailing hyphens
        name = name.strip('-')
        return name.lower()
    
    def to_snake_case(self, name: str) -> str:
        """Convert to snake_case"""
        # Handle camelCase and PascalCase
        name = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name)
        # Handle acronyms
        name = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', '_', name)
        # Convert hyphens to underscores
        name = name.replace('-', '_')
        # Clean up multiple underscores
        name = re.sub(r'_+', '_', name)
        # Remove leading/trailing underscores
        name = name.strip('_')
        return name.lower()
    
    def to_camel_case(self, name: str) -> str:
        """Convert to camelCase"""
        # Split on various separators
        parts = re.split(r'[-_\s]+', name.lower())
        if not parts:
            return name
        # First part lowercase, rest title case
        result = parts[0].lower()
        for part in parts[1:]:
            if part:
                result += part.capitalize()
        return result
    
    def to_pascal_case(self, name: str) -> str:
        """Convert to PascalCase"""
        # Split on various separators
        parts = re.split(r'[-_\s]+', name.lower())
        # All parts title case
        return ''.join(part.capitalize() for part in parts if part)
    
    def to_upper_snake_case(self, name: str) -> str:
        """Convert to UPPER_SNAKE_CASE"""
        return self.to_snake_case(name).upper()
    
    def scan_directory(self, root_path: Path) -> List[NamingViolation]:
        """Scan directory for naming violations"""
        violations = []
        
        def walk_path(path: Path):
            # Check built-in exceptions first
            if self.parser.is_exception(path):
                return
            
            # Check exclude logic first (exclude takes precedence)
            if self.exclude_manager.is_excluded(path):
                return
            
            # For include logic: if include patterns are configured, check if this path should be included
            # The key fix: we need to check if the path OR any of its parents are included
            if self.include_manager.include_patterns:
                path_included = False
                
                # Check if the path itself is included
                if self.include_manager.is_included(path):
                    path_included = True
                else:
                    # Check if any parent directory is included (for recursive scanning)
                    current_path = path
                    while current_path != current_path.parent:
                        current_path = current_path.parent
                        if self.include_manager.is_included(current_path):
                            path_included = True
                            break
                
                if not path_included:
                    return
            
            try:
                for item in path.iterdir():
                    # Check exclude logic for each item first
                    if self.exclude_manager.is_excluded(item):
                        continue
                    
                    # For include logic: if include patterns are configured, check inclusion
                    if self.include_manager.include_patterns:
                        item_included = False
                        
                        # Check if the item itself is included
                        if self.include_manager.is_included(item):
                            item_included = True
                        else:
                            # Check if any parent directory is included (for recursive scanning)
                            current_path = item
                            while current_path != current_path.parent:
                                current_path = current_path.parent
                                if self.include_manager.is_included(current_path):
                                    item_included = True
                                    break
                        
                        if not item_included:
                            continue
                        
                    if item.is_dir():
                        if not self.parser.is_exception(item):
                            violation = self.validate_directory_name(item)
                            if violation:
                                violations.append(violation)
                            walk_path(item)
                    elif item.is_file():
                        violation = self.validate_file_name(item)
                        if violation:
                            violations.append(violation)
                        
                        # Validate frontmatter if markdown
                        if item.suffix.lower() == '.md':
                            fm_violations = self.validate_frontmatter_fields(item)
                            violations.extend(fm_violations)
            except PermissionError:
                pass
        
        walk_path(root_path)
        self.violations = violations
        return violations
    
    def validate_file_name(self, file_path: Path) -> Optional[NamingViolation]:
        """Validate a file name against naming conventions"""
        if self.parser.is_exception(file_path):
            return None
        
        # Extract base name and extensions
        full_name = file_path.name
        base_name = full_name
        extensions = ""
        
        # Handle compound extensions
        while '.' in base_name and not base_name.startswith('.'):
            name_part, ext_part = base_name.rsplit('.', 1)
            extensions = '.' + ext_part + extensions
            base_name = name_part
        
        # Check if this is a standard ID format (special case)
        if self.compiled_patterns.get('standard_ids', re.compile(r'$')).match(base_name):
            return None
        
        # Check extension case
        if extensions and extensions != extensions.lower():
            return NamingViolation(
                path=str(file_path),
                current_name=full_name,
                suggested_name=base_name + extensions.lower(),
                violation_type="extension_case",
                severity="error",
                reason=f"Extensions should be lowercase: {extensions} -> {extensions.lower()}",
                context="file_extension"
            )
        
        # Validate base name
        context = self.get_context_for_path(file_path)
        is_valid, suggestion = self.validate_name(base_name, context)
        
        if not is_valid and suggestion:
            suggested_name = suggestion + extensions
            if suggested_name != full_name:
                return NamingViolation(
                    path=str(file_path),
                    current_name=full_name,
                    suggested_name=suggested_name,
                    violation_type="filename_case",
                    severity="error",
                    reason=f"Filename should follow {context} convention: {base_name} -> {suggestion}",
                    context=context
                )
        
        return None
    
    def validate_directory_name(self, dir_path: Path) -> Optional[NamingViolation]:
        """Validate a directory name"""
        if self.parser.is_exception(dir_path):
            return None
        
        dir_name = dir_path.name
        context = self.get_context_for_path(dir_path)
        is_valid, suggestion = self.validate_name(dir_name, context)
        
        if not is_valid and suggestion:
            return NamingViolation(
                path=str(dir_path),
                current_name=dir_name,
                suggested_name=suggestion,
                violation_type="directory_case",
                severity="error",
                reason=f"Directory should follow {context} convention: {dir_name} -> {suggestion}",
                context=context
            )
        
        return None
    
    def validate_frontmatter_fields(self, file_path: Path) -> List[NamingViolation]:
        """Validate frontmatter field names"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for frontmatter
            if not content.startswith('---'):
                return violations
            
            # Extract frontmatter
            first_line_end = content.find('\n')
            if first_line_end == -1:
                return violations
            
            frontmatter_start = first_line_end + 1
            fm_end_match = re.search(r'^---\s*$', content[frontmatter_start:], re.MULTILINE)
            if not fm_end_match:
                return violations
            
            frontmatter_content = content[frontmatter_start:frontmatter_start + fm_end_match.start()]
            
            # Parse YAML to get only top-level keys, avoiding nested values
            try:
                import yaml
                fm_data = yaml.safe_load(frontmatter_content)
                if not isinstance(fm_data, dict):
                    return violations
                
                # Only validate top-level frontmatter fields, not nested values
                for field in fm_data.keys():
                    if not isinstance(field, str):
                        continue
                        
                    # Check if it's a protected frontmatter field
                    if self.parser.is_protected_name(field, 'frontmatter_fields'):
                        continue
                    
                    is_valid, suggestion = self.validate_name(field, 'frontmatter_fields')
                    if not is_valid and suggestion:
                        violations.append(NamingViolation(
                            path=str(file_path),
                            current_name=f"frontmatter field: {field}",
                            suggested_name=suggestion,
                            violation_type="frontmatter_field",
                            severity="warning",
                            reason=f"Frontmatter field should use snake_case: {field} -> {suggestion}",
                            context="frontmatter_fields"
                        ))
            
            except yaml.YAMLError:
                # Fall back to regex if YAML parsing fails, but be more conservative
                # Only match fields that start at the beginning of a line (top-level)
                field_pattern = re.compile(r'^([a-zA-Z][a-zA-Z0-9_-]*)\s*:', re.MULTILINE)
                fields = field_pattern.findall(frontmatter_content)
                
                for field in fields:
                    # Check if it's a protected frontmatter field
                    if self.parser.is_protected_name(field, 'frontmatter_fields'):
                        continue
                    
                    is_valid, suggestion = self.validate_name(field, 'frontmatter_fields')
                    if not is_valid and suggestion:
                        violations.append(NamingViolation(
                            path=str(file_path),
                            current_name=f"frontmatter field: {field}",
                            suggested_name=suggestion,
                            violation_type="frontmatter_field",
                            severity="warning",
                            reason=f"Frontmatter field should use snake_case: {field} -> {suggestion}",
                            context="frontmatter_fields"
                        ))
        
        except Exception:
            pass
        
        return violations
    
    def print_report(self, show_all: bool = False):
        """Print a detailed report of violations"""
        if not self.violations:
            print("No naming violations found!")
            # Show inclusion/exclusion summary even when no violations
            if self.include_manager.include_patterns or self.exclude_manager.exclude_patterns:
                if self.include_manager.include_patterns:
                    print(f"\n{self.include_manager.get_inclusion_summary()}")
                if self.exclude_manager.exclude_patterns:
                    print(f"\n{self.exclude_manager.get_exclusion_summary()}")
            return
        
        print(f"\nNAMING VIOLATIONS REPORT")
        print(f"{'='*60}")
        print(f"Source of Truth: {self.parser.standard_path}")
        print(f"Total violations: {len(self.violations)}")
        
        # Show inclusion/exclusion summary if any patterns are configured
        if self.include_manager.include_patterns or self.exclude_manager.exclude_patterns:
            if self.include_manager.include_patterns:
                print(f"\n{self.include_manager.get_inclusion_summary()}")
            if self.exclude_manager.exclude_patterns:
                print(f"\n{self.exclude_manager.get_exclusion_summary()}")
        
        # Group by violation type
        by_type = defaultdict(list)
        for violation in self.violations:
            by_type[violation.violation_type].append(violation)
        
        for violation_type, violations in by_type.items():
            print(f"\n{violation_type.upper()} ({len(violations)} violations):")
            print("-" * 40)
            
            for violation in violations[:10 if not show_all else None]:
                print(f"  ERROR: {violation.current_name}")
                print(f"      -> {violation.suggested_name}")
                print(f"      Path: {violation.path}")
                print(f"      Reason: {violation.reason}")
                print()
            
            if not show_all and len(violations) > 10:
                print(f"      ... and {len(violations) - 10} more")
        
        print(f"\nUse --fix to apply automatic corrections")
        print(f"Use --show-all to see all violations")

    def find_content_references(self, old_path: Path, new_path: Path) -> List[ContentUpdate]:
        """Find all content references to files being renamed"""
        updates = []
        
        # Get the relative paths for both old and new files
        old_name = old_path.name
        new_name = new_path.name
        old_stem = old_path.stem
        new_stem = new_path.stem
        
        # Scan all text files in the repository for references
        root_path = Path(".")
        
        for file_path in root_path.rglob("*"):
            if not file_path.is_file():
                continue
                
            # Skip excluded files and directories, respect include/exclude logic
            if (self.parser.is_exception(file_path) or 
                self.exclude_manager.is_excluded(file_path) or 
                not self.include_manager.is_included(file_path)):
                continue
                
            # Only scan text files
            if file_path.suffix.lower() not in ['.md', '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.txt', '.html', '.css']:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for line_num, line in enumerate(lines, 1):
                    original_line = line
                    
                    # Find and replace various types of references
                    new_line = line
                    
                    # Markdown links: [text](filename.md)
                    new_line = re.sub(
                        rf'\[([^\]]*)\]\({re.escape(old_name)}\)',
                        rf'[\1]({new_name})',
                        new_line
                    )
                    
                    # Markdown links: [text](./filename.md)  
                    new_line = re.sub(
                        rf'\[([^\]]*)\]\(\.\/{re.escape(old_name)}\)',
                        rf'[\1](./{new_name})',
                        new_line
                    )
                    
                    # Wiki-style links: [[filename]]
                    new_line = re.sub(
                        rf'\[\[{re.escape(old_stem)}\]\]',
                        rf'[[{new_stem}]]',
                        new_line
                    )
                    
                    # Wiki-style links: [[filename.md]]
                    new_line = re.sub(
                        rf'\[\[{re.escape(old_name)}\]\]',
                        rf'[[{new_name}]]',
                        new_line
                    )
                    
                    # Python imports: import filename
                    if file_path.suffix == '.py':
                        old_module = old_stem.replace('-', '_')
                        new_module = new_stem.replace('-', '_')
                        new_line = re.sub(
                            rf'\bimport\s+{re.escape(old_module)}\b',
                            f'import {new_module}',
                            new_line
                        )
                        # from filename import
                        new_line = re.sub(
                            rf'\bfrom\s+{re.escape(old_module)}\s+import\b',
                            f'from {new_module} import',
                            new_line
                        )
                    
                    # File path references: "filename.md", 'filename.md'
                    new_line = re.sub(
                        rf'(["\']){re.escape(old_name)}\1',
                        rf'\1{new_name}\1',
                        new_line
                    )
                    
                    # Relative path references: ./filename.md, ../path/filename.md
                    new_line = re.sub(
                        rf'(\.\.?/[^/\s]*?){re.escape(old_name)}',
                        rf'\1{new_name}',
                        new_line
                    )
                    
                    # Add more patterns as needed...
                    
                    if new_line != original_line:
                        updates.append(ContentUpdate(
                            file_path=str(file_path),
                            line_number=line_num,
                            old_text=original_line.rstrip(),
                            new_text=new_line.rstrip(),
                            context=f"Reference in {file_path.name}",
                            update_type="file_reference"
                        ))
                        
            except Exception as e:
                # Skip files that can't be read
                continue
        
        return updates
    
    def build_rename_operations(self):
        """Build rename operations with content references"""
        self.rename_operations = []
        
        for violation in self.violations:
            if violation.violation_type in ['filename_case', 'extension_case', 'directory_case']:
                old_path = Path(violation.path)
                new_path = old_path.parent / violation.suggested_name
                
                # Find all content references
                content_updates = self.find_content_references(old_path, new_path)
                
                operation = RenameOperation(
                    old_path=old_path,
                    new_path=new_path,
                    violation_type=violation.violation_type,
                    content_updates=content_updates
                )
                
                self.rename_operations.append(operation)
    
    def apply_content_updates(self, safety_logger: SafetyLogger, dry_run: bool = True) -> int:
        """Apply all content updates BEFORE renaming files"""
        total_updates = sum(len(op.content_updates) for op in self.rename_operations)
        
        if dry_run:
            safety_logger.logger.info(f"DRY RUN - Would update {total_updates} content references")
            
            for op in self.rename_operations:
                if op.content_updates:
                    safety_logger.logger.info(f"RENAME: {op.old_path} -> {op.new_path.name}:")
                    for update in op.content_updates[:3]:  # Show first 3
                        safety_logger.logger.info(f"  FILE: {Path(update.file_path).name}:{update.line_number}")
                        safety_logger.logger.info(f"    - {update.old_text[:80]}...")
                        safety_logger.logger.info(f"    + {update.new_text[:80]}...")
                    if len(op.content_updates) > 3:
                        safety_logger.logger.info(f"    ... and {len(op.content_updates) - 3} more updates")
            
            return total_updates
        
        # Apply updates for real
        updated_files = set()
        
        # Group updates by file for atomic processing
        updates_by_file = defaultdict(list)
        for op in self.rename_operations:
            for update in op.content_updates:
                updates_by_file[update.file_path].append(update)
        
        # Apply updates file by file
        for file_path, updates in updates_by_file.items():
            log_entry = safety_logger.log_operation("content_update", file_path)
            
            try:
                # Read current content
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                log_entry.old_content = ''.join(lines)
                
                # Apply updates (sort by line number descending to avoid offset issues)
                updates.sort(key=lambda u: u.line_number, reverse=True)
                
                for update in updates:
                    if update.line_number <= len(lines):
                        lines[update.line_number - 1] = update.new_text + '\n'
                
                # Write updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                log_entry.new_content = ''.join(lines)
                safety_logger.mark_success(log_entry)
                updated_files.add(file_path)
                
            except Exception as e:
                safety_logger.mark_failed(log_entry, str(e))
        
        safety_logger.logger.info(f"SUCCESS: Updated {len(updated_files)} files with {total_updates} content references")
        return len(updated_files)
    
    def apply_frontmatter_fixes(self, safety_logger: SafetyLogger, dry_run: bool = True) -> int:
        """Apply frontmatter field name fixes"""
        frontmatter_violations = [v for v in self.violations if v.violation_type == 'frontmatter_field']
        
        if not frontmatter_violations:
            return 0
        
        # Group violations by file
        violations_by_file = defaultdict(list)
        for violation in frontmatter_violations:
            violations_by_file[violation.path].append(violation)
        
        if dry_run:
            safety_logger.logger.info(f"DRY RUN - Would fix {len(frontmatter_violations)} frontmatter fields in {len(violations_by_file)} files")
            
            for file_path, violations in violations_by_file.items():
                safety_logger.logger.info(f"FRONTMATTER {file_path}:")
                for violation in violations:
                    # Extract field name from "frontmatter field: field_name" format
                    field_name = violation.current_name.replace("frontmatter field: ", "")
                    safety_logger.logger.info(f"  {field_name} -> {violation.suggested_name}")
            
            return len(violations_by_file)
        
        # Apply frontmatter fixes for real
        fixed_files = 0
        
        for file_path, violations in violations_by_file.items():
            log_entry = safety_logger.log_operation("frontmatter_fix", file_path)
            
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                log_entry.old_content = content
                
                # Parse frontmatter
                if not content.startswith('---'):
                    continue
                
                # Split frontmatter and body
                lines = content.split('\n')
                fm_start = 1
                fm_end = -1
                
                for i, line in enumerate(lines[1:], 1):
                    if line.strip() == '---':
                        fm_end = i
                        break
                
                if fm_end == -1:
                    continue
                
                frontmatter_lines = lines[fm_start:fm_end]
                body_lines = lines[fm_end + 1:]
                
                # Apply field name fixes
                for violation in violations:
                    field_name = violation.current_name.replace("frontmatter field: ", "")
                    new_field_name = violation.suggested_name
                    
                    # Replace field name in frontmatter lines
                    for i, line in enumerate(frontmatter_lines):
                        if line.strip().startswith(f"{field_name}:"):
                            # Preserve indentation and spacing
                            indent = len(line) - len(line.lstrip())
                            value_part = line[line.find(':'):]
                            frontmatter_lines[i] = ' ' * indent + new_field_name + value_part
                            break
                
                # Reconstruct content
                new_content = '---\n' + '\n'.join(frontmatter_lines) + '\n---\n' + '\n'.join(body_lines)
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                log_entry.new_content = new_content
                safety_logger.mark_success(log_entry)
                fixed_files += 1
                
            except Exception as e:
                safety_logger.mark_failed(log_entry, str(e))
        
        safety_logger.logger.info(f"Fixed frontmatter fields in {fixed_files} files")
        return fixed_files

    def apply_file_renames(self, safety_logger: SafetyLogger, dry_run: bool = True) -> int:
        """Apply file and directory renames AFTER content updates"""
        rename_operations = [op for op in self.rename_operations 
                           if str(op.old_path) != str(op.new_path)]
        
        if dry_run:
            safety_logger.logger.info(f"DRY RUN - Would rename {len(rename_operations)} files/directories")
            
            for op in rename_operations:
                safety_logger.logger.info(f"RENAME: {op.old_path} -> {op.new_path}")
            
            return len(rename_operations)
        
        # Apply renames for real
        renamed_count = 0
        
        # Sort operations: files first, then directories (deepest first)  
        file_ops = [op for op in rename_operations 
                   if op.violation_type in ['filename_case', 'extension_case']]
        dir_ops = [op for op in rename_operations 
                  if op.violation_type == 'directory_case']
        dir_ops.sort(key=lambda op: len(op.old_path.parts), reverse=True)  # Deepest first
        
        for op in file_ops + dir_ops:
            log_entry = safety_logger.log_operation("rename", str(op.old_path), str(op.new_path))
            
            try:
                if op.old_path.exists():
                    if not op.new_path.exists() or self._is_case_only_rename(op.old_path, op.new_path):
                        self._safe_rename(op.old_path, op.new_path)
                        safety_logger.mark_success(log_entry)
                        renamed_count += 1
                    else:
                        safety_logger.mark_failed(log_entry, "Target file already exists")
                else:
                    safety_logger.mark_failed(log_entry, "Source file does not exist")
                    
            except Exception as e:
                safety_logger.mark_failed(log_entry, str(e))
        
        safety_logger.logger.info(f"SUCCESS: Renamed {renamed_count} files/directories")
        return renamed_count

    def _is_case_only_rename(self, old_path: Path, new_path: Path) -> bool:
        """Check if this is a case-only rename (same path, different case)"""
        return str(old_path).lower() == str(new_path).lower()
    
    def _safe_rename(self, old_path: Path, new_path: Path):
        """Safely rename files, handling case-only renames on Windows"""
        if self._is_case_only_rename(old_path, new_path):
            # Case-only rename - use temporary file approach for Windows compatibility
            temp_path = old_path.parent / f"temp_{uuid4().hex}_{new_path.name}"
            old_path.rename(temp_path)  # Step 1: rename to temp
            temp_path.rename(new_path)  # Step 2: rename to final
        else:
            # Different names - direct rename is safe
            old_path.rename(new_path)

def main():
    parser = argparse.ArgumentParser(
        description="""Naming Convention Enforcer v2.0 - Single Source of Truth

Automatic Files:
  .namingignore    - Automatically loaded exclusion patterns (like .gitignore)
  .naminginclude   - Automatically loaded inclusion patterns""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
╭─────────────────────────────────────────────────────────────────────────────╮
│                                 EXAMPLES                                    │
╰─────────────────────────────────────────────────────────────────────────────╯

Basic Operations:
  python naming_enforcer.py --scan .                       # Scan current directory
  python naming_enforcer.py --scan /path --show-all        # Show all violations
  python naming_enforcer.py --scan /path --fix             # Apply fixes
  python naming_enforcer.py --validate-standard            # Validate standard

INCLUSION Examples:
  python naming_enforcer.py --scan . --include-file important.py
  python naming_enforcer.py --scan . --include-dir src/ --include-dir docs/
  python naming_enforcer.py --scan . --include-glob "*.py" --include-glob "*.md"
  python naming_enforcer.py --scan . --include-regex ".*\\.py$"
  python naming_enforcer.py --scan . --include-list includes.txt

EXCLUSION Examples:
  python naming_enforcer.py --scan . --exclude-file temp.txt
  python naming_enforcer.py --scan . --exclude-dir build/ --exclude-dir dist/
  python naming_enforcer.py --scan . --exclude-glob "*.tmp" --exclude-glob "test_*"
  python naming_enforcer.py --scan . --exclude-regex ".*\\.backup$"
  python naming_enforcer.py --scan . --exclude-list excludes.txt

Advanced Usage:
  python naming_enforcer.py --scan . --dry-run --exclude-dir build/
  python naming_enforcer.py --show-exclusions --exclude-list my-excludes.txt
  python naming_enforcer.py --scan . --fix --exclude-glob "*.tmp" --exclude-dir __pycache__/
  python naming_enforcer.py --scan . --include-glob "*.py" --exclude-glob "*_test.py"
  python naming_enforcer.py --show-inclusions --include-dir src/

Tips: 
  • Use --show-inclusions/--show-exclusions to verify patterns before scanning
  • Exclude takes precedence over include (excluded files are never processed)
  • Include patterns limit processing to only matching files/directories
  • Create .namingignore/.naminginclude files for automatic pattern loading
  • Automatic files are loaded from current directory or scan directory
        """
    )
    
    parser.add_argument("--scan", type=str, default=".", 
                       help="Directory to scan for violations (default: current directory)")
    parser.add_argument("--fix", action="store_true", 
                       help="Apply automatic fixes (CAUTION: creates backups)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be fixed without making changes")
    parser.add_argument("--show-all", action="store_true", 
                       help="Show all violations (not just first 10)")
    parser.add_argument("--standard-path", type=str, 
                       default=None,
                       help="Path to the naming standard document (default: auto-detect from repo root)")
    parser.add_argument("--validate-standard", action="store_true", 
                       help="Validate that the standard document itself is correct")
    parser.add_argument("--generate-config", type=str, 
                       help="Generate JSON config file from standard (specify output path)")
    
    # Include functionality
    parser.add_argument("--include-file", action="append", metavar="FILE",
                       help="Include only a specific file (can be used multiple times)")
    parser.add_argument("--include-dir", action="append", metavar="DIR", 
                       help="Include only a specific directory (can be used multiple times)")
    parser.add_argument("--include-glob", action="append", metavar="PATTERN",
                       help="Include only files/dirs matching glob pattern (can be used multiple times)")
    parser.add_argument("--include-regex", action="append", metavar="PATTERN",
                       help="Include only files/dirs matching regex pattern (can be used multiple times)")
    parser.add_argument("--include-list", type=str, metavar="FILE",
                       help="Load inclusions from file (one pattern per line)")
    parser.add_argument("--show-inclusions", action="store_true",
                       help="Show summary of configured inclusions")
    
    # Exclude functionality
    parser.add_argument("--exclude-file", action="append", metavar="FILE",
                       help="Exclude a specific file (can be used multiple times)")
    parser.add_argument("--exclude-dir", action="append", metavar="DIR", 
                       help="Exclude a specific directory (can be used multiple times)")
    parser.add_argument("--exclude-glob", action="append", metavar="PATTERN",
                       help="Exclude files/dirs matching glob pattern (can be used multiple times)")
    parser.add_argument("--exclude-regex", action="append", metavar="PATTERN",
                       help="Exclude files/dirs matching regex pattern (can be used multiple times)")
    parser.add_argument("--exclude-list", type=str, metavar="FILE",
                       help="Load exclusions from file (one pattern per line)")
    parser.add_argument("--show-exclusions", action="store_true",
                       help="Show summary of configured exclusions")
    
    args = parser.parse_args()
    
    try:
        # Initialize enforcer
        enforcer = NamingEnforcerV2(args.standard_path)
        
        # Reload automatic files from scan directory if specified
        if args.scan:
            enforcer.reload_automatic_files(Path(args.scan))
        
        # Configure inclusions
        if args.include_file:
            for file_path in args.include_file:
                try:
                    enforcer.include_manager.add_include_file(file_path, f"CLI include-file: {file_path}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not include file '{file_path}': {e}")
        
        if args.include_dir:
            for dir_path in args.include_dir:
                try:
                    enforcer.include_manager.add_include_directory(dir_path, f"CLI include-dir: {dir_path}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not include directory '{dir_path}': {e}")
        
        if args.include_glob:
            for glob_pattern in args.include_glob:
                try:
                    enforcer.include_manager.add_include_glob(glob_pattern, f"CLI include-glob: {glob_pattern}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not add include glob pattern '{glob_pattern}': {e}")
        
        if args.include_regex:
            for regex_pattern in args.include_regex:
                try:
                    enforcer.include_manager.add_include_regex(regex_pattern, f"CLI include-regex: {regex_pattern}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not add include regex pattern '{regex_pattern}': {e}")
        
        if args.include_list:
            try:
                enforcer.include_manager.load_include_file(args.include_list)
            except Exception as e:
                print(f"ERROR: Error loading include list '{args.include_list}': {e}")
                sys.exit(1)
        
        # Configure exclusions
        if args.exclude_file:
            for file_path in args.exclude_file:
                try:
                    enforcer.exclude_manager.add_exclude_file(file_path, f"CLI exclude-file: {file_path}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not exclude file '{file_path}': {e}")
        
        if args.exclude_dir:
            for dir_path in args.exclude_dir:
                try:
                    enforcer.exclude_manager.add_exclude_directory(dir_path, f"CLI exclude-dir: {dir_path}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not exclude directory '{dir_path}': {e}")
        
        if args.exclude_glob:
            for glob_pattern in args.exclude_glob:
                try:
                    enforcer.exclude_manager.add_exclude_glob(glob_pattern, f"CLI exclude-glob: {glob_pattern}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not add glob pattern '{glob_pattern}': {e}")
        
        if args.exclude_regex:
            for regex_pattern in args.exclude_regex:
                try:
                    enforcer.exclude_manager.add_exclude_regex(regex_pattern, f"CLI exclude-regex: {regex_pattern}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not add regex pattern '{regex_pattern}': {e}")
        
        if args.exclude_list:
            try:
                enforcer.exclude_manager.load_exclude_file(args.exclude_list)
            except Exception as e:
                print(f"ERROR: Error loading exclude list '{args.exclude_list}': {e}")
                sys.exit(1)
        
        # Show inclusions if requested
        if args.show_inclusions:
            print(enforcer.include_manager.get_inclusion_summary())
            return
        
        # Show exclusions if requested
        if args.show_exclusions:
            print(enforcer.exclude_manager.get_exclusion_summary())
            return
        
        if args.validate_standard:
            print(f"SUCCESS: Successfully parsed naming standard: {args.standard_path}")
            print(f"INFO: Extracted {len(enforcer.parser.patterns)} naming patterns")
            print(f"INFO: Found {sum(len(names) for names in enforcer.parser.protected_names.values())} protected names")
            print(f"INFO: Configured {sum(len(exc) for exc in enforcer.parser.exceptions.values())} exception patterns")
            return
        
        if args.generate_config:
            # Generate configuration file from the standard
            config = {
                "patterns": enforcer.parser.patterns,
                "protected_names": {k: list(v) for k, v in enforcer.parser.protected_names.items()},
                "exceptions": enforcer.parser.exceptions,
                "source": str(enforcer.parser.standard_path),
                "generated_at": "Auto-generated from GM-CONVENTIONS-NAMING.md"
            }
            
            with open(args.generate_config, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            print(f"SUCCESS: Generated configuration: {args.generate_config}")
            return
        
        # Scan for violations
        scan_path = Path(args.scan).resolve()
        if not scan_path.exists():
            print(f"ERROR: Path does not exist: {scan_path}")
            sys.exit(1)
        
        print(f"Scanning: {scan_path}")
        print(f"Using standard: {args.standard_path}")
        
        violations = enforcer.scan_directory(scan_path)
        
        if args.fix or args.dry_run:
            # Initialize safety logging
            operation_name = "fix_violations" if args.fix else "dry_run_preview"
            safety_logger = SafetyLogger(operation_name)
            
            try:
                # Build rename operations with link detection
                safety_logger.logger.info("Building rename operations and scanning for link references...")
                enforcer.build_rename_operations()
                
                # Get all files that will be modified for backup
                files_to_backup = []
                
                # Add files with frontmatter violations
                frontmatter_violations = [v for v in violations if v.violation_type == 'frontmatter_field']
                for violation in frontmatter_violations:
                    files_to_backup.append(Path(violation.path))
                    
                # Add files from rename operations (ONLY FILES, NOT DIRECTORIES)
                for op in enforcer.rename_operations:
                    # Only backup files, not directories (directories don't need content backup)
                    if op.old_path.is_file():
                        files_to_backup.append(op.old_path)
                    # Add files with content updates to backup
                    for update in op.content_updates:
                        files_to_backup.append(Path(update.file_path))
                
                files_to_backup = list(set(files_to_backup))  # Remove duplicates
                
                if args.fix and files_to_backup:
                    # Create backup before any modifications
                    safety_logger.logger.info(f"📦 Creating backup of {len(files_to_backup)} files...")
                    if not safety_logger.create_backup(files_to_backup, f"Naming enforcer fixes for {len(violations)} violations"):
                        safety_logger.logger.error("ERROR: Backup creation failed - aborting operation")
                        sys.exit(1)
                
                # Apply frontmatter field fixes first
                frontmatter_fixes = enforcer.apply_frontmatter_fixes(safety_logger, dry_run=args.dry_run)
                
                # Apply content updates second (preserves links)
                content_updates = enforcer.apply_content_updates(safety_logger, dry_run=args.dry_run)
                
                # Then apply file renames last
                file_renames = enforcer.apply_file_renames(safety_logger, dry_run=args.dry_run)
                
                # Finalize logging
                safety_logger.finalize_operation()
                
                if args.dry_run:
                    safety_logger.logger.info("DRY RUN COMPLETE - No changes made")
                    safety_logger.logger.info(f"Use --fix to apply {frontmatter_fixes + content_updates + file_renames} changes")
                else:
                    safety_logger.logger.info("NAMING FIXES COMPLETE")
                    safety_logger.logger.info(f"Fixed {frontmatter_fixes} frontmatter fields")
                    safety_logger.logger.info(f"Updated {content_updates} content references")
                    safety_logger.logger.info(f"Renamed {file_renames} files/directories")
                    
            except Exception as e:
                safety_logger.logger.error(f"ERROR: Operation failed: {e}")
                safety_logger.finalize_operation()
                sys.exit(1)
        else:
            enforcer.print_report(args.show_all)
        
        # Exit code for CI
        sys.exit(1 if violations else 0)
        
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 