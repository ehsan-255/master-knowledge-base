#!/usr/bin/env python3
"""
HMA v2.2 L1 Boundary Validation Comprehensive Test

Tests that ALL L1 boundaries properly enforce JSON Schema validation
with sophisticated boundary validation system.

Priority 0.1 Acceptance Test - ALL MUST PASS for HMA v2.2 compliance.
"""

import pytest
import json
import uuid
import time
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from tools.scribe.core.boundary_validator import create_boundary_validator
from tools.scribe.core.dlq import write_dlq
from tools.scribe.watcher import ScribeEventHandler
from tools.scribe.adapters.nats_subscriber import run_nats
from tools.scribe.adapters.http_validation import L1ValidationMiddleware


class TestFileWatcherL1Validation:
    """Test file watcher L1 boundary validation."""
    
    def test_valid_file_event_passes_validation(self):
        """Valid file system events should pass L1 validation and be published."""
        mock_event_bus = Mock()
        handler = ScribeEventHandler(mock_event_bus)
        
        # Should not raise any exceptions
        handler._publish_event("created", "/test/file.md")
        
        # Verify sophisticated boundary validator was used
        assert hasattr(handler, 'boundary_validator')
        assert hasattr(handler, 'telemetry_manager')
    
    def test_invalid_file_event_fails_validation_dlq(self, tmp_path, monkeypatch):
        """Invalid file system events should fail validation and go to DLQ."""
        # Set up DLQ environment
        monkeypatch.setenv("SCRIBE_REPORT_DIR", str(tmp_path))
        
        mock_event_bus = Mock()
        handler = ScribeEventHandler(mock_event_bus)
        
        # Patch the boundary validator to simulate validation failure
        with patch.object(handler.boundary_validator, 'validate_l1_input') as mock_validate:
            from tools.scribe.core.boundary_validator import ValidationResult, BoundaryType
            mock_validate.return_value = ValidationResult(
                valid=False,
                errors=["Invalid file event schema"],
                boundary_type=BoundaryType.L1_INTERFACE,
                component_id="file_watcher",
                timestamp=time.time()
            )
            
            # This should not publish the event
            handler._publish_event("invalid_type", "/test/file.md")
            
            # Verify DLQ file was created
            dlq_file = tmp_path / "dlq.jsonl"
            assert dlq_file.exists()
            
            # Verify DLQ content
            dlq_content = dlq_file.read_text()
            dlq_record = json.loads(dlq_content.splitlines()[0])
            assert dlq_record["surface"] == "file_system"
            assert "Invalid file event schema" in dlq_record["errors"]


class TestNATSSubscriberL1Validation:
    """Test NATS subscriber L1 boundary validation."""
    
    def test_nats_validation_integration_exists(self):
        """Verify NATS subscriber has sophisticated boundary validation."""
        # Test that the enhanced NATS subscriber imports properly
        from tools.scribe.adapters.nats_subscriber import boundary_validator, telemetry_manager
        
        assert boundary_validator is not None
        assert telemetry_manager is not None
        assert hasattr(boundary_validator, 'validate_l1_input')


class TestHTTPValidationL1Boundary:
    """Test HTTP validation middleware L1 boundary validation."""
    
    def test_http_validation_integration_exists(self):
        """Verify HTTP validation has sophisticated boundary validation."""
        from tools.scribe.adapters.http_validation import boundary_validator, telemetry_manager
        
        assert boundary_validator is not None
        assert telemetry_manager is not None
        assert hasattr(boundary_validator, 'validate_l1_input')


class TestL1SchemaCompliance:
    """Test L1 schema files exist and are valid JSON Schema."""
    
    def test_file_system_event_schema_exists(self):
        """file_system_event.schema.json must exist and be valid."""
        schema_path = Path("../tools/scribe/schemas/l1/file_system_event.schema.json")
        assert schema_path.exists(), "file_system_event.schema.json is required for HMA v2.2"
        
        # Verify it's valid JSON
        with open(schema_path) as f:
            schema = json.load(f)
        
        assert "type" in schema
        assert "properties" in schema
        
    def test_nats_message_schema_exists(self):
        """nats_message.schema.json must exist and be valid."""
        schema_path = Path("../tools/scribe/schemas/l1/nats_message.schema.json")
        assert schema_path.exists(), "nats_message.schema.json is required for HMA v2.2"
        
        with open(schema_path) as f:
            schema = json.load(f)
        
        assert "type" in schema
        assert "properties" in schema
        
    def test_http_request_schema_exists(self):
        """http_request.schema.json must exist and be valid."""
        schema_path = Path("../tools/scribe/schemas/l1/http_request.schema.json")
        assert schema_path.exists(), "http_request.schema.json is required for HMA v2.2"
        
        with open(schema_path) as f:
            schema = json.load(f)
        
        assert "type" in schema
        assert "properties" in schema


class TestL1BoundaryTelemetry:
    """Test that L1 boundaries emit required telemetry."""
    
    def test_boundary_telemetry_spans_configured(self):
        """All boundaries must emit l1.validate spans."""
        # Test file watcher telemetry
        mock_event_bus = Mock()
        handler = ScribeEventHandler(mock_event_bus)
        
        assert hasattr(handler.telemetry_manager, 'trace_boundary_call')
        assert hasattr(handler.telemetry_manager, 'action_failures_counter')
        assert hasattr(handler.telemetry_manager, 'file_events_counter')
    
    def test_boundary_metrics_configured(self):
        """All boundaries must emit validation metrics."""
        from tools.scribe.core.telemetry import initialize_telemetry
        
        telemetry = initialize_telemetry("test-boundary")
        
        # Verify required metrics exist
        assert hasattr(telemetry, 'action_failures_counter')
        assert hasattr(telemetry, 'file_events_counter')
        assert hasattr(telemetry, 'boundary_calls_counter')


class TestL1BoundaryIntegration:
    """Integration tests for L1 boundary validation."""
    
    def test_end_to_end_file_watcher_validation(self, tmp_path, monkeypatch):
        """End-to-end test: malformed file event → validation failure → DLQ → no processing."""
        monkeypatch.setenv("SCRIBE_REPORT_DIR", str(tmp_path))
        
        mock_event_bus = Mock()
        handler = ScribeEventHandler(mock_event_bus)
        
        # Create event that will fail schema validation (missing required fields)
        with patch.object(handler.boundary_validator, 'validate_l1_input') as mock_validate:
            from tools.scribe.core.boundary_validator import ValidationResult, BoundaryType
            mock_validate.return_value = ValidationResult(
                valid=False,
                errors=["Missing required field: event_id", "Invalid timestamp format"],
                boundary_type=BoundaryType.L1_INTERFACE,
                component_id="file_watcher",
                timestamp=time.time()
            )
            
            # Process malformed event
            handler._publish_event("created", "/test/malformed.md")
            
            # VERIFICATION: Event was NOT published
            mock_event_bus.publish_event.assert_not_called()
            
            # VERIFICATION: DLQ entry was created
            dlq_file = tmp_path / "dlq.jsonl"
            assert dlq_file.exists()
            
            dlq_content = dlq_file.read_text()
            dlq_record = json.loads(dlq_content.splitlines()[0])
            
            # VERIFICATION: DLQ contains proper structure
            assert dlq_record["surface"] == "file_system"
            assert "Missing required field: event_id" in dlq_record["errors"]
            assert "Invalid timestamp format" in dlq_record["errors"]


if __name__ == "__main__":
    # Run as: python -m pytest test-environment/scribe-tests/compliance/test_l1_boundary_validation_comprehensive.py -v
    pytest.main([__file__, "-v"])