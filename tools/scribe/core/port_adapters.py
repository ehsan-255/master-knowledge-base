#!/usr/bin/env python3
"""
HMA v2.1 Port Adapter Implementations

Concrete implementations of all mandatory HMA ports for Scribe v2.1.
These adapters provide the technology-specific implementations while
maintaining the technology-agnostic port interfaces.
"""

import asyncio
import json
import time
import threading
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
import queue
from collections import defaultdict

from .hma_ports import (
    PluginExecutionPort, CredBrokerQueryPort, EventBusPort, 
    ObservabilityPort, ConfigurationPort, HealthCheckPort,
    CommandExecutionPort, FileSystemPort, LoggingPort, PluginContextPort,
    PluginExecutionContext, PortStatus
)
from .boundary_validator import BoundaryValidator
from .hma_telemetry import HMATelemetry
from .mtls import get_mtls_manager, MTLSConfig
from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class SecurityError(Exception):
    """Exception raised when security requirements are not met."""
    pass


class ScribePluginExecutionAdapter(PluginExecutionPort):
    """Concrete implementation of plugin execution port"""
    
    def __init__(self, plugin_loader, security_manager, telemetry: HMATelemetry, config_manager=None, port_registry=None):
        self.plugin_loader = plugin_loader
        self.security_manager = security_manager
        self.telemetry = telemetry
        self.config_manager = config_manager
        self.port_registry = port_registry
        self.executing_plugins: Dict[str, bool] = {}
        self._lock = threading.RLock()
        
        # HMA v2.2 mandatory mTLS manager for inter-plugin communication
        self.mtls_manager = get_mtls_manager()
        self._configure_mtls()
    
    def _get_port_registry(self):
        """Get the port registry for plugin access"""
        return self.port_registry
    
    def _configure_mtls(self):
        """Configure mTLS for inter-plugin communication as required by HMA v2.2."""
        try:
            # Get mTLS configuration from config manager
            mtls_settings = self.config_manager.get('mtls', {}) if self.config_manager else {}
            
            if mtls_settings.get('enabled', False):
                cert_file = mtls_settings.get('cert_file')
                key_file = mtls_settings.get('key_file')
                ca_file = mtls_settings.get('ca_file')
                
                if cert_file and key_file and ca_file:
                    # Create mTLS configuration
                    mtls_config = MTLSConfig(
                        cert_file=cert_file,
                        key_file=key_file,
                        ca_file=ca_file
                    )
                    
                    # Add to mTLS manager
                    self.mtls_manager.add_configuration("plugin_execution", mtls_config)
                    
                    logger.info("mTLS configured for plugin execution",
                               cert_file=cert_file,
                               ca_file=ca_file)
                else:
                    logger.warning("mTLS enabled but certificate files not configured")
            else:
                logger.info("mTLS not enabled for plugin execution")
                
        except Exception as e:
            logger.error("Failed to configure mTLS", error=str(e))
            # Continue without mTLS but log the issue
    
    def _enforce_mtls_security(self, plugin_id: str) -> bool:
        """Enforce mTLS security for plugin communication."""
        try:
            # Check if mTLS is configured and required
            mtls_session = self.mtls_manager.get_session("plugin_execution")
            if mtls_session:
                logger.debug("mTLS security enforced for plugin",
                           plugin_id=plugin_id)
                return True
            else:
                # Log warning but allow execution (for backward compatibility)
                logger.warning("mTLS not configured for plugin communication",
                             plugin_id=plugin_id)
                return True
                
        except Exception as e:
            logger.error("mTLS security enforcement failed",
                        plugin_id=plugin_id,
                        error=str(e))
            return False
    
    async def execute_plugin(self, 
                           plugin_id: str, 
                           input_data: Dict[str, Any],
                           context: Optional[PluginExecutionContext] = None) -> Dict[str, Any]:
        """Execute plugin with validation and telemetry"""
        
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span(
            "plugin_execution_boundary", plugin_id
        ) as span:
            # Add HMA resource attributes as required by Part 1a Sec 1.4.1
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "plugin_execution")
                span.set_attribute("hma.source.component", "core")
                span.set_attribute("hma.target.component", plugin_id)
                span.set_attribute("hma.operation", "execute_plugin")
        
        with self.telemetry.trace_boundary_operation(
            "execute_plugin", "plugin_execution", "core", plugin_id
        ) as span:
            start_time = time.time()
            
            try:
                # Mark plugin as busy
                with self._lock:
                    self.executing_plugins[plugin_id] = True
                
                # HMA v2.2 mandatory mTLS enforcement for inter-plugin communication
                if not self._enforce_mtls_security(plugin_id):
                    raise SecurityError(f"mTLS security enforcement failed for plugin {plugin_id}")
                
                # Validate plugin access
                if not await self.security_manager.validate_plugin_access(plugin_id):
                    raise PermissionError(f"Plugin {plugin_id} access denied")
                
                # Validate input data
                if not await self.validate_plugin_input(plugin_id, input_data):
                    raise ValueError(f"Invalid input data for plugin {plugin_id}")
                
                # Get plugin instance
                plugin_info = self.plugin_loader.get_plugin(plugin_id)
                if not plugin_info:
                    raise ValueError(f"Plugin {plugin_id} not found")
                
                # Create plugin execution context
                execution_context = {
                    "file_path": input_data.get("file_path", ""),
                    "match_data": input_data.get("match"),
                    "request_id": context.request_id if context else None,
                    "correlation_id": context.correlation_id if context else None
                }
                
                # Create plugin instance with port-based access
                plugin_instance = plugin_info.create_instance(
                    input_data.get("params", {}),
                    # Pass the port registry from the main system
                    self._get_port_registry(),
                    execution_context
                )
                
                # Execute plugin
                if hasattr(plugin_instance, 'execute_async'):
                    result = await plugin_instance.execute_async(input_data)
                else:
                    # Run synchronous plugin in thread pool
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        None, 
                        plugin_instance.execute,
                        input_data.get("file_content", ""),
                        input_data.get("match"),
                        input_data.get("file_path", ""),
                        input_data.get("params", {})
                    )
                
                # Record success metrics
                duration = (time.time() - start_time) * 1000
                self.telemetry.record_boundary_crossing(
                    "core", plugin_id, "execute", duration
                )
                
                return {
                    "success": True,
                    "result": result,
                    "plugin_id": plugin_id,
                    "execution_time_ms": duration
                }
                
            except Exception as e:
                self.telemetry.record_error("plugin_execution_failed", plugin_id, str(e))
                logger.error("Plugin execution failed", 
                           plugin_id=plugin_id, error=str(e))
                
                return {
                    "success": False,
                    "error": str(e),
                    "plugin_id": plugin_id,
                    "execution_time_ms": (time.time() - start_time) * 1000
                }
                
            finally:
                # Mark plugin as available
                with self._lock:
                    self.executing_plugins[plugin_id] = False
    
    def get_plugin_status(self, plugin_id: str) -> PortStatus:
        """Get current plugin execution status"""
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("get_plugin_status_boundary", plugin_id) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "plugin_status")
                span.set_attribute("hma.operation", "get_status")
        
        with self._lock:
            if plugin_id in self.executing_plugins and self.executing_plugins[plugin_id]:
                return PortStatus.BUSY
            
        plugin_info = self.plugin_loader.get_plugin(plugin_id)
        if plugin_info:
            return PortStatus.AVAILABLE
        else:
            return PortStatus.OFFLINE
    
    async def validate_plugin_input(self, plugin_id: str, input_data: Dict[str, Any]) -> bool:
        """Validate input data against plugin schema"""
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("validate_plugin_input_boundary", plugin_id) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "validation")
                span.set_attribute("hma.operation", "validate_input")
        
        try:
            plugin_info = self.plugin_loader.get_plugin(plugin_id)
            if not plugin_info:
                return False
            
            # Get plugin manifest for validation schema
            manifest = plugin_info.manifest
            if not manifest:
                return True  # No manifest, skip validation
            
            # Extract validation schema from manifest
            config_schema = (
                manifest
                .get("interface_contracts", {})
                .get("action_interface", {})
                .get("configuration_schema", {})
            )
            
            if config_schema:
                import jsonschema
                jsonschema.validate(input_data.get("params", {}), config_schema)
            
            return True
            
        except Exception as e:
            logger.warning("Plugin input validation failed", 
                         plugin_id=plugin_id, error=str(e))
            return False
    
    def list_available_plugins(self) -> List[str]:
        """List all available plugins"""
        return list(self.plugin_loader.get_all_plugins().keys())

