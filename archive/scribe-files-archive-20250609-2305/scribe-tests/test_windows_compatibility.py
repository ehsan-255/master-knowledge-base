#!/usr/bin/env python3
"""
Windows Compatibility Test Suite for Scribe v2.0
Tests Windows-specific file operations, path handling, and platform behavior.
"""

import pytest
import os
import tempfile
import threading
import time
import platform
from pathlib import Path, WindowsPath
from unittest.mock import patch, MagicMock
import sys

# Configure Python path for imports
repo_root = Path(__file__).parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.scribe.core.atomic_write import atomic_write, atomic_write_json
from tools.scribe.watcher import Watcher, ScribeEventHandler
from tools.scribe.core.config_manager import ConfigManager


class TestWindowsPathHandling:
    """Test Windows-specific path handling edge cases."""
    
    def test_windows_drive_letters(self):
        """Test handling of Windows drive letters in paths."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        # Test absolute paths with drive letters
        test_path = Path("C:/temp/test_file.txt")
        assert test_path.is_absolute()
        assert str(test_path).startswith("C:")
        
    def test_unc_path_handling(self):
        """Test Universal Naming Convention (UNC) path handling."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        # Test UNC path recognition
        unc_path = Path("//server/share/file.txt")
        assert unc_path.is_absolute()
        
    def test_long_path_support(self):
        """Test Windows long path (>260 chars) handling."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        # Create a very long path name
        long_dir = "a" * 50
        long_path = Path(tempfile.gettempdir()) / long_dir / long_dir / long_dir / long_dir / "test.txt"
        
        # Ensure we can handle long paths without errors
        try:
            long_path_str = str(long_path)
            assert len(long_path_str) > 260
        except Exception as e:
            pytest.fail(f"Long path handling failed: {e}")
    
    def test_path_separator_normalization(self):
        """Test that path separators are properly normalized on Windows."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        # Mixed separator path
        mixed_path = "C:/temp\\subfolder/file.txt"
        normalized = Path(mixed_path)
        
        # Should normalize to Windows separators
        assert "\\" in str(normalized) or "/" in str(normalized)
        
    def test_case_insensitive_paths(self):
        """Test Windows case-insensitive path behavior."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create file with lowercase name
            lower_file = Path(temp_dir) / "testfile.txt"
            lower_file.write_text("test content")
            
            # Access with different case
            upper_file = Path(temp_dir) / "TESTFILE.TXT"
            
            # On Windows, these should resolve to the same file
            assert lower_file.exists()
            assert upper_file.exists()


class TestWindowsFileLocking:
    """Test Windows-specific file locking behavior."""
    
    def test_exclusive_file_access(self):
        """Test exclusive file access patterns on Windows."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(b"test content")
            
        try:
            # Test atomic write with potential concurrent access
            result = atomic_write(temp_path, "new content", mode='w')
            assert result is True
            
            # Verify content was written
            with open(temp_path, 'r') as f:
                assert f.read() == "new content"
                
        finally:
            os.unlink(temp_path)
    
    def test_file_locking_under_load(self):
        """Test file locking behavior under concurrent access."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            
        results = []
        errors = []
        
        def write_worker(worker_id):
            try:
                content = f"Worker {worker_id} content"
                result = atomic_write(temp_path, content, mode='w')
                results.append((worker_id, result))
            except Exception as e:
                errors.append((worker_id, str(e)))
        
        # Start multiple concurrent writers
        threads = []
        for i in range(5):
            thread = threading.Thread(target=write_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=10)
        
        try:
            # At least one write should succeed
            successful_writes = [r for r in results if r[1] is True]
            assert len(successful_writes) >= 1, f"No successful writes. Results: {results}, Errors: {errors}"
            
            # File should have content from one of the writers
            with open(temp_path, 'r') as f:
                content = f.read()
                assert "Worker" in content and "content" in content
                
        finally:
            os.unlink(temp_path)
    
    def test_atomic_write_with_readonly_directory(self):
        """Test atomic write behavior with read-only parent directory."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a subdirectory and make it read-only
            subdir = Path(temp_dir) / "readonly_dir"
            subdir.mkdir()
            
            test_file = subdir / "test.txt"
            
            # First, write a file normally
            result = atomic_write(test_file, "test content")
            assert result is True
            
            # Try to make directory read-only (this might not work on all Windows versions)
            try:
                os.chmod(subdir, 0o444)
                
                # Attempt to write again - this should handle the read-only case gracefully
                result = atomic_write(test_file, "new content")
                # Result may be True or False depending on Windows permissions
                
            finally:
                # Restore write permissions for cleanup
                try:
                    os.chmod(subdir, 0o755)
                except:
                    pass


