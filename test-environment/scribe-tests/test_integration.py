"""
Integration tests for the Scribe Engine event flow.

These tests verify that the complete event pipeline works correctly
from file system events through to worker processing.
"""

import unittest
import tempfile
import os
import time
import threading
from pathlib import Path
import json

from tools.scribe.engine import ScribeEngine
from tools.scribe.core.config_manager import ConfigManager

# Helper function from test_full_pipeline
def create_temp_config_file(rules, plugin_dirs, security_settings=None):
    if security_settings is None:
        security_settings = {"allowed_commands": [], "restricted_paths": []}
    
    config_data = {
        "config_version": "1.0",
        "engine_settings": {
            "log_level": "INFO",
            "quarantine_path": os.path.join(tempfile.gettempdir(), "scribe_quarantine_test"),
            "pause_file": os.path.join(tempfile.gettempdir(), "scribe_pause_test"),
        },
        "plugins": {
            "directories": plugin_dirs,
            "auto_reload": False,
            "load_order": plugin_dirs
        },
        "security": security_settings,
        "rules": rules,
    }
    
    temp_config = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
    json.dump(config_data, temp_config)
    temp_config.close()
    return temp_config.name

class TestEventFlowIntegration(unittest.TestCase):
    """Test the complete event flow from file system to action execution."""

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.watch_dir = Path(self.test_dir.name)
        
        # Create a dummy plugin, as the engine requires at least one.
        plugin_dir = self.watch_dir / "test_plugins"
        plugin_dir.mkdir()
        with open(plugin_dir / "dummy_action.py", "w") as f:
            f.write(
                "from tools.scribe.actions.base import BaseAction\n"
                "class DummyAction(BaseAction):\n"
                "    def execute(self, content, match, path, params):\n"
                "        return content + ' processed'"
            )
        with open(plugin_dir / "__init__.py", "w") as f:
            pass

        # Create a config file that points to our test directories
        self.rules = [{
            "id": "RULE-999", "name": "DummyRule", "enabled": True, 
            "file_glob": "*.txt", "trigger_pattern": "initial",
            "actions": [{"type": "dummyaction", "params": {}}]
        }]
        self.config_file_path = create_temp_config_file(self.rules, [str(plugin_dir)])
        
        # We need to ensure the ScribeEngine uses this config.
        # We'll patch ConfigManager's default path for the duration of the test.
        self._original_default_path = ConfigManager.DEFAULT_CONFIG_PATH
        ConfigManager.DEFAULT_CONFIG_PATH = self.config_file_path
        
        self.engine = ScribeEngine(
            watch_paths=[str(self.watch_dir)],
            file_patterns=['*.txt']
        )
        self.engine_thread = None

    def tearDown(self):
        if self.engine_thread and self.engine_thread.is_alive():
            self.engine.stop()
            self.engine_thread.join(timeout=5)
        os.remove(self.config_file_path)
        self.test_dir.cleanup()
        # Restore the original default config path
        ConfigManager.DEFAULT_CONFIG_PATH = self._original_default_path

    def _start_engine_in_thread(self):
        self.engine_thread = threading.Thread(target=self.engine.run_forever, daemon=True)
        self.engine_thread.start()
        time.sleep(0.5) # Give engine time to initialize
        self.assertTrue(self.engine.is_running)

    def test_file_creation_event_flow(self):
        """Test that a file creation triggers the rule and action."""
        self._start_engine_in_thread()
        
        test_file = self.watch_dir / "test_create.txt"
        test_file.write_text("initial content")
        
        time.sleep(1.0) # Allow time for event processing
        
        # Verify the file was modified by the dummy action
        final_content = test_file.read_text()
        self.assertEqual(final_content, "initial content processed")

    def test_file_modification_event_flow(self):
        """Test that a file modification triggers the rule and action."""
        test_file = self.watch_dir / "test_modify.txt"
        test_file.write_text("other content") # Write before starting engine

        self._start_engine_in_thread()
        
        # Modify the file to trigger the rule
        test_file.write_text("initial content to trigger rule")
        time.sleep(1.0)
        
        final_content = test_file.read_text()
        self.assertEqual(final_content, "initial content to trigger rule processed")

    def test_non_matching_files_ignored(self):
        """Test that files not matching the glob pattern are ignored."""
        self._start_engine_in_thread()
        
        test_file = self.watch_dir / "ignored_file.md" # .md doesn't match *.txt
        initial_content = "This should not be processed."
        test_file.write_text(initial_content)
        
        time.sleep(1.0)
        
        final_content = test_file.read_text()
        self.assertEqual(final_content, initial_content)

    def test_engine_startup_and_shutdown(self):
        """Test that the engine starts and stops correctly."""
        self.assertFalse(self.engine.is_running)
        self._start_engine_in_thread()
        self.assertTrue(self.engine.is_running)
        
        # Stop is called in tearDown, let's just check the state after
        self.engine.stop()
        self.engine_thread.join(timeout=2)
        
        self.assertFalse(self.engine.is_running)

if __name__ == '__main__':
    unittest.main() 