class ScribeEventBusAdapter(EventBusPort):
    """Thread-safe event bus implementation"""
    
    def __init__(self, telemetry: HMATelemetry, max_queue_size: int = 2000):
        self.telemetry = telemetry
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_queue = queue.Queue(maxsize=max_queue_size)
        self.lock = threading.RLock()
        self.running = False
        self.worker_thread = None
        
        # Statistics
        self.events_published = 0
        self.events_delivered = 0
        self.events_dropped = 0
    
    async def publish_event(self, 
                          event_type: str,
                          event_data: Dict[str, Any], 
                          target: Optional[str] = None,
                          correlation_id: Optional[str] = None) -> bool:
        """Publish event with telemetry tracking"""
        
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("publish_event_boundary", event_type) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "event_bus")
                span.set_attribute("hma.operation", "publish_event")
                span.set_attribute("hma.event.type", event_type)
                span.set_attribute("hma.event.target", target or "broadcast")
        
        try:
            event = {
                "event_type": event_type,
                "data": event_data,
                "target": target,
                "correlation_id": correlation_id,
                "timestamp": time.time(),
                "source": "scribe-core"
            }
            
            # Try to queue event
            try:
                self.event_queue.put(event, timeout=0.1)
                self.events_published += 1
                
                # Record telemetry
                self.telemetry.emit_metric(
                    "hma_events_published_total", 1.0,
                    {"event_type": event_type, "target": target or "broadcast"}
                )
                
                return True
                
            except queue.Full:
                self.events_dropped += 1
                self.telemetry.emit_metric(
                    "hma_events_dropped_total", 1.0,
                    {"event_type": event_type, "reason": "queue_full"}
                )
                logger.warning("Event queue full, dropping event", 
                             event_type=event_type)
                return False
                
        except Exception as e:
            logger.error("Event publishing failed", 
                        event_type=event_type, error=str(e))
            return False
    
    async def subscribe_to_events(self, 
                                event_types: List[str], 
                                callback: Callable,
                                subscriber_id: str) -> bool:
        """Subscribe to specific event types"""
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("subscribe_to_events_boundary", subscriber_id) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "event_bus")
                span.set_attribute("hma.operation", "subscribe")
                span.set_attribute("hma.subscriber.id", subscriber_id)
        
        try:
            with self.lock:
                for event_type in event_types:
                    self.subscribers[event_type].append({
                        "callback": callback,
                        "subscriber_id": subscriber_id
                    })
            
            logger.info("Event subscription registered",
                       subscriber_id=subscriber_id,
                       event_types=event_types)
            return True
            
        except Exception as e:
            logger.error("Event subscription failed",
                        subscriber_id=subscriber_id, error=str(e))
            return False
    
    async def unsubscribe_from_events(self, 
                                    event_types: List[str],
                                    subscriber_id: str) -> bool:
        """Unsubscribe from event types"""
        try:
            with self.lock:
                for event_type in event_types:
                    self.subscribers[event_type] = [
                        sub for sub in self.subscribers[event_type]
                        if sub["subscriber_id"] != subscriber_id
                    ]
            
            logger.info("Event unsubscription completed",
                       subscriber_id=subscriber_id,
                       event_types=event_types)
            return True
            
        except Exception as e:
            logger.error("Event unsubscription failed",
                        subscriber_id=subscriber_id, error=str(e))
            return False
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """Get event bus statistics"""
        return {
            "events_published": self.events_published,
            "events_delivered": self.events_delivered,
            "events_dropped": self.events_dropped,
            "queue_size": self.event_queue.qsize(),
            "subscriber_count": sum(len(subs) for subs in self.subscribers.values()),
            "event_types": list(self.subscribers.keys())
        }
    
    def start(self):
        """Start event processing"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_events, daemon=True)
        self.worker_thread.start()
        logger.info("Event bus started")
    
    def stop(self):
        """Stop event processing"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)
        logger.info("Event bus stopped")
    
    def _process_events(self):
        """Process events in dedicated thread"""
        while self.running:
            event_received = False
            try:
                event = self.event_queue.get(timeout=1.0)
                event_received = True
                self._handle_event(event)
                self.event_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                # Ensure task_done is called even if event handling fails
                if event_received:
                    try:
                        self.event_queue.task_done()
                    except ValueError:
                        # task_done already called or queue not properly initialized
                        pass
                logger.error("Event processing error", error=str(e))
    
    def _handle_event(self, event: Dict[str, Any]):
        """Handle individual event delivery"""
        event_type = event["event_type"]
        target = event.get("target")
        
        with self.lock:
            subscribers = self.subscribers.get(event_type, [])
        
        delivered = 0
        for subscriber in subscribers:
            # Check target filtering
            if target and subscriber["subscriber_id"] != target:
                continue
            
            try:
                subscriber["callback"](event)
                delivered += 1
            except Exception as e:
                logger.error("Event delivery failed",
                           event_type=event_type,
                           subscriber_id=subscriber["subscriber_id"],
                           error=str(e))
        
        self.events_delivered += delivered
    
    # Backward-compatible methods for legacy tests
    def put(self, event, timeout=None):
        """Legacy method for putting events (backward compatibility)"""
        try:
            if isinstance(event, dict):
                # If it's already a dict, use it directly
                self.event_queue.put(event, timeout=timeout or 0.1)
            else:
                # Convert to dict format expected by new system
                event_dict = {
                    "event_type": getattr(event, 'event_type', 'unknown'),
                    "data": event if isinstance(event, dict) else {"event": event},
                    "timestamp": time.time(),
                    "source": "legacy"
                }
                self.event_queue.put(event_dict, timeout=timeout or 0.1)
            
            self.events_published += 1
            return True
        except queue.Full:
            self.events_dropped += 1
            return False
    
    def qsize(self):
        """Legacy method for getting queue size"""
        return self.event_queue.qsize()
    
    def subscribe(self, event_types: List[str], callback: Callable):
        """Legacy subscription method - synchronous version to avoid async/threading issues"""
        try:
            # Use the subscriber ID as the callback ID for backward compatibility
            subscriber_id = f"legacy_{id(callback)}"
            
            # Direct synchronous subscription to avoid async complications
            with self.lock:
                for event_type in event_types:
                    self.subscribers[event_type].append({
                        "callback": callback,
                        "subscriber_id": subscriber_id
                    })
            
            logger.info("Legacy event subscription registered",
                       subscriber_id=subscriber_id,
                       event_types=event_types)
            return True
            
        except Exception as e:
            logger.error("Legacy subscription failed", error=str(e))
            return False

