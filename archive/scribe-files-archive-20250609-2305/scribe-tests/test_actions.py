import unittest
import tempfile
from pathlib import Path
import os
import json

from tools.scribe.core.config_manager import ConfigManager
from tools.scribe.core.security_manager import SecurityManager
from tools.scribe.actions.run_command_action import RunCommandAction
from tools.scribe.actions.base import ActionExecutionError
from tools.scribe.core.security_manager import SecurityViolation
from tools.scribe.actions.reconciliation_action import ReconciliationAction
from tools.scribe.actions.view_generation_action import ViewGenerationAction

class TestScribeActions(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.test_dir.name)
        
        # Create a dummy .git folder to ensure repo root is found correctly
        (self.repo_root / ".git").mkdir()
        
        # Mock ConfigManager and SecurityManager
        self.config_manager = self.create_mock_config_manager()
        self.security_manager = SecurityManager(self.config_manager)

    def tearDown(self):
        self.test_dir.cleanup()

    def create_mock_config_manager(self):
        # Create a mock that provides the necessary methods for actions
        mock_cm = unittest.mock.MagicMock(spec=ConfigManager)
        mock_cm.get_repo_root.return_value = str(self.repo_root)
        mock_cm.get_security_settings.return_value = {
            "allowed_commands": ["echo", "ls", "python"],
            "restricted_paths": []
        }
        return mock_cm

    def test_run_command_action_success(self):
        """Test that RunCommandAction executes a simple, allowed command successfully."""
        action_params = {
            "command": ["echo", "hello world"],
            "timeout": 5
        }
        
        action = RunCommandAction(
            action_type="run_command",
            params=action_params,
            config_manager=self.config_manager,
            security_manager=self.security_manager
        )
        
        # The execute method for RunCommandAction doesn't use these, but they are required by the signature
        file_content = "some content"
        match = None
        file_path = "dummy_file.txt"
        
        # SecurityManager.execute_command_safely returns (success, stdout, stderr)
        # The RunCommandAction should not raise an error for a successful command.
        try:
            result_content = action.execute(file_content, match, file_path, action_params)
            # The action returns the original content on success
            self.assertEqual(result_content, file_content)
        except ActionExecutionError as e:
            self.fail(f"RunCommandAction raised an unexpected exception for a successful command: {e}")

    def test_run_command_action_disallowed(self):
        """Test that RunCommandAction raises an error for a disallowed command."""
        action_params = {
            "command": ["git", "status"], # Assume 'git' is not in allowed_commands
            "timeout": 5
        }
        
        # Create a new config manager mock that disallows 'git'
        mock_cm_disallow = unittest.mock.MagicMock(spec=ConfigManager)
        mock_cm_disallow.get_repo_root.return_value = str(self.repo_root)
        mock_cm_disallow.get_security_settings.return_value = {
            "allowed_commands": ["echo"], # 'git' is not here
            "restricted_paths": []
        }
        security_manager_disallow = SecurityManager(mock_cm_disallow)
        
        action = RunCommandAction(
            action_type="run_command",
            params=action_params,
            config_manager=mock_cm_disallow,
            security_manager=security_manager_disallow
        )
        
        with self.assertRaises(ActionExecutionError) as cm:
            action.execute("content", None, "dummy.txt", action_params)
        
        # Check that the underlying error is a SecurityViolation
        self.assertIsInstance(cm.exception.original_error, SecurityViolation)
        self.assertIn("not in the allowed commands list", str(cm.exception))

    def test_reconciliation_action_creates_index(self):
        """Test that ReconciliationAction can scan a directory and create a master index."""
        # 1. Setup the test environment for this action
        test_kb_dir = self.repo_root / "knowledge_base"
        test_kb_dir.mkdir()
        
        # Create a dummy markdown file with frontmatter
        md_content = """---
kb-id: "TEST-DOC-001"
title: "My Test Document"
version: "1.1"
---
# Content
This is a test document.
"""
        test_md_file = test_kb_dir / "test_doc.md"
        test_md_file.write_text(md_content)

        # 2. Configure and instantiate the action
        master_index_path = "master-index.jsonld"
        action_params = {
            "master_index_path": master_index_path,
            "kb_root_dirs": ["knowledge_base"],
            "exclude_dirs": [".git"]
        }
        
        action = ReconciliationAction(
            action_type="reconciliation_action",
            params=action_params,
            config_manager=self.config_manager,
            security_manager=self.security_manager
        )
        
        # 3. Execute the action
        action.execute(file_content="", match=None, file_path="dummy.txt", params=action_params)
        
        # 4. Assert the outcome
        expected_index_file = self.repo_root / master_index_path
        self.assertTrue(expected_index_file.exists())
        
        with open(expected_index_file, "r") as f:
            index_data = json.load(f)
            
        self.assertEqual(index_data["kb:documentCount"], 1)
        self.assertEqual(len(index_data["kb:documents"]), 1)
        doc_entry = index_data["kb:documents"][0]
        self.assertEqual(doc_entry["kb-id"], "TEST-DOC-001")
        self.assertEqual(doc_entry["kb:title"], "My Test Document")
        self.assertEqual(doc_entry["kb:filepath"], str(Path("knowledge_base") / "test_doc.md"))

    def test_view_generation_action_creates_view(self):
        """Test that ViewGenerationAction can generate a view from a master index."""
        # 1. Setup the test environment
        master_index_content = {
            "@context": {},
            "kb:documents": [{
                "kb-id": "VIEW-TEST-001",
                "kb:title": "View Test Document",
                "kb:version": "1.0",
                "description": "This is for the view generation test."
            }]
        }
        master_index_file = self.repo_root / "master-index.jsonld"
        with open(master_index_file, "w") as f:
            json.dump(master_index_content, f)

        # 2. Configure and instantiate the action
        output_view_path = "test-view.md"
        action_params = {
            "master_index_path": "master-index.jsonld",
            "schema_registry_path": "dummy-schema.jsonld", # Action requires this, but doesn't use it heavily for this view
            "entity_id": "VIEW-TEST-001",
            "view_type": "md",
            "output_path": output_view_path
        }
        
        # Create a dummy schema file
        (self.repo_root / "dummy-schema.jsonld").write_text("{}")
        
        action = ViewGenerationAction(
            action_type="view_generation_action",
            params=action_params,
            config_manager=self.config_manager,
            security_manager=self.security_manager
        )
        
        # 3. Execute the action
        action.execute(file_content="", match=None, file_path="dummy.txt", params=action_params)
        
        # 4. Assert the outcome
        expected_view_file = self.repo_root / output_view_path
        self.assertTrue(expected_view_file.exists())
        
        view_content = expected_view_file.read_text()
        self.assertIn("# View for Standard: VIEW-TEST-001", view_content)
        self.assertIn("## Title: View Test Document", view_content)
        self.assertIn("- **description**: This is for the view generation test.", view_content)

if __name__ == '__main__':
    unittest.main() 