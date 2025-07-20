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
from .core.logging_config import get_scribe_logger
from .core.config_manager import ConfigManager
from .core.plugin_loader import PluginLoader
from .core.security_manager import SecurityManager
from .core.rule_processor import RuleProcessor
from .core.action_dispatcher import ActionDispatcher
from .core.atomic_write import atomic_write
from .core.event_bus import EventBus
from .core.ports import AtomicFileWriter
from .core.metrics import events_processed_counter, events_failed_counter, queue_size_gauge

logger = get_scribe_logger(__name__)


class Worker(threading.Thread):
    """
    Event processing worker thread (Consumer in producer-consumer pattern).
    
    This is part of the L2 Microkernel Core that processes events from the queue
    and orchestrates the rule matching and action execution pipeline.
    """
    
    def __init__(self, 
                 event_bus: EventBus,  # Changed from event_queue
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
        self.event_bus = event_bus  # Changed from self.event_queue
        self.shutdown_event = shutdown_event
        self.queue_timeout = queue_timeout
        
        # Core service instantiation
        self.config_manager = ConfigManager()
        self.plugin_loader = PluginLoader(
            plugin_directories=self.config_manager.get_plugin_directories(),
            load_order=self.config_manager.get_plugin_load_order()
        )
        self.security_manager = SecurityManager(config_manager=self.config_manager) # Pass config_manager
        self.rule_processor = RuleProcessor(config_manager=self.config_manager) # Pass the ConfigManager instance
        # ActionDispatcher initialization in the test setup was:
        # ActionDispatcher(plugin_loader=self.worker.plugin_loader, security_config=self.worker.config_manager.get_security_settings())
        # The original Worker code is:
        # ActionDispatcher(self.plugin_loader.get_actions(), self.security_manager, self.config_manager)
        # This needs to be consistent. ActionDispatcher expects the plugin_loader *instance*.
        # And it expects security_config, not security_manager directly.
        # With ActionDispatcher __init__ changed to (plugin_loader, config_manager, security_manager, ...):
        self.action_dispatcher = ActionDispatcher(
            plugin_loader=self.plugin_loader,
            config_manager=self.config_manager,
            security_manager=self.security_manager
            # quarantine_path will use its default in ActionDispatcher.
        )
        self.file_writer = AtomicFileWriter()

        # Load all plugins
        self.plugin_loader.load_all_plugins()
        
        # Enable hot-reloading if configured
        if self.config_manager.get_plugin_auto_reload():
            self.plugin_loader.enable_hot_reload()

        # Statistics for monitoring
        self.events_processed = 0
        self.events_failed = 0
        self.start_time = None
        
        logger.info("Worker initialized", queue_timeout=queue_timeout)
        self.pre_hooks = self.config_manager.get('worker_hooks', {}).get('pre_process', [])
        self.post_hooks = self.config_manager.get('worker_hooks', {}).get('post_process', [])
    
    def run(self) -> None:
        """Main thread execution - consume and process events."""
        self.start_time = time.time()
        logger.info("Event processing worker started")
        self.event_bus.subscribe('file_event', self._process_event)  # Subscribe to file events
        try:
            while not self.shutdown_event.is_set():
                time.sleep(self.queue_timeout)  # Wait with timeout to check shutdown
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
        event_id = event.get('event_id', 'unknown')
        file_path = event.get('file_path', 'unknown') # Moved earlier for logger access
        event_type = event.get('type', 'unknown') # Moved for logger access

        try:
            logger.info("Processing event", 
                             event_id=event_id,
                             event_type=event_type,
                             file_path=file_path,
                             event_timestamp=event.get('timestamp'))

            for hook in self.pre_hooks:
                # Assuming hooks are callable or action types; simplify as log for now
                logger.info(f"Pre-hook: {hook}")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                # logger.debug(f"Successfully read content from {file_path}: {original_content}") # Optional: log content
            except IOError as e:
                logger.error(f"IOError reading file {file_path} for event {event_id}: {e}", exc_info=True)
                self.events_failed += 1
                events_failed_counter.inc()
                return
            except Exception as e: # Catch any other unexpected errors during file read
                logger.error(f"Unexpected error reading file {file_path} for event {event_id}: {e}", exc_info=True)
                self.events_failed += 1
                events_failed_counter.inc()
                return
            
            # Rule Processing
            try:
                rule_matches = self.rule_processor.process_file(file_path, original_content)
                if rule_matches:
                    logger.info(f"Found {len(rule_matches)} rule matches for file {file_path} (event {event_id}).")
                    # for match in rule_matches: # Optional: detailed logging of matches
                    #     logger.debug(f"Rule Match: {match.rule_name}, Details: {match.match_details}")
                else:
                    logger.info(f"No rule matches found for file {file_path} (event {event_id}). No actions to dispatch.")
                    pass # Continue to action dispatching
            except Exception as e:
                logger.error(f"Error during rule processing for file {file_path} (event {event_id}): {e}", exc_info=True)
                self.events_failed += 1
                events_failed_counter.inc()
                return
            
            # Action Dispatching
            current_content = original_content
            actions_executed_count = 0

            if rule_matches: # Only proceed if there are matches
                try:
                    for rule_match in rule_matches:
                        logger.info(f"Processing actions for rule '{rule_match.rule.name}' on file {file_path} (event {event_id}).")

                        # ActionDispatcher.dispatch_actions takes only the rule_match.
                        # It uses rule_match.file_content as the initial content for its action chain.
                        dispatch_result = self.action_dispatcher.dispatch_actions(rule_match)

                        if dispatch_result.success:
                            # Check if the content processed by this rule's actions actually changed from the *current* state of the content.
                            if current_content != dispatch_result.final_content:
                                logger.info(f"Content for file {file_path} updated by rule '{rule_match.rule.name}'.")
                                current_content = dispatch_result.final_content # Update overall current_content
                                actions_executed_count += dispatch_result.successful_actions
                            else:
                                logger.info(f"Rule '{rule_match.rule.name}' executed actions, but content remained unchanged from current state.")
                        else:
                            logger.warning(f"Action dispatch for rule '{rule_match.rule.name}' reported failure or was blocked. Check ActionDispatcher logs for details.")
                            # If a rule's actions fail, we might want to stop processing this file event entirely.
                            # For now, we'll let it continue, but the `current_content` won't be updated from this failed dispatch.
                            # The `events_failed` counter will be incremented if a critical error occurs causing a return.
                            # Individual action failures are logged by ActionDispatcher.

                    # Summary logging after all rule_matches for the event are processed
                    if actions_executed_count > 0 : # This counts individual successful actions that changed content
                        logger.info(f"Finished processing all rule matches for event {event_id}. Total actions resulting in modification: {actions_executed_count}.")
                    else:
                        logger.info(f"Finished processing all rule matches for event {event_id}. No actions resulted in content modification or no rules triggered actions that changed content.")

                except Exception as e:
                    logger.error(f"Error during overall action dispatching loop for file {file_path} (event {event_id}): {e}", exc_info=True)
                    self.events_failed += 1
                    events_failed_counter.inc()
                    return
            else:
                # No rule_matches, current_content remains original_content. This was logged previously.
                pass

            # Atomically write the modified content if it has changed
            if current_content != original_content:
                logger.info(f"Content for {file_path} (event {event_id}) has been modified. Attempting atomic write.")
                success = self.file_writer.write(file_path, current_content)
                if success:
                    logger.info(f"Successfully wrote modified content to {file_path} (event {event_id}).")
                else:
                    logger.error(f"Failed to write modified content to {file_path} (event {event_id}).")
                    self.events_failed += 1
                    events_failed_counter.inc()
                    return
            else:
                logger.info(f"Content for {file_path} (event {event_id}) was not modified. No write operation needed.")

            for hook in self.post_hooks:
                logger.info(f"Post-hook: {hook}")

            # If we reach here, all steps were successful or handled (no modification needed).
            processing_time = (time.time() - start_time) * 1000
            logger.info("Event processed successfully",
                             event_id=event_id,
                             event_type=event_type,
                             file_path=file_path,
                             actions_taken=actions_executed_count,
                             content_modified=current_content != original_content,
                             duration_ms=round(processing_time, 2))
            self.events_processed += 1
            events_processed_counter.inc()  # Increment metric
            
        except Exception as e: # General exception for the whole processing block if anything above failed and wasn't caught
            # This block should ideally not be reached if all specific errors return early.
            # However, it's a safeguard.
            processing_time = (time.time() - start_time) * 1000
            # events_failed would have been incremented by the specific error handling block that should have returned.
            # If it's a new error not caught before, increment here.
            # For safety, ensure it's logged if it reaches here unexpectedly.
            logger.error("Unexpected state: Reached general exception handler in _process_event",
                              event_id=event_id,
                              file_path=file_path,
                              error=str(e),
                              duration_ms=round(processing_time,2),
                              exc_info=True)
            # self.events_failed += 1 # Potentially redundant if specific handlers incremented and returned.
            # Decide if an additional increment is needed if this block is ever hit.
            
    
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
        
        status = {
            'uptime_seconds': round(uptime, 2),
            'events_processed': self.events_processed,
            'events_failed': self.events_failed,
            'total_events': total_events,
            'success_rate': round(self.events_processed / max(total_events, 1) * 100, 2),
        }
        queue_size_gauge.set(self.event_bus.get_queue_size())  # Assuming EventBus has get_queue_size method
        return status 

     