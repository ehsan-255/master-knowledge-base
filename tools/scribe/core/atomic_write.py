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
import time
import portalocker

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
        
        # Write data to temporary file with proper Windows file handle management
        try:
            if is_binary:
                if isinstance(data, str):
                    data = data.encode(encoding)
                # Use low-level file operations for binary mode
                os.write(temp_fd, data)
            else:
                if isinstance(data, bytes):
                    data = data.decode(encoding)
                # Use low-level file operations for text mode
                os.write(temp_fd, data.encode(encoding))
            
            # Force write to disk
            os.fsync(temp_fd)
            
        except Exception as write_error:
            logger.error("temp_file_write_failed",
                        temp_file=str(temp_path),
                        error=str(write_error))
            raise
        
        # Close the file descriptor before rename (Windows requirement)
        os.close(temp_fd)
        temp_fd = None
        
        # Atomic rename with simple retry logic for Windows
        max_retries = 5
        for retry in range(max_retries):
            try:
                # Perform atomic rename
                os.replace(str(temp_path), str(filepath))
                break
                
            except (OSError, PermissionError) as e:
                if retry == max_retries - 1:
                    logger.error("atomic_rename_failed_final",
                               temp_file=str(temp_path),
                               target_file=str(filepath),
                               retry_count=retry + 1,
                               error=str(e))
                    raise
                
                logger.debug("atomic_rename_retry",
                            temp_file=str(temp_path),
                            target_file=str(filepath),
                            retry_count=retry + 1,
                            error=str(e))
                time.sleep(min(1, 0.1 * (2 ** retry)))  # Exponential backoff

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


class AtomicWriteTestHelper:
    """Test helper class for simulating atomic write failures and interruptions"""
    
    def __init__(self):
        self.simulate_interruption = False
        self.simulate_fsync_failure = False
        self.simulate_rename_failure = False
        self.interruption_point = None
    
    def simulate_interruption_during_write(self, interruption_point='write'):
        """Simulate interruption at different points during write operation
        
        Args:
            interruption_point: Where to simulate failure ('write', 'fsync', 'rename')
        """
        self.simulate_interruption = True
        self.interruption_point = interruption_point
    
    def reset_simulation(self):
        """Reset all simulation flags"""
        self.simulate_interruption = False
        self.simulate_fsync_failure = False
        self.simulate_rename_failure = False
        self.interruption_point = None
    
    def should_fail_at_point(self, point):
        """Check if we should simulate failure at given point"""
        return self.simulate_interruption and self.interruption_point == point 