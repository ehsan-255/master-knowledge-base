#!/usr/bin/env python3
"""
Scribe HMA v2.2 Runtime Integration Test Runner

This script orchestrates the complete runtime testing process:
1. Starts Docker Compose stack with real services
2. Waits for services to be healthy
3. Runs comprehensive integration tests
4. Reports results and cleans up

Usage:
    python run_runtime_tests.py [--cleanup-only] [--no-cleanup]
"""

import subprocess
import time
import requests
import argparse
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple


class RuntimeTestRunner:
    """Manages the complete runtime testing lifecycle."""
    
    def __init__(self):
        self.docker_compose_file = "docker-compose.runtime.yml"
        self.services_to_check = {
            "NATS": ("http://localhost:8222/healthz", 200),
            "Prometheus": ("http://localhost:9090/-/healthy", 200),
            "Jaeger": ("http://localhost:16686/", 200),
            "OTLP Collector": ("http://localhost:13133/", 200),
            "Grafana": ("http://localhost:3000/api/health", 200),
            "Scribe Engine": ("http://localhost:9469/health", 200)
        }
        
    def print_header(self, title: str):
        """Print a formatted header."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def print_step(self, step: str):
        """Print a formatted step."""
        print(f"\n[STEP] {step}")
    
    def print_success(self, message: str):
        """Print a success message."""
        print(f"[OK] {message}")
    
    def print_error(self, message: str):
        """Print an error message."""
        print(f"[ERROR] {message}")
    
    def print_warning(self, message: str):
        """Print a warning message."""
        print(f"[WARN] {message}")
    
    def check_prerequisites(self) -> bool:
        """Check if Docker and Docker Compose are available."""
        self.print_step("Checking prerequisites...")
        
        try:
            # Check Docker
            result = subprocess.run(["docker", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                self.print_error("Docker is not available")
                return False
            self.print_success(f"Docker: {result.stdout.strip()}")
            
            # Check Docker Compose
            result = subprocess.run(["docker-compose", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                self.print_error("Docker Compose is not available")
                return False
            self.print_success(f"Docker Compose: {result.stdout.strip()}")
            
            # Check if compose file exists
            if not Path(self.docker_compose_file).exists():
                self.print_error(f"Docker Compose file {self.docker_compose_file} not found")
                return False
            self.print_success(f"Found {self.docker_compose_file}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Prerequisites check failed: {e}")
            return False
    
    def start_docker_stack(self) -> bool:
        """Start the Docker Compose stack."""
        self.print_step("Starting Docker Compose stack...")
        
        try:
            # Stop any existing containers first
            subprocess.run(["docker-compose", "-f", self.docker_compose_file, "down"], 
                         capture_output=True)
            
            # Start the stack
            result = subprocess.run([
                "docker-compose", "-f", self.docker_compose_file, 
                "up", "-d", "--build"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                self.print_error(f"Failed to start Docker stack: {result.stderr}")
                return False
            
            self.print_success("Docker Compose stack started")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to start Docker stack: {e}")
            return False
    
    def wait_for_services_healthy(self, timeout_seconds: int = 300) -> bool:
        """Wait for all services to be healthy with robust retry logic."""
        self.print_step(f"Waiting for services to be healthy (timeout: {timeout_seconds}s)...")
        
        start_time = time.time()
        healthy_services = set()
        retry_counts = {}
        
        # Special handling for slow-starting services
        slow_services = {"Scribe Engine"}
        
        while time.time() - start_time < timeout_seconds:
            for service_name, (health_url, expected_status) in self.services_to_check.items():
                if service_name in healthy_services:
                    continue
                
                # Use longer timeout for slow services
                request_timeout = 10 if service_name in slow_services else 5
                retry_counts[service_name] = retry_counts.get(service_name, 0) + 1
                
                try:
                    response = requests.get(health_url, timeout=request_timeout)
                    if response.status_code == expected_status:
                        healthy_services.add(service_name)
                        self.print_success(f"{service_name} is healthy (attempt {retry_counts[service_name]})")
                    elif service_name == "Scribe Engine" and retry_counts[service_name] % 10 == 0:
                        self.print_warning(f"Scribe Engine still installing dependencies... (attempt {retry_counts[service_name]})")
                except requests.RequestException as e:
                    # Log connection issues for debugging slow services
                    if service_name in slow_services and retry_counts[service_name] % 20 == 0:
                        self.print_warning(f"{service_name} not ready: {type(e).__name__} (attempt {retry_counts[service_name]})")
                    pass  # Service not ready yet
            
            if len(healthy_services) == len(self.services_to_check):
                self.print_success("All services are healthy!")
                return True
            
            # Exponential backoff with max 10s
            wait_time = min(2 * (1.1 ** (sum(retry_counts.values()) / len(self.services_to_check))), 10)
            time.sleep(wait_time)
        
        # Print which services are still unhealthy
        unhealthy = set(self.services_to_check.keys()) - healthy_services
        for service in unhealthy:
            attempts = retry_counts.get(service, 0)
            self.print_error(f"{service} is not healthy after {attempts} attempts")
        
        return False
    
    def run_integration_tests(self) -> Tuple[bool, str]:
        """Run the integration tests."""
        self.print_step("Running integration tests...")
        
        try:
            # Change to test directory
            test_dir = Path("test-environment")
            if not test_dir.exists():
                self.print_error("test-environment directory not found")
                return False, "Test directory not found"
            
            # Run pytest on runtime tests
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "scribe-tests/runtime/", 
                "-v", "--tb=short", "--timeout=30"
            ], cwd=test_dir, capture_output=True, text=True, timeout=300)
            
            test_output = result.stdout + result.stderr
            
            if result.returncode == 0:
                self.print_success("All integration tests passed!")
                return True, test_output
            else:
                self.print_error("Some integration tests failed")
                return False, test_output
                
        except Exception as e:
            error_msg = f"Failed to run integration tests: {e}"
            self.print_error(error_msg)
            return False, error_msg
    
    def show_service_logs(self):
        """Show logs from key services for debugging."""
        self.print_step("Showing service logs for debugging...")
        
        services_to_log = ["scribe-engine", "otel-collector", "nats"]
        
        for service in services_to_log:
            print(f"\n--- {service.upper()} LOGS ---")
            try:
                result = subprocess.run([
                    "docker-compose", "-f", self.docker_compose_file, 
                    "logs", "--tail=20", service
                ], capture_output=True, text=True, timeout=10)
                print(result.stdout)
            except Exception as e:
                print(f"Could not get logs for {service}: {e}")
    
    def cleanup_docker_stack(self):
        """Clean up the Docker Compose stack."""
        self.print_step("Cleaning up Docker Compose stack...")
        
        try:
            result = subprocess.run([
                "docker-compose", "-f", self.docker_compose_file, 
                "down", "-v"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.print_success("Docker stack cleaned up")
            else:
                self.print_warning(f"Cleanup may have issues: {result.stderr}")
                
        except Exception as e:
            self.print_warning(f"Cleanup failed: {e}")
    
    def run_full_test_cycle(self, cleanup_after: bool = True) -> bool:
        """Run the complete test cycle."""
        self.print_header("SCRIBE HMA v2.2 RUNTIME INTEGRATION TESTS")
        
        # Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Start Docker stack
        if not self.start_docker_stack():
            return False
        
        # Wait for services
        if not self.wait_for_services_healthy():
            self.show_service_logs()
            if cleanup_after:
                self.cleanup_docker_stack()
            return False
        
        # Run tests
        tests_passed, test_output = self.run_integration_tests()
        
        # Show test output
        print("\n" + "="*60)
        print("  TEST OUTPUT")
        print("="*60)
        print(test_output)
        
        if not tests_passed:
            self.show_service_logs()
        
        # Cleanup
        if cleanup_after:
            self.cleanup_docker_stack()
        
        # Final result
        if tests_passed:
            self.print_header("SUCCESS: ALL RUNTIME INTEGRATION TESTS PASSED!")
            return True
        else:
            self.print_header("FAILURE: SOME RUNTIME INTEGRATION TESTS FAILED")
            return False


def main():
    parser = argparse.ArgumentParser(description="Run Scribe runtime integration tests")
    parser.add_argument("--cleanup-only", action="store_true", 
                       help="Only cleanup existing Docker stack")
    parser.add_argument("--no-cleanup", action="store_true",
                       help="Don't cleanup Docker stack after tests")
    
    args = parser.parse_args()
    
    runner = RuntimeTestRunner()
    
    if args.cleanup_only:
        runner.cleanup_docker_stack()
        return
    
    success = runner.run_full_test_cycle(cleanup_after=not args.no_cleanup)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()