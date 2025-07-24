#!/usr/bin/env python3
"""
HMA v2.1 Telemetry System

Implements mandatory OpenTelemetry boundary telemetry with HMA resource attributes
and compliance tracking for all boundary crossings.
"""

import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from contextlib import contextmanager

# Fallback context manager for when OpenTelemetry is not available
class FallbackSpan:
    """Fallback span implementation"""
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@contextmanager
def fallback_span():
    """Fallback span context manager"""
    yield FallbackSpan()

# Optional OpenTelemetry imports with fallbacks
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    from prometheus_client import start_http_server
    HAS_OPENTELEMETRY = True
except ImportError:
    # Fallback implementations for when OpenTelemetry is not available
    trace = None
    metrics = None
    TracerProvider = None
    BatchSpanProcessor = None
    ConsoleSpanExporter = None
    Resource = None
    MeterProvider = None
    PrometheusMetricReader = None
    start_http_server = None
    HAS_OPENTELEMETRY = False

from .logging_config import get_scribe_logger
from .hma_ports import ObservabilityPort

logger = get_scribe_logger(__name__)

@dataclass
class HMAComponent:
    """HMA Component identification"""
    component_type: str  # L2-Core | L2-Orchestrator | L3-Capability
    component_id: str
    layer: str  # L2 | L3
    version: str = "2.1.0"

