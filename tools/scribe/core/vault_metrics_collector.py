#!/usr/bin/env python3
"""
Scribe Vault Metrics Collector

Enterprise-grade Prometheus metrics collection for HashiCorp Vault operations
implementing comprehensive observability for HMA v2.2 compliance.
"""

import time
import threading
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import structlog

# Prometheus and OpenTelemetry imports
from prometheus_client import Counter, Histogram, Gauge, Info, Enum as PrometheusEnum
from opentelemetry import trace, metrics
from opentelemetry.trace import Status, StatusCode
from opentelemetry.metrics import get_meter

from .logging_config import get_scribe_logger
from .vault_otlp_integration import get_vault_otlp_integration, create_vault_span, record_vault_metric

logger = get_scribe_logger(__name__)


class MetricType(Enum):
    """Types of metrics collected."""
    COUNTER = "counter"
    HISTOGRAM = "histogram"
    GAUGE = "gauge"
    INFO = "info"


class OperationStatus(Enum):
    """Operation status for metrics labeling."""
    SUCCESS = "success"
    FAILURE = "failure"
    DEGRADED = "degraded"
    TIMEOUT = "timeout"
    CIRCUIT_OPEN = "circuit_open"


@dataclass
class MetricDefinition:
    """Definition for a Vault metric."""
    name: str
    description: str
    metric_type: MetricType
    labels: List[str] = field(default_factory=list)
    buckets: Optional[List[float]] = None


