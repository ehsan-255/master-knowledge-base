#!/usr/bin/env python3
"""
Scribe Engine Async Processing Pipeline

Implements high-performance asynchronous processing for file events and actions
with concurrent execution, backpressure handling, and resource management.
"""

import asyncio
import threading
import time
from typing import Dict, Any, Optional, List, Callable, Union, Awaitable
from dataclasses import dataclass
from enum import Enum
import structlog
from concurrent.futures import ThreadPoolExecutor

from .logging_config import get_scribe_logger
from .telemetry import get_telemetry_manager
from .error_recovery import handle_error

logger = get_scribe_logger(__name__)


class TaskPriority(Enum):
    """Task priority levels for processing order."""
    LOW = 1
    NORMAL = 5
    HIGH = 8
    CRITICAL = 10


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AsyncTask:
    """Represents an asynchronous task in the processing pipeline."""
    task_id: str
    task_type: str
    priority: TaskPriority
    payload: Dict[str, Any]
    callback: Optional[Callable] = None
    created_at: float = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    status: TaskStatus = TaskStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    error: Optional[Exception] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
    
    @property
    def duration(self) -> Optional[float]:
        """Get task execution duration."""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None
    
    @property
    def wait_time(self) -> Optional[float]:
        """Get time spent waiting in queue."""
        if self.started_at:
            return self.started_at - self.created_at
        return None


