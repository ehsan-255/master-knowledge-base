"""
Unit tests for the Scribe Worker (Consumer Thread).

These tests verify the worker functionality in isolation.
"""

import unittest
import threading
import queue
import time
import os
from unittest.mock import Mock, patch

# Add the scribe module to the path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'scribe'))

from worker import Worker


class TestWorker(unittest.TestCase):
    """Test the Worker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.event_queue = queue.Queue()
        self.shutdown_event = threading.Event()
    
    def test_worker_initialization(self):
        """Test that worker initializes correctly."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=2.0
        )
        
        self.assertIs(worker.event_queue, self.event_queue)
        self.assertIs(worker.shutdown_event, self.shutdown_event)
        self.assertEqual(worker.queue_timeout, 2.0)
        self.assertEqual(worker.events_processed, 0)
        self.assertEqual(worker.events_failed, 0)
        self.assertIsNone(worker.start_time)
    
    def test_worker_default_timeout(self):
        """Test that worker uses default timeout when none provided."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        self.assertEqual(worker.queue_timeout, 1.0)
    
    def test_worker_thread_properties(self):
        """Test that worker has correct thread properties."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        self.assertEqual(worker.name, "ScribeWorker")
        self.assertTrue(worker.daemon)
    
    def test_worker_processes_single_event(self):
        """Test that worker processes a single event correctly."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        # Add an event to the queue
        test_event = {
            'type': 'modified',
            'file_path': '/test/file.md',
            'timestamp': time.time()
        }
        self.event_queue.put(test_event)
        
        # Start worker
        worker.start()
        
        # Give it time to process the event
        time.sleep(0.2)
        
        # Stop worker
        self.shutdown_event.set()
        worker.join(timeout=5.0)
        
        # Verify event was processed
        self.assertEqual(worker.events_processed, 1)
        self.assertEqual(worker.events_failed, 0)
        self.assertEqual(self.event_queue.qsize(), 0)
    
    def test_worker_processes_multiple_events(self):
        """Test that worker processes multiple events correctly."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        # Add multiple events to the queue
        for i in range(3):
            test_event = {
                'type': 'modified',
                'file_path': f'/test/file{i}.md',
                'timestamp': time.time()
            }
            self.event_queue.put(test_event)
        
        # Start worker
        worker.start()
        
        # Give it time to process all events
        time.sleep(0.5)
        
        # Stop worker
        self.shutdown_event.set()
        worker.join(timeout=5.0)
        
        # Verify all events were processed
        self.assertEqual(worker.events_processed, 3)
        self.assertEqual(worker.events_failed, 0)
        self.assertEqual(self.event_queue.qsize(), 0)
    
    def test_worker_shutdown_signal(self):
        """Test that worker respects shutdown signal."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        # Start the worker
        worker.start()
        
        # Give it a moment to start
        time.sleep(0.1)
        
        # Signal shutdown
        self.shutdown_event.set()
        
        # Wait for it to stop
        worker.join(timeout=5.0)
        
        # Verify it stopped
        self.assertFalse(worker.is_alive())
    
    def test_worker_handles_empty_queue(self):
        """Test that worker handles empty queue gracefully."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        # Start worker with empty queue
        worker.start()
        
        # Let it run for a bit with empty queue
        time.sleep(0.3)
        
        # Stop worker
        self.shutdown_event.set()
        worker.join(timeout=5.0)
        
        # Verify no events were processed (queue was empty)
        self.assertEqual(worker.events_processed, 0)
        self.assertEqual(worker.events_failed, 0)
    
    def test_worker_get_stats(self):
        """Test that worker returns correct statistics."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        # Set some test values
        worker.start_time = time.time() - 10  # 10 seconds ago
        worker.events_processed = 5
        worker.events_failed = 1
        
        stats = worker.get_stats()
        
        self.assertAlmostEqual(stats['uptime_seconds'], 10, delta=1)
        self.assertEqual(stats['events_processed'], 5)
        self.assertEqual(stats['events_failed'], 1)
        self.assertEqual(stats['total_events'], 6)
        self.assertAlmostEqual(stats['success_rate'], 83.33, delta=0.1)
        self.assertEqual(stats['queue_size'], 0)
    
    def test_worker_get_stats_no_events(self):
        """Test that worker returns correct statistics when no events processed."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        worker.start_time = time.time()
        
        stats = worker.get_stats()
        
        self.assertEqual(stats['events_processed'], 0)
        self.assertEqual(stats['events_failed'], 0)
        self.assertEqual(stats['total_events'], 0)
        self.assertEqual(stats['success_rate'], 0.0)
    
    def test_worker_process_event_success(self):
        """Test that _process_event handles valid events correctly."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        test_event = {
            'type': 'modified',
            'file_path': '/test/file.md',
            'timestamp': time.time()
        }
        
        # Process the event directly
        worker._process_event(test_event)
        
        # Verify statistics were updated
        self.assertEqual(worker.events_processed, 1)
        self.assertEqual(worker.events_failed, 0)
    
    def test_worker_process_event_missing_fields(self):
        """Test that _process_event handles events with missing fields."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        # Event with missing fields
        test_event = {}
        
        # Process the event directly
        worker._process_event(test_event)
        
        # Should still process successfully (uses defaults)
        self.assertEqual(worker.events_processed, 1)
        self.assertEqual(worker.events_failed, 0)
    
    @patch('time.sleep')
    def test_worker_process_event_exception_handling(self, mock_sleep):
        """Test that _process_event handles exceptions correctly."""
        # Make time.sleep raise an exception to simulate processing error
        mock_sleep.side_effect = Exception("Test exception")
        
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        test_event = {
            'type': 'modified',
            'file_path': '/test/file.md',
            'timestamp': time.time()
        }
        
        # Process the event directly
        worker._process_event(test_event)
        
        # Verify failure was recorded
        self.assertEqual(worker.events_processed, 0)
        self.assertEqual(worker.events_failed, 1)
    
    def test_worker_log_final_stats(self):
        """Test that _log_final_stats works correctly."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        worker.start_time = time.time() - 5  # 5 seconds ago
        worker.events_processed = 10
        worker.events_failed = 2
        
        # This should not raise an exception
        worker._log_final_stats()
    
    def test_worker_log_final_stats_no_start_time(self):
        """Test that _log_final_stats handles missing start_time."""
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event
        )
        
        # start_time is None
        worker.events_processed = 5
        worker.events_failed = 1
        
        # This should not raise an exception
        worker._log_final_stats()


if __name__ == '__main__':
    unittest.main() 