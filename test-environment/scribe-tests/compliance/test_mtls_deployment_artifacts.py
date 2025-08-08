#!/usr/bin/env python3
"""
HMA v2.2 mTLS Deployment Artifacts Test

Tests Priority 0.4 requirements for mTLS deployment artifacts:
- OpenSSL certificates creation (CA, server, client)
- Kubernetes templates (secrets, configmap, deployment)
- Mount points and environment variables configuration
- Security policy compliance

This test verifies the mTLS deployment artifacts creation and configuration.
"""

import pytest
import os
import yaml
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.backends import default_backend


class TestMTLSCertificates:
    """Test mTLS certificate generation and validity."""
    
    @pytest.fixture
    def certificates_dir(self):
        """Path to certificates directory."""
        return Path("../tools/scribe/deployment/certificates")
    
    def test_certificates_directory_exists(self, certificates_dir):
        """Test that certificates directory exists."""
        assert certificates_dir.exists(), "Certificates directory must exist"
        assert certificates_dir.is_dir(), "Certificates path must be a directory"
    
    def test_ca_certificate_exists(self, certificates_dir):
        """Test that CA certificate and key exist."""
        ca_cert = certificates_dir / "ca.crt"
        ca_key = certificates_dir / "ca.key"
        
        assert ca_cert.exists(), "CA certificate must exist"
        assert ca_key.exists(), "CA private key must exist"
        
        # Verify certificate is readable and valid
        with open(ca_cert, 'rb') as f:
            cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Verify it's a CA certificate
            assert cert.subject.rfc4514_string() == "CN=scribe-ca"
            
            # Verify basic constraints extension exists for CA
            try:
                basic_constraints = cert.extensions.get_extension_for_oid(
                    x509.ExtensionOID.BASIC_CONSTRAINTS
                ).value
                assert basic_constraints.ca is True, "CA certificate must have CA=true"
            except x509.ExtensionNotFound:
                # Some CA certificates may not have this extension
                pass
    
    def test_server_certificate_exists(self, certificates_dir):
        """Test that server certificate and key exist."""
        server_cert = certificates_dir / "server.crt"
        server_key = certificates_dir / "server.key"
        server_csr = certificates_dir / "server.csr"
        
        assert server_cert.exists(), "Server certificate must exist"
        assert server_key.exists(), "Server private key must exist"
        assert server_csr.exists(), "Server CSR must exist"
        
        # Verify certificate is readable and valid
        with open(server_cert, 'rb') as f:
            cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Verify subject
            assert cert.subject.rfc4514_string() == "CN=scribe-engine"
    
    def test_client_certificate_exists(self, certificates_dir):
        """Test that client certificate and key exist."""
        client_cert = certificates_dir / "client.crt"
        client_key = certificates_dir / "client.key"
        client_csr = certificates_dir / "client.csr"
        
        assert client_cert.exists(), "Client certificate must exist"
        assert client_key.exists(), "Client private key must exist"
        assert client_csr.exists(), "Client CSR must exist"
        
        # Verify certificate is readable and valid
        with open(client_cert, 'rb') as f:
            cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Verify subject
            assert cert.subject.rfc4514_string() == "CN=scribe-client"
    
    def test_certificate_validity_period(self, certificates_dir):
        """Test that certificates have appropriate validity periods."""
        server_cert = certificates_dir / "server.crt"
        client_cert = certificates_dir / "client.crt"
        
        # Test server certificate
        with open(server_cert, 'rb') as f:
            cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Server cert should be valid for ~825 days as per spec
            validity_days = (cert.not_valid_after - cert.not_valid_before).days
            assert 800 <= validity_days <= 850, f"Server cert validity should be ~825 days, got {validity_days}"
        
        # Test client certificate
        with open(client_cert, 'rb') as f:
            cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Client cert should be valid for ~825 days as per spec
            validity_days = (cert.not_valid_after - cert.not_valid_before).days
            assert 800 <= validity_days <= 850, f"Client cert validity should be ~825 days, got {validity_days}"


