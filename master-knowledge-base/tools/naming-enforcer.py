#!/usr/bin/env python3
"""
Naming Convention Enforcer for Knowledge Base

Validates and enforces kebab-case naming conventions across the knowledge base
with configurable exceptions and dry-run capability.
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Set, Optional

@dataclass
class NamingViolation:
    path: str
    current_name: str
    suggested_name: str
    violation_type: str
    severity: str  # 'error', 'warning', 'info'
    reason: str

class NamingEnforcer:
    def __init__(self, config_path: str = "master-knowledge-base/tools/naming-exceptions.json"):
        self.config_path = Path(config_path)
        self.violations: List[NamingViolation] = []
        self.exceptions = self.load_exceptions()
        
        # Naming patterns
        self.kebab_pattern = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
        self.snake_pattern = re.compile(r'^[a-z0-9]+(_[a-z0-9]+)*$')
        
        # Standard ID pattern (exception)
        self.standard_id_pattern = re.compile(r'^[A-Z][A-Z0-9]*-[A-Z][A-Z0-9]*-[A-Z0-9-]+$')
        
        # Frontmatter field pattern (should be kebab-case)
        self.frontmatter_field_pattern = re.compile(r'^[a-z]+(-[a-z]+)*$')
        
    def load_exceptions(self) -> Dict:
        """Load naming exceptions configuration"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get('exceptions', {})
        except Exception as e:
            print(f"Warning: Could not load exceptions config: {e}")
            return {}
    
    def is_kebab_case(self, name: str) -> bool:
        """Check if name follows kebab-case convention"""
        return bool(self.kebab_pattern.match(name))
    
    def is_snake_case(self, name: str) -> bool:
        """Check if name follows snake_case convention"""
        return bool(self.snake_pattern.match(name))
    
    def is_standard_id_format(self, name: str) -> bool:
        """Check if name follows standard ID format"""
        return bool(self.standard_id_pattern.match(name))
    
    def get_naming_convention_for_path(self, path: Path) -> str:
        """Determine which naming convention applies to a path"""
        path_str = str(path).replace('\\', '/')
        
        # Check for snake_case directories
        snake_dirs = self.exceptions.get('directory_rules', {}).get('snake_case_directories', [])
        for snake_dir in snake_dirs:
            if snake_dir in path_str or path_str.startswith(snake_dir):
                return 'snake_case'
        
        # Default to kebab-case
        return 'kebab_case'
    
    def to_kebab_case(self, name: str) -> str:
        """Convert name to kebab-case"""
        # Handle different cases
        # CamelCase -> kebab-case
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
        # snake_case -> kebab-case
        name = name.replace('_', '-')
        # Multiple hyphens -> single hyphen
        name = re.sub(r'-+', '-', name)
        # Remove leading/trailing hyphens
        name = name.strip('-')
        # Lowercase
        return name.lower()
    
    def to_snake_case(self, name: str) -> str:
        """Convert name to snake_case"""
        # Handle different cases
        # CamelCase -> snake_case
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
        # kebab-case -> snake_case
        name = name.replace('-', '_')
        # Multiple underscores -> single underscore
        name = re.sub(r'_+', '_', name)
        # Remove leading/trailing underscores
        name = name.strip('_')
        # Lowercase
        return name.lower()
    
    def is_file_excluded(self, file_path: Path) -> bool:
        """Check if file is in exceptions list"""
        file_name = file_path.name
        
        # Check explicit file exceptions
        if file_name in self.exceptions.get('files', []):
            return True
        
        # Check pattern exceptions
        for pattern in self.exceptions.get('file_patterns', []):
            if file_path.match(pattern):
                return True
        
        return False
    
    def is_directory_excluded(self, dir_path: Path) -> bool:
        """Check if directory is in exceptions list"""
        dir_name = dir_path.name
        
        # Check explicit directory exceptions
        if dir_name in self.exceptions.get('directories', []):
            return True
        
        # Check if any parent directory is excluded
        for part in dir_path.parts:
            if part in self.exceptions.get('directories', []):
                return True
        
        return False
    
    def should_exclude_path(self, path: Path) -> bool:
        """Check if path should be excluded from naming checks"""
        # Check directory exclusions
        if self.is_directory_excluded(path.parent):
            return True
        
        # Check file exclusions
        if path.is_file() and self.is_file_excluded(path):
            return True
        
        return False
    
    def validate_file_name(self, file_path: Path) -> Optional[NamingViolation]:
        """Validate a single file name"""
        if self.should_exclude_path(file_path):
            return None
        
        name_without_ext = file_path.stem
        extension = file_path.suffix
        
        # Special handling for standard ID files (always allowed)
        if self.is_standard_id_format(name_without_ext):
            return None
        
        # Check if extension needs to be lowercase
        if extension and extension != extension.lower():
            suggested_name = name_without_ext + extension.lower()
            return NamingViolation(
                path=str(file_path),
                current_name=file_path.name,
                suggested_name=suggested_name,
                violation_type="extension_case",
                severity="error",
                reason=f"File extension should be lowercase: {extension} -> {extension.lower()}"
            )
        
        # Determine naming convention for this path
        convention = self.get_naming_convention_for_path(file_path)
        
        if convention == 'snake_case':
            # Check if filename follows snake_case (for scripts)
            if not self.is_snake_case(name_without_ext):
                suggested_stem = self.to_snake_case(name_without_ext)
                suggested_name = suggested_stem + extension
                
                return NamingViolation(
                    path=str(file_path),
                    current_name=file_path.name,
                    suggested_name=suggested_name,
                    violation_type="filename_case",
                    severity="error",
                    reason=f"Script filename should be snake_case: {name_without_ext} -> {suggested_stem}"
                )
        else:
            # Check if filename follows kebab-case
            if not self.is_kebab_case(name_without_ext):
                suggested_stem = self.to_kebab_case(name_without_ext)
                suggested_name = suggested_stem + extension
                
                return NamingViolation(
                    path=str(file_path),
                    current_name=file_path.name,
                    suggested_name=suggested_name,
                    violation_type="filename_case",
                    severity="error",
                    reason=f"Filename should be kebab-case: {name_without_ext} -> {suggested_stem}"
                )
        
        return None
    
    def validate_directory_name(self, dir_path: Path) -> Optional[NamingViolation]:
        """Validate a single directory name"""
        if self.should_exclude_path(dir_path):
            return None
        
        dir_name = dir_path.name
        
        # Determine naming convention for this directory
        convention = self.get_naming_convention_for_path(dir_path)
        
        if convention == 'snake_case':
            # Directories in script areas should be kebab-case (only files should be snake_case)
            if not self.is_kebab_case(dir_name):
                suggested_name = self.to_kebab_case(dir_name)
                
                return NamingViolation(
                    path=str(dir_path),
                    current_name=dir_name,
                    suggested_name=suggested_name,
                    violation_type="directory_case",
                    severity="error",
                    reason=f"Directory should be kebab-case: {dir_name} -> {suggested_name}"
                )
        else:
            # Standard kebab-case for directories
            if not self.is_kebab_case(dir_name):
                suggested_name = self.to_kebab_case(dir_name)
                
                return NamingViolation(
                    path=str(dir_path),
                    current_name=dir_name,
                    suggested_name=suggested_name,
                    violation_type="directory_case",
                    severity="error",
                    reason=f"Directory should be kebab-case: {dir_name} -> {suggested_name}"
                )
        
        return None
    
    def validate_frontmatter_fields(self, file_path: Path) -> List[NamingViolation]:
        """Validate frontmatter field names in markdown files"""
        violations = []
        
        if not file_path.suffix.lower() == '.md':
            return violations
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for YAML frontmatter
            if not content.startswith('---\n'):
                return violations
            
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                return violations
            
            frontmatter_content = content[4:end_marker]
            
            # Extract field names (simple regex approach)
            field_pattern = re.compile(r'^([a-zA-Z][a-zA-Z0-9_-]*)\s*:', re.MULTILINE)
            fields = field_pattern.findall(frontmatter_content)
            
            for field in fields:
                if not self.frontmatter_field_pattern.match(field):
                    suggested_field = self.to_kebab_case(field)
                    
                    violation = NamingViolation(
                        path=str(file_path),
                        current_name=f"frontmatter field: {field}",
                        suggested_name=suggested_field,
                        violation_type="frontmatter_field",
                        severity="warning",
                        reason=f"Frontmatter field should be kebab-case: {field} -> {suggested_field}"
                    )
                    violations.append(violation)
            
        except Exception as e:
            # Skip files we can't read or parse
            pass
        
        return violations
    
    def scan_directory(self, root_path: Path) -> List[NamingViolation]:
        """Scan directory tree for naming violations"""
        violations = []
        
        def should_skip_directory(dir_path: Path) -> bool:
            """Check if we should completely skip scanning this directory"""
            dir_name = dir_path.name
            # Check if this directory or any parent is excluded
            for part in dir_path.parts:
                if part in self.exceptions.get('directories', []):
                    return True
            return False
        
        # Walk directory tree manually to skip excluded directories
        def walk_path(path: Path):
            if should_skip_directory(path):
                return
                
            try:
                for item in path.iterdir():
                    if item.is_dir():
                        if not should_skip_directory(item):
                            # Validate directory name
                            violation = self.validate_directory_name(item)
                            if violation:
                                violations.append(violation)
                            # Recursively scan subdirectory
                            walk_path(item)
                    elif item.is_file():
                        # Validate filename
                        violation = self.validate_file_name(item)
                        if violation:
                            violations.append(violation)
                        
                        # Validate frontmatter fields
                        frontmatter_violations = self.validate_frontmatter_fields(item)
                        violations.extend(frontmatter_violations)
            except PermissionError:
                # Skip directories we can't read
                pass
        
        walk_path(root_path)
        self.violations = violations
        return violations
    
    def print_violations_report(self, show_all: bool = False):
        """Print detailed violations report"""
        if not self.violations:
            print("✅ No naming violations found!")
            return
        
        # Group by severity
        errors = [v for v in self.violations if v.severity == 'error']
        warnings = [v for v in self.violations if v.severity == 'warning']
        
        print(f"\n🔍 NAMING VIOLATIONS REPORT")
        print(f"{'='*50}")
        print(f"Total violations: {len(self.violations)}")
        print(f"Errors: {len(errors)}")
        print(f"Warnings: {len(warnings)}")
        
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for i, violation in enumerate(errors[:20 if not show_all else None]):
                print(f"  {i+1}. {violation.current_name}")
                print(f"     Path: {violation.path}")
                print(f"     Suggested: {violation.suggested_name}")
                print(f"     Reason: {violation.reason}")
                print()
            
            if len(errors) > 20 and not show_all:
                print(f"     ... and {len(errors) - 20} more errors (use --show-all to see all)")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for i, violation in enumerate(warnings[:10 if not show_all else None]):
                print(f"  {i+1}. {violation.current_name}")
                print(f"     Path: {violation.path}")
                print(f"     Suggested: {violation.suggested_name}")
                print(f"     Reason: {violation.reason}")
                print()
            
            if len(warnings) > 10 and not show_all:
                print(f"     ... and {len(warnings) - 10} more warnings")
    
    def generate_fix_commands(self, output_file: Optional[str] = None):
        """Generate shell commands to fix violations"""
        commands = []
        
        for violation in self.violations:
            if violation.violation_type in ['filename_case', 'extension_case']:
                old_path = violation.path
                new_path = str(Path(violation.path).parent / violation.suggested_name)
                commands.append(f'mv "{old_path}" "{new_path}"')
            elif violation.violation_type == 'directory_case':
                old_path = violation.path
                new_path = str(Path(violation.path).parent / violation.suggested_name)
                commands.append(f'mv "{old_path}" "{new_path}"')
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write("# Auto-generated naming fix commands\n")
                f.write("# Review carefully before executing!\n\n")
                for cmd in commands:
                    f.write(cmd + "\n")
            print(f"Fix commands written to: {output_file}")
        else:
            print(f"\n🔧 FIX COMMANDS:")
            for cmd in commands[:10]:
                print(f"  {cmd}")
            if len(commands) > 10:
                print(f"  ... and {len(commands) - 10} more commands")
    
    def apply_fixes(self, dry_run: bool = True) -> int:
        """Apply naming fixes (with dry-run option)"""
        if dry_run:
            print(f"\n🔍 DRY RUN - Would fix {len(self.violations)} violations:")
            for violation in self.violations:
                old_path = Path(violation.path)
                new_path = old_path.parent / violation.suggested_name
                print(f"  {old_path} -> {new_path}")
            return len(self.violations)
        
        # Actually apply fixes (dangerous!)
        fixed_count = 0
        for violation in self.violations:
            try:
                old_path = Path(violation.path)
                new_path = old_path.parent / violation.suggested_name
                
                if old_path.exists() and not new_path.exists():
                    old_path.rename(new_path)
                    fixed_count += 1
                    print(f"✅ Fixed: {old_path.name} -> {new_path.name}")
                else:
                    print(f"⚠️  Skipped: {old_path} (target exists or source missing)")
                    
            except Exception as e:
                print(f"❌ Error fixing {violation.path}: {e}")
        
        return fixed_count

