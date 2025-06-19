#!/usr/bin/env python3
"""
Unified Redundancy Validator

Executes comprehensive redundancy detection and prevention validation.
Combines registry integrity, circular reference, and key definition validation.

Author: AI Development Team
Date: 2025-06-18
Purpose: Comprehensive tactical redundancy elimination and prevention
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from registry_integrity_validator import RegistryIntegrityValidator
from circular_reference_detector import CircularReferenceDetector
from key_definition_validator import KeyDefinitionValidator

class UnifiedRedundancyValidator:
    """Unified validator combining all redundancy detection mechanisms."""
    
    def __init__(self, standards_dir: str = "standards/src"):
        self.standards_dir = standards_dir
        self.root_dir = Path.cwd()
        self.validators = {
            "registry_integrity": RegistryIntegrityValidator(standards_dir),
            "circular_references": CircularReferenceDetector(standards_dir),
            "key_definitions": KeyDefinitionValidator(standards_dir)
        }
        
    def validate_all(self) -> Dict[str, Any]:
        """Run all redundancy validators and compile unified results."""
        print("🚀 STARTING UNIFIED REDUNDANCY VALIDATION")
        print("="*60)
        
        unified_results = {
            "timestamp": datetime.now().isoformat(),
            "validation_type": "unified_redundancy_validation",
            "validator_results": {},
            "summary": {
                "total_errors": 0,
                "total_warnings": 0,
                "validators_run": 0,
                "overall_status": "UNKNOWN"
            }
        }
        
        # Run each validator
        for validator_name, validator in self.validators.items():
            print(f"\n📊 Running {validator_name.replace('_', ' ').title()} Validator...")
            
            try:
                results = validator.validate_all()
                unified_results["validator_results"][validator_name] = results
                
                # Aggregate summary stats
                unified_results["summary"]["total_errors"] += results["summary"]["total_errors"]
                unified_results["summary"]["total_warnings"] += results["summary"]["total_warnings"]
                unified_results["summary"]["validators_run"] += 1
                
                print(f"✅ {validator_name}: {results['summary']['status']} "
                      f"({results['summary']['total_errors']} errors, "
                      f"{results['summary']['total_warnings']} warnings)")
                
            except Exception as e:
                error_msg = f"Failed to run {validator_name}: {str(e)}"
                print(f"❌ {error_msg}")
                unified_results["validator_results"][validator_name] = {
                    "error": error_msg,
                    "summary": {"status": "ERROR", "total_errors": 1, "total_warnings": 0}
                }
                unified_results["summary"]["total_errors"] += 1
        
        # Determine overall status
        if unified_results["summary"]["total_errors"] == 0:
            unified_results["summary"]["overall_status"] = "PASS"
        else:
            unified_results["summary"]["overall_status"] = "FAIL"
        
        return unified_results
    
    def generate_unified_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a comprehensive unified validation report."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M")
            output_file = f"tools/reports/unified-redundancy-validation-{timestamp}.md"
        
        report_content = f"""---
title: 'Unified Redundancy Validation Report'
date-created: '{results["timestamp"]}'
validation-type: '{results["validation_type"]}'
overall-status: '{results["summary"]["overall_status"]}'
---

# Unified Redundancy Validation Report

## Executive Summary

**🎯 OVERALL STATUS:** {results["summary"]["overall_status"]}
**Total Errors:** {results["summary"]["total_errors"]}
**Total Warnings:** {results["summary"]["total_warnings"]}
**Validators Run:** {results["summary"]["validators_run"]}
**Validation Date:** {results["timestamp"]}

## Validator Summary

"""
        
        # Summary table for each validator
        for validator_name, validator_results in results["validator_results"].items():
            status = validator_results.get("summary", {}).get("status", "ERROR")
            errors = validator_results.get("summary", {}).get("total_errors", 0)
            warnings = validator_results.get("summary", {}).get("total_warnings", 0)
            
            status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
            
            report_content += f"""### {status_emoji} {validator_name.replace('_', ' ').title()}
- **Status:** {status}
- **Errors:** {errors}
- **Warnings:** {warnings}

