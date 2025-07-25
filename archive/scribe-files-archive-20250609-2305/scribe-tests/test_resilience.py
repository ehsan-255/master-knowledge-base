import unittest
from tools.scribe.core.action_dispatcher import ActionDispatcher, BaseAction, ActionExecutionError
from tools.scribe.core.plugin_loader import PluginLoader
from tools.scribe.core.config_manager import ConfigManager
from tools.scribe.core.security_manager import SecurityManager
import re

class FailingAction(BaseAction):
    def execute(self, *args, **kwargs):
        raise ActionExecutionError("test", "Simulated failure")

class TestResilience(unittest.TestCase):
    def setUp(self):
        self.config = ConfigManager()
        self.loader = PluginLoader()
        self.security = SecurityManager(self.config)
        self.dispatcher = ActionDispatcher(self.loader, self.config, self.security)

    def test_retries_on_failure(self):
        action = FailingAction("failing", {}, self.config, self.security)
        result = self.dispatcher.execute_action(action, "", re.match("", ""), "", {})
        self.assertFalse(result.success)
        # Since max_retries=3, it should attempt 4 times (0-3), but fail

if __name__ == '__main__':
    unittest.main() 