class VaultMetricsCollector:
    """
    Professional Vault metrics collector with Prometheus and OpenTelemetry integration.
    
    Provides comprehensive metrics collection for all Vault operations including
    authentication, secret retrieval, certificate generation, and policy management.
    """
    
    def __init__(self, namespace: str = "scribe_vault"):
        """
        Initialize metrics collector.
        
        Args:
            namespace: Metric namespace prefix
        """
        self.namespace = namespace
        self._lock = threading.RLock()
        
        # Initialize OTLP integration
        self._otlp_integration = get_vault_otlp_integration()
        
        # OpenTelemetry components
        self._tracer = self._otlp_integration.get_tracer("vault.metrics.collector")
        self._meter = self._otlp_integration.get_meter("vault.metrics.collector")
        
        # Prometheus metrics registry
        self._prometheus_metrics: Dict[str, Any] = {}
        self._otel_metrics: Dict[str, Any] = {}
        
        # Operation tracking - REDUCED to prevent memory leaks
        self._active_operations: Dict[str, float] = {}
        self._operation_history: List[Dict[str, Any]] = []
        self._max_history_size = 50  # REDUCED from 1000 to prevent crashes
        
        # Initialize metric definitions
        self._metric_definitions = self._initialize_metric_definitions()
        
        # Create Prometheus metrics
        self._create_prometheus_metrics()
        
        # Create OpenTelemetry metrics
        self._create_otel_metrics()
        
        logger.info("Vault metrics collector initialized with OTLP integration",
                   namespace=namespace,
                   prometheus_metrics=len(self._prometheus_metrics),
                   otel_metrics=len(self._otel_metrics),
                   otlp_enabled=True)
    
    def _initialize_metric_definitions(self) -> Dict[str, MetricDefinition]:
        """Initialize metric definitions for all Vault operations."""
        return {
            # Authentication metrics
            "auth_attempts_total": MetricDefinition(
                name="auth_attempts_total",
                description="Total number of Vault authentication attempts",
                metric_type=MetricType.COUNTER,
                labels=["auth_method", "status"]
            ),
            
            "auth_duration_seconds": MetricDefinition(
                name="auth_duration_seconds",
                description="Time spent on Vault authentication operations",
                metric_type=MetricType.HISTOGRAM,
                labels=["auth_method", "status"],
                buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
            ),
            
            # Secret operations metrics
            "secret_operations_total": MetricDefinition(
                name="secret_operations_total",
                description="Total number of secret operations",
                metric_type=MetricType.COUNTER,
                labels=["operation", "mount_point", "status"]
            ),
            
            "secret_operation_duration_seconds": MetricDefinition(
                name="secret_operation_duration_seconds",
                description="Time spent on secret operations",
                metric_type=MetricType.HISTOGRAM,
                labels=["operation", "mount_point", "status"],
                buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
            ),
            
            "secret_cache_size": MetricDefinition(
                name="secret_cache_size",
                description="Number of secrets currently cached",
                metric_type=MetricType.GAUGE,
                labels=["cache_type"]
            ),
            
            "secret_cache_hit_ratio": MetricDefinition(
                name="secret_cache_hit_ratio",
                description="Ratio of cache hits to total requests",
                metric_type=MetricType.GAUGE,
                labels=["cache_type"]
            ),
            
            # Certificate operations metrics
            "certificate_operations_total": MetricDefinition(
                name="certificate_operations_total",
                description="Total number of certificate operations",
                metric_type=MetricType.COUNTER,
                labels=["operation", "common_name", "status"]
            ),
            
            "certificate_generation_duration_seconds": MetricDefinition(
                name="certificate_generation_duration_seconds",
                description="Time spent generating certificates",
                metric_type=MetricType.HISTOGRAM,
                labels=["common_name", "status"],
                buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0]
            ),
            
            "certificate_expiry_seconds": MetricDefinition(
                name="certificate_expiry_seconds",
                description="Time until certificate expiry",
                metric_type=MetricType.GAUGE,
                labels=["common_name", "serial_number"]
            ),
            
            # Circuit breaker metrics
            "circuit_breaker_state": MetricDefinition(
                name="circuit_breaker_state",
                description="Current state of circuit breakers",
                metric_type=MetricType.GAUGE,
                labels=["operation", "state"]
            ),
            
            "circuit_breaker_trips_total": MetricDefinition(
                name="circuit_breaker_trips_total",
                description="Total number of circuit breaker trips",
                metric_type=MetricType.COUNTER,
                labels=["operation", "reason"]
            ),
            
            # Retry metrics
            "retry_attempts_total": MetricDefinition(
                name="retry_attempts_total",
                description="Total number of retry attempts",
                metric_type=MetricType.COUNTER,
                labels=["operation", "attempt_number", "final_status"]
            ),
            
            "retry_backoff_duration_seconds": MetricDefinition(
                name="retry_backoff_duration_seconds",
                description="Time spent in retry backoff",
                metric_type=MetricType.HISTOGRAM,
                labels=["operation"],
                buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
            ),
            
            # Rotation metrics
            "rotation_operations_total": MetricDefinition(
                name="rotation_operations_total",
                description="Total number of secret rotation operations",
                metric_type=MetricType.COUNTER,
                labels=["rotation_type", "job_id", "status", "trigger"]
            ),
            
            "rotation_duration_seconds": MetricDefinition(
                name="rotation_duration_seconds",
                description="Time spent on rotation operations",
                metric_type=MetricType.HISTOGRAM,
                labels=["rotation_type", "status"],
                buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 300.0, 600.0]
            ),
            
            "rotation_queue_size": MetricDefinition(
                name="rotation_queue_size",
                description="Number of pending rotation operations",
                metric_type=MetricType.GAUGE,
                labels=["queue_type"]
            ),
            
            # Policy metrics
            "policy_operations_total": MetricDefinition(
                name="policy_operations_total",
                description="Total number of policy operations",
                metric_type=MetricType.COUNTER,
                labels=["operation", "policy_name", "status"]
            ),
            
            "approle_operations_total": MetricDefinition(
                name="approle_operations_total",
                description="Total number of AppRole operations",
                metric_type=MetricType.COUNTER,
                labels=["operation", "role_name", "status"]
            ),
            
            # Health and connectivity metrics
            "vault_connectivity": MetricDefinition(
                name="vault_connectivity",
                description="Vault server connectivity status",
                metric_type=MetricType.GAUGE,
                labels=["vault_url", "status"]
            ),
            
            "vault_response_time_seconds": MetricDefinition(
                name="vault_response_time_seconds",
                description="Vault server response time",
                metric_type=MetricType.HISTOGRAM,
                labels=["operation", "status"],
                buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
            ),
            
            # Service mode metrics
            "service_mode": MetricDefinition(
                name="service_mode",
                description="Current service operation mode",
                metric_type=MetricType.GAUGE,
                labels=["mode"]
            ),
            
            "degradation_events_total": MetricDefinition(
                name="degradation_events_total",
                description="Total number of service degradation events",
                metric_type=MetricType.COUNTER,
                labels=["reason", "severity"]
            )
        }
    
    def _create_prometheus_metrics(self):
        """Create Prometheus metrics based on definitions."""
        for name, definition in self._metric_definitions.items():
            full_name = f"{self.namespace}_{name}"
            
            if definition.metric_type == MetricType.COUNTER:
                metric = Counter(
                    full_name,
                    definition.description,
                    labelnames=definition.labels
                )
            elif definition.metric_type == MetricType.HISTOGRAM:
                metric = Histogram(
                    full_name,
                    definition.description,
                    labelnames=definition.labels,
                    buckets=definition.buckets or Histogram.DEFAULT_BUCKETS
                )
            elif definition.metric_type == MetricType.GAUGE:
                metric = Gauge(
                    full_name,
                    definition.description,
                    labelnames=definition.labels
                )
            elif definition.metric_type == MetricType.INFO:
                metric = Info(
                    full_name,
                    definition.description,
                    labelnames=definition.labels
                )
            else:
                continue
            
            self._prometheus_metrics[name] = metric
    
    def _create_otel_metrics(self):
        """Create OpenTelemetry metrics based on definitions."""
        for name, definition in self._metric_definitions.items():
            full_name = f"{self.namespace}.{name}"
            
            if definition.metric_type == MetricType.COUNTER:
                metric = self._meter.create_counter(
                    name=full_name,
                    description=definition.description,
                    unit="1"
                )
            elif definition.metric_type == MetricType.HISTOGRAM:
                metric = self._meter.create_histogram(
                    name=full_name,
                    description=definition.description,
                    unit="s" if "seconds" in name else "1"
                )
            elif definition.metric_type == MetricType.GAUGE:
                # OpenTelemetry uses up_down_counter for gauge-like behavior
                metric = self._meter.create_up_down_counter(
                    name=full_name,
                    description=definition.description,
                    unit="1"
                )
            else:
                continue
            
            self._otel_metrics[name] = metric
    
    def start_operation(self, operation_id: str, operation_type: str, **labels) -> str:
        """
        Start tracking an operation.
        
        Args:
            operation_id: Unique operation identifier
            operation_type: Type of operation
            **labels: Additional labels for the operation
            
        Returns:
            Span context for distributed tracing
        """
        with self._lock:
            self._active_operations[operation_id] = time.time()
        
        # Start OpenTelemetry span with OTLP integration
        span = create_vault_span(
            name=f"vault.{operation_type}",
            operation_id=operation_id,
            operation_type=operation_type,
            collector_namespace=self.namespace,
            **labels
        )
        
        # Record operation start metric through OTLP
        record_vault_metric(
            name=f"{self.namespace}_operation_started_total",
            value=1,
            unit="1",
            operation_type=operation_type,
            operation_id=operation_id,
            **labels
        )
        
        logger.debug("Started operation tracking with OTLP integration",
                    operation_id=operation_id,
                    operation_type=operation_type,
                    **labels)
        
        return span
    
    def end_operation(self, operation_id: str, span, status: OperationStatus, **metrics):
        """
        End operation tracking and record metrics.
        
        Args:
            operation_id: Operation identifier
            span: OpenTelemetry span
            status: Operation status
            **metrics: Additional metrics to record
        """
        duration = None
        
        with self._lock:
            start_time = self._active_operations.pop(operation_id, None)
            if start_time:
                duration = time.time() - start_time
        
        # Update span
        if span:
            span.set_attribute("vault.operation.duration", duration or 0)
            span.set_attribute("vault.operation.status", status.value)
            
            if status == OperationStatus.SUCCESS:
                span.set_status(Status(StatusCode.OK))
            else:
                span.set_status(Status(StatusCode.ERROR, description=f"Operation {status.value}"))
            
            span.end()
        
        # Record operation completion metrics through OTLP
        if duration:
            record_vault_metric(
                name=f"{self.namespace}_operation_duration_seconds",
                value=duration,
                unit="s",
                operation_id=operation_id,
                status=status.value,
                **metrics
            )
        
        record_vault_metric(
            name=f"{self.namespace}_operation_completed_total",
            value=1,
            unit="1",
            operation_id=operation_id,
            status=status.value,
            **metrics
        )
        
        # Record operation in history
        operation_record = {
            "operation_id": operation_id,
            "status": status.value,
            "duration": duration,
            "timestamp": time.time(),
            **metrics
        }
        
        self._record_operation_history(operation_record)
        
        # DISABLED: OTLP integration to reduce resource usage
        # self._otlp_integration.record_vault_operation(
        #     operation=operation_id.split('_')[0],  # Extract operation type
        #     duration=duration or 0,
        #     status=status.value,
        #     **metrics
        # )
        
        logger.debug("Ended operation tracking with OTLP integration",
                    operation_id=operation_id,
                    status=status.value,
                    duration=duration)
    
    def record_auth_attempt(self, auth_method: str, status: OperationStatus, duration: float):
        """Record authentication attempt metrics."""
        labels = {"auth_method": auth_method, "status": status.value}
        
        # Prometheus metrics
        if "auth_attempts_total" in self._prometheus_metrics:
            self._prometheus_metrics["auth_attempts_total"].labels(**labels).inc()
        
        if "auth_duration_seconds" in self._prometheus_metrics:
            self._prometheus_metrics["auth_duration_seconds"].labels(**labels).observe(duration)
        
        # DISABLED: OpenTelemetry metrics to reduce overhead
        # if "auth_attempts_total" in self._otel_metrics:
        #     self._otel_metrics["auth_attempts_total"].add(1, labels)
        # 
        # if "auth_duration_seconds" in self._otel_metrics:
        #     self._otel_metrics["auth_duration_seconds"].record(duration, labels)
    
    def record_secret_operation(self, operation: str, mount_point: str, 
                              status: OperationStatus, duration: float):
        """Record secret operation metrics."""
        labels = {
            "operation": operation,
            "mount_point": mount_point,
            "status": status.value
        }
        
        # Prometheus metrics
        if "secret_operations_total" in self._prometheus_metrics:
            self._prometheus_metrics["secret_operations_total"].labels(**labels).inc()
        
        if "secret_operation_duration_seconds" in self._prometheus_metrics:
            self._prometheus_metrics["secret_operation_duration_seconds"].labels(**labels).observe(duration)
        
        # DISABLED: OpenTelemetry metrics to reduce overhead
        # if "secret_operations_total" in self._otel_metrics:
        #     self._otel_metrics["secret_operations_total"].add(1, labels)
        # 
        # if "secret_operation_duration_seconds" in self._otel_metrics:
        #     self._otel_metrics["secret_operation_duration_seconds"].record(duration, labels)
    
    def record_certificate_operation(self, operation: str, common_name: str,
                                   status: OperationStatus, duration: float = None,
                                   serial_number: str = None, expiry_seconds: int = None):
        """Record certificate operation metrics."""
        labels = {
            "operation": operation,
            "common_name": common_name,
            "status": status.value
        }
        
        # Prometheus metrics
        if "certificate_operations_total" in self._prometheus_metrics:
            self._prometheus_metrics["certificate_operations_total"].labels(**labels).inc()
        
        if duration and "certificate_generation_duration_seconds" in self._prometheus_metrics:
            cert_labels = {"common_name": common_name, "status": status.value}
            self._prometheus_metrics["certificate_generation_duration_seconds"].labels(**cert_labels).observe(duration)
        
        if expiry_seconds and serial_number and "certificate_expiry_seconds" in self._prometheus_metrics:
            expiry_labels = {"common_name": common_name, "serial_number": serial_number}
            self._prometheus_metrics["certificate_expiry_seconds"].labels(**expiry_labels).set(expiry_seconds)
        
        # DISABLED: OpenTelemetry metrics to reduce overhead
        # if "certificate_operations_total" in self._otel_metrics:
        #     self._otel_metrics["certificate_operations_total"].add(1, labels)
    
    def record_circuit_breaker_state(self, operation: str, state: str):
        """Record circuit breaker state."""
        labels = {"operation": operation, "state": state}
        
        if "circuit_breaker_state" in self._prometheus_metrics:
            # Reset all states to 0, then set current state to 1
            for possible_state in ["closed", "open", "half_open"]:
                state_labels = {"operation": operation, "state": possible_state}
                value = 1 if possible_state == state else 0
                self._prometheus_metrics["circuit_breaker_state"].labels(**state_labels).set(value)
    
    def record_circuit_breaker_trip(self, operation: str, reason: str):
        """Record circuit breaker trip."""
        labels = {"operation": operation, "reason": reason}
        
        if "circuit_breaker_trips_total" in self._prometheus_metrics:
            self._prometheus_metrics["circuit_breaker_trips_total"].labels(**labels).inc()
        
        # DISABLED: OpenTelemetry metrics to reduce overhead
        # if "circuit_breaker_trips_total" in self._otel_metrics:
        #     self._otel_metrics["circuit_breaker_trips_total"].add(1, labels)
    
    def record_retry_attempt(self, operation: str, attempt_number: int, 
                           final_status: OperationStatus, backoff_duration: float = None):
        """Record retry attempt metrics."""
        labels = {
            "operation": operation,
            "attempt_number": str(attempt_number),
            "final_status": final_status.value
        }
        
        if "retry_attempts_total" in self._prometheus_metrics:
            self._prometheus_metrics["retry_attempts_total"].labels(**labels).inc()
        
        if backoff_duration and "retry_backoff_duration_seconds" in self._prometheus_metrics:
            backoff_labels = {"operation": operation}
            self._prometheus_metrics["retry_backoff_duration_seconds"].labels(**backoff_labels).observe(backoff_duration)
    
    def record_rotation_operation(self, rotation_type: str, job_id: str, 
                                status: OperationStatus, trigger: str, duration: float = None):
        """Record rotation operation metrics."""
        labels = {
            "rotation_type": rotation_type,
            "job_id": job_id,
            "status": status.value,
            "trigger": trigger
        }
        
        if "rotation_operations_total" in self._prometheus_metrics:
            self._prometheus_metrics["rotation_operations_total"].labels(**labels).inc()
        
        if duration and "rotation_duration_seconds" in self._prometheus_metrics:
            duration_labels = {"rotation_type": rotation_type, "status": status.value}
            self._prometheus_metrics["rotation_duration_seconds"].labels(**duration_labels).observe(duration)
    
    def update_cache_metrics(self, cache_type: str, cache_size: int, hit_ratio: float):
        """Update cache-related metrics."""
        if "secret_cache_size" in self._prometheus_metrics:
            self._prometheus_metrics["secret_cache_size"].labels(cache_type=cache_type).set(cache_size)
        
        if "secret_cache_hit_ratio" in self._prometheus_metrics:
            self._prometheus_metrics["secret_cache_hit_ratio"].labels(cache_type=cache_type).set(hit_ratio)
    
    def update_service_mode(self, mode: str):
        """Update service mode metric."""
        if "service_mode" in self._prometheus_metrics:
            # Reset all modes to 0, then set current mode to 1
            for possible_mode in ["normal", "degraded", "emergency"]:
                value = 1 if possible_mode == mode else 0
                self._prometheus_metrics["service_mode"].labels(mode=possible_mode).set(value)
    
    def record_degradation_event(self, reason: str, severity: str):
        """Record service degradation event."""
        labels = {"reason": reason, "severity": severity}
        
        if "degradation_events_total" in self._prometheus_metrics:
            self._prometheus_metrics["degradation_events_total"].labels(**labels).inc()
    
    def update_vault_connectivity(self, vault_url: str, is_connected: bool, response_time: float = None):
        """Update Vault connectivity metrics."""
        status = "connected" if is_connected else "disconnected"
        
        if "vault_connectivity" in self._prometheus_metrics:
            connectivity_value = 1 if is_connected else 0
            self._prometheus_metrics["vault_connectivity"].labels(vault_url=vault_url, status=status).set(connectivity_value)
        
        if response_time and "vault_response_time_seconds" in self._prometheus_metrics:
            response_labels = {"operation": "health_check", "status": status}
            self._prometheus_metrics["vault_response_time_seconds"].labels(**response_labels).observe(response_time)
    
    def _record_operation_history(self, operation_record: Dict[str, Any]):
        """Record operation in history for analysis - MINIMAL to prevent leaks."""
        with self._lock:
            # Only keep essential data to prevent memory explosion
            minimal_record = {
                "status": operation_record.get("status", "unknown"),
                "duration": operation_record.get("duration", 0),
                "timestamp": operation_record.get("timestamp", time.time())
            }
            self._operation_history.append(minimal_record)
            
            # Aggressive cleanup to prevent memory leaks
            if len(self._operation_history) > self._max_history_size:
                # Remove oldest 10 entries when limit is exceeded
                self._operation_history = self._operation_history[10:]
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        with self._lock:
            recent_operations = [
                op for op in self._operation_history 
                if time.time() - op["timestamp"] < 3600  # Last hour
            ]
            
            success_count = len([op for op in recent_operations if op["status"] == "success"])
            total_count = len(recent_operations)
            
            return {
                "active_operations": len(self._active_operations),
                "recent_operations": total_count,
                "success_rate": success_count / max(total_count, 1),
                "prometheus_metrics": len(self._prometheus_metrics),
                "otel_metrics": len(self._otel_metrics),
                "operation_history_size": len(self._operation_history)
            }
    
    def reset_metrics(self):
        """Reset all metrics (for testing purposes)."""
        with self._lock:
            self._active_operations.clear()
            self._operation_history.clear()
        
        logger.info("Vault metrics reset")


# Global metrics collector instance
_metrics_collector: Optional[VaultMetricsCollector] = None
_collector_lock = threading.RLock()


def get_vault_metrics_collector() -> VaultMetricsCollector:
    """Get or create global Vault metrics collector."""
    global _metrics_collector
    
    with _collector_lock:
        if _metrics_collector is None:
            _metrics_collector = VaultMetricsCollector()
        
        return _metrics_collector


def initialize_vault_metrics(namespace: str = "scribe_vault") -> VaultMetricsCollector:
    """
    Initialize global Vault metrics collector.
    
    Args:
        namespace: Metric namespace prefix
        
    Returns:
        Initialized metrics collector
    """
    global _metrics_collector
    
    with _collector_lock:
        _metrics_collector = VaultMetricsCollector(namespace)
        logger.info("Global Vault metrics collector initialized")
        return _metrics_collector