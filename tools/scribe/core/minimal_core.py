#!/usr/bin/env python3
"""
HMA v2.1 Minimal Core Implementation

Implements the L2 Microkernel Core with strict adherence to HMA principles:
- Routing and lifecycle management only
- No business logic
- Technology-agnostic port-based boundaries
- Comprehensive telemetry and validation
"""

import asyncio
import time
import uuid
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum

from .hma_ports import (
    PluginExecutionPort, CredBrokerQueryPort, EventBusPort, 
    ObservabilityPort, ConfigurationPort, HealthCheckPort,
    PortRegistry
)
from .boundary_validator import BoundaryValidator, BoundaryType
from .hma_telemetry import HMATelemetry
from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)

class CoreState(Enum):
    """Core operational states"""
    STOPPED = "stopped"
    STARTING = "starting" 
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"

@dataclass
class PluginRegistration:
    """Plugin registration information"""
    plugin_id: str
    plugin_type: str  # L2-Orchestrator | L3-Capability
    version: str
    manifest: Dict[str, Any]
    status: str
    registered_at: float
    
class PluginLifecycleManager:
    """Manages plugin lifecycle operations"""
    
    def __init__(self, observability: ObservabilityPort):
        self.plugins: Dict[str, PluginRegistration] = {}
        self.observability = observability
    
    async def register_plugin(self, plugin_manifest: Dict[str, Any]) -> bool:
        """Register a plugin with manifest validation"""
        try:
            plugin_id = plugin_manifest["plugin_metadata"]["id"]
            plugin_type = plugin_manifest["plugin_metadata"]["type"]
            version = plugin_manifest["plugin_metadata"]["version"]
            
            # Validate manifest schema
            if not self._validate_manifest(plugin_manifest):
                logger.error("Plugin manifest validation failed", plugin_id=plugin_id)
                return False
            
            # Create registration
            registration = PluginRegistration(
                plugin_id=plugin_id,
                plugin_type=plugin_type,
                version=version,
                manifest=plugin_manifest,
                status="registered",
                registered_at=time.time()
            )
            
            self.plugins[plugin_id] = registration
            
            # Record telemetry
            self.observability.record_plugin_activity(plugin_id, True)
            self.observability.emit_log("INFO", f"Plugin registered: {plugin_id}", "core")
            
            logger.info("Plugin registered successfully",
                       plugin_id=plugin_id,
                       plugin_type=plugin_type,
                       version=version)
            
            return True
            
        except Exception as e:
            logger.error("Plugin registration failed", error=str(e))
            return False
    
    async def unregister_plugin(self, plugin_id: str) -> bool:
        """Unregister a plugin"""
        if plugin_id not in self.plugins:
            logger.warning("Attempted to unregister unknown plugin", plugin_id=plugin_id)
            return False
        
        try:
            del self.plugins[plugin_id]
            self.observability.record_plugin_activity(plugin_id, False)
            self.observability.emit_log("INFO", f"Plugin unregistered: {plugin_id}", "core")
            
            logger.info("Plugin unregistered successfully", plugin_id=plugin_id)
            return True
            
        except Exception as e:
            logger.error("Plugin unregistration failed", plugin_id=plugin_id, error=str(e))
            return False
    
    def get_plugin_info(self, plugin_id: str) -> Optional[PluginRegistration]:
        """Get plugin registration information"""
        return self.plugins.get(plugin_id)
    
    def list_plugins(self, plugin_type: Optional[str] = None) -> List[PluginRegistration]:
        """List registered plugins, optionally filtered by type"""
        if plugin_type:
            return [p for p in self.plugins.values() if p.plugin_type == plugin_type]
        return list(self.plugins.values())
    
    def _validate_manifest(self, manifest: Dict[str, Any]) -> bool:
        """Validate plugin manifest schema"""
        required_fields = [
            "manifest_version",
            "plugin_metadata",
            "hma_compliance"
        ]
        
        try:
            for field in required_fields:
                if field not in manifest:
                    logger.error("Missing required manifest field", field=field)
                    return False
            
            # Check HMA version compatibility
            hma_version = manifest.get("hma_compliance", {}).get("hma_version")
            if hma_version != "2.1":
                logger.error("Incompatible HMA version", 
                           required="2.1", 
                           found=hma_version)
                return False
            
            return True
            
        except Exception as e:
            logger.error("Manifest validation error", error=str(e))
            return False

