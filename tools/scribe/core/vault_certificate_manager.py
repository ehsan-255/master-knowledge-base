#!/usr/bin/env python3
"""
Scribe Vault Certificate Manager

Integrates HashiCorp Vault PKI secrets engine with the existing mTLS infrastructure
to provide dynamic certificate management and automatic rotation.
"""

import os
import tempfile
import threading
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
import structlog

from .logging_config import get_scribe_logger
from .vault_secret_provider import get_vault_provider
from .mtls import MTLSConfig

logger = get_scribe_logger(__name__)


class VaultCertificateManager:
    """
    Manages certificates from Vault PKI engine for mTLS operations.
    
    Provides seamless integration between Vault-generated certificates
    and the existing mTLS infrastructure.
    """
    
    def __init__(self, config_manager):
        """
        Initialize Vault certificate manager.
        
        Args:
            config_manager: ConfigManager instance with Vault integration
        """
        self.config_manager = config_manager
        self._certificates_cache: Dict[str, Dict[str, Any]] = {}
        self._temp_files_cache: Dict[str, Tuple[str, str, str]] = {}
        self._cache_lock = threading.RLock()
        
        logger.info("VaultCertificateManager initialized")
    
    def get_mtls_config(self, 
                       common_name: str = "scribe.local", 
                       alt_names: Optional[list] = None,
                       ttl: str = "8760h") -> Optional[MTLSConfig]:
        """
        Generate or retrieve mTLS configuration using Vault certificates.
        
        Args:
            common_name: Certificate common name
            alt_names: Alternative names for the certificate
            ttl: Certificate time-to-live
            
        Returns:
            MTLSConfig instance or None if Vault not available
        """
        cache_key = f"{common_name}_{ttl}"
        
        with self._cache_lock:
            # Check if we have cached certificate files that are still valid
            if cache_key in self._temp_files_cache:
                cert_file, key_file, ca_file = self._temp_files_cache[cache_key]
                
                # Verify files still exist
                if all(Path(f).exists() for f in [cert_file, key_file, ca_file]):
                    try:
                        return MTLSConfig(cert_file, key_file, ca_file)
                    except Exception as e:
                        logger.warning("Cached certificate files invalid, regenerating",
                                     error=str(e))
                        # Remove invalid cache entry
                        del self._temp_files_cache[cache_key]
            
            # Try to get certificates from Vault
            try:
                cert_data = self._get_certificate_from_vault(common_name, alt_names, ttl)
                if not cert_data:
                    return self._fallback_to_filesystem()
                
                # Create temporary certificate files
                cert_file, key_file, ca_file = self._create_temp_certificate_files(cert_data)
                
                # Cache the file paths
                self._temp_files_cache[cache_key] = (cert_file, key_file, ca_file)
                
                logger.info("Created mTLS configuration from Vault certificates",
                           common_name=common_name,
                           cert_file=cert_file)
                
                return MTLSConfig(cert_file, key_file, ca_file)
                
            except Exception as e:
                logger.error("Failed to create mTLS config from Vault",
                           common_name=common_name,
                           error=str(e))
                return self._fallback_to_filesystem()
    
    def _get_certificate_from_vault(self, 
                                  common_name: str, 
                                  alt_names: Optional[list] = None,
                                  ttl: str = "8760h") -> Optional[Dict[str, str]]:
        """Get certificate from Vault PKI engine."""
        if not self.config_manager.is_vault_enabled():
            logger.debug("Vault not enabled, cannot retrieve certificates")
            return None
        
        try:
            # First try to get certificate from ConfigManager (which uses VaultSecretProvider)
            cert_data = self.config_manager.get_certificate(common_name, alt_names, ttl)
            
            if cert_data:
                # Validate certificate data structure
                required_keys = ['certificate', 'private_key', 'ca_cert']
                if all(key in cert_data for key in required_keys):
                    return cert_data
                else:
                    logger.warning("Incomplete certificate data from Vault",
                                 missing_keys=[k for k in required_keys if k not in cert_data])
            
            # Fallback: try to get stored certificates from KV store
            stored_certs = self.config_manager.get_secret("certificates/mtls")
            if stored_certs:
                logger.info("Using stored certificates from Vault KV store")
                return {
                    'certificate': stored_certs.get('server_cert', ''),
                    'private_key': stored_certs.get('server_key', ''),
                    'ca_cert': stored_certs.get('ca_cert', '')
                }
            
            return None
            
        except Exception as e:
            logger.error("Error retrieving certificate from Vault",
                        common_name=common_name,
                        error=str(e))
            return None
    
    def _create_temp_certificate_files(self, cert_data: Dict[str, str]) -> Tuple[str, str, str]:
        """Create temporary certificate files from Vault data."""
        try:
            # Create temporary directory with secure permissions
            temp_dir = tempfile.mkdtemp(prefix="scribe_vault_certs_")
            os.chmod(temp_dir, 0o700)
            
            cert_file = os.path.join(temp_dir, "cert.pem")
            key_file = os.path.join(temp_dir, "key.pem")
            ca_file = os.path.join(temp_dir, "ca.pem")
            
            # Write certificate files with secure permissions
            with open(cert_file, 'w', encoding='utf-8') as f:
                f.write(cert_data['certificate'])
            os.chmod(cert_file, 0o600)
            
            with open(key_file, 'w', encoding='utf-8') as f:
                f.write(cert_data['private_key'])
            os.chmod(key_file, 0o600)
                
            with open(ca_file, 'w', encoding='utf-8') as f:
                f.write(cert_data['ca_cert'])
            os.chmod(ca_file, 0o600)
            
            logger.debug("Created temporary certificate files",
                        temp_dir=temp_dir,
                        files=[cert_file, key_file, ca_file])
            
            return cert_file, key_file, ca_file
            
        except Exception as e:
            logger.error("Failed to create temporary certificate files",
                        error=str(e))
            raise
    
    def _fallback_to_filesystem(self) -> Optional[MTLSConfig]:
        """Fallback to filesystem certificates if Vault is unavailable."""
        try:
            # Try standard certificate paths
            cert_paths = [
                "tools/scribe/deployment/certificates",
                "deployment/certificates",
                "certificates"
            ]
            
            for cert_path in cert_paths:
                cert_dir = Path(cert_path)
                if cert_dir.exists():
                    cert_file = cert_dir / "server.crt"
                    key_file = cert_dir / "server.key"
                    ca_file = cert_dir / "ca.crt"
                    
                    if all(f.exists() for f in [cert_file, key_file, ca_file]):
                        logger.info("Using filesystem certificates as fallback",
                                   cert_dir=str(cert_dir))
                        return MTLSConfig(str(cert_file), str(key_file), str(ca_file))
            
            logger.warning("No filesystem certificates found for fallback")
            return None
            
        except Exception as e:
            logger.error("Failed to create fallback mTLS config",
                        error=str(e))
            return None
    
    def rotate_certificates(self, 
                          common_name: str = "scribe.local",
                          alt_names: Optional[list] = None,
                          ttl: str = "8760h") -> bool:
        """
        Force certificate rotation by clearing cache and generating new certificates.
        
        Args:
            common_name: Certificate common name
            alt_names: Alternative names
            ttl: Certificate TTL
            
        Returns:
            True if rotation successful, False otherwise
        """
        cache_key = f"{common_name}_{ttl}"
        
        with self._cache_lock:
            try:
                # Clean up old temporary files
                if cache_key in self._temp_files_cache:
                    cert_file, key_file, ca_file = self._temp_files_cache[cache_key]
                    for file_path in [cert_file, key_file, ca_file]:
                        try:
                            Path(file_path).unlink(missing_ok=True)
                        except Exception as e:
                            logger.warning("Failed to clean up temp file",
                                         file_path=file_path,
                                         error=str(e))
                    
                    # Remove from cache
                    del self._temp_files_cache[cache_key]
                
                # Generate new certificates
                new_config = self.get_mtls_config(common_name, alt_names, ttl)
                
                if new_config:
                    logger.info("Certificate rotation successful",
                               common_name=common_name)
                    return True
                else:
                    logger.error("Certificate rotation failed",
                               common_name=common_name)
                    return False
                    
            except Exception as e:
                logger.error("Error during certificate rotation",
                           common_name=common_name,
                           error=str(e))
                return False
    
    def get_certificate_info(self, common_name: str = "scribe.local") -> Dict[str, Any]:
        """
        Get information about current certificates.
        
        Args:
            common_name: Certificate common name to check
            
        Returns:
            Dictionary with certificate information
        """
        info = {
            'common_name': common_name,
            'vault_enabled': self.config_manager.is_vault_enabled(),
            'cached_certificates': len(self._temp_files_cache),
            'source': 'unknown'
        }
        
        try:
            cache_key = f"{common_name}_8760h"  # Default TTL
            
            if cache_key in self._temp_files_cache:
                cert_file, key_file, ca_file = self._temp_files_cache[cache_key]
                
                info.update({
                    'source': 'vault_cached',
                    'cert_file': cert_file,
                    'key_file': key_file,
                    'ca_file': ca_file,
                    'files_exist': all(Path(f).exists() for f in [cert_file, key_file, ca_file])
                })
            
            elif self.config_manager.is_vault_enabled():
                info['source'] = 'vault_available'
            
            else:
                # Check for filesystem certificates
                cert_paths = ["tools/scribe/deployment/certificates"]
                for cert_path in cert_paths:
                    cert_dir = Path(cert_path)
                    if cert_dir.exists():
                        cert_file = cert_dir / "server.crt"
                        key_file = cert_dir / "server.key"
                        ca_file = cert_dir / "ca.crt"
                        
                        if all(f.exists() for f in [cert_file, key_file, ca_file]):
                            info.update({
                                'source': 'filesystem',
                                'cert_file': str(cert_file),
                                'key_file': str(key_file),
                                'ca_file': str(ca_file)
                            })
                            break
                
                if info['source'] == 'unknown':
                    info['source'] = 'none_available'
            
        except Exception as e:
            info['error'] = str(e)
            logger.error("Error getting certificate info", error=str(e))
        
        return info
    
    def cleanup(self):
        """Clean up temporary certificate files."""
        with self._cache_lock:
            for cache_key, (cert_file, key_file, ca_file) in self._temp_files_cache.items():
                try:
                    # Remove temporary files
                    for file_path in [cert_file, key_file, ca_file]:
                        Path(file_path).unlink(missing_ok=True)
                    
                    # Remove temporary directory if empty
                    temp_dir = Path(cert_file).parent
                    if temp_dir.exists() and not any(temp_dir.iterdir()):
                        temp_dir.rmdir()
                        
                except Exception as e:
                    logger.warning("Failed to cleanup certificate files",
                                 cache_key=cache_key,
                                 error=str(e))
            
            self._temp_files_cache.clear()
            logger.info("Certificate cleanup completed")


# Global certificate manager instance
_cert_manager: Optional[VaultCertificateManager] = None
_cert_manager_lock = threading.RLock()


def get_vault_certificate_manager(config_manager) -> VaultCertificateManager:
    """Get or create global Vault certificate manager."""
    global _cert_manager
    
    with _cert_manager_lock:
        if _cert_manager is None:
            _cert_manager = VaultCertificateManager(config_manager)
        
        return _cert_manager


def create_vault_mtls_config(config_manager,
                           common_name: str = "scribe.local",
                           alt_names: Optional[list] = None,
                           ttl: str = "8760h") -> Optional[MTLSConfig]:
    """
    Convenience function to create mTLS configuration from Vault.
    
    Args:
        config_manager: ConfigManager instance
        common_name: Certificate common name
        alt_names: Alternative names
        ttl: Certificate TTL
        
    Returns:
        MTLSConfig instance or None
    """
    cert_manager = get_vault_certificate_manager(config_manager)
    return cert_manager.get_mtls_config(common_name, alt_names, ttl)