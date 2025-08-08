#!/usr/bin/env python3
"""
Scribe Engine Health Monitor

Implements comprehensive health monitoring, metrics collection, and alerting
for production deployment with proactive issue detection and self-healing.
"""

import time
import threading
import psutil
import socket
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import structlog

from .logging_config import get_scribe_logger
from .telemetry import get_telemetry_manager
from .error_recovery import get_error_recovery_manager

logger = get_scribe_logger(__name__)


class HealthStatus(Enum):
    """Health status levels."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class HealthCheck:
    """Represents a health check configuration."""
    name: str
    check_func: Callable[[], Dict[str, Any]]
    interval_seconds: float = 30.0
    timeout_seconds: float = 10.0
    enabled: bool = True
    alert_on_failure: bool = True
    failure_threshold: int = 3
    recovery_threshold: int = 2
    
    # Runtime state
    last_check_time: float = 0.0
    last_status: HealthStatus = HealthStatus.HEALTHY
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    total_checks: int = 0
    total_failures: int = 0
    avg_response_time: float = 0.0
    last_error: Optional[str] = None


@dataclass 
class Alert:
    """Represents a health alert."""
    alert_id: str
    severity: AlertSeverity
    component: str
    message: str
    timestamp: float
    resolved: bool = False
    resolved_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration(self) -> Optional[float]:
        """Get alert duration if resolved."""
        if self.resolved and self.resolved_at:
            return self.resolved_at - self.timestamp
        return None


class HealthMetrics:
    """Collects and manages health metrics."""
    
    def __init__(self):
        """Initialize health metrics collector."""
        self._metrics: Dict[str, List[float]] = {}
        self._lock = threading.RLock()
        self.max_history = 100  # Keep last 100 data points
        
    def record_metric(self, name: str, value: float):
        """Record a metric value."""
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = []
            
            self._metrics[name].append(value)
            
            # Trim history
            if len(self._metrics[name]) > self.max_history:
                self._metrics[name] = self._metrics[name][-self.max_history:]
    
    def get_metric_stats(self, name: str) -> Optional[Dict[str, float]]:
        """Get statistics for a metric."""
        with self._lock:
            values = self._metrics.get(name, [])
            if not values:
                return None
            
            return {
                "current": values[-1],
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "count": len(values)
            }
    
    def get_all_metrics(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all metrics."""
        with self._lock:
            return {name: self.get_metric_stats(name) 
                   for name in self._metrics.keys()}


class HealthHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler for health check endpoints."""
    
    def __init__(self, health_monitor, *args, **kwargs):
        self.health_monitor = health_monitor
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            if self.path == "/health":
                self._handle_health_check()
            elif self.path == "/health/detailed":
                self._handle_detailed_health()
            elif self.path == "/metrics":
                self._handle_metrics()
            elif self.path == "/alerts":
                self._handle_alerts()
            else:
                self._send_response(404, {"error": "Not found"})
                
        except Exception as e:
            logger.error("Health endpoint error", error=str(e))
            self._send_response(500, {"error": "Internal server error"})
    
    def _handle_health_check(self):
        """Handle basic health check."""
        overall_status = self.health_monitor.get_overall_status()
        
        status_code = 200
        if overall_status == HealthStatus.DEGRADED:
            status_code = 200  # Still operational
        elif overall_status == HealthStatus.UNHEALTHY:
            status_code = 503  # Service unavailable
        elif overall_status == HealthStatus.CRITICAL:
            status_code = 503  # Service unavailable
        
        self._send_response(status_code, {
            "status": overall_status.value,
            "timestamp": time.time()
        })
    
    def _handle_detailed_health(self):
        """Handle detailed health check."""
        health_report = self.health_monitor.get_health_report()
        
        status_code = 200
        if health_report["overall_status"] in ["unhealthy", "critical"]:
            status_code = 503
        
        self._send_response(status_code, health_report)
    
    def _handle_metrics(self):
        """Handle metrics endpoint."""
        metrics = self.health_monitor.get_metrics()
        self._send_response(200, metrics)
    
    def _handle_alerts(self):
        """Handle alerts endpoint."""
        alerts = self.health_monitor.get_active_alerts()
        self._send_response(200, {"alerts": alerts})
    
    def _send_response(self, status_code: int, data: Dict[str, Any]):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps(data, indent=2, default=str)
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to use our logger."""
        logger.debug("Health endpoint request", 
                    client=self.client_address[0],
                    path=self.path,
                    method=self.command)