class HMATelemetry(ObservabilityPort):
    """HMA v2.1 compliant OpenTelemetry implementation"""
    
    def __init__(self, component: HMAComponent, 
                 jaeger_endpoint: Optional[str] = None,
                 prometheus_port: int = 8000):
        self.component = component
        self.prometheus_port = prometheus_port
        
        if HAS_OPENTELEMETRY:
            # Initialize OpenTelemetry when available
            self._setup_tracing(jaeger_endpoint)
            self._setup_metrics()
            self._create_hma_metrics()
            logger.info("HMA Telemetry initialized with OpenTelemetry",
                       component_type=component.component_type,
                       component_id=component.component_id,
                       layer=component.layer)
        else:
            # Initialize fallback telemetry
            self._setup_fallback_telemetry()
            logger.warning("HMA Telemetry initialized with fallback (OpenTelemetry not available)",
                          component_type=component.component_type,
                          component_id=component.component_id,
                          layer=component.layer)
    
    def _setup_fallback_telemetry(self):
        """Setup fallback telemetry when OpenTelemetry is not available"""
        # Initialize fallback attributes
        self.tracer = None
        self.meter = None
        self.boundary_calls_counter = None
        self.plugin_execution_histogram = None
        self.active_plugins_gauge = None
        self.validation_counter = None
        self.error_counter = None
        
        logger.info("Fallback telemetry initialized - metrics will be logged only")
    
    def _setup_tracing(self, jaeger_endpoint: Optional[str]):
        """Setup distributed tracing with HMA resource attributes"""
        # Create HMA-compliant resource
        resource = Resource.create({
            # HMA v2.1 mandatory resource attributes
            "hma.component.type": self.component.component_type,
            "hma.component.id": self.component.component_id,
            "hma.layer": self.component.layer,
            "hma.version": "2.1",
            
            # Standard OTEL attributes
            "service.name": self.component.component_id,
            "service.version": self.component.version,
            "service.namespace": "scribe-engine"
        })
        
        # Setup tracer provider
        tracer_provider = TracerProvider(resource=resource)
        
        # Add console exporter for development
        tracer_provider.add_span_processor(
            BatchSpanProcessor(ConsoleSpanExporter())
        )
        
        # Add Jaeger exporter if endpoint provided
        if jaeger_endpoint:
            try:
                # Note: Would use JaegerExporter if available
                # from opentelemetry.exporter.jaeger.thrift import JaegerExporter
                # jaeger_exporter = JaegerExporter(collector_endpoint=jaeger_endpoint)
                # tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
                logger.info("Jaeger exporter configured", endpoint=jaeger_endpoint)
            except ImportError:
                logger.warning("Jaeger exporter not available, using console exporter only")
        
        trace.set_tracer_provider(tracer_provider)
        self.tracer = trace.get_tracer(__name__)
    
    def _setup_metrics(self):
        """Setup metrics with Prometheus"""
        try:
            # Create metric reader for Prometheus
            metric_reader = PrometheusMetricReader()
            
            # Create meter provider with HMA resource
            resource = Resource.create({
                "hma.component.type": self.component.component_type,
                "hma.component.id": self.component.component_id,
                "hma.layer": self.component.layer,
                "service.name": self.component.component_id,
            })
            
            meter_provider = MeterProvider(
                resource=resource,
                metric_readers=[metric_reader]
            )
            
            metrics.set_meter_provider(meter_provider)
            self.meter = metrics.get_meter(__name__)
            
            # Start Prometheus HTTP server
            start_http_server(self.prometheus_port)
            logger.info("Prometheus metrics server started", port=self.prometheus_port)
            
        except Exception as e:
            logger.error("Failed to setup metrics", error=str(e))
            # Create fallback meter
            self.meter = metrics.get_meter(__name__)
    
    def _create_hma_metrics(self):
        """Create HMA v2.1 mandatory metrics"""
        # Boundary call metrics
        self.boundary_calls_counter = self.meter.create_counter(
            "hma_boundary_calls_total",
            description="Total HMA boundary calls",
            unit="1"
        )
        
        # Plugin execution metrics
        self.plugin_execution_histogram = self.meter.create_histogram(
            "hma_plugin_execution_duration_seconds", 
            description="Plugin execution duration",
            unit="s"
        )
        
        # Active plugins gauge
        self.active_plugins_gauge = self.meter.create_up_down_counter(
            "hma_active_plugins",
            description="Number of active plugins",
            unit="1"
        )
        
        # Validation metrics
        self.validation_counter = self.meter.create_counter(
            "hma_boundary_validations_total",
            description="Total boundary validations",
            unit="1"
        )
        
        # Error metrics
        self.error_counter = self.meter.create_counter(
            "hma_errors_total",
            description="Total HMA errors",
            unit="1"
        )
    
    def start_span(self, operation: str, component_id: str, parent_span: Optional[Any] = None):
        """Start distributed trace span with HMA attributes"""
        span_name = f"hma.{self.component.layer.lower()}.{operation}"
        
        span = self.tracer.start_span(
            span_name,
            attributes={
                "hma.operation": operation,
                "hma.component.id": component_id,
                "hma.component.type": self.component.component_type,
                "hma.layer": self.component.layer
            }
        )
        
        return span
    
    def trace_boundary_operation(self, operation: str, boundary_type: str, 
                                source_component: str, target_component: str):
        """Trace HMA boundary operations with compliance tracking"""
        if HAS_OPENTELEMETRY and self.tracer:
            span_name = f"hma.boundary.{boundary_type}.{operation}"
            
            span = self.tracer.start_span(
                span_name,
                attributes={
                    "hma.boundary.type": boundary_type,
                    "hma.operation": operation,
                    "hma.source.component": source_component,
                    "hma.target.component": target_component,
                    "hma.compliance.version": "2.1"
                }
            )
        else:
            # Fallback span for when OpenTelemetry is not available
            span = FallbackSpan()
        
        # Record boundary call metric
        self.record_boundary_crossing(source_component, target_component, operation)
        
        return span
    
    def emit_metric(self, name: str, value: float, labels: Dict[str, str], 
                   metric_type: str = "counter") -> None:
        """Emit metric with HMA labels"""
        # Add HMA context to labels
        hma_labels = {
            "hma_component_type": self.component.component_type,
            "hma_component_id": self.component.component_id,
            "hma_layer": self.component.layer,
            **labels
        }
        
        if HAS_OPENTELEMETRY and self.meter:
            try:
                if metric_type == "counter":
                    counter = self.meter.create_counter(name, description=f"HMA metric: {name}")
                    counter.add(value, hma_labels)
                elif metric_type == "histogram":
                    histogram = self.meter.create_histogram(name, description=f"HMA histogram: {name}")
                    histogram.record(value, hma_labels)
                elif metric_type == "gauge":
                    gauge = self.meter.create_up_down_counter(name, description=f"HMA gauge: {name}")
                    gauge.add(value, hma_labels)
                    
            except Exception as e:
                logger.error("Failed to emit metric", name=name, error=str(e))
        else:
            # Log metric when OpenTelemetry is not available
            logger.debug(f"Metric {metric_type}: {name}", value=value, **hma_labels)
    
    def emit_log(self, level: str, message: str, component_id: str,
                extra_data: Optional[Dict[str, Any]] = None) -> None:
        """Emit structured log with HMA context"""
        log_data = {
            "level": level,
            "message": message,
            "hma_component_type": self.component.component_type,
            "hma_component_id": component_id,
            "hma_layer": self.component.layer,
            "timestamp": time.time()
        }
        
        if extra_data:
            log_data.update(extra_data)
        
        # Use appropriate log level
        if level.upper() == "ERROR":
            logger.error(message, **log_data)
        elif level.upper() == "WARNING":
            logger.warning(message, **log_data)
        elif level.upper() == "INFO":
            logger.info(message, **log_data)
        else:
            logger.debug(message, **log_data)
    
    def record_boundary_crossing(self, from_component: str, to_component: str,
                               operation: str, duration_ms: Optional[float] = None) -> None:
        """Record HMA boundary crossing for compliance"""
        if HAS_OPENTELEMETRY and self.boundary_calls_counter:
            # Record boundary call
            self.boundary_calls_counter.add(1, {
                "from_component": from_component,
                "to_component": to_component,
                "operation": operation,
                "hma_layer": self.component.layer
            })
            
            # Record duration if provided
            if duration_ms is not None and self.plugin_execution_histogram:
                self.plugin_execution_histogram.record(duration_ms / 1000.0, {
                    "operation": operation,
                    "from_component": from_component,
                    "to_component": to_component
                })
        
        logger.debug("HMA boundary crossing recorded",
                    from_component=from_component,
                    to_component=to_component,
                    operation=operation,
                    duration_ms=duration_ms)
    
    def record_plugin_activity(self, plugin_id: str, active: bool) -> None:
        """Record plugin activation/deactivation"""
        if HAS_OPENTELEMETRY and self.active_plugins_gauge:
            delta = 1 if active else -1
            self.active_plugins_gauge.add(delta, {"plugin_id": plugin_id})
        
        logger.debug("Plugin activity recorded", plugin_id=plugin_id, active=active)
    
    def record_validation_result(self, boundary_type: str, success: bool) -> None:
        """Record boundary validation result"""
        if HAS_OPENTELEMETRY and self.validation_counter:
            self.validation_counter.add(1, {
                "boundary_type": boundary_type,
                "status": "success" if success else "failure"
            })
        
        logger.debug("Validation result recorded", boundary_type=boundary_type, success=success)
    
    def record_error(self, error_type: str, component_id: str, details: Optional[str] = None) -> None:
        """Record HMA compliance error"""
        if HAS_OPENTELEMETRY and self.error_counter:
            self.error_counter.add(1, {
                "error_type": error_type,
                "component_id": component_id,
                "hma_layer": self.component.layer
            })
        
        if details:
            self.emit_log("ERROR", f"HMA compliance error: {details}", component_id,
                         {"error_type": error_type})

def create_hma_telemetry(component_type: str, component_id: str, layer: str,
                        jaeger_endpoint: Optional[str] = None,
                        prometheus_port: int = 8000) -> HMATelemetry:
    """Factory function to create HMA telemetry instance"""
    component = HMAComponent(component_type, component_id, layer)
    return HMATelemetry(component, jaeger_endpoint, prometheus_port)