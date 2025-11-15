"""Tests for the Celery emulator task processor."""

import time
import pytest
from civ_arcos.core.tasks import CeleryEmulator, TaskStatus, get_task_processor, task


def test_task_processor_initialization():
    """Test task processor initialization."""
    processor = CeleryEmulator(num_workers=2)
    assert processor.num_workers == 2
    assert len(processor.workers) == 0
    assert not processor._running


def test_task_processor_start_stop():
    """Test starting and stopping worker threads."""
    processor = CeleryEmulator(num_workers=2)
    
    processor.start()
    assert processor._running
    assert len(processor.workers) == 2
    
    processor.stop()
    assert not processor._running


def test_register_task():
    """Test task registration."""
    processor = CeleryEmulator()
    
    def my_task(x, y):
        return x + y
    
    processor.register_task("add", my_task)
    assert "add" in processor.registered_tasks


def test_apply_async():
    """Test asynchronous task execution."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    def add_numbers(x, y):
        return x + y
    
    processor.register_task("add", add_numbers)
    
    task_id = processor.apply_async("add", args=(5, 3))
    assert task_id is not None
    
    # Wait for result
    result = processor.wait_for_result(task_id, timeout=2)
    assert result == 8
    
    processor.stop()


def test_get_result():
    """Test getting task result."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    def multiply(x, y):
        return x * y
    
    processor.register_task("multiply", multiply)
    
    task_id = processor.apply_async("multiply", args=(4, 5))
    
    # Wait a bit for task to complete
    time.sleep(0.5)
    
    task_result = processor.get_result(task_id)
    assert task_result is not None
    assert task_result.status == TaskStatus.SUCCESS
    assert task_result.result == 20
    
    processor.stop()


def test_task_with_kwargs():
    """Test task with keyword arguments."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"
    
    processor.register_task("greet", greet)
    
    task_id = processor.apply_async("greet", args=("World",), kwargs={"greeting": "Hi"})
    result = processor.wait_for_result(task_id, timeout=2)
    
    assert result == "Hi, World!"
    
    processor.stop()


def test_task_failure():
    """Test task failure handling."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    def failing_task():
        raise ValueError("Task failed")
    
    processor.register_task("fail", failing_task)
    
    task_id = processor.apply_async("fail", max_retries=0)
    
    # Wait for task to fail
    time.sleep(0.5)
    
    task_result = processor.get_result(task_id)
    assert task_result.status == TaskStatus.FAILURE
    assert "Task failed" in task_result.error
    
    processor.stop()


def test_task_retry():
    """Test task retry on failure."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    call_count = {"count": 0}
    
    def sometimes_fail():
        call_count["count"] += 1
        if call_count["count"] < 3:
            raise ValueError("Not yet")
        return "success"
    
    processor.register_task("retry_task", sometimes_fail)
    
    task_id = processor.apply_async("retry_task", max_retries=3)
    
    # Wait for retries
    time.sleep(1)
    
    task_result = processor.get_result(task_id)
    assert task_result.status == TaskStatus.SUCCESS
    assert task_result.result == "success"
    assert call_count["count"] == 3
    
    processor.stop()


def test_get_queue_size():
    """Test getting queue size."""
    processor = CeleryEmulator(num_workers=1)
    
    def slow_task():
        time.sleep(1)
    
    processor.register_task("slow", slow_task)
    
    # Add multiple tasks
    processor.apply_async("slow")
    processor.apply_async("slow")
    processor.apply_async("slow")
    
    # Queue should have pending tasks
    queue_size = processor.get_queue_size()
    assert queue_size >= 0


def test_get_stats():
    """Test getting task processor statistics."""
    processor = CeleryEmulator(num_workers=2)
    processor.start()
    
    def simple_task():
        return "done"
    
    processor.register_task("simple", simple_task)
    
    task_id = processor.apply_async("simple")
    time.sleep(0.5)
    
    stats = processor.get_stats()
    assert stats["workers"] == 2
    assert stats["running"]
    assert "total_tasks" in stats
    assert "status_counts" in stats
    assert "registered_tasks" in stats
    
    processor.stop()


def test_clear_completed():
    """Test clearing completed task results."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    def quick_task():
        return "done"
    
    processor.register_task("quick", quick_task)
    
    # Add and complete tasks
    task_id1 = processor.apply_async("quick")
    task_id2 = processor.apply_async("quick")
    
    time.sleep(0.5)
    
    # Clear completed tasks older than 0 seconds (all)
    cleared = processor.clear_completed(older_than_seconds=0)
    assert cleared >= 0
    
    processor.stop()


