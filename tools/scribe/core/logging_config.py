"""
Scribe Engine - Structured Logging Configuration

This module configures structlog for machine-parsable JSON log output.
All logs are emitted as JSON lines to stdout for easy ingestion into
monitoring systems like Grafana Loki or ELK stack.
"""

import sys
import logging
import structlog
from typing import Dict, Any, Optional


def configure_structured_logging(
    log_level: str = "INFO",
    include_stdlib_logs: bool = True,
    add_caller_info: bool = False
) -> None:
    """
    Configure structlog for structured JSON logging.
    
    This sets up the complete processor chain to output machine-parsable
    JSON logs with timestamps, log levels, and contextual information.
    
    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        include_stdlib_logs: Whether to capture standard library logs
        add_caller_info: Whether to include caller file/line information
    """
    # Configure standard library logging to work with structlog
    if include_stdlib_logs:
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=getattr(logging, log_level.upper())
        )
    
    # Build processor chain
    processors = [
        # Filter by log level
        structlog.stdlib.filter_by_level,
        
        # Add logger name
        structlog.stdlib.add_logger_name,
        
        # Add log level
        structlog.stdlib.add_log_level,
        
        # Handle positional arguments
        structlog.stdlib.PositionalArgumentsFormatter(),
        
        # Add ISO timestamp
        structlog.processors.TimeStamper(fmt="iso"),
        
        # Add stack info for exceptions
        structlog.processors.StackInfoRenderer(),
        
        # Format exception info
        structlog.processors.format_exc_info,
        
        # Handle Unicode properly
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Add caller info if requested (useful for debugging)
    if add_caller_info:
        processors.insert(-1, structlog.processors.CallsiteParameterAdder(
            parameters=[structlog.processors.CallsiteParameter.FILENAME,
                       structlog.processors.CallsiteParameter.LINENO,
                       structlog.processors.CallsiteParameter.FUNC_NAME]
        ))
    
    # Final JSON renderer
    processors.append(structlog.processors.JSONRenderer())
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_scribe_logger(name: str, **initial_context) -> structlog.stdlib.BoundLogger:
    """
    Get a configured logger with optional initial context.
    
    Args:
        name: Logger name (typically __name__)
        **initial_context: Initial context to bind to the logger
        
    Returns:
        Configured structlog logger with bound context
    """
    logger = structlog.get_logger(name)
    
    if initial_context:
        logger = logger.bind(**initial_context)
    
    return logger


def add_global_context(**context) -> None:
    """
    Add global context that will be included in all log messages.
    
    Args:
        **context: Key-value pairs to add to global context
    """
    structlog.configure(
        processors=structlog.get_config()["processors"],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
        initial_values=context
    )


def create_request_logger(request_id: str, **context) -> structlog.stdlib.BoundLogger:
    """
    Create a logger with request-specific context.
    
    Useful for tracking events through the processing pipeline.
    
    Args:
        request_id: Unique identifier for this request/event
        **context: Additional context to bind
        
    Returns:
        Logger with bound request context
    """
    return get_scribe_logger("scribe.request").bind(
        request_id=request_id,
        **context
    )


def log_performance_metrics(
    logger: structlog.stdlib.BoundLogger,
    operation: str,
    duration_ms: float,
    **metrics
) -> None:
    """
    Log performance metrics in a standardized format.
    
    Args:
        logger: Structlog logger instance
        operation: Name of the operation being measured
        duration_ms: Duration in milliseconds
        **metrics: Additional metrics to log
    """
    logger.info(
        "performance_metrics",
        operation=operation,
        duration_ms=round(duration_ms, 2),
        **metrics
    )


def log_event_processing(
    logger: structlog.stdlib.BoundLogger,
    event_type: str,
    file_path: str,
    status: str,
    duration_ms: Optional[float] = None,
    **context
) -> None:
    """
    Log event processing in a standardized format.
    
    Args:
        logger: Structlog logger instance
        event_type: Type of file system event
        file_path: Path to the file that triggered the event
        status: Processing status (started, completed, failed)
        duration_ms: Processing duration in milliseconds
        **context: Additional context
    """
    log_data = {
        "event_processing": True,
        "event_type": event_type,
        "file_path": file_path,
        "status": status,
        **context
    }
    
    if duration_ms is not None:
        log_data["duration_ms"] = round(duration_ms, 2)
    
    if status == "failed":
        logger.error("Event processing failed", **log_data)
    elif status == "completed":
        logger.info("Event processing completed", **log_data)
    else:
        logger.info("Event processing status", **log_data)


# JSON Schema for log validation (useful for testing)
LOG_SCHEMA = {
    "type": "object",
    "required": ["timestamp", "level", "event"],
    "properties": {
        "timestamp": {"type": "string"},
        "level": {"type": "string", "enum": ["debug", "info", "warning", "error", "critical"]},
        "event": {"type": "string"},
        "logger": {"type": "string"},
        "request_id": {"type": "string"},
        "event_type": {"type": "string"},
        "file_path": {"type": "string"},
        "duration_ms": {"type": "number"},
        "status": {"type": "string"}
    },
    "additionalProperties": True
} 