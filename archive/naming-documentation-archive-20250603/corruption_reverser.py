#!/usr/bin/env python3
"""
Corruption Reverser - Undo damage from naming enforcer

This script reverses the corruption caused by the aggressive naming enforcer
by changing kebab-case back to snake_case where it broke the system.
"""

import os
import re
from pathlib import Path

# Critical patterns that need to be reversed
CRITICAL_REVERSALS = {
    # Python code corruption
    'standards_index': 'standards_index',
    '_load_standards_index': '_load_standards_index', 
    'config.standards_index': 'config.standards_index',
    
    # Frontmatter field corruption
    'standard_id:': 'standard_id:',
    'primary_domain:': 'primary_domain:',
    'sub_domain:': 'sub_domain:',
    'scope_application:': 'scope_application:',
    'lifecycle_gatekeeper:': 'lifecycle_gatekeeper:',
    'impact_areas:': 'impact_areas:',
    'change_log_url:': 'change_log_url:',
    
    # Config path corruption
    'naming_exceptions.json': 'naming_exceptions.json',
}

def reverse_file_corruption(file_path: Path) -> bool:
    """Reverse corruption in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # Apply all critical reversals
        for corrupted, original in CRITICAL_REVERSALS.items():
            if corrupted in content:
                content = content.replace(corrupted, original)
                changes_made += content.count(original) - original_content.count(original)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ FIXED: {file_path} ({changes_made} reversals)")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {file_path}: {e}")
        return False

def reverse_directory_corruption(base_path: Path) -> int:
    """Reverse corruption in all files in directory tree"""
    fixed_count = 0
    
    # Scan all text files
    for root, dirs, files in os.walk(base_path):
        # Skip excluded directories
        if any(exclude in root for exclude in ['.git', '__pycache__', 'node_modules']):
            continue
            
        for file in files:
            if file.endswith(('.py', '.json', '.md', '.yaml', '.yml', '.txt')):
                file_path = Path(root) / file
                if reverse_file_corruption(file_path):
                    fixed_count += 1
    
    return fixed_count

def main():
    """Main reversal process"""
    print("🔄 CORRUPTION REVERSER: Undoing naming enforcer damage...")
    print("=" * 60)
    
    # Start from current directory (tools) and go up to scan everything
    base_path = Path('..').resolve()
    print(f"Scanning: {base_path}")
    
    fixed_count = reverse_directory_corruption(base_path)
    
    print("=" * 60)
    print(f"🎉 REVERSAL COMPLETE: Fixed {fixed_count} files")
    
    if fixed_count > 0:
        print("\n✅ Critical system corruption has been reversed!")
        print("✅ Python syntax should now be valid")
        print("✅ Frontmatter fields restored to expected format")
        print("✅ Tools should be functional again")
    else:
        print("\n ℹ️  No corruption found to reverse")

if __name__ == "__main__":
    main() 