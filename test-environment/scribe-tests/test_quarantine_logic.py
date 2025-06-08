#!/usr/bin/env python3
"""
Test suite for quarantine logic functionality.

Tests the quarantine mechanism that moves problematic files when circuit breaker opens.
"""

import unittest
import tempfile
import shutil
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the scribe module to the path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "scribe"))

from core.action_dispatcher import ActionDispatcher, DispatchResult, ActionResult
from core.plugin_loader import PluginLoader
from core.rule_processor import RuleMatch, CompiledRule
from core.circuit_breaker import CircuitBreakerError


class TestQuarantineLogic(unittest.TestCase):
    """Test quarantine logic functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories
        self.temp_dir = tempfile.mkdtemp()
        self.quarantine_dir = Path(self.temp_dir) / "quarantine"
        self.test_files_dir = Path(self.temp_dir) / "test_files"
        self.test_files_dir.mkdir(parents=True, exist_ok=True)
        
        # Create mock plugin loader
        self.mock_plugin_loader = Mock(spec=PluginLoader)
        self.mock_plugin_loader.get_all_plugins.return_value = {}
        
        # Create action dispatcher with test quarantine path
        self.dispatcher = ActionDispatcher(
            plugin_loader=self.mock_plugin_loader,
            quarantine_path=str(self.quarantine_dir)
        )
        
        # Create test file
        self.test_file = self.test_files_dir / "test_document.md"
        self.test_file.write_text("# Test Document\n\nThis is a test file.")
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_quarantine_file_success(self):
        """Test successful file quarantine."""
        # Test quarantine operation
        result = self.dispatcher.quarantine_file(
            file_path=str(self.test_file),
            rule_id="TEST-RULE-001",
            reason="circuit_breaker_open"
        )
        
        # Verify result
        self.assertTrue(result["success"])
        self.assertEqual(result["rule_id"], "TEST-RULE-001")
        self.assertEqual(result["reason"], "circuit_breaker_open")
        self.assertIn("quarantine_path", result)
        self.assertIn("metadata_path", result)
        
        # Verify original file is removed
        self.assertFalse(self.test_file.exists())
        
        # Verify quarantined file exists
        quarantine_path = Path(result["quarantine_path"])
        self.assertTrue(quarantine_path.exists())
        
        # Verify content is preserved
        quarantined_content = quarantine_path.read_text()
        self.assertEqual(quarantined_content, "# Test Document\n\nThis is a test file.")
        
        # Verify metadata file exists and contains correct information
        metadata_path = Path(result["metadata_path"])
        self.assertTrue(metadata_path.exists())
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        self.assertEqual(metadata["original_path"], str(self.test_file))
        self.assertEqual(metadata["rule_id"], "TEST-RULE-001")
        self.assertEqual(metadata["reason"], "circuit_breaker_open")
        self.assertIn("quarantine_time", metadata)
        
        # Verify statistics updated
        stats = self.dispatcher.get_execution_stats()
        self.assertEqual(stats["files_quarantined"], 1)
    
    def test_quarantine_file_nonexistent(self):
        """Test quarantine of non-existent file."""
        nonexistent_file = self.test_files_dir / "nonexistent.md"
        
        result = self.dispatcher.quarantine_file(
            file_path=str(nonexistent_file),
            rule_id="TEST-RULE-002",
            reason="test"
        )
        
        # Verify failure result
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "File does not exist")
        self.assertEqual(result["file_path"], str(nonexistent_file))
        
        # Verify statistics not updated
        stats = self.dispatcher.get_execution_stats()
        self.assertEqual(stats["files_quarantined"], 0)
    
    def test_quarantine_preserves_directory_structure(self):
        """Test that quarantine preserves directory structure."""
        # Create nested directory structure
        nested_dir = self.test_files_dir / "subdir" / "nested"
        nested_dir.mkdir(parents=True, exist_ok=True)
        nested_file = nested_dir / "nested_file.md"
        nested_file.write_text("Nested content")
        
        # Quarantine the nested file
        result = self.dispatcher.quarantine_file(
            file_path=str(nested_file),
            rule_id="TEST-RULE-003",
            reason="test"
        )
        
        # Verify success
        self.assertTrue(result["success"])
        
        # Verify directory structure is preserved in quarantine
        quarantine_path = Path(result["quarantine_path"])
        # The quarantine should preserve some directory structure
        self.assertIn("subdir", str(quarantine_path))
        self.assertIn("nested", str(quarantine_path))
        
        # Verify content
        self.assertEqual(quarantine_path.read_text(), "Nested content")
    
    def test_quarantine_filename_timestamping(self):
        """Test that quarantined files get timestamped names."""
        # Quarantine the same file twice (recreate after first quarantine)
        result1 = self.dispatcher.quarantine_file(
            file_path=str(self.test_file),
            rule_id="TEST-RULE-004",
            reason="test"
        )
        
        # Recreate the file
        self.test_file.write_text("# Test Document\n\nThis is a test file.")
        
        # Small delay to ensure different timestamp
        time.sleep(1)
        
        result2 = self.dispatcher.quarantine_file(
            file_path=str(self.test_file),
            rule_id="TEST-RULE-004",
            reason="test"
        )
        
        # Verify both operations succeeded
        self.assertTrue(result1["success"])
        self.assertTrue(result2["success"])
        
        # Verify different quarantine paths (due to timestamps)
        self.assertNotEqual(result1["quarantine_path"], result2["quarantine_path"])
        
        # Verify both files exist
        self.assertTrue(Path(result1["quarantine_path"]).exists())
        self.assertTrue(Path(result2["quarantine_path"]).exists())
    
    def test_circuit_breaker_triggers_quarantine(self):
        """Test that circuit breaker error triggers quarantine."""
        # Create a mock rule
        mock_rule = Mock(spec=CompiledRule)
        mock_rule.id = "TEST-RULE-005"
        mock_rule.actions = []
        mock_rule.error_handling = {
            "circuit_breaker": {
                "failure_threshold": 3,
                "recovery_timeout_seconds": 60
            }
        }
        
        # Create a mock rule match
        mock_rule_match = Mock(spec=RuleMatch)
        mock_rule_match.rule = mock_rule
        mock_rule_match.file_path = str(self.test_file)
        mock_rule_match.file_content = "test content"
        mock_rule_match.match = Mock()
        
        # Mock the circuit breaker to raise CircuitBreakerError
        with patch.object(self.dispatcher.circuit_breaker_manager, 'get_breaker') as mock_get_breaker:
            mock_breaker = Mock()
            mock_breaker.execute.side_effect = CircuitBreakerError(
                rule_id="TEST-RULE-005",
                failure_count=5,
                last_failure_time=time.time()
            )
            mock_get_breaker.return_value = mock_breaker
            
            # Execute dispatch_actions
            result = self.dispatcher.dispatch_actions(mock_rule_match)
            
            # Verify dispatch result indicates circuit breaker block
            self.assertIsInstance(result, DispatchResult)
            self.assertEqual(result.rule_id, "TEST-RULE-005")
            self.assertEqual(len(result.action_results), 1)
            
            action_result = result.action_results[0]
            self.assertEqual(action_result.action_type, "circuit_breaker")
            self.assertFalse(action_result.success)
            self.assertTrue(action_result.metadata["blocked_by_circuit_breaker"])
            self.assertTrue(action_result.metadata["quarantined"])
            self.assertEqual(action_result.metadata["quarantine_reason"], "circuit_breaker_open")
            
            # Verify file was quarantined
            self.assertFalse(self.test_file.exists())
            
            # Verify statistics updated
            stats = self.dispatcher.get_execution_stats()
            self.assertEqual(stats["circuit_breaker_blocks"], 1)
            self.assertEqual(stats["files_quarantined"], 1)
    
    def test_quarantine_stats_in_execution_stats(self):
        """Test that quarantine statistics are included in execution stats."""
        # Quarantine a file
        self.dispatcher.quarantine_file(
            file_path=str(self.test_file),
            rule_id="TEST-RULE-006",
            reason="test"
        )
        
        # Get execution stats
        stats = self.dispatcher.get_execution_stats()
        
        # Verify quarantine stats are included
        self.assertIn("quarantine_stats", stats)
        quarantine_stats = stats["quarantine_stats"]
        self.assertEqual(quarantine_stats["files_quarantined"], 1)
        self.assertEqual(quarantine_stats["quarantine_path"], str(self.quarantine_dir))
    
    def test_quarantine_error_handling(self):
        """Test quarantine error handling for permission issues."""
        # Create a file in a read-only directory (simulate permission error)
        with patch('pathlib.Path.unlink') as mock_unlink:
            mock_unlink.side_effect = PermissionError("Permission denied")
            
            result = self.dispatcher.quarantine_file(
                file_path=str(self.test_file),
                rule_id="TEST-RULE-007",
                reason="test"
            )
            
            # Verify failure result
            self.assertFalse(result["success"])
            self.assertIn("Permission denied", result["error"])
            self.assertEqual(result["rule_id"], "TEST-RULE-007")
            
            # Verify statistics not updated
            stats = self.dispatcher.get_execution_stats()
            self.assertEqual(stats["files_quarantined"], 0)
    
    def test_reset_stats_includes_quarantine(self):
        """Test that reset_stats resets quarantine statistics."""
        # Quarantine a file
        self.dispatcher.quarantine_file(
            file_path=str(self.test_file),
            rule_id="TEST-RULE-008",
            reason="test"
        )
        
        # Verify stats updated
        stats = self.dispatcher.get_execution_stats()
        self.assertEqual(stats["files_quarantined"], 1)
        
        # Reset stats
        self.dispatcher.reset_stats()
        
        # Verify stats reset
        stats = self.dispatcher.get_execution_stats()
        self.assertEqual(stats["files_quarantined"], 0)


if __name__ == '__main__':
    unittest.main() 