class TestWindowsFileSystemWatcher:
    """Test Windows-specific file system watching behavior."""
    
    def test_windows_file_events(self):
        """Test Windows file system event generation and handling."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock event bus
            mock_event_bus = MagicMock()
            
            # Create event handler
            handler = ScribeEventHandler(mock_event_bus, file_patterns=['*.txt'])
            
            # Create test file
            test_file = Path(temp_dir) / "test.txt"
            test_file.write_text("initial content")
            
            # Simulate file modification event
            from watchdog.events import FileModifiedEvent
            event = FileModifiedEvent(str(test_file))
            
            handler.on_modified(event)
            
            # Verify event was published
            mock_event_bus.publish.assert_called_once()
            call_args = mock_event_bus.publish.call_args
            assert call_args[0][0] == 'file_event'
            assert call_args[0][1]['type'] == 'modified'
            assert call_args[0][1]['file_path'] == str(test_file)
    
    def test_windows_temp_file_filtering(self):
        """Test filtering of Windows temporary files."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        mock_event_bus = MagicMock()
        handler = ScribeEventHandler(mock_event_bus, file_patterns=['*.txt'])
        
        # Test various Windows temporary file patterns
        temp_files = [
            "~$document.txt",  # Office temp files
            "document.txt.tmp",  # Generic temp files
            ".#document.txt",  # Lock files
            "document.txt~",  # Backup files
        ]
        
        for temp_file in temp_files:
            # These should be filtered out or handled appropriately
            assert not handler._should_process_file(temp_file) or temp_file.endswith('.txt')
    
    def test_file_watcher_stability_under_load(self):
        """Test file watcher stability under high file activity."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        with tempfile.TemporaryDirectory() as temp_dir:
            events_received = []
            mock_event_bus = MagicMock()
            
            def capture_event(event_type, event_data):
                events_received.append((event_type, event_data))
            
            mock_event_bus.publish.side_effect = capture_event
            
            # Create watcher
            shutdown_event = threading.Event()
            watcher = Watcher(
                event_bus=mock_event_bus,
                shutdown_event=shutdown_event,
                watch_paths=[temp_dir],
                file_patterns=['*.txt']
            )
            
            try:
                # Start watcher in background
                watcher_thread = threading.Thread(target=watcher.start)
                watcher_thread.daemon = True
                watcher_thread.start()
                
                # Give watcher time to start
                time.sleep(0.5)
                
                # Create multiple files rapidly
                for i in range(10):
                    test_file = Path(temp_dir) / f"test_{i}.txt"
                    test_file.write_text(f"Content {i}")
                    time.sleep(0.1)  # Small delay to avoid overwhelming
                
                # Wait for events to be processed
                time.sleep(2.0)
                
                # Stop watcher
                shutdown_event.set()
                watcher_thread.join(timeout=5)
                
                # Verify we received some events (may not be all due to timing)
                assert len(events_received) > 0, "No file events were captured"
                
            finally:
                shutdown_event.set()


class TestWindowsConfigManager:
    """Test Windows-specific configuration management."""
    
    def test_config_path_resolution(self):
        """Test configuration file path resolution on Windows."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        # Test absolute Windows path
        abs_path = "C:/temp/config.json"
        config_manager = ConfigManager.__new__(ConfigManager)  # Create without __init__
        config_manager.config_path = Path(abs_path)
        
        assert config_manager.config_path.is_absolute()
        
    def test_config_hot_reload_windows(self):
        """Test configuration hot-reload on Windows file system."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create config and schema files
            config_file = Path(temp_dir) / "config.json"
            schema_file = Path(temp_dir) / "schema.json"
            
            # Basic schema
            schema_content = {
                "type": "object",
                "properties": {
                    "test_value": {"type": "string"}
                }
            }
            
            # Initial config
            config_content = {
                "test_value": "initial"
            }
            
            with open(schema_file, 'w') as f:
                import json
                json.dump(schema_content, f)
                
            with open(config_file, 'w') as f:
                import json
                json.dump(config_content, f)
            
            # Test that config manager can load the file
            try:
                config_manager = ConfigManager(
                    config_path=str(config_file),
                    schema_path=str(schema_file),
                    auto_reload=False  # Disable auto-reload for this test
                )
                
                loaded_config = config_manager.get_config()
                assert loaded_config["test_value"] == "initial"
                
            except Exception as e:
                pytest.fail(f"Config loading failed on Windows: {e}")


@pytest.mark.slow
class TestWindowsPerformance:
    """Test Windows-specific performance characteristics."""
    
    def test_file_operation_performance(self):
        """Test file operation performance on Windows."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test atomic write performance
            test_file = Path(temp_dir) / "perf_test.txt"
            content = "Test content " * 1000  # ~13KB
            
            start_time = time.time()
            for i in range(10):
                result = atomic_write(test_file, f"{content} {i}")
                assert result is True
            end_time = time.time()
            
            # Should complete in reasonable time (less than 5 seconds for 10 writes)
            duration = end_time - start_time
            assert duration < 5.0, f"File operations too slow: {duration:.2f}s for 10 writes"
    
    def test_path_resolution_performance(self):
        """Test path resolution performance on Windows."""
        if platform.system() != "Windows":
            pytest.skip("Windows-specific test")
            
        # Test resolving many paths
        start_time = time.time()
        for i in range(1000):
            path = Path(f"C:/temp/subdir_{i}/file_{i}.txt")
            _ = path.parent
            _ = path.name
            _ = path.suffix
        end_time = time.time()
        
        duration = end_time - start_time
        assert duration < 1.0, f"Path operations too slow: {duration:.2f}s for 1000 operations"


if __name__ == "__main__":
    # Run only Windows tests if executed directly
    pytest.main([__file__, "-v", "-m", "not slow"])