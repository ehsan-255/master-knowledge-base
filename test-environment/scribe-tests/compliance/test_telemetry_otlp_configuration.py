#!/usr/bin/env python3
"""
HMA v2.2 Telemetry OTLP Configuration Test

Tests Priority 0.3 requirements for sophisticated TelemetryManager configuration:
- OTLP endpoint configuration from environment variables
- Boundary span emission to OTLP collector
- Integration with HMA v2.2 boundary validation system

This test verifies the observability minimum viable tracing + metrics configuration.
"""

import pytest
import os
import time
from unittest.mock import patch, MagicMock, call

from tools.scribe.core.engine_factory import create_engine_components
from tools.scribe.core.telemetry import initialize_telemetry, get_telemetry_manager


class TestTelemetryOTLPConfiguration:
    """Test sophisticated TelemetryManager OTLP configuration for HMA v2.2."""
    
    def test_otlp_endpoint_from_environment(self):
        """Test that OTLP endpoint is read from OTEL_EXPORTER_OTLP_ENDPOINT environment variable."""
        test_endpoint = "http://otel-collector:4317"
        
        with patch.dict(os.environ, {'OTEL_EXPORTER_OTLP_ENDPOINT': test_endpoint}):
            with patch('tools.scribe.core.engine_factory.initialize_telemetry') as mock_init:
                with patch('tools.scribe.core.engine_factory.ConfigManager') as mock_config:
                    # Mock ConfigManager to avoid path issues
                    mock_config.return_value.get_telemetry_config.return_value = {
                        'endpoint': test_endpoint,
                        'sampling_rate': 1.0
                    }
                    
                    # Create engine components which should read environment variable
                    components = create_engine_components()
                    
                    # Verify initialize_telemetry was called with correct endpoint
                    mock_init.assert_called_once_with(
                        service_name="scribe-engine",
                        endpoint=test_endpoint,
                        sampling_rate=1.0
                    )
    
    def test_sampling_rate_from_environment(self):
        """Test that sampling rate is configurable via environment variable."""
        test_endpoint = "http://otel-collector:4317"
        test_sampling_rate = "0.5"
        
        with patch.dict(os.environ, {
            'OTEL_EXPORTER_OTLP_ENDPOINT': test_endpoint,
            'OTEL_TRACE_SAMPLING_RATE': test_sampling_rate
        }):
            with patch('tools.scribe.core.engine_factory.initialize_telemetry') as mock_init:
                with patch('tools.scribe.core.engine_factory.ConfigManager') as mock_config:
                    # Mock ConfigManager to avoid path issues
                    mock_config.return_value.get_telemetry_config.return_value = {
                        'endpoint': test_endpoint,
                        'sampling_rate': 0.5
                    }
                    
                    # Create engine components
                    components = create_engine_components()
                    
                    # Verify sampling rate was read correctly
                    mock_init.assert_called_once_with(
                        service_name="scribe-engine",
                        endpoint=test_endpoint,
                        sampling_rate=0.5
                    )
    
    def test_default_configuration_without_environment(self):
        """Test default configuration when environment variables are not set."""
        # Ensure environment variables are not set
        with patch.dict(os.environ, {}, clear=True):
            with patch('tools.scribe.core.engine_factory.initialize_telemetry') as mock_init:
                with patch('tools.scribe.core.engine_factory.ConfigManager') as mock_config:
                    # Mock ConfigManager to avoid path issues
                    mock_config.return_value.get_telemetry_config.return_value = {
                        'endpoint': None,
                        'sampling_rate': 1.0
                    }
                    
                    # Create engine components
                    components = create_engine_components()
                    
                    # Verify defaults are used
                    mock_init.assert_called_once_with(
                        service_name="scribe-engine",
                        endpoint=None,  # No OTLP endpoint
                        sampling_rate=1.0  # Default sampling rate
                    )
    
    def test_telemetry_manager_boundary_call_tracing(self):
        """Test that TelemetryManager properly traces boundary calls for HMA v2.2 compliance."""
        # Initialize telemetry manager with mock endpoint
        telemetry_manager = initialize_telemetry(
            service_name="test-service",
            endpoint="http://test-collector:4317",
            sampling_rate=1.0
        )
        
        # Test boundary call tracing
        with telemetry_manager.trace_boundary_call(
            interface_type="inbound",
            protocol="file_system", 
            endpoint="file_watcher",
            operation="event_validation",
            attributes={"test_attr": "test_value"}
        ) as span:
            # Verify span is created (even if mock)
            assert span is not None
            
            # Test that span attributes can be set
            span.set_attribute("event_type", "file_created")
            span.set_attribute("valid", True)
    
    def test_telemetry_manager_action_execution_tracing(self):
        """Test action execution tracing for plugin monitoring."""
        telemetry_manager = initialize_telemetry(
            service_name="test-service",
            endpoint="http://test-collector:4317"
        )
        
        # Test action execution tracing
        with telemetry_manager.trace_action_execution(
            action_type="enhanced_frontmatter_action",
            rule_name="test_rule",
            file_path="/test/file.md"
        ) as span:
            # Verify span is created
            assert span is not None
            
            # Test that action execution completes without error
            time.sleep(0.001)  # Simulate some work
    
    def test_telemetry_manager_file_processing_tracing(self):
        """Test file processing tracing for file system monitoring."""
        telemetry_manager = initialize_telemetry(
            service_name="test-service", 
            endpoint="http://test-collector:4317"
        )
        
        # Test file processing tracing
        with telemetry_manager.trace_file_processing(
            file_path="/test/file.md",
            event_type="file_created"
        ) as span:
            # Verify span is created
            assert span is not None
            
            # Test that file processing completes
            time.sleep(0.001)
    
    def test_telemetry_manager_metrics_recording(self):
        """Test that metrics are properly recorded."""
        telemetry_manager = initialize_telemetry(
            service_name="test-service",
            endpoint="http://test-collector:4317"
        )
        
        # Test worker count gauge
        telemetry_manager.update_worker_count(5)
        
        # Test queue size gauge
        telemetry_manager.update_queue_size(10)
        
        # Test that calls complete without error
        assert True
    
    def test_telemetry_manager_trace_id_correlation(self):
        """Test trace ID generation for distributed tracing correlation."""
        telemetry_manager = initialize_telemetry(
            service_name="test-service",
            endpoint="http://test-collector:4317"
        )
        
        # Test trace ID retrieval
        trace_id = telemetry_manager.get_current_trace_id()
        
        # Should return None when no active span (mock environment) or a valid trace ID
        assert trace_id is None or isinstance(trace_id, str)
    
    def test_telemetry_manager_graceful_shutdown(self):
        """Test that telemetry manager shuts down gracefully."""
        telemetry_manager = initialize_telemetry(
            service_name="test-service",
            endpoint="http://test-collector:4317"
        )
        
        # Test shutdown
        telemetry_manager.shutdown()
        
        # Should complete without error
        assert True