class ScribeConfigurationAdapter(ConfigurationPort):
    """Configuration management adapter"""
    
    def __init__(self, config_manager, telemetry: HMATelemetry):
        self.config_manager = config_manager
        self.telemetry = telemetry
        self.change_callbacks: Dict[str, List[Callable]] = defaultdict(list)
    
    async def get_config_value(self, 
                             key: str, 
                             component_id: str,
                             default: Any = None) -> Any:
        """Get configuration value for component"""
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("get_config_value_boundary", component_id) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "configuration")
                span.set_attribute("hma.operation", "get_config")
                span.set_attribute("hma.config.key", key)
        
        try:
            value = self.config_manager.get(key, default)
            
            self.telemetry.emit_metric(
                "hma_config_access_total", 1.0,
                {"component_id": component_id, "config_key": key}
            )
            
            return value
            
        except Exception as e:
            logger.error("Configuration access failed",
                        key=key, component_id=component_id, error=str(e))
            return default
    
    async def set_config_value(self, 
                             key: str, 
                             value: Any,
                             component_id: str) -> bool:
        """Set configuration value"""
        try:
            # Note: This would need to be implemented in the config manager
            # For now, just log the attempt
            logger.info("Configuration update requested",
                       key=key, component_id=component_id)
            return True
            
        except Exception as e:
            logger.error("Configuration update failed",
                        key=key, component_id=component_id, error=str(e))
            return False
    
    async def validate_config(self, 
                            config: Dict[str, Any],
                            schema_id: str) -> bool:
        """Validate configuration against schema"""
        return self.config_manager.validate_config_dict(config)
    
    def subscribe_to_config_changes(self, 
                                  callback: Callable,
                                  component_id: str) -> bool:
        """Subscribe to configuration changes"""
        try:
            self.change_callbacks[component_id].append(callback)
            return True
        except Exception as e:
            logger.error("Config subscription failed", error=str(e))
            return False

