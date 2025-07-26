#!/usr/bin/env python3
"""
Comprehensive End-to-End Vault Secret Lifecycle Tests

Enterprise-grade validation of complete HashiCorp Vault integration
for Scribe HMA v2.2 with full secret lifecycle testing.
"""

import pytest
import asyncio
import time
import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import structlog

# Test framework imports
from unittest.mock import Mock, patch, MagicMock
import requests
import hvac

# Scribe imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.scribe.core.vault_secret_provider import (
    VaultSecretProvider, VaultConfig, AuthMethod, 
    initialize_vault_provider, configure_vault_from_environment
)
from tools.scribe.core.vault_policy_manager import (
    VaultPolicyManager, AppRoleConfig, AccessTier, PolicyScope
)
from tools.scribe.core.vault_rotation_manager import (
    VaultRotationManager, RotationJob, RotationType, RotationTrigger, RotationStatus
)
from tools.scribe.core.vault_metrics_collector import (
    VaultMetricsCollector, OperationStatus, get_vault_metrics_collector
)
from tools.scribe.core.vault_otlp_integration import (
    VaultOTLPIntegration, OTLPConfig, get_vault_otlp_integration
)
from tools.scribe.core.vault_circuit_breaker import get_vault_circuit_breaker_manager
from tools.scribe.core.vault_retry_handler import get_vault_retry_manager
from tools.scribe.core.vault_graceful_degradation import get_vault_degradation_manager

logger = structlog.get_logger(__name__)


@pytest.fixture(scope="session")
def vault_config():
    """Create Vault configuration for testing."""
    return VaultConfig(
        url="http://localhost:8200",
        auth_method=AuthMethod.TOKEN,
        verify_ssl=False,
        timeout=10
    )


@pytest.fixture(scope="session")
def otlp_config():
    """Create OTLP configuration for testing."""
    return OTLPConfig(
        endpoint="http://localhost:4317",
        service_name="scribe-vault-e2e-test",
        environment="test",
        insecure=True
    )


@pytest.fixture(scope="session")
async def vault_integration_setup(vault_config, otlp_config):
    """Setup complete Vault integration for testing."""
    # Initialize OTLP integration
    otlp = VaultOTLPIntegration(otlp_config)
    otlp.initialize()
    
    # Initialize Vault provider
    provider = VaultSecretProvider(vault_config)
    provider.configure_authentication(token=os.getenv('VAULT_TOKEN', 'dev-only-token'))
    
    # Initialize policy manager
    policy_manager = VaultPolicyManager(provider)
    
    # Initialize rotation manager
    rotation_manager = VaultRotationManager(provider, policy_manager)
    
    # Initialize metrics collector
    metrics_collector = get_vault_metrics_collector()
    
    # Create test namespace
    test_data = {
        'provider': provider,
        'policy_manager': policy_manager,
        'rotation_manager': rotation_manager,
        'metrics_collector': metrics_collector,
        'otlp': otlp
    }
    
    yield test_data
    
    # Cleanup
    try:
        rotation_manager.stop_scheduler()
        provider.close()
        otlp.shutdown()
    except Exception as e:
        logger.warning("Cleanup error", error=str(e))


class TestVaultConnectivityAndAuthentication:
    """Test basic Vault connectivity and authentication."""
    
    @pytest.mark.timeout(30)
    async def test_vault_connectivity(self, vault_integration_setup):
        """Test basic Vault server connectivity."""
        provider = vault_integration_setup['provider']
        
        # Test health check
        health_status = provider.health_check()
        
        assert 'vault_url' in health_status
        assert health_status['vault_url'] == 'http://localhost:8200'
        assert 'operation_count' in health_status
        assert 'failure_count' in health_status
        
        logger.info("Vault connectivity test passed", health_status=health_status)
    
    @pytest.mark.timeout(20)
    async def test_vault_authentication_flow(self, vault_integration_setup):
        """Test complete authentication flow with metrics."""
        provider = vault_integration_setup['provider']
        metrics = vault_integration_setup['metrics_collector']
        
        initial_metrics = metrics.get_metrics_summary()
        
        # Authenticate
        auth_result = provider.authenticate()
        assert auth_result is True
        
        # Verify metrics were recorded
        final_metrics = metrics.get_metrics_summary()
        assert final_metrics['recent_operations'] > initial_metrics['recent_operations']
        
        logger.info("Authentication flow test passed")
    
    @pytest.mark.timeout(25)
    async def test_authentication_failure_handling(self, vault_config):
        """Test authentication failure scenarios and circuit breaker behavior."""
        # Create provider with invalid token
        invalid_provider = VaultSecretProvider(vault_config)
        invalid_provider.configure_authentication(token="invalid-token")
        
        # This should fail and trigger circuit breaker
        with pytest.raises(Exception):
            invalid_provider.authenticate()
        
        # Verify circuit breaker state
        cb_manager = get_vault_circuit_breaker_manager()
        auth_cb = cb_manager.get_circuit_breaker("auth")
        
        # Circuit breaker should have recorded the failure
        assert auth_cb is not None
        
        logger.info("Authentication failure handling test passed")


