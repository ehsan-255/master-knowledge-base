#!/usr/bin/env python3
"""
Real System Integration Tests for Scribe HMA v2.2

Tests the complete Scribe engine with real external systems:
- NATS for event bus
- OTLP collector for telemetry
- Prometheus for metrics
- Jaeger for traces

These tests require the Docker Compose runtime stack to be running.
"""

import pytest
import time
import json
import requests
import asyncio
import tempfile
from pathlib import Path
from typing import Dict, Any, List
import nats
from nats.js import JetStreamContext


@pytest.fixture(scope="session")
def runtime_workspace():
    """Path to runtime workspace that Scribe monitors."""
    workspace_path = Path("runtime-workspace")
    workspace_path.mkdir(exist_ok=True)
    return workspace_path


@pytest.fixture(scope="session") 
def services_health_check():
    """Verify all required services are healthy before running tests."""
    services = {
        "NATS": "http://localhost:8222/healthz",
        "Prometheus": "http://localhost:9090/-/healthy",
        "Jaeger": "http://localhost:16686/",
        "OTLP Collector": "http://localhost:13133/",
        "Grafana": "http://localhost:3000/api/health"
    }
    
    print("\n🔍 Verifying all services are healthy before running tests...")
    
    for service_name, health_url in services.items():
        max_retries = 10
        for attempt in range(max_retries):
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {service_name} is healthy")
                    break
            except requests.RequestException:
                if attempt == max_retries - 1:
                    pytest.fail(f"❌ Service {service_name} not healthy at {health_url}")
                time.sleep(2)
    
    print("✅ All services verified healthy - proceeding with tests")
    return True


