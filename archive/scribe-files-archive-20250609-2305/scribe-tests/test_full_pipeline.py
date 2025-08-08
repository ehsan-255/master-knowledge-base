import unittest
import tempfile
import os
import time
import threading
import queue
import json
from pathlib import Path

# Scribe components
from tools.scribe.worker import Worker
from tools.scribe.core.config_manager import ConfigManager
from tools.scribe.core.event_bus import EventBus

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

def create_dummy_action_plugin(plugin_dir, action_name="append_text_action"):
    os.makedirs(plugin_dir, exist_ok=True)
    action_file_content = f'''
import re
from tools.scribe.actions.base import BaseAction

class {action_name.capitalize().replace("_", "")}(BaseAction):
    def execute(self, file_content: str, match: re.Match, file_path: str, params: dict) -> str:
        text_to_append = params.get("text_to_append", " Scribe was here!")
        self.logger.info(f"Dummy action '{{self.action_type}}' executing: appending text to file {{file_path}}.")
        return file_content + text_to_append
'''
    with open(os.path.join(plugin_dir, f"{action_name}.py"), "w") as f:
        f.write(action_file_content)
    with open(os.path.join(plugin_dir, "__init__.py"), "w") as f:
        pass

class TestFullPipeline(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.watch_dir = Path(self.test_dir.name) / "watched_folder"
        self.watch_dir.mkdir()

        self.test_file_path = self.watch_dir / "test_file.txt"
        with open(self.test_file_path, "w") as f:
            f.write("Initial content.")

        self.plugin_dir = Path(self.test_dir.name) / "test_plugins"
        create_dummy_action_plugin(str(self.plugin_dir), "append_text_action")
        
        # Determine the absolute path to the 'actions' directory relative to this test file.
        # This assumes the test file is in 'test-environment/scribe-tests'.
        self.repo_root = Path(__file__).parent.parent.parent
        self.real_actions_dir = str(self.repo_root / 'tools' / 'scribe' / 'actions')

        self.rules = [{
            "id": "RULE-001",
            "name": "AppendScribeTest",
            "enabled": True,
            "file_glob": "*.txt",
            "trigger_pattern": "Initial content",
            "actions": [{
                "type": "appendtextaction",
                "params": {"text_to_append": " Scribe test successful!"}
            }]
        }]
        
        self.security_settings = {"allowed_commands": ["python"], "restricted_paths": []}
        
        self.config_file_path = create_temp_config_file(
            self.rules, 
            [str(self.plugin_dir)], 
            self.security_settings
        )

        self.event_bus = EventBus()
        self.shutdown_event = threading.Event()
        
        # Instantiate ConfigManager correctly without patching
        self.config_manager = ConfigManager(config_path=self.config_file_path, auto_reload=False)
        
        # Instantiate Worker with HMA-compliant components
        self.worker = Worker(
            event_bus=self.event_bus,
            shutdown_event=self.shutdown_event,
            config_manager=self.config_manager  # Pass the real ConfigManager
        )
        
        # Ensure the worker's plugin loader loads from our test directories
        self.worker.plugin_loader.plugin_directories = [self.plugin_dir, Path(self.real_actions_dir)]
        self.worker.plugin_loader.load_all_plugins()

    def tearDown(self):
        self.shutdown_event.set()
        if hasattr(self, 'worker_thread') and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1)
        os.remove(self.config_file_path)
        self.test_dir.cleanup()

    def test_file_modification_triggers_action(self):
        # Start the worker in a separate thread
        self.worker_thread = threading.Thread(target=self.worker.run, daemon=True)
        self.worker_thread.start()

        # Simulate a file event being published to the event bus
        event_data = {
            'event_id': 'test-event-123',
            'type': 'modified',
            'file_path': str(self.test_file_path),
            'timestamp': time.time()
        }
        self.event_bus.publish('file_event', event_data)

        # Allow time for the worker to process the event
        time.sleep(0.5)

        # Check the content of the test file
        with open(self.test_file_path, "r") as f:
            content_after = f.read()

        expected_content = "Initial content. Scribe test successful!"
        self.assertEqual(content_after, expected_content)
        self.assertGreaterEqual(self.worker.events_processed, 1)

    def test_security_manager_scrubs_environment(self):
        """
        Tests the SecurityManager's environment scrubbing directly.
        """
        # Get the security manager from the worker
        security_manager = self.worker.security_manager
        
        # Prepare test environment
        os.environ["SCRIBE_ALLOWED_VAR"] = "scribe_rocks"
        os.environ["SCRIBE_SECRET_VAR"] = "super_secret"
        
        # Test case 1: Allow specific variable
        allowed_vars = ["SCRIBE_ALLOWED_VAR", "PATH"]
        safe_env = security_manager.scrub_environment(allowed_env_vars=allowed_vars)
        
        self.assertIn("SCRIBE_ALLOWED_VAR", safe_env)
        self.assertEqual(safe_env["SCRIBE_ALLOWED_VAR"], "scribe_rocks")
        self.assertNotIn("SCRIBE_SECRET_VAR", safe_env)
        self.assertIn("PATH", safe_env) # Should be passed through
        
        # Test case 2: No allowed variables (should get minimal safe env)
        minimal_env = security_manager.scrub_environment(allowed_env_vars=None)
        self.assertNotIn("SCRIBE_ALLOWED_VAR", minimal_env)
        self.assertNotIn("SCRIBE_SECRET_VAR", minimal_env)
        self.assertIn("PATH", minimal_env) # Should have safe default
        self.assertEqual(minimal_env["PATH"], "/usr/bin:/bin")

        # Cleanup environment
        del os.environ["SCRIBE_ALLOWED_VAR"]
        del os.environ["SCRIBE_SECRET_VAR"]

if __name__ == "__main__":
    unittest.main()
