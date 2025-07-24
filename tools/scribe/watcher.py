"""
Scribe Engine - File System Watcher (Producer Thread)

This module implements the L1 Driving Adapter in the HMA architecture.
It monitors file system events and feeds them into the event processing pipeline.
"""

import threading
import queue
import time
import uuid
from pathlib import Path
from typing import List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import structlog
from tools.scribe.core.logging_config import get_scribe_logger
from tools.scribe.core.ports import IEventSource

logger = get_scribe_logger(__name__)


class ScribeEventHandler(FileSystemEventHandler):
    """Custom event handler that filters and queues relevant file system events."""
    
    def __init__(self, event_bus: 'EventBus', file_patterns: Optional[List[str]] = None):
        """
        Initialize the event handler.
        
        Args:
            event_bus: EventBus to publish events to
            file_patterns: List of file patterns to monitor (e.g., ['*.md', '*.txt'])
        """
        super().__init__()
        self.event_bus = event_bus
        self.file_patterns = file_patterns or ['*.md']  # Default to markdown files
        
    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if not event.is_directory and self._should_process_file(event.src_path):
            self._queue_event('modified', event.src_path)
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if not event.is_directory and self._should_process_file(event.src_path):
            self._queue_event('created', event.src_path)
    
    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move/rename events."""
        if not event.is_directory and self._should_process_file(event.dest_path):
            self._queue_event('moved', event.dest_path, event.src_path)
    
    def _should_process_file(self, file_path: str) -> bool:
        """Check if file matches our monitoring patterns."""
        path = Path(file_path)
        return any(path.match(pattern) for pattern in self.file_patterns)
    
    def _queue_event(self, event_type: str, file_path: str, old_path: Optional[str] = None) -> None:
        """Queue a processed event for the worker thread."""
        # Generate unique event_id for traceability
        event_id = str(uuid.uuid4())
        
        event_data = {
            'event_id': event_id,
            'type': event_type,
            'file_path': file_path,
            'old_path': old_path,
            'timestamp': time.time()
        }
        
        # Backward compatibility: handle both event bus and direct queue
        if hasattr(self.event_bus, 'publish'):
            # New event bus interface
            self.event_bus.publish('file_event', event_data)
        elif hasattr(self.event_bus, 'put'):
            # Legacy queue interface
            try:
                self.event_bus.put(event_data, timeout=1.0)
            except Exception:
                # Queue full or other issue - fail silently for tests
                pass
        else:
            # No valid interface - log error but don't crash
            logger.warning("Event bus has no publish or put method", event_bus_type=type(self.event_bus).__name__)
        logger.debug("Published event", 
                        event_id=event_id,
                        event_type=event_type, 
                        file_path=file_path)


class Watcher(threading.Thread, IEventSource):
    """
    File system watcher thread (Producer in producer-consumer pattern).
    
    This is the L1 Driving Adapter that observes file system events
    and feeds them into the Scribe processing pipeline.
    """
    
    def __init__(self, 
                 watch_paths: List[str],
                 file_patterns: Optional[List[str]] = None,
                 event_bus = None,
                 shutdown_event: threading.Event = None,
                 debounce_seconds: float = 0.5,
                 event_queue=None):  # Backward compatibility alias
        """
        Initialize the watcher thread.
        
        Args:
            watch_paths: List of directory paths to monitor
            file_patterns: List of file patterns to monitor
            event_bus: EventBus to publish events to
            shutdown_event: Event to signal graceful shutdown
            debounce_seconds: Debounce delay for file events
        """
        super().__init__(name="ScribeWatcher", daemon=True)
        
        # Handle backward compatibility for event_queue parameter  
        if event_queue is not None and event_bus is None:
            event_bus = event_queue
        elif event_bus is None and event_queue is None:
            # Allow None for testing - some tests may not provide either
            pass
            
        self.watch_paths = watch_paths
        self.file_patterns = file_patterns or ['*.md']
        self.event_bus = event_bus
        # Add backward compatible property alias
        self.event_queue = event_bus
        self.shutdown_event = shutdown_event or threading.Event()
        self.debounce_seconds = debounce_seconds
        
        # Initialize observer
        self.observer = Observer()
        
        # Create event handler
        self.event_handler = ScribeEventHandler(
            event_bus=self.event_bus, 
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