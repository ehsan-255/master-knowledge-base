#!/usr/bin/env python3
"""
Scribe Vault OTLP Integration

Enterprise-grade OpenTelemetry integration for HashiCorp Vault operations
ensuring comprehensive observability through OTLP protocol for HMA v2.2 compliance.
"""

import os
import time
import atexit
from typing import Dict, Any, Optional
from dataclasses import dataclass
import structlog

# OpenTelemetry imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


@dataclass
class OTLPConfig:
    """Configuration for OTLP integration."""
    endpoint: str = "http://localhost:4317"
    service_name: str = "scribe-vault"
    service_version: str = "2.2.0"
    environment: str = "production"
    insecure: bool = True
    headers: Optional[Dict[str, str]] = None
    timeout: int = 30
    enable_compression: bool = True
    export_interval_millis: int = 5000
    max_export_batch_size: int = 512


class VaultOTLPIntegration:
    """
    Professional OTLP integration for Vault operations.
    
    Provides comprehensive OpenTelemetry integration including traces, metrics,
    and logs for all Vault operations with enterprise-grade configuration.
    """
    
    def __init__(self, config: Optional[OTLPConfig] = None):
        """
        Initialize OTLP integration.
        
        Args:
            config: OTLP configuration
        """
        self.config = config or self._create_default_config()
        self._tracer_provider: Optional[TracerProvider] = None
        self._meter_provider: Optional[MeterProvider] = None
        self._span_processor: Optional[BatchSpanProcessor] = None
        self._metric_reader: Optional[PeriodicExportingMetricReader] = None
        self._initialized = False
        
        logger.info("Vault OTLP integration initializing",
                   endpoint=self.config.endpoint,
                   service_name=self.config.service_name,
                   environment=self.config.environment)
    
    def _create_default_config(self) -> OTLPConfig:
        """Create default OTLP configuration from environment variables."""
        return OTLPConfig(
            endpoint=os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4317'),
            service_name=os.getenv('OTEL_SERVICE_NAME', 'scribe-vault'),
            service_version=os.getenv('OTEL_SERVICE_VERSION', '2.2.0'),
            environment=os.getenv('OTEL_RESOURCE_ATTRIBUTES_ENVIRONMENT', 'production'),
            insecure=os.getenv('OTEL_EXPORTER_OTLP_INSECURE', 'true').lower() == 'true',
            timeout=int(os.getenv('OTEL_EXPORTER_OTLP_TIMEOUT', '30')),
            enable_compression=os.getenv('OTEL_EXPORTER_OTLP_COMPRESSION', 'gzip') == 'gzip',
            export_interval_millis=int(os.getenv('OTEL_METRIC_EXPORT_INTERVAL', '5000')),
            max_export_batch_size=int(os.getenv('OTEL_EXPORTER_OTLP_BATCH_SIZE', '512'))
        )
    
    def initialize(self) -> bool:
        """
        Initialize OpenTelemetry with OTLP exporters.
        
        Returns:
            True if initialization successful
        """
        if self._initialized:
            logger.warning("OTLP integration already initialized")
            return True
        
        try:
            # Create resource with comprehensive attributes
            resource = Resource.create({
                SERVICE_NAME: self.config.service_name,
                SERVICE_VERSION: self.config.service_version,
                "deployment.environment": self.config.environment,
                "vault.integration": "enterprise",
                "service.namespace": "scribe-hma-v2.2",
                "telemetry.sdk.name": "opentelemetry",
                "telemetry.sdk.language": "python",
                "host.name": os.getenv('HOSTNAME', 'unknown'),
                "process.pid": str(os.getpid())
            })
            
            # Initialize tracing
            self._initialize_tracing(resource)
            
            # Initialize metrics
            self._initialize_metrics(resource)
            
            # Initialize instrumentation
            self._initialize_instrumentation()
            
            # Register cleanup
            atexit.register(self.shutdown)
            
            self._initialized = True
            
            logger.info("OTLP integration initialized successfully",
                       service_name=self.config.service_name,
                       endpoint=self.config.endpoint,
                       tracing_enabled=True,
                       metrics_enabled=True)
            
            return True
            
        except Exception as e:
            logger.error("Failed to initialize OTLP integration",
                        error=str(e),
                        endpoint=self.config.endpoint)
            return False
    
    def _initialize_tracing(self, resource: Resource):
        """Initialize OpenTelemetry tracing with OTLP exporter."""
        # Create OTLP span exporter
        span_exporter = OTLPSpanExporter(
            endpoint=self.config.endpoint,
            insecure=self.config.insecure,
            headers=self.config.headers or {},
            timeout=self.config.timeout,
            compression="gzip" if self.config.enable_compression else None
        )
        
        # Create span processor
        self._span_processor = BatchSpanProcessor(
            span_exporter,
            max_queue_size=2048,
            max_export_batch_size=self.config.max_export_batch_size,
            export_timeout_millis=self.config.timeout * 1000,
            schedule_delay_millis=500
        )
        
        # Create tracer provider
        self._tracer_provider = TracerProvider(resource=resource)
        self._tracer_provider.add_span_processor(self._span_processor)
        
        # Set global tracer provider
        trace.set_tracer_provider(self._tracer_provider)
        
        logger.debug("Tracing initialized with OTLP exporter")
    
    def _initialize_metrics(self, resource: Resource):
        """Initialize OpenTelemetry metrics with OTLP exporter."""
        # Create OTLP metric exporter
        metric_exporter = OTLPMetricExporter(
            endpoint=self.config.endpoint,
            insecure=self.config.insecure,
            headers=self.config.headers or {},
            timeout=self.config.timeout,
            compression="gzip" if self.config.enable_compression else None
        )
        
        # Create metric reader
        self._metric_reader = PeriodicExportingMetricReader(
            exporter=metric_exporter,
            export_interval_millis=self.config.export_interval_millis,
            export_timeout_millis=self.config.timeout * 1000
        )
        
        # Create meter provider
        self._meter_provider = MeterProvider(
            resource=resource,
            metric_readers=[self._metric_reader]
        )
        
        # Set global meter provider
        metrics.set_meter_provider(self._meter_provider)
        
        logger.debug("Metrics initialized with OTLP exporter")
    
    def _initialize_instrumentation(self):
        """Initialize automatic instrumentation for common libraries."""
        try:
            # Instrument HTTP requests
            RequestsInstrumentor().instrument()
            URLLib3Instrumentor().instrument()
            
            logger.debug("Automatic instrumentation initialized")
            
        except Exception as e:
            logger.warning("Failed to initialize some instrumentation",
                          error=str(e))
    
    def get_tracer(self, name: str) -> trace.Tracer:
        """
        Get a tracer for the specified component.
        
        Args:
            name: Tracer name
            
        Returns:
            OpenTelemetry tracer
        """
        if not self._initialized:
            self.initialize()
        
        return trace.get_tracer(name)
    
    def get_meter(self, name: str) -> metrics.Meter:
        """
        Get a meter for the specified component.
        
        Args:
            name: Meter name
            
        Returns:
            OpenTelemetry meter
        """
        if not self._initialized:
            self.initialize()
        
        return metrics.get_meter(name, version=self.config.service_version)
    
    def create_span(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> trace.Span:
        """
        Create a new span with Vault-specific attributes.
        
        Args:
            name: Span name
            attributes: Additional span attributes
            
        Returns:
            OpenTelemetry span
        """
        tracer = self.get_tracer("vault.operations")
        
        span_attributes = {
            "vault.service": self.config.service_name,
            "vault.version": self.config.service_version,
            "operation.timestamp": time.time()
        }
        
        if attributes:
            span_attributes.update(attributes)
        
        return tracer.start_span(name, attributes=span_attributes)
    
    def record_vault_operation(self, operation: str, duration: float, 
                             status: str, **attributes):
        """
        Record a Vault operation with comprehensive telemetry.
        
        Args:
            operation: Operation name
            duration: Operation duration in seconds
            status: Operation status (success/failure)
            **attributes: Additional operation attributes
        """
        # Create operation span
        with self.create_span(f"vault.{operation}", {
            "vault.operation": operation,
            "vault.duration": duration,
            "vault.status": status,
            **attributes
        }) as span:
            span.set_attribute("vault.operation.completed", True)
            
            if status == "failure":
                span.set_status(trace.Status(trace.StatusCode.ERROR))
            else:
                span.set_status(trace.Status(trace.StatusCode.OK))
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get OTLP integration health status.
        
        Returns:
            Health status information
        """
        return {
            "initialized": self._initialized,
            "service_name": self.config.service_name,
            "service_version": self.config.service_version,
            "endpoint": self.config.endpoint,
            "tracing_enabled": self._tracer_provider is not None,
            "metrics_enabled": self._meter_provider is not None,
            "environment": self.config.environment
        }
    
    def shutdown(self, timeout: int = 30):
        """
        Shutdown OTLP integration gracefully.
        
        Args:
            timeout: Shutdown timeout in seconds
        """
        if not self._initialized:
            return
        
        logger.info("Shutting down OTLP integration")
        
        try:
            # Shutdown span processor
            if self._span_processor:
                self._span_processor.shutdown(timeout_millis=timeout * 1000)
            
            # Shutdown metric reader
            if self._metric_reader:
                self._metric_reader.shutdown(timeout_millis=timeout * 1000)
            
            # Shutdown tracer provider
            if self._tracer_provider:
                self._tracer_provider.shutdown()
            
            # Shutdown meter provider
            if self._meter_provider:
                self._meter_provider.shutdown(timeout_millis=timeout * 1000)
            
            self._initialized = False
            
            logger.info("OTLP integration shutdown completed")
            
        except Exception as e:
            logger.error("Error during OTLP integration shutdown",
                        error=str(e))


# Global OTLP integration instance
_otlp_integration: Optional[VaultOTLPIntegration] = None


def get_vault_otlp_integration() -> VaultOTLPIntegration:
    """Get or create global Vault OTLP integration."""
    global _otlp_integration
    
    if _otlp_integration is None:
        _otlp_integration = VaultOTLPIntegration()
        _otlp_integration.initialize()
    
    return _otlp_integration


def initialize_vault_otlp(config: Optional[OTLPConfig] = None) -> VaultOTLPIntegration:
    """
    Initialize global Vault OTLP integration.
    
    Args:
        config: OTLP configuration
        
    Returns:
        Initialized OTLP integration
    """
    global _otlp_integration
    
    _otlp_integration = VaultOTLPIntegration(config)
    _otlp_integration.initialize()
    
    logger.info("Global Vault OTLP integration initialized")
    return _otlp_integration


def create_vault_span(name: str, **attributes) -> trace.Span:
    """
    Create a Vault operation span with automatic configuration.
    
    Args:
        name: Span name
        **attributes: Span attributes
        
    Returns:
        OpenTelemetry span
    """
    otlp = get_vault_otlp_integration()
    return otlp.create_span(name, attributes)


def record_vault_metric(name: str, value: float, unit: str = "1", **attributes):
    """
    Record a Vault metric through OTLP.
    
    Args:
        name: Metric name
        value: Metric value
        unit: Metric unit
        **attributes: Metric attributes
    """
    otlp = get_vault_otlp_integration()
    meter = otlp.get_meter("vault.metrics")
    
    # Create appropriate metric type based on name
    if "duration" in name.lower() or "time" in name.lower():
        histogram = meter.create_histogram(
            name=name,
            description=f"Vault {name} histogram",
            unit=unit
        )
        histogram.record(value, attributes)
    elif "count" in name.lower() or "total" in name.lower():
        counter = meter.create_counter(
            name=name,
            description=f"Vault {name} counter",
            unit=unit
        )
        counter.add(value, attributes)
    else:
        gauge = meter.create_up_down_counter(
            name=name,
            description=f"Vault {name} gauge",
            unit=unit
        )
        gauge.add(value, attributes)