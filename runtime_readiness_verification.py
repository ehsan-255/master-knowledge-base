#!/usr/bin/env python3
"""
Scribe HMA v2.2 Runtime Readiness Verification

This script verifies that all runtime infrastructure components are properly
configured and ready for deployment, even without Docker services running.

It validates:
- Docker Compose configuration correctness
- Service configurations and networking
- Scribe engine configuration
- mTLS certificate validity
- OTLP collector configuration
- All deployment artifacts
"""

import yaml
import json
import time
from pathlib import Path
from typing import Dict, List, Any
import subprocess


class RuntimeReadinessChecker:
    """Comprehensive runtime readiness verification."""
    
    def __init__(self):
        self.checks_passed = 0
        self.checks_total = 0
        self.issues = []
    
    def print_header(self, title: str):
        """Print formatted header."""
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}")
    
    def print_check(self, description: str, passed: bool, details: str = ""):
        """Print check result."""
        self.checks_total += 1
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {description}")
        if details:
            print(f"      {details}")
        if passed:
            self.checks_passed += 1
        else:
            self.issues.append(f"{description}: {details}")
    
    def check_docker_compose_configuration(self) -> bool:
        """Verify Docker Compose configuration is valid."""
        self.print_header("DOCKER COMPOSE CONFIGURATION VERIFICATION")
        
        compose_file = Path("docker-compose.runtime.yml")
        if not compose_file.exists():
            self.print_check("Docker Compose file exists", False, "docker-compose.runtime.yml not found")
            return False
        
        try:
            with open(compose_file) as f:
                compose_config = yaml.safe_load(f)
            
            # Check required services
            required_services = ["nats", "jaeger", "prometheus", "otel-collector", "grafana", "scribe-engine"]
            services = compose_config.get("services", {})
            
            for service in required_services:
                exists = service in services
                self.print_check(f"Service '{service}' defined", exists)
            
            # Check networking
            networks_defined = "networks" in compose_config
            self.print_check("Networks defined", networks_defined)
            
            # Check volumes
            volumes_defined = "volumes" in compose_config
            self.print_check("Volumes defined", volumes_defined)
            
            # Check environment variables for Scribe
            scribe_config = services.get("scribe-engine", {})
            env_vars = scribe_config.get("environment", [])
            required_env_vars = ["OTEL_EXPORTER_OTLP_ENDPOINT", "SCRIBE_MTLS_ENABLED", "NATS_URL"]
            
            for env_var in required_env_vars:
                found = any(env_var in str(env) for env in env_vars)
                self.print_check(f"Environment variable '{env_var}' configured", found)
            
            return True
            
        except Exception as e:
            self.print_check("Docker Compose file is valid YAML", False, str(e))
            return False
    
    def check_scribe_configuration(self) -> bool:
        """Verify Scribe runtime configuration."""
        self.print_header("SCRIBE ENGINE CONFIGURATION VERIFICATION")
        
        config_file = Path("test-environment/runtime-config/scribe_runtime_config.yaml")
        if not config_file.exists():
            self.print_check("Scribe config file exists", False, "scribe_runtime_config.yaml not found")
            return False
        
        try:
            with open(config_file) as f:
                config = yaml.safe_load(f)
            
            # Check required sections
            required_sections = ["engine", "logging", "rules", "security", "telemetry", "performance"]
            for section in required_sections:
                exists = section in config
                self.print_check(f"Configuration section '{section}' defined", exists)
            
            # Check telemetry endpoint
            telemetry = config.get("telemetry", {})
            otel_endpoint = telemetry.get("endpoint", "")
            correct_endpoint = "otel-collector:4317" in otel_endpoint
            self.print_check("OTLP endpoint correctly configured", correct_endpoint, 
                           f"Endpoint: {otel_endpoint}")
            
            # Check security settings
            security = config.get("security", {})
            sandbox_enabled = security.get("enable_sandbox", False)
            self.print_check("Security sandbox enabled", sandbox_enabled)
            
            return True
            
        except Exception as e:
            self.print_check("Scribe config file is valid YAML", False, str(e))
            return False
    
    def check_mtls_certificates(self) -> bool:
        """Verify mTLS certificates are properly configured."""
        self.print_header("mTLS CERTIFICATE VERIFICATION")
        
        cert_dir = Path("tools/scribe/deployment/certificates")
        required_files = ["ca.crt", "ca.key", "server.crt", "server.key", "client.crt", "client.key"]
        
        for cert_file in required_files:
            cert_path = cert_dir / cert_file
            exists = cert_path.exists()
            self.print_check(f"Certificate file '{cert_file}' exists", exists)
            
            if exists and cert_file.endswith('.crt'):
                # Check certificate validity (basic check)
                try:
                    from cryptography import x509
                    from cryptography.hazmat.backends import default_backend
                    
                    with open(cert_path, 'rb') as f:
                        cert_data = f.read()
                        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
                    
                    # Check validity period
                    validity_days = (cert.not_valid_after - cert.not_valid_before).days
                    valid_period = 800 <= validity_days <= 850
                    self.print_check(f"Certificate '{cert_file}' has correct validity period", 
                                   valid_period, f"{validity_days} days")
                    
                except Exception as e:
                    self.print_check(f"Certificate '{cert_file}' is readable", False, str(e))
        
        return True
    
    def check_observability_configuration(self) -> bool:
        """Verify observability stack configuration."""
        self.print_header("OBSERVABILITY STACK VERIFICATION")
        
        # Check OTLP collector config
        otel_config = Path("tools/scribe/deployment/observability/otel-collector.yaml")
        if otel_config.exists():
            try:
                with open(otel_config) as f:
                    config = yaml.safe_load(f)
                
                # Check required sections
                required_sections = ["receivers", "exporters", "service"]
                for section in required_sections:
                    exists = section in config
                    self.print_check(f"OTLP collector '{section}' configured", exists)
                
                # Check OTLP receiver
                receivers = config.get("receivers", {})
                otlp_configured = "otlp" in receivers
                self.print_check("OTLP receiver configured", otlp_configured)
                
            except Exception as e:
                self.print_check("OTLP collector config is valid", False, str(e))
        else:
            self.print_check("OTLP collector config exists", False)
        
        # Check Prometheus config
        prom_config = Path("tools/scribe/deployment/observability/prometheus.yml")
        if prom_config.exists():
            try:
                with open(prom_config) as f:
                    config = yaml.safe_load(f)
                
                scrape_configs = config.get("scrape_configs", [])
                scribe_target_found = any(
                    "scribe-engine" in str(job.get("job_name", "")) 
                    for job in scrape_configs
                )
                self.print_check("Prometheus scraping Scribe engine", scribe_target_found)
                
            except Exception as e:
                self.print_check("Prometheus config is valid", False, str(e))
        else:
            self.print_check("Prometheus config exists", False)
        
        # Check alert rules
        alert_rules = Path("tools/scribe/deployment/observability/alert_rules.yml")
        if alert_rules.exists():
            try:
                with open(alert_rules) as f:
                    config = yaml.safe_load(f)
                
                groups = config.get("groups", [])
                hma_alerts_found = any(
                    "hma" in group.get("name", "").lower() 
                    for group in groups
                )
                self.print_check("HMA v2.2 compliance alerts configured", hma_alerts_found)
                
            except Exception as e:
                self.print_check("Alert rules config is valid", False, str(e))
        else:
            self.print_check("Alert rules config exists", False)
        
        return True
    
    def check_kubernetes_deployment_readiness(self) -> bool:
        """Verify Kubernetes deployment templates."""
        self.print_header("KUBERNETES DEPLOYMENT VERIFICATION")
        
        k8s_dir = Path("tools/scribe/deployment/kubernetes")
        required_files = [
            "scribe-deployment.yaml",
            "scribe-secrets.template.yaml", 
            "scribe-configmap.template.yaml"
        ]
        
        for k8s_file in required_files:
            file_path = k8s_dir / k8s_file
            exists = file_path.exists()
            self.print_check(f"Kubernetes file '{k8s_file}' exists", exists)
            
            if exists and k8s_file.endswith('.yaml'):
                try:
                    with open(file_path) as f:
                        content = f.read()
                    
                    # Check if it's a template file (contains template placeholders)
                    is_template = '{{' in content and '}}' in content
                    
                    if is_template:
                        # For template files, just check basic YAML structure without parsing values
                        # Remove template placeholders temporarily for validation
                        temp_content = content
                        import re
                        temp_content = re.sub(r'\{\{[^}]+\}\}', '"TEMPLATE_PLACEHOLDER"', temp_content)
                        documents = list(yaml.safe_load_all(temp_content))
                        valid = len(documents) > 0 and all(doc is not None for doc in documents if doc)
                        self.print_check(f"Kubernetes template '{k8s_file}' has valid structure", valid)
                    else:
                        # Regular YAML file
                        documents = list(yaml.safe_load_all(content))
                        valid = len(documents) > 0 and all(doc is not None for doc in documents if doc)
                        self.print_check(f"Kubernetes file '{k8s_file}' is valid YAML", valid)
                        
                except Exception as e:
                    self.print_check(f"Kubernetes file '{k8s_file}' validation", False, str(e))
        
        return True
    
    def check_scribe_package_readiness(self) -> bool:
        """Verify Scribe package is properly configured."""
        self.print_header("SCRIBE PACKAGE VERIFICATION")
        
        # Check setup.py
        setup_file = Path("tools/scribe/setup.py")
        setup_exists = setup_file.exists()
        self.print_check("setup.py exists", setup_exists)
        
        # Check requirements.txt
        req_file = Path("tools/scribe/requirements.txt")
        req_exists = req_file.exists()
        self.print_check("requirements.txt exists", req_exists)
        
        if req_exists:
            try:
                with open(req_file) as f:
                    requirements = f.read()
                
                required_deps = ["nats-py", "opentelemetry", "fastapi", "structlog", "watchdog"]
                for dep in required_deps:
                    found = dep in requirements
                    self.print_check(f"Dependency '{dep}' in requirements", found)
                    
            except Exception as e:
                self.print_check("Requirements file is readable", False, str(e))
        
        # Check main.py
        main_file = Path("tools/scribe/main.py")
        main_exists = main_file.exists()
        self.print_check("main.py entry point exists", main_exists)
        
        return True
    
    def run_comprehensive_verification(self) -> bool:
        """Run all verification checks."""
        print("SCRIBE HMA v2.2 RUNTIME READINESS VERIFICATION")
        print("=" * 70)
        print("Verifying all runtime infrastructure components are ready for deployment...")
        
        # Run all checks
        self.check_docker_compose_configuration()
        self.check_scribe_configuration()
        self.check_mtls_certificates()
        self.check_observability_configuration()
        self.check_kubernetes_deployment_readiness()
        self.check_scribe_package_readiness()
        
        # Summary
        self.print_header("VERIFICATION SUMMARY")
        
        success_rate = (self.checks_passed / self.checks_total) * 100 if self.checks_total > 0 else 0
        
        print(f"Total Checks: {self.checks_total}")
        print(f"Passed: {self.checks_passed}")
        print(f"Failed: {self.checks_total - self.checks_passed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.issues:
            print(f"\nIssues Found:")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        
        is_ready = success_rate >= 95  # 95% success rate threshold
        
        if is_ready:
            self.print_header("SUCCESS: RUNTIME INFRASTRUCTURE IS READY!")
            print("All critical components are properly configured.")
            print("The Scribe HMA v2.2 engine is ready for deployment.")
            print("\nTo deploy:")
            print("  docker-compose -f docker-compose.runtime.yml up -d")
            print("\nTo run integration tests:")
            print("  python run_runtime_tests.py")
        else:
            self.print_header("ISSUES FOUND: Runtime readiness verification failed")
            print("Please resolve the issues above before deployment.")
        
        return is_ready


def main():
    """Main entry point."""
    checker = RuntimeReadinessChecker()
    success = checker.run_comprehensive_verification()
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)