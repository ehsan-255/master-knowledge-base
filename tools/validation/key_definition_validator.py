#!/usr/bin/env python3
"""
Key Definition Validator

Ensures semantic clarity and purpose distinction in key definition files.
Prevents conceptual redundancy and validates key-value relationships.

Author: AI Development Team
Date: 2025-06-18
Purpose: Tactical redundancy elimination and prevention
"""

import os
import yaml
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime
from collections import defaultdict

class KeyDefinitionValidator:
    """Validates key definitions for semantic clarity and purpose distinction."""
    
    def __init__(self, standards_dir: str = "standards/src"):
        self.standards_dir = Path(standards_dir)
        self.root_dir = Path.cwd()
        self.errors = []
        self.warnings = []
        self.key_definitions = {}
        
    def validate_all(self) -> Dict[str, Any]:
        """Run comprehensive key definition validation."""
        print("🔍 Starting Key Definition Validation...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "validation_type": "key_definition_validation",
            "errors": [],
            "warnings": [],
            "summary": {}
        }
        
        # Validate UA-KEYDEFS-GLOBAL.md
        keydefs_file = self.standards_dir / "UA-KEYDEFS-GLOBAL.md"
        if keydefs_file.exists():
            self._validate_global_keydefs(keydefs_file)
        else:
            self.errors.append(f"Critical: UA-KEYDEFS-GLOBAL.md not found at {keydefs_file}")
        
        # Validate key relationships and semantics
        self._validate_key_semantics()
        
        # Check for conceptual redundancy
        self._detect_conceptual_redundancy()
        
        # Validate key naming conventions
        self._validate_key_naming()
        
        # Cross-validate key usage
        self._cross_validate_key_usage()
        
        # Compile results
        results["errors"] = self.errors
        results["warnings"] = self.warnings
        results["summary"] = {
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "status": "PASS" if len(self.errors) == 0 else "FAIL",
            "keys_analyzed": len(self.key_definitions),
            "categories_found": len(set(key.split('-')[0] for key in self.key_definitions.keys() if '-' in key))
        }
        
        return results
    
    def _validate_global_keydefs(self, keydefs_file: Path) -> None:
        """Validate UA-KEYDEFS-GLOBAL.md structure and content."""
        print(f"📋 Validating {keydefs_file.name}...")
        
        try:
            with open(keydefs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML frontmatter
            if content.startswith('---\n'):
                end_yaml = content.find('\n---\n', 4)
                if end_yaml != -1:
                    yaml_content = content[4:end_yaml]
                    frontmatter = yaml.safe_load(yaml_content)
                    
                    # Extract key definitions from keys section
                    if 'keys' in frontmatter:
                        self.key_definitions = frontmatter['keys']
                        print(f"   📊 Found {len(self.key_definitions)} key definitions")
                    else:
                        self.errors.append("Missing 'keys' section in UA-KEYDEFS-GLOBAL.md")
                else:
                    self.errors.append("Invalid YAML frontmatter in UA-KEYDEFS-GLOBAL.md")
            else:
                self.errors.append("Missing YAML frontmatter in UA-KEYDEFS-GLOBAL.md")
                
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error in UA-KEYDEFS-GLOBAL.md: {str(e)}")
        except Exception as e:
            self.errors.append(f"Failed to parse UA-KEYDEFS-GLOBAL.md: {str(e)}")
    
    def _validate_key_semantics(self) -> None:
        """Validate semantic meaning and purpose of each key."""
        print("🎯 Validating key semantics...")
        
        for key, value in self.key_definitions.items():
            # Check for empty or null values
            if not value or (isinstance(value, str) and value.strip() == ""):
                self.errors.append(f"Empty value for key: {key}")
                continue
            
            # Check for placeholder values
            placeholder_patterns = [
                r'TODO', r'PLACEHOLDER', r'FIXME', r'TBD', r'NOT_SET'
            ]
            
            if isinstance(value, str):
                for pattern in placeholder_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        self.warnings.append(f"Placeholder value detected for key '{key}': {value}")
            
            # Validate specific key types
            self._validate_specific_key_types(key, value)
    
    def _validate_specific_key_types(self, key: str, value: Any) -> None:
        """Validate specific types of keys for appropriate values."""
        
        # URL keys should be valid paths or URLs
        if 'url' in key.lower() or 'link' in key.lower():
            if isinstance(value, str):
                if not (value.startswith(('http://', 'https://', '/', './', '../')) or 
                       value.endswith(('.md', '.html', '.json', '.yaml', '.yml'))):
                    self.warnings.append(f"Unusual URL/link format for key '{key}': {value}")
        
        # Date keys should follow date patterns
        if 'date' in key.lower():
            if isinstance(value, str):
                # Check for common date patterns
                date_patterns = [
                    r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                    r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                    r'\d{2}-\d{2}-\d{4}'   # MM-DD-YYYY
                ]
                
                if not any(re.search(pattern, value) for pattern in date_patterns):
                    self.warnings.append(f"Unusual date format for key '{key}': {value}")
        
        # Version keys should follow version patterns
        if 'version' in key.lower():
            if isinstance(value, str):
                version_pattern = r'^\d+\.\d+(\.\d+)?(-\w+)?$'
                if not re.match(version_pattern, value):
                    self.warnings.append(f"Unusual version format for key '{key}': {value}")
    
    def _detect_conceptual_redundancy(self) -> None:
        """Detect conceptual redundancy between keys."""
        print("🔍 Detecting conceptual redundancy...")
        
        # Group keys by similar values
        value_groups = defaultdict(list)
        for key, value in self.key_definitions.items():
            if isinstance(value, str):
                value_groups[value].append(key)
        
        # Check for duplicate values
        for value, keys in value_groups.items():
            if len(keys) > 1:
                # Check if these are conceptually different
                key_purposes = []
                for key in keys:
                    purpose = self._infer_key_purpose(key)
                    key_purposes.append((key, purpose))
                
                # If purposes are similar, flag as redundancy
                unique_purposes = set(purpose for _, purpose in key_purposes)
                if len(unique_purposes) < len(keys):
                    self.errors.append(
                        f"Conceptual redundancy detected - multiple keys with same value '{value}': {keys}"
                    )
                else:
                    self.warnings.append(
                        f"Same value used for different purposes: {value} -> {keys}"
                    )
    
    def _infer_key_purpose(self, key: str) -> str:
        """Infer the purpose of a key from its name."""
        key_lower = key.lower()
        
        # Purpose categories
        if 'missing' in key_lower or 'fallback' in key_lower or 'default' in key_lower:
            return 'fallback_value'
        elif 'url' in key_lower or 'link' in key_lower:
            return 'reference_link'
        elif 'name' in key_lower or 'title' in key_lower:
            return 'identifier'
        elif 'date' in key_lower or 'time' in key_lower:
            return 'temporal'
        elif 'version' in key_lower:
            return 'versioning'
        elif 'path' in key_lower or 'dir' in key_lower:
            return 'file_system'
        else:
            return 'general'
    
    def _validate_key_naming(self) -> None:
        """Validate key naming conventions."""
        print("📝 Validating key naming conventions...")
        
        for key in self.key_definitions.keys():
            # Check naming convention (kebab-case recommended)
            if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', key):
                self.warnings.append(f"Key '{key}' doesn't follow kebab-case convention")
            
            # Check for overly long keys
            if len(key) > 50:
                self.warnings.append(f"Overly long key name: {key}")
            
            # Check for unclear abbreviations
            unclear_abbrevs = ['tmp', 'temp', 'aux', 'misc', 'util']
            for abbrev in unclear_abbrevs:
                if abbrev in key.lower():
                    self.warnings.append(f"Unclear abbreviation in key '{key}': {abbrev}")
    
    def _cross_validate_key_usage(self) -> None:
        """Cross-validate key usage across standards files."""
        print("🔄 Cross-validating key usage...")
        
        # Find key references in other files
        used_keys = set()
        unused_keys = set(self.key_definitions.keys())
        
        for file_path in self.standards_dir.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for key references in various formats
                for key in self.key_definitions.keys():
                    patterns = [
                        rf'\[\[{re.escape(key)}\]\]',  # [[key]] format
                        rf'`{re.escape(key)}`',        # `key` format
                        rf'{{{{.*{re.escape(key)}.*}}}}'  # {{key}} template format
                    ]
                    
                    for pattern in patterns:
                        if re.search(pattern, content):
                            used_keys.add(key)
                            unused_keys.discard(key)
                            break
                            
            except Exception as e:
                self.warnings.append(f"Failed to read {file_path} for key usage: {str(e)}")
        
        # Report unused keys
        if unused_keys:
            self.warnings.append(f"Unused keys detected: {sorted(unused_keys)}")
        
        print(f"   📊 Key usage: {len(used_keys)} used, {len(unused_keys)} unused")
    
    def generate_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a formatted validation report."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M")
            output_file = f"tools/reports/key-definition-validation-{timestamp}.md"
        
        report_content = f"""---
title: 'Key Definition Validation Report'
date-created: '{results["timestamp"]}'
validation-type: '{results["validation_type"]}'
status: '{results["summary"]["status"]}'
---

# Key Definition Validation Report

## Executive Summary

**Validation Status:** {results["summary"]["status"]}
**Total Errors:** {results["summary"]["total_errors"]}
**Total Warnings:** {results["summary"]["total_warnings"]}
**Keys Analyzed:** {results["summary"]["keys_analyzed"]}
**Categories Found:** {results["summary"]["categories_found"]}
**Validation Date:** {results["timestamp"]}

## Errors Found

"""
        
        if results["errors"]:
            for i, error in enumerate(results["errors"], 1):
                report_content += f"{i}. ❌ **ERROR:** {error}\n"
        else:
            report_content += "✅ **No key definition errors found!**\n"
        
        report_content += "\n## Warnings Found\n\n"
        
        if results["warnings"]:
            for i, warning in enumerate(results["warnings"], 1):
                report_content += f"{i}. ⚠️ **WARNING:** {warning}\n"
        else:
            report_content += "✅ **No key definition warnings found!**\n"
        
        # Add key analysis summary
        if self.key_definitions:
            report_content += f"""

## Key Definition Analysis

### Key Categories
"""
            
            # Categorize keys
            categories = defaultdict(list)
            for key in self.key_definitions.keys():
                purpose = self._infer_key_purpose(key)
                categories[purpose].append(key)
            
            for category, keys in sorted(categories.items()):
                report_content += f"- **{category.replace('_', ' ').title()}:** {len(keys)} keys\n"
                for key in sorted(keys)[:5]:  # Show first 5
                    report_content += f"  - `{key}`\n"
                if len(keys) > 5:
                    report_content += f"  - ... and {len(keys) - 5} more\n"
        
        report_content += f"""

## Validation Details

- **File Analyzed:** UA-KEYDEFS-GLOBAL.md
- **Validation Areas:**
  - Semantic clarity and purpose distinction
  - Conceptual redundancy detection
  - Key naming conventions
  - Cross-file usage validation
  - Value format validation
- **Detection Methods:**
  - Value similarity analysis
  - Purpose inference from key names
  - Pattern-based validation
  - Cross-reference scanning

## Recommendations

"""
        
        if results["summary"]["status"] == "FAIL":
            report_content += "🚨 **IMMEDIATE ACTION REQUIRED:** Key definition issues detected.\n\n"
        else:
            report_content += "✅ **Key definitions validated successfully.**\n\n"
        
        report_content += """
## Next Steps

1. **Fix conceptual redundancies** to maintain clarity
2. **Review naming conventions** for consistency
3. **Remove unused keys** to reduce bloat
4. **Document key purposes** for future maintainers

---
*Generated by Key Definition Validator*
"""
        
        # Write report file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return output_file

def main():
    """Main execution function."""
    validator = KeyDefinitionValidator()
    results = validator.validate_all()
    
    # Generate report
    report_file = validator.generate_report(results)
    
    # Print summary
    print("\n" + "="*60)
    print("🔑 KEY DEFINITION VALIDATION COMPLETE")
    print("="*60)
    print(f"Status: {results['summary']['status']}")
    print(f"Errors: {results['summary']['total_errors']}")
    print(f"Warnings: {results['summary']['total_warnings']}")
    print(f"Keys: {results['summary']['keys_analyzed']}")
    print(f"Categories: {results['summary']['categories_found']}")
    print(f"Report: {report_file}")
    
    if results['summary']['status'] == "FAIL":
        print("\n🚨 ACTION REQUIRED: Key definition issues detected!")
        for error in results['errors']:
            print(f"   ❌ {error}")
    else:
        print("\n✅ Key definitions validated successfully!")
    
    return results['summary']['total_errors']

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 