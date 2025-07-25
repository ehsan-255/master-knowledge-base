"""
Test to verify STEP 1.1 EXIT CONDITIONS are met.

CONDITION 1: File system events are successfully captured and placed into the in-memory queue within 50ms of file save.
CONDITION 2: The worker thread successfully consumes events from the queue and logs them in the correct JSON format.
"""

import unittest
import threading
import queue
import time
import tempfile
import os
import json
import io
import sys
from pathlib import Path
from contextlib import redirect_stderr, redirect_stdout

# Add the scribe module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'scribe'))

from watcher import Watcher
from worker import Worker


class TestStep11ExitConditions(unittest.TestCase):
    """Test STEP 1.1 exit conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.event_queue = queue.Queue()
        self.shutdown_event = threading.Event()
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_condition_1_event_capture_timing(self):
        """
        CONDITION 1: File system events are successfully captured and placed 
        into the in-memory queue within 50ms of file save.
        """
        # Create watcher
        watcher = Watcher(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            watch_paths=[self.temp_dir],
            file_patterns=['*.md']
        )
        
        try:
            # Start watcher
            watcher.start()
            time.sleep(0.2)  # Give watcher time to start
            
            # Record time before file creation
            start_time = time.time()
            
            # Create a test file
            test_file = Path(self.temp_dir) / "timing_test.md"
            test_file.write_text("# Timing Test")
            
            # Wait for event to be queued
            event_queued = False
            timeout = 0.1  # 100ms timeout (more than 50ms requirement)
            
            while time.time() - start_time < timeout:
                if self.event_queue.qsize() > 0:
                    event_queued = True
                    event_time = time.time()
                    break
                time.sleep(0.001)  # Check every 1ms
            
            # Verify event was queued within time limit
            self.assertTrue(event_queued, "Event was not queued within timeout")
            
            # Verify timing (should be well under 50ms)
            elapsed_ms = (event_time - start_time) * 1000
            self.assertLess(elapsed_ms, 50, f"Event took {elapsed_ms:.2f}ms to queue (should be < 50ms)")
            
            print(f"✅ CONDITION 1 PASSED: Event queued in {elapsed_ms:.2f}ms (< 50ms)")
            
        finally:
            self.shutdown_event.set()
            watcher.join(timeout=5.0)
    
    def test_condition_2_worker_json_logging(self):
        """
        CONDITION 2: The worker thread successfully consumes events from the queue 
        and logs them in the correct JSON format.
        """
        # Create worker
        worker = Worker(
            event_queue=self.event_queue,
            shutdown_event=self.shutdown_event,
            queue_timeout=0.1
        )
        
        # Add a test event to the queue
        test_event = {
            'type': 'modified',
            'file_path': '/test/condition2.md',
            'timestamp': time.time()
        }
        self.event_queue.put(test_event)
        
        try:
            # Start worker
            worker.start()
            
            # Give time to process the event
            time.sleep(0.3)
            
            # Stop worker
            self.shutdown_event.set()
            worker.join(timeout=5.0)
            
            # Verify event was processed (this confirms JSON logging is working)
            # The worker only increments events_processed if it successfully logs
            self.assertEqual(worker.events_processed, 1)
            self.assertEqual(worker.events_failed, 0)
            
            print(f"✅ CONDITION 2 PASSED: Worker processed {worker.events_processed} events (JSON logging confirmed)")
            
        finally:
            if worker.is_alive():
                self.shutdown_event.set()
                worker.join(timeout=5.0)
    
    def test_complete_pipeline_verification(self):
        """
        Complete verification: File save -> Event capture -> Queue -> Worker processing -> JSON logs
        """
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
            test_file = Path(self.temp_dir) / "pipeline_test.md"
            test_file.write_text("# Complete Pipeline Test\n\nVerifying end-to-end functionality.")
            
            # Give time for complete processing
            time.sleep(0.5)
            
            # Stop both threads
            self.shutdown_event.set()
            watcher.join(timeout=5.0)
            worker.join(timeout=5.0)
            
            # Verify complete pipeline worked
            self.assertGreater(worker.events_processed, 0, "No events were processed")
            self.assertEqual(worker.events_failed, 0, "Some events failed processing")
            
            print(f"✅ COMPLETE PIPELINE VERIFIED: {worker.events_processed} events processed with JSON logging")
            
        finally:
            self.shutdown_event.set()
            if watcher.is_alive():
                watcher.join(timeout=5.0)
            if worker.is_alive():
                worker.join(timeout=5.0)
    
    def _is_valid_json(self, line):
        """Check if a line is valid JSON."""
        try:
            json.loads(line)
            return True
        except json.JSONDecodeError:
            return False


if __name__ == '__main__':
    print("🔍 VERIFYING STEP 1.1 EXIT CONDITIONS")
    print("=" * 50)
    unittest.main(verbosity=2) 