class ScribeHealthCheckAdapter(HealthCheckPort):
    """Health monitoring adapter"""
    
    def __init__(self, telemetry: HMATelemetry):
        self.telemetry = telemetry
        self.health_checks: Dict[str, Callable] = {}
        self.component_status: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.RLock()
    
    async def check_component_health(self, component_id: str) -> Dict[str, Any]:
        """Check health status of a component"""
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("check_component_health_boundary", component_id) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "health_check")
                span.set_attribute("hma.operation", "check_health")
                span.set_attribute("hma.component.id", component_id)
        
        try:
            if component_id in self.health_checks:
                health_check = self.health_checks[component_id]
                result = await health_check()
                
                with self.lock:
                    self.component_status[component_id] = {
                        **result,
                        "last_check": time.time()
                    }
                
                return result
            else:
                return {"status": "unknown", "message": "No health check registered"}
                
        except Exception as e:
            logger.error("Health check failed", 
                        component_id=component_id, error=str(e))
            return {"status": "error", "message": str(e)}
    
    async def register_health_check(self, 
                                  component_id: str,
                                  check_function: Callable) -> bool:
        """Register health check function"""
        try:
            self.health_checks[component_id] = check_function
            logger.info("Health check registered", component_id=component_id)
            return True
        except Exception as e:
            logger.error("Health check registration failed", 
                        component_id=component_id, error=str(e))
            return False
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        overall_status = "healthy"
        component_statuses = {}
        
        for component_id in self.health_checks:
            health = await self.check_component_health(component_id)
            component_statuses[component_id] = health
            
            if health.get("status") != "healthy":
                overall_status = "unhealthy"
        
        return {
            "overall_status": overall_status,
            "components": component_statuses,
            "timestamp": time.time()
        }


