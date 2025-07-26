#!/usr/bin/env python3
"""
Scribe Vault Secret Provider

Professional HashiCorp Vault integration for centralized secret management
as required by enterprise security standards and HMA v2.2 compliance.
"""

import os
import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, Tuple
from dataclasses import dataclass
from enum import Enum
import structlog
import hvac
from hvac.exceptions import VaultError, InvalidPath, Forbidden
import tempfile
import json
import ssl
from datetime import datetime, timedelta

from .logging_config import get_scribe_logger
from .vault_circuit_breaker import get_vault_circuit_breaker_manager, circuit_breaker_protected
from .vault_retry_handler import get_vault_retry_manager, retry_on_failure, RetryExhaustedError
from .vault_graceful_degradation import (
    get_vault_degradation_manager, 
    DegradationConfig, 
    DegradationStrategy,
    ServiceMode
)
from .vault_metrics_collector import get_vault_metrics_collector, OperationStatus

logger = get_scribe_logger(__name__)


class AuthMethod(Enum):
    """Supported Vault authentication methods."""
    APPROLE = "approle"
    TOKEN = "token"
    KUBERNETES = "kubernetes"
    AWS = "aws"


@dataclass
class VaultConfig:
    """Configuration for Vault connection and authentication."""
    url: str
    auth_method: AuthMethod
    mount_point: str = "auth/approle"
    namespace: Optional[str] = None
    ca_cert_path: Optional[str] = None
    client_cert_path: Optional[str] = None
    client_key_path: Optional[str] = None
    verify_ssl: bool = True
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0


@dataclass
class SecretMetadata:
    """Metadata for cached secrets."""
    secret_data: Dict[str, Any]
    retrieved_at: datetime
    ttl_seconds: int
    lease_id: Optional[str] = None
    renewable: bool = False

    @property
    def is_expired(self) -> bool:
        """Check if the secret has expired."""
        if self.ttl_seconds <= 0:
            return False  # No expiration
        return datetime.now() > self.retrieved_at + timedelta(seconds=self.ttl_seconds)

    @property
    def needs_renewal(self) -> bool:
        """Check if the secret needs renewal (at 80% of TTL)."""
        if not self.renewable or self.ttl_seconds <= 0:
            return False
        renewal_threshold = self.retrieved_at + timedelta(seconds=self.ttl_seconds * 0.8)
        return datetime.now() > renewal_threshold


