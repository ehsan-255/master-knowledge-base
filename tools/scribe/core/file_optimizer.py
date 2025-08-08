#!/usr/bin/env python3
"""
Scribe Engine File System Optimizer

Implements high-performance file system operations with batching, streaming,
memory mapping, and intelligent I/O scheduling for optimal performance.
"""

import os
import mmap
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Iterator, BinaryIO, TextIO, Any
from dataclasses import dataclass
from collections import deque
import structlog

from .logging_config import get_scribe_logger
from cache_manager import get_cache_manager, memoize
from .telemetry import get_telemetry_manager

logger = get_scribe_logger(__name__)


@dataclass
class FileOperation:
    """Represents a file operation for batching."""
    operation_type: str  # 'read', 'write', 'stat', 'delete'
    file_path: Path
    data: Optional[Union[str, bytes]] = None
    encoding: str = 'utf-8'
    callback: Optional[callable] = None
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class FileStreamReader:
    """Memory-efficient streaming file reader."""
    
    def __init__(self, file_path: Union[str, Path], chunk_size: int = 8192):
        """
        Initialize streaming reader.
        
        Args:
            file_path: Path to file
            chunk_size: Size of chunks to read
        """
        self.file_path = Path(file_path)
        self.chunk_size = chunk_size
        self._file: Optional[BinaryIO] = None
        self._position = 0
        
    def __enter__(self):
        self._file = open(self.file_path, 'rb')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
    
    def __iter__(self) -> Iterator[bytes]:
        """Iterate over file chunks."""
        if not self._file:
            raise RuntimeError("FileStreamReader not opened")
        
        while True:
            chunk = self._file.read(self.chunk_size)
            if not chunk:
                break
            self._position += len(chunk)
            yield chunk
    
    def read_lines(self, encoding: str = 'utf-8') -> Iterator[str]:
        """Iterate over file lines."""
        buffer = b''
        
        for chunk in self:
            buffer += chunk
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                yield line.decode(encoding, errors='replace') + '\n'
        
        # Yield remaining buffer if any
        if buffer:
            yield buffer.decode(encoding, errors='replace')
    
    def seek(self, position: int) -> int:
        """Seek to position in file."""
        if self._file:
            self._file.seek(position)
            self._position = position
            return position
        return 0
    
    def tell(self) -> int:
        """Get current position."""
        return self._position


class MemoryMappedFile:
    """Memory-mapped file for efficient large file access."""
    
    def __init__(self, file_path: Union[str, Path], mode: str = 'r'):
        """
        Initialize memory-mapped file.
        
        Args:
            file_path: Path to file
            mode: Access mode ('r', 'r+', 'w+')
        """
        self.file_path = Path(file_path)
        self.mode = mode
        self._file: Optional[BinaryIO] = None
        self._mmap: Optional[mmap.mmap] = None
        
    def __enter__(self):
        if self.mode == 'r':
            self._file = open(self.file_path, 'rb')
            self._mmap = mmap.mmap(self._file.fileno(), 0, access=mmap.ACCESS_READ)
        elif self.mode in ('r+', 'w+'):
            self._file = open(self.file_path, 'r+b')
            self._mmap = mmap.mmap(self._file.fileno(), 0)
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._mmap:
            self._mmap.close()
        if self._file:
            self._file.close()
    
    def read(self, size: int = -1) -> bytes:
        """Read from memory-mapped file."""
        if not self._mmap:
            raise RuntimeError("MemoryMappedFile not opened")
        
        if size == -1:
            return self._mmap[:]
        else:
            current_pos = self._mmap.tell()
            return self._mmap[current_pos:current_pos + size]
    
    def readline(self) -> bytes:
        """Read a line from memory-mapped file."""
        if not self._mmap:
            raise RuntimeError("MemoryMappedFile not opened")
        
        return self._mmap.readline()
    
    def write(self, data: bytes) -> int:
        """Write to memory-mapped file."""
        if not self._mmap:
            raise RuntimeError("MemoryMappedFile not opened")
        
        return self._mmap.write(data)
    
    def seek(self, position: int) -> int:
        """Seek to position."""
        if self._mmap:
            self._mmap.seek(position)
            return position
        return 0
    
    def tell(self) -> int:
        """Get current position."""
        if self._mmap:
            return self._mmap.tell()
        return 0
    
    def size(self) -> int:
        """Get file size."""
        if self._mmap:
            return self._mmap.size()
        return 0