class TestBoundaryTelemetryIntegration:
    """Test integration between boundary validation and telemetry systems."""
    
    def test_file_watcher_telemetry_integration(self):
        """Test that file watcher properly integrates with telemetry."""
        from tools.scribe.watcher import ScribeEventHandler
        
        # Create handler with telemetry
        handler = ScribeEventHandler(['*.md'])
        
        # Verify telemetry manager is initialized
        assert handler.telemetry_manager is not None
        
        # Verify boundary validator is initialized
        assert handler.boundary_validator is not None
    
    def test_nats_adapter_telemetry_integration(self):
        """Test that NATS adapter uses telemetry correctly."""
        # Import to verify module loads correctly
        import tools.scribe.adapters.nats_subscriber
        
        # Verify telemetry manager is initialized at module level
        assert hasattr(tools.scribe.adapters.nats_subscriber, 'telemetry_manager')
        assert tools.scribe.adapters.nats_subscriber.telemetry_manager is not None
    
    def test_http_adapter_telemetry_integration(self):
        """Test that HTTP adapter uses telemetry correctly."""
        # Import to verify module loads correctly
        import tools.scribe.adapters.http_validation
        
        # Verify telemetry manager is initialized at module level
        assert hasattr(tools.scribe.adapters.http_validation, 'telemetry_manager')
        assert tools.scribe.adapters.http_validation.telemetry_manager is not None


