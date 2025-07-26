"""
Scribe Engine - File System Watcher (Producer Thread)

This module implements the L1 Driving Adapter in the HMA architecture.
It monitors file system events and feeds them into the event processing pipeline.
"""

import threading
import queue
import time
import uuid
import asyncio
from pathlib import Path
from typing import List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import structlog
from tools.scribe.core.logging_config import get_scribe_logger
from tools.scribe.core.ports import IEventSource
from tools.scribe.core.boundary_validator import create_boundary_validator, BoundaryType
from tools.scribe.core.telemetry import get_telemetry_manager, initialize_telemetry
from tools.scribe.core.dlq import write_dlq

logger = get_scribe_logger(__name__)


class ScribeEventHandler(FileSystemEventHandler):
    """Custom event handler that filters and queues relevant file system events with HMA v2.2 L1 boundary validation."""
    
    def __init__(self, event_bus_port, file_patterns: Optional[List[str]] = None):
        """
        Initialize the event handler with sophisticated boundary validation.
        
        Args:
            event_bus_port: EventBusPort to publish events to
            file_patterns: List of file patterns to monitor (e.g., ['*.md', '*.txt'])
        """
        super().__init__()
        self.event_bus_port = event_bus_port
        self.file_patterns = file_patterns or ['*.md']  # Default to markdown files
        
        # Initialize sophisticated HMA v2.2 L1 boundary validation
        self.boundary_validator = create_boundary_validator()
        
        # Initialize telemetry for boundary tracking  
        self.telemetry_manager = initialize_telemetry("scribe-file-watcher")
        
        logger.info("ScribeEventHandler initialized with HMA v2.2 L1 boundary validation",
                   file_patterns=self.file_patterns)
        
    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if not event.is_directory and self._should_process_file(event.src_path):
            self._publish_event('modified', event.src_path)
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if not event.is_directory and self._should_process_file(event.src_path):
            self._publish_event('created', event.src_path)
    
    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move/rename events."""
        if not event.is_directory and self._should_process_file(event.dest_path):
            self._publish_event('moved', event.dest_path, event.src_path)
    
    def _should_process_file(self, file_path: str) -> bool:
        """Check if file matches our monitoring patterns."""
        path = Path(file_path)
        return any(path.match(pattern) for pattern in self.file_patterns)
    
    def _publish_event(self, event_type: str, file_path: str, old_path: Optional[str] = None) -> None:
        """Publish a processed event with HMA v2.2 L1 boundary validation."""
        # Generate unique event_id for traceability
        event_id = str(uuid.uuid4())
        
        event_data = {
            'event_id': event_id,
            'type': event_type,
            'file_path': file_path,
            'old_path': old_path,
            'timestamp': time.time()
        }
        
        # HMA v2.2 L1 Boundary Validation BEFORE processing
        with self.telemetry_manager.trace_boundary_call(
            "inbound", "file_system", "file_watcher", "event_validation"
        ) as span:
            # Validate against L1 file_system_event schema using sophisticated boundary validator
            validation_result = self.boundary_validator.validate_l1_input(event_data, "file_system")
            
            span.set_attribute("surface", "file_system")
            span.set_attribute("event_type", event_type)
            span.set_attribute("valid", validation_result.valid)
            span.set_attribute("error_count", len(validation_result.errors))
            span.set_attribute("event_id", event_id)
            
            if not validation_result.valid:
                # L1 validation failed - drop event and DLQ
                self.telemetry_manager.action_failures_counter.add(1, {
                    "surface": "file_system",
                    "reason": "l1_validation_failed"
                })
                
                write_dlq("file_system", event_id, validation_result.errors, {
                    "file_path": file_path,
                    "event_type": event_type,
                    "component_id": validation_result.component_id
                })
                
                logger.error("L1 boundary validation failed; file system event dropped",
                           event_id=event_id,
                           event_type=event_type,
                           file_path=file_path,
                           errors=validation_result.errors,
                           boundary_type=validation_result.boundary_type.value)
                return
            
            # Validation passed - record success metrics
            self.telemetry_manager.file_events_counter.add(1, {
                "surface": "file_system",
                "event_type": event_type
            })
        
        # Publish validated event through EventBusPort
        try:
            # Create an event loop if one doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Publish via EventBusPort
            loop.run_until_complete(
                self.event_bus_port.publish_event('file_event', event_data, correlation_id=event_id)
            )
            
            logger.debug("File system event published after L1 validation", 
                        event_id=event_id,
                        event_type=event_type, 
                        file_path=file_path,
                        validation_passed=True)
        except Exception as e:
            logger.error("Failed to publish validated event", 
                        event_id=event_id,
                        event_type=event_type,
                        file_path=file_path,
                        error=str(e))


class Watcher(threading.Thread, IEventSource):
    """
    File system watcher thread (Producer in producer-consumer pattern).
    
    This is the L1 Driving Adapter that observes file system events
    and feeds them into the Scribe processing pipeline.
    """
    
    def __init__(self, 
                 watch_paths: List[str],
                 file_patterns: Optional[List[str]] = None,
                 event_bus_port = None,
                 shutdown_event: threading.Event = None,
                 debounce_seconds: float = 0.5):
        """
        Initialize the watcher thread.
        
        Args:
            watch_paths: List of directory paths to monitor
            file_patterns: List of file patterns to monitor
            event_bus_port: EventBusPort to publish events to
            shutdown_event: Event to signal graceful shutdown
            debounce_seconds: Debounce delay for file events
        """
        super().__init__(name="ScribeWatcher", daemon=True)
            
        self.watch_paths = watch_paths
        self.file_patterns = file_patterns or ['*.md']
        self.event_bus_port = event_bus_port
        self.shutdown_event = shutdown_event or threading.Event()
        self.debounce_seconds = debounce_seconds
        
        # Initialize observer
        self.observer = Observer()
        
        # Create event handler
        self.event_handler = ScribeEventHandler(
            event_bus_port=self.event_bus_port, 
            file_patterns=self.file_patterns
        )
        
        logger.info("Watcher initialized", 
                   watch_paths=watch_paths, 
                   file_patterns=file_patterns)
    
    def start(self):
        """Start the watcher (start the thread and setup observers)"""
        # Start the thread
        super().start()
        
        # Setup file system monitoring
        try:
            for watch_path in self.watch_paths:
                path = Path(watch_path)
                if path.exists():
                    self.observer.schedule(self.event_handler, str(path), recursive=True)
                    logger.info("Watching path", path=str(path))
                else:
                    logger.warning("Watch path does not exist", path=str(path))
            
            # Start the observer
            self.observer.start()
            logger.info("File system watcher started")
        except Exception as e:
            logger.error("Failed to start watcher", error=str(e))
    
    def run(self) -> None:
        """Main thread execution - wait for shutdown signal"""
        try:
            # Main loop - check for shutdown signal
            while not self.shutdown_event.is_set():
                time.sleep(0.1)  # Check shutdown every 100ms
            
            logger.info("Shutdown signal received, stopping watcher")
            
        except Exception as e:
            logger.error("Watcher thread error", error=str(e), exc_info=True)
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the watcher and clean up resources"""
        try:
            # Stop the observer if it's running
            if hasattr(self, 'observer') and self.observer:
                if self.observer.is_alive():
                    self.observer.stop()
                    self.observer.join(timeout=5.0)  # Wait up to 5 seconds
                    
                if self.observer.is_alive():
                    logger.warning("Observer did not stop gracefully")
                else:
                    logger.info("File system watcher stopped cleanly")
            
            # Set shutdown event
            if self.shutdown_event:
                self.shutdown_event.set()
                
        except Exception as e:
            logger.error("Error during watcher cleanup", error=str(e))