class BatchFileProcessor:
    """Batches file operations for improved I/O performance."""
    
    def __init__(self,
                 batch_size: int = 50,
                 batch_timeout: float = 1.0,
                 max_concurrent: int = 5):
        """
        Initialize batch processor.
        
        Args:
            batch_size: Maximum operations per batch
            batch_timeout: Maximum time to wait for batch
            max_concurrent: Maximum concurrent batches
        """
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.max_concurrent = max_concurrent
        
        self._operations: deque = deque()
        self._lock = threading.RLock()
        self._batch_thread: Optional[threading.Thread] = None
        self._running = False
        
        # Statistics
        self._stats = {
            "operations_batched": 0,
            "batches_processed": 0,
            "total_processing_time": 0.0,
            "avg_batch_size": 0.0
        }
        
        self._start_batch_processor()
        
        logger.debug("BatchFileProcessor initialized",
                    batch_size=batch_size,
                    batch_timeout=batch_timeout)
    
    def _start_batch_processor(self):
        """Start batch processing thread."""
        self._running = True
        self._batch_thread = threading.Thread(
            target=self._batch_worker,
            name="BatchFileProcessor",
            daemon=True
        )
        self._batch_thread.start()
    
    def _batch_worker(self):
        """Process batches of file operations."""
        try:
            while self._running:
                batch = self._collect_batch()
                if batch:
                    self._process_batch(batch)
                else:
                    time.sleep(0.1)  # No operations, brief pause
                    
        except Exception as e:
            logger.error("Batch processor error", error=str(e), exc_info=True)
    
    def _collect_batch(self) -> List[FileOperation]:
        """Collect operations for a batch."""
        batch = []
        start_time = time.time()
        
        with self._lock:
            # Collect operations until batch size or timeout
            while (len(batch) < self.batch_size and 
                   time.time() - start_time < self.batch_timeout):
                
                if self._operations:
                    batch.append(self._operations.popleft())
                else:
                    # No more operations, wait briefly
                    time.sleep(0.01)
                
                # Check if we should continue waiting
                if not self._operations and batch:
                    break
        
        return batch
    
    def _process_batch(self, batch: List[FileOperation]):
        """Process a batch of file operations."""
        if not batch:
            return
        
        start_time = time.time()
        
        try:
            # Group operations by type for efficiency
            read_ops = []
            write_ops = []
            stat_ops = []
            delete_ops = []
            
            for op in batch:
                if op.operation_type == 'read':
                    read_ops.append(op)
                elif op.operation_type == 'write':
                    write_ops.append(op)
                elif op.operation_type == 'stat':
                    stat_ops.append(op)
                elif op.operation_type == 'delete':
                    delete_ops.append(op)
            
            # Process each type in batch
            self._process_read_batch(read_ops)
            self._process_write_batch(write_ops)
            self._process_stat_batch(stat_ops)
            self._process_delete_batch(delete_ops)
            
            # Update statistics
            processing_time = time.time() - start_time
            with self._lock:
                self._stats["operations_batched"] += len(batch)
                self._stats["batches_processed"] += 1
                self._stats["total_processing_time"] += processing_time
                self._stats["avg_batch_size"] = (
                    self._stats["operations_batched"] / self._stats["batches_processed"]
                )
            
            logger.debug("Batch processed",
                        batch_size=len(batch),
                        processing_time=processing_time,
                        read_ops=len(read_ops),
                        write_ops=len(write_ops),
                        stat_ops=len(stat_ops),
                        delete_ops=len(delete_ops))
        
        except Exception as e:
            logger.error("Error processing batch",
                        batch_size=len(batch),
                        error=str(e),
                        exc_info=True)
    
    def _process_read_batch(self, operations: List[FileOperation]):
        """Process batch of read operations."""
        for op in operations:
            try:
                if op.file_path.exists():
                    with open(op.file_path, 'r', encoding=op.encoding) as f:
                        content = f.read()
                    
                    if op.callback:
                        op.callback(content, None)
                else:
                    error = FileNotFoundError(f"File not found: {op.file_path}")
                    if op.callback:
                        op.callback(None, error)
                        
            except Exception as e:
                logger.error("Read operation failed",
                           file_path=str(op.file_path),
                           error=str(e))
                if op.callback:
                    op.callback(None, e)
    
    def _process_write_batch(self, operations: List[FileOperation]):
        """Process batch of write operations."""
        for op in operations:
            try:
                # Ensure parent directory exists
                op.file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(op.file_path, 'w', encoding=op.encoding) as f:
                    f.write(op.data)
                
                if op.callback:
                    op.callback(True, None)
                    
            except Exception as e:
                logger.error("Write operation failed",
                           file_path=str(op.file_path),
                           error=str(e))
                if op.callback:
                    op.callback(False, e)
    
    def _process_stat_batch(self, operations: List[FileOperation]):
        """Process batch of stat operations."""
        for op in operations:
            try:
                stat_result = op.file_path.stat() if op.file_path.exists() else None
                
                if op.callback:
                    op.callback(stat_result, None)
                    
            except Exception as e:
                logger.error("Stat operation failed",
                           file_path=str(op.file_path),
                           error=str(e))
                if op.callback:
                    op.callback(None, e)
    
    def _process_delete_batch(self, operations: List[FileOperation]):
        """Process batch of delete operations."""
        for op in operations:
            try:
                success = False
                if op.file_path.exists():
                    if op.file_path.is_file():
                        op.file_path.unlink()
                        success = True
                    elif op.file_path.is_dir():
                        op.file_path.rmdir()
                        success = True
                
                if op.callback:
                    op.callback(success, None)
                    
            except Exception as e:
                logger.error("Delete operation failed",
                           file_path=str(op.file_path),
                           error=str(e))
                if op.callback:
                    op.callback(False, e)
    
    def submit_operation(self, operation: FileOperation) -> bool:
        """Submit file operation for batch processing."""
        with self._lock:
            if len(self._operations) >= self.batch_size * 10:  # Prevent unbounded growth
                logger.warning("Operation queue full, dropping operation",
                             file_path=str(operation.file_path),
                             operation_type=operation.operation_type)
                return False
            
            self._operations.append(operation)
            return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get batch processor statistics."""
        with self._lock:
            return {
                **self._stats.copy(),
                "pending_operations": len(self._operations),
                "running": self._running
            }
    
    def shutdown(self):
        """Shutdown batch processor."""
        self._running = False
        if self._batch_thread and self._batch_thread.is_alive():
            self._batch_thread.join(timeout=5.0)
        logger.debug("Batch processor shutdown completed")


class FileOptimizer:
    """
    Main file system optimizer with caching, batching, and streaming.
    """
    
    def __init__(self):
        """Initialize file optimizer."""
        self._batch_processor = BatchFileProcessor()
        self._cache_manager = get_cache_manager()
        self._telemetry = get_telemetry_manager()
        
        # File handle pool for reuse
        self._file_handles: Dict[str, Any] = {}
        self._handle_lock = threading.RLock()
        
        logger.info("FileOptimizer initialized")
    
    @memoize(cache_name="file_metadata", ttl=300.0)
    def get_file_info(self, file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        Get file information with caching.
        
        Args:
            file_path: Path to file
            
        Returns:
            File information dictionary
        """
        path = Path(file_path)
        
        try:
            if not path.exists():
                return None
            
            stat = path.stat()
            
            return {
                "size": stat.st_size,
                "modified_time": stat.st_mtime,
                "created_time": stat.st_ctime,
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
                "permissions": oct(stat.st_mode)[-3:],
                "path": str(path.absolute())
            }
            
        except Exception as e:
            logger.error("Error getting file info",
                        file_path=str(file_path),
                        error=str(e))
            return None
    
    def read_file_optimized(self,
                          file_path: Union[str, Path],
                          encoding: str = 'utf-8',
                          use_cache: bool = True,
                          stream: bool = False) -> Union[str, FileStreamReader, None]:
        """
        Read file with optimization strategies.
        
        Args:
            file_path: Path to file
            encoding: Text encoding
            use_cache: Whether to use cache
            stream: Whether to return stream reader
            
        Returns:
            File content, stream reader, or None
        """
        path = Path(file_path)
        path_str = str(path)
        
        # Check cache first if enabled
        if use_cache and not stream:
            cache = self._cache_manager.get_cache("file_content")
            if cache:
                cached_content = cache.get(path_str)
                if cached_content is not None:
                    logger.debug("File read from cache", file_path=path_str)
                    return cached_content
        
        try:
            # Record telemetry
            with self._telemetry.trace_boundary_call(
                "outbound", "file_system", str(path), "read"
            ) if self._telemetry else nullcontext():
                
                if stream:
                    # Return streaming reader for large files
                    return FileStreamReader(path)
                
                # Check file size for optimization strategy
                file_info = self.get_file_info(path)
                if not file_info:
                    return None
                
                file_size = file_info["size"]
                
                if file_size > 10 * 1024 * 1024:  # 10MB threshold
                    # Use memory mapping for large files
                    with MemoryMappedFile(path, 'r') as mmf:
                        content = mmf.read().decode(encoding, errors='replace')
                else:
                    # Regular read for small files
                    with open(path, 'r', encoding=encoding) as f:
                        content = f.read()
                
                # Cache the content if not too large
                if use_cache and file_size < 1024 * 1024:  # 1MB cache limit
                    cache = self._cache_manager.get_cache("file_content")
                    if cache:
                        # TTL based on file size (larger files cached shorter)
                        ttl = max(300, 3600 - (file_size // 1024))  # 5min to 1hour
                        cache.put(path_str, content, ttl=ttl)
                
                logger.debug("File read completed",
                           file_path=path_str,
                           size=file_size,
                           cached=use_cache)
                
                return content
        
        except Exception as e:
            logger.error("Error reading file",
                        file_path=path_str,
                        error=str(e))
            return None
    
    def write_file_optimized(self,
                           file_path: Union[str, Path],
                           content: str,
                           encoding: str = 'utf-8',
                           atomic: bool = True,
                           batch: bool = False) -> bool:
        """
        Write file with optimization strategies.
        
        Args:
            file_path: Path to file
            content: Content to write
            encoding: Text encoding
            atomic: Whether to use atomic write
            batch: Whether to batch the operation
            
        Returns:
            True if successful
        """
        path = Path(file_path)
        
        if batch:
            # Submit to batch processor
            operation = FileOperation(
                operation_type='write',
                file_path=path,
                data=content,
                encoding=encoding
            )
            return self._batch_processor.submit_operation(operation)
        
        try:
            # Record telemetry
            with self._telemetry.trace_boundary_call(
                "outbound", "file_system", str(path), "write"
            ) if self._telemetry else nullcontext():
                
                if atomic:
                    # Use atomic write for safety
                    from atomic_write import atomic_write
                    success = atomic_write(path, content, encoding=encoding)
                else:
                    # Direct write for performance
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, 'w', encoding=encoding) as f:
                        f.write(content)
                    success = True
                
                if success:
                    # Invalidate cache
                    cache = self._cache_manager.get_cache("file_content")
                    if cache:
                        cache.delete(str(path))
                    
                    logger.debug("File write completed",
                               file_path=str(path),
                               size=len(content),
                               atomic=atomic)
                
                return success
        
        except Exception as e:
            logger.error("Error writing file",
                        file_path=str(path),
                        error=str(e))
            return False
    
    def copy_file_optimized(self,
                          src_path: Union[str, Path],
                          dst_path: Union[str, Path],
                          chunk_size: int = 64 * 1024) -> bool:
        """
        Copy file with streaming for large files.
        
        Args:
            src_path: Source file path
            dst_path: Destination file path
            chunk_size: Size of chunks for streaming copy
            
        Returns:
            True if successful
        """
        src = Path(src_path)
        dst = Path(dst_path)
        
        try:
            # Ensure destination directory exists
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # Get source file size
            src_size = src.stat().st_size
            
            # Record telemetry
            with self._telemetry.trace_boundary_call(
                "outbound", "file_system", f"{src}->{dst}", "copy"
            ) if self._telemetry else nullcontext():
                
                if src_size > 100 * 1024 * 1024:  # 100MB threshold
                    # Streaming copy for large files
                    with open(src, 'rb') as src_file, open(dst, 'wb') as dst_file:
                        while True:
                            chunk = src_file.read(chunk_size)
                            if not chunk:
                                break
                            dst_file.write(chunk)
                else:
                    # Memory copy for small files
                    with open(src, 'rb') as src_file:
                        content = src_file.read()
                    with open(dst, 'wb') as dst_file:
                        dst_file.write(content)
                
                logger.debug("File copy completed",
                           src_path=str(src),
                           dst_path=str(dst),
                           size=src_size)
                
                return True
        
        except Exception as e:
            logger.error("Error copying file",
                        src_path=str(src),
                        dst_path=str(dst),
                        error=str(e))
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get optimizer statistics."""
        return {
            "batch_processor": self._batch_processor.get_stats(),
            "cache_manager": self._cache_manager.get_stats()
        }
    
    def shutdown(self):
        """Shutdown file optimizer."""
        self._batch_processor.shutdown()
        logger.info("File optimizer shutdown completed")


# Context manager for null context (Python 3.7+ has nullcontext)
class nullcontext:
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass


# Global file optimizer instance
_file_optimizer: Optional[FileOptimizer] = None
_optimizer_lock = threading.RLock()


def get_file_optimizer() -> FileOptimizer:
    """Get or create global file optimizer."""
    global _file_optimizer
    
    with _optimizer_lock:
        if _file_optimizer is None:
            _file_optimizer = FileOptimizer()
        
        return _file_optimizer


def shutdown_file_optimizer():
    """Shutdown the global file optimizer."""
    global _file_optimizer
    
    with _optimizer_lock:
        if _file_optimizer:
            _file_optimizer.shutdown()
            _file_optimizer = None