class VaultSecretProvider:
    """
    Professional Vault secret provider with authentication, caching, and error handling.
    
    This class provides a robust interface to HashiCorp Vault for secret management
    in the Scribe HMA v2.2 architecture.
    """

    def __init__(self, config: VaultConfig):
        """
        Initialize Vault secret provider with enterprise resilience patterns.
        
        Args:
            config: Vault configuration
        """
        self.config = config
        self._client: Optional[hvac.Client] = None
        self._authenticated = False
        self._secret_cache: Dict[str, SecretMetadata] = {}
        self._lock = threading.RLock()
        self._auth_lock = threading.Lock()
        
        # Authentication credentials
        self._role_id: Optional[str] = None
        self._secret_id: Optional[str] = None
        self._token: Optional[str] = None
        
        # Initialize resilience components
        self._circuit_breaker_manager = get_vault_circuit_breaker_manager()
        self._retry_manager = get_vault_retry_manager()
        self._degradation_manager = get_vault_degradation_manager(
            DegradationConfig(
                enable_secret_cache=True,
                cache_ttl_seconds=3600,
                vault_failure_threshold=3,
                allow_insecure_fallback=False
            )
        )
        
        # Initialize metrics collector
        self._metrics_collector = get_vault_metrics_collector()
        
        # Metrics for monitoring
        self._operation_count = 0
        self._failure_count = 0
        self._degraded_operations = 0
        self._cache_hits = 0
        self._cache_misses = 0
        
        logger.info("Vault secret provider initialized with resilience patterns",
                    vault_url=config.url,
                    auth_method=config.auth_method.value,
                    namespace=config.namespace,
                    circuit_breaker_enabled=True,
                    retry_enabled=True,
                    degradation_enabled=True)

    def configure_authentication(self, **auth_params) -> None:
        """
        Configure authentication parameters.
        
        Args:
            **auth_params: Authentication parameters specific to the method
                          - For AppRole: role_id, secret_id
                          - For Token: token
                          - For Kubernetes: jwt_token, role
        """
        with self._auth_lock:
            if self.config.auth_method == AuthMethod.APPROLE:
                self._role_id = auth_params.get('role_id')
                self._secret_id = auth_params.get('secret_id')
                if not self._role_id or not self._secret_id:
                    raise ValueError("AppRole authentication requires role_id and secret_id")
                    
            elif self.config.auth_method == AuthMethod.TOKEN:
                self._token = auth_params.get('token')
                if not self._token:
                    raise ValueError("Token authentication requires token")
                    
            else:
                raise NotImplementedError(f"Authentication method {self.config.auth_method} not implemented")
                
            logger.debug("Authentication configured",
                        auth_method=self.config.auth_method.value)

    def _create_client(self) -> hvac.Client:
        """Create and configure Vault client."""
        client_kwargs = {
            'url': self.config.url,
            'namespace': self.config.namespace,
            'timeout': self.config.timeout
        }
        
        # Configure TLS
        if self.config.verify_ssl:
            if self.config.ca_cert_path:
                client_kwargs['verify'] = self.config.ca_cert_path
            if self.config.client_cert_path and self.config.client_key_path:
                client_kwargs['cert'] = (self.config.client_cert_path, self.config.client_key_path)
        else:
            client_kwargs['verify'] = False
            
        return hvac.Client(**client_kwargs)

    @circuit_breaker_protected("auth")
    @retry_on_failure("auth")
    def authenticate(self) -> bool:
        """
        Authenticate with Vault using configured method with resilience patterns.
        
        Returns:
            True if authentication successful, False otherwise
        """
        with self._auth_lock:
            self._operation_count += 1
            start_time = time.time()
            operation_id = f"auth_{int(start_time)}"
            
            # Start metrics tracking
            span = self._metrics_collector.start_operation(
                operation_id=operation_id,
                operation_type="authenticate",
                auth_method=self.config.auth_method.value
            )
            
            try:
                if not self._client:
                    self._client = self._create_client()
                
                if self.config.auth_method == AuthMethod.APPROLE:
                    response = self._client.auth.approle.login(
                        role_id=self._role_id,
                        secret_id=self._secret_id,
                        mount_point=self.config.mount_point.split('/')[-1]
                    )
                    
                elif self.config.auth_method == AuthMethod.TOKEN:
                    self._client.token = self._token
                    # Verify token is valid
                    self._client.lookup_token()
                    
                self._authenticated = True
                self._degradation_manager.handle_vault_success("authenticate")
                
                # Record successful authentication metrics
                duration = time.time() - start_time
                self._metrics_collector.record_auth_attempt(
                    auth_method=self.config.auth_method.value,
                    status=OperationStatus.SUCCESS,
                    duration=duration
                )
                
                self._metrics_collector.end_operation(
                    operation_id=operation_id,
                    span=span,
                    status=OperationStatus.SUCCESS,
                    duration=duration
                )
                
                logger.info("Successfully authenticated with Vault",
                           auth_method=self.config.auth_method.value,
                           duration=duration)
                return True
                
            except Exception as e:
                self._failure_count += 1
                self._degradation_manager.handle_vault_failure(e, "authenticate")
                
                # Record failed authentication metrics
                duration = time.time() - start_time
                self._metrics_collector.record_auth_attempt(
                    auth_method=self.config.auth_method.value,
                    status=OperationStatus.FAILURE,
                    duration=duration
                )
                
                self._metrics_collector.end_operation(
                    operation_id=operation_id,
                    span=span,
                    status=OperationStatus.FAILURE,
                    duration=duration,
                    error=str(e)
                )
                
                logger.error("Failed to authenticate with Vault",
                           auth_method=self.config.auth_method.value,
                           error=str(e),
                           duration=duration)
                self._authenticated = False
                raise  # Re-raise for circuit breaker and retry logic

    def _ensure_authenticated(self) -> None:
        """Ensure the client is authenticated, authenticate if necessary."""
        if not self._authenticated or not self._client or not self._client.is_authenticated():
            if not self.authenticate():
                raise VaultError("Failed to authenticate with Vault")

    def get_secret(self, path: str, mount_point: str = "kv") -> Dict[str, Any]:
        """
        Retrieve secret from Vault with comprehensive resilience patterns.
        
        Args:
            path: Secret path
            mount_point: Secret engine mount point
            
        Returns:
            Secret data
        """
        self._operation_count += 1
        
        # Use degradation manager for resilient secret retrieval
        def vault_secret_operation(secret_path: str, **kwargs) -> Dict[str, Any]:
            return self._fetch_secret_from_vault(secret_path, mount_point)
        
        try:
            result = self._degradation_manager.get_secret_with_degradation(
                path=path,
                vault_func=vault_secret_operation,
                fallback_strategy=DegradationStrategy.USE_CACHED_VALUES
            )
            
            if result is None:
                raise VaultError(f"Failed to retrieve secret '{path}' from all sources")
            
            return result
            
        except Exception as e:
            self._failure_count += 1
            logger.error("Secret retrieval failed completely",
                        path=path,
                        mount_point=mount_point,
                        error=str(e))
            raise
    
    @circuit_breaker_protected("secret_read")
    @retry_on_failure("secret_read")
    def _fetch_secret_from_vault(self, path: str, mount_point: str = "kv") -> Dict[str, Any]:
        """Internal method to fetch secret directly from Vault."""
        cache_key = f"{mount_point}/{path}"
        start_time = time.time()
        operation_id = f"secret_read_{int(start_time)}"
        
        # Start metrics tracking
        span = self._metrics_collector.start_operation(
            operation_id=operation_id,
            operation_type="secret_read",
            path=path,
            mount_point=mount_point
        )
        
        try:
            with self._lock:
                # Check cache first
                if cache_key in self._secret_cache:
                    metadata = self._secret_cache[cache_key]
                    if not metadata.is_expired:
                        self._cache_hits += 1
                        duration = time.time() - start_time
                        
                        # Record cache hit metrics
                        self._metrics_collector.record_secret_operation(
                            operation="read_cached",
                            mount_point=mount_point,
                            status=OperationStatus.SUCCESS,
                            duration=duration
                        )
                        
                        self._metrics_collector.end_operation(
                            operation_id=operation_id,
                            span=span,
                            status=OperationStatus.SUCCESS,
                            duration=duration,
                            cache_hit=True
                        )
                        
                        logger.debug("Retrieved secret from internal cache", 
                                   path=path, duration=duration)
                        return metadata.secret_data
                    else:
                        logger.debug("Cached secret expired, fetching fresh", path=path)
                        del self._secret_cache[cache_key]
                
                self._cache_misses += 1
                
                # Fetch from Vault
                self._ensure_authenticated()
                
                response = self._client.secrets.kv.v2.read_secret_version(
                    path=path,
                    mount_point=mount_point
                )
                
                secret_data = response['data']['data']
                metadata_dict = response['data']['metadata']
                
                # Cache the secret
                ttl = metadata_dict.get('ttl', 3600)  # Default 1 hour
                metadata = SecretMetadata(
                    secret_data=secret_data,
                    retrieved_at=datetime.now(),
                    ttl_seconds=ttl,
                    lease_id=response.get('lease_id'),
                    renewable=response.get('renewable', False)
                )
                
                self._secret_cache[cache_key] = metadata
                
                # Record successful metrics
                duration = time.time() - start_time
                self._metrics_collector.record_secret_operation(
                    operation="read_vault",
                    mount_point=mount_point,
                    status=OperationStatus.SUCCESS,
                    duration=duration
                )
                
                # Update cache metrics
                hit_ratio = self._cache_hits / max(self._cache_hits + self._cache_misses, 1)
                self._metrics_collector.update_cache_metrics(
                    cache_type="secrets",
                    cache_size=len(self._secret_cache),
                    hit_ratio=hit_ratio
                )
                
                self._metrics_collector.end_operation(
                    operation_id=operation_id,
                    span=span,
                    status=OperationStatus.SUCCESS,
                    duration=duration,
                    cache_hit=False
                )
                
                logger.info("Retrieved secret from Vault",
                           path=path,
                           mount_point=mount_point,
                           ttl=ttl,
                           duration=duration)
                
                return secret_data
                
        except Exception as e:
            duration = time.time() - start_time
            self._metrics_collector.record_secret_operation(
                operation="read_vault",
                mount_point=mount_point,
                status=OperationStatus.FAILURE,
                duration=duration
            )
            
            self._metrics_collector.end_operation(
                operation_id=operation_id,
                span=span,
                status=OperationStatus.FAILURE,
                duration=duration,
                error=str(e)
            )
            raise

    def get_certificate(self, common_name: str, 
                       alt_names: Optional[List[str]] = None,
                       ttl: str = "8760h",  # 1 year
                       mount_point: str = "pki") -> Dict[str, str]:
        """
        Generate or retrieve certificate from Vault PKI engine with resilience.
        
        Args:
            common_name: Certificate common name
            alt_names: Alternative names for the certificate
            ttl: Certificate TTL
            mount_point: PKI engine mount point
            
        Returns:
            Dictionary with certificate, private_key, ca_cert, and serial_number
        """
        self._operation_count += 1
        
        # Use degradation manager for resilient certificate generation
        def vault_cert_operation(cert_name: str, **kwargs) -> Dict[str, str]:
            return self._generate_certificate_from_vault(cert_name, alt_names, ttl, mount_point)
        
        try:
            result = self._degradation_manager.get_certificate_with_degradation(
                common_name=common_name,
                vault_func=vault_cert_operation,
                fallback_strategy=DegradationStrategy.FALLBACK_TO_FILESYSTEM,
                alt_names=alt_names,
                ttl=ttl
            )
            
            if result is None:
                raise VaultError(f"Failed to generate certificate '{common_name}' from all sources")
            
            return result
            
        except Exception as e:
            self._failure_count += 1
            logger.error("Certificate generation failed completely",
                        common_name=common_name,
                        error=str(e))
            raise
    
    @circuit_breaker_protected("pki_generate")
    @retry_on_failure("pki_generate")
    def _generate_certificate_from_vault(self, 
                                       common_name: str, 
                                       alt_names: Optional[List[str]] = None,
                                       ttl: str = "8760h",
                                       mount_point: str = "pki") -> Dict[str, str]:
        """Internal method to generate certificate directly from Vault."""
        start_time = time.time()
        operation_id = f"cert_generate_{int(start_time)}"
        
        # Start metrics tracking
        span = self._metrics_collector.start_operation(
            operation_id=operation_id,
            operation_type="certificate_generate",
            common_name=common_name,
            ttl=ttl,
            mount_point=mount_point
        )
        
        try:
            self._ensure_authenticated()
            
            params = {
                'common_name': common_name,
                'ttl': ttl
            }
            
            if alt_names:
                params['alt_names'] = ','.join(alt_names)
            
            response = self._client.secrets.pki.generate_certificate(
                name='scribe-role',  # Role should be configured in Vault
                mount_point=mount_point,
                extra_params=params
            )
            
            cert_data = {
                'certificate': response['data']['certificate'],
                'private_key': response['data']['private_key'],
                'ca_cert': response['data']['issuing_ca'],
                'serial_number': response['data']['serial_number']
            }
            
            # Calculate certificate expiry time (rough estimate from TTL)
            duration = time.time() - start_time
            ttl_hours = int(ttl.rstrip('h')) if ttl.endswith('h') else 8760
            expiry_seconds = ttl_hours * 3600
            
            # Record certificate generation metrics
            self._metrics_collector.record_certificate_operation(
                operation="generate",
                common_name=common_name,
                status=OperationStatus.SUCCESS,
                duration=duration,
                serial_number=cert_data['serial_number'],
                expiry_seconds=expiry_seconds
            )
            
            self._metrics_collector.end_operation(
                operation_id=operation_id,
                span=span,
                status=OperationStatus.SUCCESS,
                duration=duration,
                serial_number=cert_data['serial_number']
            )
            
            logger.info("Generated certificate from Vault PKI",
                       common_name=common_name,
                       serial_number=cert_data['serial_number'],
                       ttl=ttl,
                       duration=duration)
            
            return cert_data
            
        except Exception as e:
            duration = time.time() - start_time
            self._metrics_collector.record_certificate_operation(
                operation="generate",
                common_name=common_name,
                status=OperationStatus.FAILURE,
                duration=duration
            )
            
            self._metrics_collector.end_operation(
                operation_id=operation_id,
                span=span,
                status=OperationStatus.FAILURE,
                duration=duration,
                error=str(e)
            )
            raise

    @circuit_breaker_protected("secret_write")
    @retry_on_failure("secret_write")
    def write_secret(self, path: str, secret_data: Dict[str, Any], 
                    mount_point: str = "kv") -> None:
        """
        Write secret to Vault with resilience patterns.
        
        Args:
            path: Secret path
            secret_data: Secret data to write
            mount_point: Secret engine mount point
        """
        self._operation_count += 1
        
        try:
            self._ensure_authenticated()
            
            self._client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret_data,
                mount_point=mount_point
            )
            
            # Invalidate cache
            cache_key = f"{mount_point}/{path}"
            with self._lock:
                if cache_key in self._secret_cache:
                    del self._secret_cache[cache_key]
            
            self._degradation_manager.handle_vault_success(f"write_secret:{path}")
            
            logger.info("Wrote secret to Vault",
                       path=path,
                       mount_point=mount_point)
                       
        except Exception as e:
            self._failure_count += 1
            self._degradation_manager.handle_vault_failure(e, f"write_secret:{path}")
            
            logger.error("Failed to write secret",
                        path=path,
                        error=str(e))
            raise

    def create_temporary_cert_files(self, cert_data: Dict[str, str]) -> Tuple[str, str, str]:
        """
        Create temporary files for certificate data.
        
        Args:
            cert_data: Certificate data from Vault
            
        Returns:
            Tuple of (cert_file_path, key_file_path, ca_file_path)
        """
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix="scribe_vault_certs_")
            
            cert_file = os.path.join(temp_dir, "cert.pem")
            key_file = os.path.join(temp_dir, "key.pem")
            ca_file = os.path.join(temp_dir, "ca.pem")
            
            # Write certificate files
            with open(cert_file, 'w') as f:
                f.write(cert_data['certificate'])
            
            with open(key_file, 'w') as f:
                f.write(cert_data['private_key'])
                
            with open(ca_file, 'w') as f:
                f.write(cert_data['ca_cert'])
            
            # Secure permissions
            os.chmod(cert_file, 0o600)
            os.chmod(key_file, 0o600)
            os.chmod(ca_file, 0o600)
            
            logger.debug("Created temporary certificate files",
                        temp_dir=temp_dir)
            
            return cert_file, key_file, ca_file
            
        except Exception as e:
            logger.error("Failed to create temporary certificate files",
                        error=str(e))
            raise

    @circuit_breaker_protected("health")
    @retry_on_failure("health")
    def health_check(self) -> Dict[str, Any]:
        """
        Check Vault health and connectivity with resilience patterns.
        
        Returns:
            Health status information
        """
        self._operation_count += 1
        start_time = time.time()
        operation_id = f"health_check_{int(start_time)}"
        
        # Start metrics tracking
        span = self._metrics_collector.start_operation(
            operation_id=operation_id,
            operation_type="health_check",
            vault_url=self.config.url
        )
        
        try:
            if not self._client:
                self._client = self._create_client()
            
            health_response = self._client.sys.read_health_status()
            
            # Get comprehensive metrics
            circuit_breaker_metrics = self._circuit_breaker_manager.get_all_metrics()
            retry_metrics = self._retry_manager.get_all_metrics()
            degradation_metrics = self._degradation_manager.get_metrics()
            vault_metrics_summary = self._metrics_collector.get_metrics_summary()
            
            # Calculate response time and connectivity
            duration = time.time() - start_time
            is_healthy = not health_response.get('sealed', True)
            
            # Update connectivity metrics
            self._metrics_collector.update_vault_connectivity(
                vault_url=self.config.url,
                is_connected=True,
                response_time=duration
            )
            
            # Update service mode metrics
            current_mode = degradation_metrics.get('current_mode', 'normal')
            self._metrics_collector.update_service_mode(current_mode)
            
            # Calculate cache hit ratio
            hit_ratio = self._cache_hits / max(self._cache_hits + self._cache_misses, 1)
            self._metrics_collector.update_cache_metrics(
                cache_type="secrets",
                cache_size=len(self._secret_cache),
                hit_ratio=hit_ratio
            )
            
            status = {
                'vault_url': self.config.url,
                'authenticated': self._authenticated,
                'cluster_name': health_response.get('cluster_name', 'unknown'),
                'version': health_response.get('version', 'unknown'),
                'sealed': health_response.get('sealed', True),
                'standby': health_response.get('standby', True),
                'cached_secrets': len(self._secret_cache),
                'cache_hit_ratio': hit_ratio,
                'response_time_seconds': duration,
                
                # Resilience metrics
                'service_mode': current_mode,
                'operation_count': self._operation_count,
                'failure_count': self._failure_count,
                'degraded_operations': self._degraded_operations,
                'failure_rate': self._failure_count / max(self._operation_count, 1),
                
                # Circuit breaker health
                'circuit_breakers': circuit_breaker_metrics,
                
                # Retry statistics
                'retry_handlers': retry_metrics,
                
                # Degradation status
                'degradation_manager': degradation_metrics,
                
                # Vault metrics summary
                'vault_metrics': vault_metrics_summary
            }
            
            self._degradation_manager.handle_vault_success("health_check")
            
            self._metrics_collector.end_operation(
                operation_id=operation_id,
                span=span,
                status=OperationStatus.SUCCESS,
                duration=duration,
                is_healthy=is_healthy
            )
            
            logger.debug("Vault health check completed with comprehensive metrics",
                        duration=duration,
                        is_healthy=is_healthy)
            return status
            
        except Exception as e:
            self._failure_count += 1
            self._degradation_manager.handle_vault_failure(e, "health_check")
            
            duration = time.time() - start_time
            
            # Update connectivity metrics for failure
            self._metrics_collector.update_vault_connectivity(
                vault_url=self.config.url,
                is_connected=False,
                response_time=duration
            )
            
            self._metrics_collector.end_operation(
                operation_id=operation_id,
                span=span,
                status=OperationStatus.FAILURE,
                duration=duration,
                error=str(e)
            )
            
            logger.error("Vault health check failed", 
                        error=str(e), 
                        duration=duration)
            
            # Return basic status even if health check fails
            return {
                'vault_url': self.config.url,
                'authenticated': False,
                'error': str(e),
                'cached_secrets': len(self._secret_cache),
                'service_mode': self._degradation_manager.get_current_mode().value,
                'operation_count': self._operation_count,
                'failure_count': self._failure_count,
                'response_time_seconds': duration,
                'status': 'unhealthy'
            }

    def cleanup_cache(self) -> None:
        """Remove expired secrets from cache."""
        with self._lock:
            expired_keys = [
                key for key, metadata in self._secret_cache.items()
                if metadata.is_expired
            ]
            
            for key in expired_keys:
                del self._secret_cache[key]
                
            if expired_keys:
                logger.debug("Cleaned up expired secrets from cache",
                           expired_count=len(expired_keys))

    def close(self) -> None:
        """Clean up resources and close connections."""
        with self._lock:
            self._secret_cache.clear()
            
        self._authenticated = False
        self._client = None
        
        logger.info("Vault secret provider closed")


