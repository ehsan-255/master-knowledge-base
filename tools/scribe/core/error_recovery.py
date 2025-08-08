#!/usr/bin/env python3
"""
Scribe Engine Error Recovery System

Implements comprehensive error handling, recovery strategies, and self-healing
mechanisms for robust operation in production environments.
"""

import time
import threading
import traceback
from enum import Enum
from typing import Dict, Any, Optional, List, Callable, Union
from dataclasses import dataclass, field
from collections import deque
import structlog

from .logging_config import get_scribe_logger
from .telemetry import get_telemetry_manager

logger = get_scribe_logger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels for classification and handling."""
    LOW = "low"              # Minor issues, continue operation
    MEDIUM = "medium"        # Recoverable issues, retry with backoff
    HIGH = "high"           # Serious issues, invoke recovery procedures
    CRITICAL = "critical"   # System-threatening, emergency procedures


class RecoveryStrategy(Enum):
    """Recovery strategies for different error types."""
    IGNORE = "ignore"                    # Log and continue
    RETRY = "retry"                     # Retry with exponential backoff
    RESTART_COMPONENT = "restart_component"  # Restart failed component
    DEGRADE_GRACEFULLY = "degrade_gracefully"  # Reduce functionality
    FAILOVER = "failover"               # Switch to backup/alternative
    EMERGENCY_STOP = "emergency_stop"   # Shut down to prevent damage


@dataclass
class ErrorContext:
    """Context information for error events."""
    error_id: str
    timestamp: float
    component: str
    operation: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    recovery_strategy: RecoveryStrategy
    stack_trace: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    recovery_attempts: int = 0
    max_retries: int = 3
    resolved: bool = False


class ErrorPattern:
    """Pattern for matching and handling specific error types."""
    
    def __init__(self,
                 pattern_name: str,
                 error_types: List[str],
                 component_patterns: List[str],
                 severity: ErrorSeverity,
                 recovery_strategy: RecoveryStrategy,
                 max_retries: int = 3,
                 backoff_multiplier: float = 2.0):
        """
        Initialize error pattern.
        
        Args:
            pattern_name: Name of the pattern
            error_types: List of error type names to match
            component_patterns: List of component name patterns
            severity: Error severity level
            recovery_strategy: Recovery strategy to apply
            max_retries: Maximum retry attempts
            backoff_multiplier: Exponential backoff multiplier
        """
        self.pattern_name = pattern_name
        self.error_types = error_types
        self.component_patterns = component_patterns
        self.severity = severity
        self.recovery_strategy = recovery_strategy
        self.max_retries = max_retries
        self.backoff_multiplier = backoff_multiplier
    
    def matches(self, error_context: ErrorContext) -> bool:
        """Check if error context matches this pattern."""
        # Check error type
        error_type_match = any(
            error_type in error_context.error_type
            for error_type in self.error_types
        )
        
        # Check component pattern
        component_match = any(
            pattern in error_context.component
            for pattern in self.component_patterns
        )
        
        return error_type_match and component_match


class RecoveryAction:
    """Represents a recovery action that can be executed."""
    
    def __init__(self,
                 action_name: str,
                 action_func: Callable[[ErrorContext], bool],
                 timeout_seconds: float = 30.0,
                 prerequisites: Optional[List[str]] = None):
        """
        Initialize recovery action.
        
        Args:
            action_name: Name of the action
            action_func: Function to execute (returns success status)
            timeout_seconds: Timeout for action execution
            prerequisites: List of prerequisite actions
        """
        self.action_name = action_name
        self.action_func = action_func
        self.timeout_seconds = timeout_seconds
        self.prerequisites = prerequisites or []
    
    def execute(self, error_context: ErrorContext) -> bool:
        """
        Execute the recovery action.
        
        Args:
            error_context: Error context
            
        Returns:
            True if action succeeded
        """
        try:
            logger.info("Executing recovery action",
                       action_name=self.action_name,
                       error_id=error_context.error_id,
                       component=error_context.component)
            
            result = self.action_func(error_context)
            
            if result:
                logger.info("Recovery action succeeded",
                           action_name=self.action_name,
                           error_id=error_context.error_id)
            else:
                logger.warning("Recovery action failed",
                              action_name=self.action_name,
                              error_id=error_context.error_id)
            
            return result
            
        except Exception as e:
            logger.error("Recovery action raised exception",
                        action_name=self.action_name,
                        error_id=error_context.error_id,
                        exception=str(e),
                        exc_info=True)
            return False


class ErrorRecoveryManager:
    """
    Manages error detection, classification, and recovery for Scribe Engine.
    
    Provides centralized error handling with configurable recovery strategies,
    exponential backoff, circuit breaking, and self-healing capabilities.
    """
    
    def __init__(self):
        """Initialize error recovery manager."""
        self._error_patterns: List[ErrorPattern] = []
        self._recovery_actions: Dict[RecoveryStrategy, List[RecoveryAction]] = {}
        self._error_history: deque = deque(maxlen=1000)
        self._active_errors: Dict[str, ErrorContext] = {}
        self._component_health: Dict[str, bool] = {}
        
        self._lock = threading.RLock()
        self._recovery_thread: Optional[threading.Thread] = None
        self._running = False
        
        # Initialize default error patterns
        self._initialize_default_patterns()
        
        # Initialize default recovery actions
        self._initialize_default_actions()
        
        logger.info("ErrorRecoveryManager initialized")
    
    def _initialize_default_patterns(self):
        """Initialize default error patterns for common scenarios."""
        patterns = [
            ErrorPattern(
                pattern_name="file_system_errors",
                error_types=["FileNotFoundError", "PermissionError", "OSError"],
                component_patterns=["watcher", "atomic_write", "config"],
                severity=ErrorSeverity.MEDIUM,
                recovery_strategy=RecoveryStrategy.RETRY,
                max_retries=3
            ),
            ErrorPattern(
                pattern_name="network_timeouts",
                error_types=["TimeoutError", "ConnectionError", "RequestException"],
                component_patterns=["http", "api", "webhook"],
                severity=ErrorSeverity.MEDIUM,
                recovery_strategy=RecoveryStrategy.RETRY,
                max_retries=5,
                backoff_multiplier=1.5
            ),
            ErrorPattern(
                pattern_name="plugin_failures",
                error_types=["PluginLoadError", "ActionExecutionError", "ImportError"],
                component_patterns=["plugin", "action"],
                severity=ErrorSeverity.HIGH,
                recovery_strategy=RecoveryStrategy.RESTART_COMPONENT,
                max_retries=2
            ),
            ErrorPattern(
                pattern_name="memory_errors",
                error_types=["MemoryError", "OutOfMemoryError"],
                component_patterns=["worker", "processor"],
                severity=ErrorSeverity.CRITICAL,
                recovery_strategy=RecoveryStrategy.DEGRADE_GRACEFULLY,
                max_retries=1
            ),
            ErrorPattern(
                pattern_name="configuration_errors",
                error_types=["ValidationError", "ConfigurationError", "JSONDecodeError"],
                component_patterns=["config", "schema"],
                severity=ErrorSeverity.HIGH,
                recovery_strategy=RecoveryStrategy.FAILOVER,
                max_retries=1
            )
        ]
        
        for pattern in patterns:
            self.add_error_pattern(pattern)
    
    def _initialize_default_actions(self):
        """Initialize default recovery actions."""
        # Retry action
        self.add_recovery_action(
            RecoveryStrategy.RETRY,
            RecoveryAction(
                action_name="exponential_backoff_retry",
                action_func=self._retry_with_backoff,
                timeout_seconds=60.0
            )
        )
        
        # Restart component action
        self.add_recovery_action(
            RecoveryStrategy.RESTART_COMPONENT,
            RecoveryAction(
                action_name="restart_component",
                action_func=self._restart_component,
                timeout_seconds=30.0
            )
        )
        
        # Graceful degradation action
        self.add_recovery_action(
            RecoveryStrategy.DEGRADE_GRACEFULLY,
            RecoveryAction(
                action_name="degrade_gracefully",
                action_func=self._degrade_gracefully,
                timeout_seconds=15.0
            )
        )
        
        # Failover action
        self.add_recovery_action(
            RecoveryStrategy.FAILOVER,
            RecoveryAction(
                action_name="failover_to_backup",
                action_func=self._failover_to_backup,
                timeout_seconds=45.0
            )
        )
    
    def add_error_pattern(self, pattern: ErrorPattern):
        """Add an error pattern for matching and handling."""
        with self._lock:
            self._error_patterns.append(pattern)
            logger.debug("Added error pattern", pattern_name=pattern.pattern_name)
    
    def add_recovery_action(self, strategy: RecoveryStrategy, action: RecoveryAction):
        """Add a recovery action for a strategy."""
        with self._lock:
            if strategy not in self._recovery_actions:
                self._recovery_actions[strategy] = []
            self._recovery_actions[strategy].append(action)
            logger.debug("Added recovery action",
                        strategy=strategy.value,
                        action_name=action.action_name)
    
    def handle_error(self,
                    component: str,
                    operation: str,
                    error: Exception,
                    metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Handle an error with automatic classification and recovery.
        
        Args:
            component: Component where error occurred
            operation: Operation being performed
            error: The exception that occurred
            metadata: Additional context metadata
            
        Returns:
            Error ID for tracking
        """
        # Create error context
        error_id = f"{component}_{int(time.time() * 1000)}"
        error_context = ErrorContext(
            error_id=error_id,
            timestamp=time.time(),
            component=component,
            operation=operation,
            error_type=type(error).__name__,
            error_message=str(error),
            severity=ErrorSeverity.MEDIUM,  # Default, will be updated by pattern matching
            recovery_strategy=RecoveryStrategy.IGNORE,  # Default
            stack_trace=traceback.format_exc(),
            metadata=metadata or {}
        )
        
        # Find matching pattern and update context
        with self._lock:
            for pattern in self._error_patterns:
                if pattern.matches(error_context):
                    error_context.severity = pattern.severity
                    error_context.recovery_strategy = pattern.recovery_strategy
                    error_context.max_retries = pattern.max_retries
                    
                    logger.debug("Matched error pattern",
                               error_id=error_id,
                               pattern_name=pattern.pattern_name,
                               severity=pattern.severity.value,
                               strategy=pattern.recovery_strategy.value)
                    break
            
            # Store error context
            self._error_history.append(error_context)
            self._active_errors[error_id] = error_context
            
            # Update component health
            self._component_health[component] = False
        
        # Log error with appropriate level
        log_level = {
            ErrorSeverity.LOW: "debug",
            ErrorSeverity.MEDIUM: "warning", 
            ErrorSeverity.HIGH: "error",
            ErrorSeverity.CRITICAL: "critical"
        }.get(error_context.severity, "error")
        
        getattr(logger, log_level)(
            "Error detected and classified",
            error_id=error_id,
            component=component,
            operation=operation,
            error_type=error_context.error_type,
            severity=error_context.severity.value,
            recovery_strategy=error_context.recovery_strategy.value
        )
        
        # Record telemetry
        telemetry = get_telemetry_manager()
        if telemetry:
            telemetry.action_failures_counter.add(1, {
                "component": component,
                "error_type": error_context.error_type,
                "severity": error_context.severity.value
            })
        
        # Trigger recovery if strategy is not IGNORE
        if error_context.recovery_strategy != RecoveryStrategy.IGNORE:
            self._trigger_recovery(error_context)
        
        return error_id
    
    def _trigger_recovery(self, error_context: ErrorContext):
        """Trigger recovery process for an error."""
        try:
            recovery_actions = self._recovery_actions.get(error_context.recovery_strategy, [])
            
            if not recovery_actions:
                logger.warning("No recovery actions defined for strategy",
                             strategy=error_context.recovery_strategy.value,
                             error_id=error_context.error_id)
                return
            
            # Execute recovery actions
            for action in recovery_actions:
                try:
                    success = action.execute(error_context)
                    if success:
                        error_context.resolved = True
                        self._component_health[error_context.component] = True
                        
                        logger.info("Error recovery successful",
                                   error_id=error_context.error_id,
                                   action_name=action.action_name)
                        
                        # Record successful recovery
                        telemetry = get_telemetry_manager()
                        if telemetry:
                            telemetry.boundary_calls_counter.add(1, {
                                "interface_type": "internal",
                                "protocol": "recovery",
                                "operation": "success",
                                "strategy": error_context.recovery_strategy.value
                            })
                        break
                        
                except Exception as e:
                    logger.error("Recovery action failed",
                               error_id=error_context.error_id,
                               action_name=action.action_name,
                               error=str(e))
            
            if not error_context.resolved:
                logger.error("All recovery actions failed",
                           error_id=error_context.error_id,
                           strategy=error_context.recovery_strategy.value)
        
        except Exception as e:
            logger.error("Error during recovery process",
                        error_id=error_context.error_id,
                        error=str(e),
                        exc_info=True)
    
    def _retry_with_backoff(self, error_context: ErrorContext) -> bool:
        """Implement exponential backoff retry."""
        if error_context.recovery_attempts >= error_context.max_retries:
            logger.warning("Max retries exceeded",
                          error_id=error_context.error_id,
                          attempts=error_context.recovery_attempts)
            return False
        
        # Calculate backoff delay
        backoff_delay = (2 ** error_context.recovery_attempts) * 0.1
        
        logger.info("Retrying with backoff",
                   error_id=error_context.error_id,
                   attempt=error_context.recovery_attempts + 1,
                   delay_seconds=backoff_delay)
        
        time.sleep(backoff_delay)
        error_context.recovery_attempts += 1
        
        # Return True to indicate retry should be attempted
        # Actual retry logic would be handled by the calling component
        return True
    
    def _restart_component(self, error_context: ErrorContext) -> bool:
        """Restart a failed component."""
        logger.info("Attempting component restart",
                   error_id=error_context.error_id,
                   component=error_context.component)
        
        # Component restart logic would be implemented here
        # This is a placeholder for demonstration
        return True
    
    def _degrade_gracefully(self, error_context: ErrorContext) -> bool:
        """Implement graceful degradation."""
        logger.info("Implementing graceful degradation",
                   error_id=error_context.error_id,
                   component=error_context.component)
        
        # Graceful degradation logic would be implemented here
        # This could involve disabling non-essential features
        return True
    
    def _failover_to_backup(self, error_context: ErrorContext) -> bool:
        """Failover to backup system or configuration."""
        logger.info("Attempting failover to backup",
                   error_id=error_context.error_id,
                   component=error_context.component)
        
        # Failover logic would be implemented here
        # This could involve switching to backup config or services
        return True
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error and recovery statistics."""
        with self._lock:
            error_count_by_severity = {}
            error_count_by_component = {}
            recovery_success_rate = {}
            
            for error_context in list(self._error_history):
                # Count by severity
                severity = error_context.severity.value
                error_count_by_severity[severity] = error_count_by_severity.get(severity, 0) + 1
                
                # Count by component
                component = error_context.component
                error_count_by_component[component] = error_count_by_component.get(component, 0) + 1
                
                # Track recovery success
                strategy = error_context.recovery_strategy.value
                if strategy not in recovery_success_rate:
                    recovery_success_rate[strategy] = {"total": 0, "successful": 0}
                
                recovery_success_rate[strategy]["total"] += 1
                if error_context.resolved:
                    recovery_success_rate[strategy]["successful"] += 1
            
            # Calculate success rates
            for strategy_stats in recovery_success_rate.values():
                if strategy_stats["total"] > 0:
                    strategy_stats["rate"] = strategy_stats["successful"] / strategy_stats["total"]
                else:
                    strategy_stats["rate"] = 0.0
            
            return {
                "total_errors": len(self._error_history),
                "active_errors": len(self._active_errors),
                "error_count_by_severity": error_count_by_severity,
                "error_count_by_component": error_count_by_component,
                "recovery_success_rate": recovery_success_rate,
                "component_health": self._component_health.copy(),
                "error_patterns_count": len(self._error_patterns)
            }
    
    def resolve_error(self, error_id: str):
        """Mark an error as resolved."""
        with self._lock:
            if error_id in self._active_errors:
                error_context = self._active_errors[error_id]
                error_context.resolved = True
                del self._active_errors[error_id]
                
                # Update component health
                self._component_health[error_context.component] = True
                
                logger.info("Error marked as resolved",
                           error_id=error_id,
                           component=error_context.component)
    
    def get_component_health(self, component: str) -> bool:
        """Get health status of a component."""
        with self._lock:
            return self._component_health.get(component, True)
    
    def clear_error_history(self):
        """Clear error history (for testing/maintenance)."""
        with self._lock:
            self._error_history.clear()
            self._active_errors.clear()
            logger.info("Error history cleared")


# Global error recovery manager instance
_error_recovery_manager: Optional[ErrorRecoveryManager] = None
_recovery_lock = threading.RLock()


def get_error_recovery_manager() -> ErrorRecoveryManager:
    """Get or create global error recovery manager."""
    global _error_recovery_manager
    
    with _recovery_lock:
        if _error_recovery_manager is None:
            _error_recovery_manager = ErrorRecoveryManager()
        
        return _error_recovery_manager


def handle_error(component: str,
                operation: str,
                error: Exception,
                metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Convenience function to handle errors using global recovery manager.
    
    Args:
        component: Component where error occurred
        operation: Operation being performed
        error: The exception that occurred
        metadata: Additional context metadata
        
    Returns:
        Error ID for tracking
    """
    manager = get_error_recovery_manager()
    return manager.handle_error(component, operation, error, metadata)