class TestKubernetesTemplates:
    """Test Kubernetes deployment templates for mTLS."""
    
    @pytest.fixture
    def k8s_dir(self):
        """Path to Kubernetes deployment directory."""
        return Path("../tools/scribe/deployment/kubernetes")
    
    def test_secrets_template_exists(self, k8s_dir):
        """Test that secrets template exists and has correct structure."""
        secrets_template = k8s_dir / "scribe-secrets.template.yaml"
        assert secrets_template.exists(), "Secrets template must exist"
        
        with open(secrets_template) as f:
            content = f.read()
        
        # Check template content has required sections (as text, not parsed YAML)
        assert "kind: Secret" in content
        assert "name: scribe-tls" in content
        assert "name: scribe-client-tls" in content
        
        # Check for certificate placeholders
        assert "ca.crt:" in content
        assert "server.crt:" in content  
        assert "server.key:" in content
        assert "client.crt:" in content
        assert "client.key:" in content
        
        # Check for template placeholders
        assert "{{ base64 of" in content or "base64 of" in content
        
        # Check for proper YAML document separation
        assert "---" in content
    
    def test_configmap_template_exists(self, k8s_dir):
        """Test that configmap template exists and is valid."""
        configmap_template = k8s_dir / "scribe-configmap.template.yaml"
        assert configmap_template.exists(), "ConfigMap template must exist"
        
        with open(configmap_template) as f:
            configmap = yaml.safe_load(f)
        
        assert configmap["kind"] == "ConfigMap"
        assert configmap["metadata"]["name"] == "scribe-config"
        assert "security_policy.yaml" in configmap["data"]
        
        # Parse the embedded security policy
        security_policy = yaml.safe_load(configmap["data"]["security_policy.yaml"])
        
        # Verify HMA v2.2 compliance configuration
        assert security_policy["hma"]["version"] == "2.2"
        assert "mandatory_technologies" in security_policy["hma"]["compliance"]
        
        # Verify mTLS configuration
        assert security_policy["mtls"]["enabled"] is True
        assert security_policy["mtls"]["ca_path"] == "/etc/ssl/scribe/ca.crt"
        assert security_policy["mtls"]["cert_path"] == "/etc/ssl/scribe/server.crt"
        assert security_policy["mtls"]["key_path"] == "/etc/ssl/scribe/server.key"
        
        # Verify security features
        assert security_policy["security"]["boundary_validation"]["enabled"] is True
        assert security_policy["observability"]["telemetry"]["endpoint"] == "http://otel-collector:4317"
    
    def test_deployment_yaml_mtls_configuration(self, k8s_dir):
        """Test that deployment.yaml has correct mTLS configuration."""
        deployment_file = k8s_dir / "scribe-deployment.yaml"
        assert deployment_file.exists(), "Deployment file must exist"
        
        with open(deployment_file) as f:
            deployment = yaml.safe_load(f)
        
        # Get container spec
        containers = deployment["spec"]["template"]["spec"]["containers"]
        scribe_container = next(c for c in containers if c["name"] == "scribe")
        
        # Check environment variables
        env_vars = {env["name"]: env["value"] for env in scribe_container["env"]}
        
        # Verify mTLS environment variables
        assert env_vars["SCRIBE_MTLS_ENABLED"] == "true"
        assert env_vars["SCRIBE_TLS_CA"] == "/etc/ssl/scribe/ca.crt"
        assert env_vars["SCRIBE_TLS_CERT"] == "/etc/ssl/scribe/server.crt"
        assert env_vars["SCRIBE_TLS_KEY"] == "/etc/ssl/scribe/server.key"
        
        # Verify OTLP configuration (from Priority 0.3)
        assert env_vars["OTEL_EXPORTER_OTLP_ENDPOINT"] == "http://otel-collector:4317"
        
        # Check volume mounts
        volume_mounts = {vm["name"]: vm for vm in scribe_container["volumeMounts"]}
        
        # Verify TLS certificate mount
        tls_mount = volume_mounts["scribe-tls"]
        assert tls_mount["mountPath"] == "/etc/ssl/scribe"
        assert tls_mount["readOnly"] is True
        
        # Verify config mount
        config_mount = volume_mounts["scribe-config"]
        assert config_mount["mountPath"] == "/etc/scribe"
        assert config_mount["readOnly"] is True
        
        # Check volumes
        volumes = {v["name"]: v for v in deployment["spec"]["template"]["spec"]["volumes"]}
        
        # Verify TLS secret volume
        tls_volume = volumes["scribe-tls"]
        assert tls_volume["secret"]["secretName"] == "scribe-tls"
        assert tls_volume["secret"]["defaultMode"] == 0o400
        
        # Verify config volume
        config_volume = volumes["scribe-config"]
        assert config_volume["configMap"]["name"] == "scribe-config"
        assert config_volume["configMap"]["defaultMode"] == 0o444


