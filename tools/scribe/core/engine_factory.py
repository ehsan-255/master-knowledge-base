#!/usr/bin/env python3
"""
HMA v2.2 Compliant Engine Factory

This factory creates and configures all engine components to maintain
the minimalist core principle. The engine should only handle routing
and plugin lifecycle management, not component instantiation.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

from .config_manager import ConfigManager
from .security_manager import SecurityManager
from .plugin_loader import PluginLoader
from .async_processor import AsyncProcessor
from .telemetry import initialize_telemetry
from .port_adapters import (
    ScribePluginExecutionAdapter, ScribeConfigurationAdapter, ScribeHealthCheckAdapter,
    ScribeCommandExecutionAdapter, ScribeFileSystemAdapter, ScribeLoggingAdapter
)
from .adapters.nats_adapter import NatsEventBusAdapter
from .hma_ports import PortRegistry
from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class EngineComponents:
    """Container for all engine components created by the factory."""
    
    def __init__(self):
        self.config_manager: Optional[ConfigManager] = None
        self.security_manager: Optional[SecurityManager] = None
        self.plugin_loader: Optional[PluginLoader] = None
        self.async_processor: Optional[AsyncProcessor] = None
        self.telemetry = None
        self.port_registry: Optional[PortRegistry] = None
        
        # Port adapters
        self.plugin_execution_adapter = None
        self.event_bus_adapter = None
        self.configuration_adapter = None
        self.health_check_adapter = None
        self.command_execution_adapter = None
        self.file_system_adapter = None
        self.logging_adapter = None


def create_engine_components(
    config_path: str = "tools/scribe/config/config.json",
    telemetry_config: Optional[Dict[str, Any]] = None,
    health_port: int = 9090
) -> EngineComponents:
    """
    Factory function to create all engine components following HMA v2.2 minimalist core principle.
    
    This function is responsible for instantiating ConfigManager, SecurityManager, 
    PluginLoader, AsyncProcessor, and all port adapters.
    
    Args:
        config_path: Path to configuration file
        telemetry_config: Telemetry configuration
        health_port: Port for health server
        
    Returns:
        EngineComponents: Container with all instantiated components
    """
    logger.info("Creating HMA v2.2 compliant engine components")
    
    components = EngineComponents()
    
    try:
        # Initialize configuration manager
        components.config_manager = ConfigManager(config_path=config_path)
        logger.debug("ConfigManager created")
        
        # Initialize sophisticated TelemetryManager with OTLP endpoint from environment
        otlp_endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')
        sampling_rate = float(os.getenv('OTEL_TRACE_SAMPLING_RATE', '1.0'))
        
        components.telemetry = initialize_telemetry(
            service_name="scribe-engine",
            endpoint=otlp_endpoint,
            sampling_rate=sampling_rate
        )
        logger.debug("Sophisticated TelemetryManager created with OTLP endpoint", endpoint=otlp_endpoint)
        
        # Initialize security manager
        components.security_manager = SecurityManager(
            config_manager=components.config_manager
        )
        logger.debug("SecurityManager created")
        
        # Initialize plugin loader
        plugin_directories = components.config_manager.get_plugin_directories()
        components.plugin_loader = PluginLoader(
            plugin_directories=plugin_directories
        )
        logger.debug("PluginLoader created")
        
        # Initialize async processor
        components.async_processor = AsyncProcessor()
        logger.debug("AsyncProcessor created")
        
        # Initialize port registry
        components.port_registry = PortRegistry()
        logger.debug("PortRegistry created")
        
        # Create and register port adapters
        _create_port_adapters(components)
        
        # Load all plugins
        components.plugin_loader.load_all_plugins()
        
        # Enable hot-reloading if configured
        if components.config_manager.get_plugin_auto_reload():
            components.plugin_loader.enable_hot_reload()
        
        logger.info("Engine components created successfully")
        return components
        
    except Exception as e:
        logger.error("Failed to create engine components", error=str(e), exc_info=True)
        raise


def _create_port_adapters(components: EngineComponents) -> None:
    """Create and register all port adapters."""
    
    # Plugin execution port adapter
    components.plugin_execution_adapter = ScribePluginExecutionAdapter(
        components.plugin_loader,
        components.security_manager, 
        components.telemetry,
        components.config_manager,
        components.port_registry
    )
    components.port_registry.register_port(
        "plugin_execution", 
        components.plugin_execution_adapter
    )
    logger.debug("Plugin execution adapter registered")
    
    # NATS-based event bus port adapter (HMA v2.2 Tier 2 recommended)
    nats_config = components.config_manager.get('nats', {})
    nats_url = nats_config.get('url', 'nats://localhost:4222')
    
    components.event_bus_adapter = NatsEventBusAdapter(
        components.telemetry,
        nats_url=nats_url,
        max_reconnect_attempts=nats_config.get('max_reconnect_attempts', -1),
        reconnect_time_wait=nats_config.get('reconnect_time_wait', 2)
    )
    
    # Start NATS adapter asynchronously (will be handled by the async loop)
    components.port_registry.register_port(
        "event_bus", 
        components.event_bus_adapter
    )
    logger.debug("NATS event bus adapter registered")
    
    # Configuration port adapter
    components.configuration_adapter = ScribeConfigurationAdapter(
        components.config_manager, 
        components.telemetry
    )
    components.port_registry.register_port(
        "configuration", 
        components.configuration_adapter
    )
    logger.debug("Configuration adapter registered")
    
    # Health check port adapter
    components.health_check_adapter = ScribeHealthCheckAdapter(components.telemetry)
    components.port_registry.register_port(
        "health_check", 
        components.health_check_adapter
    )
    logger.debug("Health check adapter registered")
    
    # Observability port (telemetry itself implements this)
    components.port_registry.register_port("observability", components.telemetry)
    logger.debug("Observability port registered")
    
    # Command execution port adapter
    components.command_execution_adapter = ScribeCommandExecutionAdapter(
        components.security_manager,
        components.telemetry
    )
    components.port_registry.register_port(
        "command_execution",
        components.command_execution_adapter
    )
    logger.debug("Command execution adapter registered")
    
    # File system port adapter
    components.file_system_adapter = ScribeFileSystemAdapter(
        components.security_manager,
        components.telemetry
    )
    components.port_registry.register_port(
        "file_system",
        components.file_system_adapter
    )
    logger.debug("File system adapter registered")
    
    # Logging port adapter
    components.logging_adapter = ScribeLoggingAdapter(components.telemetry)
    components.port_registry.register_port(
        "logging",
        components.logging_adapter
    )
    logger.debug("Logging adapter registered")