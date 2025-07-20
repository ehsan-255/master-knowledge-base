#!/usr/bin/env python3
"""
Scribe Engine OpenTelemetry Integration

Implements HMA v2.2 mandatory boundary telemetry requirements using OpenTelemetry.
Provides tracing, metrics, and logging for all boundary interfaces.
"""

import time
import threading
from typing import Dict, Any, Optional, List, Union
from contextlib import contextmanager
import structlog

try:
    from opentelemetry import trace, metrics
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.semconv.resource import ResourceAttributes
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.threading import ThreadingInstrumentor
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class MockTracer:
    """Mock tracer for when OpenTelemetry is not available."""
    
    def start_span(self, name: str, **kwargs):
        return MockSpan()
    
    def start_as_current_span(self, name: str, **kwargs):
        return MockSpan()


class MockSpan:
    """Mock span for when OpenTelemetry is not available."""
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
    
    def set_attribute(self, key: str, value: Any):
        pass
    
    def set_status(self, status):
        pass
    
    def record_exception(self, exception: Exception):
        pass


class MockMeter:
    """Mock meter for when OpenTelemetry is not available."""
    
    def create_counter(self, name: str, **kwargs):
        return MockCounter()
    
    def create_histogram(self, name: str, **kwargs):
        return MockHistogram()
    
    def create_gauge(self, name: str, **kwargs):
        return MockGauge()


class MockCounter:
    """Mock counter for when OpenTelemetry is not available."""
    
    def add(self, amount: Union[int, float], attributes: Optional[Dict[str, Any]] = None):
        pass


class MockHistogram:
    """Mock histogram for when OpenTelemetry is not available."""
    
    def record(self, amount: Union[int, float], attributes: Optional[Dict[str, Any]] = None):
        pass


class MockGauge:
    """Mock gauge for when OpenTelemetry is not available."""
    
    def set(self, amount: Union[int, float], attributes: Optional[Dict[str, Any]] = None):
        pass


