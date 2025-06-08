#!/usr/bin/env python3
"""
Test script for the exclude functionality of the naming enforcer
"""

import sys
from pathlib import Path
from naming_enforcer import NamingEnforcerV2

def test_exclude_functionality():
    """Test various exclude patterns"""
    print("Testing Naming Enforcer Exclude Functionality")
    print("=" * 50)
    
    # Initialize enforcer with correct path
    standard_path = "../../standards/src/GM-CONVENTIONS-NAMING.md"
    enforcer = NamingEnforcerV2(standard_path)
    
    # Test 1: Add individual exclusions
    print("\n1. Testing individual exclusions:")
    enforcer.exclude_manager.add_exclude_file("temp.txt", "Test file exclusion")
    enforcer.exclude_manager.add_exclude_directory("build", "Test directory exclusion")
    enforcer.exclude_manager.add_exclude_glob("*.tmp", "Test glob exclusion")
    enforcer.exclude_manager.add_exclude_regex(r".*_test\.py$", "Test regex exclusion")
    
    print(enforcer.exclude_manager.get_exclusion_summary())
    
    # Test 2: Test exclusion logic
    print("\n2. Testing exclusion logic:")
    test_paths = [
        Path("temp.txt"),
        Path("build/output.txt"),
        Path("file.tmp"),
        Path("my_test.py"),
        Path("normal_file.py"),
        Path("regular.md")
    ]
    
    for test_path in test_paths:
        is_excluded = enforcer.exclude_manager.is_excluded(test_path)
        print(f"  {test_path}: {'EXCLUDED' if is_excluded else 'included'}")
    
    # Test 3: Load from file
    print("\n3. Testing exclude file loading:")
    try:
        # Create a fresh enforcer to test file loading
        enforcer2 = NamingEnforcerV2(standard_path)
        enforcer2.exclude_manager.load_exclude_file("example-excludes.txt")
        print("Successfully loaded exclude file")
        print(f"Total patterns: {len(enforcer2.exclude_manager.exclude_patterns)}")
        
        # Test some patterns from the file
        test_file_paths = [
            Path("backup.md"),
            Path("__pycache__/test.pyc"),
            Path("file.backup"),
            Path("temp_data.json"),
            Path("normal.py")
        ]
        
        print("\n  Testing patterns from exclude file:")
        for test_path in test_file_paths:
            is_excluded = enforcer2.exclude_manager.is_excluded(test_path)
            print(f"    {test_path}: {'EXCLUDED' if is_excluded else 'included'}")
            
    except Exception as e:
        print(f"Error loading exclude file: {e}")
    
    print("\n✅ Exclude functionality test completed!")

if __name__ == "__main__":
    test_exclude_functionality() 