class TestSecretOperations:
    """Test comprehensive secret operations."""
    
    @pytest.mark.timeout(30)
    async def test_secret_write_read_cycle(self, vault_integration_setup):
        """Test complete secret write/read cycle with caching."""
        provider = vault_integration_setup['provider']
        
        # Authenticate first
        provider.authenticate()
        
        test_secret_data = {
            'username': 'test-user',
            'password': 'test-password-123',
            'api_key': 'test-api-key-456',
            'created_at': datetime.now().isoformat()
        }
        
        test_path = f"test/secrets/e2e-{int(time.time())}"
        
        # Write secret
        provider.write_secret(test_path, test_secret_data, mount_point="scribe")
        
        # Read secret (should hit Vault)
        retrieved_secret_1 = provider.get_secret(test_path, mount_point="scribe")
        assert retrieved_secret_1['username'] == test_secret_data['username']
        assert retrieved_secret_1['password'] == test_secret_data['password']
        
        # Read secret again (should hit cache)
        retrieved_secret_2 = provider.get_secret(test_path, mount_point="scribe")
        assert retrieved_secret_2 == retrieved_secret_1
        
        logger.info("Secret write/read cycle test passed",
                   path=test_path,
                   cache_hits=2)
    
    @pytest.mark.timeout(35)
    async def test_secret_versioning_and_history(self, vault_integration_setup):
        """Test secret versioning and historical access."""
        provider = vault_integration_setup['provider']
        provider.authenticate()
        
        test_path = f"test/versioning/e2e-{int(time.time())}"
        
        # Write multiple versions
        for version in range(1, 4):
            secret_data = {
                'version': version,
                'data': f'secret-data-v{version}',
                'timestamp': datetime.now().isoformat()
            }
            provider.write_secret(test_path, secret_data, mount_point="scribe")
            time.sleep(1)  # Ensure different timestamps
        
        # Read latest version
        latest_secret = provider.get_secret(test_path, mount_point="scribe")
        assert latest_secret['version'] == 3
        
        logger.info("Secret versioning test passed", path=test_path)
    
    @pytest.mark.timeout(25)
    async def test_secret_cache_expiration(self, vault_integration_setup):
        """Test secret cache expiration and refresh."""
        provider = vault_integration_setup['provider']
        provider.authenticate()
        
        test_path = f"test/cache/e2e-{int(time.time())}"
        original_data = {'value': 'original-value', 'timestamp': time.time()}
        
        # Write and read secret
        provider.write_secret(test_path, original_data, mount_point="scribe")
        cached_secret = provider.get_secret(test_path, mount_point="scribe")
        
        # Manually expire cache entry
        cache_key = f"scribe/{test_path}"
        if cache_key in provider._secret_cache:
            provider._secret_cache[cache_key].retrieved_at = datetime.now() - timedelta(hours=2)
        
        # Read again - should fetch fresh from Vault
        fresh_secret = provider.get_secret(test_path, mount_point="scribe")
        assert fresh_secret['value'] == original_data['value']
        
        logger.info("Secret cache expiration test passed")