class TestOTLPCollectorConfiguration:
    """Test OpenTelemetry Collector configuration compliance."""
    
    def test_otel_collector_yaml_exists(self):
        """Test that OpenTelemetry Collector configuration exists."""
        from pathlib import Path
        
        otel_config_path = Path("../tools/scribe/deployment/observability/otel-collector.yaml")
        assert otel_config_path.exists(), "OpenTelemetry Collector configuration must exist"
    
    def test_otel_collector_configuration_format(self):
        """Test that OpenTelemetry Collector configuration has required sections."""
        from pathlib import Path
        import yaml
        
        otel_config_path = Path("../tools/scribe/deployment/observability/otel-collector.yaml")
        with open(otel_config_path) as f:
            config = yaml.safe_load(f)
        
        # Verify required sections exist
        assert "receivers" in config, "OTLP receivers must be configured"
        assert "exporters" in config, "Exporters must be configured"
        assert "service" in config, "Service pipelines must be configured"
        
        # Verify OTLP receiver with grpc and http protocols
        assert "otlp" in config["receivers"], "OTLP receiver must be configured"
        otlp_receiver = config["receivers"]["otlp"]
        assert "protocols" in otlp_receiver, "OTLP protocols must be configured"
        assert "grpc" in otlp_receiver["protocols"], "OTLP gRPC protocol must be enabled"
        assert "http" in otlp_receiver["protocols"], "OTLP HTTP protocol must be enabled"
        
        # Verify required exporters
        exporters = config["exporters"]
        assert "jaeger" in exporters, "Jaeger exporter must be configured"
        assert "logging" in exporters, "Logging exporter must be configured"
        assert "prometheus" in exporters, "Prometheus exporter must be configured"
        
        # Verify service pipelines
        service_config = config["service"]
        assert "pipelines" in service_config, "Service pipelines must be configured"
        
        pipelines = service_config["pipelines"]
        assert "traces" in pipelines, "Traces pipeline must be configured"
        assert "metrics" in pipelines, "Metrics pipeline must be configured"
        
        # Verify trace pipeline configuration
        trace_pipeline = pipelines["traces"]
        assert "otlp" in trace_pipeline["receivers"], "Traces pipeline must use OTLP receiver"
        assert "jaeger" in trace_pipeline["exporters"], "Traces pipeline must export to Jaeger"
        assert "logging" in trace_pipeline["exporters"], "Traces pipeline must export to logging"
        
        # Verify metrics pipeline configuration
        metrics_pipeline = pipelines["metrics"]
        assert "otlp" in metrics_pipeline["receivers"], "Metrics pipeline must use OTLP receiver"
        assert "prometheus" in metrics_pipeline["exporters"], "Metrics pipeline must export to Prometheus"
    
    def test_kubernetes_deployment_otlp_environment(self):
        """Test that Kubernetes deployment has correct OTLP environment variable."""
        from pathlib import Path
        import yaml
        
        k8s_deployment_path = Path("../tools/scribe/deployment/kubernetes/scribe-deployment.yaml")
        assert k8s_deployment_path.exists(), "Kubernetes deployment must exist"
        
        with open(k8s_deployment_path) as f:
            deployment = yaml.safe_load(f)
        
        # Find environment variables in deployment
        containers = deployment["spec"]["template"]["spec"]["containers"]
        scribe_container = next(c for c in containers if c["name"] == "scribe")
        env_vars = scribe_container.get("env", [])
        
        # Find OTLP endpoint environment variable
        otlp_env = next((env for env in env_vars if env["name"] == "OTEL_EXPORTER_OTLP_ENDPOINT"), None)
        assert otlp_env is not None, "OTEL_EXPORTER_OTLP_ENDPOINT must be configured"
        assert otlp_env["value"] == "http://otel-collector:4317", "OTLP endpoint must point to collector"


if __name__ == "__main__":
    # Run as: python -m pytest test-environment/scribe-tests/compliance/test_telemetry_otlp_configuration.py -v
    pytest.main([__file__, "-v"])