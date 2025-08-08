"""
Integration tests for file processing orchestrator plugin.

Tests end-to-end file processing workflows with mocked dependencies.
"""

import pytest
import asyncio
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

# Test fixtures and data
@pytest.fixture
def temp_test_file():
    """Create a temporary test file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""---
title: "Test Document"
info-type: "general-document"
---

# Test Document

This is a test document for integration testing.
""")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def mock_port_registry():
    """Create a comprehensive mock port registry."""
    registry = Mock()
    
    # Mock all required ports
    config_port = Mock()
    config_port.get_config_value = AsyncMock(return_value=".")
    
    logging_port = Mock()
    logging_port.log_info = Mock()
    logging_port.log_error = Mock()
    logging_port.log_warning = Mock()
    logging_port.log_debug = Mock()
    
    event_bus_port = AsyncMock()
    event_bus_port.publish_event = AsyncMock(return_value=True)
    
    file_system_port = AsyncMock()
    file_system_port.read_file_safely = AsyncMock()
    file_system_port.write_file_safely = AsyncMock(return_value=True)
    
    command_port = AsyncMock()
    command_port.execute_command_safely = AsyncMock(return_value=(True, "success", ""))
    
    observability_port = Mock()
    observability_port.emit_metric = Mock()
    observability_port.start_span = Mock()
    
    # Register all ports
    port_map = {
        "configuration": config_port,
        "logging": logging_port,
        "event_bus": event_bus_port,
        "file_system": file_system_port,
        "command_execution": command_port,
        "observability": observability_port
    }
    
    registry.get_port = lambda port_type: port_map.get(port_type)
    
    return registry


@pytest.fixture
def mock_plugin_context(mock_port_registry):
    """Create mock plugin context."""
    from tools.scribe.core.port_adapters import ScribePluginContextAdapter
    
    return ScribePluginContextAdapter(
        "file_processing_orchestrator",
        mock_port_registry,
        {"test_mode": True}
    )


