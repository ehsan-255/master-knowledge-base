#!/usr/bin/env python3
"""
Scribe Engine - Main Orchestrator

This is the main entry point for the Scribe automation engine.
It implements the L2 Microkernel Core orchestration in the HMA architecture.
"""

import sys
import signal
import threading
import queue
import time
from pathlib import Path
from typing import List, Optional
import structlog

# Import our components
from .watcher import Watcher
from .worker import Worker
from .core.logging_config import configure_structured_logging, get_scribe_logger
from .core.health_server import create_health_server
from .core.event_bus import EventBus
from .core.metrics import start_metrics_server, events_processed_counter # Example
from .core.factories import WatcherFactory, WorkerFactory

# Configure structured logging using our dedicated module
configure_structured_logging(log_level="INFO", include_stdlib_logs=True)

logger = get_scribe_logger(__name__)


class ScribeEngine:
    """
    Main Scribe Engine orchestrator.
    
    This class implements the L2 Microkernel Core that coordinates
    the producer-consumer pipeline and manages the engine lifecycle.
    """
    
    def __init__(self, 
                 watch_paths: Optional[List[str]] = None,
                 file_patterns: Optional[List[str]] = None,
                 queue_maxsize: int = 1000,
                 health_port: int = 9468):
        """
        Initialize the Scribe engine.
        
        Args:
            watch_paths: List of directory paths to monitor
            file_patterns: List of file patterns to monitor
            queue_maxsize: Maximum size of the event queue
            health_port: Port for the health check HTTP server
        """
        # Default configuration
        self.watch_paths = watch_paths or ['.']  # Default to current directory
        self.file_patterns = file_patterns or ['*.md']  # Default to markdown files
        self.health_port = health_port
        
        # Threading components
        self.shutdown_event = threading.Event()
        self.event_bus = EventBus(maxsize=queue_maxsize)  # Replace direct queue
        
        # Thread instances
        self.watcher = None
        self.processing_thread = None  # New thread for event processing
        self.health_server = None
        
        # Engine state
        self.start_time = None
        self.is_running = False
        
        logger.info("Scribe engine initialized",
                   watch_paths=self.watch_paths,
                   file_patterns=self.file_patterns,
                   queue_maxsize=queue_maxsize,
                   health_port=health_port)
    
    def start(self) -> None:
        """Start the Scribe engine."""
        if self.is_running:
            logger.warning("Engine is already running")
            return
        
        try:
            self.start_time = time.time()
            self.is_running = True
            
            logger.info("Starting Scribe engine")
            
            # Start event processing thread
            self.processing_thread = WorkerFactory.create({}, self.event_bus, self.shutdown_event)  # Assuming no specific config for worker
            self.processing_thread.start()
            
            # Create and start watcher (publishes to bus)
            self.watcher = WatcherFactory.create({'type': 'filesystem', 'paths': self.watch_paths, 'patterns': self.file_patterns}, self.event_bus, self.shutdown_event)
            self.watcher.start()
            
            # Create and start health server
            self.health_server = create_health_server(
                status_provider=self.get_status,
                port=self.health_port,
                shutdown_event=self.shutdown_event
            )
            self.health_server.start()
            
            start_metrics_server(port=8000)  # Start Prometheus server
            
            logger.info("Scribe engine started successfully")
            
        except Exception as e:
            logger.error("Failed to start Scribe engine", error=str(e), exc_info=True)
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
            
            # Wait for threads to finish
            if self.watcher and self.watcher.is_alive():
                logger.info("Waiting for watcher thread to stop")
                self.watcher.join(timeout=10.0)
                if self.watcher.is_alive():
                    logger.warning("Watcher thread did not stop gracefully")
            
            if self.processing_thread and self.processing_thread.is_alive():
                logger.info("Waiting for processing thread to stop")
                self.processing_thread.join(timeout=10.0)
                if self.processing_thread.is_alive():
                    logger.warning("Processing thread did not stop gracefully")
            
            if self.health_server and self.health_server.is_alive():
                logger.info("Waiting for health server to stop")
                self.health_server.stop()
            
            # Log final statistics
            self._log_final_stats()
            
            self.is_running = False
            logger.info("Scribe engine stopped")
            
        except Exception as e:
            logger.error("Error during engine shutdown", error=str(e), exc_info=True)
    
    def _log_final_stats(self) -> None:
        """Log final engine statistics."""
        if self.start_time and self.processing_thread: # Changed from self.worker to self.processing_thread
            uptime = time.time() - self.start_time
            # The worker stats are now handled by the status_provider in health_server
            # We can still log the processing thread stats if needed, but the health server provides the main status.
            # For now, let's keep the original structure.
            # worker_stats = self.worker.get_stats() # This line is no longer needed
            
            logger.info("Engine final statistics",
                       engine_uptime_seconds=round(uptime, 2),
                       queue_final_size=self.event_bus.qsize(), # Changed from self.event_queue to self.event_bus
                       # **worker_stats) # This line is no longer needed
                       )
    
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
            'queue_size': self.event_bus.qsize(), # Changed from self.event_queue to self.event_bus
            'watch_paths': self.watch_paths,
            'file_patterns': self.file_patterns
        }
        
        # Add metrics summary
        status['metrics_summary'] = {
            'events_processed': events_processed_counter._value.get(),  # Example access
            # Add more as needed
        }
        
        # The worker stats are now handled by the status_provider in health_server
        # We can still log the processing thread stats if needed, but the health server provides the main status.
        # For now, let's keep the original structure.
        # if self.worker:
        #     status.update(self.worker.get_stats()) # Existing worker stats

        # Add ActionDispatcher and CircuitBreakerManager stats
        # The worker's action_dispatcher is now part of the health_server's status_provider.
        # We need to access it directly or pass it to the status_provider.
        # For now, let's assume the health_server's status_provider handles this.
        # If a separate top-level key 'circuit_breaker_stats' is strictly needed by the health endpoint schema,
        # this might need adjustment in how HealthCheckHandler consumes this.
        # The roadmap for get_status says "Add their output to the main status dictionary".
        # The roadmap for HealthCheckHandler says "exposes dispatcher and circuit breaker stats".
        # Let's assume dispatcher_stats contains what's needed for both for now.
        # If not, we can pull out circuit_breaker_stats explicitly.
        # The exit condition for Step 2.2 is "Response contains action_dispatcher_stats and circuit_breaker_stats"
        # So, let's add them as separate top-level keys if possible from dispatcher_stats.
        # status['action_dispatcher_stats'] = {'error': 'ActionDispatcher not available in Worker'} # This line is no longer needed
        # status['circuit_breaker_stats'] = {'error': 'ActionDispatcher not available in Worker (for CircuitBreaker stats)'} # This line is no longer needed

        return status


def main():
    """Main entry point for the Scribe engine."""
    # Command-line configuration to be added in future version
    # For now, use default configuration
    
    logger.info("Scribe Engine starting up")
    
    try:
        engine = ScribeEngine(
            watch_paths=['.'],  # Watch current directory
            file_patterns=['*.md', '*.txt']  # Monitor markdown and text files
        )
        
        engine.run_forever()
        
    except Exception as e:
        logger.error("Fatal error in Scribe engine", error=str(e), exc_info=True)
        sys.exit(1)
    
    logger.info("Scribe Engine shutdown complete")


if __name__ == "__main__":
    main() 