#!/usr/bin/env python3
"""
Windows-Enhanced Atomic Write System for HMA v2.1

Provides Windows-optimized atomic file operations with proper file locking,
long path support, and comprehensive retry mechanisms for Windows-specific issues.
"""

import os
import sys
import tempfile
import time
import ctypes
from pathlib import Path, PurePath
from typing import Union, Dict, Any, Optional
import threading

from .logging_config import get_scribe_logger

# Windows-specific imports
if os.name == 'nt':
    try:
        import win32file
        import win32api
        import win32con
        HAS_PYWIN32 = True
    except ImportError:
        HAS_PYWIN32 = False
        import warnings
        warnings.warn("pywin32 not available, Windows optimizations disabled")

logger = get_scribe_logger(__name__)

class WindowsFileHandler:
    """Windows-specific file handling with proper path support"""
    
    @staticmethod
    def normalize_path(path_input: Union[str, Path]) -> Path:
        """Properly normalize paths for Windows with long path support"""
        try:
            path = Path(path_input).resolve()
            
            # Handle long path names on Windows (>260 characters)
            if os.name == 'nt' and len(str(path)) > 260:
                # Use \\?\ prefix for long paths
                if not str(path).startswith('\\\\?\\'):
                    return Path(f"\\\\?\\{path}")
            
            return path
        except Exception as e:
            logger.error("Path normalization failed", path=str(path_input), error=str(e))
            return Path(path_input)
    
    @staticmethod
    def is_case_sensitive_match(path1: str, path2: str) -> bool:
        """Check if paths match considering Windows case insensitivity"""
        if os.name == 'nt':
            try:
                return Path(path1).resolve() == Path(path2).resolve()
            except Exception:
                return path1.lower() == path2.lower()
        else:
            return path1 == path2
    
    @staticmethod 
    def get_windows_permissions(file_path: str) -> Dict[str, bool]:
        """Get Windows file permissions"""
        try:
            return {
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK),
                'executable': os.access(file_path, os.X_OK)
            }
        except Exception as e:
            logger.warning("Failed to get Windows permissions", path=file_path, error=str(e))
            return {'readable': False, 'writable': False, 'executable': False}

