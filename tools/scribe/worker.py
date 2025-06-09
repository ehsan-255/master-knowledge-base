"""
Scribe Engine - Event Processing Worker (Consumer Thread)

This module implements the L2 Microkernel Core worker in the HMA architecture.
It consumes file system events from the queue and processes them according to rules.
"""

import threading
import queue
import time
from typing import Dict, Any, Optional
import structlog
from core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class Worker(threading.Thread):
    """
    Event processing worker thread (Consumer in producer-consumer pattern).
    
    This is part of the L2 Microkernel Core that processes events from the queue
    and orchestrates the rule matching and action execution pipeline.
    """
    
    def __init__(self, 
                 event_queue: queue.Queue,
                 shutdown_event: threading.Event,
                 queue_timeout: float = 1.0):
        """
        Initialize the worker thread.
        
        Args:
            event_queue: Thread-safe queue to consume events from
            shutdown_event: Event to signal graceful shutdown
            queue_timeout: Timeout in seconds for queue.get() operations
        """
        super().__init__(name="ScribeWorker", daemon=True)
        self.event_queue = event_queue
        self.shutdown_event = shutdown_event
        self.queue_timeout = queue_timeout
        
        # Statistics for monitoring
        self.events_processed = 0
        self.events_failed = 0
        self.start_time = None
        
        logger.info("Worker initialized", queue_timeout=queue_timeout)
    
    def run(self) -> None:
        """Main thread execution - consume and process events."""
        self.start_time = time.time()
        logger.info("Event processing worker started")
        
        try:
            while not self.shutdown_event.is_set():
                try:
                    # Get event from queue with timeout to allow shutdown checking
                    event = self.event_queue.get(timeout=self.queue_timeout)
                    
                    # Process the event
                    self._process_event(event)
                    
                    # Mark task as done
                    self.event_queue.task_done()
                    
                except queue.Empty:
                    # Timeout occurred, continue loop to check shutdown
                    continue
                except Exception as e:
                    logger.error("Unexpected error in worker loop", error=str(e), exc_info=True)
                    self.events_failed += 1
                    
        except Exception as e:
            logger.error("Worker thread error", error=str(e), exc_info=True)
        finally:
            self._log_final_stats()
            logger.info("Event processing worker stopped")
    
    def _process_event(self, event: Dict[str, Any]) -> None:
        """
        Process a single file system event.
        
        Args:
            event: Event data dictionary from the watcher
        """
        start_time = time.time()
        
        try:
            event_id = event.get('event_id', 'unknown')
            event_type = event.get('type', 'unknown')
            file_path = event.get('file_path', 'unknown')
            
            logger.info("Processing event", 
                       event_id=event_id,
                       event_type=event_type, 
                       file_path=file_path,
                       event_timestamp=event.get('timestamp'))
            
            # TODO: This is where rule matching and action execution will happen
            # For now, we just log the event to verify the pipeline works
            
            # Simulate some processing time
            time.sleep(0.001)  # 1ms processing time
            
            processing_time = (time.time() - start_time) * 1000  # Convert to ms
            
            logger.info("Event processed successfully",
                       event_id=event_id,
                       event_type=event_type,
                       file_path=file_path,
                       duration_ms=round(processing_time, 2))
            
            self.events_processed += 1
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            event_id = event.get('event_id', 'unknown')
            
            logger.error("Failed to process event",
                        event_id=event_id,
                        event_data=event,
                        error=str(e),
                        duration_ms=round(processing_time, 2),
                        exc_info=True)
            
            self.events_failed += 1
    
    def _log_final_stats(self) -> None:
        """Log final processing statistics."""
        if self.start_time:
            uptime = time.time() - self.start_time
            total_events = self.events_processed + self.events_failed
            
            logger.info("Worker final statistics",
                       uptime_seconds=round(uptime, 2),
                       events_processed=self.events_processed,
                       events_failed=self.events_failed,
                       total_events=total_events,
                       success_rate=round(self.events_processed / max(total_events, 1) * 100, 2))
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get current worker statistics.
        
        Returns:
            Dictionary with current statistics
        """
        uptime = time.time() - self.start_time if self.start_time else 0
        total_events = self.events_processed + self.events_failed
        
        return {
            'uptime_seconds': round(uptime, 2),
            'events_processed': self.events_processed,
            'events_failed': self.events_failed,
            'total_events': total_events,
            'success_rate': round(self.events_processed / max(total_events, 1) * 100, 2),
            'queue_size': self.event_queue.qsize()
        } 