#!/usr/bin/env python3
"""
Scribe Vault Graceful Degradation

Implements professional graceful degradation strategies for Vault operations
to maintain service availability when Vault is unavailable or degraded.
"""

import os
import time
import threading
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
import structlog
import json

from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class DegradationStrategy(Enum):
    """Available degradation strategies."""
    FALLBACK_TO_FILESYSTEM = "fallback_to_filesystem"
    USE_CACHED_VALUES = "use_cached_values"
    GENERATE_TEMPORARY_CERTS = "generate_temporary_certs"
    FAIL_SAFE_MODE = "fail_safe_mode"
    READ_ONLY_MODE = "read_only_mode"


class ServiceMode(Enum):
    """Current service operation mode."""
    NORMAL = "normal"                    # Full functionality with Vault
    DEGRADED = "degraded"               # Limited functionality without Vault
    READ_ONLY = "read_only"             # Read operations only
    EMERGENCY = "emergency"             # Minimal functionality for critical operations
    MAINTENANCE = "maintenance"         # Planned maintenance mode


@dataclass
class DegradationConfig:
    """Configuration for graceful degradation behavior."""
    # Cache settings
    enable_secret_cache: bool = True
    cache_ttl_seconds: int = 3600        # 1 hour default
    max_cache_size: int = 1000
    
    # Fallback settings
    filesystem_fallback_paths: list = None
    emergency_certificate_ttl: int = 86400  # 24 hours
    
    # Service mode transitions
    vault_failure_threshold: int = 3     # Failures before degrading
    recovery_check_interval: int = 60    # Seconds between recovery checks
    
    # Security settings
    allow_insecure_fallback: bool = False
    log_all_degradation_events: bool = True


