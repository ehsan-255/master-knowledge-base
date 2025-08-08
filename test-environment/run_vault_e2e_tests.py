#!/usr/bin/env python3
"""
Vault End-to-End Test Runner

Comprehensive test runner for Vault secret lifecycle with Docker stack management
ensuring enterprise-grade validation of all Vault integration components.
"""

import os
import sys
import time
import json
import subprocess
import tempfile
import signal
from pathlib import Path
from typing import Dict, Any, List, Optional
import structlog
import requests
import docker
import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = structlog.get_logger(__name__)


class VaultE2ETestRunner:
    """
    Professional end-to-end test runner for Vault integration.
    
    Manages Docker stack deployment, service health checks, test execution,
    and comprehensive result reporting for enterprise validation.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize test runner.
        
        Args:
            config_dir: Optional configuration directory
        """
        self.project_root = project_root
        self.config_dir = Path(config_dir) if config_dir else self.project_root / "tools" / "scribe" / "deployment"
        self.test_results: Dict[str, Any] = {}
        self.docker_client = None
        self.services_started = False
        
        # Test configuration
        self.test_config = {
            'vault_url': 'http://localhost:8200',
            'vault_token': 'dev-only-token',
            'otlp_endpoint': 'http://localhost:4317',
            'prometheus_url': 'http://localhost:8889',
            'grafana_url': 'http://localhost:3000',
            'max_startup_wait': 180,
            'health_check_interval': 5,
            'test_timeout': 300
        }
        
        logger.info("Vault E2E test runner initialized",
                   config_dir=str(self.config_dir),
                   test_config=self.test_config)
    
    def setup_docker_environment(self) -> bool:
        """
        Setup Docker environment for testing.
        
        Returns:
            True if setup successful
        """
        try:
            self.docker_client = docker.from_env()
            
            # Verify Docker is running
            self.docker_client.ping()
            
            logger.info("Docker environment setup completed")
            return True
            
        except Exception as e:
            logger.error("Failed to setup Docker environment", error=str(e))
            return False
    
    def start_test_stack(self) -> bool:
        """
        Start the complete test stack using Docker Compose.
        
        Returns:
            True if stack started successfully
        """
        try:
            compose_file = self.config_dir / "docker-compose.runtime.yml"
            
            if not compose_file.exists():
                logger.error("Docker Compose file not found", file=str(compose_file))
                return False
            
            logger.info("Starting Docker test stack", compose_file=str(compose_file))
            
            # Start services
            cmd = [
                "docker-compose",
                "-f", str(compose_file),
                "up", "-d",
                "--build"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(compose_file.parent)
            )
            
            if result.returncode != 0:
                logger.error("Failed to start Docker stack",
                           stderr=result.stderr,
                           stdout=result.stdout)
                return False
            
            self.services_started = True
            logger.info("Docker test stack started successfully")
            
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("Docker stack startup timed out")
            return False
        except Exception as e:
            logger.error("Failed to start Docker stack", error=str(e))
            return False
    
    def wait_for_services(self) -> bool:
        """
        Wait for all services to become healthy.
        
        Returns:
            True if all services are healthy
        """
        logger.info("Waiting for services to become healthy")
        
        services_to_check = [
            {
                'name': 'Vault',
                'url': f"{self.test_config['vault_url']}/v1/sys/health",
                'expected_status': 200,
                'required': True
            },
            {
                'name': 'OTLP Collector',
                'url': 'http://localhost:13133',
                'expected_status': 200,
                'required': True
            },
            {
                'name': 'Prometheus',
                'url': f"{self.test_config['prometheus_url']}/api/v1/status/config",
                'expected_status': 200,
                'required': False
            },
            {
                'name': 'Grafana',
                'url': f"{self.test_config['grafana_url']}/api/health",
                'expected_status': 200,
                'required': False
            }
        ]
        
        max_wait = self.test_config['max_startup_wait']
        check_interval = self.test_config['health_check_interval']
        
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait:
            all_healthy = True
            
            for service in services_to_check:
                try:
                    response = requests.get(
                        service['url'],
                        timeout=10,
                        verify=False
                    )
                    
                    if response.status_code == service['expected_status']:
                        logger.debug("Service healthy", 
                                   service=service['name'],
                                   url=service['url'])
                    else:
                        if service['required']:
                            all_healthy = False
                        logger.warning("Service not healthy",
                                     service=service['name'],
                                     status_code=response.status_code)
                        
                except requests.exceptions.RequestException as e:
                    if service['required']:
                        all_healthy = False
                    logger.warning("Service not reachable",
                                 service=service['name'],
                                 error=str(e))
            
            if all_healthy:
                logger.info("All required services are healthy",
                           elapsed_time=time.time() - start_time)
                return True
            
            time.sleep(check_interval)
        
        logger.error("Services health check timed out",
                   max_wait=max_wait)
        return False
    
    def initialize_vault_for_testing(self) -> bool:
        """
        Initialize Vault with test data and policies.
        
        Returns:
            True if initialization successful
        """
        try:
            logger.info("Initializing Vault for testing")
            
            # Set environment variables for Vault
            env = os.environ.copy()
            env.update({
                'VAULT_ADDR': self.test_config['vault_url'],
                'VAULT_TOKEN': self.test_config['vault_token']
            })
            
            # Run Vault initialization script
            init_script = self.config_dir / "vault" / "init" / "init-vault.sh"
            
            if not init_script.exists():
                logger.warning("Vault init script not found", script=str(init_script))
                return True  # Continue without initialization
            
            # Make script executable
            os.chmod(init_script, 0o755)
            
            result = subprocess.run(
                [str(init_script)],
                env=env,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                logger.info("Vault initialization completed successfully")
                return True
            else:
                logger.warning("Vault initialization had issues",
                             stderr=result.stderr,
                             stdout=result.stdout)
                return True  # Continue anyway for testing
                
        except Exception as e:
            logger.error("Failed to initialize Vault", error=str(e))
            return False
    
    def run_test_suite(self) -> Dict[str, Any]:
        """
        Execute the complete test suite.
        
        Returns:
            Test results summary
        """
        logger.info("Starting Vault E2E test suite execution")
        
        # Prepare test environment
        test_env = os.environ.copy()
        test_env.update({
            'VAULT_ADDR': self.test_config['vault_url'],
            'VAULT_TOKEN': self.test_config['vault_token'],
            'OTEL_EXPORTER_OTLP_ENDPOINT': self.test_config['otlp_endpoint'],
            'OTEL_SERVICE_NAME': 'scribe-vault-e2e-test',
            'PYTHONPATH': str(self.project_root)
        })
        
        # Test file path
        test_file = self.project_root / "test-environment" / "scribe-tests" / "test_vault_e2e_lifecycle.py"
        
        # Prepare pytest arguments
        pytest_args = [
            str(test_file),
            "-v",
            "--tb=short",
            f"--timeout={self.test_config['test_timeout']}",
            "--capture=no",
            "--junit-xml=vault_e2e_results.xml",
            "--json-report",
            "--json-report-file=vault_e2e_results.json"
        ]
        
        try:
            logger.info("Executing pytest with E2E tests",
                       test_file=str(test_file),
                       args=pytest_args)
            
            # Run tests
            result = subprocess.run(
                ["python", "-m", "pytest"] + pytest_args,
                env=test_env,
                capture_output=True,
                text=True,
                timeout=self.test_config['test_timeout'] + 60,
                cwd=str(self.project_root)
            )
            
            # Parse results
            test_results = {
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0,
                'timestamp': time.time()
            }
            
            # Try to load JSON results if available
            json_results_file = self.project_root / "vault_e2e_results.json"
            if json_results_file.exists():
                try:
                    with open(json_results_file, 'r') as f:
                        json_results = json.load(f)
                        test_results['detailed_results'] = json_results
                except Exception as e:
                    logger.warning("Failed to load JSON test results", error=str(e))
            
            self.test_results = test_results
            
            logger.info("Test suite execution completed",
                       success=test_results['success'],
                       return_code=test_results['return_code'])
            
            return test_results
            
        except subprocess.TimeoutExpired:
            logger.error("Test suite execution timed out")
            return {
                'return_code': -1,
                'success': False,
                'error': 'Test execution timed out',
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error("Failed to execute test suite", error=str(e))
            return {
                'return_code': -1,
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def generate_test_report(self) -> str:
        """
        Generate comprehensive test report.
        
        Returns:
            Test report as string
        """
        if not self.test_results:
            return "No test results available"
        
        report_lines = [
            "=" * 80,
            "🔐 VAULT END-TO-END TEST RESULTS - SCRIBE HMA v2.2",
            "=" * 80,
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.test_results['timestamp']))}",
            f"Overall Result: {'✅ PASSED' if self.test_results['success'] else '❌ FAILED'}",
            f"Return Code: {self.test_results['return_code']}",
            "",
            "📊 Test Configuration:",
            f"  Vault URL: {self.test_config['vault_url']}",
            f"  OTLP Endpoint: {self.test_config['otlp_endpoint']}",
            f"  Test Timeout: {self.test_config['test_timeout']}s",
            ""
        ]
        
        # Add detailed results if available
        if 'detailed_results' in self.test_results:
            detailed = self.test_results['detailed_results']
            summary = detailed.get('summary', {})
            
            report_lines.extend([
                "📈 Test Summary:",
                f"  Total Tests: {summary.get('total', 'N/A')}",
                f"  Passed: {summary.get('passed', 'N/A')}",
                f"  Failed: {summary.get('failed', 'N/A')}",
                f"  Skipped: {summary.get('skipped', 'N/A')}",
                f"  Duration: {summary.get('duration', 'N/A')}s",
                ""
            ])
            
            # Add test details
            if 'tests' in detailed:
                report_lines.append("🧪 Test Details:")
                for test in detailed['tests']:
                    status = "✅" if test.get('outcome') == 'passed' else "❌"
                    duration = test.get('duration', 0)
                    report_lines.append(f"  {status} {test.get('nodeid', 'Unknown')} ({duration:.2f}s)")
                report_lines.append("")
        
        # Add stdout/stderr if available
        if self.test_results.get('stdout'):
            report_lines.extend([
                "📝 Test Output:",
                "=" * 40,
                self.test_results['stdout'],
                "=" * 40,
                ""
            ])
        
        if self.test_results.get('stderr'):
            report_lines.extend([
                "🚨 Error Output:",
                "=" * 40,
                self.test_results['stderr'],
                "=" * 40,
                ""
            ])
        
        report_lines.extend([
            "🏁 Test Execution Summary:",
            f"  Services Started: {'✅' if self.services_started else '❌'}",
            f"  Docker Environment: {'✅' if self.docker_client else '❌'}",
            f"  Overall Success: {'✅' if self.test_results['success'] else '❌'}",
            "",
            "=" * 80,
            "End of Vault E2E Test Report",
            "=" * 80
        ])
        
        return "\n".join(report_lines)
    
    def cleanup_test_environment(self):
        """Clean up test environment and Docker services."""
        logger.info("Cleaning up test environment")
        
        try:
            if self.services_started:
                compose_file = self.config_dir / "docker-compose.runtime.yml"
                
                if compose_file.exists():
                    cmd = [
                        "docker-compose",
                        "-f", str(compose_file),
                        "down",
                        "-v"  # Remove volumes
                    ]
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=60,
                        cwd=str(compose_file.parent)
                    )
                    
                    if result.returncode == 0:
                        logger.info("Docker stack stopped successfully")
                    else:
                        logger.warning("Docker stack cleanup had issues",
                                     stderr=result.stderr)
            
            # Clean up result files
            result_files = [
                self.project_root / "vault_e2e_results.xml",
                self.project_root / "vault_e2e_results.json"
            ]
            
            for file_path in result_files:
                if file_path.exists():
                    file_path.unlink()
            
            logger.info("Test environment cleanup completed")
            
        except Exception as e:
            logger.error("Error during cleanup", error=str(e))
    
    def run_complete_test_cycle(self) -> bool:
        """
        Run complete test cycle with setup, execution, and cleanup.
        
        Returns:
            True if all tests passed
        """
        success = False
        
        try:
            logger.info("🚀 Starting complete Vault E2E test cycle")
            
            # Setup phase
            if not self.setup_docker_environment():
                logger.error("Failed to setup Docker environment")
                return False
            
            if not self.start_test_stack():
                logger.error("Failed to start test stack")
                return False
            
            if not self.wait_for_services():
                logger.error("Services failed to become healthy")
                return False
            
            if not self.initialize_vault_for_testing():
                logger.error("Failed to initialize Vault")
                return False
            
            # Test execution phase
            test_results = self.run_test_suite()
            success = test_results.get('success', False)
            
            # Report generation
            report = self.generate_test_report()
            print(report)
            
            # Save report to file
            report_file = self.project_root / f"vault_e2e_report_{int(time.time())}.txt"
            with open(report_file, 'w') as f:
                f.write(report)
            
            logger.info("Test report saved", report_file=str(report_file))
            
            return success
            
        except KeyboardInterrupt:
            logger.warning("Test cycle interrupted by user")
            return False
        except Exception as e:
            logger.error("Unexpected error in test cycle", error=str(e))
            return False
        finally:
            # Always cleanup
            self.cleanup_test_environment()


def main():
    """Main entry point for test runner."""
    # Setup structured logging
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
    
    # Create and run test runner
    runner = VaultE2ETestRunner()
    
    # Handle interruption gracefully
    def signal_handler(signum, frame):
        logger.info("Received interrupt signal, cleaning up...")
        runner.cleanup_test_environment()
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run complete test cycle
    success = runner.run_complete_test_cycle()
    
    if success:
        logger.info("🎉 All Vault E2E tests passed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Some Vault E2E tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()