#!/usr/bin/env python3
"""
HMA v2.1 Mandatory Port Definitions

This module defines all mandatory HMA ports required for v2.1 compliance.
These ports provide technology-agnostic interfaces for all boundary interactions.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable
import asyncio
from dataclasses import dataclass
from enum import Enum

class PortStatus(Enum):
    """Port status enumeration"""
    AVAILABLE = "available"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class PluginExecutionContext:
    """Context for plugin execution"""
    plugin_id: str
    request_id: str
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = None

class PluginExecutionPort(ABC):
    """HMA v2.1 mandatory port for plugin execution"""
    
    @abstractmethod
    async def execute_plugin(self, 
                           plugin_id: str, 
                           input_data: Dict[str, Any],
                           context: Optional[PluginExecutionContext] = None) -> Dict[str, Any]:
        """
        Execute plugin with validated input
        
        Args:
            plugin_id: Unique plugin identifier
            input_data: Validated input data
            context: Execution context
            
        Returns:
            Plugin execution result
        """
        pass
    
    @abstractmethod
    def get_plugin_status(self, plugin_id: str) -> PortStatus:
        """Get current plugin execution status"""
        pass
    
    @abstractmethod
    async def validate_plugin_input(self, plugin_id: str, input_data: Dict[str, Any]) -> bool:
        """Validate input data against plugin schema"""
        pass
    
    @abstractmethod
    def list_available_plugins(self) -> List[str]:
        """List all available plugins"""
        pass

class CredBrokerQueryPort(ABC):
    """HMA v2.1 mandatory port for credential access"""
    
    @abstractmethod
    async def get_credential(self, 
                           credential_id: str, 
                           requesting_plugin: str,
                           context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Retrieve credential with access control
        
        Args:
            credential_id: Unique credential identifier
            requesting_plugin: Plugin requesting the credential
            context: Request context for audit
            
        Returns:
            Credential value if authorized, None otherwise
        """
        pass
    
    @abstractmethod
    async def validate_access(self, credential_id: str, plugin_id: str) -> bool:
        """Validate plugin access to credential"""
        pass
    
    @abstractmethod
    async def store_credential(self, 
                             credential_id: str, 
                             credential_value: str,
                             metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Store credential securely"""
        pass
    
    @abstractmethod
    async def revoke_access(self, credential_id: str, plugin_id: str) -> bool:
        """Revoke plugin access to credential"""
        pass

class EventBusPort(ABC):
    """HMA v2.1 mandatory port for event communication"""
    
    @abstractmethod
    async def publish_event(self, 
                          event_type: str,
                          event_data: Dict[str, Any], 
                          target: Optional[str] = None,
                          correlation_id: Optional[str] = None) -> bool:
        """
        Publish event with optional targeting
        
        Args:
            event_type: Type of event being published
            event_data: Event payload
            target: Optional target plugin/component
            correlation_id: For distributed tracing
            
        Returns:
            True if event was published successfully
        """
        pass
    
    @abstractmethod
    async def subscribe_to_events(self, 
                                event_types: List[str], 
                                callback: Callable,
                                subscriber_id: str) -> bool:
        """Subscribe to specific event types"""
        pass
    
    @abstractmethod
    async def unsubscribe_from_events(self, 
                                    event_types: List[str],
                                    subscriber_id: str) -> bool:
        """Unsubscribe from event types"""
        pass
    
    @abstractmethod
    def get_event_statistics(self) -> Dict[str, Any]:
        """Get event bus statistics"""
        pass

class ObservabilityPort(ABC):
    """HMA v2.1 mandatory port for telemetry"""
    
    @abstractmethod
    def emit_metric(self, 
                   name: str, 
                   value: float, 
                   labels: Dict[str, str],
                   metric_type: str = "counter") -> None:
        """Emit metric with HMA labels"""
        pass
    
    @abstractmethod
    def start_span(self, 
                  operation: str, 
                  component_id: str,
                  parent_span: Optional[Any] = None) -> Any:
        """Start distributed trace span"""
        pass
    
    @abstractmethod
    def emit_log(self, 
                level: str, 
                message: str, 
                component_id: str,
                extra_data: Optional[Dict[str, Any]] = None) -> None:
        """Emit structured log with HMA context"""
        pass
    
    @abstractmethod
    def record_boundary_crossing(self, 
                               from_component: str,
                               to_component: str,
                               operation: str,
                               duration_ms: Optional[float] = None) -> None:
        """Record HMA boundary crossing for compliance"""
        pass

class ConfigurationPort(ABC):
    """HMA v2.1 port for configuration management"""
    
    @abstractmethod
    async def get_config_value(self, 
                             key: str, 
                             component_id: str,
                             default: Any = None) -> Any:
        """Get configuration value for component"""
        pass
    
    @abstractmethod
    async def set_config_value(self, 
                             key: str, 
                             value: Any,
                             component_id: str) -> bool:
        """Set configuration value"""
        pass
    
    @abstractmethod
    async def validate_config(self, 
                            config: Dict[str, Any],
                            schema_id: str) -> bool:
        """Validate configuration against schema"""
        pass
    
    @abstractmethod
    def subscribe_to_config_changes(self, 
                                  callback: Callable,
                                  component_id: str) -> bool:
        """Subscribe to configuration changes"""
        pass

class HealthCheckPort(ABC):
    """HMA v2.1 port for health monitoring"""
    
    @abstractmethod
    async def check_component_health(self, component_id: str) -> Dict[str, Any]:
        """Check health status of a component"""
        pass
    
    @abstractmethod
    async def register_health_check(self, 
                                  component_id: str,
                                  check_function: Callable) -> bool:
        """Register health check function"""
        pass
    
    @abstractmethod
    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        pass

# Additional ports for plugin operations
class CommandExecutionPort(ABC):
    """HMA v2.2 port for secure command execution"""
    
    @abstractmethod
    async def execute_command_safely(self, 
                                   command_list: List[str],
                                   cwd: Optional[str] = None,
                                   timeout: int = 30,
                                   allowed_env_vars: Optional[List[str]] = None) -> tuple[bool, str, str]:
        """Execute command with security controls"""
        pass
    
    @abstractmethod
    async def validate_command_security(self, command_list: List[str]) -> bool:
        """Validate command against security policies"""
        pass

class FileSystemPort(ABC):
    """HMA v2.2 port for file system operations"""
    
    @abstractmethod
    async def read_file_safely(self, file_path: str) -> Optional[str]:
        """Read file with security validation"""
        pass
    
    @abstractmethod
    async def write_file_safely(self, file_path: str, content: str) -> bool:
        """Write file with security validation"""
        pass
    
    @abstractmethod
    async def validate_file_access(self, file_path: str, operation: str) -> bool:
        """Validate file access permissions"""
        pass

class LoggingPort(ABC):
    """HMA v2.2 port for structured logging"""
    
    @abstractmethod
    def log_info(self, message: str, **context) -> None:
        """Log information with context"""
        pass
    
    @abstractmethod
    def log_warning(self, message: str, **context) -> None:
        """Log warning with context"""
        pass
    
    @abstractmethod
    def log_error(self, message: str, **context) -> None:
        """Log error with context"""
        pass
    
    @abstractmethod
    def log_debug(self, message: str, **context) -> None:
        """Log debug information with context"""
        pass

class PluginContextPort(ABC):
    """HMA v2.2 port providing plugin execution context"""
    
    @abstractmethod
    def get_plugin_id(self) -> str:
        """Get current plugin identifier"""
        pass
    
    @abstractmethod
    def get_execution_context(self) -> Dict[str, Any]:
        """Get plugin execution context"""
        pass
    
    @abstractmethod
    def get_port(self, port_type: str) -> Any:
        """Get access to other ports through context"""
        pass

# Port registry for dependency injection
class PortRegistry:
    """Registry for HMA ports to enable dependency injection"""
    
    def __init__(self):
        self._ports: Dict[str, Any] = {}
    
    def register_port(self, port_type: str, port_instance: Any) -> None:
        """Register a port implementation"""
        self._ports[port_type] = port_instance
    
    def get_port(self, port_type: str) -> Any:
        """Get a registered port implementation"""
        if port_type not in self._ports:
            raise ValueError(f"Port type '{port_type}' not registered")
        return self._ports[port_type]
    
    def list_registered_ports(self) -> List[str]:
        """List all registered port types"""
        return list(self._ports.keys())