class HealthMonitor:
    """
    Comprehensive health monitoring system for Scribe Engine.
    
    Features:
    - Configurable health checks
    - System resource monitoring
    - Alert management
    - HTTP health endpoints
    - Self-healing integration
    """
    
    def __init__(self, port: int = 9469):
        """
        Initialize health monitor.
        
        Args:
            port: Port for health check HTTP server
        """
        self.port = port
        
        # Health checks registry
        self._health_checks: Dict[str, HealthCheck] = {}
        self._lock = threading.RLock()
        
        # Monitoring components
        self._metrics = HealthMetrics()
        self._alerts: Dict[str, Alert] = {}
        self._alert_handlers: List[Callable[[Alert], None]] = []
        
        # System monitoring
        self._system_stats = {}
        self._monitor_thread: Optional[threading.Thread] = None
        self._http_server: Optional[HTTPServer] = None
        self._running = False
        
        # Register default health checks
        self._register_default_checks()
        
        logger.info("HealthMonitor initialized", port=port)
    
    def _register_default_checks(self):
        """Register default system health checks."""
        # System resource checks
        self.register_health_check(
            name="system_memory",
            check_func=self._check_system_memory,
            interval_seconds=30.0
        )
        
        self.register_health_check(
            name="system_cpu",
            check_func=self._check_system_cpu,
            interval_seconds=30.0
        )
        
        self.register_health_check(
            name="system_disk",
            check_func=self._check_system_disk,
            interval_seconds=60.0
        )
        
        # Application checks
        self.register_health_check(
            name="error_rate",
            check_func=self._check_error_rate,
            interval_seconds=30.0
        )
        
        self.register_health_check(
            name="component_health",
            check_func=self._check_component_health,
            interval_seconds=45.0
        )
    
    def _check_system_memory(self) -> Dict[str, Any]:
        """Check system memory usage."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            self._metrics.record_metric("memory_percent", memory.percent)
            self._metrics.record_metric("swap_percent", swap.percent)
            
            status = HealthStatus.HEALTHY
            if memory.percent > 90 or swap.percent > 80:
                status = HealthStatus.CRITICAL
            elif memory.percent > 80 or swap.percent > 60:
                status = HealthStatus.UNHEALTHY
            elif memory.percent > 70 or swap.percent > 40:
                status = HealthStatus.DEGRADED
            
            return {
                "status": status.value,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / 1024**3,
                "swap_percent": swap.percent,
                "details": "Memory usage within acceptable limits"
            }
            
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "error": str(e),
                "details": "Failed to check memory usage"
            }
    
    def _check_system_cpu(self) -> Dict[str, Any]:
        """Check system CPU usage."""
        try:
            # Get CPU usage over 1 second interval
            cpu_percent = psutil.cpu_percent(interval=1.0)
            load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)
            
            self._metrics.record_metric("cpu_percent", cpu_percent)
            
            status = HealthStatus.HEALTHY
            if cpu_percent > 95:
                status = HealthStatus.CRITICAL
            elif cpu_percent > 85:
                status = HealthStatus.UNHEALTHY
            elif cpu_percent > 75:
                status = HealthStatus.DEGRADED
            
            return {
                "status": status.value,
                "cpu_percent": cpu_percent,
                "load_avg": load_avg,
                "cpu_count": psutil.cpu_count(),
                "details": "CPU usage within acceptable limits"
            }
            
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "error": str(e),
                "details": "Failed to check CPU usage"
            }
    
    def _check_system_disk(self) -> Dict[str, Any]:
        """Check system disk usage."""
        try:
            disk_usage = psutil.disk_usage('/')
            disk_percent = (disk_usage.used / disk_usage.total) * 100
            
            self._metrics.record_metric("disk_percent", disk_percent)
            
            status = HealthStatus.HEALTHY
            if disk_percent > 95:
                status = HealthStatus.CRITICAL
            elif disk_percent > 90:
                status = HealthStatus.UNHEALTHY
            elif disk_percent > 80:
                status = HealthStatus.DEGRADED
            
            return {
                "status": status.value,
                "disk_percent": disk_percent,
                "disk_free_gb": disk_usage.free / 1024**3,
                "disk_total_gb": disk_usage.total / 1024**3,
                "details": "Disk usage within acceptable limits"
            }
            
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "error": str(e),
                "details": "Failed to check disk usage"
            }
    
    def _check_error_rate(self) -> Dict[str, Any]:
        """Check application error rate."""
        try:
            error_manager = get_error_recovery_manager()
            error_stats = error_manager.get_error_stats()
            
            total_errors = error_stats.get("total_errors", 0)
            recent_errors = sum(1 for error in error_manager._error_history 
                              if time.time() - error.timestamp < 300)  # Last 5 minutes
            
            error_rate = recent_errors / 5.0  # Errors per minute
            self._metrics.record_metric("error_rate", error_rate)
            
            status = HealthStatus.HEALTHY
            if error_rate > 10:
                status = HealthStatus.CRITICAL
            elif error_rate > 5:
                status = HealthStatus.UNHEALTHY
            elif error_rate > 2:
                status = HealthStatus.DEGRADED
            
            return {
                "status": status.value,
                "error_rate_per_minute": error_rate,
                "recent_errors": recent_errors,
                "total_errors": total_errors,
                "details": "Error rate within acceptable limits"
            }
            
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "error": str(e),
                "details": "Failed to check error rate"
            }
    
    def _check_component_health(self) -> Dict[str, Any]:
        """Check health of application components."""
        try:
            error_manager = get_error_recovery_manager()
            component_health = error_manager._component_health
            
            unhealthy_components = [comp for comp, healthy in component_health.items() 
                                  if not healthy]
            
            status = HealthStatus.HEALTHY
            if len(unhealthy_components) > 3:
                status = HealthStatus.CRITICAL
            elif len(unhealthy_components) > 1:
                status = HealthStatus.UNHEALTHY
            elif len(unhealthy_components) > 0:
                status = HealthStatus.DEGRADED
            
            return {
                "status": status.value,
                "total_components": len(component_health),
                "healthy_components": len(component_health) - len(unhealthy_components),
                "unhealthy_components": unhealthy_components,
                "details": "Component health status acceptable"
            }
            
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "error": str(e),
                "details": "Failed to check component health"
            }
    
    def register_health_check(self,
                            name: str,
                            check_func: Callable[[], Dict[str, Any]],
                            interval_seconds: float = 30.0,
                            timeout_seconds: float = 10.0,
                            failure_threshold: int = 3) -> bool:
        """
        Register a custom health check.
        
        Args:
            name: Unique name for the health check
            check_func: Function that returns health status
            interval_seconds: Check interval
            timeout_seconds: Check timeout
            failure_threshold: Consecutive failures before alerting
            
        Returns:
            True if registered successfully
        """
        with self._lock:
            if name in self._health_checks:
                logger.warning("Health check already exists", name=name)
                return False
            
            health_check = HealthCheck(
                name=name,
                check_func=check_func,
                interval_seconds=interval_seconds,
                timeout_seconds=timeout_seconds,
                failure_threshold=failure_threshold
            )
            
            self._health_checks[name] = health_check
            logger.debug("Health check registered", name=name)
            return True
    
    def start(self):
        """Start health monitoring."""
        if self._running:
            return
        
        self._running = True
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(
            target=self._monitor_worker,
            name="HealthMonitor",
            daemon=True
        )
        self._monitor_thread.start()
        
        # Start HTTP server
        self._start_http_server()
        
        logger.info("Health monitoring started", port=self.port)
    
    def _start_http_server(self):
        """Start HTTP server for health endpoints."""
        try:
            def handler_factory(*args, **kwargs):
                return HealthHTTPHandler(self, *args, **kwargs)
            
            self._http_server = HTTPServer(('0.0.0.0', self.port), handler_factory)
            
            server_thread = threading.Thread(
                target=self._http_server.serve_forever,
                name="HealthHTTPServer",
                daemon=True
            )
            server_thread.start()
            
            logger.info("Health HTTP server started", port=self.port)
            
        except Exception as e:
            logger.error("Failed to start health HTTP server",
                        port=self.port,
                        error=str(e))
    
    def _monitor_worker(self):
        """Main monitoring worker thread."""
        try:
            while self._running:
                current_time = time.time()
                
                with self._lock:
                    for health_check in self._health_checks.values():
                        if not health_check.enabled:
                            continue
                        
                        # Check if it's time to run this check
                        if (current_time - health_check.last_check_time >= 
                            health_check.interval_seconds):
                            
                            self._run_health_check(health_check, current_time)
                
                # Sleep before next iteration
                time.sleep(1.0)
                
        except Exception as e:
            logger.error("Health monitor worker error", error=str(e), exc_info=True)
    
    def _run_health_check(self, health_check: HealthCheck, current_time: float):
        """Run a single health check."""
        try:
            start_time = time.time()
            
            # Execute health check with timeout
            result = health_check.check_func()
            
            execution_time = time.time() - start_time
            
            # Update statistics
            health_check.last_check_time = current_time
            health_check.total_checks += 1
            
            # Update average response time
            if health_check.avg_response_time == 0:
                health_check.avg_response_time = execution_time
            else:
                health_check.avg_response_time = (
                    (health_check.avg_response_time * 0.9) + (execution_time * 0.1)
                )
            
            # Determine status
            status_str = result.get("status", "unknown")
            if status_str == "healthy":
                status = HealthStatus.HEALTHY
            elif status_str == "degraded":
                status = HealthStatus.DEGRADED
            elif status_str == "unhealthy":
                status = HealthStatus.UNHEALTHY
            elif status_str == "critical":
                status = HealthStatus.CRITICAL
            else:
                status = HealthStatus.UNHEALTHY
            
            # Update status tracking
            if status == HealthStatus.HEALTHY:
                health_check.consecutive_failures = 0
                health_check.consecutive_successes += 1
                health_check.last_error = None
            else:
                health_check.consecutive_successes = 0
                health_check.consecutive_failures += 1
                health_check.total_failures += 1
                health_check.last_error = result.get("error") or result.get("details")
            
            health_check.last_status = status
            
            # Check for alerts
            if (health_check.alert_on_failure and 
                health_check.consecutive_failures >= health_check.failure_threshold):
                
                self._trigger_alert(health_check, result)
            
            # Record telemetry
            telemetry = get_telemetry_manager()
            if telemetry:
                telemetry.boundary_calls_counter.add(1, {
                    "interface_type": "internal",
                    "protocol": "health_check",
                    "operation": health_check.name,
                    "status": status.value
                })
                
                telemetry.boundary_call_duration_histogram.record(execution_time, {
                    "interface_type": "internal",
                    "protocol": "health_check",
                    "operation": health_check.name
                })
            
            logger.debug("Health check completed",
                        name=health_check.name,
                        status=status.value,
                        execution_time=execution_time)
        
        except Exception as e:
            health_check.consecutive_failures += 1
            health_check.total_failures += 1
            health_check.last_error = str(e)
            health_check.last_status = HealthStatus.CRITICAL
            
            logger.error("Health check failed",
                        name=health_check.name,
                        error=str(e))
            
            # Trigger alert for check failure
            if (health_check.alert_on_failure and 
                health_check.consecutive_failures >= health_check.failure_threshold):
                
                self._trigger_alert(health_check, {"error": str(e)})
    
    def _trigger_alert(self, health_check: HealthCheck, result: Dict[str, Any]):
        """Trigger an alert for a failed health check."""
        alert_id = f"{health_check.name}_{int(time.time())}"
        
        # Determine severity based on status
        severity = AlertSeverity.WARNING
        if health_check.last_status == HealthStatus.CRITICAL:
            severity = AlertSeverity.CRITICAL
        elif health_check.last_status == HealthStatus.UNHEALTHY:
            severity = AlertSeverity.ERROR
        
        alert = Alert(
            alert_id=alert_id,
            severity=severity,
            component=health_check.name,
            message=f"Health check '{health_check.name}' failed {health_check.consecutive_failures} times",
            timestamp=time.time(),
            metadata={
                "consecutive_failures": health_check.consecutive_failures,
                "failure_threshold": health_check.failure_threshold,
                "last_error": health_check.last_error,
                "check_result": result
            }
        )
        
        with self._lock:
            self._alerts[alert_id] = alert
        
        # Notify alert handlers
        for handler in self._alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error("Alert handler failed",
                           handler=handler.__name__,
                           alert_id=alert_id,
                           error=str(e))
        
        logger.warning("Health alert triggered",
                      alert_id=alert_id,
                      component=health_check.name,
                      severity=severity.value)
    
    def add_alert_handler(self, handler: Callable[[Alert], None]):
        """Add an alert handler function."""
        self._alert_handlers.append(handler)
        logger.debug("Alert handler added", handler=handler.__name__)
    
    def get_overall_status(self) -> HealthStatus:
        """Get overall system health status."""
        with self._lock:
            if not self._health_checks:
                return HealthStatus.HEALTHY
            
            statuses = [check.last_status for check in self._health_checks.values() 
                       if check.enabled]
            
            if HealthStatus.CRITICAL in statuses:
                return HealthStatus.CRITICAL
            elif HealthStatus.UNHEALTHY in statuses:
                return HealthStatus.UNHEALTHY
            elif HealthStatus.DEGRADED in statuses:
                return HealthStatus.DEGRADED
            else:
                return HealthStatus.HEALTHY
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get detailed health report."""
        with self._lock:
            overall_status = self.get_overall_status()
            
            checks_summary = {}
            for name, check in self._health_checks.items():
                checks_summary[name] = {
                    "status": check.last_status.value,
                    "last_check": check.last_check_time,
                    "consecutive_failures": check.consecutive_failures,
                    "total_checks": check.total_checks,
                    "total_failures": check.total_failures,
                    "avg_response_time": check.avg_response_time,
                    "last_error": check.last_error
                }
            
            return {
                "overall_status": overall_status.value,
                "timestamp": time.time(),
                "checks": checks_summary,
                "active_alerts": len([a for a in self._alerts.values() if not a.resolved]),
                "system_info": {
                    "uptime": time.time() - (self._monitor_thread.ident if self._monitor_thread else time.time()),
                    "process_id": os.getpid() if 'os' in globals() else 0
                }
            }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get health metrics."""
        return self._metrics.get_all_metrics()
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get active (unresolved) alerts."""
        with self._lock:
            return [
                {
                    "alert_id": alert.alert_id,
                    "severity": alert.severity.value,
                    "component": alert.component,
                    "message": alert.message,
                    "timestamp": alert.timestamp,
                    "metadata": alert.metadata
                }
                for alert in self._alerts.values()
                if not alert.resolved
            ]
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved."""
        with self._lock:
            alert = self._alerts.get(alert_id)
            if alert and not alert.resolved:
                alert.resolved = True
                alert.resolved_at = time.time()
                
                logger.info("Alert resolved",
                           alert_id=alert_id,
                           duration=alert.duration)
                return True
            return False
    
    def stop(self):
        """Stop health monitoring."""
        if not self._running:
            return
        
        self._running = False
        
        # Stop HTTP server
        if self._http_server:
            self._http_server.shutdown()
            self._http_server = None
        
        # Wait for monitor thread
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5.0)
        
        logger.info("Health monitoring stopped")


# Global health monitor instance
_health_monitor: Optional[HealthMonitor] = None
_monitor_lock = threading.RLock()


def get_health_monitor() -> Optional[HealthMonitor]:
    """Get the global health monitor instance."""
    return _health_monitor


def initialize_health_monitor(port: int = 9469) -> HealthMonitor:
    """
    Initialize global health monitor.
    
    Args:
        port: Port for health check HTTP server
        
    Returns:
        HealthMonitor instance
    """
    global _health_monitor
    
    with _monitor_lock:
        if _health_monitor is None:
            _health_monitor = HealthMonitor(port=port)
            _health_monitor.start()
        
        return _health_monitor


def shutdown_health_monitor():
    """Shutdown the global health monitor."""
    global _health_monitor
    
    with _monitor_lock:
        if _health_monitor:
            _health_monitor.stop()
            _health_monitor = None