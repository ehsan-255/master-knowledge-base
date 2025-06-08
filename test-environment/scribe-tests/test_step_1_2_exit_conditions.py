"""
STEP 1.2 Exit Conditions Verification Test Suite

This module verifies all exit conditions for STEP 1.2: Foundational Reliability & Observability.
All conditions must pass for STEP 1.2 to be considered complete.
"""

import unittest
import tempfile
import time
import json
import requests
from pathlib import Path
from unittest.mock import patch
import sys
import io
import contextlib

# Add the scribe module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "scribe"))

from engine import ScribeEngine
from core.atomic_write import atomic_write
from core.logging_config import configure_structured_logging, get_scribe_logger


class TestStep12ExitConditions(unittest.TestCase):
    """
    Comprehensive test suite for STEP 1.2 exit conditions.
    
    STEP 1.2 EXIT CONDITIONS:
    1. A test confirms that a simulated interruption during a file write does not result in a corrupted file.
    2. Logs for at least 5 different event types are captured and validated against the JSON log schema.
    3. The /health endpoint is accessible via curl and returns a 200 OK with a valid JSON payload.
    """
    
    def setUp(self):
        """Set up test environment."""
        # Configure logging for tests
        configure_structured_logging(log_level="INFO")
        
        # Create temporary directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Use unique port for testing
        self.test_port = 9471
        
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
    
    def test_condition_1_atomic_write_crash_safety(self):
        """
        CONDITION 1: A test confirms that a simulated interruption during a file write 
        does not result in a corrupted file.
        """
        print("\n🧪 Testing CONDITION 1: Atomic Write Crash Safety")
        
        test_file = self.temp_path / "condition_1_test.txt"
        original_content = "Original file content that must be preserved during interruption"
        corrupted_content = "This content should NEVER appear if atomic write works correctly"
        
        # Create original file
        test_file.write_text(original_content)
        original_size = test_file.stat().st_size
        original_mtime = test_file.stat().st_mtime
        
        # Simulate interruption by mocking the rename operation
        with patch('core.atomic_write.Path.rename') as mock_rename:
            mock_rename.side_effect = KeyboardInterrupt("Simulated power loss during rename")
            
            # Attempt write that will be interrupted
            result = atomic_write(test_file, corrupted_content)
            
            # Verify write failed
            self.assertFalse(result, "Atomic write should fail when interrupted")
            
            # CRITICAL: Verify file is not corrupted
            self.assertTrue(test_file.exists(), "Original file must still exist")
            self.assertEqual(test_file.read_text(), original_content, 
                           "Original file content must be unchanged")
            self.assertEqual(test_file.stat().st_size, original_size,
                           "Original file size must be unchanged")
            self.assertEqual(test_file.stat().st_mtime, original_mtime,
                           "Original file modification time must be unchanged")
            
            # Verify no partial writes or corruption
            self.assertNotIn("This content should NEVER appear", test_file.read_text(),
                           "Corrupted content must not appear in file")
        
        print("✅ CONDITION 1 PASSED: Simulated interruption does not corrupt files")
        return True
    
    def test_condition_2_structured_logging_validation(self):
        """
        CONDITION 2: Logs for at least 5 different event types are captured and 
        validated against the JSON log schema.
        """
        print("\n🧪 Testing CONDITION 2: Structured Logging Validation")
        
        # Capture log output
        log_capture = io.StringIO()
        
        # Create engine to generate various log events
        self.engine = ScribeEngine(
            watch_paths=[str(self.temp_path)],
            file_patterns=['*.md'],
            health_port=self.test_port
        )
        
        # Redirect logging to capture
        import logging
        import structlog
        
        # Configure structlog to output to our capture
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        # Capture stdout to get JSON logs
        with contextlib.redirect_stdout(log_capture):
            try:
                # Start engine (generates multiple log events)
                self.engine.start()
                time.sleep(1.0)
                
                # Create test files to generate file system events
                for i in range(3):
                    test_file = self.temp_path / f"test_log_{i}.md"
                    test_file.write_text(f"# Test File {i}\n\nContent for logging test")
                    time.sleep(0.1)
                
                # Give time for events to be processed
                time.sleep(1.0)
                
                # Make health request to generate HTTP log events
                try:
                    health_url = f"http://localhost:{self.test_port}/health"
                    requests.get(health_url, timeout=2.0)
                except:
                    pass  # Don't fail if health request fails
                
                time.sleep(0.5)
                
            finally:
                # Stop engine
                if self.engine:
                    self.engine.stop()
        
        # Parse captured logs
        log_output = log_capture.getvalue()
        log_lines = [line.strip() for line in log_output.split('\n') if line.strip()]
        
        # Validate JSON logs
        valid_json_logs = []
        event_types = set()
        
        for line in log_lines:
            try:
                log_entry = json.loads(line)
                valid_json_logs.append(log_entry)
                
                # Extract event type
                if 'event' in log_entry:
                    event_types.add(log_entry['event'])
                elif 'logger' in log_entry:
                    event_types.add(f"logger_{log_entry['logger']}")
                
                # Validate required JSON schema fields
                self.assertIn('timestamp', log_entry, "Log entry must have timestamp")
                self.assertIn('level', log_entry, "Log entry must have level")
                
            except json.JSONDecodeError:
                # Skip non-JSON lines
                continue
        
        # Verify we have at least 5 different event types
        self.assertGreaterEqual(len(event_types), 5, 
                              f"Must have at least 5 event types, found: {event_types}")
        
        # Verify we have valid JSON logs
        self.assertGreater(len(valid_json_logs), 0, "Must have valid JSON log entries")
        
        print(f"✅ CONDITION 2 PASSED: Found {len(event_types)} event types in {len(valid_json_logs)} JSON logs")
        print(f"   Event types: {sorted(event_types)}")
        return True
    
    def test_condition_3_health_endpoint_accessibility(self):
        """
        CONDITION 3: The /health endpoint is accessible via curl and returns a 200 OK 
        with a valid JSON payload.
        """
        print("\n🧪 Testing CONDITION 3: Health Endpoint Accessibility")
        
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
        self.assertEqual(response.status_code, 200, "Health endpoint must return 200 OK")
        
        # CRITICAL: Verify valid JSON payload
        try:
            health_data = response.json()
        except json.JSONDecodeError:
            self.fail("Health endpoint response is not valid JSON")
        
        # Verify required JSON structure
        required_fields = ['status', 'timestamp', 'uptime_seconds', 'queue_size']
        for field in required_fields:
            self.assertIn(field, health_data, f"Health response missing required field: {field}")
        
        # Verify status is healthy
        self.assertEqual(health_data['status'], 'healthy', "Engine status must be healthy")
        
        # Verify numeric fields are valid
        self.assertIsInstance(health_data['uptime_seconds'], (int, float), 
                            "uptime_seconds must be numeric")
        self.assertIsInstance(health_data['queue_size'], int, 
                            "queue_size must be integer")
        self.assertIsInstance(health_data['timestamp'], (int, float), 
                            "timestamp must be numeric")
        
        print(f"✅ CONDITION 3 PASSED: Health endpoint accessible at {health_url}")
        print(f"   Status: {health_data['status']}, Uptime: {health_data['uptime_seconds']}s")
        
        # Stop engine
        self.engine.stop()
        return True
    
    def test_all_step_1_2_exit_conditions(self):
        """
        Comprehensive test that verifies ALL STEP 1.2 exit conditions.
        This is the definitive test for STEP 1.2 completion.
        """
        print("\n" + "="*80)
        print("🎯 STEP 1.2 EXIT CONDITIONS VERIFICATION")
        print("   Testing all conditions for: Foundational Reliability & Observability")
        print("="*80)
        
        # Track condition results
        results = {}
        
        try:
            # Test Condition 1: Atomic Write Crash Safety
            results['condition_1'] = self.test_condition_1_atomic_write_crash_safety()
            
            # Test Condition 2: Structured Logging Validation  
            results['condition_2'] = self.test_condition_2_structured_logging_validation()
            
            # Test Condition 3: Health Endpoint Accessibility
            results['condition_3'] = self.test_condition_3_health_endpoint_accessibility()
            
        except Exception as e:
            print(f"❌ STEP 1.2 EXIT CONDITIONS FAILED: {e}")
            raise
        
        # Verify all conditions passed
        all_passed = all(results.values())
        
        if all_passed:
            print("\n" + "="*80)
            print("🎉 STEP 1.2 EXIT CONDITIONS: ALL PASSED")
            print("✅ CONDITION 1: Atomic write crash safety verified")
            print("✅ CONDITION 2: Structured logging with 5+ event types validated")
            print("✅ CONDITION 3: Health endpoint accessible with 200 OK + JSON")
            print("\n🚀 STEP 1.2: FOUNDATIONAL RELIABILITY & OBSERVABILITY COMPLETE")
            print("="*80)
        else:
            failed_conditions = [k for k, v in results.items() if not v]
            print(f"\n❌ STEP 1.2 EXIT CONDITIONS FAILED: {failed_conditions}")
            self.fail(f"STEP 1.2 exit conditions failed: {failed_conditions}")
        
        return all_passed


if __name__ == '__main__':
    unittest.main(verbosity=2) 