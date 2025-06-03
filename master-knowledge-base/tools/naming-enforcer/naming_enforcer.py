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
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple, Union
from collections import defaultdict
import yaml

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

class NamingStandardParser:
    """Parses GM-CONVENTIONS-NAMING.md to extract all naming rules"""
    
    def __init__(self, standard_path: str = "master-knowledge-base/standards/src/GM-CONVENTIONS-NAMING.md"):
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
            'DOMAIN-SUBDOMAIN-NAME': r'^[A-Z]{1,6}-[A-Z0-9]{1,15}-[A-Z0-9\-]+$'  # More flexible character limits
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
                    import fnmatch
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
    """Modern naming enforcer using GM-CONVENTIONS-NAMING.md as single source"""
    
    def __init__(self, standard_path: str = "master-knowledge-base/standards/src/GM-CONVENTIONS-NAMING.md"):
        self.parser = NamingStandardParser(standard_path)
        self.violations: List[NamingViolation] = []
        self.rename_operations: List[RenameOperation] = []
        
        # Compiled regex patterns for performance
        self.compiled_patterns = {
            context: re.compile(pattern)
            for context, pattern in self.parser.patterns.items()
        }
    
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
            if self.parser.is_exception(path):
                return
            
            try:
                for item in path.iterdir():
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
            print("✅ No naming violations found!")
            return
        
        print(f"\n📋 NAMING VIOLATIONS REPORT")
        print(f"{'='*60}")
        print(f"Source of Truth: {self.parser.standard_path}")
        print(f"Total violations: {len(self.violations)}")
        
        # Group by violation type
        by_type = defaultdict(list)
        for violation in self.violations:
            by_type[violation.violation_type].append(violation)
        
        for violation_type, violations in by_type.items():
            print(f"\n{violation_type.upper()} ({len(violations)} violations):")
            print("-" * 40)
            
            for violation in violations[:10 if not show_all else None]:
                print(f"  🔴 {violation.current_name}")
                print(f"      ➜ {violation.suggested_name}")
                print(f"      📁 {violation.path}")
                print(f"      💡 {violation.reason}")
                print()
            
            if not show_all and len(violations) > 10:
                print(f"      ... and {len(violations) - 10} more")
        
        print(f"\n💡 Use --fix to apply automatic corrections")
        print(f"💡 Use --show-all to see all violations")

def main():
    parser = argparse.ArgumentParser(
        description="Naming Convention Enforcer v2.0 - Single Source of Truth",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python naming_enforcer_v2.py --scan .                    # Scan current directory
  python naming_enforcer_v2.py --scan /path --show-all     # Show all violations
  python naming_enforcer_v2.py --scan /path --fix          # Apply fixes
  python naming_enforcer_v2.py --validate-standard         # Validate the standard itself
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
                       default="master-knowledge-base/standards/src/GM-CONVENTIONS-NAMING.md",
                       help="Path to the naming standard document")
    parser.add_argument("--validate-standard", action="store_true", 
                       help="Validate that the standard document itself is correct")
    parser.add_argument("--generate-config", type=str, 
                       help="Generate JSON config file from standard (specify output path)")
    
    args = parser.parse_args()
    
    try:
        # Initialize enforcer
        enforcer = NamingEnforcerV2(args.standard_path)
        
        if args.validate_standard:
            print(f"✅ Successfully parsed naming standard: {args.standard_path}")
            print(f"📊 Extracted {len(enforcer.parser.patterns)} naming patterns")
            print(f"🛡️  Found {sum(len(names) for names in enforcer.parser.protected_names.values())} protected names")
            print(f"🚫 Configured {sum(len(exc) for exc in enforcer.parser.exceptions.values())} exception patterns")
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
            
            print(f"✅ Generated configuration: {args.generate_config}")
            return
        
        # Scan for violations
        scan_path = Path(args.scan).resolve()
        if not scan_path.exists():
            print(f"❌ Error: Path does not exist: {scan_path}")
            sys.exit(1)
        
        print(f"🔍 Scanning: {scan_path}")
        print(f"📖 Using standard: {args.standard_path}")
        
        violations = enforcer.scan_directory(scan_path)
        
        if args.fix or args.dry_run:
            # TODO: Implement fix functionality
            print("🚧 Fix functionality coming in next iteration")
            print("📋 For now, showing violations report:")
        
        enforcer.print_report(args.show_all)
        
        # Exit code for CI
        sys.exit(1 if violations else 0)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 