def main():
    parser = argparse.ArgumentParser(description="Enforce naming conventions across knowledge base")
    parser.add_argument("--directory", "-d", default=".", help="Directory to scan")
    parser.add_argument("--config", "-c", default="master-knowledge-base/tools/naming-exceptions.json", 
                       help="Path to exceptions config file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without applying")
    parser.add_argument("--apply-fixes", action="store_true", help="Actually apply naming fixes")
    parser.add_argument("--show-all", action="store_true", help="Show all violations (not just first 20)")
    parser.add_argument("--output-commands", "-o", help="Output fix commands to file")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    enforcer = NamingEnforcer(args.config)
    
    print(f"🔍 Scanning {args.directory} for naming violations...")
    violations = enforcer.scan_directory(Path(args.directory))
    
    if args.format == "json":
        # JSON output
        violation_data = [
            {
                "path": v.path,
                "current_name": v.current_name,
                "suggested_name": v.suggested_name,
                "violation_type": v.violation_type,
                "severity": v.severity,
                "reason": v.reason
            }
            for v in violations
        ]
        print(json.dumps(violation_data, indent=2))
    else:
        # Text output
        enforcer.print_violations_report(args.show_all)
        
        if args.output_commands:
            enforcer.generate_fix_commands(args.output_commands)
        
        if args.dry_run or args.apply_fixes:
            fixed_count = enforcer.apply_fixes(dry_run=args.dry_run)
            if args.dry_run:
                print(f"\n🔍 DRY RUN COMPLETE: Would fix {fixed_count} items")
            else:
                print(f"\n✅ FIXES APPLIED: {fixed_count} items renamed")

if __name__ == "__main__":
    main() 