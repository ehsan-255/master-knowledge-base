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
from .core.logging_config import get_scribe_logger
from .core.ports import IEventSource

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
        
        self.event_bus.publish('file_event', event_data)
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
                 event_bus: 'EventBus',  # Changed from event_queue
                 shutdown_event: threading.Event,
                 watch_paths: List[str],
                 file_patterns: Optional[List[str]] = None):
        """
        Initialize the watcher thread.
        
        Args:
            event_bus: EventBus to publish events to
            shutdown_event: Event to signal graceful shutdown
            watch_paths: List of directory paths to monitor
            file_patterns: List of file patterns to monitor
        """
        super().__init__(name="ScribeWatcher", daemon=True)
        self.event_bus = event_bus  # Changed from self.event_queue
        self.shutdown_event = shutdown_event
        self.watch_paths = watch_paths
        self.file_patterns = file_patterns or ['*.md']
        
        self.observer = Observer()
        self.event_handler = ScribeEventHandler(event_bus=self.event_bus, file_patterns=file_patterns)  # Pass event_bus
        
        logger.info("Watcher initialized", 
                   watch_paths=watch_paths, 
                   file_patterns=file_patterns)
    
    def run(self) -> None:
        """Main thread execution - start watching and handle shutdown."""
        try:
            # Set up file system observers for each watch path
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
            
            # Main loop - check for shutdown signal
            while not self.shutdown_event.is_set():
                time.sleep(0.1)  # Check shutdown every 100ms
            
            logger.info("Shutdown signal received, stopping watcher")
            
        except Exception as e:
            logger.error("Watcher thread error", error=str(e), exc_info=True)
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Clean up resources on shutdown."""
        try:
            if self.observer.is_alive():
                self.observer.stop()
                self.observer.join(timeout=5.0)  # Wait up to 5 seconds
                
            if self.observer.is_alive():
                logger.warning("Observer did not stop gracefully")
            else:
                logger.info("File system watcher stopped cleanly")
                
        except Exception as e:
            logger.error("Error during watcher cleanup", error=str(e)) 