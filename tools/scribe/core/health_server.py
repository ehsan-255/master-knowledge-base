#!/usr/bin/env python3
"""
Health Server Implementation

Provides HTTP health endpoint for Scribe engine monitoring.
"""

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from typing import Callable, Dict, Any
import socket

from tools.scribe.core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)

class HealthRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for health checks"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/health':
            self._handle_health_check()
        elif self.path == '/':
            self._handle_root()
        else:
            self._handle_not_found()
    
    def _handle_health_check(self):
        """Handle /health endpoint"""
        try:
            status = self.server.status_provider()
            response_code = 200 if status.get('is_running', False) else 503
            
            self.send_response(response_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response_data = {
                "status": "healthy" if response_code == 200 else "unhealthy",
                "timestamp": time.time(),
                **status
            }
            
            self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
            
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            self._send_error_response(500, "Internal server error")
    
    def _handle_root(self):
        """Handle root path"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Scribe Health Server')
    
    def _handle_not_found(self):
        """Handle 404 responses"""
        self._send_error_response(404, "Not found")
    
    def _send_error_response(self, code: int, message: str):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"error": message, "code": code}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to use structured logging"""
        logger.debug("Health server request", message=format % args)

class HealthServer(threading.Thread):
    """HTTP server for health checks"""
    
    def __init__(self, port: int = 9090, status_provider: Callable[[], Dict[str, Any]] = None):
        super().__init__(daemon=True, name="HealthServer")
        self.port = port
        self.status_provider = status_provider or (lambda: {"status": "unknown"})
        self.server = None
        self.running = False
    
    def run(self):
        """Start the health server"""
        try:
            # Create the server with retry logic for port binding
            for attempt in range(5):
                try:
                    self.server = HTTPServer(('localhost', self.port), HealthRequestHandler)
                    break
                except OSError as e:
                    if e.errno == 10048:  # Windows: Address already in use
                        logger.warning(f"Port {self.port} in use, trying {self.port + 1}")
                        self.port += 1
                        continue
                    elif e.errno == 98:  # Linux: Address already in use  
                        logger.warning(f"Port {self.port} in use, trying {self.port + 1}")
                        self.port += 1
                        continue
                    else:
                        raise
            
            if not self.server:
                raise Exception("Could not bind to any port after 5 attempts")
            
            self.server.status_provider = self.status_provider
            self.running = True
            
            logger.info("Health server started", port=self.port)
            self.server.serve_forever()
            
        except Exception as e:
            logger.error("Health server failed to start", port=self.port, error=str(e))
            self.running = False
    
    def stop(self):
        """Stop the health server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
            logger.info("Health server stopped")
    
    def is_alive(self):
        """Check if server is running"""
        return self.running and super().is_alive()
    
    def get_port(self):
        """Get the actual port the server is running on"""
        return self.port