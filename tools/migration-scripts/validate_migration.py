#!/usr/bin/env python3
"""
Migration Validator for Master Knowledge Base Migration

This script validates that the migration from master-knowledge-base/ to repository root
was completed successfully.

Author: Automated Migration System
Generated: 2025-01-27
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
import logging

class MigrationValidator:
    """Validates migration success and integrity."""
    
    def __init__(self, repo_root: Path, logger: logging.Logger):
        self.repo_root = repo_root
        self.logger = logger
        
        # Expected structure after migration
        self.expected_root_items = [
            "standards",
            "tools",
            "dist",
            "AS-INDEX-KB-MASTER.md",
            "repo-tree.md"
        ]
        
        # Critical files that must exist
        self.critical_files = [
            "standards/src",
            "standards/registry", 
            "standards/templates",
            "tools/linter",
            "tools/indexer",
            "tools/utilities"
        ]
        
        # Patterns that should NOT exist after migration
        self.forbidden_patterns = [
            r'standards/',
            r'tools/',
            r'dist/',
            r'/standards/',
            r'/tools/',
            r'/dist/'
        ]
    
    def validate_migration(self) -> Dict:
        """Perform comprehensive migration validation."""
        results = {
            "overall_success": True,
            "structure_validation": {},
            "path_reference_validation": {},
            "file_integrity_validation": {},
            "errors": [],
            "warnings": []
        }
        
        try:
            self.logger.info("Starting migration validation...")
            
            # Validate directory structure
            structure_results = self.validate_structure()
            results["structure_validation"] = structure_results
            if not structure_results["success"]:
                results["overall_success"] = False
            
            # Validate path references
            path_results = self.validate_path_references()
            results["path_reference_validation"] = path_results
            if not path_results["success"]:
                results["overall_success"] = False
            
            # Validate file integrity
            integrity_results = self.validate_file_integrity()
            results["file_integrity_validation"] = integrity_results
            if not integrity_results["success"]:
                results["overall_success"] = False
            
            # Compile overall results
            results["errors"] = (
                structure_results.get("errors", []) +
                path_results.get("errors", []) +
                integrity_results.get("errors", [])
            )
            
            results["warnings"] = (
                structure_results.get("warnings", []) +
                path_results.get("warnings", []) +
                integrity_results.get("warnings", [])
            )
            
            if results["overall_success"]:
                self.logger.info("✅ Migration validation PASSED")
            else:
                self.logger.error("❌ Migration validation FAILED")
                for error in results["errors"]:
                    self.logger.error(f"  - {error}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Migration validation failed: {e}")
            results["overall_success"] = False
            results["errors"].append(f"Validation exception: {e}")
            return results
    
    def validate_structure(self) -> Dict:
        """Validate that the directory structure is correct after migration."""
        results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "found_items": [],
            "missing_items": []
        }
        
        try:
            self.logger.info("Validating directory structure...")
            
            # Check that expected items exist in root
            for item_name in self.expected_root_items:
                item_path = self.repo_root / item_name
                if item_path.exists():
                    results["found_items"].append(item_name)
                    self.logger.info(f"✅ Found: {item_name}")
                else:
                    results["missing_items"].append(item_name)
                    results["errors"].append(f"Missing expected item: {item_name}")
                    self.logger.error(f"❌ Missing: {item_name}")
            
            # Check critical subdirectories
            for critical_path in self.critical_files:
                full_path = self.repo_root / critical_path
                if full_path.exists():
                    self.logger.info(f"✅ Critical path exists: {critical_path}")
                else:
                    results["errors"].append(f"Missing critical path: {critical_path}")
                    self.logger.error(f"❌ Missing critical path: {critical_path}")
            
            # Check if master-knowledge-base still contains moved items
            mkb_path = self.repo_root / "master-knowledge-base"
            if mkb_path.exists():
                for item_name in self.expected_root_items:
                    old_path = mkb_path / item_name
                    if old_path.exists():
                        results["warnings"].append(f"Item still exists in old location: master-knowledge-base/{item_name}")
                        self.logger.warning(f"⚠️  Item still in old location: master-knowledge-base/{item_name}")
            
            if results["errors"]:
                results["success"] = False
            
            return results
            
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Structure validation failed: {e}")
            return results
    
    def validate_path_references(self) -> Dict:
        """Validate that path references have been updated correctly."""
        results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "files_with_old_references": [],
            "total_files_checked": 0
        }
        
        try:
            self.logger.info("Validating path references...")
            
            # Get all text files to check
            files_to_check = self.get_text_files()
            results["total_files_checked"] = len(files_to_check)
            
            for file_path in files_to_check:
                old_refs = self.find_old_path_references(file_path)
                if old_refs:
                    results["files_with_old_references"].append({
                        "file": str(file_path.relative_to(self.repo_root)),
                        "references": old_refs
                    })
                    results["errors"].append(f"Old path references found in: {file_path.relative_to(self.repo_root)}")
            
            if results["files_with_old_references"]:
                results["success"] = False
                self.logger.error(f"❌ Found old path references in {len(results['files_with_old_references'])} files")
            else:
                self.logger.info("✅ No old path references found")
            
            return results
            
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Path reference validation failed: {e}")
            return results
    
    def validate_file_integrity(self) -> Dict:
        """Validate that files were moved correctly and are intact."""
        results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "file_counts": {}
        }
        
        try:
            self.logger.info("Validating file integrity...")
            
            # Count files in key directories
            for item_name in ["standards", "tools"]:
                item_path = self.repo_root / item_name
                if item_path.exists():
                    file_count = self.count_files_recursive(item_path)
                    results["file_counts"][item_name] = file_count
                    self.logger.info(f"✅ {item_name}: {file_count} files")
                else:
                    results["errors"].append(f"Directory not found: {item_name}")
            
            # Check for empty directories
            empty_dirs = self.find_empty_directories()
            if empty_dirs:
                results["warnings"].extend([f"Empty directory: {d}" for d in empty_dirs])
            
            # Basic file integrity checks
            if results["file_counts"].get("standards", 0) < 50:
                results["warnings"].append("Standards directory has fewer files than expected")
            
            if results["file_counts"].get("tools", 0) < 10:
                results["warnings"].append("Tools directory has fewer files than expected")
            
            return results
            
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"File integrity validation failed: {e}")
            return results
    
    def get_text_files(self) -> List[Path]:
        """Get list of text files to check for path references."""
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
    
    def find_old_path_references(self, file_path: Path) -> List[str]:
        """Find old path references in a file."""
        old_references = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for forbidden patterns
            for pattern in self.forbidden_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    old_references.extend(matches)
            
        except (UnicodeDecodeError, PermissionError):
            # Skip files that can't be read
            pass
        except Exception as e:
            self.logger.warning(f"Could not check {file_path}: {e}")
        
        return old_references
    
    def count_files_recursive(self, directory: Path) -> int:
        """Count files recursively in a directory."""
        count = 0
        try:
            for root, dirs, files in os.walk(directory):
                count += len(files)
        except Exception:
            pass
        return count
    
    def find_empty_directories(self) -> List[str]:
        """Find empty directories that might indicate incomplete migration."""
        empty_dirs = []
        
        try:
            for root, dirs, files in os.walk(self.repo_root):
                # Skip archive and other excluded directories
                if 'archive' in root or '.git' in root:
                    continue
                
                if not dirs and not files:
                    rel_path = Path(root).relative_to(self.repo_root)
                    empty_dirs.append(str(rel_path))
        
        except Exception:
            pass
        
        return empty_dirs

if __name__ == "__main__":
    # This script is meant to be imported, not run directly
    print("This script should be imported by the migration controller.") 