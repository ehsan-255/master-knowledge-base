import pytest
import sys
from pathlib import Path

def main():
    """
    Runs the Scribe test suite with the correct Python path configuration.
    This script ensures that the 'tools' directory is added to the Python path
    before running the tests, which is essential for resolving module imports.
    """
    # Add the 'tools' directory to the Python path
    repo_root = Path(__file__).parent.parent
    tools_dir = repo_root / 'tools'
    
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    
    # Also add the root for general imports if needed
    if str(repo_root) not in sys.path:
        sys.path.insert(1, str(repo_root))

    # Define the path to the test directory
    test_dir = str(Path(__file__).parent / 'scribe-tests')
    
    # Run pytest
    exit_code = pytest.main([test_dir])
    
    # Exit with the same code as pytest
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 