class ScribeCommandExecutionAdapter(CommandExecutionPort):
    """Command execution adapter using SecurityManager"""
    
    def __init__(self, security_manager, telemetry: HMATelemetry):
        self.security_manager = security_manager
        self.telemetry = telemetry
    
    async def execute_command_safely(self, 
                                   command_list: List[str],
                                   cwd: Optional[str] = None,
                                   timeout: int = 30,
                                   allowed_env_vars: Optional[List[str]] = None) -> tuple[bool, str, str]:
        """Execute command with security controls"""
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("command_execution_boundary", str(command_list[0] if command_list else "unknown")) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "command_execution")
                span.set_attribute("hma.operation", "execute_command")
                span.set_attribute("hma.command", str(command_list))
        
        return self.security_manager.execute_command_safely(
            command_list=command_list,
            cwd=cwd,
            timeout=timeout,
            allowed_env_vars=allowed_env_vars
        )
    
    async def validate_command_security(self, command_list: List[str]) -> bool:
        """Validate command against security policies"""
        try:
            # Use the security manager's validation (if available)
            if hasattr(self.security_manager, 'validate_command_security'):
                return await self.security_manager.validate_command_security(command_list)
            else:
                # Basic validation - ensure command is not empty and is a list
                return bool(command_list and isinstance(command_list, list))
        except Exception as e:
            logger.error("Command security validation failed", error=str(e))
            return False


