#!/usr/bin/env python3
"""
Scribe Vault Retry Handler

Implements professional exponential backoff retry logic with jitter
for Vault operations to handle transient failures gracefully.
"""

import time
import random
import threading
from typing import Callable, Any, Optional, Type, Union, List
from dataclasses import dataclass, field
from enum import Enum
import structlog

from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class RetryStrategy(Enum):
    """Available retry strategies."""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff" 
    FIXED_INTERVAL = "fixed_interval"


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3                              # Maximum retry attempts
    base_delay: float = 1.0                           # Base delay in seconds
    max_delay: float = 60.0                           # Maximum delay in seconds
    exponential_base: float = 2.0                     # Exponential backoff base
    jitter: bool = True                               # Add random jitter
    jitter_range: float = 0.1                        # Jitter range (±10%)
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    
    # Exception handling
    retryable_exceptions: tuple = field(default_factory=lambda: (
        ConnectionError,
        TimeoutError,
        OSError,
        # Add Vault-specific exceptions
    ))
    
    # Conditions for retrying
    retry_on_status_codes: List[int] = field(default_factory=lambda: [
        429,  # Too Many Requests
        500,  # Internal Server Error
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
    ])


class RetryExhaustedError(Exception):
    """Exception raised when all retry attempts are exhausted."""
    
    def __init__(self, message: str, attempts: int, last_exception: Exception):
        self.attempts = attempts
        self.last_exception = last_exception
        super().__init__(message)


class VaultRetryHandler:
    """
    Professional retry handler for Vault operations.
    
    Implements exponential backoff with jitter to handle transient failures
    while avoiding thundering herd problems.
    """
    
    def __init__(self, config: RetryConfig, name: str = "vault_retry_handler"):
        """
        Initialize retry handler.
        
        Args:
            config: Retry configuration
            name: Name for logging and identification
        """
        self.config = config
        self.name = name
        
        # Metrics for monitoring
        self._total_calls = 0
        self._total_retries = 0
        self._successful_retries = 0
        self._failed_after_retries = 0
        self._lock = threading.RLock()
        
        logger.info("Retry handler initialized",
                   name=self.name,
                   max_attempts=config.max_attempts,
                   base_delay=config.base_delay,
                   strategy=config.strategy.value)
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with retry logic.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            RetryExhaustedError: If all retry attempts fail
            Original exception: If non-retryable exception occurs
        """
        with self._lock:
            self._total_calls += 1
        
        last_exception = None
        attempt = 0
        
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                if attempt > 1:
                    with self._lock:
                        self._total_retries += 1
                    
                    logger.info("Retrying function execution",
                               function=func.__name__,
                               attempt=attempt,
                               max_attempts=self.config.max_attempts,
                               previous_error=str(last_exception) if last_exception else None)
                
                # Execute the function
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                if attempt > 1:
                    with self._lock:
                        self._successful_retries += 1
                    
                    logger.info("Function succeeded after retry",
                               function=func.__name__,
                               attempt=attempt,
                               execution_time=execution_time)
                else:
                    logger.debug("Function succeeded on first attempt",
                               function=func.__name__,
                               execution_time=execution_time)
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # Check if exception is retryable
                if not self._is_retryable_exception(e):
                    logger.warning("Non-retryable exception occurred",
                                 function=func.__name__,
                                 attempt=attempt,
                                 error=str(e),
                                 error_type=type(e).__name__)
                    raise e
                
                # Don't sleep after the last attempt
                if attempt < self.config.max_attempts:
                    delay = self._calculate_delay(attempt)
                    
                    logger.warning("Function failed, retrying after delay",
                                 function=func.__name__,
                                 attempt=attempt,
                                 max_attempts=self.config.max_attempts,
                                 error=str(e),
                                 delay=delay)
                    
                    time.sleep(delay)
                else:
                    logger.error("Function failed after all retry attempts",
                               function=func.__name__,
                               total_attempts=attempt,
                               final_error=str(e))
        
        # All retry attempts exhausted
        with self._lock:
            self._failed_after_retries += 1
        
        raise RetryExhaustedError(
            f"Function '{func.__name__}' failed after {attempt} attempts",
            attempt,
            last_exception
        )
    
    def _is_retryable_exception(self, exception: Exception) -> bool:
        """
        Determine if exception is retryable.
        
        Args:
            exception: Exception to check
            
        Returns:
            True if exception should trigger retry
        """
        # Check if exception type is retryable
        if isinstance(exception, self.config.retryable_exceptions):
            return True
        
        # Check for HTTP status codes (if exception has status_code attribute)
        if hasattr(exception, 'status_code'):
            return exception.status_code in self.config.retry_on_status_codes
        
        # Check for response status codes (for requests-like exceptions)
        if hasattr(exception, 'response') and hasattr(exception.response, 'status_code'):
            return exception.response.status_code in self.config.retry_on_status_codes
        
        # Check for Vault-specific error patterns in exception message
        error_message = str(exception).lower()
        vault_retryable_patterns = [
            'connection refused',
            'connection timeout',
            'service unavailable',
            'temporary failure',
            'rate limit',
            'too many requests',
            'network unreachable',
            'name resolution failure'
        ]
        
        return any(pattern in error_message for pattern in vault_retryable_patterns)
    
    def _calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt number.
        
        Args:
            attempt: Current attempt number (1-based)
            
        Returns:
            Delay in seconds
        """
        if self.config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            # Exponential backoff: base_delay * (exponential_base ^ (attempt - 1))
            delay = self.config.base_delay * (self.config.exponential_base ** (attempt - 1))
        
        elif self.config.strategy == RetryStrategy.LINEAR_BACKOFF:
            # Linear backoff: base_delay * attempt
            delay = self.config.base_delay * attempt
        
        elif self.config.strategy == RetryStrategy.FIXED_INTERVAL:
            # Fixed interval: always use base_delay
            delay = self.config.base_delay
        
        else:
            # Default to exponential backoff
            delay = self.config.base_delay * (self.config.exponential_base ** (attempt - 1))
        
        # Apply maximum delay limit
        delay = min(delay, self.config.max_delay)
        
        # Add jitter to prevent thundering herd
        if self.config.jitter:
            jitter_amount = delay * self.config.jitter_range
            jitter = random.uniform(-jitter_amount, jitter_amount)
            delay = max(0.1, delay + jitter)  # Ensure minimum delay of 100ms
        
        return delay
    
    def get_metrics(self) -> dict:
        """Get retry handler metrics for monitoring."""
        with self._lock:
            return {
                'name': self.name,
                'total_calls': self._total_calls,
                'total_retries': self._total_retries,
                'successful_retries': self._successful_retries,
                'failed_after_retries': self._failed_after_retries,
                'retry_rate': self._total_retries / max(self._total_calls, 1),
                'retry_success_rate': self._successful_retries / max(self._total_retries, 1),
                'config': {
                    'max_attempts': self.config.max_attempts,
                    'base_delay': self.config.base_delay,
                    'max_delay': self.config.max_delay,
                    'strategy': self.config.strategy.value
                }
            }
    
    def reset_metrics(self):
        """Reset retry metrics."""
        with self._lock:
            self._total_calls = 0
            self._total_retries = 0
            self._successful_retries = 0
            self._failed_after_retries = 0
            
            logger.info("Retry handler metrics reset", name=self.name)