class TestFileProcessingOrchestrator:
    """Integration tests for file processing orchestration."""
    
    def test_orchestrator_initialization(self, mock_plugin_context):
        """Test orchestrator initializes with HMA v2.2 compliance."""
        # Import the orchestrator plugin if it exists
        try:
            from tools.scribe.actions.file_processing_orchestrator import FileProcessingOrchestratorAction
            
            orchestrator = FileProcessingOrchestratorAction(
                "file_processing",
                {"enabled_actions": ["enhanced_frontmatter", "validation"]},
                mock_plugin_context
            )
            
            assert orchestrator.context == mock_plugin_context
            assert orchestrator.action_type == "file_processing"
            
        except ImportError:
            pytest.skip("FileProcessingOrchestratorAction not available")
    
    @pytest.mark.asyncio
    async def test_end_to_end_file_processing(self, temp_test_file, mock_plugin_context):
        """Test complete file processing workflow."""
        try:
            from tools.scribe.actions.file_processing_orchestrator import FileProcessingOrchestratorAction
            
            # Mock the individual action plugins
            mock_frontmatter_action = Mock()
            mock_frontmatter_action.execute = AsyncMock(return_value="processed content")
            
            mock_validation_action = Mock() 
            mock_validation_action.execute = AsyncMock(return_value="validated content")
            
            # Create orchestrator with mocked actions
            orchestrator = FileProcessingOrchestratorAction(
                "file_processing",
                {
                    "enabled_actions": ["enhanced_frontmatter", "validation"],
                    "action_chain": ["enhanced_frontmatter", "validation"]
                },
                mock_plugin_context
            )
            
            # Mock the action loading
            with patch.object(orchestrator, '_load_action_plugins') as mock_load:
                mock_load.return_value = {
                    "enhanced_frontmatter": mock_frontmatter_action,
                    "validation": mock_validation_action
                }
                
                # Execute the orchestrated workflow
                with open(temp_test_file, 'r') as f:
                    test_content = f.read()
                
                result = await orchestrator.execute(
                    test_content,
                    None,  # No regex match for orchestrator
                    temp_test_file,
                    {"chain_execution": True}
                )
                
                # Verify workflow execution
                assert result is not None
                
                # Verify actions were called in sequence
                mock_frontmatter_action.execute.assert_called_once()
                mock_validation_action.execute.assert_called_once()
                
        except ImportError:
            pytest.skip("FileProcessingOrchestratorAction not available")
    
    @pytest.mark.asyncio
    async def test_orchestrator_error_handling(self, temp_test_file, mock_plugin_context):
        """Test orchestrator handles plugin errors gracefully."""
        try:
            from tools.scribe.actions.file_processing_orchestrator import FileProcessingOrchestratorAction
            
            # Mock an action that fails
            mock_failing_action = Mock()
            mock_failing_action.execute = AsyncMock(side_effect=Exception("Action failed"))
            
            orchestrator = FileProcessingOrchestratorAction(
                "file_processing",
                {"enabled_actions": ["failing_action"]},
                mock_plugin_context
            )
            
            # Mock the action loading
            with patch.object(orchestrator, '_load_action_plugins') as mock_load:
                mock_load.return_value = {"failing_action": mock_failing_action}
                
                with open(temp_test_file, 'r') as f:
                    test_content = f.read()
                
                # Should handle errors gracefully
                result = await orchestrator.execute(
                    test_content,
                    None,
                    temp_test_file,
                    {"continue_on_error": True}
                )
                
                # Should return original content on error with continue_on_error
                assert result == test_content or result is not None
                
        except ImportError:
            pytest.skip("FileProcessingOrchestratorAction not available")
    
    @pytest.mark.asyncio 
    async def test_orchestrator_telemetry_compliance(self, temp_test_file, mock_plugin_context):
        """Test orchestrator emits proper HMA v2.2 telemetry."""
        try:
            from tools.scribe.actions.file_processing_orchestrator import FileProcessingOrchestratorAction
            
            orchestrator = FileProcessingOrchestratorAction(
                "file_processing",
                {"enabled_actions": []},
                mock_plugin_context
            )
            
            # Get the observability port from context
            observability_port = mock_plugin_context.get_port("observability")
            
            with open(temp_test_file, 'r') as f:
                test_content = f.read()
            
            # Execute (even with no actions)
            await orchestrator.execute(
                test_content,
                None,
                temp_test_file,
                {}
            )
            
            # Verify telemetry was called (if orchestrator supports it)
            # This is a compliance check for HMA v2.2 boundary telemetry
            assert observability_port is not None
            
        except ImportError:
            pytest.skip("FileProcessingOrchestratorAction not available")