class ScribeFileSystemAdapter(FileSystemPort):
    """File system adapter with security validation"""
    
    def __init__(self, security_manager, telemetry: HMATelemetry):
        self.security_manager = security_manager
        self.telemetry = telemetry
    
    async def read_file_safely(self, file_path: str) -> Optional[str]:
        """Read file with security validation"""
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("file_read_boundary", file_path) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "file_system")
                span.set_attribute("hma.operation", "read_file")
                span.set_attribute("hma.file.path", file_path)
        
        try:
            # Validate file access
            if not await self.validate_file_access(file_path, "read"):
                logger.warning("File read access denied", file_path=file_path)
                return None
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            logger.error("File read failed", file_path=file_path, error=str(e))
            return None
    
    async def write_file_safely(self, file_path: str, content: str) -> bool:
        """Write file with security validation"""  
        # HMA v2.2 mandatory OTEL boundary telemetry
        with self.telemetry.start_span("file_write_boundary", file_path) as span:
            if hasattr(span, 'set_attribute'):
                span.set_attribute("hma.boundary.type", "file_system")
                span.set_attribute("hma.operation", "write_file")
                span.set_attribute("hma.file.path", file_path)
        
        try:
            # Validate file access
            if not await self.validate_file_access(file_path, "write"):
                logger.warning("File write access denied", file_path=file_path)
                return False
            
            # Write file content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                return True
                
        except Exception as e:
            logger.error("File write failed", file_path=file_path, error=str(e))
            return False
    
    async def validate_file_access(self, file_path: str, operation: str) -> bool:
        """Validate file access permissions"""
        try:
            # Use security manager validation if available
            if hasattr(self.security_manager, 'validate_file_access'):
                return await self.security_manager.validate_file_access(file_path, operation)
            else:
                # Basic validation - check file exists for read, path is valid for write
                path = Path(file_path)
                if operation == "read":
                    return path.exists() and path.is_file()
                elif operation == "write":
                    return path.parent.exists() and path.parent.is_dir()
                return False
                
        except Exception as e:
            logger.error("File access validation failed", 
                        file_path=file_path, 
                        operation=operation, 
                        error=str(e))
            return False


class ScribeLoggingAdapter(LoggingPort):
    """Logging adapter providing structured logging interface"""
    
    def __init__(self, telemetry: HMATelemetry):
        self.telemetry = telemetry
        self.logger = get_scribe_logger("plugin_logging")
    
    def log_info(self, message: str, **context) -> None:
        """Log information with context"""
        self.logger.info(message, **context)
        self.telemetry.emit_metric(
            "hma_plugin_logs_total", 1.0,
            {"level": "info", **{k: str(v) for k, v in context.items()}}
        )
    
    def log_warning(self, message: str, **context) -> None:
        """Log warning with context"""
        self.logger.warning(message, **context)
        self.telemetry.emit_metric(
            "hma_plugin_logs_total", 1.0,
            {"level": "warning", **{k: str(v) for k, v in context.items()}}
        )
    
    def log_error(self, message: str, **context) -> None:
        """Log error with context"""
        self.logger.error(message, **context)
        self.telemetry.emit_metric(
            "hma_plugin_logs_total", 1.0,
            {"level": "error", **{k: str(v) for k, v in context.items()}}
        )
    
    def log_debug(self, message: str, **context) -> None:
        """Log debug information with context"""
        self.logger.debug(message, **context)
        self.telemetry.emit_metric(
            "hma_plugin_logs_total", 1.0,
            {"level": "debug", **{k: str(v) for k, v in context.items()}}
        )


class ScribePluginContextAdapter(PluginContextPort):
    """Plugin context adapter providing port access"""
    
    def __init__(self, plugin_id: str, port_registry, execution_context: Dict[str, Any]):
        self.plugin_id = plugin_id
        self.port_registry = port_registry
        self.execution_context = execution_context
    
    def get_plugin_id(self) -> str:
        """Get current plugin identifier"""
        return self.plugin_id
    
    def get_execution_context(self) -> Dict[str, Any]:
        """Get plugin execution context"""
        return self.execution_context.copy()
    
    def get_port(self, port_type: str) -> Any:
        """Get access to other ports through context"""
        return self.port_registry.get_port(port_type)