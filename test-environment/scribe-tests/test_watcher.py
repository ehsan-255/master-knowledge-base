"""
Unit tests for the Scribe Watcher (Producer Thread).

These tests verify the watcher functionality in isolation.
"""

import unittest
import threading
import queue
import time
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add the scribe module to the path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'scribe'))

from watcher import Watcher, ScribeEventHandler


class TestScribeEventHandler(unittest.TestCase):
    """Test the ScribeEventHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.event_queue = queue.Queue()
        self.handler = ScribeEventHandler(self.event_queue, ['*.md', '*.txt'])
    
    def test_should_process_file_matching_pattern(self):
        """Test that files matching patterns are processed."""
        self.assertTrue(self.handler._should_process_file('/path/to/file.md'))
        self.assertTrue(self.handler._should_process_file('/path/to/file.txt'))
        self.assertFalse(self.handler._should_process_file('/path/to/file.py'))
        self.assertFalse(self.handler._should_process_file('/path/to/file.json'))
    
    def test_queue_event_success(self):
        """Test that events are queued successfully."""
        self.handler._queue_event('modified', '/path/to/test.md')
        
        self.assertEqual(self.event_queue.qsize(), 1)
        event = self.event_queue.get_nowait()
        
        self.assertEqual(event['type'], 'modified')
        self.assertEqual(event['file_path'], '/path/to/test.md')
        self.assertIsNone(event['old_path'])
        self.assertIsInstance(event['timestamp'], float)
    
    def test_queue_event_with_old_path(self):
        """Test that move events include old path."""
        self.handler._queue_event('moved', '/new/path.md', '/old/path.md')
        
        event = self.event_queue.get_nowait()
        self.assertEqual(event['type'], 'moved')
        self.assertEqual(event['file_path'], '/new/path.md')
        self.assertEqual(event['old_path'], '/old/path.md')
    
    def test_queue_event_full_queue(self):
        """Test behavior when queue is full."""
        # Create a small queue and fill it
        small_queue = queue.Queue(maxsize=1)
        handler = ScribeEventHandler(small_queue, ['*.md'])
        
        # Fill the queue
        handler._queue_event('test1', '/path1.md')
        self.assertEqual(small_queue.qsize(), 1)
        
        # Try to add another event (should be dropped)
        # The queue should still have only 1 item (second event dropped)
        handler._queue_event('test2', '/path2.md')
        self.assertEqual(small_queue.qsize(), 1)
        
        # Verify the first event is still there
        event = small_queue.get_nowait()
        self.assertEqual(event['type'], 'test1')
    
    @patch('watchdog.events.FileSystemEvent')
    def test_on_modified_processes_matching_files(self, mock_event):
        """Test that on_modified processes matching files."""
        mock_event.is_directory = False
        mock_event.src_path = '/path/to/test.md'
        
        self.handler.on_modified(mock_event)
        
        self.assertEqual(self.event_queue.qsize(), 1)
        event = self.event_queue.get_nowait()
        self.assertEqual(event['type'], 'modified')
        self.assertEqual(event['file_path'], '/path/to/test.md')
    
    @patch('watchdog.events.FileSystemEvent')
    def test_on_modified_ignores_directories(self, mock_event):
        """Test that on_modified ignores directory events."""
        mock_event.is_directory = True
        mock_event.src_path = '/path/to/directory'
        
        self.handler.on_modified(mock_event)
        
        self.assertEqual(self.event_queue.qsize(), 0)
    
    @patch('watchdog.events.FileSystemEvent')
    def test_on_modified_ignores_non_matching_files(self, mock_event):
        """Test that on_modified ignores non-matching files."""
        mock_event.is_directory = False
        mock_event.src_path = '/path/to/test.py'
        
        self.handler.on_modified(mock_event)
        
        self.assertEqual(self.event_queue.qsize(), 0)


class TestWatcher(unittest.TestCase):
    """Test the Watcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.event_queue = queue.Queue()
        self.shutdown_event = threading.Event()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_watcher_initialization(self):
        """Test that watcher initializes correctly."""
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir],
            file_patterns=['*.md']
        )
        
        self.assertEqual(watcher.watch_paths, [self.temp_dir])
        self.assertEqual(watcher.file_patterns, ['*.md'])
        self.assertIs(watcher.event_queue, self.event_queue)
        self.assertIs(watcher.shutdown_event, self.shutdown_event)
    
    def test_watcher_default_patterns(self):
        """Test that watcher uses default patterns when none provided."""
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir]
        )
        
        self.assertEqual(watcher.file_patterns, ['*.md'])
    
    def test_watcher_thread_properties(self):
        """Test that watcher has correct thread properties."""
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir]
        )
        
        self.assertEqual(watcher.name, "ScribeWatcher")
        self.assertTrue(watcher.daemon)
    
    def test_watcher_shutdown_signal(self):
        """Test that watcher respects shutdown signal."""
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir]
        )
        
        # Start the watcher
        watcher.start()
        
        # Give it a moment to start
        time.sleep(0.1)
        
        # Signal shutdown
        self.shutdown_event.set()
        
        # Wait for it to stop
        watcher.join(timeout=5.0)
        
        # Verify it stopped
        self.assertFalse(watcher.is_alive())
    
    def test_watcher_nonexistent_path_handling(self):
        """Test that watcher handles nonexistent paths gracefully."""
        nonexistent_path = '/this/path/does/not/exist'
        
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[nonexistent_path]
        )
        
        # Start and quickly stop
        watcher.start()
        time.sleep(0.1)
        self.shutdown_event.set()
        watcher.join(timeout=5.0)
        
        # Watcher should stop gracefully even with nonexistent path
        self.assertFalse(watcher.is_alive())


if __name__ == '__main__':
    unittest.main() 