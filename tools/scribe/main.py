#!/usr/bin/env python3
"""
Scribe HMA v2.2 Engine Main Entry Point

This is the main entry point for the Scribe engine that handles:
- Configuration loading and validation
- Engine component initialization  
- Graceful startup and shutdown
- Health check endpoint
- Signal handling
"""

import asyncio
import signal
import sys
import time
import threading
from pathlib import Path
from typing import Optional

import click
import structlog
import uvicorn
from fastapi import FastAPI

from .core.engine_factory import create_engine_components
from .core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class ScribeEngine:
    """Main Scribe engine that orchestrates all components."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.components = None
        self.shutdown_event = threading.Event()
        self.health_app = None
        self.health_server = None
        
    async def initialize(self):
        """Initialize all engine components."""
        logger.info("Initializing Scribe HMA v2.2 engine", config_path=self.config_path)
        
        try:
            # Create engine components
            self.components = create_engine_components(config_path=self.config_path)
            logger.info("Engine components initialized successfully")
            
            # Setup health check endpoint
            self.setup_health_endpoint()
            
            return True
            
        except Exception as e:
            logger.error("Failed to initialize engine", error=str(e), exc_info=True)
            return False
    
    def setup_health_endpoint(self):
        """Setup FastAPI health check endpoint."""
        self.health_app = FastAPI(title="Scribe Engine Health", version="2.2.0")
        
        @self.health_app.get("/health")
        async def health_check():
            """Health check endpoint."""
            if self.components is None:
                return {"status": "initializing", "timestamp": time.time()}
            
            # Basic health checks
            health_status = {
                "status": "healthy",
                "timestamp": time.time(),
                "version": "2.2.0",
                "hma_compliance": "v2.2",
                "components": {
                    "config_manager": self.components.config_manager is not None,
                    "telemetry": self.components.telemetry is not None,
                    "security_manager": self.components.security_manager is not None,
                    "plugin_loader": self.components.plugin_loader is not None,
                }
            }
            
            # Add Vault health information if available
            if (self.components.config_manager and 
                hasattr(self.components.config_manager, 'get_vault_health')):
                try:
                    vault_health = self.components.config_manager.get_vault_health()
                    health_status["vault"] = vault_health
                except Exception as e:
                    health_status["vault"] = {
                        "enabled": False,
                        "status": "error",
                        "error": str(e)
                    }
            
            return health_status
        
        @self.health_app.get("/")
        async def root():
            """Root endpoint."""
            return {"service": "scribe-engine", "version": "2.2.0", "status": "running"}
    
    async def start(self):
        """Start the engine and all its components."""
        logger.info("Starting Scribe engine")
        
        if not await self.initialize():
            logger.error("Engine initialization failed, exiting")
            return False
        
        try:
            # Start health server in background
            if self.components.config_manager:
                health_port = getattr(
                    self.components.config_manager.get_engine_settings(), 
                    'health_port', 
                    9469
                )
            else:
                health_port = 9469
            
            config = uvicorn.Config(
                self.health_app, 
                host="0.0.0.0", 
                port=health_port,
                log_level="info"
            )
            self.health_server = uvicorn.Server(config)
            
            # Start health server in background task
            health_task = asyncio.create_task(self.health_server.serve())
            
            logger.info("Engine started successfully", health_port=health_port)
            
            # Main engine loop - just wait for shutdown signal
            while not self.shutdown_event.is_set():
                await asyncio.sleep(1)
                
                # Simulate some engine activity
                if self.components and self.components.telemetry:
                    # Record that engine is running
                    pass
            
            logger.info("Shutdown signal received, stopping engine")
            
            # Stop health server
            if self.health_server:
                self.health_server.should_exit = True
                await health_task
            
            return True
            
        except Exception as e:
            logger.error("Engine runtime error", error=str(e), exc_info=True)
            return False
    
    def stop(self):
        """Stop the engine gracefully."""
        logger.info("Stopping Scribe engine")
        self.shutdown_event.set()
        
        if self.components:
            # Stop any running components
            try:
                # Add component cleanup here
                logger.info("Engine components stopped")
            except Exception as e:
                logger.error("Error stopping components", error=str(e))


# Global engine instance
engine_instance: Optional[ScribeEngine] = None


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info("Received shutdown signal", signal=signum)
    if engine_instance:
        engine_instance.stop()


@click.command()
@click.option('--config', '-c', 
              help='Path to configuration file',
              type=click.Path(exists=True, path_type=Path))
@click.option('--log-level', 
              default='INFO',
              help='Logging level',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']))
def main(config: Optional[Path], log_level: str):
    """
    Scribe HMA v2.2 Engine
    
    A sophisticated file processing engine with HMA v2.2 compliance,
    boundary validation, telemetry, and plugin architecture.
    """
    global engine_instance
    
    # Configure logging
    structlog.configure(
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    logger.info("Starting Scribe HMA v2.2 Engine")
    logger.info("Configuration", config_path=str(config) if config else None, log_level=log_level)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run engine
    engine_instance = ScribeEngine(config_path=str(config) if config else None)
    
    try:
        # Run the async engine
        success = asyncio.run(engine_instance.start())
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down")
        sys.exit(0)
    except Exception as e:
        logger.error("Unhandled exception in main", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()