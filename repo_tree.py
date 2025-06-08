#!/usr/bin/env python3
"""
Repository Tree Generator - Quick Runner

Simple script to regenerate the repository tree structure.
Executes the main tree generator script and provides feedback.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the repository tree generator."""
    print("🎯🚀 Repository Tree Generator")
    print("=" * 50)
    
    # Path to the main generator script in the new location
    script_path = Path("tools/utilities/repo-tree/main_repo_tree.py")
    
    if not script_path.exists():
        print("❌ Error: Generator script not found!")
        print(f"   Expected: {script_path}")
        return 1
    
    try:
        # Run the generator script
        result = subprocess.run([
            sys.executable, str(script_path)
        ], capture_output=True, text=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print("\n✅ Repository tree updated successfully!")
            print("📍 Output: repo-tree.md")
        else:
            print(f"\n❌ Script failed with exit code: {result.returncode}")
            return result.returncode
            
    except Exception as e:
        print(f"❌ Error running generator: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 