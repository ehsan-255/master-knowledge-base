"""
Test suite for atomic write functionality.

This module tests the crash-safe atomic write operations to ensure
that file writes are truly atomic and handle interruptions gracefully.
"""

import unittest
import tempfile
import os
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add the scribe module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "scribe"))

from core.atomic_write import atomic_write, atomic_write_json, atomic_write_yaml
from core.logging_config import configure_structured_logging


class TestAtomicWrite(unittest.TestCase):
    """Test cases for atomic write functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Configure logging for tests
        configure_structured_logging(log_level="DEBUG")
        
        # Create temporary directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
    def tearDown(self):
        """Clean up test environment."""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_basic_text_write(self):
        """Test basic text file writing."""
        test_file = self.temp_path / "test_basic.txt"
        test_content = "Hello, World!\nThis is a test file."
        
        # Write the file
        result = atomic_write(test_file, test_content)
        
        # Verify success
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        
        # Verify content
        with open(test_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, test_content)
    
    def test_basic_binary_write(self):
        """Test basic binary file writing."""
        test_file = self.temp_path / "test_binary.bin"
        test_content = b"Binary content\x00\x01\x02\x03"
        
        # Write the file
        result = atomic_write(test_file, test_content, mode='wb')
        
        # Verify success
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        
        # Verify content
        with open(test_file, 'rb') as f:
            content = f.read()
        self.assertEqual(content, test_content)
    
    def test_overwrite_existing_file(self):
        """Test overwriting an existing file."""
        test_file = self.temp_path / "test_overwrite.txt"
        
        # Create initial file
        initial_content = "Initial content"
        test_file.write_text(initial_content)
        self.assertEqual(test_file.read_text(), initial_content)
        
        # Overwrite with atomic write
        new_content = "New content that replaces the old"
        result = atomic_write(test_file, new_content)
        
        # Verify success and content
        self.assertTrue(result)
        self.assertEqual(test_file.read_text(), new_content)
    
    def test_directory_creation(self):
        """Test that parent directories are created if they don't exist."""
        nested_file = self.temp_path / "nested" / "deep" / "test.txt"
        test_content = "Content in nested directory"
        
        # Verify directory doesn't exist
        self.assertFalse(nested_file.parent.exists())
        
        # Write file (should create directories)
        result = atomic_write(nested_file, test_content)
        
        # Verify success
        self.assertTrue(result)
        self.assertTrue(nested_file.exists())
        self.assertEqual(nested_file.read_text(), test_content)
    
    def test_invalid_mode(self):
        """Test that invalid modes raise ValueError."""
        test_file = self.temp_path / "test_invalid.txt"
        
        with self.assertRaises(ValueError):
            atomic_write(test_file, "content", mode='invalid')
    
    def test_json_write(self):
        """Test atomic JSON writing."""
        test_file = self.temp_path / "test.json"
        test_data = {
            "name": "test",
            "value": 42,
            "nested": {"key": "value"},
            "list": [1, 2, 3]
        }
        
        # Write JSON
        result = atomic_write_json(test_file, test_data)
        
        # Verify success
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        
        # Verify content
        import json
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, test_data)
    
    def test_yaml_write(self):
        """Test atomic YAML writing."""
        test_file = self.temp_path / "test.yaml"
        test_data = {
            "name": "test",
            "value": 42,
            "nested": {"key": "value"},
            "list": [1, 2, 3]
        }
        
        # Write YAML
        result = atomic_write_yaml(test_file, test_data)
        
        # Verify success
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        
        # Verify content
        import yaml
        with open(test_file, 'r') as f:
            loaded_data = yaml.safe_load(f)
        self.assertEqual(loaded_data, test_data)
    
    def test_interruption_during_write_critical_test(self):
        """
        CRITICAL TEST: Inject exception between temp file write and rename.
        
        This test verifies the core safety guarantee of atomic writes:
        if the process is interrupted after writing the temp file but before
        the rename, the original file remains unchanged and temp files are cleaned up.
        """
        test_file = self.temp_path / "test_interruption.txt"
        original_content = "Original content that must remain unchanged"
        new_content = "New content that should not appear"
        
        # Create original file
        test_file.write_text(original_content)
        original_mtime = test_file.stat().st_mtime
        
        # Mock os.rename to raise an exception (simulating interruption)
        with patch('core.atomic_write.Path.rename') as mock_rename:
            mock_rename.side_effect = OSError("Simulated interruption during rename")
            
            # Attempt atomic write (should fail)
            result = atomic_write(test_file, new_content)
            
            # Verify write failed
            self.assertFalse(result)
            
            # CRITICAL ASSERTION: Original file must be unchanged
            self.assertTrue(test_file.exists())
            self.assertEqual(test_file.read_text(), original_content)
            
            # Verify original file wasn't modified
            current_mtime = test_file.stat().st_mtime
            self.assertEqual(current_mtime, original_mtime)
            
            # Verify no temporary files remain
            temp_files = list(self.temp_path.glob("*.tmp.*"))
            temp_files.extend(list(self.temp_path.glob(".*tmp*")))
            temp_files.extend(list(self.temp_path.glob("*.atomic")))
            
            self.assertEqual(len(temp_files), 0, 
                           f"Temporary files not cleaned up: {temp_files}")
    
    def test_interruption_during_fsync(self):
        """Test interruption during fsync operation."""
        test_file = self.temp_path / "test_fsync_interruption.txt"
        original_content = "Original content"
        new_content = "New content"
        
        # Create original file
        test_file.write_text(original_content)
        
        # Mock os.fsync to raise an exception
        with patch('core.atomic_write.os.fsync') as mock_fsync:
            mock_fsync.side_effect = OSError("Simulated fsync failure")
            
            # Attempt atomic write (should fail)
            result = atomic_write(test_file, new_content)
            
            # Verify write failed
            self.assertFalse(result)
            
            # Verify original file is unchanged
            self.assertTrue(test_file.exists())
            self.assertEqual(test_file.read_text(), original_content)
    
    def test_interruption_during_temp_file_creation(self):
        """Test interruption during temporary file creation."""
        test_file = self.temp_path / "test_temp_creation.txt"
        original_content = "Original content"
        new_content = "New content"
        
        # Create original file
        test_file.write_text(original_content)
        
        # Mock tempfile.mkstemp to raise an exception
        with patch('core.atomic_write.tempfile.mkstemp') as mock_mkstemp:
            mock_mkstemp.side_effect = OSError("Cannot create temporary file")
            
            # Attempt atomic write (should fail)
            result = atomic_write(test_file, new_content)
            
            # Verify write failed
            self.assertFalse(result)
            
            # Verify original file is unchanged
            self.assertTrue(test_file.exists())
            self.assertEqual(test_file.read_text(), original_content)
    
    def test_concurrent_writes_safety(self):
        """Test that concurrent writes don't interfere with each other."""
        import threading
        import time
        
        test_file = self.temp_path / "test_concurrent.txt"
        results = []
        
        def write_worker(content, delay=0):
            if delay:
                time.sleep(delay)
            result = atomic_write(test_file, content)
            results.append((content, result))
        
        # Start multiple concurrent writes
        threads = []
        for i in range(5):
            content = f"Content from thread {i}"
            thread = threading.Thread(target=write_worker, args=(content, i * 0.01))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all writes succeeded
        for content, result in results:
            self.assertTrue(result, f"Write failed for content: {content}")
        
        # Verify file exists and has valid content
        self.assertTrue(test_file.exists())
        final_content = test_file.read_text()
        
        # Final content should be from one of the threads
        thread_contents = [f"Content from thread {i}" for i in range(5)]
        self.assertIn(final_content, thread_contents)
    
    def test_large_file_write(self):
        """Test writing a large file to verify performance and reliability."""
        test_file = self.temp_path / "test_large.txt"
        
        # Create large content (1MB)
        large_content = "A" * (1024 * 1024)
        
        # Write large file
        start_time = time.time()
        result = atomic_write(test_file, large_content)
        write_time = time.time() - start_time
        
        # Verify success
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        
        # Verify content
        self.assertEqual(test_file.read_text(), large_content)
        
        # Verify reasonable performance (should complete in under 5 seconds)
        self.assertLess(write_time, 5.0, f"Large file write took too long: {write_time}s")
    
    def test_unicode_content(self):
        """Test writing Unicode content."""
        test_file = self.temp_path / "test_unicode.txt"
        unicode_content = "Hello 世界! 🌍 Ñoño café résumé"
        
        # Write Unicode content
        result = atomic_write(test_file, unicode_content)
        
        # Verify success
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        
        # Verify content
        self.assertEqual(test_file.read_text(encoding='utf-8'), unicode_content)


