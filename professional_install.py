#!/usr/bin/env python3
"""
Professional installation script for Scribe with clean build environment
"""

import subprocess
import sys
import os

def professional_install():
    """Perform professional installation with clean build environment."""
    print('=== PROFESSIONAL CLEAN INSTALLATION ===')
    print(f'Python: {sys.version}')
    print(f'Executable: {sys.executable}')
    print()
    
    # Change to scribe directory
    scribe_dir = r"C:\Users\E L I A N A\Downloads\_apmdd_vault\master-knowledge-base\tools\scribe"
    print(f'Working directory: {scribe_dir}')
    os.chdir(scribe_dir)
    
    # Clean installation with verbose output
    cmd = [
        sys.executable, '-m', 'pip', 'install', 
        '-e', '.', 
        '--no-cache-dir', 
        '--force-reinstall', 
        '--verbose',
        '--no-build-isolation'  # Disable build isolation to use current environment
    ]
    
    print(f'Command: {" ".join(cmd)}')
    print('='*60)
    
    try:
        # Run with real-time output
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True
        )
        
        # Print output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        rc = process.poll()
        print('='*60)
        print(f'Installation completed with return code: {rc}')
        
        if rc == 0:
            print('✅ INSTALLATION SUCCESSFUL')
            
            # Test the installation
            print('\nTesting installation...')
            try:
                import scribe
                print(f'✅ Scribe imported successfully from: {scribe.__file__}')
            except ImportError as e:
                print(f'❌ Import test failed: {e}')
        else:
            print('❌ INSTALLATION FAILED')
            
    except Exception as e:
        print(f'Installation error: {e}')

if __name__ == "__main__":
    professional_install()