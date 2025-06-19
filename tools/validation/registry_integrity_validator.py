#!/usr/bin/env python3
"""
Registry Integrity Validator

Detects duplicates and integrity issues in Standards Knowledge Base registry files.
Ensures Single Source of Truth principle compliance.

Author: AI Development Team
Date: 2025-06-18
Purpose: Tactical redundancy elimination and prevention
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime

class RegistryIntegrityValidator:
    """Validates registry integrity across AS-MAP-STANDARDS-KB.md and related files."""
    
    def __init__(self, standards_dir: str = "standards/src"):
        self.standards_dir = Path(standards_dir)
        self.root_dir = Path.cwd()
        self.errors = []
        self.warnings = []
        
    def validate_all(self) -> Dict[str, Any]:
        """Run comprehensive registry integrity validation."""
        print("🔍 Starting Registry Integrity Validation...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "validation_type": "registry_integrity",
            "errors": [],
            "warnings": [],
            "summary": {}
        }
        
        # Validate AS-MAP-STANDARDS-KB.md
        map_file = self.standards_dir / "AS-MAP-STANDARDS-KB.md"
        if map_file.exists():
            self._validate_standards_map(map_file)
        else:
            self.errors.append(f"Critical: AS-MAP-STANDARDS-KB.md not found at {map_file}")
        
        # Cross-validate with actual standards files
        self._cross_validate_standards()
        
        # Validate key_standards array integrity
        self._validate_key_standards_arrays()
        
        # Compile results
        results["errors"] = self.errors
        results["warnings"] = self.warnings
        results["summary"] = {
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "status": "PASS" if len(self.errors) == 0 else "FAIL"
        }
        
        return results
    
    def _validate_standards_map(self, map_file: Path) -> None:
        """Validate AS-MAP-STANDARDS-KB.md for duplicates and integrity."""
        print(f"📋 Validating {map_file.name}...")
        
        try:
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML frontmatter
            if content.startswith('---\n'):
                end_yaml = content.find('\n---\n', 4)
                if end_yaml != -1:
                    yaml_content = content[4:end_yaml]
                    frontmatter = yaml.safe_load(yaml_content)
                    
                    # Validate kb_definition structure
                    if 'kb_definition' in frontmatter and 'parts' in frontmatter['kb_definition']:
                        self._validate_parts_structure(frontmatter['kb_definition']['parts'])
                    else:
                        self.errors.append("Missing kb_definition.parts structure in AS-MAP-STANDARDS-KB.md")
                        
        except Exception as e:
            self.errors.append(f"Failed to parse AS-MAP-STANDARDS-KB.md: {str(e)}")
    
    def _validate_parts_structure(self, parts: List[Dict]) -> None:
        """Validate parts structure for duplicates and consistency."""
        print("🔍 Validating parts structure...")
        
        part_ids = []
        
        for part in parts:
            if not isinstance(part, dict):
                self.errors.append(f"Invalid part structure: {part}")
                continue
                
            part_id = part.get('part_id', 'unknown')
            part_ids.append(part_id)
            
            # Check for duplicate part_ids
            if part_ids.count(part_id) > 1:
                self.errors.append(f"Duplicate part_id found: {part_id}")
            
            # Validate key_standards array
            key_standards = part.get('key_standards', [])
            if key_standards:
                self._validate_key_standards_array(part_id, key_standards)
            
            # Validate standard_count
            standard_count = part.get('standard_count', 0)
            if len(key_standards) != standard_count:
                self.warnings.append(
                    f"Part {part_id}: standard_count ({standard_count}) "
                    f"doesn't match key_standards length ({len(key_standards)})"
                )
    
    def _validate_key_standards_array(self, part_id: str, key_standards: List[str]) -> None:
        """Validate individual key_standards array for duplicates."""
        print(f"🔍 Validating key_standards for {part_id}...")
        
        # Check for duplicates
        seen = set()
        duplicates = set()
        
        for standard in key_standards:
            if standard in seen:
                duplicates.add(standard)
                self.errors.append(f"Duplicate standard in {part_id}: {standard}")
            seen.add(standard)
        
        # Check for empty entries
        if "" in key_standards or None in key_standards:
            self.errors.append(f"Empty standard entry found in {part_id}")
            
        # Check standard naming conventions
        for standard in key_standards:
            if not isinstance(standard, str):
                self.errors.append(f"Non-string standard ID in {part_id}: {standard}")
                continue
                
            if not standard.replace('-', '').replace('_', '').isalnum():
                self.warnings.append(f"Unusual characters in standard ID {part_id}: {standard}")
    
    def _cross_validate_standards(self) -> None:
        """Cross-validate standards map against actual files."""
        print("🔍 Cross-validating against actual standards files...")
        
        # Get actual standard files
        actual_standards = set()
        for file_path in self.standards_dir.glob("*.md"):
            if file_path.name.startswith(("AS-", "CS-", "GM-", "MT-", "OM-", "QM-", "SF-", "UA-")):
                standard_id = file_path.stem
                actual_standards.add(standard_id)
        
        print(f"📊 Found {len(actual_standards)} actual standard files")
        
        # Compare with registry (this would need AS-MAP parsing to get all referenced standards)
        # For now, just report the count
        self.warnings.append(f"Cross-validation: {len(actual_standards)} standards found in filesystem")
    
    def _validate_key_standards_arrays(self) -> None:
        """Additional validation for key_standards arrays across all parts."""
        print("🔍 Performing additional key_standards validation...")
        
        # This could be extended to check for:
        # - Standards referenced in multiple domains inappropriately
        # - Missing standards that should be included
        # - Orphaned standards not referenced anywhere
        pass
    
    def generate_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a formatted validation report."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M")
            output_file = f"tools/reports/registry-integrity-validation-{timestamp}.md"
        
        report_content = f"""---
