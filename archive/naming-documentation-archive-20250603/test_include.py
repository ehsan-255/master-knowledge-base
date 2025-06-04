#!/usr/bin/env python3
"""
Test script for the include functionality of the naming enforcer
"""

import sys
from pathlib import Path
from naming_enforcer import NamingEnforcerV2

def test_include_functionality():
    """Test various include patterns and precedence rules"""
    print("Testing Naming Enforcer Include Functionality")
    print("=" * 50)
    
    # Initialize enforcer with correct path
    standard_path = "../../standards/src/GM-CONVENTIONS-NAMING.md"
    enforcer = NamingEnforcerV2(standard_path)
    
    # Test 1: Add individual inclusions
    print("\n1. Testing individual inclusions:")
    enforcer.include_manager.add_include_file("naming_enforcer.py", "Test file inclusion")
    enforcer.include_manager.add_include_directory("tests", "Test directory inclusion")
    enforcer.include_manager.add_include_glob("*.py", "Test glob inclusion")
    enforcer.include_manager.add_include_regex(r".*\.md$", "Test regex inclusion")
    
    print(enforcer.include_manager.get_inclusion_summary())
    
    # Test 2: Test inclusion logic
    print("\n2. Testing inclusion logic:")
    test_paths = [
        Path("naming_enforcer.py"),  # Should be included (specific file + glob)
        Path("tests/test_file.py"),  # Should be included (directory + glob)
        Path("README.md"),           # Should be included (regex)
        Path("temp.txt"),            # Should NOT be included
        Path("other_script.py"),     # Should be included (glob)
        Path("docs/guide.md")        # Should be included (regex)
    ]
    
    for test_path in test_paths:
        is_included = enforcer.include_manager.is_included(test_path)
        print(f"  {test_path}: {'INCLUDED' if is_included else 'excluded'}")
    
    # Test 3: Test precedence rules (exclude takes precedence over include)
    print("\n3. Testing precedence rules (exclude > include):")
    
    # Add some exclusions
    enforcer.exclude_manager.add_exclude_file("naming_enforcer.py", "Test exclusion precedence")
    enforcer.exclude_manager.add_exclude_glob("*test*", "Test glob exclusion")
    
    print("Include patterns:", len(enforcer.include_manager.include_patterns))
    print("Exclude patterns:", len(enforcer.exclude_manager.exclude_patterns))
    
    precedence_test_paths = [
        Path("naming_enforcer.py"),  # Included by glob, but EXCLUDED by file exclusion
        Path("tests/test_file.py"),  # Included by directory, but EXCLUDED by glob exclusion
        Path("other_script.py"),     # Included by glob, NOT excluded
        Path("README.md"),           # Included by regex, NOT excluded
        Path("temp.txt"),            # NOT included, NOT excluded
    ]
    
    for test_path in precedence_test_paths:
        is_included = enforcer.include_manager.is_included(test_path)
        is_excluded = enforcer.exclude_manager.is_excluded(test_path)
        
        # Final decision: exclude takes precedence
        final_decision = is_included and not is_excluded
        
        print(f"  {test_path}:")
        print(f"    Include: {is_included}, Exclude: {is_excluded} → Final: {'PROCESS' if final_decision else 'SKIP'}")
    
    # Test 4: Test with no include patterns (should include everything)
    print("\n4. Testing default behavior (no include patterns):")
    enforcer_default = NamingEnforcerV2(standard_path)
    
    default_test_paths = [
        Path("any_file.txt"),
        Path("any_script.py"),
        Path("any_doc.md")
    ]
    
    for test_path in default_test_paths:
        is_included = enforcer_default.include_manager.is_included(test_path)
        print(f"  {test_path}: {'INCLUDED' if is_included else 'excluded'} (default: include all)")
    
    print("\n✅ Include functionality test completed!")

if __name__ == "__main__":
    test_include_functionality() 