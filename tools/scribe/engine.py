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
        self.event_queue = queue.Queue(maxsize=queue_maxsize)
        
        # Thread instances
        self.watcher = None
        self.worker = None
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
            
            # Create and start worker thread
            self.worker = Worker(
                event_queue=self.event_queue,
                shutdown_event=self.shutdown_event
            )
            self.worker.start()
            
            # Create and start watcher thread
            self.watcher = Watcher(
                event_queue=self.event_queue,
                shutdown_event=self.shutdown_event,
                watch_paths=self.watch_paths,
                file_patterns=self.file_patterns
            )
            self.watcher.start()
            
            # Create and start health server
            self.health_server = create_health_server(
                status_provider=self.get_status,
                port=self.health_port,
                shutdown_event=self.shutdown_event
            )
            self.health_server.start()
            
            logger.info("Scribe engine started successfully",
                       health_url=self.health_server.get_url())
            
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
            
            if self.worker and self.worker.is_alive():
                logger.info("Waiting for worker thread to stop")
                self.worker.join(timeout=10.0)
                if self.worker.is_alive():
                    logger.warning("Worker thread did not stop gracefully")
            
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
        if self.start_time and self.worker:
            uptime = time.time() - self.start_time
            worker_stats = self.worker.get_stats()
            
            logger.info("Engine final statistics",
                       engine_uptime_seconds=round(uptime, 2),
                       queue_final_size=self.event_queue.qsize(),
                       **worker_stats)
    
    def run_forever(self) -> None:
        """
        Run the engine until interrupted.
        
        This method starts the engine and blocks until a shutdown signal is received.
        """
        # Set up signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            logger.info("Received shutdown signal", signal=signum)
            self.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
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
            'queue_size': self.event_queue.qsize(),
            'watch_paths': self.watch_paths,
            'file_patterns': self.file_patterns
        }
        
        if self.worker:
            status.update(self.worker.get_stats()) # Existing worker stats

            # Add ActionDispatcher and CircuitBreakerManager stats
            if hasattr(self.worker, 'action_dispatcher') and self.worker.action_dispatcher:
                try:
                    dispatcher_stats = self.worker.action_dispatcher.get_execution_stats()
                    # As per ActionDispatcher.get_execution_stats(), this includes 'circuit_breaker_stats'
                    status['action_dispatcher_stats'] = dispatcher_stats
                    # For explicitness, if health endpoint specifically wants a top-level circuit_breaker_stats:
                    # status['circuit_breaker_stats'] = dispatcher_stats.get('circuit_breaker_stats', {})
                    # However, the roadmap implies they are separate keys in the final /health output,
                    # but ActionDispatcher.get_execution_stats() nests circuit_breaker_stats.
                    # For now, let's include the whole dispatcher_stats which contains circuit_breaker_stats.
                    # If a separate top-level key 'circuit_breaker_stats' is strictly needed by the health endpoint schema,
                    # this might need adjustment in how HealthCheckHandler consumes this.
                    # The roadmap for get_status says "Add their output to the main status dictionary".
                    # The roadmap for HealthCheckHandler says "exposes dispatcher and circuit breaker stats".
                    # Let's assume dispatcher_stats contains what's needed for both for now.
                    # If not, we can pull out circuit_breaker_stats explicitly.
                    # The exit condition for Step 2.2 is "Response contains action_dispatcher_stats and circuit_breaker_stats"
                    # So, let's add them as separate top-level keys if possible from dispatcher_stats.
                    status['circuit_breaker_stats'] = dispatcher_stats.get('circuit_breaker_stats',
                                                                          {'error': 'Circuit breaker stats not found in dispatcher stats'})

                except Exception as e:
                    logger.error("Failed to get ActionDispatcher stats for health endpoint", exc_info=True)
                    status['action_dispatcher_stats'] = {'error': f'Failed to get ActionDispatcher stats: {str(e)}'}
                    status['circuit_breaker_stats'] = {'error': f'Failed to get CircuitBreaker stats (via Dispatcher): {str(e)}'}
            else:
                status['action_dispatcher_stats'] = {'error': 'ActionDispatcher not available in Worker'}
                status['circuit_breaker_stats'] = {'error': 'ActionDispatcher not available in Worker (for CircuitBreaker stats)'}
        else:
            status['action_dispatcher_stats'] = {'error': 'Worker not initialized'}
            status['circuit_breaker_stats'] = {'error': 'Worker not initialized'}

        return status


def main():
    """Main entry point for the Scribe engine."""
    # TODO: Add command-line argument parsing for configuration
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