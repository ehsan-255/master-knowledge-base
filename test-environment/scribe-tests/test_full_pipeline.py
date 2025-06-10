import unittest
import tempfile
import os
import time
import threading
import queue # Add this import
import json # For config files
from pathlib import Path # For path manipulation in tests

# Assuming Scribe engine components are accessible.
# Adjust imports based on the actual location if Scribe is a package or paths need adjustment.
# This might require adding `tools` to sys.path or making Scribe installable.
from tools.scribe.engine import ScribeEngine
from tools.scribe.watcher import Watcher # Needed to simulate events or direct call to worker
from tools.scribe.worker import Worker
from tools.scribe.core.config_manager import ConfigManager # For creating test config

# Helper function to create a temporary config file for Scribe
def create_temp_config_file(rules, plugin_dirs, security_settings=None): # Added security_settings
    # Basic valid structure according to config.schema.json
    if security_settings is None:
        security_settings = {
            "allowed_commands": [], # Default to empty if not provided
            "restricted_paths": []
        }
    config_data = {
        "config_version": "1.0",
        "engine_settings": {
            "log_level": "INFO",
            "quarantine_path": os.path.join(tempfile.gettempdir(), "scribe_quarantine_test"),
            "pause_file": os.path.join(tempfile.gettempdir(), "scribe_pause_test"),
        },
        "security": security_settings, # Use provided or default security_settings
        "rules": rules, # Rules structure also needs to match schema
        # "plugin_directories": plugin_dirs, # This key is not allowed by schema at root
        # We will need to find another way to tell PluginLoader where to find test plugins.
        # This might involve patching self.worker.config_manager.get_plugin_directories() later in setUp.
    }
    temp_config = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
    json.dump(config_data, temp_config)
    temp_config.close()
    return temp_config.name

# Helper function to create a dummy action plugin file
def create_dummy_action_plugin(plugin_dir, action_name="append_text_action"):
    os.makedirs(plugin_dir, exist_ok=True)
    action_file_content = f'''
import re # Required for re.Match type hint
from tools.scribe.actions.base import BaseAction

class {action_name.capitalize().replace("_", "")}(BaseAction): # e.g., Appendtextaction
    # Signature must match BaseAction.execute
    def execute(self, file_content: str, match: re.Match, file_path: str, params: dict) -> str:
        # Get text_to_append from params passed into execute method
        text_to_append = params.get("text_to_append", " Scribe was here!")
        # Use self.logger (available from BaseAction) and correct action_name
        # Escape self.action_type for the generated code string
        self.logger.info(f"Dummy action '{{self.action_type}}' executing: appending text to file {{file_path}}.")
        return file_content + text_to_append
'''
    with open(os.path.join(plugin_dir, f"{action_name}.py"), "w") as f:
        f.write(action_file_content)

    # Create __init__.py if it doesn't exist
    with open(os.path.join(plugin_dir, "__init__.py"), "w") as f:
        pass # Empty __init__.py makes it a package


