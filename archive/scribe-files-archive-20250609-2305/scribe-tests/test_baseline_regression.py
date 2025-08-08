#!/usr/bin/env python3
"""
Baseline Regression Test Suite for Scribe v2.0
Protects existing functionality during refactoring phases.
"""

import pytest
import os
import tempfile
import json
import time
import threading
from pathlib import Path
from unittest.mock import MagicMock, patch
import sys

# Configure Python path for imports
repo_root = Path(__file__).parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.scribe.engine import ScribeEngine
from tools.scribe.core.config_manager import ConfigManager
from tools.scribe.core.action_dispatcher import ActionDispatcher
from tools.scribe.actions.base import BaseAction


class TestCoreEngineRegression:
    """Test core engine functionality remains intact."""
    
    def test_engine_initialization(self):
        """Test that engine initializes without errors."""
        engine = ScribeEngine(
            watch_paths=["."],
            file_patterns=["*.md"],
            queue_maxsize=100,
            health_port=9469  # Use different port to avoid conflicts
        )
        
        assert engine.watch_paths == ["."]
        assert engine.file_patterns == ["*.md"]
        assert engine.is_running is False
        
    def test_engine_start_stop_cycle(self):
        """Test engine can start and stop cleanly."""
        engine = ScribeEngine(
            watch_paths=["."],
            file_patterns=["*.md"],
            queue_maxsize=100,
            health_port=9470
        )
        
        try:
            # Start engine
            start_thread = threading.Thread(target=engine.start)
            start_thread.daemon = True
            start_thread.start()
            
            # Give it time to start
            time.sleep(1.0)
            assert engine.is_running is True
            
            # Stop engine
            engine.stop()
            
            # Wait for cleanup
            start_thread.join(timeout=5)
            assert engine.is_running is False
            
        except Exception as e:
            pytest.fail(f"Engine start/stop cycle failed: {e}")
        finally:
            if engine.is_running:
                engine.stop()
    
    def test_engine_status_reporting(self):
        """Test engine status reporting functionality."""
        engine = ScribeEngine(
            watch_paths=["."],
            file_patterns=["*.md"],
            health_port=9471
        )
        
        status = engine.get_status()
        
        # Verify status structure
        assert 'is_running' in status
        assert 'uptime_seconds' in status
        assert 'queue_size' in status
        assert 'watch_paths' in status
        assert 'file_patterns' in status
        
        # Verify values
        assert status['is_running'] is False
        assert status['watch_paths'] == ["."]
        assert status['file_patterns'] == ["*.md"]


class TestConfigManagerRegression:
    """Test configuration management functionality."""
    
    def test_config_loading_basic(self):
        """Test basic configuration loading."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create minimal config files
            config_file = Path(temp_dir) / "config.json"
            schema_file = Path(temp_dir) / "schema.json"
            
            # Minimal schema
            schema = {
                "type": "object",
                "properties": {
                    "test_field": {"type": "string"}
                }
            }
            
            # Minimal config
            config = {
                "test_field": "test_value"
            }
            
            with open(schema_file, 'w') as f:
                json.dump(schema, f)
                
            with open(config_file, 'w') as f:
                json.dump(config, f)
            
            # Test loading
            config_manager = ConfigManager(
                config_path=str(config_file),
                schema_path=str(schema_file),
                auto_reload=False
            )
            
            loaded_config = config_manager.get_config()
            assert loaded_config["test_field"] == "test_value"
    
    def test_config_validation_errors(self):
        """Test config validation error handling."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "config.json"
            schema_file = Path(temp_dir) / "schema.json"
            
            # Schema requiring string
            schema = {
                "type": "object",
                "properties": {
                    "required_field": {"type": "string"}
                },
                "required": ["required_field"]
            }
            
            # Config missing required field
            config = {
                "other_field": "value"
            }
            
            with open(schema_file, 'w') as f:
                json.dump(schema, f)
                
            with open(config_file, 'w') as f:
                json.dump(config, f)
            
            # Should raise validation error
            with pytest.raises(Exception):  # Could be jsonschema.ValidationError or similar
                ConfigManager(
                    config_path=str(config_file),
                    schema_path=str(schema_file),
                    auto_reload=False
                )


class TestActionSystemRegression:
    """Test action plugin system functionality."""
    
    def test_base_action_interface(self):
        """Test BaseAction interface remains stable."""
        # Create a minimal action implementation
        class TestAction(BaseAction):
            def execute(self, file_content, match, file_path, params):
                return file_content + " [modified]"
            
            def get_required_params(self):
                return ["test_param"]
            
            def get_description(self):
                return "Test action"
        
        # Mock dependencies
        mock_config = MagicMock()
        mock_security = MagicMock()
        
        # Test action instantiation
        action = TestAction("test_action", {"test_param": "value"}, mock_config, mock_security)
        
        assert action.action_type == "test_action"
        assert action.params == {"test_param": "value"}
        assert action.get_required_params() == ["test_param"]
        assert action.get_description() == "Test action"
        
        # Test execution
        import re
        mock_match = re.match(r"test", "test")
        result = action.execute("original content", mock_match, "/test/path", {"test_param": "value"})
        assert result == "original content [modified]"
    
    def test_action_dispatcher_initialization(self):
        """Test ActionDispatcher can be initialized."""
        mock_plugin_loader = MagicMock()
        mock_config_manager = MagicMock()
        mock_security_manager = MagicMock()
        
        dispatcher = ActionDispatcher(
            plugin_loader=mock_plugin_loader,
            config_manager=mock_config_manager,
            security_manager=mock_security_manager,
            quarantine_path="test/quarantine"
        )
        
        assert dispatcher.quarantine_path == "test/quarantine"
        assert dispatcher.plugin_loader == mock_plugin_loader
        assert dispatcher.config_manager == mock_config_manager
        assert dispatcher.security_manager == mock_security_manager
    
    def test_action_dispatcher_stats(self):
        """Test ActionDispatcher statistics functionality."""
        mock_plugin_loader = MagicMock()
        mock_plugin_loader.get_all_plugins.return_value = {"test_action": "test_plugin"}
        
        mock_config_manager = MagicMock()
        mock_security_manager = MagicMock()
        
        dispatcher = ActionDispatcher(
            plugin_loader=mock_plugin_loader,
            config_manager=mock_config_manager,
            security_manager=mock_security_manager
        )
        
        stats = dispatcher.get_execution_stats()
        
        # Verify stats structure
        assert 'total_dispatches' in stats
        assert 'successful_dispatches' in stats
        assert 'failed_dispatches' in stats
        assert 'success_rate' in stats
        assert 'available_action_types' in stats
        
        # Initial values should be zero/empty
        assert stats['total_dispatches'] == 0
        assert stats['successful_dispatches'] == 0
        assert stats['failed_dispatches'] == 0
        assert stats['success_rate'] == 0.0


