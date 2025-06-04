#!/usr/bin/env python3
"""
Quick test to verify the new exclusion patterns work correctly
"""

from pathlib import Path
from naming_enforcer import NamingEnforcerV2

def test_new_exclusions():
    print("Testing new exclusion patterns:")
    print("=" * 40)
    
    enforcer = NamingEnforcerV2()
    
    # Test paths that should be excluded
    test_paths = [
        Path('.git'),                                    # Hidden directory
        Path('.vscode'),                                 # Hidden directory
        Path('./archive'),                               # Archive directory
        Path('src/__pycache__'),                         # Python cache
        Path('deep/nested/__pycache__/file.pyc'),        # Nested Python cache
        Path('master-knowledge-base/tools/reports'),     # Reports directory
        Path('master-knowledge-base/tools/reports/file.txt'),  # File in reports
        Path('dist'),                                    # Should NOT be excluded (removed)
        Path('regular_file.py'),                         # Should NOT be excluded
    ]
    
    for test_path in test_paths:
        is_excluded = enforcer.exclude_manager.is_excluded(test_path)
        status = "EXCLUDED" if is_excluded else "included"
        print(f"  {test_path}: {status}")
    
    print("\n✅ Exclusion pattern test completed!")

if __name__ == "__main__":
    test_new_exclusions() 