#!/usr/bin/env python3
"""
Scribe Engine Cache Manager

Implements intelligent caching and memoization for performance optimization
with TTL, LRU eviction, memory management, and cache warming strategies.
"""

import time
import threading
import hashlib
import pickle
import weakref
from typing import Any, Dict, Optional, Callable, Union, TypeVar, Generic, List
from dataclasses import dataclass, field
from collections import OrderedDict
from functools import wraps, partial
import structlog

from .logging_config import get_scribe_logger
from .telemetry import get_telemetry_manager

logger = get_scribe_logger(__name__)

T = TypeVar('T')


@dataclass
class CacheEntry(Generic[T]):
    """Represents a cached value with metadata."""
    value: T
    created_at: float
    accessed_at: float
    access_count: int = 0
    ttl: Optional[float] = None
    size_bytes: int = 0
    
    @property
    def is_expired(self) -> bool:
        """Check if entry has expired based on TTL."""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl
    
    @property
    def age(self) -> float:
        """Get age of entry in seconds."""
        return time.time() - self.created_at
    
    def touch(self):
        """Update access time and count."""
        self.accessed_at = time.time()
        self.access_count += 1


class LRUCache:
    """
    LRU cache with TTL, size limits, and intelligent eviction.
    
    Features:
    - TTL-based expiration
    - Size-based eviction (LRU)
    - Memory usage tracking
    - Thread-safe operations
    - Cache statistics
    """
    
    def __init__(self,
                 max_size: int = 1000,
                 max_memory_mb: float = 100.0,
                 default_ttl: Optional[float] = 3600.0,
                 cleanup_interval: float = 300.0):
        """
        Initialize LRU cache.
        
        Args:
            max_size: Maximum number of entries
            max_memory_mb: Maximum memory usage in MB
            default_ttl: Default TTL in seconds (None = no expiration)
            cleanup_interval: Cleanup interval in seconds
        """
        self.max_size = max_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024)
        self.default_ttl = default_ttl
        self.cleanup_interval = cleanup_interval
        
        # Cache storage (key -> CacheEntry)
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        
        # Statistics
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "expirations": 0,
            "memory_bytes": 0,
            "cleanup_runs": 0
        }
        
        # Cleanup thread
        self._cleanup_thread: Optional[threading.Thread] = None
        self._running = False
        
        self._start_cleanup_thread()
        
        logger.debug("LRU cache initialized",
                    max_size=max_size,
                    max_memory_mb=max_memory_mb,
                    default_ttl=default_ttl)
    
    def _start_cleanup_thread(self):
        """Start background cleanup thread."""
        self._running = True
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_worker,
            name="CacheCleanup",
            daemon=True
        )
        self._cleanup_thread.start()
    
    def _cleanup_worker(self):
        """Background worker for cache cleanup."""
        try:
            while self._running:
                time.sleep(self.cleanup_interval)
                if self._running:
                    self._cleanup_expired()
                    
        except Exception as e:
            logger.error("Cache cleanup worker error", error=str(e))
    
    def _cleanup_expired(self):
        """Remove expired entries."""
        with self._lock:
            expired_keys = []
            for key, entry in self._cache.items():
                if entry.is_expired:
                    expired_keys.append(key)
            
            for key in expired_keys:
                entry = self._cache.pop(key, None)
                if entry:
                    self._stats["expirations"] += 1
                    self._stats["memory_bytes"] -= entry.size_bytes
            
            if expired_keys:
                self._stats["cleanup_runs"] += 1
                logger.debug("Cache cleanup completed",
                           expired_entries=len(expired_keys),
                           remaining_entries=len(self._cache))
    
    def _estimate_size(self, value: Any) -> int:
        """Estimate memory size of value in bytes."""
        try:
            # Use pickle to estimate serialized size
            return len(pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL))
        except Exception:
            # Fallback estimation
            if isinstance(value, str):
                return len(value.encode('utf-8'))
            elif isinstance(value, (int, float)):
                return 8
            elif isinstance(value, (list, tuple)):
                return sum(self._estimate_size(item) for item in value)
            elif isinstance(value, dict):
                return sum(self._estimate_size(k) + self._estimate_size(v) 
                          for k, v in value.items())
            else:
                return 64  # Default estimate
    
    def _evict_lru(self):
        """Evict least recently used entries to make space."""
        with self._lock:
            while (len(self._cache) >= self.max_size or 
                   self._stats["memory_bytes"] >= self.max_memory_bytes):
                
                if not self._cache:
                    break
                
                # Remove least recently used (first in OrderedDict)
                key, entry = self._cache.popitem(last=False)
                self._stats["evictions"] += 1
                self._stats["memory_bytes"] -= entry.size_bytes
                
                logger.debug("Cache entry evicted",
                           key=key,
                           age=entry.age,
                           access_count=entry.access_count)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                self._stats["misses"] += 1
                return None
            
            if entry.is_expired:
                # Remove expired entry
                del self._cache[key]
                self._stats["expirations"] += 1
                self._stats["memory_bytes"] -= entry.size_bytes
                self._stats["misses"] += 1
                return None
            
            # Move to end (most recently used)
            entry.touch()
            self._cache.move_to_end(key)
            self._stats["hits"] += 1
            
            return entry.value
    
    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None uses default)
            
        Returns:
            True if cached successfully
        """
        if ttl is None:
            ttl = self.default_ttl
        
        # Estimate size
        size_bytes = self._estimate_size(value)
        
        # Check if value is too large
        if size_bytes > self.max_memory_bytes:
            logger.warning("Value too large for cache",
                          key=key,
                          size_mb=size_bytes / 1024 / 1024,
                          max_mb=self.max_memory_bytes / 1024 / 1024)
            return False
        
        with self._lock:
            # Remove existing entry if present
            if key in self._cache:
                old_entry = self._cache[key]
                self._stats["memory_bytes"] -= old_entry.size_bytes
            
            # Create new entry
            entry = CacheEntry(
                value=value,
                created_at=time.time(),
                accessed_at=time.time(),
                ttl=ttl,
                size_bytes=size_bytes
            )
            
            # Add to cache
            self._cache[key] = entry
            self._stats["memory_bytes"] += size_bytes
            
            # Evict if necessary
            self._evict_lru()
            
            logger.debug("Cache entry stored",
                        key=key,
                        size_bytes=size_bytes,
                        ttl=ttl,
                        cache_size=len(self._cache))
            
            return True
    
    def delete(self, key: str) -> bool:
        """
        Delete entry from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if entry was deleted
        """
        with self._lock:
            entry = self._cache.pop(key, None)
            if entry:
                self._stats["memory_bytes"] -= entry.size_bytes
                logger.debug("Cache entry deleted", key=key)
                return True
            return False
    
    def clear(self):
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._stats["memory_bytes"] = 0
            logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self._stats["hits"] + self._stats["misses"]
            hit_rate = self._stats["hits"] / total_requests if total_requests > 0 else 0.0
            
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "memory_bytes": self._stats["memory_bytes"],
                "memory_mb": self._stats["memory_bytes"] / 1024 / 1024,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024,
                "hit_rate": hit_rate,
                **self._stats
            }
    
    def shutdown(self):
        """Shutdown cache and cleanup thread."""
        self._running = False
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=5.0)
        logger.debug("Cache shutdown completed")


class CacheManager:
    """
    Central cache manager with multiple cache instances and strategies.
    """
    
    def __init__(self):
        """Initialize cache manager."""
        self._caches: Dict[str, LRUCache] = {}
        self._lock = threading.RLock()
        
        # Default caches
        self._create_default_caches()
        
        logger.info("CacheManager initialized")
    
    def _create_default_caches(self):
        """Create default cache instances."""
        # File content cache
        self.create_cache(
            name="file_content",
            max_size=500,
            max_memory_mb=50.0,
            default_ttl=1800.0  # 30 minutes
        )
        
        # File metadata cache
        self.create_cache(
            name="file_metadata",
            max_size=2000,
            max_memory_mb=10.0,
            default_ttl=600.0  # 10 minutes
        )
        
        # Action results cache
        self.create_cache(
            name="action_results",
            max_size=1000,
            max_memory_mb=25.0,
            default_ttl=3600.0  # 1 hour
        )
        
        # Configuration cache
        self.create_cache(
            name="config",
            max_size=100,
            max_memory_mb=5.0,
            default_ttl=None  # No expiration
        )
    
    def create_cache(self,
                    name: str,
                    max_size: int = 1000,
                    max_memory_mb: float = 100.0,
                    default_ttl: Optional[float] = 3600.0) -> LRUCache:
        """
        Create a named cache instance.
        
        Args:
            name: Cache name
            max_size: Maximum number of entries
            max_memory_mb: Maximum memory usage in MB
            default_ttl: Default TTL in seconds
            
        Returns:
            LRU cache instance
        """
        with self._lock:
            if name in self._caches:
                raise ValueError(f"Cache '{name}' already exists")
            
            cache = LRUCache(
                max_size=max_size,
                max_memory_mb=max_memory_mb,
                default_ttl=default_ttl
            )
            
            self._caches[name] = cache
            logger.debug("Cache created", name=name)
            return cache
    
    def get_cache(self, name: str) -> Optional[LRUCache]:
        """Get cache instance by name."""
        with self._lock:
            return self._caches.get(name)
    
    def delete_cache(self, name: str) -> bool:
        """Delete a cache instance."""
        with self._lock:
            cache = self._caches.pop(name, None)
            if cache:
                cache.shutdown()
                logger.debug("Cache deleted", name=name)
                return True
            return False
    
    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all caches."""
        with self._lock:
            return {name: cache.get_stats() 
                   for name, cache in self._caches.items()}
    
    def clear_all(self):
        """Clear all caches."""
        with self._lock:
            for cache in self._caches.values():
                cache.clear()
            logger.info("All caches cleared")
    
    def shutdown(self):
        """Shutdown all caches."""
        with self._lock:
            for cache in self._caches.values():
                cache.shutdown()
            logger.info("Cache manager shutdown completed")