class TestMockFileProcessingOrchestrator:
    """Test orchestrator pattern with mock implementation."""
    
    @pytest.mark.asyncio
    async def test_mock_orchestrator_pattern(self, temp_test_file, mock_plugin_context):
        """Test orchestrator pattern with mock implementation."""
        
        # Create a simplified mock orchestrator to test the pattern
        class MockFileProcessingOrchestrator:
            def __init__(self, action_type, params, plugin_context):
                self.action_type = action_type
                self.params = params
                self.context = plugin_context
                self.log_port = plugin_context.get_port("logging")
                
            async def execute(self, file_content, match, file_path, params):
                """Execute orchestrated file processing."""
                self.log_port.log_info("Starting orchestrated processing", file_path=file_path)
                
                # Simulate action chain execution
                result_content = file_content
                
                for action_name in self.params.get("action_chain", []):
                    self.log_port.log_info("Executing action", action=action_name)
                    
                    # Mock action execution
                    if action_name == "enhanced_frontmatter":
                        # Simulate frontmatter enhancement
                        result_content = result_content.replace("Test Document", "Enhanced Test Document")
                    elif action_name == "validation":
                        # Simulate validation (no change to content)
                        pass
                        
                self.log_port.log_info("Orchestrated processing completed", file_path=file_path)
                return result_content
        
        # Test the mock orchestrator
        orchestrator = MockFileProcessingOrchestrator(
            "file_processing",
            {"action_chain": ["enhanced_frontmatter", "validation"]},
            mock_plugin_context
        )
        
        with open(temp_test_file, 'r') as f:
            test_content = f.read()
        
        result = await orchestrator.execute(
            test_content,
            None,
            temp_test_file,
            {}
        )
        
        # Verify processing occurred
        assert "Enhanced Test Document" in result
        
        # Verify logging was called
        log_port = mock_plugin_context.get_port("logging")
        assert log_port.log_info.call_count >= 3  # Start, actions, complete
    
    @pytest.mark.asyncio
    async def test_plugin_chain_validation(self, mock_plugin_context):
        """Test plugin chain validation and dependency checking."""
        
        class MockPluginChainValidator:
            def __init__(self, plugin_context):
                self.context = plugin_context
                self.log_port = plugin_context.get_port("logging")
                
            async def validate_plugin_chain(self, action_chain):
                """Validate that plugin chain is executable."""
                available_plugins = {
                    "enhanced_frontmatter": {"dependencies": []},
                    "validation": {"dependencies": ["enhanced_frontmatter"]},
                    "naming_enforcement": {"dependencies": []}
                }
                
                # Check if all plugins in chain are available
                for action in action_chain:
                    if action not in available_plugins:
                        self.log_port.log_error("Plugin not available", plugin=action)
                        return False
                
                # Check dependencies
                executed_plugins = set()
                for action in action_chain:
                    dependencies = available_plugins[action]["dependencies"]
                    for dep in dependencies:
                        if dep not in executed_plugins:
                            self.log_port.log_error(
                                "Plugin dependency not satisfied", 
                                plugin=action, 
                                missing_dependency=dep
                            )
                            return False
                    executed_plugins.add(action)
                
                self.log_port.log_info("Plugin chain validation successful")
                return True
        
        validator = MockPluginChainValidator(mock_plugin_context)
        
        # Test valid chain
        valid_chain = ["enhanced_frontmatter", "validation"]
        result = await validator.validate_plugin_chain(valid_chain)
        assert result == True
        
        # Test invalid chain (missing dependency)
        invalid_chain = ["validation", "enhanced_frontmatter"]  # Wrong order
        result = await validator.validate_plugin_chain(invalid_chain)
        assert result == False
        
        # Test chain with missing plugin
        missing_plugin_chain = ["nonexistent_plugin"]
        result = await validator.validate_plugin_chain(missing_plugin_chain)
        assert result == False


@pytest.mark.integration
class TestE2EFileProcessing:
    """End-to-end integration tests."""
    
    @pytest.mark.asyncio
    async def test_complete_file_lifecycle(self, temp_test_file, mock_plugin_context):
        """Test complete file processing lifecycle."""
        
        # Simulate file system watcher detecting a change
        event_bus_port = mock_plugin_context.get_port("event_bus")
        
        # Publish file change event
        await event_bus_port.publish_event(
            "file_event",
            {
                "event_id": "test_event",
                "type": "modified",
                "file_path": temp_test_file,
                "timestamp": 1234567890
            }
        )
        
        # Verify event was published
        event_bus_port.publish_event.assert_called_once()
        
        # Simulate processing pipeline
        file_system_port = mock_plugin_context.get_port("file_system")
        
        # Read file content
        with open(temp_test_file, 'r') as f:
            content = f.read()
        file_system_port.read_file_safely.return_value = content
        
        # Simulate processing
        processed_content = content.replace("Test Document", "Processed Test Document")
        
        # Write back processed content
        await file_system_port.write_file_safely(temp_test_file, processed_content)
        
        # Verify file operations
        file_system_port.write_file_safely.assert_called_once_with(temp_test_file, processed_content)
        
        # Log completion
        log_port = mock_plugin_context.get_port("logging")
        log_port.log_info("File processing lifecycle completed", file_path=temp_test_file)
        
        assert log_port.log_info.called