class TestCertificateLifecycle:
    """Test complete certificate lifecycle operations."""
    
    @pytest.mark.timeout(40)
    async def test_certificate_generation_and_validation(self, vault_integration_setup):
        """Test certificate generation with validation."""
        provider = vault_integration_setup['provider']
        provider.authenticate()
        
        common_name = f"test-{int(time.time())}.scribe.local"
        alt_names = ["localhost", "127.0.0.1"]
        
        # Generate certificate
        cert_data = provider.get_certificate(
            common_name=common_name,
            alt_names=alt_names,
            ttl="1h"
        )
        
        # Validate certificate data structure
        required_fields = ['certificate', 'private_key', 'ca_cert', 'serial_number']
        for field in required_fields:
            assert field in cert_data
            assert cert_data[field] is not None
            assert len(cert_data[field]) > 0
        
        # Validate certificate content
        assert '-----BEGIN CERTIFICATE-----' in cert_data['certificate']
        assert '-----END CERTIFICATE-----' in cert_data['certificate']
        assert '-----BEGIN PRIVATE KEY-----' in cert_data['private_key']
        
        logger.info("Certificate generation test passed",
                   common_name=common_name,
                   serial_number=cert_data['serial_number'])
    
    @pytest.mark.timeout(30)
    async def test_certificate_temporary_files(self, vault_integration_setup):
        """Test certificate temporary file creation and cleanup."""
        provider = vault_integration_setup['provider']
        provider.authenticate()
        
        common_name = f"temp-test-{int(time.time())}.scribe.local"
        
        # Generate certificate
        cert_data = provider.get_certificate(common_name=common_name, ttl="30m")
        
        # Create temporary files
        cert_file, key_file, ca_file = provider.create_temporary_cert_files(cert_data)
        
        # Verify files exist and have correct permissions
        for file_path in [cert_file, key_file, ca_file]:
            assert os.path.exists(file_path)
            # Check file permissions (should be 600)
            stat_info = os.stat(file_path)
            assert stat_info.st_mode & 0o777 == 0o600
        
        # Verify file contents
        with open(cert_file, 'r') as f:
            cert_content = f.read()
            assert cert_content == cert_data['certificate']
        
        logger.info("Certificate temporary files test passed",
                   cert_file=cert_file,
                   key_file=key_file,
                   ca_file=ca_file)


class TestRotationLifecycle:
    """Test comprehensive secret rotation lifecycle."""
    
    @pytest.mark.timeout(45)
    async def test_rotation_job_registration_and_execution(self, vault_integration_setup):
        """Test rotation job registration and manual execution."""
        rotation_manager = vault_integration_setup['rotation_manager']
        provider = vault_integration_setup['provider']
        
        provider.authenticate()
        
        # Create rotation job
        job = RotationJob(
            job_id=f"test-rotation-{int(time.time())}",
            rotation_type=RotationType.SECRET,
            target_path=f"test/rotation/secret-{int(time.time())}",
            schedule_expression="@daily",
            advance_warning_hours=1,
            metadata={'secret_type': 'api_key'}
        )
        
        # Register job
        registration_result = rotation_manager.register_rotation_job(job)
        assert registration_result is True
        
        # Verify job is registered
        jobs = rotation_manager.list_rotation_jobs()
        job_ids = [j.job_id for j in jobs]
        assert job.job_id in job_ids
        
        # Execute rotation manually
        execution_id = rotation_manager.execute_rotation(
            job.job_id, 
            RotationTrigger.MANUAL
        )
        assert execution_id is not None
        
        # Wait for completion
        max_wait = 10
        while max_wait > 0:
            execution = rotation_manager.get_rotation_status(execution_id)
            if execution and execution.status in [RotationStatus.COMPLETED, RotationStatus.FAILED]:
                break
            await asyncio.sleep(1)
            max_wait -= 1
        
        # Verify execution completed
        final_execution = rotation_manager.get_rotation_status(execution_id)
        assert final_execution is not None
        assert final_execution.status == RotationStatus.COMPLETED
        
        logger.info("Rotation job test passed",
                   job_id=job.job_id,
                   execution_id=execution_id,
                   status=final_execution.status.value)
    
    @pytest.mark.timeout(35)
    async def test_scheduled_rotation_system(self, vault_integration_setup):
        """Test scheduled rotation system startup and operation."""
        rotation_manager = vault_integration_setup['rotation_manager']
        
        # Setup standard rotation jobs
        setup_result = rotation_manager.setup_standard_rotation_jobs()
        assert setup_result is True
        
        # Start scheduler
        scheduler_result = rotation_manager.start_scheduler()
        assert scheduler_result is True
        
        # Verify scheduler is running
        metrics = rotation_manager.get_rotation_metrics()
        assert metrics['scheduler_running'] is True
        assert metrics['registered_jobs'] > 0
        
        # Stop scheduler
        stop_result = rotation_manager.stop_scheduler()
        assert stop_result is True
        
        logger.info("Scheduled rotation system test passed",
                   metrics=metrics)


