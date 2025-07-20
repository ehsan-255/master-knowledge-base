#!/usr/bin/env python3
"""
Scribe Engine mTLS Implementation

Implements mutual TLS authentication for secure network communications
as required by HMA v2.2 mandatory Tier 1 technologies.
"""

import ssl
import socket
import threading
import urllib3
from pathlib import Path
from typing import Optional, Dict, Any, Union
import structlog
import requests

from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class MTLSConfig:
    """Configuration for mutual TLS authentication."""
    
    def __init__(self,
                 cert_file: Union[str, Path],
                 key_file: Union[str, Path],
                 ca_file: Union[str, Path],
                 verify_mode: int = ssl.CERT_REQUIRED,
                 check_hostname: bool = True):
        """
        Initialize mTLS configuration.
        
        Args:
            cert_file: Path to client certificate file
            key_file: Path to client private key file  
            ca_file: Path to CA certificate file
            verify_mode: SSL verification mode
            check_hostname: Whether to verify hostname
        """
        self.cert_file = Path(cert_file)
        self.key_file = Path(key_file)
        self.ca_file = Path(ca_file)
        self.verify_mode = verify_mode
        self.check_hostname = check_hostname
        
        # Validate certificate files exist
        self._validate_certificate_files()
        
        logger.info("mTLS configuration initialized",
                   cert_file=str(self.cert_file),
                   ca_file=str(self.ca_file),
                   verify_mode=verify_mode,
                   check_hostname=check_hostname)
    
    def _validate_certificate_files(self):
        """Validate that all certificate files exist and are readable."""
        for file_path, file_type in [
            (self.cert_file, "client certificate"),
            (self.key_file, "client private key"), 
            (self.ca_file, "CA certificate")
        ]:
            if not file_path.exists():
                raise FileNotFoundError(f"{file_type} file not found: {file_path}")
            
            if not file_path.is_file():
                raise ValueError(f"{file_type} path is not a file: {file_path}")
            
            try:
                with open(file_path, 'r') as f:
                    f.read(1)
            except PermissionError:
                raise PermissionError(f"Cannot read {file_type} file: {file_path}")
    
    def create_ssl_context(self) -> ssl.SSLContext:
        """
        Create SSL context with mTLS configuration.
        
        Returns:
            Configured SSL context
        """
        try:
            # Create SSL context with TLS 1.2+ support
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            
            # Load CA certificate for server verification
            context.load_verify_locations(str(self.ca_file))
            
            # Load client certificate and key for client authentication
            context.load_cert_chain(str(self.cert_file), str(self.key_file))
            
            # Configure verification settings
            context.verify_mode = self.verify_mode
            context.check_hostname = self.check_hostname
            
            # Ensure strong cipher suites only
            context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA')
            
            # Disable weak protocols
            context.options |= ssl.OP_NO_SSLv2
            context.options |= ssl.OP_NO_SSLv3
            context.options |= ssl.OP_NO_TLSv1
            context.options |= ssl.OP_NO_TLSv1_1
            
            logger.debug("SSL context created successfully")
            return context
            
        except Exception as e:
            logger.error("Failed to create SSL context",
                        error=str(e),
                        cert_file=str(self.cert_file),
                        ca_file=str(self.ca_file))
            raise


class MTLSHTTPAdapter(requests.adapters.HTTPAdapter):
    """Custom HTTP adapter with mTLS support for requests library."""
    
    def __init__(self, mtls_config: MTLSConfig, *args, **kwargs):
        """
        Initialize mTLS HTTP adapter.
        
        Args:
            mtls_config: mTLS configuration
        """
        self.mtls_config = mtls_config
        super().__init__(*args, **kwargs)
        
        logger.debug("mTLS HTTP adapter initialized")
    
    def init_poolmanager(self, *args, **kwargs):
        """Initialize urllib3 pool manager with mTLS SSL context."""
        ssl_context = self.mtls_config.create_ssl_context()
        kwargs['ssl_context'] = ssl_context
        
        return super().init_poolmanager(*args, **kwargs)