class TestFileOperationsRegression:
    """Test file operation functionality."""
    
    def test_atomic_write_basic(self):
        """Test basic atomic write functionality."""
        from tools.scribe.core.atomic_write import atomic_write
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            
        try:
            # Test successful write
            result = atomic_write(temp_path, "test content", mode='w')
            assert result is True
            
            # Verify content
            with open(temp_path, 'r') as f:
                content = f.read()
                assert content == "test content"
                
        finally:
            os.unlink(temp_path)
    
    def test_atomic_write_json(self):
        """Test atomic JSON write functionality."""
        from tools.scribe.core.atomic_write import atomic_write_json
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
            temp_path = temp_file.name
            
        try:
            test_data = {"key": "value", "number": 42}
            
            # Test JSON write
            result = atomic_write_json(temp_path, test_data)
            assert result is True
            
            # Verify JSON content
            with open(temp_path, 'r') as f:
                loaded_data = json.load(f)
                assert loaded_data == test_data
                
        finally:
            os.unlink(temp_path)


class TestEventSystemRegression:
    """Test event handling system functionality."""
    
    def test_event_bus_basic(self):
        """Test basic event bus functionality."""
        from tools.scribe.core.event_bus import EventBus
        
        event_bus = EventBus(maxsize=100)
        
        # Test basic event publishing and subscribing
        events_received = []
        
        def test_handler(event_type, event_data):
            events_received.append((event_type, event_data))
        
        event_bus.subscribe("test_event", test_handler)
        event_bus.publish("test_event", {"test": "data"})
        
        # Process events
        event_bus.process_events()
        
        # Verify event was received
        assert len(events_received) == 1
        assert events_received[0][0] == "test_event"
        assert events_received[0][1] == {"test": "data"}
    
    def test_watcher_event_generation(self):
        """Test file watcher event generation."""
        from tools.scribe.watcher import ScribeEventHandler
        
        mock_event_bus = MagicMock()
        handler = ScribeEventHandler(mock_event_bus, file_patterns=['*.txt'])
        
        # Test should_process_file
        assert handler._should_process_file("test.txt") is True
        assert handler._should_process_file("test.md") is False
        assert handler._should_process_file("test.py") is False
        
        # Test event queueing
        handler._queue_event("modified", "/test/path.txt")
        
        # Verify event was published
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args
        assert call_args[0][0] == 'file_event'
        assert call_args[0][1]['type'] == 'modified'
        assert call_args[0][1]['file_path'] == '/test/path.txt'


class TestHealthEndpointRegression:
    """Test health endpoint functionality."""
    
    def test_health_server_creation(self):
        """Test health server can be created."""
        from tools.scribe.core.health_server import create_health_server
        
        mock_status_provider = MagicMock()
        mock_status_provider.return_value = {"status": "ok"}
        
        shutdown_event = threading.Event()
        
        # Test server creation
        server = create_health_server(
            status_provider=mock_status_provider,
            port=9472,
            shutdown_event=shutdown_event
        )
        
        assert server is not None
        # Server should be a thread
        assert hasattr(server, 'start')
        assert hasattr(server, 'stop')


class TestCircuitBreakerRegression:
    """Test circuit breaker functionality."""
    
    def test_circuit_breaker_basic(self):
        """Test basic circuit breaker functionality."""
        from tools.scribe.core.circuit_breaker import CircuitBreaker
        
        breaker = CircuitBreaker(
            rule_id="test_rule",
            failure_threshold=3,
            recovery_timeout_seconds=60,
            success_threshold=2
        )
        
        # Initially closed
        assert breaker.state.value == "closed"
        
        # Test successful execution
        result = breaker.execute(lambda: "success")
        assert result == "success"
        assert breaker.state.value == "closed"
    
    def test_circuit_breaker_manager(self):
        """Test circuit breaker manager functionality."""
        from tools.scribe.core.circuit_breaker import CircuitBreakerManager
        
        manager = CircuitBreakerManager()
        
        # Get breaker for rule
        breaker = manager.get_breaker("test_rule", failure_threshold=3)
        assert breaker.rule_id == "test_rule"
        
        # Should return same instance for same rule
        breaker2 = manager.get_breaker("test_rule", failure_threshold=5)
        assert breaker is breaker2
        
        # Stats should be available
        stats = manager.get_manager_stats()
        assert 'total_breakers' in stats
        assert 'breakers_by_state' in stats


if __name__ == "__main__":
    # Run regression tests
    pytest.main([__file__, "-v"])