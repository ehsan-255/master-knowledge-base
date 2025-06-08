"""
Integration tests for the Scribe Engine event flow.

These tests verify that the complete event pipeline works correctly
from file system events through to worker processing.
"""

import unittest
import threading
import queue
import time
import tempfile
import os
from pathlib import Path

# Add the scribe module to the path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'scribe'))

from engine import ScribeEngine
from watcher import Watcher
from worker import Worker


class TestEventFlowIntegration(unittest.TestCase):
    """Test the complete event flow from watcher to worker."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.event_queue = queue.Queue()
        self.shutdown_event = threading.Event()
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_file_creation_event_flow(self):
        """Test that a file creation flows from watcher to worker."""
        # Create watcher and worker
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir],
            file_patterns=['*.md']
        )
        
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        try:
            # Start both threads
            watcher.start()
            worker.start()
            
            # Give them time to start
            time.sleep(0.2)
            
            # Create a test file
            test_file = Path(self.temp_dir) / "test.md"
            test_file.write_text("# Test File\n\nThis is a test.")
            
            # Give time for event to be processed
            time.sleep(0.5)
            
            # Verify worker processed the event
            self.assertGreater(worker.events_processed, 0)
            self.assertEqual(worker.events_failed, 0)
            
        finally:
            # Clean shutdown
            self.shutdown_event.set()
            watcher.join(timeout=5.0)
            worker.join(timeout=5.0)
    
    def test_file_modification_event_flow(self):
        """Test that a file modification flows from watcher to worker."""
        # Create a test file first
        test_file = Path(self.temp_dir) / "existing.md"
        test_file.write_text("# Initial Content")
        
        # Create watcher and worker
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir],
            file_patterns=['*.md']
        )
        
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        try:
            # Start both threads
            watcher.start()
            worker.start()
            
            # Give them time to start
            time.sleep(0.2)
            
            # Modify the test file
            test_file.write_text("# Modified Content\n\nThis has been changed.")
            
            # Give time for event to be processed
            time.sleep(0.5)
            
            # Verify worker processed the event
            self.assertGreater(worker.events_processed, 0)
            self.assertEqual(worker.events_failed, 0)
            
        finally:
            # Clean shutdown
            self.shutdown_event.set()
            watcher.join(timeout=5.0)
            worker.join(timeout=5.0)
    
    def test_multiple_file_events_flow(self):
        """Test that multiple file events are processed correctly."""
        # Create watcher and worker
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir],
            file_patterns=['*.md']
        )
        
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        try:
            # Start both threads
            watcher.start()
            worker.start()
            
            # Give them time to start
            time.sleep(0.2)
            
            # Create multiple test files
            for i in range(3):
                test_file = Path(self.temp_dir) / f"test{i}.md"
                test_file.write_text(f"# Test File {i}\n\nContent for file {i}.")
                time.sleep(0.1)  # Small delay between creations
            
            # Give time for all events to be processed
            time.sleep(1.0)
            
            # Verify worker processed multiple events
            self.assertGreaterEqual(worker.events_processed, 3)
            self.assertEqual(worker.events_failed, 0)
            
        finally:
            # Clean shutdown
            self.shutdown_event.set()
            watcher.join(timeout=5.0)
            worker.join(timeout=5.0)
    
    def test_non_matching_files_ignored(self):
        """Test that non-matching files are ignored by the pipeline."""
        # Create watcher and worker
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir],
            file_patterns=['*.md']  # Only watch .md files
        )
        
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        try:
            # Start both threads
            watcher.start()
            worker.start()
            
            # Give them time to start
            time.sleep(0.2)
            
            # Create a non-matching file
            test_file = Path(self.temp_dir) / "test.txt"  # .txt file, not .md
            test_file.write_text("This should be ignored.")
            
            # Give time for potential event processing
            time.sleep(0.5)
            
            # Verify no events were processed
            self.assertEqual(worker.events_processed, 0)
            self.assertEqual(worker.events_failed, 0)
            
        finally:
            # Clean shutdown
            self.shutdown_event.set()
            watcher.join(timeout=5.0)
            worker.join(timeout=5.0)
    
    def test_queue_communication(self):
        """Test that the queue correctly communicates between watcher and worker."""
        # Create watcher and worker
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir],
            file_patterns=['*.md']
        )
        
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        try:
            # Start both threads
            watcher.start()
            worker.start()
            
            # Give them time to start
            time.sleep(0.2)
            
            # Verify queue starts empty
            initial_queue_size = self.event_queue.qsize()
            
            # Create a test file
            test_file = Path(self.temp_dir) / "queue_test.md"
            test_file.write_text("# Queue Test")
            
            # Give time for event to be queued and processed
            time.sleep(0.5)
            
            # Queue should be empty again (event processed)
            final_queue_size = self.event_queue.qsize()
            
            self.assertEqual(initial_queue_size, 0)
            self.assertEqual(final_queue_size, 0)
            self.assertGreater(worker.events_processed, 0)
            
        finally:
            # Clean shutdown
            self.shutdown_event.set()
            watcher.join(timeout=5.0)
            worker.join(timeout=5.0)

    def test_engine_startup_and_shutdown(self):
        """Test that the engine starts and stops correctly."""
        engine = ScribeEngine(
            watch_paths=[self.temp_dir],
            file_patterns=['*.md']
        )
        
        try:
            # Start the engine
            engine.start()
            
            # Verify it's running
            self.assertTrue(engine.is_running)
            self.assertIsNotNone(engine.watcher)
            self.assertIsNotNone(engine.worker)
            self.assertTrue(engine.watcher.is_alive())
            self.assertTrue(engine.worker.is_alive())
            
            # Give it a moment to run
            time.sleep(0.2)
            
        finally:
            # Stop the engine
            engine.stop()
            
            # Give time for shutdown to complete
            time.sleep(0.2)
            
            # Verify it stopped
            self.assertFalse(engine.is_running)
            if engine.watcher:
                self.assertFalse(engine.watcher.is_alive())
            if engine.worker:
                self.assertFalse(engine.worker.is_alive())


if __name__ == '__main__':
    unittest.main() 