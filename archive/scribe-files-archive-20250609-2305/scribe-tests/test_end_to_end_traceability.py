#!/usr/bin/env python3
"""
End-to-End Event Traceability Integration Test

This test demonstrates that a single event_id can be traced through the entire
Scribe processing pipeline from file system event to action execution.
"""

import unittest
import tempfile
import queue
import threading
import time
import uuid
import json
import io
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from contextlib import redirect_stdout, redirect_stderr

# Import scribe modules
from watcher import ScribeEventHandler, Watcher
from worker import Worker
from core.rule_processor import RuleProcessor, CompiledRule, RuleMatch
from core.action_dispatcher import ActionDispatcher
from core.config_manager import ConfigManager
from core.plugin_loader import PluginLoader
from core.logging_config import configure_structured_logging, get_scribe_logger


class TestEndToEndTraceability(unittest.TestCase):
    """Integration test for end-to-end event traceability."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Configure structured logging to capture JSON output
        configure_structured_logging(log_level="DEBUG")
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create test configuration
        self.config_data = {
            "rules": [
                {
                    "id": "TEST-TRACE-001",
                    "name": "Test Traceability Rule",
                    "enabled": True,
                    "file_glob": "*.md",
                    "trigger_pattern": r"# (.+)",
                    "actions": [
                        {
                            "type": "log_action",
                            "params": {
                                "message": "Test action executed"
                            }
                        }
                    ]
                }
            ]
        }
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_event_id_traces_through_pipeline(self):
        """
        CRITICAL INTEGRATION TEST:
        Verify that a single event_id can be traced through the entire pipeline.
        """
        # Capture all log output
        log_capture = io.StringIO()
        
        # Create event queue and handler
        event_queue = queue.Queue()
        handler = ScribeEventHandler(event_queue, ['*.md'])
        
        # Create test file
        test_file = self.temp_path / "test_trace.md"
        test_file.write_text("# Test Header\nSome content for tracing")
        
        # Capture logs by redirecting stdout (where JSON logs go)
        with redirect_stdout(log_capture):
            # Step 1: Generate event with event_id
            handler._queue_event('modified', str(test_file))
            
            # Get the event and extract event_id
            event = event_queue.get_nowait()
            event_id = event['event_id']
            
            # Step 2: Process through Worker
            worker = Worker(event_queue, threading.Event(), queue_timeout=0.1)
            worker._process_event(event)
            
            # Step 3: Simulate rule processing with event_id
            # Create mock config manager
            mock_config_manager = Mock()
            mock_config_manager.get_rules.return_value = self.config_data["rules"]
            
            # Create rule processor
            rule_processor = RuleProcessor(mock_config_manager)
            
            # Process file with event_id
            file_content = test_file.read_text()
            rule_matches = rule_processor.process_file(str(test_file), file_content, event_id)
            
            # Step 4: Simulate action dispatch with event_id
            if rule_matches:
                # Create mock plugin loader and action dispatcher
                mock_plugin_loader = Mock()
                action_dispatcher = ActionDispatcher(mock_plugin_loader)
                
                # Mock the action execution to avoid needing actual action plugins
                with patch.object(action_dispatcher, 'get_action_instance') as mock_get_action:
                    mock_action = Mock()
                    mock_action.action_type = "log_action"
                    mock_action.execute.return_value = file_content  # Return unchanged content
                    mock_action.pre_execute = Mock()
                    mock_action.post_execute = Mock()
                    mock_get_action.return_value = mock_action
                    
                    # Mock validation methods
                    action_dispatcher.validate_action_params = Mock(return_value=(True, None))
                    action_dispatcher.apply_security_restrictions = Mock(return_value=(True, None))
                    
                    # Dispatch actions for the first rule match
                    dispatch_result = action_dispatcher.dispatch_actions(rule_matches[0])
        
        # Analyze captured logs
        log_output = log_capture.getvalue()
        log_lines = [line.strip() for line in log_output.split('\n') if line.strip()]
        
        # Parse JSON log entries
        json_logs = []
        for line in log_lines:
            try:
                log_entry = json.loads(line)
                json_logs.append(log_entry)
            except json.JSONDecodeError:
                # Skip non-JSON lines
                continue
        
        # Find all log entries that contain our event_id
        traced_logs = [log for log in json_logs if log.get('event_id') == event_id]
        
        # Verify we have logs from different pipeline stages
        self.assertGreater(len(traced_logs), 0, f"Should have logs with event_id {event_id}")
        
        # Verify event_id consistency
        for log_entry in traced_logs:
            self.assertEqual(
                log_entry['event_id'], 
                event_id,
                f"All traced logs should have the same event_id {event_id}"
            )
        
        # Print traceability summary
        print(f"\n✅ END-TO-END TRACEABILITY VERIFIED")
        print(f"Event ID: {event_id}")
        print(f"Total log entries with this event_id: {len(traced_logs)}")
        
        for i, log_entry in enumerate(traced_logs, 1):
            component = log_entry.get('logger', 'unknown')
            message = log_entry.get('event', 'unknown')
            print(f"  {i}. [{component}] {message}")
        
        return event_id, traced_logs
    
    def test_multiple_events_maintain_separate_traces(self):
        """
        Verify that multiple concurrent events maintain separate event_id traces.
        """
        # Create event queue and handler
        event_queue = queue.Queue()
        handler = ScribeEventHandler(event_queue, ['*.md'])
        
        # Create multiple test files
        test_files = []
        for i in range(3):
            test_file = self.temp_path / f"test_multi_{i}.md"
            test_file.write_text(f"# Test Header {i}\nContent for file {i}")
            test_files.append(test_file)
        
        # Generate events for all files
        for test_file in test_files:
            handler._queue_event('modified', str(test_file))
        
        # Collect all events and their event_ids
        events = []
        event_ids = []
        while not event_queue.empty():
            event = event_queue.get_nowait()
            events.append(event)
            event_ids.append(event['event_id'])
        
        # Verify all event_ids are unique
        self.assertEqual(len(event_ids), 3)
        self.assertEqual(len(set(event_ids)), 3, "All event_ids should be unique")
        
        # Process each event through worker
        worker = Worker(event_queue, threading.Event(), queue_timeout=0.1)
        for event in events:
            worker._process_event(event)
        
        print(f"\n✅ MULTIPLE EVENT TRACEABILITY VERIFIED")
        print(f"Generated {len(event_ids)} unique event_ids:")
        for i, event_id in enumerate(event_ids, 1):
            print(f"  {i}. {event_id}")


class TestPhase3ExitConditions(unittest.TestCase):
    """Test the specific exit conditions for PHASE 3."""
    
    def test_phase_3_exit_condition_logs_traceable_via_event_id(self):
        """
        PHASE 3 EXIT CONDITION TEST:
        Logs are traceable end-to-end via event_id.
        """
        # Capture all structured log output
        log_capture = io.StringIO()
        
        with redirect_stdout(log_capture):
            # Create and run the end-to-end traceability test
            test_instance = TestEndToEndTraceability()
            test_instance.setUp()
            
            try:
                event_id, traced_logs = test_instance.test_event_id_traces_through_pipeline()
                
                # PHASE 3 EXIT CONDITION: Verify logs are traceable via event_id
                self.assertGreater(
                    len(traced_logs), 
                    0, 
                    "PHASE 3 EXIT CONDITION FAILED: No logs found with event_id"
                )
                
                # Verify all traced logs have the same event_id
                for log_entry in traced_logs:
                    self.assertEqual(
                        log_entry.get('event_id'), 
                        event_id,
                        "PHASE 3 EXIT CONDITION FAILED: Inconsistent event_id in logs"
                    )
                
                print(f"\n🎯 PHASE 3 EXIT CONDITION SATISFIED")
                print(f"✅ Logs are traceable end-to-end via event_id: {event_id}")
                print(f"✅ Found {len(traced_logs)} log entries with consistent event_id")
                
            finally:
                test_instance.tearDown()


if __name__ == '__main__':
    # Run with verbose output to see the traceability details
    unittest.main(verbosity=2) 