class VaultDegradationManager:
    """
    Manages graceful degradation when Vault is unavailable.
    
    Implements multiple fallback strategies to maintain service availability
    while ensuring security and compliance requirements are met.
    """
    
    def __init__(self, config: DegradationConfig):
        """
        Initialize degradation manager.
        
        Args:
            config: Degradation configuration
        """
        self.config = config
        self._current_mode = ServiceMode.NORMAL
        self._vault_failures = 0
        self._last_vault_success = time.time()
        self._last_recovery_check = 0.0
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Secret cache for degraded mode
        self._secret_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_timestamps: Dict[str, float] = {}
        
        # Filesystem fallback paths
        self._fallback_paths = config.filesystem_fallback_paths or [
            "tools/scribe/deployment/certificates",
            "tools/scribe/deployment/secrets",
            "deployment/certificates",
            "certificates",
            "secrets"
        ]
        
        # Metrics
        self._degradation_events = 0
        self._fallback_operations = 0
        self._cache_hits = 0
        self._cache_misses = 0
        
        logger.info("Vault degradation manager initialized",
                   cache_enabled=config.enable_secret_cache,
                   cache_ttl=config.cache_ttl_seconds,
                   fallback_paths=len(self._fallback_paths))
    
    def handle_vault_failure(self, error: Exception, operation: str) -> None:
        """
        Handle Vault operation failure and potentially trigger degradation.
        
        Args:
            error: The exception that occurred
            operation: The operation that failed
        """
        with self._lock:
            self._vault_failures += 1
            
            logger.warning("Vault operation failed",
                         operation=operation,
                         error=str(error),
                         failure_count=self._vault_failures,
                         current_mode=self._current_mode.value)
            
            # Check if we should degrade service
            if (self._current_mode == ServiceMode.NORMAL and 
                self._vault_failures >= self.config.vault_failure_threshold):
                
                self._transition_to_degraded_mode()
    
    def handle_vault_success(self, operation: str) -> None:
        """
        Handle successful Vault operation and potentially recover.
        
        Args:
            operation: The operation that succeeded
        """
        with self._lock:
            self._last_vault_success = time.time()
            
            # Reset failure count on success
            if self._vault_failures > 0:
                logger.info("Vault operation succeeded, resetting failure count",
                           operation=operation,
                           previous_failures=self._vault_failures)
                self._vault_failures = 0
            
            # Check if we should recover from degraded mode
            if self._current_mode != ServiceMode.NORMAL:
                self._attempt_recovery()
    
    def get_secret_with_degradation(self, 
                                  path: str, 
                                  vault_func: Callable,
                                  fallback_strategy: DegradationStrategy = DegradationStrategy.USE_CACHED_VALUES,
                                  **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get secret with graceful degradation support.
        
        Args:
            path: Secret path
            vault_func: Function to call for Vault operation
            fallback_strategy: Strategy to use if Vault fails
            **kwargs: Additional arguments for vault_func
            
        Returns:
            Secret data or None if all strategies fail
        """
        cache_key = f"secret:{path}"
        
        # Try Vault first if in normal mode
        if self._current_mode == ServiceMode.NORMAL:
            try:
                result = vault_func(path, **kwargs)
                if result:
                    # Cache successful result
                    self._cache_secret(cache_key, result)
                    self.handle_vault_success(f"get_secret:{path}")
                    return result
            except Exception as e:
                self.handle_vault_failure(e, f"get_secret:{path}")
                # Continue to degradation strategies
        
        # Apply degradation strategy
        return self._apply_degradation_strategy(
            cache_key, 
            fallback_strategy, 
            path,
            operation_type="secret_read"
        )
    
    def get_certificate_with_degradation(self,
                                       common_name: str,
                                       vault_func: Callable,
                                       fallback_strategy: DegradationStrategy = DegradationStrategy.FALLBACK_TO_FILESYSTEM,
                                       **kwargs) -> Optional[Dict[str, str]]:
        """
        Get certificate with graceful degradation support.
        
        Args:
            common_name: Certificate common name
            vault_func: Function to call for Vault PKI operation
            fallback_strategy: Strategy to use if Vault fails
            **kwargs: Additional arguments for vault_func
            
        Returns:
            Certificate data or None if all strategies fail
        """
        cache_key = f"certificate:{common_name}"
        
        # Try Vault first if in normal mode
        if self._current_mode == ServiceMode.NORMAL:
            try:
                result = vault_func(common_name, **kwargs)
                if result:
                    # Cache successful result (with shorter TTL for certificates)
                    self._cache_secret(cache_key, result, ttl_override=1800)  # 30 minutes
                    self.handle_vault_success(f"get_certificate:{common_name}")
                    return result
            except Exception as e:
                self.handle_vault_failure(e, f"get_certificate:{common_name}")
                # Continue to degradation strategies
        
        # Apply degradation strategy
        return self._apply_degradation_strategy(
            cache_key,
            fallback_strategy,
            common_name,
            operation_type="certificate_generate"
        )
    
    def _apply_degradation_strategy(self, 
                                  cache_key: str,
                                  strategy: DegradationStrategy,
                                  identifier: str,
                                  operation_type: str) -> Optional[Dict[str, Any]]:
        """Apply the specified degradation strategy."""
        with self._lock:
            self._fallback_operations += 1
            
            logger.info("Applying degradation strategy",
                       strategy=strategy.value,
                       identifier=identifier,
                       operation_type=operation_type,
                       current_mode=self._current_mode.value)
            
            if strategy == DegradationStrategy.USE_CACHED_VALUES:
                return self._get_cached_secret(cache_key)
            
            elif strategy == DegradationStrategy.FALLBACK_TO_FILESYSTEM:
                return self._fallback_to_filesystem(identifier, operation_type)
            
            elif strategy == DegradationStrategy.GENERATE_TEMPORARY_CERTS:
                return self._generate_temporary_certificate(identifier)
            
            elif strategy == DegradationStrategy.FAIL_SAFE_MODE:
                return self._fail_safe_operation(identifier, operation_type)
            
            else:
                logger.warning("Unknown degradation strategy",
                             strategy=strategy.value)
                return None
    
    def _cache_secret(self, key: str, data: Dict[str, Any], ttl_override: Optional[int] = None):
        """Cache secret data with TTL."""
        if not self.config.enable_secret_cache:
            return
        
        with self._lock:
            # Check cache size limit
            if len(self._secret_cache) >= self.config.max_cache_size:
                self._evict_oldest_cache_entry()
            
            ttl = ttl_override or self.config.cache_ttl_seconds
            self._secret_cache[key] = data
            self._cache_timestamps[key] = time.time() + ttl
            
            logger.debug("Secret cached",
                        key=key,
                        ttl=ttl,
                        cache_size=len(self._secret_cache))
    
    def _get_cached_secret(self, key: str) -> Optional[Dict[str, Any]]:
        """Get secret from cache if available and not expired."""
        if not self.config.enable_secret_cache:
            self._cache_misses += 1
            return None
        
        with self._lock:
            if key not in self._secret_cache:
                self._cache_misses += 1
                return None
            
            # Check if cached value has expired
            if time.time() > self._cache_timestamps.get(key, 0):
                logger.debug("Cached secret expired", key=key)
                del self._secret_cache[key]
                del self._cache_timestamps[key]
                self._cache_misses += 1
                return None
            
            self._cache_hits += 1
            logger.debug("Secret retrieved from cache", key=key)
            return self._secret_cache[key].copy()
    
    def _fallback_to_filesystem(self, identifier: str, operation_type: str) -> Optional[Dict[str, Any]]:
        """Attempt to read secrets/certificates from filesystem."""
        for fallback_path in self._fallback_paths:
            path = Path(fallback_path)
            if not path.exists():
                continue
            
            try:
                if operation_type == "certificate_generate":
                    # Look for certificate files
                    cert_file = path / "server.crt"
                    key_file = path / "server.key"
                    ca_file = path / "ca.crt"
                    
                    if all(f.exists() for f in [cert_file, key_file, ca_file]):
                        logger.info("Using filesystem certificates as fallback",
                                   path=str(path))
                        
                        return {
                            'certificate': cert_file.read_text(encoding='utf-8'),
                            'private_key': key_file.read_text(encoding='utf-8'),
                            'ca_cert': ca_file.read_text(encoding='utf-8'),
                            'serial_number': f"filesystem-{int(time.time())}"
                        }
                
                elif operation_type == "secret_read":
                    # Look for secret files
                    secret_file = path / f"{identifier}.json"
                    if secret_file.exists():
                        logger.info("Using filesystem secret as fallback",
                                   file=str(secret_file))
                        
                        with open(secret_file, 'r', encoding='utf-8') as f:
                            return json.load(f)
                
            except Exception as e:
                logger.warning("Failed to read from filesystem fallback",
                             path=str(path),
                             error=str(e))
                continue
        
        logger.warning("No filesystem fallback found",
                      identifier=identifier,
                      operation_type=operation_type,
                      searched_paths=self._fallback_paths)
        return None
    
    def _generate_temporary_certificate(self, common_name: str) -> Optional[Dict[str, str]]:
        """Generate temporary self-signed certificate for emergency use."""
        if not self.config.allow_insecure_fallback:
            logger.warning("Temporary certificate generation disabled by policy")
            return None
        
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            import datetime
            
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            # Create self-signed certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Scribe Emergency CA"),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(seconds=self.config.emergency_certificate_ttl)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName(common_name),
                    x509.DNSName("localhost"),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256())
            
            # Serialize certificate and key
            cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
            key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            
            logger.warning("Generated temporary self-signed certificate",
                          common_name=common_name,
                          ttl=self.config.emergency_certificate_ttl,
                          serial=cert.serial_number)
            
            return {
                'certificate': cert_pem,
                'private_key': key_pem,
                'ca_cert': cert_pem,  # Self-signed, so cert is also CA
                'serial_number': str(cert.serial_number)
            }
            
        except ImportError:
            logger.error("cryptography library not available for temporary certificate generation")
            return None
        except Exception as e:
            logger.error("Failed to generate temporary certificate",
                        error=str(e))
            return None
    
    def _fail_safe_operation(self, identifier: str, operation_type: str) -> Optional[Dict[str, Any]]:
        """Perform fail-safe operation with minimal functionality."""
        logger.warning("Performing fail-safe operation",
                      identifier=identifier,
                      operation_type=operation_type)
        
        # Return minimal safe values
        if operation_type == "secret_read":
            return {
                'value': '',
                'metadata': {
                    'source': 'fail_safe',
                    'timestamp': time.time(),
                    'warning': 'Using fail-safe mode - secret not available'
                }
            }
        
        return None
    
    def _transition_to_degraded_mode(self):
        """Transition service to degraded mode."""
        previous_mode = self._current_mode
        self._current_mode = ServiceMode.DEGRADED
        self._degradation_events += 1
        
        logger.error("Service transitioning to DEGRADED mode",
                    previous_mode=previous_mode.value,
                    vault_failures=self._vault_failures,
                    degradation_events=self._degradation_events)
        
        if self.config.log_all_degradation_events:
            # Log detailed degradation event for monitoring
            logger.error("DEGRADATION_EVENT",
                        event_type="service_degraded",
                        timestamp=time.time(),
                        failure_count=self._vault_failures,
                        previous_mode=previous_mode.value,
                        current_mode=self._current_mode.value)
    
    def _attempt_recovery(self):
        """Attempt to recover from degraded mode."""
        current_time = time.time()
        
        # Check if enough time has passed since last recovery check
        if current_time - self._last_recovery_check < self.config.recovery_check_interval:
            return
        
        self._last_recovery_check = current_time
        
        if self._current_mode != ServiceMode.NORMAL:
            logger.info("Attempting recovery to normal mode",
                       current_mode=self._current_mode.value,
                       last_success=time.time() - self._last_vault_success)
            
            # Transition back to normal mode
            previous_mode = self._current_mode
            self._current_mode = ServiceMode.NORMAL
            self._vault_failures = 0
            
            logger.info("Service recovered to NORMAL mode",
                       previous_mode=previous_mode.value,
                       recovery_time=current_time - self._last_vault_success)
    
    def _evict_oldest_cache_entry(self):
        """Evict the oldest cache entry when cache is full."""
        if not self._cache_timestamps:
            return
        
        oldest_key = min(self._cache_timestamps.keys(), 
                        key=lambda k: self._cache_timestamps[k])
        
        del self._secret_cache[oldest_key]
        del self._cache_timestamps[oldest_key]
        
        logger.debug("Evicted oldest cache entry", key=oldest_key)
    
    def get_current_mode(self) -> ServiceMode:
        """Get current service mode."""
        with self._lock:
            return self._current_mode
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get degradation manager metrics."""
        with self._lock:
            return {
                'current_mode': self._current_mode.value,
                'vault_failures': self._vault_failures,
                'degradation_events': self._degradation_events,
                'fallback_operations': self._fallback_operations,
                'cache_hits': self._cache_hits,
                'cache_misses': self._cache_misses,
                'cache_hit_rate': self._cache_hits / max(self._cache_hits + self._cache_misses, 1),
                'cached_secrets': len(self._secret_cache),
                'last_vault_success': self._last_vault_success,
                'last_recovery_check': self._last_recovery_check
            }
    
    def force_mode(self, mode: ServiceMode):
        """Force service to specific mode (for testing/maintenance)."""
        with self._lock:
            previous_mode = self._current_mode
            self._current_mode = mode
            
            logger.warning("Service mode manually changed",
                          previous_mode=previous_mode.value,
                          new_mode=mode.value)
    
    def clear_cache(self):
        """Clear all cached secrets."""
        with self._lock:
            cache_size = len(self._secret_cache)
            self._secret_cache.clear()
            self._cache_timestamps.clear()
            
            logger.info("Secret cache cleared", 
                       cleared_entries=cache_size)


# Global degradation manager instance
_degradation_manager: Optional[VaultDegradationManager] = None
_manager_lock = threading.RLock()


def get_vault_degradation_manager(config: Optional[DegradationConfig] = None) -> VaultDegradationManager:
    """Get or create global degradation manager."""
    global _degradation_manager
    
    with _manager_lock:
        if _degradation_manager is None:
            _degradation_manager = VaultDegradationManager(
                config or DegradationConfig()
            )
        
        return _degradation_manager