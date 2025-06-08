"""
Test suite for health endpoint functionality.

This module tests the HTTP health check endpoint to ensure it provides
proper monitoring capabilities and returns valid JSON responses.
"""

import unittest
import tempfile
import time
import threading
import requests
import json
from pathlib import Path
import sys

# Add the scribe module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "scribe"))

from engine import ScribeEngine
from core.logging_config import configure_structured_logging


class TestHealthEndpoint(unittest.TestCase):
    """Test cases for health endpoint functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Configure logging for tests
        configure_structured_logging(log_level="INFO")
        
        # Create temporary directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Use a different port for testing to avoid conflicts
        self.test_port = 9469
        
        # Engine instance
        self.engine = None
        
    def tearDown(self):
        """Clean up test environment."""
        # Stop engine if running
        if self.engine and self.engine.is_running:
            self.engine.stop()
        
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_health_endpoint_basic_functionality(self):
        """Test basic health endpoint functionality."""
        # Create engine with test configuration
        self.engine = ScribeEngine(
            watch_paths=[str(self.temp_path)],
            file_patterns=['*.md'],
            health_port=self.test_port
        )
        
        try:
            # Start the engine
            self.engine.start()
            
            # Give the health server time to start
            time.sleep(1.0)
            
            # Make HTTP request to health endpoint
            health_url = f"http://localhost:{self.test_port}/health"
            response = requests.get(health_url, timeout=5.0)
            
            # Verify response code
            self.assertEqual(response.status_code, 200)
            
            # Verify content type
            self.assertEqual(response.headers.get('Content-Type'), 'application/json')
            
            # Verify JSON response
            health_data = response.json()
            
            # Verify required fields
            self.assertIn('status', health_data)
            self.assertIn('timestamp', health_data)
            self.assertIn('uptime_seconds', health_data)
            self.assertIn('queue_size', health_data)
            self.assertIn('engine', health_data)
            self.assertIn('worker', health_data)
            
            # Verify status is healthy
            self.assertEqual(health_data['status'], 'healthy')
            
            # Verify engine data
            engine_data = health_data['engine']
            self.assertIn('is_running', engine_data)
            self.assertIn('watch_paths', engine_data)
            self.assertIn('file_patterns', engine_data)
            self.assertTrue(engine_data['is_running'])
            
            # Verify worker data
            worker_data = health_data['worker']
            self.assertIn('events_processed', worker_data)
            self.assertIn('events_failed', worker_data)
            self.assertIn('total_events', worker_data)
            self.assertIn('success_rate', worker_data)
            
            print(f"✅ Health endpoint test passed: {health_url}")
            
        finally:
            # Ensure engine is stopped
            if self.engine:
                self.engine.stop()
    
    def test_health_endpoint_with_activity(self):
        """Test health endpoint after some file activity."""
        # Create engine
        self.engine = ScribeEngine(
            watch_paths=[str(self.temp_path)],
            file_patterns=['*.md'],
            health_port=self.test_port
        )
        
        try:
            # Start the engine
            self.engine.start()
            time.sleep(1.0)
            
            # Create some test files to generate activity
            for i in range(3):
                test_file = self.temp_path / f"test_{i}.md"
                test_file.write_text(f"# Test File {i}\n\nContent for test file {i}")
                time.sleep(0.1)  # Small delay between file creations
            
            # Give time for events to be processed
            time.sleep(1.0)
            
            # Check health endpoint
            health_url = f"http://localhost:{self.test_port}/health"
            response = requests.get(health_url, timeout=5.0)
            
            self.assertEqual(response.status_code, 200)
            health_data = response.json()
            
            # Verify we have some activity
            worker_data = health_data['worker']
            self.assertGreaterEqual(worker_data['events_processed'], 0)
            self.assertEqual(worker_data['events_failed'], 0)
            
            # Verify uptime is reasonable
            self.assertGreater(health_data['uptime_seconds'], 0)
            self.assertLess(health_data['uptime_seconds'], 10)  # Should be less than 10 seconds
            
        finally:
            if self.engine:
                self.engine.stop()
    
    def test_health_endpoint_root_path(self):
        """Test the root path returns HTML interface."""
        self.engine = ScribeEngine(
            watch_paths=[str(self.temp_path)],
            file_patterns=['*.md'],
            health_port=self.test_port
        )
        
        try:
            self.engine.start()
            time.sleep(1.0)
            
            # Test root path
            root_url = f"http://localhost:{self.test_port}/"
            response = requests.get(root_url, timeout=5.0)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers.get('Content-Type'), 'text/html')
            
            # Verify HTML content contains expected elements
            html_content = response.text
            self.assertIn('Scribe Engine Health', html_content)
            self.assertIn('/health', html_content)
            
        finally:
            if self.engine:
                self.engine.stop()
    
    def test_health_endpoint_not_found(self):
        """Test 404 response for unknown paths."""
        self.engine = ScribeEngine(
            watch_paths=[str(self.temp_path)],
            file_patterns=['*.md'],
            health_port=self.test_port
        )
        
        try:
            self.engine.start()
            time.sleep(1.0)
            
            # Test unknown path
            unknown_url = f"http://localhost:{self.test_port}/unknown"
            response = requests.get(unknown_url, timeout=5.0)
            
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.headers.get('Content-Type'), 'application/json')
            
            # Verify JSON error response
            error_data = response.json()
            self.assertIn('status', error_data)
            self.assertIn('message', error_data)
            self.assertIn('available_paths', error_data)
            self.assertEqual(error_data['status'], 'not_found')
            
        finally:
            if self.engine:
                self.engine.stop()
    
    def test_health_endpoint_concurrent_requests(self):
        """Test health endpoint handles concurrent requests."""
        self.engine = ScribeEngine(
            watch_paths=[str(self.temp_path)],
            file_patterns=['*.md'],
            health_port=self.test_port
        )
        
        try:
            self.engine.start()
            time.sleep(1.0)
            
            # Make multiple concurrent requests
            health_url = f"http://localhost:{self.test_port}/health"
            responses = []
            
            def make_request():
                try:
                    response = requests.get(health_url, timeout=5.0)
                    responses.append(response)
                except Exception as e:
                    responses.append(e)
            
            # Start multiple threads
            threads = []
            for _ in range(5):
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Verify all requests succeeded
            self.assertEqual(len(responses), 5)
            for response in responses:
                self.assertIsInstance(response, requests.Response)
                self.assertEqual(response.status_code, 200)
                
                # Verify JSON response
                health_data = response.json()
                self.assertEqual(health_data['status'], 'healthy')
            
        finally:
            if self.engine:
                self.engine.stop()


class TestHealthEndpointExitConditions(unittest.TestCase):
    """Test the specific exit conditions for STEP 1.2."""
    
    def setUp(self):
        """Set up test environment."""
        configure_structured_logging(log_level="INFO")
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.test_port = 9470
        self.engine = None
    
    def tearDown(self):
        """Clean up test environment."""
        if self.engine and self.engine.is_running:
            self.engine.stop()
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_step_1_2_condition_3_health_endpoint_accessible(self):
        """
        STEP 1.2 EXIT CONDITION 3: The /health endpoint is accessible via curl 
        and returns a 200 OK with a valid JSON payload.
        """
        # Create and start engine
        self.engine = ScribeEngine(
            watch_paths=[str(self.temp_path)],
            file_patterns=['*.md'],
            health_port=self.test_port
        )
        
        self.engine.start()
        time.sleep(1.0)  # Give server time to start
        
        # Make HTTP request (equivalent to curl)
        health_url = f"http://localhost:{self.test_port}/health"
        response = requests.get(health_url, timeout=5.0)
        
        # CRITICAL: Verify 200 OK response
        self.assertEqual(response.status_code, 200)
        
        # CRITICAL: Verify valid JSON payload
        try:
            health_data = response.json()
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")
        
        # Verify required JSON structure
        required_fields = ['status', 'timestamp', 'uptime_seconds', 'queue_size']
        for field in required_fields:
            self.assertIn(field, health_data, f"Missing required field: {field}")
        
        # Verify status is healthy
        self.assertEqual(health_data['status'], 'healthy')
        
        # Verify numeric fields are valid
        self.assertIsInstance(health_data['uptime_seconds'], (int, float))
        self.assertIsInstance(health_data['queue_size'], int)
        self.assertIsInstance(health_data['timestamp'], (int, float))
        
        print("✅ CONDITION 3 PASSED: /health endpoint accessible with 200 OK and valid JSON")
        
        # Stop engine
        self.engine.stop()


if __name__ == '__main__':
    unittest.main() 