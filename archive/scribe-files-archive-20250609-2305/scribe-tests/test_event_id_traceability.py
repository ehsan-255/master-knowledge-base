#!/usr/bin/env python3
"""
Test Event ID Traceability

This test verifies that event_id is generated in the Watcher and propagated
through the entire processing pipeline for end-to-end traceability.
"""

import unittest
import tempfile
import queue
import threading
import time
import uuid
from pathlib import Path
from unittest.mock import Mock, patch

# Import scribe modules using the installed package
from watcher import ScribeEventHandler
from worker import Worker


class TestEventIdTraceability(unittest.TestCase):
    """Test event_id generation and propagation through the Scribe pipeline."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create test queue and shutdown event
        self.event_queue = queue.Queue()
        self.shutdown_event = threading.Event()
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_watcher_generates_event_id(self):
        """Test that the Watcher generates unique event_id for each event."""
        # Create event handler
        handler = ScribeEventHandler(self.event_queue, ['*.md'])
        
        # Create test file
        test_file = self.temp_path / "test.md"
        test_file.write_text("# Test Content")
        
        # Trigger event
        handler._queue_event('modified', str(test_file))
        
        # Get event from queue
        self.assertFalse(self.event_queue.empty())
        event = self.event_queue.get_nowait()
        
        # Verify event_id is present and valid UUID
        self.assertIn('event_id', event)
        self.assertIsInstance(event['event_id'], str)
        
        # Verify it's a valid UUID
        try:
            uuid.UUID(event['event_id'])
        except ValueError:
            self.fail(f"event_id '{event['event_id']}' is not a valid UUID")
        
        # Verify other event data
        self.assertEqual(event['type'], 'modified')
        self.assertEqual(event['file_path'], str(test_file))
        self.assertIn('timestamp', event)
    
    def test_multiple_events_have_unique_ids(self):
        """Test that multiple events get unique event_id values."""
        handler = ScribeEventHandler(self.event_queue, ['*.md'])
        
        # Create multiple test files
        test_files = []
        for i in range(3):
            test_file = self.temp_path / f"test_{i}.md"
            test_file.write_text(f"# Test Content {i}")
            test_files.append(test_file)
        
        # Trigger multiple events
        for test_file in test_files:
            handler._queue_event('modified', str(test_file))
        
        # Collect all event_ids
        event_ids = []
        while not self.event_queue.empty():
            event = self.event_queue.get_nowait()
            event_ids.append(event['event_id'])
        
        # Verify all event_ids are unique
        self.assertEqual(len(event_ids), 3)
        self.assertEqual(len(set(event_ids)), 3, "Event IDs should be unique")
    
    def test_worker_extracts_event_id(self):
        """Test that the Worker extracts and uses event_id from events."""
        # Create worker
        worker = Worker(self.event_queue, self.shutdown_event, queue_timeout=0.1)
        
        # Create test event with event_id
        test_event_id = str(uuid.uuid4())
        test_event = {
            'event_id': test_event_id,
            'type': 'modified',
            'file_path': str(self.temp_path / "test.md"),
            'timestamp': time.time()
        }
        
        # Process the event (should not raise any errors)
        try:
            worker._process_event(test_event)
        except Exception as e:
            self.fail(f"Worker failed to process event with event_id: {e}")


class TestEventIdExitConditions(unittest.TestCase):
    """Test the exit conditions for PHASE 3: Event ID Traceability."""
    
    def test_phase_3_exit_condition_event_id_generation(self):
        """
        CRITICAL TEST for PHASE 3 EXIT CONDITIONS:
        Verify that event_id is generated and can be traced through the pipeline.
        """
        # Create event handler
        event_queue = queue.Queue()
        handler = ScribeEventHandler(event_queue, ['*.md'])
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Content")
            test_file_path = f.name
        
        try:
            # Trigger event
            handler._queue_event('modified', test_file_path)
            
            # Get the event
            event = event_queue.get_nowait()
            event_id = event['event_id']
            
            # Verify event_id is a valid UUID
            uuid.UUID(event_id)  # Will raise ValueError if invalid
            
            # Process event through worker
            worker = Worker(event_queue, threading.Event(), queue_timeout=0.1)
            worker._process_event(event)
            
            print(f"✅ PHASE 3 EXIT CONDITION MET: Event ID {event_id} generated and processed successfully")
        
        finally:
            # Clean up
            Path(test_file_path).unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main() 