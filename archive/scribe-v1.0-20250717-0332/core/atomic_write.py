"""
Atomic file write utility for crash-safe file operations.

This module implements the write-temp -> fsync -> rename pattern to ensure
that file writes are atomic and crash-safe. If the process is interrupted
during a write operation, the original file remains unchanged.
"""

import os
import tempfile
from pathlib import Path
from typing import Union, BinaryIO, TextIO
import structlog
from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


def atomic_write(filepath: Union[str, Path], data: Union[str, bytes], 
                 encoding: str = 'utf-8', mode: str = 'w') -> bool:
    """
    Write data to a file atomically using the write-temp -> fsync -> rename pattern.
    
    This function ensures that either the entire write operation succeeds, or the
    original file remains completely unchanged. It protects against corruption
    from power loss, process crashes, or other interruptions.
    
    Args:
        filepath: Path to the target file
        data: Data to write (string or bytes)
        encoding: Text encoding to use (ignored for binary mode)
        mode: Write mode ('w' for text, 'wb' for binary)
        
    Returns:
        bool: True if write succeeded, False otherwise
        
    Raises:
        ValueError: If mode is not supported
        OSError: If file operations fail
    """
    filepath = Path(filepath)
    
    # Validate mode
    if mode not in ('w', 'wb'):
        raise ValueError(f"Unsupported mode '{mode}'. Use 'w' for text or 'wb' for binary.")
    
    # Determine if we're writing text or binary
    is_binary = mode == 'wb'
    
    # Create temporary file in the same directory as target
    # This ensures the rename operation is atomic on POSIX systems
    temp_dir = filepath.parent
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    temp_fd = None
    temp_path = None
    
    try:
        # Create temporary file in same directory as target
        temp_fd, temp_path = tempfile.mkstemp(
            dir=temp_dir,
            prefix=f".{filepath.name}.tmp.",
            suffix=".atomic"
        )
        temp_path = Path(temp_path)
        
        logger.debug("atomic_write_started", 
                    target_file=str(filepath),
                    temp_file=str(temp_path),
                    data_size=len(data),
                    mode=mode)
        
        # Write data to temporary file
        if is_binary:
            if isinstance(data, str):
                data = data.encode(encoding)
            os.write(temp_fd, data)
        else:
            if isinstance(data, bytes):
                data = data.decode(encoding)
            os.write(temp_fd, data.encode(encoding))
        
        # Force write to disk (fsync)
        os.fsync(temp_fd)
        
        # Close the file descriptor before rename
        os.close(temp_fd)
        temp_fd = None
        
        # Atomic rename - this is the critical operation
        # On POSIX systems, this is guaranteed to be atomic
        temp_path.rename(filepath)
        
        logger.info("atomic_write_completed",
                   target_file=str(filepath),
                   data_size=len(data),
                   mode=mode)
        
        return True
        
    except Exception as e:
        logger.error("atomic_write_failed",
                    target_file=str(filepath),
                    temp_file=str(temp_path) if temp_path else None,
                    error=str(e),
                    error_type=type(e).__name__)
        
        # Clean up temporary file if it exists
        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
                logger.debug("temp_file_cleaned_up", temp_file=str(temp_path))
            except Exception as cleanup_error:
                logger.warning("temp_file_cleanup_failed",
                             temp_file=str(temp_path),
                             cleanup_error=str(cleanup_error))
        
        return False
        
    finally:
        # Ensure file descriptor is closed
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except Exception:
                pass  # Already closed or invalid


def atomic_write_json(filepath: Union[str, Path], data: dict, 
                      indent: int = 2, ensure_ascii: bool = False) -> bool:
    """
    Write JSON data to a file atomically.
    
    Args:
        filepath: Path to the target file
        data: Dictionary to write as JSON
        indent: JSON indentation level
        ensure_ascii: Whether to escape non-ASCII characters
        
    Returns:
        bool: True if write succeeded, False otherwise
    """
    import json
    
    try:
        json_data = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
        return atomic_write(filepath, json_data, mode='w')
    except (TypeError, ValueError) as e:
        logger.error("json_serialization_failed",
                    target_file=str(filepath),
                    error=str(e))
        return False


def atomic_write_yaml(filepath: Union[str, Path], data: dict) -> bool:
    """
    Write YAML data to a file atomically.
    
    Args:
        filepath: Path to the target file
        data: Dictionary to write as YAML
        
    Returns:
        bool: True if write succeeded, False otherwise
    """
    try:
        import yaml
        yaml_data = yaml.dump(data, default_flow_style=False, sort_keys=False)
        return atomic_write(filepath, yaml_data, mode='w')
    except ImportError:
        logger.error("yaml_module_not_available", target_file=str(filepath))
        return False
    except yaml.YAMLError as e:
        logger.error("yaml_serialization_failed",
                    target_file=str(filepath),
                    error=str(e))
        return False 