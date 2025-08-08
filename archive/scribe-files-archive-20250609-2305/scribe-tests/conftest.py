import pytest
import sys
from pathlib import Path

@pytest.fixture(scope="session", autouse=True)
def configure_python_path():
    """
    Adds the project's root directory to the Python path to resolve imports
    during testing. This enables imports from tools.scribe.* modules.
    """
    repo_root = Path(__file__).parent.parent.parent
    tools_scribe_parent = repo_root  # Since tools is in repo root
    tools_scribe_path = repo_root / "tools" / "scribe"
    
    # Add both the repo root and the scribe directory to the path
    for path in [str(tools_scribe_parent), str(tools_scribe_path)]:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"Added to Python path: {tools_scribe_parent}, {tools_scribe_path}")
    print(f"Current sys.path: {sys.path[:4]}")  # Show first 4 entries 