# Global provider instance
_vault_provider: Optional[VaultSecretProvider] = None
_provider_lock = threading.RLock()


def get_vault_provider() -> Optional[VaultSecretProvider]:
    """Get the global Vault provider instance."""
    with _provider_lock:
        return _vault_provider


def initialize_vault_provider(config: VaultConfig) -> VaultSecretProvider:
    """
    Initialize the global Vault provider.
    
    Args:
        config: Vault configuration
        
    Returns:
        Initialized Vault provider
    """
    global _vault_provider
    
    with _provider_lock:
        if _vault_provider:
            _vault_provider.close()
            
        _vault_provider = VaultSecretProvider(config)
        logger.info("Global Vault provider initialized")
        return _vault_provider


def configure_vault_from_environment() -> Optional[VaultConfig]:
    """
    Create Vault configuration from environment variables.
    
    Environment variables:
        VAULT_ADDR: Vault server URL
        VAULT_AUTH_METHOD: Authentication method (approle, token)
        VAULT_ROLE_ID: AppRole role ID
        VAULT_SECRET_ID: AppRole secret ID
        VAULT_TOKEN: Vault token
        VAULT_NAMESPACE: Vault namespace
        VAULT_CACERT: Path to CA certificate
        VAULT_CLIENT_CERT: Path to client certificate
        VAULT_CLIENT_KEY: Path to client key
        VAULT_SKIP_VERIFY: Skip SSL verification
        
    Returns:
        Vault configuration or None if required variables missing
    """
    vault_addr = os.getenv('VAULT_ADDR')
    if not vault_addr:
        logger.warning("VAULT_ADDR environment variable not set")
        return None
    
    auth_method_str = os.getenv('VAULT_AUTH_METHOD', 'approle').lower()
    try:
        auth_method = AuthMethod(auth_method_str)
    except ValueError:
        logger.error("Invalid VAULT_AUTH_METHOD", method=auth_method_str)
        return None
    
    config = VaultConfig(
        url=vault_addr,
        auth_method=auth_method,
        namespace=os.getenv('VAULT_NAMESPACE'),
        ca_cert_path=os.getenv('VAULT_CACERT'),
        client_cert_path=os.getenv('VAULT_CLIENT_CERT'),
        client_key_path=os.getenv('VAULT_CLIENT_KEY'),
        verify_ssl=os.getenv('VAULT_SKIP_VERIFY', 'false').lower() != 'true'
    )
    
    logger.info("Created Vault configuration from environment",
                vault_addr=vault_addr,
                auth_method=auth_method.value)
    
    return config