class HMAMinimalCore:
    """
    HMA v2.1 compliant minimal core
    
    Responsibilities:
    1. Request routing to appropriate plugins
    2. Plugin lifecycle management  
    3. Control plane service access
    
    Non-responsibilities (delegated to L2 Orchestrators):
    - Business logic processing
    - Multi-plugin workflow coordination
    - Domain-specific decision making
    """
    
    def __init__(self, port_registry: PortRegistry, config: Dict[str, Any]):
        self.config = config
        self.state = CoreState.STOPPED
        
        # Get ports from registry
        self.plugin_execution_port = port_registry.get_port("plugin_execution")
        self.event_bus_port = port_registry.get_port("event_bus")
        self.observability_port = port_registry.get_port("observability")
        self.config_port = port_registry.get_port("configuration")
        self.health_port = port_registry.get_port("health_check")
        
        # Initialize components
        self.lifecycle_manager = PluginLifecycleManager(self.observability_port)
        self.boundary_validator = BoundaryValidator({}, self.observability_port)
        
        # Routing table maps request types to plugins
        self.routing_table: Dict[str, str] = {}
        
        # Core telemetry
        from .hma_telemetry import HMAComponent
        component = HMAComponent(
            component_type="L2-Core",
            component_id="scribe-minimal-core", 
            layer="L2"
        )
        self.telemetry = HMATelemetry(component)
        
        logger.info("HMA Minimal Core initialized")
    
    async def start(self) -> bool:
        """Start the core system"""
        if self.state != CoreState.STOPPED:
            logger.warning("Core already running or starting")
            return False
        
        try:
            self.state = CoreState.STARTING
            
            with self.telemetry.trace_boundary_operation(
                "core_startup", "l2_core", "system", "core"
            ):
                # Load configuration
                await self._load_configuration()
                
                # Initialize routing table
                await self._initialize_routing()
                
                # Register health check
                await self.health_port.register_health_check(
                    "core", self._health_check
                )
                
                self.state = CoreState.RUNNING
                
                self.observability_port.emit_log(
                    "INFO", "HMA Minimal Core started successfully", "core"
                )
                
                logger.info("HMA Minimal Core started successfully")
                return True
                
        except Exception as e:
            self.state = CoreState.ERROR
            logger.error("Core startup failed", error=str(e))
            self.observability_port.record_error("core_startup_failed", "core", str(e))
            return False
    
    async def stop(self) -> bool:
        """Stop the core system gracefully"""
        if self.state not in [CoreState.RUNNING, CoreState.ERROR]:
            return True
        
        try:
            self.state = CoreState.STOPPING
            
            with self.telemetry.trace_boundary_operation(
                "core_shutdown", "l2_core", "core", "system"
            ):
                # Unregister all plugins
                for plugin_id in list(self.lifecycle_manager.plugins.keys()):
                    await self.lifecycle_manager.unregister_plugin(plugin_id)
                
                self.state = CoreState.STOPPED
                
                logger.info("HMA Minimal Core stopped successfully")
                return True
                
        except Exception as e:
            logger.error("Core shutdown failed", error=str(e))
            return False
    
    async def route_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core responsibility: Route requests to appropriate plugins
        
        This is pure routing logic with no business processing.
        """
        if self.state != CoreState.RUNNING:
            raise RuntimeError("Core not running")
        
        with self.telemetry.trace_boundary_operation(
            "route_request", "l2_core", "external", "core"
        ) as span:
            # Validate request at boundary
            validation_result = self.boundary_validator.validate_l2_plugin_call(
                request, "core"
            )
            
            if not validation_result.valid:
                error_msg = f"Request validation failed: {validation_result.errors}"
                self.observability_port.record_error(
                    "boundary_validation_failed", "core", error_msg
                )
                raise ValueError(error_msg)
            
            # Determine target plugin (pure routing logic)
            plugin_id = self._resolve_plugin(request)
            
            if not plugin_id:
                raise ValueError(f"No plugin found for request type: {request.get('type')}")
            
            # Route to plugin via port (no business logic here)
            try:
                result = await self.plugin_execution_port.execute_plugin(
                    plugin_id, request
                )
                
                # Record successful routing
                self.observability_port.record_boundary_crossing(
                    "core", plugin_id, "route_request"
                )
                
                return result
                
            except Exception as e:
                self.observability_port.record_error(
                    "plugin_execution_failed", plugin_id, str(e)
                )
                raise
    
    def _resolve_plugin(self, request: Dict[str, Any]) -> Optional[str]:
        """
        Simple routing logic - no business processing
        
        Routes based on request type to registered plugin.
        Complex routing decisions are delegated to L2 Orchestrators.
        """
        request_type = request.get("type")
        if not request_type:
            return None
        
        # Check direct mapping first
        if request_type in self.routing_table:
            return self.routing_table[request_type]
        
        # For file events, route to appropriate handler
        if request_type in ["file_created", "file_modified", "file_deleted"]:
            # Check for specific file-based routing
            file_path = request.get("file_path", "")
            
            # Simple pattern matching (no complex business logic)
            if file_path.endswith((".md", ".txt")):
                return self.routing_table.get("file_processor")
            elif file_path.endswith((".cmd", ".trigger")):
                return self.routing_table.get("command_processor")
        
        # Default fallback to orchestrator for complex decisions
        return self.routing_table.get("default_orchestrator")
    
    async def register_plugin(self, plugin_manifest: Dict[str, Any]) -> bool:
        """Core responsibility: Plugin lifecycle management"""
        with self.telemetry.trace_boundary_operation(
            "register_plugin", "l2_core", "external", "core"
        ):
            success = await self.lifecycle_manager.register_plugin(plugin_manifest)
            
            if success:
                # Update routing table based on plugin capabilities
                await self._update_routing(plugin_manifest)
            
            return success
    
    async def unregister_plugin(self, plugin_id: str) -> bool:
        """Unregister plugin and update routing"""
        with self.telemetry.trace_boundary_operation(
            "unregister_plugin", "l2_core", "external", "core"
        ):
            # Remove from routing table
            self._remove_from_routing(plugin_id)
            
            # Unregister plugin
            return await self.lifecycle_manager.unregister_plugin(plugin_id)
    
    def get_plugin_status(self, plugin_id: str) -> Optional[str]:
        """Get plugin status"""
        plugin_info = self.lifecycle_manager.get_plugin_info(plugin_id)
        return plugin_info.status if plugin_info else None
    
    def get_core_status(self) -> Dict[str, Any]:
        """Get core system status"""
        plugins = self.lifecycle_manager.list_plugins()
        
        return {
            "state": self.state.value,
            "plugin_count": len(plugins),
            "plugins_by_type": {
                "L2-Orchestrator": len([p for p in plugins if p.plugin_type == "L2-Orchestrator"]),
                "L3-Capability": len([p for p in plugins if p.plugin_type == "L3-Capability"])
            },
            "routing_rules": len(self.routing_table),
            "uptime_seconds": time.time() - getattr(self, 'start_time', time.time())
        }
    
    async def _load_configuration(self) -> None:
        """Load core configuration"""
        # Load routing configuration
        routing_config = await self.config_port.get_config_value(
            "routing", "core", {}
        )
        
        # Initialize default routing
        self.routing_table.update(routing_config)
    
    async def _initialize_routing(self) -> None:
        """Initialize routing table with defaults"""
        default_routes = {
            "file_processor": "enhanced_frontmatter_action",
            "command_processor": "run_command_action", 
            "default_orchestrator": "file_processing_orchestrator"
        }
        
        self.routing_table.update(default_routes)
    
    async def _update_routing(self, plugin_manifest: Dict[str, Any]) -> None:
        """Update routing table when plugin is registered"""
        try:
            plugin_id = plugin_manifest["plugin_metadata"]["id"]
            
            # Check if plugin defines event patterns for routing
            interface_contracts = plugin_manifest.get("interface_contracts", {})
            action_interface = interface_contracts.get("action_interface", {})
            event_patterns = action_interface.get("event_patterns", [])
            
            # Add routing rules based on event patterns
            for pattern in event_patterns:
                event_type = pattern.get("event_type")
                if event_type:
                    self.routing_table[event_type] = plugin_id
                    
        except Exception as e:
            logger.warning("Failed to update routing for plugin", error=str(e))
    
    def _remove_from_routing(self, plugin_id: str) -> None:
        """Remove plugin from routing table"""
        routes_to_remove = [
            route_key for route_key, route_plugin 
            in self.routing_table.items() 
            if route_plugin == plugin_id
        ]
        
        for route_key in routes_to_remove:
            del self.routing_table[route_key]
    
    async def _health_check(self) -> Dict[str, Any]:
        """Core health check"""
        return {
            "status": "healthy" if self.state == CoreState.RUNNING else "unhealthy",
            "state": self.state.value,
            "plugin_count": len(self.lifecycle_manager.plugins),
            "routing_rules": len(self.routing_table)
        }