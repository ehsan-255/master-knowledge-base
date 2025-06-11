#!/usr/bin/env python3
"""
Path Reference Updater for Master Knowledge Base Migration

This script updates all path references in files during the migration from
master-knowledge-base/ to repository root.

Handles different file types with appropriate replacement patterns.

Author: Automated Migration System
Generated: 2025-01-27
"""

import os
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import logging

class PathReferenceUpdater:
    """Updates path references in files during migration."""
    
    def __init__(self, repo_root: Path, dry_run: bool, logger: logging.Logger):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.logger = logger
        self.modified_files = []
        
        # Define replacement patterns
        self.replacement_patterns = [
            # Direct path references
            (r'standards/', 'standards/'),
            (r'tools/', 'tools/'),
            (r'dist/', 'dist/'),
            (r'/standards/', '/standards/'),
            (r'/tools/', '/tools/'),
            (r'/dist/', '/dist/'),
            
            # Relative path references
            (r'\.\./standards/', '../standards/'),
            (r'\.\./tools/', '../tools/'),
            (r'\.\./dist/', '../dist/'),
            
            # Quoted path references
            (r'"standards/', '"standards/'),
            (r'"tools/', '"tools/'),
            (r'"dist/', '"dist/'),
            
            # Configuration and documentation references
            (r'`standards/', '`standards/'),
            (r'`tools/', '`tools/'),
            (r'`dist/', '`dist/'),
        ]
        
        # Special Python patterns for path calculations
        self.python_patterns = [
            # Path object construction
            (r'Path\("([^"]+)"\)', r'Path("\1")'),
            
            # String path references
            (r'"([^"]+)"', r'"\1"'),
            (r"'([^']+)'", r"'\1'"),
            
            # Parent directory traversal adjustments
            (r'script_dir\.parent\.parent\.parent', 'script_dir.parent.parent'),
        ]
        
        # Files that require special handling
        self.special_files = {
            'tools/naming-enforcer/naming_enforcer.py': self.update_naming_enforcer,
            'tools/linter/kb_linter.py': self.update_kb_linter,
            'tools/naming-enforcer/generate_naming_configs.py': self.update_naming_configs,
            'dist/standards_index.json': self.update_standards_index,
        }
    
    def get_modified_files(self) -> List[str]:
        """Return list of modified files."""
        return self.modified_files
    
    def update_all_references(self) -> bool:
        """Update all path references in the repository."""
        try:
            self.logger.info("Starting path reference updates...")
            
            # Get all files to process
            files_to_process = self.get_files_to_process()
            self.logger.info(f"Found {len(files_to_process)} files to process")
            
            success_count = 0
            error_count = 0
            
            for file_path in files_to_process:
                try:
                    if self.update_file_references(file_path):
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {e}")
                    error_count += 1
                
                # Progress indicator every 50 files
                if (success_count + error_count) % 50 == 0:
                    print(f"Processed {success_count + error_count}/{len(files_to_process)} files")
            
            self.logger.info(f"Path reference update completed: {success_count} success, {error_count} errors")
            return error_count == 0
            
        except Exception as e:
            self.logger.error(f"Path reference update failed: {e}")
            return False
    
    def get_files_to_process(self) -> List[Path]:
        """Get list of files that need path reference updates."""
        files = []
        
        # Exclude directories
        exclude_dirs = {'archive', '.git', '__pycache__', 'node_modules'}
        
        # Include file extensions
        include_extensions = {'.md', '.py', '.json', '.yaml', '.yml', '.txt'}
        
        for root, dirs, filenames in os.walk(self.repo_root):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Check if file extension should be processed
                if file_path.suffix.lower() in include_extensions:
                    files.append(file_path)
        
        return files
    
    def update_file_references(self, file_path: Path) -> bool:
        """Update path references in a single file."""
        try:
            # Check if this file needs special handling
            relative_path = str(file_path.relative_to(self.repo_root))
            if relative_path in self.special_files:
                return self.special_files[relative_path](file_path)
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Skip binary files
                return True
            
            original_content = content
            
            # Apply replacement patterns based on file type
            if file_path.suffix == '.py':
                content = self.update_python_file(content)
            elif file_path.suffix in ['.json']:
                content = self.update_json_file(content, file_path)
            elif file_path.suffix in ['.yaml', '.yml']:
                content = self.update_yaml_file(content, file_path)
            else:
                content = self.update_text_file(content)
            
            # Check if content changed
            if content != original_content:
                if self.dry_run:
                    self.logger.info(f"[DRY RUN] Would update: {file_path}")
                    # Detailed change logging removed for performance
                else:
                    # Write updated content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.logger.info(f"Updated: {file_path}")
                
                self.modified_files.append(str(file_path))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update {file_path}: {e}")
            return False
    
    def update_text_file(self, content: str) -> str:
        """Update path references in text files (markdown, etc.)."""
        for pattern, replacement in self.replacement_patterns:
            content = re.sub(pattern, replacement, content)
        return content
    
    def update_python_file(self, content: str) -> str:
        """Update path references in Python files."""
        # Apply general patterns
        for pattern, replacement in self.replacement_patterns:
            content = re.sub(pattern, replacement, content)
        
        # Apply Python-specific patterns
        for pattern, replacement in self.python_patterns:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def update_json_file(self, content: str, file_path: Path) -> str:
        """Update path references in JSON files."""
        try:
            # Parse JSON
            data = json.loads(content)
            
            # Update paths recursively
            self.update_json_paths(data)
            
            # Return formatted JSON
            return json.dumps(data, indent=2)
            
        except json.JSONDecodeError:
            # Fallback to text replacement
            self.logger.warning(f"Could not parse JSON in {file_path}, using text replacement")
            return self.update_text_file(content)
    
    def update_yaml_file(self, content: str, file_path: Path) -> str:
        """Update path references in YAML files."""
        try:
            # Parse YAML
            data = yaml.safe_load(content)
            
            if data is not None:
                # Update paths recursively
                self.update_json_paths(data)  # Same logic works for YAML
                
                # Return formatted YAML
                return yaml.dump(data, default_flow_style=False, sort_keys=False)
            else:
                return content
                
        except yaml.YAMLError:
            # Fallback to text replacement
            self.logger.warning(f"Could not parse YAML in {file_path}, using text replacement")
            return self.update_text_file(content)
    
    def update_json_paths(self, obj):
        """Recursively update paths in JSON/YAML objects."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    # Apply path replacements
                    for pattern, replacement in self.replacement_patterns:
                        value = re.sub(pattern, replacement, value)
                    obj[key] = value
                else:
                    self.update_json_paths(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str):
                    # Apply path replacements
                    for pattern, replacement in self.replacement_patterns:
                        item = re.sub(pattern, replacement, item)
                    obj[i] = item
                else:
                    self.update_json_paths(item)
    
    def update_naming_enforcer(self, file_path: Path) -> bool:
        """Special handling for naming_enforcer.py."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Update parent directory traversal logic
            content = re.sub(
                r'script_dir\.parent\.parent\.parent',
                'script_dir.parent.parent',
                content
            )
            
            # Apply general patterns
            content = self.update_python_file(content)
            
            if content != original_content:
                if self.dry_run:
                    self.logger.info(f"[DRY RUN] Would update naming_enforcer.py")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.logger.info("Updated naming_enforcer.py")
                
                self.modified_files.append(str(file_path))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update naming_enforcer.py: {e}")
            return False
    
    def update_kb_linter(self, file_path: Path) -> bool:
        """Special handling for kb_linter.py."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Update master-knowledge-base detection logic
            content = re.sub(
                r'if str\(config\.repo_base\)\.endswith\("master-knowledge-base"\) and lint_target_dir_rel\.startswith\("master-knowledge-base/"\):',
                'if False:  # Disabled after migration',
                content
            )
            
            # Update default directory
            content = re.sub(
                r'default="standards/src"',
                'default="standards/src"',
                content
            )
            
            # Apply general patterns
            content = self.update_python_file(content)
            
            if content != original_content:
                if self.dry_run:
                    self.logger.info(f"[DRY RUN] Would update kb_linter.py")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.logger.info("Updated kb_linter.py")
                
                self.modified_files.append(str(file_path))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update kb_linter.py: {e}")
            return False
    
    def update_naming_configs(self, file_path: Path) -> bool:
        """Special handling for generate_naming_configs.py."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Update relative path
            content = re.sub(
                r'Path\("../../standards/src/GM-CONVENTIONS-NAMING\.md"\)',
                'Path("../standards/src/GM-CONVENTIONS-NAMING.md")',
                content
            )
            
            # Apply general patterns
            content = self.update_python_file(content)
            
            if content != original_content:
                if self.dry_run:
                    self.logger.info(f"[DRY RUN] Would update generate_naming_configs.py")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.logger.info("Updated generate_naming_configs.py")
                
                self.modified_files.append(str(file_path))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update generate_naming_configs.py: {e}")
            return False
    
    def update_standards_index(self, file_path: Path) -> bool:
        """Special handling for standards_index.json."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # This file will be regenerated, so just log it
            if self.dry_run:
                self.logger.info(f"[DRY RUN] Would regenerate standards_index.json")
            else:
                self.logger.info("standards_index.json will be regenerated")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to handle standards_index.json: {e}")
            return False
    
    def log_changes(self, file_path: Path, original: str, updated: str):
        """Log the changes that would be made."""
        # Find differences and log them
        original_lines = original.split('\n')
        updated_lines = updated.split('\n')
        
        changes_found = False
        for i, (orig_line, new_line) in enumerate(zip(original_lines, updated_lines)):
            if orig_line != new_line:
                if not changes_found:
                    self.logger.info(f"  Changes in {file_path}:")
                    changes_found = True
                self.logger.info(f"    Line {i+1}: '{orig_line}' -> '{new_line}'")
        
        if not changes_found and len(original_lines) != len(updated_lines):
            self.logger.info(f"  Line count changed in {file_path}: {len(original_lines)} -> {len(updated_lines)}")

if __name__ == "__main__":
    # This script is meant to be imported, not run directly
    print("This script should be imported by the migration controller.") 