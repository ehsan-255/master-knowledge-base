#!/usr/bin/env python3
"""
Manual test for SecurityManager list-based command execution.
"""

import sys
from pathlib import Path

# Add the scribe module to the path
# Import scribe modules using the installed package

from core.security_manager import SecurityManager
from unittest.mock import Mock

def main():
    print("🧪 Manual SecurityManager Test")
    print("=" * 40)
    
    # Create mock config manager
    mock_config = Mock()
    mock_config.get_security_settings.return_value = {
        'allowed_commands': ['git', 'echo'],
        'restricted_paths': [],
        'dangerous_patterns': []
    }
    
    # Create SecurityManager
    sm = SecurityManager(mock_config)
    
    try:
        # Test 1: List-based command (this should work)
        print("\n📋 Test 1: List-based command execution")
        try:
            success, stdout, stderr = sm.execute_command_safely(['echo', 'hello world'])
            print(f'✅ SUCCESS: success={success}, stdout="{stdout.strip()}"')
        except Exception as e:
            print(f'❌ FAILED: {e}')
        
        # Test 2: Empty list (this should fail)
        print("\n📋 Test 2: Empty command list (should fail)")
        try:
            sm.execute_command_safely([])
            print('❌ FAILED: Empty list should have raised exception')
        except Exception as e:
            print(f'✅ SUCCESS: Correctly raised {type(e).__name__}: {e}')
        
        # Test 3: Invalid command (should fail)
        print("\n📋 Test 3: Invalid command (should fail)")
        try:
            sm.execute_command_safely(['rm', '-rf', '/'])
            print('❌ FAILED: Invalid command should have raised exception')
        except Exception as e:
            print(f'✅ SUCCESS: Correctly raised {type(e).__name__}: {e}')
        
        print("\n🎉 All manual tests completed successfully!")
        
    finally:
        sm.stop()

if __name__ == '__main__':
    main() 