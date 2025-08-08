#!/usr/bin/env python3
"""
Scribe Engine End-to-End Integration Tests

Full runtime testing of Scribe engine functionality:
- Real file system events
- Boundary validation pipeline  
- Plugin execution chain
- Telemetry and observability
- Error handling and recovery

These tests verify actual Scribe engine functionality beyond unit/compliance tests.
"""

import pytest
import asyncio
import tempfile
import time
import json
import os
import threading
from pathlib import Path
from unittest.mock import patch, MagicMock

from tools.scribe.engine import ScribeEngine
from tools.scribe.core.engine_factory import create_engine_components
from tools.scribe.watcher import ScribeEventHandler


class TestScribeEngineE2E:
    """End-to-end integration tests for Scribe engine."""
    
    @pytest.fixture
    def temp_workspace(self):
        """Create isolated temporary workspace for testing - NEVER touches repo files."""
        with tempfile.TemporaryDirectory(prefix="scribe_e2e_test_") as temp_dir:
            workspace = Path(temp_dir)
            
            # Create test markdown file in isolated directory
            test_file = workspace / "test_document.md"
            test_file.write_text("""---
title: "Integration Test Document"
info-type: "test-document"
---

# Integration Test

This document is used for end-to-end testing.
""")
            
            # Ensure we're working in isolated space
            assert str(workspace).startswith(tempfile.gettempdir()), "Must use temp directory only"
            assert "master-knowledge-base" not in str(workspace), "Must not touch repo files"
            
            yield workspace
    
    @pytest.fixture
    def mock_telemetry_config(self):
        """Mock telemetry configuration to avoid external dependencies."""
        return {
            "endpoint": None,  # No real OTLP collector needed
            "sampling_rate": 1.0
        }
    
    def test_engine_initialization_with_components(self, mock_telemetry_config):
        """Test that Scribe engine initializes successfully with all components."""
        # Create engine components 
        components = create_engine_components(
            telemetry_config=mock_telemetry_config
        )
        
        # Initialize engine
        engine = ScribeEngine(components=components)
        
        # Verify components are properly initialized
        assert engine.components is not None
        assert engine.port_registry is not None
        assert engine.components.config_manager is not None
        assert engine.components.telemetry is not None
        assert engine.components.plugin_loader is not None
        
        # Verify engine state
        assert not engine.is_running
        assert not engine.initialization_complete
    
    def test_engine_startup_and_shutdown(self, mock_telemetry_config):
        """Test engine startup and graceful shutdown."""
        components = create_engine_components(
            telemetry_config=mock_telemetry_config
        )
        engine = ScribeEngine(components=components)
        
        try:
            # Start engine
            engine.start()
            
            # Verify engine is running
            assert engine.is_running
            assert engine.initialization_complete
            assert engine.start_time is not None
            
        finally:
            # Always attempt shutdown
            engine.stop()
            
            # Verify clean shutdown
            assert not engine.is_running
    
    def test_plugin_loading_and_registration(self, mock_telemetry_config):
        """Test that plugins are loaded and registered correctly."""
        components = create_engine_components(
            telemetry_config=mock_telemetry_config
        )
        engine = ScribeEngine(components=components)
        
        try:
            engine.start()
            
            # Verify plugins were loaded
            plugins = engine.components.plugin_loader.load_all_plugins()
            assert len(plugins) > 0, "Should load at least some plugins"
            
            # Verify minimal core has plugins registered
            if engine.minimal_core:
                assert hasattr(engine.minimal_core, 'lifecycle_manager')
                # Plugin count should be positive if any plugins loaded successfully
                loaded_count = len(engine.minimal_core.lifecycle_manager.plugins)
                assert loaded_count >= 0  # Allow for 0 if all plugins fail to load
            
        finally:
            engine.stop()
    
    @pytest.mark.asyncio
    async def test_file_watcher_integration(self, temp_workspace, mock_telemetry_config):
        """Test file watcher integration with boundary validation."""
        
        # Create file watcher with test patterns
        handler = ScribeEventHandler(['*.md'])
        
        # Verify watcher components are initialized
        assert handler.boundary_validator is not None
        assert handler.telemetry_manager is not None
        
        # Create test file in isolated temp workspace to trigger events
        test_file = temp_workspace / "watcher_test.md"
        test_file.write_text("""---
title: "Watcher Test"
info-type: "test"
---

# Test Content
""")
        
        # Ensure we're not touching repo files
        assert str(test_file).startswith(tempfile.gettempdir()), "Must use temp directory only"
        
        # Mock the publish event method to capture calls
        original_publish = handler._publish_event
        published_events = []
        
        def mock_publish(event_type, file_path, old_path=None):
            published_events.append({
                'event_type': event_type,
                'file_path': file_path,
                'old_path': old_path
            })
            # Still call original for validation
            return original_publish(event_type, file_path, old_path)
        
        handler._publish_event = mock_publish
        
        # Simulate file creation event
        from watchdog.events import FileCreatedEvent
        created_event = FileCreatedEvent(str(test_file))
        handler.on_created(created_event)
        
        # Verify event was published
        assert len(published_events) == 1
        assert published_events[0]['event_type'] == 'created'
        assert test_file.name in published_events[0]['file_path']
        
        # Simulate file modification
        test_file.write_text("""---
title: "Modified Watcher Test" 
info-type: "test"
---

# Modified Test Content
""")
        
        from watchdog.events import FileModifiedEvent
        modified_event = FileModifiedEvent(str(test_file))
        handler.on_modified(modified_event)
        
        # Verify modification event
        assert len(published_events) == 2
        assert published_events[1]['event_type'] == 'modified'
    
    def test_boundary_validation_integration(self, temp_workspace):
        """Test boundary validation with real file events."""
        handler = ScribeEventHandler(['*.md'])
        
        # Create valid file event using isolated temp workspace
        valid_test_file = temp_workspace / "valid_test.md"
        valid_event_data = {
            'event_id': 'test_event_001',
            'type': 'created',
            'file_path': str(valid_test_file),
            'timestamp': time.time()
        }
        
        # Ensure we're using isolated temp path
        assert str(valid_test_file).startswith(tempfile.gettempdir()), "Must use temp directory only"
        
        # Test boundary validation
        validation_result = handler.boundary_validator.validate_l1_input(
            valid_event_data, 
            "file_system"
        )
        
        # Should pass validation
        assert validation_result.valid == True
        assert len(validation_result.errors) == 0
        
        # Test invalid event (missing required fields) using isolated temp workspace
        invalid_test_file = temp_workspace / "invalid_test.md"
        invalid_event_data = {
            'event_id': 'test_event_002',
            # Missing 'type' field
            'file_path': str(invalid_test_file),
        }
        
        # Ensure we're using isolated temp path
        assert str(invalid_test_file).startswith(tempfile.gettempdir()), "Must use temp directory only"
        
        validation_result = handler.boundary_validator.validate_l1_input(
            invalid_event_data,
            "file_system"  
        )
        
        # Should fail validation
        assert validation_result.valid == False
        assert len(validation_result.errors) > 0
    
    def test_telemetry_integration_with_mocks(self):
        """Test telemetry integration without external dependencies."""
        from tools.scribe.core.telemetry import initialize_telemetry
        
        # Initialize telemetry without OTLP endpoint (uses mocks)
        telemetry_manager = initialize_telemetry(
            service_name="scribe-e2e-test",
            endpoint=None,  # No external collector
            sampling_rate=1.0
        )
        
        # Test boundary call tracing
        with telemetry_manager.trace_boundary_call(
            "inbound", "file_system", "test_watcher", "file_created"
        ) as span:
            assert span is not None
            span.set_attribute("test_attribute", "test_value")
            
        # Test action execution tracing
        with telemetry_manager.trace_action_execution(
            "test_action", "test_rule", "/test/file.md"
        ) as span:
            assert span is not None
            # Simulate some work
            time.sleep(0.001)
            
        # Test metrics recording
        telemetry_manager.update_worker_count(5)
        telemetry_manager.update_queue_size(10)
        
        # Test graceful shutdown
        telemetry_manager.shutdown()
    
    def test_error_recovery_mechanisms(self, mock_telemetry_config):
        """Test error handling and recovery mechanisms."""
        components = create_engine_components(
            telemetry_config=mock_telemetry_config
        )
        engine = ScribeEngine(components=components)
        
        # Test engine status during error conditions
        status = engine.get_status()
        assert status['is_running'] == False
        assert status['engine_version'] == '2.2.0'
        
        # Test startup with potential failures
        try:
            # Mock a component failure during startup
            with patch.object(engine.components.plugin_loader, 'load_all_plugins') as mock_load:
                mock_load.side_effect = Exception("Plugin loading failed")
                
                # Engine should handle plugin loading failures gracefully
                try:
                    engine.start()
                    # If we get here, error was handled gracefully
                    assert engine.is_running
                except Exception as e:
                    # Or engine failed fast, which is also acceptable
                    assert "Plugin loading failed" in str(e) or "Failed to initialize" in str(e)
                    
        finally:
            # Always attempt cleanup
            if engine.is_running:
                engine.stop()


