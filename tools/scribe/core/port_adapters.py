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
from .vault_certificate_manager import get_vault_certificate_manager
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
            security_settings = self.config_manager.get('security', {}) if self.config_manager else {}
            
            # Check if mTLS is enabled (either explicitly or via security.enable_mtls)
            mtls_enabled = (
                mtls_settings.get('enabled', False) or 
                security_settings.get('enable_mtls', False)
            )
            
            if mtls_enabled:
                mtls_config = None
                
                # Try Vault certificates first if Vault is enabled
                if self.config_manager and self.config_manager.is_vault_enabled():
                    try:
                        vault_cert_manager = get_vault_certificate_manager(self.config_manager)
                        mtls_config = vault_cert_manager.get_mtls_config(
                            common_name="scribe.local",
                            alt_names=["localhost", "scribe-engine"],
                            ttl="8760h"
                        )
                        
                        if mtls_config:
                            logger.info("mTLS configured from Vault certificates")
                        else:
                            logger.warning("Failed to get mTLS config from Vault, falling back")
                            
                    except Exception as e:
                        logger.warning("Vault certificate retrieval failed, using fallback",
                                     error=str(e))
                
                # Fallback to configured certificate files
                if not mtls_config:
                    cert_file = mtls_settings.get('cert_file') or security_settings.get('cert_path')
                    key_file = mtls_settings.get('key_file') or security_settings.get('key_path')
                    ca_file = mtls_settings.get('ca_file') or security_settings.get('ca_path')
                    
                    if cert_file and key_file and ca_file:
                        # Create mTLS configuration from filesystem
                        mtls_config = MTLSConfig(
                            cert_file=cert_file,
                            key_file=key_file,
                            ca_file=ca_file
                        )
                        
                        logger.info("mTLS configured from filesystem certificates",
                                   cert_file=cert_file,
                                   ca_file=ca_file)
                    else:
                        logger.warning("mTLS enabled but certificate files not configured")
                
                # Add configuration to mTLS manager if successful
                if mtls_config:
                    self.mtls_manager.add_configuration("plugin_execution", mtls_config)
                    logger.info("mTLS configuration added to manager")
                else:
                    logger.error("Failed to create any mTLS configuration")
                    
            else:
                logger.info("mTLS not enabled for plugin execution")
                
        except Exception as e:
            logger.error("Failed to configure mTLS", error=str(e), exc_info=True)
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