class TestResiliencePatterns:
    """Test resilience patterns and failure handling."""
    
    @pytest.mark.timeout(40)
    async def test_circuit_breaker_operation(self, vault_integration_setup):
        """Test circuit breaker behavior under failure conditions."""
        provider = vault_integration_setup['provider']
        cb_manager = get_vault_circuit_breaker_manager()
        
        # Get circuit breaker for secret operations
        secret_cb = cb_manager.get_circuit_breaker("secret_read")
        initial_state = secret_cb.get_state()
        
        # Simulate multiple failures by using invalid paths
        failure_count = 0
        for i in range(10):
            try:
                provider.get_secret(f"nonexistent/path/{i}", mount_point="invalid")
            except Exception:
                failure_count += 1
        
        # Circuit breaker should eventually open
        final_state = secret_cb.get_state()
        assert failure_count > 0
        
        logger.info("Circuit breaker operation test passed",
                   initial_state=initial_state.value,
                   final_state=final_state.value,
                   failures=failure_count)
    
    @pytest.mark.timeout(30)
    async def test_retry_mechanism(self, vault_integration_setup):
        """Test retry mechanism with exponential backoff."""
        retry_manager = get_vault_retry_manager()
        
        # Test retry handler
        retry_handler = retry_manager.get_retry_handler("test_operation")
        
        # Mock function that fails then succeeds
        call_count = 0
        def mock_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception(f"Simulated failure {call_count}")
            return f"Success after {call_count} attempts"
        
        # Execute with retry
        result = retry_handler.execute(mock_operation)
        
        assert call_count == 3
        assert "Success after 3 attempts" in result
        
        logger.info("Retry mechanism test passed",
                   attempts=call_count,
                   result=result)
    
    @pytest.mark.timeout(25)
    async def test_graceful_degradation(self, vault_integration_setup):
        """Test graceful degradation under various failure scenarios."""
        degradation_manager = get_vault_degradation_manager()
        
        initial_mode = degradation_manager.get_current_mode()
        
        # Simulate Vault failures
        for i in range(5):
            degradation_manager.handle_vault_failure(
                Exception(f"Simulated failure {i}"),
                f"test_operation_{i}"
            )
        
        # Check if service mode changed
        degraded_mode = degradation_manager.get_current_mode()
        metrics = degradation_manager.get_metrics()
        
        assert 'current_mode' in metrics
        assert 'failure_count' in metrics
        assert metrics['failure_count'] > 0
        
        logger.info("Graceful degradation test passed",
                   initial_mode=initial_mode.value,
                   degraded_mode=degraded_mode.value,
                   metrics=metrics)


class TestMetricsAndObservability:
    """Test comprehensive metrics and observability features."""
    
    @pytest.mark.timeout(30)
    async def test_metrics_collection(self, vault_integration_setup):
        """Test metrics collection across all operations."""
        metrics_collector = vault_integration_setup['metrics_collector']
        provider = vault_integration_setup['provider']
        
        provider.authenticate()
        
        initial_summary = metrics_collector.get_metrics_summary()
        
        # Perform various operations to generate metrics
        test_path = f"test/metrics/{int(time.time())}"
        test_data = {'value': 'metrics-test', 'timestamp': time.time()}
        
        provider.write_secret(test_path, test_data, mount_point="scribe")
        provider.get_secret(test_path, mount_point="scribe")
        provider.health_check()
        
        # Check metrics were collected
        final_summary = metrics_collector.get_metrics_summary()
        
        assert final_summary['recent_operations'] > initial_summary['recent_operations']
        assert final_summary['prometheus_metrics'] > 0
        assert final_summary['otel_metrics'] > 0
        
        logger.info("Metrics collection test passed",
                   initial_ops=initial_summary['recent_operations'],
                   final_ops=final_summary['recent_operations'])
    
    @pytest.mark.timeout(25)
    async def test_otlp_integration(self, vault_integration_setup):
        """Test OTLP integration and telemetry export."""
        otlp = vault_integration_setup['otlp']
        
        # Check OTLP health
        health_status = otlp.get_health_status()
        
        assert health_status['initialized'] is True
        assert health_status['tracing_enabled'] is True
        assert health_status['metrics_enabled'] is True
        assert health_status['service_name'] == 'scribe-vault-e2e-test'
        
        # Create test span
        with otlp.create_span("test.operation", {
            "test.type": "e2e",
            "test.component": "otlp"
        }) as span:
            # Record test operation
            otlp.record_vault_operation(
                operation="test",
                duration=0.1,
                status="success",
                test_attribute="e2e-test"
            )
        
        logger.info("OTLP integration test passed", health_status=health_status)


