"""
Scribe Engine - Health Check HTTP Server

This module implements a lightweight HTTP server that exposes engine status
and metrics via a /health endpoint. It runs in a separate thread and provides
monitoring capabilities for operational visibility.
"""

import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Callable, Optional
from urllib.parse import urlparse
from core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP request handler for health check endpoints."""
    
    def __init__(self, status_provider: Callable[[], Dict[str, Any]], *args, **kwargs):
        """
        Initialize the handler with a status provider function.
        
        Args:
            status_provider: Function that returns current engine status
        """
        self.status_provider = status_provider
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/health':
            self._handle_health_check()
        elif parsed_path.path == '/':
            self._handle_root()
        else:
            self._handle_not_found()
    
    def _handle_health_check(self):
        """Handle /health endpoint requests."""
        try:
            # Get current engine status
            status = self.status_provider()
            
            # Add health-specific information
            health_status = {
                'status': 'healthy' if status.get('is_running', False) else 'unhealthy',
                'timestamp': time.time(),
                'uptime_seconds': status.get('uptime_seconds', 0),
                'queue_size': status.get('queue_size', 0),
                'engine': {
                    'is_running': status.get('is_running', False),
                    'watch_paths': status.get('watch_paths', []),
                    'file_patterns': status.get('file_patterns', [])
                },
                'worker': {
                    'events_processed': status.get('events_processed', 0),
                    'events_failed': status.get('events_failed', 0),
                    'total_events': status.get('total_events', 0),
                    'success_rate': status.get('success_rate', 0.0)
                }
            }
            
            # Send successful response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            response_json = json.dumps(health_status, indent=2)
            self.wfile.write(response_json.encode('utf-8'))
            
            logger.debug("Health check request served",
                        client_ip=self.client_address[0],
                        status=health_status['status'],
                        queue_size=health_status['queue_size'])
            
        except Exception as e:
            logger.error("Error handling health check request",
                        error=str(e),
                        client_ip=self.client_address[0],
                        exc_info=True)
            
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_response = {
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def _handle_root(self):
        """Handle root path requests."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        
        html_response = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Scribe Engine Health</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .status { padding: 20px; border-radius: 5px; margin: 20px 0; }
                .healthy { background-color: #d4edda; color: #155724; }
                .unhealthy { background-color: #f8d7da; color: #721c24; }
            </style>
        </head>
        <body>
            <h1>Scribe Engine Health Monitor</h1>
            <p>Available endpoints:</p>
            <ul>
                <li><a href="/health">/health</a> - JSON health status</li>
            </ul>
            <p>For monitoring integration, use the <code>/health</code> endpoint.</p>
        </body>
        </html>
        """
        self.wfile.write(html_response.encode('utf-8'))
    
    def _handle_not_found(self):
        """Handle 404 Not Found responses."""
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        error_response = {
            'status': 'not_found',
            'message': f"Path '{self.path}' not found",
            'available_paths': ['/health', '/'],
            'timestamp': time.time()
        }
        self.wfile.write(json.dumps(error_response, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override default logging to use our structured logger."""
        logger.info("HTTP request",
                   client_ip=self.client_address[0],
                   method=self.command,
                   path=self.path,
                   user_agent=self.headers.get('User-Agent', 'unknown'))


class HealthServer(threading.Thread):
    """
    HTTP health check server that runs in a separate thread.
    
    Provides a /health endpoint that returns JSON status information
    about the Scribe engine for monitoring and operational visibility.
    """
    
    def __init__(self, 
                 status_provider: Callable[[], Dict[str, Any]],
                 host: str = 'localhost',
                 port: int = 9468,
                 shutdown_event: Optional[threading.Event] = None):
        """
        Initialize the health server.
        
        Args:
            status_provider: Function that returns current engine status
            host: Host to bind the server to
            port: Port to bind the server to
            shutdown_event: Event to signal graceful shutdown
        """
        super().__init__(name="ScribeHealthServer", daemon=True)
        self.status_provider = status_provider
        self.host = host
        self.port = port
        self.shutdown_event = shutdown_event or threading.Event()
        
        self.server = None
        self.is_running = False
        
        logger.info("Health server initialized",
                   host=host,
                   port=port)
    
    def run(self):
        """Start the HTTP server."""
        try:
            # Create handler class with status provider
            def handler_factory(*args, **kwargs):
                return HealthCheckHandler(self.status_provider, *args, **kwargs)
            
            # Create and start server
            self.server = HTTPServer((self.host, self.port), handler_factory)
            self.server.timeout = 1.0  # 1 second timeout for shutdown checking
            self.is_running = True
            
            logger.info("Health server started",
                       host=self.host,
                       port=self.port,
                       url=f"http://{self.host}:{self.port}/health")
            
            # Server loop with shutdown checking
            while not self.shutdown_event.is_set():
                self.server.handle_request()
                
        except Exception as e:
            logger.error("Health server error",
                        error=str(e),
                        host=self.host,
                        port=self.port,
                        exc_info=True)
        finally:
            self.is_running = False
            if self.server:
                self.server.server_close()
            logger.info("Health server stopped")
    
    def stop(self):
        """Stop the health server gracefully."""
        logger.info("Stopping health server")
        self.shutdown_event.set()
        
        if self.is_alive():
            self.join(timeout=5.0)
            if self.is_alive():
                logger.warning("Health server did not stop gracefully")
    
    def get_url(self) -> str:
        """Get the health check URL."""
        return f"http://{self.host}:{self.port}/health"


def create_health_server(status_provider: Callable[[], Dict[str, Any]], 
                        host: str = 'localhost', 
                        port: int = 9468,
                        shutdown_event: Optional[threading.Event] = None) -> HealthServer:
    """
    Create and return a health server instance.
    
    Args:
        status_provider: Function that returns current engine status
        host: Host to bind the server to
        port: Port to bind the server to
        shutdown_event: Event to signal graceful shutdown
        
    Returns:
        Configured HealthServer instance
    """
    return HealthServer(
        status_provider=status_provider,
        host=host,
        port=port,
        shutdown_event=shutdown_event
    ) 