class AsyncTaskQueue:
    """Priority queue for async tasks with backpressure handling."""
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize async task queue.
        
        Args:
            max_size: Maximum queue size for backpressure
        """
        self.max_size = max_size
        self._queue = asyncio.PriorityQueue(maxsize=max_size)
        self._lock = asyncio.Lock()
        self._task_counter = 0
        
        logger.debug("AsyncTaskQueue initialized", max_size=max_size)
    
    async def put(self, task: AsyncTask) -> bool:
        """
        Add task to queue with backpressure handling.
        
        Args:
            task: Task to add
            
        Returns:
            True if task was added, False if queue is full
        """
        try:
            # Check queue size for backpressure
            if self._queue.qsize() >= self.max_size:
                logger.warning("Task queue full, dropping task",
                             task_id=task.task_id,
                             queue_size=self._queue.qsize())
                return False
            
            # Priority queue item: (priority, insertion_order, task)
            priority_value = -task.priority.value  # Negative for descending order
            async with self._lock:
                self._task_counter += 1
                await self._queue.put((priority_value, self._task_counter, task))
            
            logger.debug("Task queued",
                        task_id=task.task_id,
                        priority=task.priority.value,
                        queue_size=self._queue.qsize())
            return True
            
        except Exception as e:
            logger.error("Error queuing task",
                        task_id=task.task_id,
                        error=str(e))
            return False
    
    async def get(self) -> Optional[AsyncTask]:
        """Get next task from queue."""
        try:
            priority, order, task = await self._queue.get()
            
            logger.debug("Task dequeued",
                        task_id=task.task_id,
                        priority=task.priority.value,
                        queue_size=self._queue.qsize())
            
            return task
            
        except Exception as e:
            logger.error("Error dequeuing task", error=str(e))
            return None
    
    def qsize(self) -> int:
        """Get current queue size."""
        return self._queue.qsize()
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()
    
    def full(self) -> bool:
        """Check if queue is full."""
        return self._queue.qsize() >= self.max_size


class AsyncProcessor:
    """
    High-performance async processor for Scribe Engine.
    
    Implements concurrent processing with configurable worker pools,
    priority queues, backpressure handling, and resource management.
    """
    
    def __init__(self,
                 max_workers: int = 10,
                 max_queue_size: int = 1000,
                 worker_timeout: float = 300.0):
        """
        Initialize async processor.
        
        Args:
            max_workers: Maximum number of async workers
            max_queue_size: Maximum task queue size
            worker_timeout: Timeout for worker tasks
        """
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size
        self.worker_timeout = worker_timeout
        
        # Async components
        self._task_queue = AsyncTaskQueue(max_queue_size)
        self._workers: List[asyncio.Task] = []
        self._running = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        
        # Thread pool for CPU-bound tasks
        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        
        # Task registry and stats
        self._active_tasks: Dict[str, AsyncTask] = {}
        self._completed_tasks: Dict[str, AsyncTask] = {}
        self._task_handlers: Dict[str, Callable] = {}
        
        # Metrics
        self._stats = {
            "tasks_processed": 0,
            "tasks_failed": 0,
            "tasks_cancelled": 0,
            "total_processing_time": 0.0,
            "avg_processing_time": 0.0,
            "queue_high_water_mark": 0
        }
        
        # Thread safety
        self._lock = threading.RLock()
        
        logger.info("AsyncProcessor initialized",
                   max_workers=max_workers,
                   max_queue_size=max_queue_size,
                   worker_timeout=worker_timeout)
    
    def register_handler(self, task_type: str, handler: Callable):
        """
        Register a handler function for a task type.
        
        Args:
            task_type: Type of task to handle
            handler: Async or sync function to handle the task
        """
        with self._lock:
            self._task_handlers[task_type] = handler
            logger.debug("Registered task handler",
                        task_type=task_type,
                        handler_name=handler.__name__)
    
    def start(self):
        """Start the async processor."""
        if self._running:
            return
        
        self._running = True
        
        # Start async event loop in separate thread
        self._thread = threading.Thread(
            target=self._run_event_loop,
            name="AsyncProcessor",
            daemon=True
        )
        self._thread.start()
        
        logger.info("AsyncProcessor started")
    
    def stop(self):
        """Stop the async processor gracefully."""
        if not self._running:
            return
        
        self._running = False
        
        # Stop event loop
        if self._loop and not self._loop.is_closed():
            self._loop.call_soon_threadsafe(self._loop.stop)
        
        # Wait for thread to finish
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=10.0)
        
        # Shutdown thread pool
        self._thread_pool.shutdown(wait=True)
        
        logger.info("AsyncProcessor stopped")
    
    def _run_event_loop(self):
        """Run the async event loop."""
        try:
            # Create new event loop for this thread
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            
            # Start worker tasks
            for i in range(self.max_workers):
                worker = self._loop.create_task(self._worker(f"worker-{i}"))
                self._workers.append(worker)
            
            # Start stats collector
            stats_task = self._loop.create_task(self._stats_collector())
            
            # Run until stopped
            self._loop.run_forever()
            
            # Cancel all tasks when stopping
            for worker in self._workers:
                worker.cancel()
            
            stats_task.cancel()
            
            # Wait for tasks to complete
            pending = [task for task in self._workers + [stats_task] if not task.done()]
            if pending:
                self._loop.run_until_complete(
                    asyncio.gather(*pending, return_exceptions=True)
                )
            
        except Exception as e:
            logger.error("Error in async event loop", error=str(e), exc_info=True)
        finally:
            if self._loop and not self._loop.is_closed():
                self._loop.close()
    
    async def _worker(self, worker_name: str):
        """Async worker that processes tasks from the queue."""
        logger.debug("Async worker started", worker_name=worker_name)
        
        try:
            while self._running:
                try:
                    # Get next task from queue
                    task = await asyncio.wait_for(
                        self._task_queue.get(),
                        timeout=1.0
                    )
                    
                    if task is None:
                        continue
                    
                    # Process the task
                    await self._process_task(task, worker_name)
                    
                except asyncio.TimeoutError:
                    # No task available, continue
                    continue
                except Exception as e:
                    logger.error("Worker error",
                                worker_name=worker_name,
                                error=str(e),
                                exc_info=True)
        
        except asyncio.CancelledError:
            logger.debug("Async worker cancelled", worker_name=worker_name)
        except Exception as e:
            logger.error("Async worker failed",
                        worker_name=worker_name,
                        error=str(e),
                        exc_info=True)
        finally:
            logger.debug("Async worker stopped", worker_name=worker_name)
    
    async def _process_task(self, task: AsyncTask, worker_name: str):
        """Process a single task."""
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        
        # Add to active tasks
        with self._lock:
            self._active_tasks[task.task_id] = task
        
        # Record telemetry
        telemetry = get_telemetry_manager()
        
        try:
            logger.debug("Processing task",
                        task_id=task.task_id,
                        task_type=task.task_type,
                        worker_name=worker_name,
                        wait_time=task.wait_time)
            
            # Get handler for task type
            handler = self._task_handlers.get(task.task_type)
            if not handler:
                raise ValueError(f"No handler registered for task type: {task.task_type}")
            
            # Execute handler with timeout
            if asyncio.iscoroutinefunction(handler):
                # Async handler
                result = await asyncio.wait_for(
                    handler(task),
                    timeout=self.worker_timeout
                )
            else:
                # Sync handler - run in thread pool
                result = await self._loop.run_in_executor(
                    self._thread_pool,
                    handler,
                    task
                )
            
            # Task completed successfully
            task.status = TaskStatus.COMPLETED
            task.completed_at = time.time()
            
            # Call callback if provided
            if task.callback:
                try:
                    if asyncio.iscoroutinefunction(task.callback):
                        await task.callback(task, result)
                    else:
                        await self._loop.run_in_executor(
                            self._thread_pool,
                            task.callback,
                            task,
                            result
                        )
                except Exception as e:
                    logger.warning("Task callback failed",
                                  task_id=task.task_id,
                                  error=str(e))
            
            # Update stats
            with self._lock:
                self._stats["tasks_processed"] += 1
                if task.duration:
                    self._stats["total_processing_time"] += task.duration
                    self._stats["avg_processing_time"] = (
                        self._stats["total_processing_time"] / self._stats["tasks_processed"]
                    )
            
            # Record successful telemetry
            if telemetry:
                telemetry.action_executions_counter.add(1, {
                    "task_type": task.task_type,
                    "status": "success",
                    "worker": worker_name
                })
                
                if task.duration:
                    telemetry.action_duration_histogram.record(task.duration, {
                        "task_type": task.task_type,
                        "status": "success"
                    })
            
            logger.debug("Task completed successfully",
                        task_id=task.task_id,
                        duration=task.duration,
                        worker_name=worker_name)
        
        except asyncio.TimeoutError:
            task.status = TaskStatus.FAILED
            task.error = Exception(f"Task timeout after {self.worker_timeout}s")
            task.completed_at = time.time()
            
            with self._lock:
                self._stats["tasks_failed"] += 1
            
            logger.error("Task timed out",
                        task_id=task.task_id,
                        timeout=self.worker_timeout,
                        worker_name=worker_name)
            
            # Handle error through recovery system
            handle_error("async_processor", "task_execution", task.error, {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "worker": worker_name
            })
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = e
            task.completed_at = time.time()
            
            with self._lock:
                self._stats["tasks_failed"] += 1
            
            # Record failed telemetry
            if telemetry:
                telemetry.action_failures_counter.add(1, {
                    "task_type": task.task_type,
                    "error_type": type(e).__name__,
                    "worker": worker_name
                })
                
                if task.duration:
                    telemetry.action_duration_histogram.record(task.duration, {
                        "task_type": task.task_type,
                        "status": "error"
                    })
            
            logger.error("Task failed",
                        task_id=task.task_id,
                        task_type=task.task_type,
                        error=str(e),
                        worker_name=worker_name,
                        exc_info=True)
            
            # Handle error through recovery system
            handle_error("async_processor", "task_execution", e, {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "worker": worker_name
            })
        
        finally:
            # Move from active to completed
            with self._lock:
                if task.task_id in self._active_tasks:
                    del self._active_tasks[task.task_id]
                self._completed_tasks[task.task_id] = task
                
                # Limit completed tasks history
                if len(self._completed_tasks) > 1000:
                    oldest_task_id = min(self._completed_tasks.keys(), 
                                       key=lambda k: self._completed_tasks[k].created_at)
                    del self._completed_tasks[oldest_task_id]
    
    async def _stats_collector(self):
        """Collect and update processor statistics."""
        try:
            while self._running:
                await asyncio.sleep(10.0)  # Update every 10 seconds
                
                # Update queue metrics
                queue_size = self._task_queue.qsize()
                with self._lock:
                    if queue_size > self._stats["queue_high_water_mark"]:
                        self._stats["queue_high_water_mark"] = queue_size
                
                # Update telemetry
                telemetry = get_telemetry_manager()
                if telemetry:
                    telemetry.queue_size_gauge.set(queue_size)
                    telemetry.active_workers_gauge.set(len(self._active_tasks))
                
                logger.debug("Processor stats updated",
                           queue_size=queue_size,
                           active_tasks=len(self._active_tasks),
                           completed_tasks=len(self._completed_tasks))
        
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("Stats collector error", error=str(e))
    
    def submit_task(self,
                   task_type: str,
                   payload: Dict[str, Any],
                   priority: TaskPriority = TaskPriority.NORMAL,
                   callback: Optional[Callable] = None,
                   task_id: Optional[str] = None) -> str:
        """
        Submit a task for async processing.
        
        Args:
            task_type: Type of task
            payload: Task payload data
            priority: Task priority
            callback: Optional callback function
            task_id: Optional custom task ID
            
        Returns:
            Task ID for tracking
        """
        if task_id is None:
            task_id = f"{task_type}_{int(time.time() * 1000000)}"
        
        task = AsyncTask(
            task_id=task_id,
            task_type=task_type,
            priority=priority,
            payload=payload,
            callback=callback
        )
        
        # Submit to event loop
        if self._loop and self._running:
            future = asyncio.run_coroutine_threadsafe(
                self._task_queue.put(task),
                self._loop
            )
            
            try:
                success = future.result(timeout=1.0)
                if success:
                    logger.debug("Task submitted",
                               task_id=task_id,
                               task_type=task_type,
                               priority=priority.value)
                    return task_id
                else:
                    raise Exception("Failed to queue task - queue full")
            except Exception as e:
                logger.error("Failed to submit task",
                           task_id=task_id,
                           error=str(e))
                raise
        else:
            raise RuntimeError("AsyncProcessor not running")
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get status of a task."""
        with self._lock:
            if task_id in self._active_tasks:
                return self._active_tasks[task_id].status
            elif task_id in self._completed_tasks:
                return self._completed_tasks[task_id].status
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processor statistics."""
        with self._lock:
            return {
                **self._stats.copy(),
                "active_tasks": len(self._active_tasks),
                "completed_tasks": len(self._completed_tasks),
                "queue_size": self._task_queue.qsize(),
                "workers_count": len(self._workers),
                "running": self._running
            }


# Global async processor instance
_async_processor: Optional[AsyncProcessor] = None
_processor_lock = threading.RLock()


def get_async_processor() -> Optional[AsyncProcessor]:
    """Get the global async processor instance."""
    return _async_processor


def initialize_async_processor(max_workers: int = 10,
                             max_queue_size: int = 1000,
                             worker_timeout: float = 300.0) -> AsyncProcessor:
    """
    Initialize global async processor.
    
    Args:
        max_workers: Maximum number of async workers
        max_queue_size: Maximum task queue size
        worker_timeout: Timeout for worker tasks
        
    Returns:
        AsyncProcessor instance
    """
    global _async_processor
    
    with _processor_lock:
        if _async_processor is None:
            _async_processor = AsyncProcessor(
                max_workers=max_workers,
                max_queue_size=max_queue_size,
                worker_timeout=worker_timeout
            )
            _async_processor.start()
        
        return _async_processor


def shutdown_async_processor():
    """Shutdown the global async processor."""
    global _async_processor
    
    with _processor_lock:
        if _async_processor:
            _async_processor.stop()
            _async_processor = None