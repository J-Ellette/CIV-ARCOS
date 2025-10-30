"""
Background task processor for asynchronous evidence collection.
Emulates Celery functionality without external dependencies.
"""

import uuid
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime, timezone
from threading import Thread, Lock
from queue import Queue, Empty
from enum import Enum


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    RETRY = "retry"


class TaskResult:
    """Represents the result of a background task."""

    def __init__(self, task_id: str, task_name: str):
        """
        Initialize task result.

        Args:
            task_id: Unique task identifier
            task_name: Name of the task
        """
        self.task_id = task_id
        self.task_name = task_name
        self.status = TaskStatus.PENDING
        self.result: Any = None
        self.error: Optional[str] = None
        self.created_at = datetime.now(timezone.utc)
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.retries = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "retries": self.retries,
            "duration_seconds": (
                (self.completed_at - self.started_at).total_seconds()
                if self.started_at and self.completed_at
                else None
            ),
        }


class Task:
    """Represents a background task."""

    def __init__(
        self,
        task_id: str,
        func: Callable,
        args: Tuple = (),
        kwargs: Dict[str, Any] = None,
        max_retries: int = 3,
    ):
        """
        Initialize task.

        Args:
            task_id: Unique task identifier
            func: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            max_retries: Maximum retry attempts
        """
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.max_retries = max_retries
        self.result = TaskResult(task_id, func.__name__)


class CeleryEmulator:
    """
    Background task processor emulating Celery functionality.
    Provides asynchronous task execution for evidence collection.
    """

    def __init__(self, num_workers: int = 4):
        """
        Initialize Celery emulator.

        Args:
            num_workers: Number of worker threads
        """
        self.num_workers = num_workers
        self.task_queue: Queue = Queue()
        self.workers: List[Thread] = []
        self.results: Dict[str, TaskResult] = {}
        self.registered_tasks: Dict[str, Callable] = {}
        self._lock = Lock()
        self._running = False

    def start(self) -> None:
        """Start worker threads."""
        if self._running:
            return

        self._running = True
        for i in range(self.num_workers):
            worker = Thread(target=self._worker_loop, args=(i,), daemon=True)
            worker.start()
            self.workers.append(worker)

    def stop(self) -> None:
        """Stop worker threads."""
        self._running = False
        # Wait for workers to finish
        for worker in self.workers:
            if worker.is_alive():
                worker.join(timeout=2)
        self.workers.clear()

    def register_task(self, name: str, func: Callable) -> None:
        """
        Register a task function.

        Args:
            name: Task name
            func: Function to register
        """
        with self._lock:
            self.registered_tasks[name] = func

    def apply_async(
        self,
        task_name: str,
        args: Tuple = (),
        kwargs: Dict[str, Any] = None,
        max_retries: int = 3,
    ) -> str:
        """
        Execute task asynchronously.

        Args:
            task_name: Name of registered task
            args: Positional arguments
            kwargs: Keyword arguments
            max_retries: Maximum retry attempts

        Returns:
            Task ID
        """
        if task_name not in self.registered_tasks:
            raise ValueError(f"Task '{task_name}' not registered")

        task_id = str(uuid.uuid4())
        func = self.registered_tasks[task_name]
        task = Task(task_id, func, args, kwargs or {}, max_retries)

        with self._lock:
            self.results[task_id] = task.result

        self.task_queue.put(task)
        return task_id

    def get_result(self, task_id: str) -> Optional[TaskResult]:
        """
        Get task result.

        Args:
            task_id: Task ID

        Returns:
            TaskResult or None if not found
        """
        with self._lock:
            return self.results.get(task_id)

    def wait_for_result(self, task_id: str, timeout: Optional[float] = None) -> Optional[Any]:
        """
        Wait for task to complete and return result.

        Args:
            task_id: Task ID
            timeout: Maximum time to wait in seconds

        Returns:
            Task result or None on timeout
        """
        start_time = time.time()
        while True:
            result = self.get_result(task_id)
            if result is None:
                return None

            if result.status in [TaskStatus.SUCCESS, TaskStatus.FAILURE]:
                return result.result if result.status == TaskStatus.SUCCESS else None

            if timeout and (time.time() - start_time) > timeout:
                return None

            time.sleep(0.1)

    def _worker_loop(self, worker_id: int) -> None:
        """
        Worker thread loop.

        Args:
            worker_id: Worker identifier
        """
        while self._running:
            try:
                task = self.task_queue.get(timeout=1)
            except Empty:
                continue

            self._execute_task(task, worker_id)
            self.task_queue.task_done()

    def _execute_task(self, task: Task, worker_id: int) -> None:
        """
        Execute a single task.

        Args:
            task: Task to execute
            worker_id: Worker identifier
        """
        task.result.status = TaskStatus.RUNNING
        task.result.started_at = datetime.now(timezone.utc)

        try:
            result = task.func(*task.args, **task.kwargs)
            task.result.status = TaskStatus.SUCCESS
            task.result.result = result
        except Exception as e:
            task.result.error = str(e)

            # Retry logic
            if task.result.retries < task.max_retries:
                task.result.retries += 1
                task.result.status = TaskStatus.RETRY
                # Re-queue for retry
                self.task_queue.put(task)
            else:
                task.result.status = TaskStatus.FAILURE

        task.result.completed_at = datetime.now(timezone.utc)

    def get_queue_size(self) -> int:
        """Get number of pending tasks."""
        return self.task_queue.qsize()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get task processor statistics.

        Returns:
            Statistics dictionary
        """
        with self._lock:
            total_tasks = len(self.results)
            status_counts = {status.value: 0 for status in TaskStatus}

            for result in self.results.values():
                status_counts[result.status.value] += 1

            return {
                "workers": self.num_workers,
                "running": self._running,
                "queue_size": self.get_queue_size(),
                "total_tasks": total_tasks,
                "status_counts": status_counts,
                "registered_tasks": list(self.registered_tasks.keys()),
            }

    def clear_completed(self, older_than_seconds: int = 3600) -> int:
        """
        Clear completed task results older than specified time.

        Args:
            older_than_seconds: Clear results older than this

        Returns:
            Number of results cleared
        """
        cutoff_time = datetime.now(timezone.utc).timestamp() - older_than_seconds
        cleared = 0

        with self._lock:
            to_remove = []
            for task_id, result in self.results.items():
                if result.status in [TaskStatus.SUCCESS, TaskStatus.FAILURE]:
                    if result.completed_at and result.completed_at.timestamp() < cutoff_time:
                        to_remove.append(task_id)

            for task_id in to_remove:
                del self.results[task_id]
                cleared += 1

        return cleared


# Global task processor instance
_task_processor: Optional[CeleryEmulator] = None


def get_task_processor() -> CeleryEmulator:
    """
    Get global task processor instance (singleton).

    Returns:
        CeleryEmulator instance
    """
    global _task_processor
    if _task_processor is None:
        _task_processor = CeleryEmulator()
        _task_processor.start()
    return _task_processor


# Decorator for registering tasks
def task(name: Optional[str] = None, max_retries: int = 3):
    """
    Decorator to register a function as a background task.

    Args:
        name: Optional task name (defaults to function name)
        max_retries: Maximum retry attempts

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        task_name = name or func.__name__
        processor = get_task_processor()
        processor.register_task(task_name, func)

        # Add convenience method to function
        def apply_async(*args, **kwargs):
            return processor.apply_async(task_name, args, kwargs, max_retries)

        func.apply_async = apply_async
        func.task_name = task_name
        return func

    return decorator