class TelemetryManager:
    """
    Manages OpenTelemetry integration for Scribe Engine.
    
    Implements HMA v2.2 mandatory boundary telemetry requirements:
    - Traces all boundary interface calls
    - Collects performance metrics
    - Provides correlation IDs for distributed tracing
    """
    
    def __init__(self, 
                 service_name: str = "scribe-engine",
                 endpoint: Optional[str] = None,
                 sampling_rate: float = 1.0):
        """
        Initialize telemetry manager.
        
        Args:
            service_name: Name of the service for telemetry
            endpoint: OpenTelemetry collector endpoint
            sampling_rate: Trace sampling rate (0.0 to 1.0)
        """
        self.service_name = service_name
        self.endpoint = endpoint
        self.sampling_rate = sampling_rate
        self.enabled = OTEL_AVAILABLE and endpoint is not None
        
        self._lock = threading.RLock()
        self._initialized = False
        
        # Initialize telemetry components
        if self.enabled:
            self._initialize_telemetry()
        else:
            self._initialize_mock_telemetry()
        
        logger.info("TelemetryManager initialized",
                   enabled=self.enabled,
                   service_name=service_name,
                   endpoint=endpoint,
                   otel_available=OTEL_AVAILABLE)
    
    def _initialize_telemetry(self):
        """Initialize real OpenTelemetry components."""
        try:
            # Create resource
            resource = Resource.create({
                ResourceAttributes.SERVICE_NAME: self.service_name,
                ResourceAttributes.SERVICE_VERSION: "2.0.0",
                "scribe.component": "engine"
            })
            
            # Initialize tracing
            if self.endpoint:
                span_exporter = OTLPSpanExporter(endpoint=self.endpoint)
                span_processor = BatchSpanProcessor(span_exporter)
            else:
                span_processor = None
            
            tracer_provider = TracerProvider(resource=resource)
            if span_processor:
                tracer_provider.add_span_processor(span_processor)
            
            trace.set_tracer_provider(tracer_provider)
            self.tracer = trace.get_tracer(self.service_name)
            
            # Initialize metrics
            if self.endpoint:
                metric_exporter = OTLPMetricExporter(endpoint=self.endpoint)
                metric_reader = PeriodicExportingMetricReader(
                    exporter=metric_exporter,
                    export_interval_millis=10000  # 10 seconds
                )
            else:
                metric_reader = None
            
            meter_provider = MeterProvider(
                resource=resource,
                metric_readers=[metric_reader] if metric_reader else []
            )
            metrics.set_meter_provider(meter_provider)
            self.meter = metrics.get_meter(self.service_name)
            
            # Create standard metrics
            self._create_standard_metrics()
            
            # Auto-instrument common libraries
            RequestsInstrumentor().instrument()
            ThreadingInstrumentor().instrument()
            
            self._initialized = True
            logger.info("OpenTelemetry initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize OpenTelemetry",
                        error=str(e),
                        exc_info=True)
            self._initialize_mock_telemetry()
    
    def _initialize_mock_telemetry(self):
        """Initialize mock telemetry components."""
        self.tracer = MockTracer()
        self.meter = MockMeter()
        self._create_mock_metrics()
        self._initialized = True
        logger.info("Mock telemetry initialized")
    
    def _create_standard_metrics(self):
        """Create standard metrics for Scribe Engine."""
        # Counters
        self.action_executions_counter = self.meter.create_counter(
            name="scribe_action_executions_total",
            description="Total number of action executions",
            unit="1"
        )
        
        self.action_failures_counter = self.meter.create_counter(
            name="scribe_action_failures_total",
            description="Total number of action execution failures",
            unit="1"
        )
        
        self.file_events_counter = self.meter.create_counter(
            name="scribe_file_events_total", 
            description="Total number of file system events processed",
            unit="1"
        )
        
        self.boundary_calls_counter = self.meter.create_counter(
            name="scribe_boundary_calls_total",
            description="Total number of boundary interface calls",
            unit="1"
        )
        
        # Histograms
        self.action_duration_histogram = self.meter.create_histogram(
            name="scribe_action_duration_seconds",
            description="Duration of action executions",
            unit="s"
        )
        
        self.file_processing_duration_histogram = self.meter.create_histogram(
            name="scribe_file_processing_duration_seconds",
            description="Duration of file processing",
            unit="s"
        )
        
        self.boundary_call_duration_histogram = self.meter.create_histogram(
            name="scribe_boundary_call_duration_seconds",
            description="Duration of boundary interface calls",
            unit="s"
        )
        
        # Gauges
        self.active_workers_gauge = self.meter.create_gauge(
            name="scribe_active_workers",
            description="Number of active worker threads",
            unit="1"
        )
        
        self.queue_size_gauge = self.meter.create_gauge(
            name="scribe_queue_size",
            description="Current size of event queue",
            unit="1"
        )
    
    def _create_mock_metrics(self):
        """Create mock metrics."""
        self.action_executions_counter = MockCounter()
        self.action_failures_counter = MockCounter()
        self.file_events_counter = MockCounter()
        self.boundary_calls_counter = MockCounter()
        self.action_duration_histogram = MockHistogram()
        self.file_processing_duration_histogram = MockHistogram()
        self.boundary_call_duration_histogram = MockHistogram()
        self.active_workers_gauge = MockGauge()
        self.queue_size_gauge = MockGauge()
    
    @contextmanager
    def trace_boundary_call(self, 
                           interface_type: str,
                           protocol: str,
                           endpoint: str,
                           operation: str,
                           attributes: Optional[Dict[str, Any]] = None):
        """
        Trace a boundary interface call with HMA v2.2 compliance.
        
        Args:
            interface_type: Type of interface (inbound/outbound/bidirectional)
            protocol: Protocol used (http/grpc/websocket/file_system/event_bus)
            endpoint: Endpoint identifier
            operation: Operation being performed
            attributes: Additional attributes to include in the trace
        """
        span_name = f"{interface_type}_{protocol}_{operation}"
        start_time = time.time()
        
        span_attributes = {
            "scribe.boundary.interface_type": interface_type,
            "scribe.boundary.protocol": protocol,
            "scribe.boundary.endpoint": endpoint,
            "scribe.boundary.operation": operation,
            "scribe.component": "boundary"
        }
        
        if attributes:
            span_attributes.update(attributes)
        
        with self.tracer.start_as_current_span(span_name, attributes=span_attributes) as span:
            try:
                # Record boundary call metric
                self.boundary_calls_counter.add(1, {
                    "interface_type": interface_type,
                    "protocol": protocol,
                    "endpoint": endpoint,
                    "operation": operation
                })
                
                yield span
                
                # Record success
                duration = time.time() - start_time
                self.boundary_call_duration_histogram.record(duration, {
                    "interface_type": interface_type,
                    "protocol": protocol,
                    "operation": operation,
                    "status": "success"
                })
                
            except Exception as e:
                # Record failure
                duration = time.time() - start_time
                self.boundary_call_duration_histogram.record(duration, {
                    "interface_type": interface_type,
                    "protocol": protocol,
                    "operation": operation,
                    "status": "error"
                })
                
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
    
    @contextmanager
    def trace_action_execution(self, action_type: str, rule_name: str, file_path: str):
        """
        Trace action execution with performance metrics.
        
        Args:
            action_type: Type of action being executed
            rule_name: Name of the rule triggering the action
            file_path: Path of the file being processed
        """
        span_name = f"action_{action_type}"
        start_time = time.time()
        
        span_attributes = {
            "scribe.action.type": action_type,
            "scribe.rule.name": rule_name,
            "scribe.file.path": file_path,
            "scribe.component": "action"
        }
        
        with self.tracer.start_as_current_span(span_name, attributes=span_attributes) as span:
            try:
                # Record action execution metric
                self.action_executions_counter.add(1, {
                    "action_type": action_type,
                    "rule_name": rule_name
                })
                
                yield span
                
                # Record success metrics
                duration = time.time() - start_time
                self.action_duration_histogram.record(duration, {
                    "action_type": action_type,
                    "rule_name": rule_name,
                    "status": "success"
                })
                
            except Exception as e:
                # Record failure metrics
                duration = time.time() - start_time
                self.action_duration_histogram.record(duration, {
                    "action_type": action_type,
                    "rule_name": rule_name,
                    "status": "error"
                })
                
                self.action_failures_counter.add(1, {
                    "action_type": action_type,
                    "rule_name": rule_name,
                    "error_type": type(e).__name__
                })
                
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
    
    @contextmanager
    def trace_file_processing(self, file_path: str, event_type: str):
        """
        Trace file processing operations.
        
        Args:
            file_path: Path of the file being processed
            event_type: Type of file system event
        """
        span_name = f"file_processing_{event_type}"
        start_time = time.time()
        
        span_attributes = {
            "scribe.file.path": file_path,
            "scribe.file.event_type": event_type,
            "scribe.component": "file_processor"
        }
        
        with self.tracer.start_as_current_span(span_name, attributes=span_attributes) as span:
            try:
                # Record file event metric
                self.file_events_counter.add(1, {
                    "event_type": event_type
                })
                
                yield span
                
                # Record success metrics
                duration = time.time() - start_time
                self.file_processing_duration_histogram.record(duration, {
                    "event_type": event_type,
                    "status": "success"
                })
                
            except Exception as e:
                # Record failure metrics
                duration = time.time() - start_time
                self.file_processing_duration_histogram.record(duration, {
                    "event_type": event_type,
                    "status": "error"
                })
                
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
    
    def update_worker_count(self, count: int):
        """Update active worker count gauge."""
        self.active_workers_gauge.set(count)
    
    def update_queue_size(self, size: int):
        """Update event queue size gauge."""
        self.queue_size_gauge.set(size)
    
    def get_current_trace_id(self) -> Optional[str]:
        """Get current trace ID for correlation."""
        if not self.enabled:
            return None
        
        try:
            current_span = trace.get_current_span()
            if current_span:
                trace_id = current_span.get_span_context().trace_id
                return format(trace_id, '032x')
        except Exception:
            pass
        
        return None
    
    def shutdown(self):
        """Shutdown telemetry components gracefully."""
        if not self._initialized:
            return
        
        try:
            if self.enabled and OTEL_AVAILABLE:
                # Flush any pending telemetry data
                tracer_provider = trace.get_tracer_provider()
                if hasattr(tracer_provider, 'shutdown'):
                    tracer_provider.shutdown()
                
                meter_provider = metrics.get_meter_provider()
                if hasattr(meter_provider, 'shutdown'):
                    meter_provider.shutdown()
            
            logger.info("Telemetry manager shutdown completed")
            
        except Exception as e:
            logger.error("Error during telemetry shutdown",
                        error=str(e),
                        exc_info=True)


# Global telemetry manager instance
_telemetry_manager: Optional[TelemetryManager] = None
_telemetry_lock = threading.RLock()


def initialize_telemetry(service_name: str = "scribe-engine",
                        endpoint: Optional[str] = None,
                        sampling_rate: float = 1.0) -> TelemetryManager:
    """
    Initialize global telemetry manager.
    
    Args:
        service_name: Name of the service for telemetry
        endpoint: OpenTelemetry collector endpoint
        sampling_rate: Trace sampling rate (0.0 to 1.0)
        
    Returns:
        TelemetryManager instance
    """
    global _telemetry_manager
    
    with _telemetry_lock:
        if _telemetry_manager is None:
            _telemetry_manager = TelemetryManager(
                service_name=service_name,
                endpoint=endpoint,
                sampling_rate=sampling_rate
            )
        
        return _telemetry_manager


def get_telemetry_manager() -> Optional[TelemetryManager]:
    """Get the global telemetry manager instance."""
    return _telemetry_manager


def shutdown_telemetry():
    """Shutdown the global telemetry manager."""
    global _telemetry_manager
    
    with _telemetry_lock:
        if _telemetry_manager:
            _telemetry_manager.shutdown()
            _telemetry_manager = None