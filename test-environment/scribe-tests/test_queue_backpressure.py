#!/usr/bin/env python3
"""
Test Queue Backpressure

This test verifies that the bounded queue correctly drops events under high load
and generates appropriate warning messages.
"""

import unittest
import threading
import queue
import time
import tempfile
import os
import shutil
from pathlib import Path
from unittest.mock import patch
import logging
import io

# Import scribe modules
from engine import ScribeEngine
from watcher import Watcher, ScribeEventHandler


class TestQueueBackpressure(unittest.TestCase):
    """Test queue backpressure behavior under high load."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.shutdown_event = threading.Event()
        
        # Set up log capture
        self.log_stream = io.StringIO()
        self.log_handler = logging.StreamHandler(self.log_stream)
        self.log_handler.setLevel(logging.WARNING)
        
        # Get the scribe logger and add our handler
        import structlog
        from core.logging_config import get_scribe_logger
        self.logger = get_scribe_logger("watcher")
        
    def tearDown(self):
        """Clean up test fixtures."""
        self.shutdown_event.set()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_bounded_queue_drops_events_under_high_load(self):
        """Test that bounded queue drops events when full and logs warnings."""
        # Create a very small queue to easily trigger backpressure
        small_queue = queue.Queue(maxsize=3)
        
        # Create event handler with small queue
        event_handler = ScribeEventHandler(small_queue, ['*.md'])
        
        # Capture log output
        with patch('watcher.logger') as mock_logger:
            # Fill the queue to capacity
            event_handler._queue_event('test1', '/path/test1.md')
            event_handler._queue_event('test2', '/path/test2.md')
            event_handler._queue_event('test3', '/path/test3.md')
            
            # Verify queue is full
            self.assertEqual(small_queue.qsize(), 3)
            
            # Try to add more events - these should be dropped
            event_handler._queue_event('test4', '/path/test4.md')
            event_handler._queue_event('test5', '/path/test5.md')
            
            # Queue should still be at capacity
            self.assertEqual(small_queue.qsize(), 3)
            
            # Verify warning messages were logged for dropped events
            warning_calls = [call for call in mock_logger.warning.call_args_list 
                           if "Event queue is full, dropping event" in str(call)]
            self.assertEqual(len(warning_calls), 2)  # Two events should have been dropped
    
    def test_engine_with_small_queue_under_burst_load(self):
        """Test engine behavior with small queue under burst file creation."""
        # Create engine with very small queue
        engine = ScribeEngine(
            watch_paths=[self.temp_dir],
            file_patterns=['*.md'],
            queue_maxsize=5  # Very small queue
        )
        
        try:
            # Start the engine
            engine.start()
            time.sleep(0.2)  # Let it start up
            
            # Capture logs
            with patch('watcher.logger') as mock_logger:
                # Create burst of files rapidly
                for i in range(15):  # More files than queue capacity
                    test_file = Path(self.temp_dir) / f"burst_test_{i}.md"
                    test_file.write_text(f"# Test File {i}\n\nContent {i}")
                    time.sleep(0.01)  # Small delay to ensure events are generated
                
                # Give time for events to be processed
                time.sleep(1.0)
                
                # Check if any warning messages were logged
                warning_calls = [call for call in mock_logger.warning.call_args_list 
                               if "Event queue is full, dropping event" in str(call)]
                
                # We should have some dropped events due to the small queue
                self.assertGreater(len(warning_calls), 0, 
                                 "Expected some events to be dropped due to small queue size")
                
                print(f"Successfully triggered {len(warning_calls)} backpressure warnings")
                
        finally:
            engine.stop()
    
    def test_queue_backpressure_logging_details(self):
        """Test that backpressure logging includes proper event details."""
        small_queue = queue.Queue(maxsize=1)
        event_handler = ScribeEventHandler(small_queue, ['*.md'])
        
        with patch('watcher.logger') as mock_logger:
            # Fill queue
            event_handler._queue_event('created', '/path/file1.md')
            
            # Try to add another event (should be dropped)
            event_handler._queue_event('modified', '/path/file2.md')
            
            # Verify the warning call includes event details
            mock_logger.warning.assert_called_with(
                "Event queue is full, dropping event",
                event_id=unittest.mock.ANY,  # UUID will be different each time
                event_type='modified',
                file_path='/path/file2.md'
            )
    
    def test_queue_normal_operation_no_drops(self):
        """Test that normal operation doesn't trigger backpressure warnings."""
        normal_queue = queue.Queue(maxsize=100)  # Large enough queue
        event_handler = ScribeEventHandler(normal_queue, ['*.md'])
        
        with patch('watcher.logger') as mock_logger:
            # Add several events within capacity
            for i in range(10):
                event_handler._queue_event('test', f'/path/file{i}.md')
            
            # Verify no warning messages were logged
            warning_calls = [call for call in mock_logger.warning.call_args_list 
                           if "Event queue is full, dropping event" in str(call)]
            self.assertEqual(len(warning_calls), 0)
            
            # Verify all events were queued
            self.assertEqual(normal_queue.qsize(), 10)


if __name__ == '__main__':
    unittest.main() 