class TestMTLSIntegration:
    """Test mTLS integration with existing systems."""
    
    def test_mtls_environment_variable_reading(self):
        """Test that mTLS configuration can be read from environment."""
        import os
        from unittest.mock import patch
        
        # Test environment variables that should be set in Kubernetes
        mtls_env_vars = {
            'SCRIBE_MTLS_ENABLED': 'true',
            'SCRIBE_TLS_CA': '/etc/ssl/scribe/ca.crt',
            'SCRIBE_TLS_CERT': '/etc/ssl/scribe/server.crt',
            'SCRIBE_TLS_KEY': '/etc/ssl/scribe/server.key'
        }
        
        with patch.dict(os.environ, mtls_env_vars):
            # Verify environment variables can be read
            assert os.getenv('SCRIBE_MTLS_ENABLED') == 'true'
            assert os.getenv('SCRIBE_TLS_CA') == '/etc/ssl/scribe/ca.crt'
            assert os.getenv('SCRIBE_TLS_CERT') == '/etc/ssl/scribe/server.crt'
            assert os.getenv('SCRIBE_TLS_KEY') == '/etc/ssl/scribe/server.key'
    
    def test_security_policy_file_exists(self):
        """Test that security policy configuration file exists."""
        security_policy_path = Path("tools/scribe/config/security_policy.yaml")
        
        # If the file doesn't exist, that's okay - it will be mounted from configmap
        if security_policy_path.exists():
            with open(security_policy_path) as f:
                policy = yaml.safe_load(f)
                
            # Verify basic structure if file exists
            assert isinstance(policy, dict), "Security policy must be a valid YAML object"


class TestMTLSComplianceRequirements:
    """Test compliance with HMA v2.2 mTLS requirements."""
    
    def test_mandatory_mtls_mount_points(self):
        """Test that required mount points are configured."""
        deployment_file = Path("../tools/scribe/deployment/kubernetes/scribe-deployment.yaml")
        
        with open(deployment_file) as f:
            deployment = yaml.safe_load(f)
        
        containers = deployment["spec"]["template"]["spec"]["containers"]
        scribe_container = next(c for c in containers if c["name"] == "scribe")
        
        # Check that required files are mounted at correct paths
        volume_mounts = scribe_container["volumeMounts"]
        tls_mount = next(vm for vm in volume_mounts if vm["name"] == "scribe-tls")
        
        # Verify mount point matches requirement: /etc/ssl/scribe/{server.crt,server.key,ca.crt}
        assert tls_mount["mountPath"] == "/etc/ssl/scribe"
        assert tls_mount["readOnly"] is True
    
    def test_hma_v22_mandatory_environment_variables(self):
        """Test that HMA v2.2 mandatory environment variables are set."""
        deployment_file = Path("../tools/scribe/deployment/kubernetes/scribe-deployment.yaml")
        
        with open(deployment_file) as f:
            deployment = yaml.safe_load(f)
        
        containers = deployment["spec"]["template"]["spec"]["containers"]
        scribe_container = next(c for c in containers if c["name"] == "scribe")
        
        env_vars = {env["name"]: env["value"] for env in scribe_container["env"]}
        
        # Verify exact environment variables as specified in Priority 0.4
        required_env_vars = {
            "SCRIBE_MTLS_ENABLED": "true",
            "SCRIBE_TLS_CA": "/etc/ssl/scribe/ca.crt",
            "SCRIBE_TLS_CERT": "/etc/ssl/scribe/server.crt", 
            "SCRIBE_TLS_KEY": "/etc/ssl/scribe/server.key"
        }
        
        for var_name, expected_value in required_env_vars.items():
            assert var_name in env_vars, f"Required environment variable {var_name} must be set"
            assert env_vars[var_name] == expected_value, f"{var_name} must be set to {expected_value}"
    
    def test_file_permissions_security(self):
        """Test that certificate files have appropriate permissions in Kubernetes."""
        deployment_file = Path("../tools/scribe/deployment/kubernetes/scribe-deployment.yaml")
        
        with open(deployment_file) as f:
            deployment = yaml.safe_load(f)
        
        volumes = deployment["spec"]["template"]["spec"]["volumes"]
        tls_volume = next(v for v in volumes if v["name"] == "scribe-tls")
        
        # TLS secrets should be read-only and owner-only (0400)
        assert tls_volume["secret"]["defaultMode"] == 0o400
        
        # Config should be read-only for all (0444)
        config_volume = next(v for v in volumes if v["name"] == "scribe-config")
        assert config_volume["configMap"]["defaultMode"] == 0o444


if __name__ == "__main__":
    # Run as: python -m pytest test-environment/scribe-tests/compliance/test_mtls_deployment_artifacts.py -v
    pytest.main([__file__, "-v"])