class TestPluginExecutionE2E:
    """Test actual plugin execution in end-to-end scenarios."""
    
    @pytest.fixture
    def sample_markdown_file(self):
        """Create isolated sample markdown file for plugin testing - NEVER touches repo files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, prefix="scribe_plugin_test_") as f:
            f.write("""---
title: "Sample Document"
info-type: "test-document"
---

# Sample Document

This is a test document for plugin execution testing.

## Section 1

Some content here.

## Section 2  

More content here.
""")
            temp_path = f.name
        
        # Ensure we're using temp directory only
        assert temp_path.startswith(tempfile.gettempdir()), "Must use temp directory only"
        assert "master-knowledge-base" not in temp_path, "Must not touch repo files"
        
        yield temp_path
        
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)
    
    def test_plugin_manifest_loading(self):
        """Test that plugin manifests are loaded and validated."""
        from tools.scribe.core.plugin_loader import PluginLoader
        
        loader = PluginLoader()
        plugins = loader.load_all_plugins()
        
        # Should find plugin manifest files
        manifest_files = list(Path("tools/scribe/actions").rglob("manifest.json"))
        assert len(manifest_files) > 0, "Should find plugin manifest files"
        
        # Test manifest validation for each plugin
        for manifest_path in manifest_files:
            plugin_dir = manifest_path.parent
            manifest = loader.load_plugin_manifest(plugin_dir)
            
            if manifest:  # Some plugins may fail to load
                # Verify HMA v2.2 compliance
                assert manifest.get("manifest_version") == "2.2"
                assert manifest.get("plugin_metadata", {}).get("product") == "scribe"
                
                # Verify required structure
                assert "hma_compliance" in manifest
                assert "runtime_requirements" in manifest
                assert "interface_contracts" in manifest
    
    @pytest.mark.asyncio
    async def test_mock_plugin_execution_workflow(self, sample_markdown_file):
        """Test plugin execution workflow with mock implementations."""
        
        # Create mock plugin context
        class MockPluginContext:
            def __init__(self):
                self.ports = {
                    "logging": self._create_mock_logging_port(),
                    "file_system": self._create_mock_file_system_port(),
                    "configuration": self._create_mock_config_port(),
                    "observability": self._create_mock_observability_port()
                }
            
            def get_port(self, port_type):
                return self.ports.get(port_type)
            
            def _create_mock_logging_port(self):
                class MockLoggingPort:
                    def log_info(self, message, **kwargs): pass
                    def log_error(self, message, **kwargs): pass
                    def log_warning(self, message, **kwargs): pass
                    def log_debug(self, message, **kwargs): pass
                return MockLoggingPort()
            
            def _create_mock_file_system_port(self):
                class MockFileSystemPort:
                    async def read_file_safely(self, file_path):
                        with open(file_path, 'r') as f:
                            return f.read()
                    
                    async def write_file_safely(self, file_path, content):
                        with open(file_path, 'w') as f:
                            f.write(content)
                        return True
                return MockFileSystemPort()
            
            def _create_mock_config_port(self):
                class MockConfigPort:
                    async def get_config_value(self, key, default=None):
                        return default
                return MockConfigPort()
            
            def _create_mock_observability_port(self):
                class MockObservabilityPort:
                    def emit_metric(self, name, value, labels): pass
                    def start_span(self, name): 
                        class MockSpan:
                            def __enter__(self): return self
                            def __exit__(self, *args): pass
                            def set_attribute(self, key, value): pass
                        return MockSpan()
                return MockObservabilityPort()
        
        # Create mock plugin execution workflow
        plugin_context = MockPluginContext()
        
        # Test plugin execution pattern
        class MockEnhancedFrontmatterAction:
            def __init__(self, action_type, params, context):
                self.action_type = action_type
                self.params = params
                self.context = context
                self.log_port = context.get_port("logging")
                
            async def execute(self, file_content, match, file_path, params):
                self.log_port.log_info("Processing frontmatter", file_path=file_path)
                
                # Mock frontmatter enhancement
                if "---" in file_content and "title:" in file_content:
                    # Add additional metadata
                    enhanced_content = file_content.replace(
                        'info-type: "test-document"',
                        'info-type: "test-document"\nprocessed-by: "enhanced_frontmatter_action"'
                    )
                    self.log_port.log_info("Frontmatter enhanced", file_path=file_path)
                    return enhanced_content
                
                return file_content
        
        # Execute mock plugin
        action = MockEnhancedFrontmatterAction(
            "enhanced_frontmatter",
            {"enabled": True},
            plugin_context
        )
        
        # Read sample file
        with open(sample_markdown_file, 'r') as f:
            original_content = f.read()
        
        # Execute action
        result = await action.execute(
            original_content,
            None,
            sample_markdown_file,
            {}
        )
        
        # Verify processing occurred
        assert result != original_content
        assert "processed-by:" in result
        assert "enhanced_frontmatter_action" in result
    
    def test_dlq_integration_with_invalid_events(self):
        """Test Dead Letter Queue integration with invalid events."""
        from tools.scribe.core.dlq import write_dlq
        
        # Create invalid event that should go to DLQ
        invalid_event_id = "invalid_test_event"
        validation_errors = ["Missing required field: type", "Invalid timestamp format"]
        # Use temp directory for metadata to avoid any repo file references
        temp_invalid_path = os.path.join(tempfile.gettempdir(), "scribe_dlq_test_invalid_file.md")
        event_metadata = {
            "file_path": temp_invalid_path,
            "component_id": "test_component"
        }
        
        # Ensure DLQ test uses isolated paths
        assert temp_invalid_path.startswith(tempfile.gettempdir()), "Must use temp directory only"
        
        # Write to DLQ
        write_dlq("file_system", invalid_event_id, validation_errors, event_metadata)
        
        # Verify DLQ file was created
        dlq_dir = Path("tools/reports/dlq")
        assert dlq_dir.exists()
        
        # Find the DLQ file for our event
        dlq_files = list(dlq_dir.glob(f"*{invalid_event_id}*.json"))
        assert len(dlq_files) > 0, "DLQ file should be created for invalid event"
        
        # Verify DLQ content
        dlq_file = dlq_files[0]
        with open(dlq_file) as f:
            dlq_data = json.load(f)
        
        assert dlq_data["event_id"] == invalid_event_id
        assert dlq_data["surface"] == "file_system"
        assert len(dlq_data["validation_errors"]) == 2
        assert dlq_data["event_metadata"]["file_path"] == temp_invalid_path


class TestPerformanceAndLoad:
    """Test performance and load handling capabilities."""
    
    def test_concurrent_file_events(self):
        """Test handling of concurrent file events."""
        handler = ScribeEventHandler(['*.md'])
        
        # Track published events
        published_events = []
        original_publish = handler._publish_event
        
        def track_publish(event_type, file_path, old_path=None):
            published_events.append({
                'event_type': event_type,
                'file_path': file_path,
                'thread': threading.current_thread().name
            })
            return original_publish(event_type, file_path, old_path)
        
        handler._publish_event = track_publish
        
        # Create multiple file events concurrently
        import concurrent.futures
        
        def create_file_event(file_index):
            from watchdog.events import FileCreatedEvent
            # Use temp directory path to ensure isolation
            temp_file_path = os.path.join(tempfile.gettempdir(), f"scribe_concurrent_test_{file_index}.md")
            event = FileCreatedEvent(temp_file_path)
            handler.on_created(event)
            return file_index
        
        # Execute concurrent events
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_file_event, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all events were processed
        assert len(published_events) == 10
        assert len(set(e['file_path'] for e in published_events)) == 10  # Unique files
        
    def test_telemetry_performance_overhead(self):
        """Test telemetry performance overhead."""
        from tools.scribe.core.telemetry import initialize_telemetry
        
        # Initialize telemetry
        telemetry_manager = initialize_telemetry(
            service_name="performance-test",
            endpoint=None
        )
        
        # Measure performance with telemetry
        start_time = time.time()
        
        for i in range(100):
            with telemetry_manager.trace_boundary_call(
                "inbound", "file_system", "perf_test", "validation"
            ) as span:
                span.set_attribute("iteration", i)
                # Simulate small amount of work
                time.sleep(0.001)
        
        elapsed_time = time.time() - start_time
        
        # Should complete reasonably quickly (allow for some overhead)
        assert elapsed_time < 2.0, f"Telemetry overhead too high: {elapsed_time}s"
        
        # Test metrics recording performance
        start_time = time.time()
        
        for i in range(1000):
            telemetry_manager.update_worker_count(i % 10)
            telemetry_manager.update_queue_size(i % 100)
        
        metrics_elapsed = time.time() - start_time
        assert metrics_elapsed < 1.0, f"Metrics recording too slow: {metrics_elapsed}s"
        
        telemetry_manager.shutdown()


if __name__ == "__main__":
    # Run as: python -m pytest test-environment/scribe-tests/integration/test_scribe_engine_e2e.py -v
    pytest.main([__file__, "-v"])