class MTLSSession:
    """HTTP session with mTLS support."""
    
    def __init__(self, mtls_config: MTLSConfig):
        """
        Initialize mTLS session.
        
        Args:
            mtls_config: mTLS configuration
        """
        self.mtls_config = mtls_config
        self.session = requests.Session()
        
        # Mount mTLS adapter for HTTPS URLs
        adapter = MTLSHTTPAdapter(mtls_config)
        self.session.mount('https://', adapter)
        
        logger.debug("mTLS session initialized")
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """Make GET request with mTLS authentication."""
        return self._request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """Make POST request with mTLS authentication."""
        return self._request('POST', url, **kwargs)
    
    def put(self, url: str, **kwargs) -> requests.Response:
        """Make PUT request with mTLS authentication."""
        return self._request('PUT', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        """Make DELETE request with mTLS authentication."""
        return self._request('DELETE', url, **kwargs)
    
    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make HTTP request with mTLS authentication and error handling.
        
        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters
            
        Returns:
            HTTP response
        """
        try:
            logger.debug("Making mTLS request",
                        method=method,
                        url=url)
            
            response = self.session.request(method, url, **kwargs)
            
            logger.debug("mTLS request completed",
                        method=method,
                        url=url,
                        status_code=response.status_code)
            
            return response
            
        except ssl.SSLError as e:
            logger.error("SSL error during mTLS request",
                        method=method,
                        url=url,
                        error=str(e))
            raise
        
        except requests.exceptions.RequestException as e:
            logger.error("Request error during mTLS request",
                        method=method,
                        url=url,
                        error=str(e))
            raise
        
        except Exception as e:
            logger.error("Unexpected error during mTLS request",
                        method=method,
                        url=url,
                        error=str(e),
                        error_type=type(e).__name__)
            raise
    
    def close(self):
        """Close the session and clean up resources."""
        self.session.close()
        logger.debug("mTLS session closed")


class MTLSServer:
    """Simple mTLS server for testing and local services."""
    
    def __init__(self,
                 host: str,
                 port: int,
                 mtls_config: MTLSConfig,
                 request_handler=None):
        """
        Initialize mTLS server.
        
        Args:
            host: Server host
            port: Server port
            mtls_config: mTLS configuration
            request_handler: Custom request handler function
        """
        self.host = host
        self.port = port
        self.mtls_config = mtls_config
        self.request_handler = request_handler or self._default_handler
        
        self._server_socket = None
        self._running = False
        self._server_thread = None
        
        logger.info("mTLS server initialized",
                   host=host,
                   port=port)
    
    def _default_handler(self, client_socket: ssl.SSLSocket, address: tuple):
        """Default request handler that sends a simple HTTP response."""
        try:
            # Read request
            request = client_socket.recv(4096).decode('utf-8')
            
            # Send simple HTTP response
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "mTLS server OK"
            )
            
            client_socket.send(response.encode('utf-8'))
            
            logger.debug("Handled mTLS request",
                        client_address=address,
                        request_preview=request.split('\n')[0] if request else "")
            
        except Exception as e:
            logger.error("Error handling mTLS request",
                        client_address=address,
                        error=str(e))
        finally:
            client_socket.close()
    
    def start(self):
        """Start the mTLS server."""
        if self._running:
            return
        
        try:
            # Create SSL context
            ssl_context = self.mtls_config.create_ssl_context()
            
            # Create server socket
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._server_socket.bind((self.host, self.port))
            self._server_socket.listen(5)
            
            # Wrap with SSL
            self._server_socket = ssl_context.wrap_socket(
                self._server_socket,
                server_side=True
            )
            
            self._running = True
            
            # Start server thread
            self._server_thread = threading.Thread(
                target=self._server_loop,
                name=f"MTLSServer-{self.host}:{self.port}",
                daemon=True
            )
            self._server_thread.start()
            
            logger.info("mTLS server started",
                       host=self.host,
                       port=self.port)
            
        except Exception as e:
            logger.error("Failed to start mTLS server",
                        host=self.host,
                        port=self.port,
                        error=str(e))
            self._running = False
            raise
    
    def _server_loop(self):
        """Main server loop."""
        try:
            while self._running:
                try:
                    # Accept client connection
                    client_socket, address = self._server_socket.accept()
                    
                    logger.debug("Accepted mTLS connection",
                               client_address=address)
                    
                    # Handle request in separate thread
                    client_thread = threading.Thread(
                        target=self.request_handler,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except Exception as e:
                    if self._running:
                        logger.error("Error accepting mTLS connection",
                                    error=str(e))
                        
        except Exception as e:
            logger.error("mTLS server loop error",
                        error=str(e))
        finally:
            self._cleanup()
    
    def stop(self):
        """Stop the mTLS server."""
        if not self._running:
            return
        
        self._running = False
        
        try:
            if self._server_socket:
                self._server_socket.close()
            
            if self._server_thread and self._server_thread.is_alive():
                self._server_thread.join(timeout=5.0)
            
            logger.info("mTLS server stopped",
                       host=self.host,
                       port=self.port)
            
        except Exception as e:
            logger.error("Error stopping mTLS server",
                        error=str(e))
    
    def _cleanup(self):
        """Clean up server resources."""
        try:
            if self._server_socket:
                self._server_socket.close()
                self._server_socket = None
        except Exception:
            pass


class MTLSManager:
    """Manager for mTLS configurations and sessions."""
    
    def __init__(self):
        """Initialize mTLS manager."""
        self._configurations: Dict[str, MTLSConfig] = {}
        self._sessions: Dict[str, MTLSSession] = {}
        self._lock = threading.RLock()
        
        logger.info("mTLS manager initialized")
    
    def add_configuration(self, name: str, mtls_config: MTLSConfig):
        """
        Add a named mTLS configuration.
        
        Args:
            name: Configuration name
            mtls_config: mTLS configuration
        """
        with self._lock:
            self._configurations[name] = mtls_config
            logger.debug("Added mTLS configuration", name=name)
    
    def get_session(self, config_name: str) -> Optional[MTLSSession]:
        """
        Get or create mTLS session for configuration.
        
        Args:
            config_name: Name of the configuration
            
        Returns:
            mTLS session or None if configuration not found
        """
        with self._lock:
            if config_name not in self._configurations:
                logger.warning("mTLS configuration not found", config_name=config_name)
                return None
            
            if config_name not in self._sessions:
                config = self._configurations[config_name]
                self._sessions[config_name] = MTLSSession(config)
                logger.debug("Created new mTLS session", config_name=config_name)
            
            return self._sessions[config_name]
    
    def close_session(self, config_name: str):
        """
        Close mTLS session for configuration.
        
        Args:
            config_name: Name of the configuration
        """
        with self._lock:
            if config_name in self._sessions:
                self._sessions[config_name].close()
                del self._sessions[config_name]
                logger.debug("Closed mTLS session", config_name=config_name)
    
    def close_all_sessions(self):
        """Close all mTLS sessions."""
        with self._lock:
            for config_name in list(self._sessions.keys()):
                self.close_session(config_name)
            logger.info("Closed all mTLS sessions")
    
    def list_configurations(self) -> List[str]:
        """Get list of configuration names."""
        with self._lock:
            return list(self._configurations.keys())


# Global mTLS manager instance
_mtls_manager: Optional[MTLSManager] = None
_mtls_lock = threading.RLock()


def get_mtls_manager() -> MTLSManager:
    """Get or create global mTLS manager."""
    global _mtls_manager
    
    with _mtls_lock:
        if _mtls_manager is None:
            _mtls_manager = MTLSManager()
        
        return _mtls_manager


def create_mtls_session(cert_file: Union[str, Path],
                       key_file: Union[str, Path],
                       ca_file: Union[str, Path]) -> MTLSSession:
    """
    Create a new mTLS session with the provided certificates.
    
    Args:
        cert_file: Path to client certificate file
        key_file: Path to client private key file
        ca_file: Path to CA certificate file
        
    Returns:
        Configured mTLS session
    """
    config = MTLSConfig(cert_file, key_file, ca_file)
    return MTLSSession(config)