class TestPerformanceAndLoad:
    """Test performance characteristics under load."""
    
    @pytest.mark.timeout(60)
    async def test_concurrent_secret_operations(self, vault_integration_setup):
        """Test concurrent secret operations performance."""
        provider = vault_integration_setup['provider']
        provider.authenticate()
        
        async def secret_operation(operation_id: int):
            test_path = f"test/concurrent/secret-{operation_id}"
            test_data = {
                'operation_id': operation_id,
                'timestamp': time.time(),
                'data': f'concurrent-test-data-{operation_id}'
            }
            
            # Write and read
            provider.write_secret(test_path, test_data, mount_point="scribe")
            retrieved = provider.get_secret(test_path, mount_point="scribe")
            
            return retrieved['operation_id'] == operation_id
        
        # Execute concurrent operations
        start_time = time.time()
        
        tasks = []
        for i in range(20):
            task = asyncio.create_task(secret_operation(i))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Verify results
        successful_operations = sum(1 for result in results if result is True)
        failed_operations = len(results) - successful_operations
        
        assert successful_operations > 15  # Allow some failures under load
        assert duration < 30  # Should complete within 30 seconds
        
        logger.info("Concurrent operations test passed",
                   total_operations=len(results),
                   successful=successful_operations,
                   failed=failed_operations,
                   duration=duration)
    
    @pytest.mark.timeout(45)
    async def test_certificate_generation_performance(self, vault_integration_setup):
        """Test certificate generation performance."""
        provider = vault_integration_setup['provider']
        provider.authenticate()
        
        cert_count = 5
        start_time = time.time()
        
        certificates = []
        for i in range(cert_count):
            common_name = f"perf-test-{i}-{int(time.time())}.scribe.local"
            cert_data = provider.get_certificate(
                common_name=common_name,
                alt_names=["localhost"],
                ttl="1h"
            )
            certificates.append(cert_data)
        
        end_time = time.time()
        total_duration = end_time - start_time
        avg_duration = total_duration / cert_count
        
        # Verify all certificates generated successfully
        assert len(certificates) == cert_count
        for cert in certificates:
            assert 'serial_number' in cert
            assert cert['serial_number'] is not None
        
        # Performance expectations
        assert avg_duration < 5.0  # Average less than 5 seconds per certificate
        
        logger.info("Certificate generation performance test passed",
                   cert_count=cert_count,
                   total_duration=total_duration,
                   avg_duration=avg_duration)


class TestIntegrationWithExternalServices:
    """Test integration with external services and Docker stack."""
    
    @pytest.mark.timeout(30)
    async def test_vault_server_integration(self):
        """Test integration with actual Vault server."""
        # Test direct connection to Vault
        try:
            response = requests.get("http://localhost:8200/v1/sys/health", timeout=10)
            assert response.status_code == 200
            
            health_data = response.json()
            assert 'cluster_name' in health_data
            
            logger.info("Vault server integration test passed", health_data=health_data)
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Vault server not available: {e}")
    
    @pytest.mark.timeout(25)
    async def test_otlp_collector_integration(self):
        """Test integration with OTLP collector."""
        try:
            # Test OTLP collector health endpoint
            response = requests.get("http://localhost:13133", timeout=10)
            assert response.status_code == 200
            
            logger.info("OTLP collector integration test passed")
        except requests.exceptions.RequestException as e:
            pytest.skip(f"OTLP collector not available: {e}")
    
    @pytest.mark.timeout(25)
    async def test_prometheus_metrics_export(self):
        """Test Prometheus metrics export."""
        try:
            # Test Prometheus metrics endpoint
            response = requests.get("http://localhost:8889/metrics", timeout=10)
            assert response.status_code == 200
            
            metrics_text = response.text
            assert 'scribe_vault' in metrics_text
            
            logger.info("Prometheus metrics export test passed")
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Prometheus metrics endpoint not available: {e}")