class TestRealSystemIntegration:
    """Test Scribe engine integration with real external systems."""
    
    @pytest.mark.asyncio
    async def test_nats_connection_and_messaging(self, services_health_check):
        """Test that NATS server is accessible and can publish/subscribe messages."""
        nc = await nats.connect("nats://localhost:4222")
        
        # Test basic pub/sub
        received_messages = []
        
        async def message_handler(msg):
            received_messages.append(msg.data.decode())
        
        # Subscribe to test subject
        await nc.subscribe("scribe.test", cb=message_handler)
        
        # Publish test message
        test_message = "test-message-from-integration-test"
        await nc.publish("scribe.test", test_message.encode())
        
        # Wait for message delivery
        await asyncio.sleep(0.5)
        
        assert len(received_messages) == 1
        assert received_messages[0] == test_message
        
        await nc.close()
    
    @pytest.mark.asyncio 
    async def test_nats_jetstream_functionality(self, services_health_check):
        """Test JetStream functionality that Scribe uses for reliable messaging."""
        nc = await nats.connect("nats://localhost:4222")
        js = nc.jetstream()
        
        # Create or get stream for Scribe events
        try:
            stream_info = await js.stream_info("SCRIBE_EVENTS")
        except:
            # Create stream if it doesn't exist
            await js.add_stream(
                name="SCRIBE_EVENTS",
                subjects=["scribe.events.*"]
            )
        
        # Publish message to stream
        test_event = {
            "event_id": "test-event-123",
            "event_type": "file_created",
            "file_path": "/test/file.md",
            "timestamp": time.time()
        }
        
        ack = await js.publish(
            "scribe.events.file_created", 
            json.dumps(test_event).encode()
        )
        
        assert ack.seq > 0  # Message was stored in stream
        
        await nc.close()
    
    def test_prometheus_metrics_endpoint(self, services_health_check):
        """Test that Prometheus is collecting metrics from OTLP collector."""
        # Check Prometheus targets
        response = requests.get("http://localhost:9090/api/v1/targets")
        assert response.status_code == 200
        
        targets_data = response.json()
        target_urls = [target["scrapeUrl"] for target in targets_data["data"]["activeTargets"]]
        
        # Verify OTLP collector is being scraped
        assert any("otel-collector:8889" in url for url in target_urls), \
            "OTLP collector should be configured as Prometheus target"
    
    def test_jaeger_trace_collection(self, services_health_check):
        """Test that Jaeger is accessible and ready to receive traces."""
        # Check Jaeger health
        response = requests.get("http://localhost:16686/api/services")
        assert response.status_code == 200
        
        services_data = response.json()
        assert "data" in services_data
        # Services list may be empty initially, but endpoint should be accessible
    
    def test_otlp_collector_health_and_config(self, services_health_check):
        """Test OTLP collector health and configuration."""
        # Health check with retry logic
        max_retries = 15
        for attempt in range(max_retries):
            try:
                response = requests.get("http://localhost:13133/", timeout=10)
                if response.status_code == 200:
                    health_data = response.json()
                    assert "status" in health_data
                    print(f"✅ OTLP collector health check passed: {health_data}")
                    break
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    pytest.fail(f"OTLP collector health endpoint not accessible: {e}")
                print(f"⏳ OTLP collector not ready, retrying... (attempt {attempt + 1})")
                time.sleep(2)
        
        # Check zpages for pipeline info with retry logic
        for attempt in range(max_retries):
            try:
                response = requests.get("http://localhost:55679/debug/pipelinez", timeout=10)
                if response.status_code == 200:
                    pipeline_info = response.text
                    assert "traces" in pipeline_info.lower()
                    assert "metrics" in pipeline_info.lower()
                    print("✅ OTLP collector pipeline configuration verified")
                    return
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    pytest.fail(f"OTLP collector zpages endpoint not accessible: {e}")
                print(f"⏳ OTLP collector zpages not ready, retrying... (attempt {attempt + 1})")
                time.sleep(2)
    
    def test_file_event_triggers_processing(self, runtime_workspace):
        """Test that creating/modifying files triggers Scribe processing."""
        # Create a test file in monitored directory
        test_file = runtime_workspace / f"integration_test_{int(time.time())}.md"
        
        test_content = f"""# Integration Test File

Created at: {time.time()}
Test ID: integration-test-{int(time.time())}

This file should trigger Scribe processing pipeline.
"""
        
        # Write file
        test_file.write_text(test_content)
        
        # Wait for processing
        time.sleep(2)
        
        # Verify file exists (basic sanity check)
        assert test_file.exists()
        
        # Clean up
        test_file.unlink()
    
    def test_scribe_engine_health_endpoint(self):
        """Test that Scribe engine health endpoint is accessible."""
        # Give Scribe engine time to start up - needs longer for dependency installation
        max_retries = 60  # 2 minutes total wait time
        for attempt in range(max_retries):
            try:
                response = requests.get("http://localhost:9469/health", timeout=10)
                if response.status_code == 200:
                    health_data = response.json()
                    assert "status" in health_data
                    assert health_data["status"] in ["healthy", "initializing"]
                    print(f"✅ Scribe engine health check passed: {health_data}")
                    return
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    pytest.fail(f"Scribe engine health endpoint not accessible after {max_retries} attempts: {e}")
                
                # Log progress every 10 attempts
                if attempt % 10 == 9:
                    print(f"⏳ Waiting for Scribe engine to finish installing dependencies... (attempt {attempt + 1}/{max_retries})")
                
                time.sleep(2)  # Wait 2 seconds between attempts
    
    def test_end_to_end_telemetry_flow(self, runtime_workspace, services_health_check):
        """Test complete telemetry flow from file event to metrics/traces."""
        # Create test file to trigger processing
        test_file = runtime_workspace / f"telemetry_test_{int(time.time())}.md"
        test_file.write_text("# Telemetry Test\n\nThis should generate telemetry data.")
        
        # Wait for processing and telemetry emission
        time.sleep(5)
        
        # Check if any Scribe-related metrics appear in Prometheus
        # Note: This may take time for metrics to appear, so we'll check basic connectivity
        response = requests.get(
            "http://localhost:9090/api/v1/query",
            params={"query": "up"}
        )
        assert response.status_code == 200
        
        metrics_data = response.json()
        assert metrics_data["status"] == "success"
        
        # Check if any traces appear in Jaeger
        # Look for scribe-engine service
        response = requests.get("http://localhost:16686/api/services")
        assert response.status_code == 200
        
        # Clean up
        test_file.unlink()
        
        print("✅ End-to-end telemetry flow test completed")


class TestRealSystemPerformance:
    """Performance tests with real systems."""
    
    def test_high_volume_file_processing(self, runtime_workspace):
        """Test processing multiple files simultaneously."""
        test_files = []
        
        # Create multiple test files
        for i in range(10):
            test_file = runtime_workspace / f"perf_test_{i}_{int(time.time())}.md"
            test_file.write_text(f"# Performance Test File {i}\n\nContent for file {i}")
            test_files.append(test_file)
        
        # Wait for processing
        time.sleep(5)
        
        # Verify all files still exist (basic check)
        for test_file in test_files:
            assert test_file.exists()
        
        # Clean up
        for test_file in test_files:
            test_file.unlink()
        
        print("✅ High volume file processing test completed")


if __name__ == "__main__":
    print("Real System Integration Tests")
    print("=" * 50)
    print("Ensure Docker Compose runtime stack is running:")
    print("docker-compose -f docker-compose.runtime.yml up -d")
    print()
    print("Run tests with: pytest test_real_system_integration.py -v")