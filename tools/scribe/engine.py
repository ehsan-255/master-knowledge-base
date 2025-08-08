#!/usr/bin/env python3
"""
Scribe Engine v2.2 - HMA Compliant Minimalist Core

This is the main entry point for the Scribe v2.2 automation engine.
It implements HMA v2.2 compliant architecture with true minimalist core,
following dependency injection principles and removing god object anti-patterns.
"""

import sys
import signal
import threading
import time
import asyncio
from typing import List, Optional, Dict, Any

# HMA v2.2 Core Components
from tools.scribe.core.minimal_core import HMAMinimalCore, CoreState
from tools.scribe.core.engine_factory import create_engine_components, EngineComponents
from tools.scribe.core.logging_config import configure_structured_logging, get_scribe_logger

# Configure structured logging
configure_structured_logging(log_level="INFO", include_stdlib_logs=True)
logger = get_scribe_logger(__name__)


class ScribeEngine:
    """
    HMA v2.2 Compliant Scribe Engine - Minimalist Core
    
    This class implements the HMA v2.2 architecture with:
    - True minimal core focused only on routing and lifecycle management
    - Dependency injection to eliminate god object anti-patterns
    - No component instantiation (handled by factory)
    - Pure L2 Core responsibilities only
    """
    
    def __init__(self, 
                 components: Optional[EngineComponents] = None,
                 config_path: str = "tools/scribe/config/config.json",
                 telemetry_config: Optional[Dict[str, Any]] = None,
                 health_port: int = 9090):
        """
        Initialize the HMA v2.2 compliant minimalist Scribe engine.
        
        Args:
            components: Pre-created engine components (via factory)
            config_path: Path to configuration file (fallback if components not provided)
            telemetry_config: Telemetry configuration (fallback if components not provided)
            health_port: Health server port (fallback if components not provided)
        """
        # Create components via factory if not provided (maintaining backward compatibility)
        if components is None:
            logger.info("No components provided, creating via factory")
            components = create_engine_components(
                config_path=config_path,
                telemetry_config=telemetry_config or {},
                health_port=health_port
            )
        
        # Injected components (no instantiation in core)
        self.components = components
        self.port_registry = components.port_registry
        self.minimal_core = None
        self.shutdown_event = threading.Event()
        
        # State management (minimal core responsibilities only)
        self.start_time = None
        self.is_running = False
        self.initialization_complete = False
        
        logger.info("Scribe Engine v2.2 minimalist core initialized")
    
    async def initialize_minimal_core(self) -> bool:
        """Initialize HMA v2.2 minimal core (components already created by factory)"""
        try:
            # Components already created by factory, just initialize minimal core
            core_config = self.components.config_manager.get_engine_settings()
            self.minimal_core = HMAMinimalCore(self.port_registry, core_config)
            
            # Load plugins through the existing plugin loader
            await self._load_plugins(self.components.plugin_loader)
            
            self.initialization_complete = True
            logger.info("HMA v2.2 minimal core initialized successfully")
            return True
            
        except Exception as e:
            logger.error("HMA minimal core initialization failed", error=str(e), exc_info=True)
            return False
    
    def start(self) -> None:
        """Start the HMA v2.2 compliant minimalist Scribe engine."""
        if self.is_running:
            logger.warning("Engine is already running")
            return
        
        try:
            self.start_time = time.time()
            
            logger.info("Starting Scribe Engine v2.2 minimalist core")
            
            # Initialize minimal core asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Start NATS event bus adapter
                event_bus = self.port_registry.get_port("event_bus")
                if event_bus and hasattr(event_bus, 'start'):
                    if not loop.run_until_complete(event_bus.start()):
                        logger.warning("Failed to start NATS event bus - continuing with limited functionality")
                
                # Initialize minimal core (components already created)
                if not loop.run_until_complete(self.initialize_minimal_core()):
                    raise RuntimeError("Failed to initialize minimal core")
                
                # Start minimal core
                if not loop.run_until_complete(self.minimal_core.start()):
                    raise RuntimeError("Failed to start minimal core")
                
                self.is_running = True
                logger.info("Scribe Engine v2.2 started successfully")
                
            finally:
                loop.close()
            
        except Exception as e:
            logger.error("Failed to start Scribe Engine v2.2", error=str(e), exc_info=True)
            self.stop()
            raise
    
    def stop(self) -> None:
        """Stop the Scribe engine gracefully."""
        if not self.is_running:
            logger.warning("Engine is not running")
            return
        
        logger.info("Stopping Scribe engine")
        
        try:
            # Signal shutdown to all threads
            self.shutdown_event.set()
            
            # Stop HMA minimal core
            if self.minimal_core:
                logger.info("Stopping minimal core")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self.minimal_core.stop())
                finally:
                    loop.close()
            
            # Stop NATS event bus adapter
            if self.port_registry:
                event_bus = self.port_registry.get_port("event_bus")
                if event_bus and hasattr(event_bus, 'stop'):
                    # NATS adapter requires async stop
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(event_bus.stop())
                    finally:
                        loop.close()
            
            # Log final statistics
            self._log_final_stats()
            
            self.is_running = False
            logger.info("Scribe engine stopped successfully")
            
        except Exception as e:
            logger.error("Error during engine shutdown", error=str(e), exc_info=True)
    
    def _log_final_stats(self) -> None:
        """Log final engine statistics."""
        if self.start_time:
            uptime = time.time() - self.start_time
            
            stats = {
                "engine_uptime_seconds": round(uptime, 2),
                "initialization_complete": self.initialization_complete
            }
            
            # Add event bus stats if available
            if self.port_registry:
                event_bus = self.port_registry.get_port("event_bus")
                if event_bus and hasattr(event_bus, 'get_event_statistics'):
                    stats["event_bus_stats"] = event_bus.get_event_statistics()
            
            # Add core stats if available
            if self.minimal_core:
                stats["core_status"] = self.minimal_core.get_core_status()
            
            logger.info("Engine final statistics", **stats)
    
    def run_forever(self) -> None:
        """
        Run the engine until interrupted.
        
        This method starts the engine and blocks until a shutdown signal is received.
        """
        # Set up signal handlers for graceful shutdown (only in main thread)
        try:
            def signal_handler(signum, frame):
                logger.info("Received shutdown signal", signal=signum)
                self.stop()
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        except ValueError:
            # Not in main thread, signal handling not available
            logger.debug("Signal handling not available in background thread")
        
        try:
            self.start()
            
            # Main loop - wait for shutdown
            while self.is_running and not self.shutdown_event.is_set():
                time.sleep(1.0)  # Check every second
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error("Unexpected error in main loop", error=str(e), exc_info=True)
        finally:
            self.stop()
    
    def get_status(self) -> dict:
        """
        Get current engine status.
        
        Returns:
            Dictionary with current engine status and statistics
        """
        uptime = time.time() - self.start_time if self.start_time else 0
        
        status = {
            'is_running': self.is_running,
            'uptime_seconds': round(uptime, 2),
            'initialization_complete': self.initialization_complete,
            'engine_version': '2.2.0'
        }
        
        # Add HMA components status
        if self.minimal_core:
            status['hma_core'] = self.minimal_core.get_core_status()
        
        # Add event bus statistics
        if self.port_registry:
            event_bus = self.port_registry.get_port("event_bus")
            if event_bus and hasattr(event_bus, 'get_event_statistics'):
                event_stats = event_bus.get_event_statistics()
                status['queue_size'] = event_stats.get('queue_size', 0)
                status['event_bus_stats'] = event_stats
            else:
                status['queue_size'] = 0
        else:
            status['queue_size'] = 0
        
        # Add telemetry status if available
        if self.components and self.components.telemetry:
            status['telemetry_active'] = True
        
        return status
    
    async def _load_plugins(self, plugin_loader) -> None:
        """Load and register all plugins with the minimal core"""
        try:
            # Load available plugins
            plugins = plugin_loader.load_all_plugins()
            
            # Register each plugin with the minimal core
            for plugin_id, plugin_info in plugins.items():
                try:
                    # Get plugin manifest
                    manifest = plugin_info.manifest
                    if not manifest:
                        logger.warning("Plugin missing manifest, skipping", plugin_id=plugin_id)
                        continue
                    
                    # Register with minimal core
                    success = await self.minimal_core.register_plugin(manifest)
                    if success:
                        logger.info("Plugin registered successfully", 
                                   plugin_id=plugin_id, 
                                   plugin_type=manifest.get("plugin_metadata", {}).get("type"))
                    else:
                        logger.error("Plugin registration failed", plugin_id=plugin_id)
                        
                except Exception as e:
                    logger.error("Plugin loading failed", 
                               plugin_id=plugin_id, 
                               error=str(e))
            
            logger.info("Plugin loading completed", 
                       total_plugins=len(plugins),
                       registered_plugins=len(self.minimal_core.lifecycle_manager.plugins))
            
        except Exception as e:
            logger.error("Plugin loading process failed", error=str(e))
            raise
    


def main():
    """Main entry point for the Scribe engine."""
    logger.info("Scribe Engine v2.2 starting up")
    
    try:
        # Create engine components via factory (HMA v2.2 compliant)
        components = create_engine_components()
        
        # Create minimalist engine with dependency injection
        engine = ScribeEngine(components=components)
        
        engine.run_forever()
        
    except Exception as e:
        logger.error("Fatal error in Scribe engine", error=str(e), exc_info=True)
        sys.exit(1)
    
    logger.info("Scribe Engine v2.2 shutdown complete")


if __name__ == "__main__":
    main() 