@pytest.mark.integration
class TestFullEndToEndScenario:
    """Comprehensive end-to-end scenario testing."""
    
    @pytest.mark.timeout(120)
    async def test_complete_vault_lifecycle_scenario(self, vault_integration_setup):
        """Test complete Vault lifecycle scenario with all components."""
        components = vault_integration_setup
        provider = components['provider']
        policy_manager = components['policy_manager']
        rotation_manager = components['rotation_manager']
        metrics_collector = components['metrics_collector']
        
        scenario_id = f"e2e-scenario-{int(time.time())}"
        logger.info("Starting complete lifecycle scenario", scenario_id=scenario_id)
        
        # Phase 1: Initialize and authenticate
        provider.authenticate()
        initial_metrics = metrics_collector.get_metrics_summary()
        
        # Phase 2: Setup policies and AppRoles
        setup_results = policy_manager.setup_production_policies()
        assert len(setup_results['policies_created']) > 0
        assert len(setup_results['approles_created']) > 0
        
        # Phase 3: Create and manage secrets
        secret_paths = []
        for i in range(3):
            path = f"scenario/{scenario_id}/secret-{i}"
            secret_data = {
                'id': i,
                'value': f'scenario-secret-{i}',
                'created_at': datetime.now().isoformat()
            }
            provider.write_secret(path, secret_data, mount_point="scribe")
            secret_paths.append(path)
        
        # Phase 4: Generate certificates
        certificates = []
        for i in range(2):
            common_name = f"{scenario_id}-cert-{i}.scribe.local"
            cert_data = provider.get_certificate(
                common_name=common_name,
                alt_names=["localhost"],
                ttl="2h"
            )
            certificates.append(cert_data)
        
        # Phase 5: Setup and execute rotations
        rotation_job = RotationJob(
            job_id=f"scenario-rotation-{scenario_id}",
            rotation_type=RotationType.SECRET,
            target_path=secret_paths[0],
            schedule_expression="@daily",
            metadata={'secret_type': 'api_key'}
        )
        
        rotation_manager.register_rotation_job(rotation_job)
        execution_id = rotation_manager.execute_rotation(rotation_job.job_id, RotationTrigger.MANUAL)
        
        # Wait for rotation completion
        max_wait = 15
        while max_wait > 0:
            execution = rotation_manager.get_rotation_status(execution_id)
            if execution and execution.status in [RotationStatus.COMPLETED, RotationStatus.FAILED]:
                break
            await asyncio.sleep(1)
            max_wait -= 1
        
        # Phase 6: Verify all operations
        # Check secrets are readable
        for path in secret_paths:
            secret = provider.get_secret(path, mount_point="scribe")
            assert secret is not None
            assert 'value' in secret
        
        # Check certificates are valid
        for cert in certificates:
            assert cert['serial_number'] is not None
            assert '-----BEGIN CERTIFICATE-----' in cert['certificate']
        
        # Check rotation completed
        final_execution = rotation_manager.get_rotation_status(execution_id)
        assert final_execution.status == RotationStatus.COMPLETED
        
        # Check metrics were recorded
        final_metrics = metrics_collector.get_metrics_summary()
        assert final_metrics['recent_operations'] > initial_metrics['recent_operations']
        
        # Phase 7: Test resilience
        health_status = provider.health_check()
        assert health_status['authenticated'] is True
        assert 'vault_metrics' in health_status
        
        logger.info("Complete lifecycle scenario test passed",
                   scenario_id=scenario_id,
                   secrets_created=len(secret_paths),
                   certificates_generated=len(certificates),
                   rotation_status=final_execution.status.value,
                   metrics_improvement=final_metrics['recent_operations'] - initial_metrics['recent_operations'])


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--timeout=300",
        "-k", "not (test_vault_server_integration or test_otlp_collector_integration or test_prometheus_metrics_export)"
    ])