class TestFullPipeline(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.watch_dir = os.path.join(self.test_dir.name, "watched_folder")
        os.makedirs(self.watch_dir, exist_ok=True)

        self.test_file_path = os.path.join(self.watch_dir, "test_file.txt")
        with open(self.test_file_path, "w") as f:
            f.write("Initial content.")

        # Create a dummy plugin directory for our test action
        self.plugin_dir = os.path.join(self.test_dir.name, "test_plugins")
        create_dummy_action_plugin(self.plugin_dir, "append_text_action")

        # Create a temporary Scribe config file
        # Rule structure needs to conform to config.schema.json
        self.rules = [
            {
                "id": "RULE-001", # Required: string, pattern ^RULE-\\d{3}$
                "name": "AppendScribeTest", # Required: string
                "enabled": True, # Required: boolean
                "file_glob": "*.txt", # Required: string (glob syntax)
                "trigger_pattern": "Initial content", # Required: string (regex)
                # "description" is not in schema, "match_patterns" was incorrect.
                "actions": [ # Required: array, minItems: 1
                    {
                        "type": "appendtextaction", # Changed to match how PluginLoader determines it from class name "Appendtextaction"
                        # "name" was incorrect for action identifier.
                        "params": {"text_to_append": " Scribe test successful!"} # Required: object
                    }
                ],
                # "error_handling" is optional
            }
        ]
        # Default security settings for the main test config (used by test_file_modification_triggers_action)
        # Allow "python" here if any other test might use run_command with python, otherwise keep it minimal.
        # For now, let's keep it minimal for the default config.
        default_security_settings = {"allowed_commands": [], "restricted_paths": []}
        self.config_file_path = create_temp_config_file(self.rules, [self.plugin_dir], security_settings=default_security_settings)

        # Initialize Scribe components directly for more controlled testing
        # This avoids running the full engine with watcher threads if possible
        self.event_queue = queue.Queue()
        self.shutdown_event = threading.Event()

        # Create ConfigManager with our temp config file
        # Note: ConfigManager by default loads 'config/config.json'. We need to override this.
        # This might require a change in ConfigManager or a way to pass config path to Worker components
        # For now, let's assume Worker and its sub-components can be initialized with a specific config_path
        # or that we can mock/patch ConfigManager.get_config_file_path() if ScribeEngine is used.

        # Option 1: If ScribeEngine can take a config_path (IDEAL)
        # self.engine = ScribeEngine(config_file_path=self.config_file_path, watch_directory=self.watch_dir)
        # For this test, we'll manually create the worker and simulate event queueing.

        # Patch ConfigManager's __init__ to use our temporary config file
        self.original_config_manager_init = ConfigManager.__init__

        # Patch ConfigManager's __init__ to use our temporary config file and add get_plugin_directories
        self.original_config_manager_init = ConfigManager.__init__

        _test_config_path = self.config_file_path
        _test_plugin_dir_str = str(self.plugin_dir)

        def mocked_config_manager_init(slf, config_path=None, schema_path="config/config.schema.json", auto_reload=True):
            # Call original __init__ with the test config path and auto_reload=False
            self.original_config_manager_init(slf, config_path=_test_config_path, schema_path=schema_path, auto_reload=False)

            # Add get_plugin_directories method to this specific ConfigManager instance (slf)
            # This method should return what Worker expects for PluginLoader.
            # PluginLoader.__init__ expects a single string path.
            slf.get_plugin_directories = lambda: _test_plugin_dir_str
            # Note: If Worker expects a list of directories from get_plugin_directories,
            # then this should return [_test_plugin_dir_str] and Worker should handle the list.
            # For now, assuming Worker passes the result directly to PluginLoader which wants a string.

        ConfigManager.__init__ = mocked_config_manager_init

        # Now, when Worker instantiates ConfigManager, it will be this mocked version.
        # The ConfigManager instance (self.worker.config_manager) will have .get_plugin_directories()
        self.worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.05
        )

        # Worker's internal PluginLoader should now have been initialized with the correct test plugin path.
        # We need to ensure its plugins are loaded.
        self.worker.plugin_loader.load_all_plugins()

        # Worker's ActionDispatcher is initialized using self.plugin_loader.get_actions() or similar.
        # Since plugin_loader is now correctly pointing to test plugins and they are loaded,
        # ActionDispatcher should also be correctly initialized by Worker's __init__.
        # No need to re-initialize action_dispatcher here if Worker's __init__ does it *after* plugin_loader.
        # Worker.__init__ sequence:
        # 1. self.config_manager = ConfigManager() (mocked to have get_plugin_directories, uses test_config)
        # 2. self.plugin_loader = PluginLoader(self.config_manager.get_plugin_directories()) (should get _test_plugin_dir_str)
        # 3. self.action_dispatcher = ActionDispatcher(self.plugin_loader, self.security_manager, self.config_manager)
        # This seems correct. The call to load_all_plugins() above is important.

        # For specific tests that modify os.environ
        self._original_environ = os.environ.copy()
        self.env_dump_file_path = os.path.join(self.watch_dir, "env_dump.json")


    def tearDown(self):
        # Restore original ConfigManager.__init__
        if hasattr(self, 'original_config_manager_init') and self.original_config_manager_init is not None:
             ConfigManager.__init__ = self.original_config_manager_init

        self.shutdown_event.set()
        if hasattr(self, 'worker_thread') and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1)

        # No need for duplicated restore here

        if hasattr(self, 'config_file_path') and os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)

        # Cleanup for env_vars_test config file
        if hasattr(self, 'current_test_config_path_for_env_test') and os.path.exists(self.current_test_config_path_for_env_test):
             os.remove(self.current_test_config_path_for_env_test)

        self.test_dir.cleanup()

        # Clean up environment variables set by tests
        if hasattr(self, '_original_environ'):
            os.environ.clear()
            os.environ.update(self._original_environ)

        # Clean up env_dump file if created by a test
        if hasattr(self, 'env_dump_file_path') and os.path.exists(self.env_dump_file_path):
            try:
                os.remove(self.env_dump_file_path)
            except OSError:
                pass

    def test_file_modification_triggers_action(self):
        # Start the worker in a separate thread
        self.worker_thread = threading.Thread(target=self.worker.run, daemon=True)
        self.worker_thread.start()

        # Simulate a file event being put onto the queue
        # This is what the Watcher component would normally do
        event = {
            'event_type': 'modified', # Or 'created'/'moved' depending on rule
            'file_path': self.test_file_path,
            'timestamp': time.time()
        }
        self.event_queue.put(event)

        # Wait for the worker to process the event
        # This timeout needs to be sufficient for the worker to pick up, process, and write.
        time.sleep(0.5) # Increased sleep time

        # Check the content of the test file
        with open(self.test_file_path, "r") as f:
            content_after = f.read()

        expected_content = "Initial content. Scribe test successful!"
        self.assertEqual(content_after, expected_content,
                         f"File content was not modified as expected. Got: '{content_after}'")

        # Check worker stats (optional, but good for verification)
        self.assertGreaterEqual(self.worker.events_processed, 1, "Worker should have processed at least one event.")
        # Depending on the test, one might also check events_failed, actions_taken etc.

    def test_run_command_allowed_env_vars(self):
        allowed_var_name = "SCRIBE_ALLOWED_VAR"
        allowed_var_value = "scribe_rocks"
        disallowed_var_name = "SCRIBE_SECRET_VAR"
        disallowed_var_value = "super_secret"

        # Set env vars for the current test process, to be picked up by os.environ
        os.environ[allowed_var_name] = allowed_var_value
        os.environ[disallowed_var_name] = disallowed_var_value

        # Define specific config for this test
        # Ensure self.env_dump_file_path is defined (done in setUp)
        env_test_rules = [
            {
                "id": "RULE-002", # Changed to be compliant with schema ^RULE-\\d{3}$
                "name": "EnvVarTestRule",
                "enabled": True,
                "file_glob": "*.txt",
                "trigger_pattern": "Initial content",
                "actions": [
                    {
                        "type": "run_command",
                        "params": {
                            "command": [
                                "python", "-c",
                                # Write to a relative path "env_dump.json".
                                # The CWD for the command will be Scribe's execution directory (e.g., /app)
                                f"import os, json; f=open(r'env_dump.json', 'w'); json.dump(dict(os.environ), f); f.close()"
                            ],
                            # "cwd": self.watch_dir, # Removed to avoid absolute path validation issue in SecurityManager
                            "allowed_env_vars": [allowed_var_name, "PATH", "LC_ALL", "LANG"]
                        }
                    }
                ]
            }
        ]

        # Define security settings for this test, allowing 'python'
        env_test_security_settings = {"allowed_commands": ["python"], "restricted_paths": []}
        self.current_test_config_path_for_env_test = create_temp_config_file(env_test_rules, [], security_settings=env_test_security_settings)


        test_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        # This should point to 'tools/scribe/actions' for the real run_command_action.py
        scribe_actions_dir = str(test_file_dir.parent.parent / 'tools' / 'scribe' / 'actions')

        original_cm_init_for_this_test = ConfigManager.__init__ # Save CfgMan.__init__ (possibly patched by setUp)
        _test_cfg_path = self.current_test_config_path_for_env_test
        # For PluginLoader default: it's 'actions' relative to 'tools/scribe/'
        # Path(__file__) is test_full_pipeline.py
        # tools_scribe_dir = Path(__file__).parent.parent.parent / 'tools' / 'scribe'
        # actions_dir_path = str(tools_scribe_dir / 'actions')
        # This pathing is tricky; let's rely on PluginLoader's default if possible by passing None,
        # or ensure the main self.plugin_dir (dummy) is not used if run_command is a real plugin.
        # For this test, we need the *actual* run_command_action.py to be loaded.
        # The PluginLoader in self.worker might be using the dummy self.plugin_dir.

        # Temporarily patch ConfigManager.__init__ for this test's specific worker
        def temp_mocked_cm_init_for_env_test(slf, config_path=None, schema_path="config/config.schema.json", auto_reload=True):
            # Use the specific config for this env test
            # Call the true original __init__ saved in setUp
            self.original_config_manager_init(slf, config_path=_test_cfg_path, schema_path=schema_path, auto_reload=False)
            # Make get_plugin_directories return the path to the *actual* 'actions' directory
            # so that 'run_command' can be found.
            # This assumes 'tools/scribe/actions' is where run_command_action.py is.
            # This needs to be robust. Let's assume tools_dir is available or calculable.
            # tools_dir_path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / 'tools'
            # This is still fragile. The path for PluginLoader should ideally be configurable for Scribe instances.
            # For the test, if we rely on the default 'actions' dir of PluginLoader, we pass None to its constructor.
            # The current self.worker.plugin_loader uses self.plugin_dir (dummy).
            # We must ensure the worker for *this test* uses a PluginLoader that finds the real 'run_command_action'.

            # For this test, we need SecurityManager to use the config that has run_command in allowed_commands.
            # The default test config might not allow "python".
            # The config.schema.json defines security.allowed_commands
            # Our create_temp_config_file sets security.allowed_commands = []
            # This means "python" won't be allowed! We need to update this.
            # This should be part of env_test_rules or the temp_config_file creation.
            # This will be handled by modifying create_temp_config_file to accept security settings.
            # For now, let's assume the command *would* run if allowed. The focus is env var passing.
            # The dummy ConfigManager init below must ensure the loaded config is the one from current_test_config_path.

            # This lambda for get_plugin_directories will be on the ConfigManager *instance*
            # It needs to return the path to the actual 'actions' directory for run_command_action.
            # Assuming 'tools/scribe/actions' from where this test file is.
            # This lambda for get_plugin_directories will be on the ConfigManager *instance*
            # It needs to return the path to the actual 'actions' directory for run_command_action.
            slf.get_plugin_directories = lambda: scribe_actions_dir


        ConfigManager.__init__ = temp_mocked_cm_init_for_env_test

        # This worker will use the config and plugin path defined in temp_mocked_cm_init_for_env_test
        worker_for_env_test = Worker(
            event_queue=queue.Queue(),
            shutdown_event=threading.Event(),
            queue_timeout=0.05
        )
        # Ensure its specific plugin loader loads plugins from the correct 'actions' directory
        # The PluginLoader inside worker_for_env_test was initialized using slf.get_plugin_directories via the mocked ConfigManager
        # So, its self.plugins_directory should already be scribe_actions_dir.
        # worker_for_env_test.plugin_loader.plugins_directory = Path(scribe_actions_dir) # This might be redundant if above is correct
        worker_for_env_test.plugin_loader.load_all_plugins()

        ConfigManager.__init__ = original_cm_init_for_this_test # Restore to state before this specific test method's patch

        # Define the expected path for env_dump.json (relative to Scribe's CWD, likely /app)
        # For the test, we'll assume it's created in the current working directory of the test runner if CWD is not specified for command.
        # The test runner's CWD is /app.
        env_dump_output_path = "env_dump.json"
        if os.path.exists(env_dump_output_path): # Clean up from previous failed run if any
            os.remove(env_dump_output_path)


        event = {'event_type': 'modified', 'file_path': self.test_file_path, 'timestamp': time.time()}
        worker_for_env_test.event_queue.put(event)

        env_worker_thread = threading.Thread(target=worker_for_env_test.run, daemon=True)
        env_worker_thread.start()
        time.sleep(1.5) # Increased sleep slightly for file I/O
        worker_for_env_test.shutdown_event.set()
        env_worker_thread.join(timeout=1.0)

        self.assertTrue(os.path.exists(env_dump_output_path), f"Environment dump file '{env_dump_output_path}' was not created.")

        dumped_env = {}
        with open(env_dump_output_path, "r") as f:
            dumped_env = json.load(f)

        if os.path.exists(env_dump_output_path): # Clean up after reading
            os.remove(env_dump_output_path)

        self.assertIn(allowed_var_name, dumped_env, f"{allowed_var_name} should be in the dumped environment.")
        self.assertEqual(dumped_env[allowed_var_name], allowed_var_value, f"{allowed_var_name} has incorrect value.")
        self.assertNotIn(disallowed_var_name, dumped_env, f"{disallowed_var_name} should NOT be in the dumped environment.")
        self.assertIn("PATH", dumped_env, "PATH should be in the dumped environment.")
        # Since "PATH" is in allowed_env_vars, it should be the system's PATH.
        self.assertEqual(dumped_env["PATH"], os.environ["PATH"], "PATH was not the expected system PATH when allowed.")

        # Cleanup specific to this test method
        # os.environ restoration is handled in tearDown
        # env_dump_file_path deletion is handled in tearDown


if __name__ == "__main__":
    # This allows running the test directly
    # Add tools directory to sys.path for imports if running directly and scribe is not installed
    import sys
    # Assuming the script is run from the repo root or test-environment folder
    # This is a common way to handle imports for non-packaged local modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tools_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'tools')) # Adjust if test is deeper
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)

    # Re-import after path adjustment if necessary for direct run
    # from tools.scribe.worker import Worker
    # from tools.scribe.core.config_manager import ConfigManager

    unittest.main()