def memoize(cache_name: str = "default",
           ttl: Optional[float] = None,
           key_func: Optional[Callable] = None):
    """
    Decorator for memoizing function results.
    
    Args:
        cache_name: Name of cache to use
        ttl: Time to live for cached results
        key_func: Function to generate cache key from args/kwargs
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get cache instance
            cache_manager = get_cache_manager()
            cache = cache_manager.get_cache(cache_name)
            
            if cache is None:
                # No cache available, execute function directly
                return func(*args, **kwargs)
            
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                key_parts = [func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = hashlib.md5("|".join(key_parts).encode()).hexdigest()
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                logger.debug("Cache hit for memoized function",
                           function=func.__name__,
                           cache_key=cache_key)
                return result
            
            # Execute function and cache result
            logger.debug("Cache miss for memoized function",
                        function=func.__name__,
                        cache_key=cache_key)
            
            result = func(*args, **kwargs)
            cache.put(cache_key, result, ttl=ttl)
            
            return result
        
        # Add cache control methods to wrapper
        wrapper._cache_name = cache_name
        wrapper._original_func = func
        
        def invalidate_cache():
            """Clear all cached results for this function."""
            cache_manager = get_cache_manager()
            cache = cache_manager.get_cache(cache_name)
            if cache:
                # For simplicity, clear entire cache
                # In production, you might want more granular invalidation
                cache.clear()
        
        wrapper.invalidate_cache = invalidate_cache
        
        return wrapper
    
    return decorator


def cache_warm_up(cache_name: str, items: List[tuple]):
    """
    Warm up cache with pre-computed values.
    
    Args:
        cache_name: Name of cache to warm up
        items: List of (key, value, ttl) tuples
    """
    cache_manager = get_cache_manager()
    cache = cache_manager.get_cache(cache_name)
    
    if cache is None:
        logger.warning("Cache not found for warm-up", cache_name=cache_name)
        return
    
    warmed_count = 0
    for key, value, ttl in items:
        if cache.put(key, value, ttl=ttl):
            warmed_count += 1
    
    logger.info("Cache warm-up completed",
               cache_name=cache_name,
               items_warmed=warmed_count,
               total_items=len(items))


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None
_cache_lock = threading.RLock()


def get_cache_manager() -> CacheManager:
    """Get or create global cache manager."""
    global _cache_manager
    
    with _cache_lock:
        if _cache_manager is None:
            _cache_manager = CacheManager()
        
        return _cache_manager


def shutdown_cache_manager():
    """Shutdown the global cache manager."""
    global _cache_manager
    
    with _cache_lock:
        if _cache_manager:
            _cache_manager.shutdown()
            _cache_manager = None