"""
        
        # Detailed results for each validator
        report_content += "## Detailed Results\n\n"
        
        for validator_name, validator_results in results["validator_results"].items():
            report_content += f"### {validator_name.replace('_', ' ').title()} Details\n\n"
            
            if "error" in validator_results:
                report_content += f"❌ **Validator Error:** {validator_results['error']}\n\n"
                continue
            
            # Errors
            errors = validator_results.get("errors", [])
            if errors:
                report_content += "**Errors:**\n"
                for i, error in enumerate(errors, 1):
                    report_content += f"{i}. ❌ {error}\n"
                report_content += "\n"
            
            # Warnings
            warnings = validator_results.get("warnings", [])
            if warnings:
                report_content += "**Warnings:**\n"
                for i, warning in enumerate(warnings, 1):
                    report_content += f"{i}. ⚠️ {warning}\n"
                report_content += "\n"
            
            if not errors and not warnings:
                report_content += "✅ **No issues found!**\n\n"
        
        # Overall assessment and recommendations
        report_content += f"""## Overall Assessment

"""
        
        if results["summary"]["overall_status"] == "PASS":
            report_content += """✅ **EXCELLENT:** All redundancy validators passed successfully!

The Standards Knowledge Base demonstrates excellent architectural integrity with:
- No registry duplications
- No circular references
- Clear key definitions
- Proper separation of concerns

"""
        else:
            report_content += f"""🚨 **ACTION REQUIRED:** {results["summary"]["total_errors"]} errors detected across validators.

Critical issues must be addressed immediately to maintain:
- Single Source of Truth principle
- Architectural integrity
- Operational clarity
- System reliability

"""
        
        report_content += f"""## Redundancy Prevention Framework

### Validation Coverage
1. **Registry Integrity:** Duplicate detection in key_standards arrays
2. **Circular References:** Self-referencing and navigation loops
3. **Key Definitions:** Semantic clarity and purpose distinction

### Integration Points
- **Current Tools:** Integrated with existing `tools/validation/` directory
- **CI/CD Ready:** All validators support automated execution
- **Reporting:** Timestamped reports in `tools/reports/`
- **Standards Compliant:** Follows Master Knowledge Base architecture

### Recommended Execution Schedule
- **Pre-commit:** Run unified validator before major changes
- **Daily:** Automated validation in CI/CD pipeline
- **Release:** Comprehensive validation before publishing
- **Quarterly:** Deep architectural review with all validators

## Next Steps

"""
        
        if results["summary"]["overall_status"] == "FAIL":
            report_content += """### Immediate Actions (P0-Critical)
1. **Fix all errors identified** by validators
2. **Verify fixes** by re-running validation
3. **Update documentation** to reflect changes
4. **Commit clean state** to version control

### Strategic Actions (P1-High)
"""
        else:
            report_content += "### Strategic Actions (P1-High)\n"
        
        report_content += """1. **Integrate validators** into development workflow
2. **Set up automated validation** in CI/CD pipeline
3. **Create monitoring dashboards** for ongoing compliance
4. **Document validation procedures** for team training

### Long-term Integration (P2-Medium)
1. **Extend validation rules** based on emerging patterns
2. **Create validation metrics** for architectural health
3. **Implement real-time validation** for live editing
4. **Develop validation plugins** for development tools

---
*Generated by Unified Redundancy Validator - Master Knowledge Base Quality Assurance*
"""
        
        # Write report file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return output_file
    
    def save_json_results(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Save detailed results in JSON format for programmatic use."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M")
            output_file = f"tools/reports/unified-redundancy-validation-{timestamp}.json"
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        
        return output_file

def main():
    """Main execution function."""
    print("🚀 UNIFIED REDUNDANCY VALIDATOR")
    print("="*60)
    print("Comprehensive redundancy detection and prevention for Master Knowledge Base")
    print("Validators: Registry Integrity | Circular References | Key Definitions")
    print("="*60)
    
    validator = UnifiedRedundancyValidator()
    results = validator.validate_all()
    
    # Generate reports
    report_file = validator.generate_unified_report(results)
    json_file = validator.save_json_results(results)
    
    # Print final summary
    print("\n" + "="*60)
    print("🎯 UNIFIED REDUNDANCY VALIDATION COMPLETE")
    print("="*60)
    print(f"Overall Status: {results['summary']['overall_status']}")
    print(f"Total Errors: {results['summary']['total_errors']}")
    print(f"Total Warnings: {results['summary']['total_warnings']}")
    print(f"Validators Run: {results['summary']['validators_run']}")
    print(f"Report: {report_file}")
    print(f"JSON Data: {json_file}")
    
    if results['summary']['overall_status'] == "FAIL":
        print(f"\n🚨 CRITICAL: {results['summary']['total_errors']} errors require immediate attention!")
        print("Review the detailed report for specific issues and remediation steps.")
    else:
        print("\n✅ SUCCESS: All redundancy validators passed!")
        print("Standards Knowledge Base maintains excellent architectural integrity.")
    
    print("="*60)
    
    return results['summary']['total_errors']

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 