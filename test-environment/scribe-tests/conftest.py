import pytest
import sys
from pathlib import Path

@pytest.fixture(scope="session", autouse=True)
def configure_python_path():
    """
    Adds the project's 'scribe' directory to the Python path to resolve imports
    during testing. This is a pytest best practice for handling test discovery
    and module imports in complex project structures.
    """
    repo_root = Path(__file__).parent.parent.parent
    scribe_dir = repo_root / 'scribe'
    
    if str(scribe_dir) not in sys.path:
        sys.path.insert(0, str(scribe_dir))
    
    # Also add the root for general imports if needed, though 'scribe' is more specific
    if str(repo_root) not in sys.path:
        sys.path.insert(1, str(repo_root)) 