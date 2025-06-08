#!/usr/bin/env python3
"""
Test script for the automatic file loading functionality (.namingignore and .naminginclude)
"""

import sys
import tempfile
import shutil
from pathlib import Path
from naming_enforcer import NamingEnforcerV2

def test_automatic_file_loading():
    """Test automatic loading of .namingignore and .naminginclude files"""
    print("Testing Automatic File Loading Functionality")
    print("=" * 50)
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Test 1: No automatic files
        print("\n1. Testing with no automatic files:")
        standard_path = Path("../../standards/src/GM-CONVENTIONS-NAMING.md").resolve()
        enforcer1 = NamingEnforcerV2(str(standard_path))
        print(f"Include patterns: {len(enforcer1.include_manager.include_patterns)}")
        print(f"Exclude patterns: {len(enforcer1.exclude_manager.exclude_patterns)}")
        
        # Test 2: Create automatic files in temp directory
        print("\n2. Testing with automatic files:")
        
        # Create .namingignore file
        namingignore_content = """# Test .namingignore file
*.tmp
*.bak
build/
test_*
"""
        (temp_path / ".namingignore").write_text(namingignore_content)
        
        # Create .naminginclude file
        naminginclude_content = """# Test .naminginclude file
*.py
*.md
src/
docs/
"""
        (temp_path / ".naminginclude").write_text(naminginclude_content)
        
        # Change to temp directory and create enforcer
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(temp_path)
            
            enforcer2 = NamingEnforcerV2(str(standard_path))
            print(f"Include patterns: {len(enforcer2.include_manager.include_patterns)}")
            print(f"Exclude patterns: {len(enforcer2.exclude_manager.exclude_patterns)}")
            
            # Test 3: Test pattern matching
            print("\n3. Testing pattern matching from automatic files:")
            test_paths = [
                Path("script.py"),      # Should be included
                Path("readme.md"),      # Should be included  
                Path("temp.tmp"),       # Should be excluded
                Path("backup.bak"),     # Should be excluded
                Path("src/main.py"),    # Should be included (directory + file)
                Path("build/output"),   # Should be excluded (directory)
                Path("test_file.py"),   # Should be excluded (test pattern)
                Path("other.txt"),      # Should NOT be included (not in include patterns)
            ]
            
            for test_path in test_paths:
                is_included = enforcer2.include_manager.is_included(test_path)
                is_excluded = enforcer2.exclude_manager.is_excluded(test_path)
                final_decision = is_included and not is_excluded
                
                print(f"  {test_path}:")
                print(f"    Include: {is_included}, Exclude: {is_excluded} → Final: {'PROCESS' if final_decision else 'SKIP'}")
            
        finally:
            os.chdir(original_cwd)
        
        # Test 4: Test reload functionality with different directory
        print("\n4. Testing reload functionality:")
        
        # Create another temp directory with different patterns
        with tempfile.TemporaryDirectory() as temp_dir2:
            temp_path2 = Path(temp_dir2)
            
            # Create different automatic files
            namingignore_content2 = """# Different .namingignore file
*.log
cache/
"""
            (temp_path2 / ".namingignore").write_text(namingignore_content2)
            
            naminginclude_content2 = """# Different .naminginclude file
*.js
*.css
web/
"""
            (temp_path2 / ".naminginclude").write_text(naminginclude_content2)
            
            # Test reload from different directory
            print(f"Before reload - Include patterns: {len(enforcer2.include_manager.include_patterns)}")
            print(f"Before reload - Exclude patterns: {len(enforcer2.exclude_manager.exclude_patterns)}")
            
            enforcer2.reload_automatic_files(temp_path2)
            
            print(f"After reload - Include patterns: {len(enforcer2.include_manager.include_patterns)}")
            print(f"After reload - Exclude patterns: {len(enforcer2.exclude_manager.exclude_patterns)}")
            
            # Test new patterns
            test_paths2 = [
                Path("script.js"),      # Should be included (new pattern)
                Path("style.css"),      # Should be included (new pattern)
                Path("app.log"),        # Should be excluded (new pattern)
                Path("cache/data"),     # Should be excluded (new pattern)
                Path("script.py"),      # Should still be included (old pattern)
            ]
            
            print("\n   Testing new patterns:")
            for test_path in test_paths2:
                is_included = enforcer2.include_manager.is_included(test_path)
                is_excluded = enforcer2.exclude_manager.is_excluded(test_path)
                final_decision = is_included and not is_excluded
                
                print(f"    {test_path}: {'PROCESS' if final_decision else 'SKIP'}")
    
    print("\n✅ Automatic file loading test completed!")

def test_command_line_combination():
    """Test that automatic files work with command line options"""
    print("\n" + "=" * 50)
    print("Testing Command Line Combination")
    print("=" * 50)
    
    # This test would require running the actual command line interface
    # For now, we'll test the programmatic interface
    
    standard_path = Path("../../standards/src/GM-CONVENTIONS-NAMING.md").resolve()
    enforcer = NamingEnforcerV2(str(standard_path))
    
    # Add some command line style patterns
    enforcer.include_manager.add_include_glob("*.html", "CLI include")
    enforcer.exclude_manager.add_exclude_file("specific.py", "CLI exclude")
    
    print(f"Total include patterns: {len(enforcer.include_manager.include_patterns)}")
    print(f"Total exclude patterns: {len(enforcer.exclude_manager.exclude_patterns)}")
    
    # Test that both automatic and CLI patterns work
    test_paths = [
        Path("page.html"),      # Should be included (CLI pattern)
        Path("script.py"),      # Should be included (automatic pattern)
        Path("specific.py"),    # Should be excluded (CLI pattern)
        Path("temp.tmp"),       # Should be excluded (automatic pattern)
    ]
    
    print("\nTesting combined patterns:")
    for test_path in test_paths:
        is_included = enforcer.include_manager.is_included(test_path)
        is_excluded = enforcer.exclude_manager.is_excluded(test_path)
        final_decision = is_included and not is_excluded
        
        print(f"  {test_path}: {'PROCESS' if final_decision else 'SKIP'}")
    
    print("\n✅ Command line combination test completed!")

if __name__ == "__main__":
    test_automatic_file_loading()
    test_command_line_combination() 