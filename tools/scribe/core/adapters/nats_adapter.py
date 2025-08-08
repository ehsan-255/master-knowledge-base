#!/usr/bin/env python3
"""
NATS EventBus Adapter - HMA v2.2 Tier 2 Recommended Implementation

This adapter implements the EventBusPort interface using NATS as the underlying
message broker, replacing the legacy in-memory queue implementation.
"""

import asyncio
import json
import time
import threading
from typing import Dict, Any, Optional, List, Callable
from collections import defaultdict
import nats
from nats.aio.client import Client as NATSClient
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

from ..hma_ports import EventBusPort
from ..hma_telemetry import HMATelemetry
from ..logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class NatsEventBusAdapter(EventBusPort):
    """
    NATS-based EventBus implementation as recommended by HMA v2.2 Tier 2 technologies.
    
    This adapter replaces the legacy in-memory queue with a production-grade
    NATS message broker for improved scalability and resilience.
    """
    
    def __init__(self, 
                 telemetry: HMATelemetry,
                 nats_url: str = "nats://localhost:4222",
                 max_reconnect_attempts: int = -1,
                 reconnect_time_wait: int = 2):
        """
        Initialize NATS EventBus adapter.
        
        Args:
            telemetry: HMA telemetry instance
            nats_url: NATS server URL
            max_reconnect_attempts: Maximum reconnection attempts (-1 for unlimited)
            reconnect_time_wait: Wait time between reconnection attempts
        """
        self.telemetry = telemetry
        self.nats_url = nats_url
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_time_wait = reconnect_time_wait
        
        # NATS client and connection management
        self.nats_client: Optional[NATSClient] = None
        self.connected = False
        self.running = False
        
        # Subscription management
        self.subscribers: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.nats_subscriptions: Dict[str, Any] = {}
        self.lock = threading.RLock()
        
        # Statistics tracking
        self.events_published = 0
        self.events_delivered = 0
        self.events_dropped = 0
        self.connection_errors = 0
        
        logger.info("NATS EventBus adapter initialized",
                   nats_url=nats_url,
                   max_reconnect_attempts=max_reconnect_attempts)
    
    async def start(self) -> bool:
        """Start the NATS EventBus adapter."""
        if self.running:
            logger.warning("NATS EventBus adapter already running")
            return True
        
        try:
            # Create NATS client
            self.nats_client = nats.connect(
                servers=[self.nats_url],
                max_reconnect_attempts=self.max_reconnect_attempts,
                reconnect_time_wait=self.reconnect_time_wait,
                disconnected_cb=self._on_disconnected,
                reconnected_cb=self._on_reconnected,
                error_cb=self._on_error,
                closed_cb=self._on_closed
            )
            
            # Connect to NATS server
            await self.nats_client
            self.connected = True
            self.running = True
            
            logger.info("NATS EventBus adapter started successfully",
                       server_info=self.nats_client.server_info)
            
            # Record telemetry
            self.telemetry.emit_metric(
                "hma_nats_connection_total", 1.0,
                {"status": "connected", "server": self.nats_url}
            )
            
            return True
            
        except Exception as e:
            logger.error("Failed to start NATS EventBus adapter",
                        error=str(e),
                        nats_url=self.nats_url)
            self.connection_errors += 1
            self.telemetry.record_error("nats_connection_failed", "nats_adapter", str(e))
            return False
    
    async def stop(self) -> None:
        """Stop the NATS EventBus adapter."""
        if not self.running:
            return
        
        try:
            self.running = False
            
            # Unsubscribe from all subjects
            for subject, subscription in self.nats_subscriptions.items():
                try:
                    await subscription.unsubscribe()
                    logger.debug("Unsubscribed from NATS subject", subject=subject)
                except Exception as e:
                    logger.warning("Failed to unsubscribe from subject",
                                 subject=subject,
                                 error=str(e))
            
            self.nats_subscriptions.clear()
            
            # Close NATS connection
            if self.nats_client and self.connected:
                await self.nats_client.close()
                self.connected = False
                logger.info("NATS connection closed")
            
            # Record final statistics
            self._log_final_stats()
            
            logger.info("NATS EventBus adapter stopped successfully")
            
        except Exception as e:
            logger.error("Error stopping NATS EventBus adapter", error=str(e))
    
    async def publish_event(self, 
                          event_type: str,
                          event_data: Dict[str, Any], 
                          target: Optional[str] = None,
                          correlation_id: Optional[str] = None) -> bool:
        """Publish event to NATS broker."""
        
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("nats_publish_event_boundary", event_type) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "event_bus")
                span.set_attribute("hma.operation", "publish_event")
                span.set_attribute("hma.event.type", event_type)
                span.set_attribute("hma.event.target", target or "broadcast")
                span.set_attribute("hma.message_broker", "nats")
        
        if not self.connected or not self.nats_client:
            logger.error("Cannot publish event - NATS not connected",
                        event_type=event_type)
            self.events_dropped += 1
            return False
        
        try:
            # Create HMA-compliant event structure
            event = {
                "eventId": correlation_id or f"event_{int(time.time() * 1000000)}",
                "eventType": event_type,
                "eventVersion": "2.2",
                "source": "scribe-core",
                "timestamp": time.time(),
                "data": event_data
            }
            
            # Determine NATS subject
            subject = f"scribe.events.{event_type}"
            if target:
                subject = f"scribe.events.{event_type}.{target}"
            
            # Serialize event data
            event_json = json.dumps(event).encode('utf-8')
            
            # Publish to NATS
            await self.nats_client.publish(subject, event_json)
            
            self.events_published += 1
            
            # Record telemetry
            self.telemetry.emit_metric(
                "hma_events_published_total", 1.0,
                {"event_type": event_type, "target": target or "broadcast", "broker": "nats"}
            )
            
            logger.debug("Event published to NATS",
                        event_type=event_type,
                        subject=subject,
                        target=target,
                        correlation_id=correlation_id)
            
            return True
            
        except Exception as e:
            logger.error("Failed to publish event to NATS",
                        event_type=event_type,
                        error=str(e))
            self.events_dropped += 1
            self.telemetry.emit_metric(
                "hma_events_dropped_total", 1.0,
                {"event_type": event_type, "reason": "nats_publish_error"}
            )
            return False
    
    async def subscribe_to_events(self, 
                                event_types: List[str], 
                                callback: Callable,
                                subscriber_id: str) -> bool:
        """Subscribe to specific event types via NATS."""
        
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("nats_subscribe_boundary", subscriber_id) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "event_bus")
                span.set_attribute("hma.operation", "subscribe")
                span.set_attribute("hma.subscriber.id", subscriber_id)
                span.set_attribute("hma.message_broker", "nats")
        
        if not self.connected or not self.nats_client:
            logger.error("Cannot subscribe to events - NATS not connected",
                        subscriber_id=subscriber_id,
                        event_types=event_types)
            return False
        
        try:
            with self.lock:
                for event_type in event_types:
                    # Add to local subscribers tracking
                    self.subscribers[event_type].append({
                        "callback": callback,
                        "subscriber_id": subscriber_id
                    })
                    
                    # Create NATS subscription if not exists
                    subject = f"scribe.events.{event_type}"
                    if subject not in self.nats_subscriptions:
                        subscription = await self.nats_client.subscribe(
                            subject,
                            cb=self._create_nats_callback(event_type)
                        )
                        self.nats_subscriptions[subject] = subscription
                        
                        logger.debug("Created NATS subscription",
                                   subject=subject,
                                   event_type=event_type)
            
            logger.info("Subscribed to NATS events",
                       subscriber_id=subscriber_id,
                       event_types=event_types)
            return True
            
        except Exception as e:
            logger.error("Failed to subscribe to NATS events",
                        subscriber_id=subscriber_id,
                        event_types=event_types,
                        error=str(e))
            return False
    
    async def unsubscribe_from_events(self, 
                                    event_types: List[str],
                                    subscriber_id: str) -> bool:
        """Unsubscribe from event types."""
        
        try:
            with self.lock:
                for event_type in event_types:
                    # Remove from local subscribers
                    self.subscribers[event_type] = [
                        sub for sub in self.subscribers[event_type]
                        if sub["subscriber_id"] != subscriber_id
                    ]
                    
                    # If no more local subscribers, remove NATS subscription
                    if not self.subscribers[event_type]:
                        subject = f"scribe.events.{event_type}"
                        if subject in self.nats_subscriptions:
                            await self.nats_subscriptions[subject].unsubscribe()
                            del self.nats_subscriptions[subject]
                            
                            logger.debug("Removed NATS subscription",
                                       subject=subject,
                                       event_type=event_type)
            
            logger.info("Unsubscribed from NATS events",
                       subscriber_id=subscriber_id,
                       event_types=event_types)
            return True
            
        except Exception as e:
            logger.error("Failed to unsubscribe from NATS events",
                        subscriber_id=subscriber_id,
                        event_types=event_types,
                        error=str(e))
            return False
    
    def _create_nats_callback(self, event_type: str) -> Callable:
        """Create NATS message callback for event type."""
        
        async def nats_callback(msg):
            """Handle NATS message and deliver to subscribers."""
            try:
                # Parse event data
                event_data = json.loads(msg.data.decode('utf-8'))
                
                # Validate HMA event structure
                if not self._validate_hma_event(event_data):
                    logger.warning("Received invalid HMA event structure",
                                 event_type=event_type,
                                 subject=msg.subject)
                    return
                
                # Deliver to all subscribers for this event type
                with self.lock:
                    subscribers = self.subscribers.get(event_type, [])
                
                delivered = 0
                for subscriber in subscribers:
                    try:
                        # Call subscriber callback
                        callback = subscriber["callback"]
                        if asyncio.iscoroutinefunction(callback):
                            await callback(event_data)
                        else:
                            callback(event_data)
                        
                        delivered += 1
                        
                    except Exception as e:
                        logger.error("Error delivering NATS event to subscriber",
                                   event_type=event_type,
                                   subscriber_id=subscriber["subscriber_id"],
                                   error=str(e))
                
                self.events_delivered += delivered
                
                logger.debug("NATS event delivered",
                           event_type=event_type,
                           subscribers_delivered=delivered,
                           event_id=event_data.get("eventId"))
                
            except Exception as e:
                logger.error("Error processing NATS message",
                           event_type=event_type,
                           subject=msg.subject,
                           error=str(e))
        
        return nats_callback
    
    def _validate_hma_event(self, event_data: Dict[str, Any]) -> bool:
        """Validate HMA v2.2 event structure."""
        required_fields = ["eventId", "eventType", "eventVersion", "source", "timestamp", "data"]
        
        for field in required_fields:
            if field not in event_data:
                logger.warning("Missing required HMA event field", field=field)
                return False
        
        return True
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """Get NATS event bus statistics."""
        return {
            "events_published": self.events_published,
            "events_delivered": self.events_delivered,
            "events_dropped": self.events_dropped,
            "connection_errors": self.connection_errors,
            "connected": self.connected,
            "running": self.running,
            "nats_url": self.nats_url,
            "subscriber_count": sum(len(subs) for subs in self.subscribers.values()),
            "event_types": list(self.subscribers.keys()),
            "nats_subscriptions": len(self.nats_subscriptions),
            "broker_type": "nats"
        }
    
    # Backward compatibility methods for legacy tests
    def put(self, event, timeout=None):
        """Legacy method for putting events (backward compatibility)."""
        logger.warning("Using legacy put() method - consider migrating to publish_event()")
        
        # Convert legacy event to modern format
        if isinstance(event, dict):
            event_type = event.get('type', event.get('event_type', 'unknown'))
            event_data = event.get('data', event)
        else:
            event_type = 'legacy_event'
            event_data = {"legacy_event": event}
        
        # Use asyncio to run the async publish method
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, schedule the coroutine
                asyncio.create_task(self.publish_event(event_type, event_data))
                return True
            else:
                # If not in async context, run until complete
                return loop.run_until_complete(self.publish_event(event_type, event_data))
        except Exception as e:
            logger.error("Legacy put() method failed", error=str(e))
            return False
    
    def qsize(self) -> int:
        """Legacy method for getting queue size (NATS doesn't have traditional queue size)."""
        # For NATS, we return the number of active subscriptions as a proxy
        return len(self.nats_subscriptions)
    
    def _log_final_stats(self) -> None:
        """Log final NATS adapter statistics."""
        if self.events_published > 0 or self.events_delivered > 0:
            stats = self.get_event_statistics()
            logger.info("NATS EventBus final statistics", **stats)
    
    # NATS connection event handlers
    async def _on_disconnected(self):
        """Handle NATS disconnection."""
        logger.warning("NATS connection lost")
        self.connected = False
        self.connection_errors += 1
        self.telemetry.emit_metric(
            "hma_nats_disconnections_total", 1.0,
            {"server": self.nats_url}
        )
    
    async def _on_reconnected(self):
        """Handle NATS reconnection."""
        logger.info("NATS connection restored")
        self.connected = True
        self.telemetry.emit_metric(
            "hma_nats_reconnections_total", 1.0,
            {"server": self.nats_url}
        )
    
    async def _on_error(self, error):
        """Handle NATS errors."""
        logger.error("NATS error occurred", error=str(error))
        self.connection_errors += 1
        self.telemetry.record_error("nats_error", "nats_adapter", str(error))
    
    async def _on_closed(self):
        """Handle NATS connection closed."""
        logger.info("NATS connection closed")
        self.connected = False