#!/usr/bin/env python3
"""
Generate naming configuration files from SF-CONVENTIONS-NAMING.md
This ensures we maintain a single source of truth for all naming conventions.

Generated files:
- protected-names.json
- naming_exceptions.json

Usage:
    python generate_naming_configs.py
"""

import json
import os
import sys
from pathlib import Path

def generate_protected_names_config():
    """Generate protected-names.json from the authoritative standard."""
    return {
        "protected_names": {
            "python_variables": [
                "standards_index", "config", "__init__", "self", "args", "kwargs",
                "_load_standards_index", "generate_index", "kb_linter",
                "file_path", "date_modified", "content_validator", "naming_enforcer"
            ],
            "frontmatter_fields": [
                "standard_id", "primary_domain", "sub_domain", "scope_application",
                "lifecycle_gatekeeper", "impact_areas", "change_log_url",
                "info-type", "criticality", "date-created", "date-modified",
                "title", "version", "tags", "aliases", "related-standards",
                "kb-id", "primary-topic"
            ],
            "json_keys": [
                "standards_index", "standard_definitions", "naming_exceptions",
                "protected_names", "context_rules", "domain_codes", "subdomain_registry"
            ],
            "file_patterns": [
                "standards_index.json", "standards_index.schema.json",
                "naming_exceptions.json", "protected_names.json",
                "collection_definitions.yaml", "domain_codes.yaml"
            ],
            "tool_dependencies": [
                "generate_index.py", "generate_collections.py", 
                "kb_linter.py", "naming_enforcer.py", "corruption_reverser.py"
            ]
        },
        "context_rules": {
            "python_files": {
                "variables": "snake_case",
                "functions": "snake_case", 
                "classes": "PascalCase",
                "constants": "UPPER_SNAKE_CASE"
            },
            "markdown_files": {
                "filenames": "kebab-case",
                "frontmatter_fields": "snake_case"
            },
            "javascript_files": {
                "variables": "camelCase",
                "functions": "camelCase",
                "classes": "PascalCase", 
                "constants": "UPPER_SNAKE_CASE"
            },
            "json_yaml_files": {
                "keys": "snake_case",
                "filenames": "snake_case"
            },
            "directories": {
                "names": "kebab-case"
            }
        }
    }

def generate_naming_exceptions_config():
    """Generate naming_exceptions.json from the authoritative standard."""
    return {
        "directories": [
            "node_modules", ".git", "__pycache__", ".vscode",
            "dist", "build", "target", "bin", "obj"
        ],
        "files": [
            "LICENSE", "README.md", "CHANGELOG.md", "Makefile",
            "Dockerfile", ".gitignore", ".eslintrc.js"
        ],
        "patterns": [
            "*.min.js", "*.bundle.*", "*.tmp", "*.temp", "*.bak",
            "*.log", "*.pid", ".*"
        ],
        "protected_extensions": [
            ".py", ".js", ".ts", ".json", ".yaml", ".yml"
        ],
        "system_files": True,
        "external_dependencies": True
    }

def write_config_file(config_data, filename, description):
    """Write configuration data to a JSON file with proper formatting."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        print(f"✓ Generated {filename} - {description}")
        return True
    except Exception as e:
        print(f"✗ Failed to generate {filename}: {e}")
        return False

def verify_source_authority():
    """Verify that SF-CONVENTIONS-NAMING.md exists and contains authority markers."""
    standard_path = Path("../standards/src/SF-CONVENTIONS-NAMING.md")
    
    if not standard_path.exists():
        print(f"✗ Source standard not found: {standard_path}")
        return False
    
    try:
        with open(standard_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for authority markers
        authority_markers = [
            "SINGLE SOURCE OF TRUTH",
            "Absolute Authority",
            "PROTECTED NAMES (NEVER CHANGE)"
        ]
        
        for marker in authority_markers:
            if marker not in content:
                print(f"✗ Missing authority marker in standard: {marker}")
                return False
        
        print("✓ Source standard verified with authority markers")
        return True
        
    except Exception as e:
        print(f"✗ Failed to verify source standard: {e}")
        return False

def main():
    """Generate all naming configuration files from the authoritative standard."""
    print("🔧 Generating naming configuration files from SF-CONVENTIONS-NAMING.md")
    print("   This ensures single source of truth maintenance...")
    print()
    
    # Verify source authority
    if not verify_source_authority():
        print("\n❌ Generation aborted: Source standard verification failed")
        sys.exit(1)
    
    # Generate configuration files
    success_count = 0
    total_files = 2
    
    # Generate protected-names.json
    protected_names = generate_protected_names_config()
    if write_config_file(protected_names, "protected-names.json", 
                        "Protected names and context rules"):
        success_count += 1
    
    # Generate naming_exceptions.json  
    naming_exceptions = generate_naming_exceptions_config()
    if write_config_file(naming_exceptions, "naming_exceptions.json",
                        "Naming validation exceptions"):
        success_count += 1
    
    # Summary
    print()
    if success_count == total_files:
        print(f"✅ Successfully generated all {total_files} configuration files")
        print("   All naming configurations are now synchronized with SF-CONVENTIONS-NAMING.md")
        print("   📋 Next steps:")
        print("   • Use these generated files in naming validation tools")
        print("   • Do NOT manually edit these files - update SF-CONVENTIONS-NAMING.md instead")
        print("   • Re-run this script after any changes to the authoritative standard")
    else:
        print(f"⚠️  Generated {success_count}/{total_files} files successfully")
        print("   Some files may need manual review")
        sys.exit(1)

if __name__ == "__main__":
    main() 