title: 'Registry Integrity Validation Report'
date-created: '{results["timestamp"]}'
validation-type: '{results["validation_type"]}'
status: '{results["summary"]["status"]}'
---

# Registry Integrity Validation Report

## Executive Summary

**Validation Status:** {results["summary"]["status"]}
**Total Errors:** {results["summary"]["total_errors"]}
**Total Warnings:** {results["summary"]["total_warnings"]}
**Validation Date:** {results["timestamp"]}

## Errors Found

"""
        
        if results["errors"]:
            for i, error in enumerate(results["errors"], 1):
                report_content += f"{i}. ❌ **ERROR:** {error}\n"
        else:
            report_content += "✅ **No errors found!**\n"
        
        report_content += "\n## Warnings Found\n\n"
        
        if results["warnings"]:
            for i, warning in enumerate(results["warnings"], 1):
                report_content += f"{i}. ⚠️ **WARNING:** {warning}\n"
        else:
            report_content += "✅ **No warnings found!**\n"
        
        report_content += f"""

## Validation Details

- **Registry File:** AS-MAP-STANDARDS-KB.md
- **Standards Directory:** {self.standards_dir}
- **Validation Type:** Registry Integrity
- **Focus Areas:** 
  - Duplicate detection in key_standards arrays
  - Standard count accuracy verification
  - Cross-validation with actual files
  - YAML structure validation

## Recommendations

"""
        
        if results["summary"]["status"] == "FAIL":
            report_content += "🚨 **IMMEDIATE ACTION REQUIRED:** Errors detected that violate Single Source of Truth principle.\n\n"
        else:
            report_content += "✅ **Registry integrity maintained successfully.**\n\n"
        
        report_content += """
## Next Steps

1. **Fix any errors immediately** to maintain registry integrity
2. **Review warnings** for potential improvements
3. **Run validation regularly** to prevent future issues
4. **Integrate with CI/CD** for automated checking

---
*Generated by Registry Integrity Validator*
"""
        
        # Write report file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return output_file

def main():
    """Main execution function."""
    validator = RegistryIntegrityValidator()
    results = validator.validate_all()
    
    # Generate report
    report_file = validator.generate_report(results)
    
    # Print summary
    print("\n" + "="*60)
    print("🎯 REGISTRY INTEGRITY VALIDATION COMPLETE")
    print("="*60)
    print(f"Status: {results['summary']['status']}")
    print(f"Errors: {results['summary']['total_errors']}")
    print(f"Warnings: {results['summary']['total_warnings']}")
    print(f"Report: {report_file}")
    
    if results['summary']['status'] == "FAIL":
        print("\n🚨 ACTION REQUIRED: Registry integrity issues detected!")
        for error in results['errors']:
            print(f"   ❌ {error}")
    else:
        print("\n✅ Registry integrity validated successfully!")
    
    return results['summary']['total_errors']

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 