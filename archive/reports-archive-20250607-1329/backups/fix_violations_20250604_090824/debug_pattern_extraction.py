#!/usr/bin/env python3
"""
Debug script to investigate naming enforcer pattern extraction issues
"""

import sys
import re
from pathlib import Path

# Add the naming enforcer to path
sys.path.append('.')

from naming_enforcer import NamingStandardParser, NamingEnforcerV2

def debug_pattern_extraction():
    """Debug the pattern extraction process"""
    print("=== DEBUGGING NAMING ENFORCER PATTERN EXTRACTION ===\n")
    
    # Initialize parser
    print("1. Initializing NamingStandardParser...")
    parser = NamingStandardParser()
    
    # Check if standard file exists
    standard_path = Path(parser.standard_path)
    print(f"   Standard path: {standard_path}")
    print(f"   File exists: {standard_path.exists()}")
    
    if not standard_path.exists():
        print("   ERROR: Standard file not found!")
        return
    
    # Load and parse
    print("\n2. Loading and parsing standard document...")
    try:
        parser.load_and_parse()
        print("   ✓ Successfully loaded and parsed")
    except Exception as e:
        print(f"   ✗ Error during load_and_parse: {e}")
        return
    
    # Check extracted patterns
    print("\n3. Extracted patterns:")
    for context, pattern in parser.patterns.items():
        print(f"   {context}: {pattern}")
    
    # Check if standard_ids pattern exists
    print(f"\n4. Standard IDs pattern check:")
    standard_ids_pattern = parser.patterns.get('standard_ids')
    if standard_ids_pattern:
        print(f"   ✓ Found: {standard_ids_pattern}")
        
        # Test the pattern against known Standard IDs
        test_cases = [
            "GM-CONVENTIONS-NAMING",
            "MT-SCHEMA-FRONTMATTER", 
            "AS-STRUCTURE-KB-ROOT",
            "SF-FORMATTING-MARKDOWN-GENERAL",
            "my-document",  # Should NOT match
            "test-file"     # Should NOT match
        ]
        
        print("   Testing pattern against known cases:")
        compiled_pattern = re.compile(standard_ids_pattern)
        for test_case in test_cases:
            matches = bool(compiled_pattern.match(test_case))
            status = "✓" if matches else "✗"
            print(f"     {status} {test_case}: {matches}")
    else:
        print("   ✗ Standard IDs pattern NOT FOUND!")
    
    # Check protected names
    print(f"\n5. Protected names categories:")
    for category, names in parser.protected_names.items():
        print(f"   {category}: {len(names)} items")
        if len(names) <= 10:
            print(f"     Items: {list(names)}")
        else:
            print(f"     Sample: {list(names)[:5]}...")
    
    # Check standard ID prefixes
    print(f"\n6. Standard ID prefixes:")
    print(f"   Found: {parser.standard_id_prefixes}")
    
    # Check exceptions
    print(f"\n7. Exception patterns:")
    for category, patterns in parser.exceptions.items():
        print(f"   {category}: {patterns}")

def test_specific_files():
    """Test specific files that should be protected"""
    print("\n=== TESTING SPECIFIC FILE PROTECTION ===\n")
    
    # Initialize enforcer
    enforcer = NamingEnforcerV2()
    
    test_files = [
        "GM-CONVENTIONS-NAMING.md",
        "MT-SCHEMA-FRONTMATTER.md",
        "AS-STRUCTURE-KB-ROOT.md",
        "registry-schema.yaml",
        "naming_enforcer.py",
        "my-document.md",  # Should be flagged
        "TestFile.md"      # Should be flagged
    ]
    
    print("Testing file validation:")
    for filename in test_files:
        file_path = Path(filename)
        
        # Test if it's an exception
        is_exception = enforcer.parser.is_exception(file_path)
        
        # Test if it's a protected name
        base_name = file_path.stem
        is_protected = enforcer.parser.is_protected_name(base_name)
        
        # Test context detection
        context = enforcer.get_context_for_path(file_path)
        
        # Test validation
        violation = enforcer.validate_file_name(file_path)
        
        print(f"\n  File: {filename}")
        print(f"    Exception: {is_exception}")
        print(f"    Protected: {is_protected}")
        print(f"    Context: {context}")
        print(f"    Violation: {'None' if violation is None else violation.violation_type}")

def debug_standard_id_detection():
    """Debug why Standard ID detection is failing"""
    print("\n=== DEBUGGING STANDARD ID DETECTION ===\n")
    
    parser = NamingStandardParser()
    parser.load_and_parse()
    
    # Check the extract_context_patterns method
    print("1. Checking extract_context_patterns method...")
    
    # Look for Standard ID pattern in the raw content
    print("2. Searching for Standard ID pattern in raw content...")
    
    # Search for the pattern definition
    pattern_matches = re.findall(r'### 1\.5 Standard IDs.*?Pattern.*?`([^`]+)`', parser.raw_content, re.DOTALL)
    print(f"   Found pattern matches: {pattern_matches}")
    
    # Search for examples
    example_matches = re.findall(r'### 1\.5 Standard IDs.*?Examples.*?`([^`]+)`', parser.raw_content, re.DOTALL)
    print(f"   Found example matches: {example_matches}")
    
    # Check what the extract_context_patterns method actually extracts
    print("3. Re-running extract_context_patterns...")
    parser.patterns = {}  # Reset
    parser.extract_context_patterns()
    
    print(f"   Patterns after extraction: {parser.patterns}")

if __name__ == "__main__":
    debug_pattern_extraction()
    test_specific_files()
    debug_standard_id_detection() 