class TestAtomicWriteExitConditions(unittest.TestCase):
    """Test the specific exit conditions for STEP 1.2."""
    
    def setUp(self):
        """Set up test environment."""
        configure_structured_logging(log_level="DEBUG")
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_step_1_2_condition_1_simulated_interruption(self):
        """
        STEP 1.2 EXIT CONDITION 1: A test confirms that a simulated interruption 
        during a file write does not result in a corrupted file.
        """
        test_file = self.temp_path / "condition_1_test.txt"
        original_content = "Original file content that must be preserved"
        corrupted_content = "This content should never appear in the file"
        
        # Create original file
        test_file.write_text(original_content)
        original_size = test_file.stat().st_size
        original_mtime = test_file.stat().st_mtime
        
        # Simulate interruption by mocking the rename operation
        with patch('core.atomic_write.Path.rename') as mock_rename:
            mock_rename.side_effect = KeyboardInterrupt("Simulated power loss")
            
            # Attempt write that will be interrupted
            result = atomic_write(test_file, corrupted_content)
            
            # Verify write failed
            self.assertFalse(result)
            
            # CRITICAL: Verify file is not corrupted
            self.assertTrue(test_file.exists())
            self.assertEqual(test_file.read_text(), original_content)
            self.assertEqual(test_file.stat().st_size, original_size)
            self.assertEqual(test_file.stat().st_mtime, original_mtime)
            
            # Verify no partial writes or corruption
            self.assertNotIn("This content should never appear", test_file.read_text())
        
        print("✅ CONDITION 1 PASSED: Simulated interruption does not corrupt files")


if __name__ == '__main__':
    unittest.main() 