class WindowsAtomicWriter:
    """Windows-optimized atomic write operations with comprehensive retry logic"""
    
    def __init__(self):
        self.max_retries = 15
        self.base_delay = 0.025  # Start with 25ms
        self.max_delay = 5.0     # Max 5 seconds
        self.backoff_multiplier = 1.5
        
        # Thread-local storage for tracking retries
        self._local = threading.local()
    
    def atomic_write(self, filepath: Union[str, Path], data: Union[str, bytes], 
                    encoding: str = 'utf-8', mode: str = 'w') -> bool:
        """
        Windows-optimized atomic write with comprehensive error handling
        
        Args:
            filepath: Target file path
            data: Data to write
            encoding: Text encoding (for text mode)
            mode: Write mode ('w' or 'wb')
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Normalize path for Windows
        filepath = WindowsFileHandler.normalize_path(filepath)
        temp_path = None
        temp_fd = None
        
        try:
            # Validate mode
            if mode not in ('w', 'wb'):
                raise ValueError(f"Unsupported mode '{mode}'. Use 'w' for text or 'wb' for binary.")
            
            is_binary = mode == 'wb'
            
            # Ensure parent directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Create temp file in same directory for atomic rename
            temp_fd, temp_path = tempfile.mkstemp(
                dir=filepath.parent,
                prefix=f".{filepath.name}.tmp.",
                suffix=".scribe-atomic"
            )
            temp_path = Path(temp_path)
            
            logger.debug("Starting atomic write",
                        target_file=str(filepath),
                        temp_file=str(temp_path),
                        data_size=len(data),
                        mode=mode)
            
            # Write data to temporary file
            success = self._write_temp_file(temp_fd, data, encoding, is_binary)
            if not success:
                return False
            
            # Close file descriptor before rename (Windows requirement)
            os.close(temp_fd)
            temp_fd = None
            
            # Perform atomic move with Windows-specific retry logic
            return self._atomic_move_windows(temp_path, filepath)
            
        except Exception as e:
            logger.error("Atomic write failed",
                        target_file=str(filepath),
                        temp_file=str(temp_path) if temp_path else None,
                        error=str(e),
                        error_type=type(e).__name__)
            return False
        finally:
            # Cleanup
            if temp_fd is not None:
                try:
                    os.close(temp_fd)
                except:
                    pass
            
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                    logger.debug("Temp file cleaned up", temp_file=str(temp_path))
                except Exception as cleanup_error:
                    logger.warning("Temp file cleanup failed",
                                 temp_file=str(temp_path),
                                 cleanup_error=str(cleanup_error))
    
    def _write_temp_file(self, temp_fd: int, data: Union[str, bytes], 
                        encoding: str, is_binary: bool) -> bool:
        """Write data to temporary file with proper encoding"""
        try:
            if is_binary:
                if isinstance(data, str):
                    data = data.encode(encoding)
                os.write(temp_fd, data)
            else:
                if isinstance(data, bytes):
                    data = data.decode(encoding)
                os.write(temp_fd, data.encode(encoding))
            
            # Force data to disk
            os.fsync(temp_fd)
            return True
            
        except Exception as e:
            logger.error("Failed to write temp file", error=str(e))
            return False
    
    def _atomic_move_windows(self, src: Path, dst: Path) -> bool:
        """Windows-specific atomic move with comprehensive retry logic"""
        
        for attempt in range(self.max_retries):
            try:
                # Method 1: Try standard os.replace (fastest)
                os.replace(str(src), str(dst))
                logger.info("Atomic write completed successfully",
                           target_file=str(dst),
                           attempts=attempt + 1)
                return True
                
            except PermissionError as e:
                if self._is_sharing_violation(e):
                    # File is locked by another process - wait and retry
                    delay = self._calculate_backoff_delay(attempt)
                    logger.debug("File sharing violation, retrying",
                               target_file=str(dst),
                               attempt=attempt + 1,
                               delay=delay,
                               error=str(e))
                    time.sleep(delay)
                    continue
                else:
                    # Permission issue - try Win32 fallback
                    if self._try_win32_move(src, dst):
                        logger.info("Atomic write completed via Win32 API",
                                   target_file=str(dst),
                                   attempts=attempt + 1)
                        return True
                    
                    # If Win32 also fails, continue retry loop
                    delay = self._calculate_backoff_delay(attempt)
                    time.sleep(delay)
                    continue
                    
            except FileExistsError:
                # Target exists - try to remove and retry
                try:
                    dst.unlink()
                    logger.debug("Removed existing target file", target_file=str(dst))
                    continue
                except Exception as unlink_error:
                    logger.debug("Failed to remove existing file",
                               target_file=str(dst),
                               error=str(unlink_error))
                    delay = self._calculate_backoff_delay(attempt)
                    time.sleep(delay)
                    continue
                    
            except OSError as e:
                if hasattr(e, 'winerror'):
                    if e.winerror == 32:  # ERROR_SHARING_VIOLATION
                        delay = self._calculate_backoff_delay(attempt)
                        logger.debug("Windows sharing violation, retrying",
                                   target_file=str(dst),
                                   attempt=attempt + 1,
                                   delay=delay)
                        time.sleep(delay)
                        continue
                    elif e.winerror == 5:  # ERROR_ACCESS_DENIED
                        # Try Win32 approach
                        if self._try_win32_move(src, dst):
                            return True
                        delay = self._calculate_backoff_delay(attempt)
                        time.sleep(delay)
                        continue
                
                # Unknown OS error - log and retry
                logger.warning("OS error during atomic move",
                             target_file=str(dst),
                             attempt=attempt + 1,
                             error=str(e))
                delay = self._calculate_backoff_delay(attempt)
                time.sleep(delay)
                continue
                
            except Exception as e:
                # Unexpected error
                logger.warning("Unexpected error during atomic move",
                             target_file=str(dst),
                             attempt=attempt + 1,
                             error=str(e),
                             error_type=type(e).__name__)
                if attempt == self.max_retries - 1:
                    break
                delay = self._calculate_backoff_delay(attempt)
                time.sleep(delay)
                continue
        
        logger.error("Atomic move failed after all retries",
                    source_file=str(src),
                    target_file=str(dst),
                    max_retries=self.max_retries)
        return False
    
    def _try_win32_move(self, src: Path, dst: Path) -> bool:
        """Fallback using Win32 API for stubborn files"""
        if not HAS_PYWIN32:
            return False
        
        try:
            # Use MoveFileEx with replace existing flag
            win32file.MoveFileEx(
                str(src),
                str(dst),
                win32file.MOVEFILE_REPLACE_EXISTING | win32file.MOVEFILE_WRITE_THROUGH
            )
            return True
        except Exception as e:
            logger.debug("Win32 move failed", error=str(e))
            return False
    
    def _is_sharing_violation(self, error: PermissionError) -> bool:
        """Check if error is a Windows file sharing violation"""
        error_msg = str(error).lower()
        sharing_indicators = [
            "being used by another process",
            "sharing violation",
            "access is denied"
        ]
        return any(indicator in error_msg for indicator in sharing_indicators)
    
    def _calculate_backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter"""
        base_delay = self.base_delay * (self.backoff_multiplier ** attempt)
        # Add some jitter (±20%)
        import random
        jitter = random.uniform(0.8, 1.2)
        delay = min(base_delay * jitter, self.max_delay)
        return delay

# Global instance for convenience
_windows_writer = None

def get_windows_atomic_writer() -> WindowsAtomicWriter:
    """Get singleton Windows atomic writer instance"""
    global _windows_writer
    if _windows_writer is None:
        _windows_writer = WindowsAtomicWriter()
    return _windows_writer

def atomic_write_windows(filepath: Union[str, Path], data: Union[str, bytes],
                        encoding: str = 'utf-8', mode: str = 'w') -> bool:
    """
    Convenience function for Windows-optimized atomic writes
    
    This is a drop-in replacement for the original atomic_write function
    with Windows-specific optimizations.
    """
    writer = get_windows_atomic_writer()
    return writer.atomic_write(filepath, data, encoding, mode)