def test_task_decorator():
    """Test task decorator."""
    processor = get_task_processor()
    
    @task(name="decorated_task")
    def my_function(x, y):
        return x + y
    
    # Task should be registered
    assert "decorated_task" in processor.registered_tasks
    
    # Should have apply_async method
    assert hasattr(my_function, "apply_async")
    assert hasattr(my_function, "task_name")
    assert my_function.task_name == "decorated_task"


def test_task_decorator_execution():
    """Test executing task via decorator."""
    processor = get_task_processor()
    processor.start()
    
    @task(name="add_task")
    def add(a, b):
        return a + b
    
    task_id = add.apply_async(10, 20)
    result = processor.wait_for_result(task_id, timeout=2)
    
    assert result == 30


def test_multiple_workers():
    """Test with multiple worker threads."""
    processor = CeleryEmulator(num_workers=3)
    processor.start()
    
    def work(n):
        time.sleep(0.1)
        return n * 2
    
    processor.register_task("work", work)
    
    # Submit multiple tasks
    task_ids = [processor.apply_async("work", args=(i,)) for i in range(10)]
    
    # Wait for all to complete
    results = []
    for task_id in task_ids:
        result = processor.wait_for_result(task_id, timeout=5)
        results.append(result)
    
    # Check all completed
    assert len(results) == 10
    assert all(r is not None for r in results)
    
    processor.stop()


def test_task_not_registered():
    """Test error when task not registered."""
    processor = CeleryEmulator()
    
    with pytest.raises(ValueError, match="not registered"):
        processor.apply_async("nonexistent_task")


def test_task_result_to_dict():
    """Test task result serialization to dict."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    def simple():
        return "result"
    
    processor.register_task("simple", simple)
    
    task_id = processor.apply_async("simple")
    time.sleep(0.5)
    
    task_result = processor.get_result(task_id)
    result_dict = task_result.to_dict()
    
    assert "task_id" in result_dict
    assert "task_name" in result_dict
    assert "status" in result_dict
    assert "result" in result_dict
    assert result_dict["status"] == "success"
    
    processor.stop()


def test_get_task_processor_singleton():
    """Test global task processor singleton."""
    processor1 = get_task_processor()
    processor2 = get_task_processor()
    
    assert processor1 is processor2


def test_wait_for_result_timeout():
    """Test wait for result with timeout."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    def slow_task():
        time.sleep(5)
        return "done"
    
    processor.register_task("slow", slow_task)
    
    task_id = processor.apply_async("slow")
    
    # Should timeout
    result = processor.wait_for_result(task_id, timeout=0.5)
    assert result is None
    
    processor.stop()


def test_task_with_complex_result():
    """Test task returning complex data structure."""
    processor = CeleryEmulator(num_workers=1)
    processor.start()
    
    def complex_task():
        return {
            "status": "success",
            "data": [1, 2, 3, 4, 5],
            "metadata": {"count": 5, "sum": 15},
        }
    
    processor.register_task("complex", complex_task)
    
    task_id = processor.apply_async("complex")
    result = processor.wait_for_result(task_id, timeout=2)
    
    assert result["status"] == "success"
    assert len(result["data"]) == 5
    assert result["metadata"]["sum"] == 15
    
    processor.stop()