class VaultRetryManager:
    """
    Manages retry handlers for different Vault operations.
    
    Provides centralized configuration and monitoring of retry behavior
    for various Vault API operations.
    """
    
    def __init__(self):
        """Initialize retry manager."""
        self._handlers: dict[str, VaultRetryHandler] = {}
        self._lock = threading.RLock()
        self._max_handlers = 10  # CRITICAL: Limit to prevent unbounded growth
        
        # Default retry configurations for different operations
        self._default_configs = {
            'secret_read': RetryConfig(
                max_attempts=3,
                base_delay=0.5,
                max_delay=10.0,
                strategy=RetryStrategy.EXPONENTIAL_BACKOFF
            ),
            'secret_write': RetryConfig(
                max_attempts=2,
                base_delay=1.0,
                max_delay=15.0,
                strategy=RetryStrategy.EXPONENTIAL_BACKOFF
            ),
            'pki_generate': RetryConfig(
                max_attempts=3,
                base_delay=2.0,
                max_delay=30.0,
                strategy=RetryStrategy.EXPONENTIAL_BACKOFF
            ),
            'auth': RetryConfig(
                max_attempts=2,
                base_delay=0.5,
                max_delay=5.0,
                strategy=RetryStrategy.EXPONENTIAL_BACKOFF
            ),
            'health': RetryConfig(
                max_attempts=2,
                base_delay=0.2,
                max_delay=2.0,
                strategy=RetryStrategy.LINEAR_BACKOFF
            )
        }
        
        logger.info("Retry manager initialized",
                   available_configs=list(self._default_configs.keys()))
    
    def get_handler(self, operation_type: str, custom_config: Optional[RetryConfig] = None) -> VaultRetryHandler:
        """
        Get or create retry handler for operation type.
        
        Args:
            operation_type: Type of operation
            custom_config: Optional custom configuration
            
        Returns:
            Retry handler instance
        """
        with self._lock:
            if operation_type not in self._handlers:
                # CRITICAL: Prevent unbounded growth that causes crashes
                if len(self._handlers) >= self._max_handlers:
                    logger.warning("Too many retry handlers, clearing oldest",
                                 current_count=len(self._handlers),
                                 max_allowed=self._max_handlers)
                    # Clear all handlers to prevent memory exhaustion
                    self._handlers.clear()
                
                config = custom_config or self._default_configs.get(
                    operation_type,
                    RetryConfig()  # Default configuration
                )
                
                handler_name = f"vault_retry_{operation_type}"
                self._handlers[operation_type] = VaultRetryHandler(config, handler_name)
                
                logger.info("Created new retry handler",
                           operation_type=operation_type,
                           name=handler_name)
            
            return self._handlers[operation_type]
    
    def get_all_metrics(self) -> dict[str, dict]:
        """Get metrics for all retry handlers."""
        with self._lock:
            return {
                operation_type: handler.get_metrics()
                for operation_type, handler in self._handlers.items()
            }
    
    def reset_all_metrics(self):
        """Reset metrics for all retry handlers."""
        with self._lock:
            for handler in self._handlers.values():
                handler.reset_metrics()
            
            logger.info("All retry handler metrics reset",
                       count=len(self._handlers))


# Global retry manager instance
_retry_manager: Optional[VaultRetryManager] = None
_manager_lock = threading.RLock()


def get_vault_retry_manager() -> VaultRetryManager:
    """Get or create global retry manager."""
    global _retry_manager
    
    with _manager_lock:
        if _retry_manager is None:
            _retry_manager = VaultRetryManager()
        
        return _retry_manager


def retry_on_failure(operation_type: str, custom_config: Optional[RetryConfig] = None):
    """
    Decorator to add retry logic to functions.
    
    Args:
        operation_type: Type of operation for retry handler selection
        custom_config: Optional custom retry configuration
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            manager = get_vault_retry_manager()
            handler = manager.get_handler(operation_type, custom_config)
            return handler.execute(func, *args, **kwargs)
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    
    return decorator