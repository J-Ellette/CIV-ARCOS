#!/usr/bin/env python3
"""
Example usage of the infrastructure modules.
Demonstrates the core emulated infrastructure components.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from infrastructure.cache import RedisEmulator
from infrastructure.tasks import CeleryEmulator, Task
from infrastructure.graph import EvidenceGraph
from infrastructure.framework import Application, Request, Response

def example_cache():
    """Example: Using the Redis emulator."""
    print("=== Redis Emulator Example ===")
    
    # Create cache
    cache = RedisEmulator()
    
    # Set values
    cache.set("user:1:name", "Alice")
    cache.set("user:1:email", "alice@example.com")
    cache.set("session:abc123", "active", ttl=3600)  # Expires in 1 hour
    
    # Get values
    print(f"User name: {cache.get('user:1:name')}")
    print(f"User email: {cache.get('user:1:email')}")
    print(f"Session: {cache.get('session:abc123')}")
    
    # Delete value
    cache.delete("session:abc123")
    print(f"Session after delete: {cache.get('session:abc123')}")
    print()

def example_tasks():
    """Example: Using the Celery emulator."""
    print("=== Celery Emulator Example ===")
    
    # Create task queue
    celery = CeleryEmulator()
    
    # Define a task function
    def process_data(data):
        """Example task that processes data."""
        return f"Processed: {data}"
    
    # Register task
    celery.register_task("process_data", process_data)
    
    # Start worker
    celery.start()
    
    # Submit task
    task_id = celery.apply_async("process_data", args=("test data",))
    print(f"Task submitted: {task_id}")
    
    # Wait for completion
    import time
    time.sleep(0.5)
    
    # Get result
    result = celery.get_result(task_id)
    print(f"Task status: {result.status.value}")
    print(f"Task result: {result.result}")
    
    # Stop worker
    celery.stop()
    print()

def example_graph():
    """Example: Using the graph database emulator."""
    print("=== Graph Database Example ===")
    
    # Create graph
    graph = EvidenceGraph(storage_path=":memory:")
    
    # Create nodes
    e_node = graph.create_node("Evidence", {
        "type": "test_result",
        "status": "passed"
    })
    g_node = graph.create_node("Goal", {
        "description": "System is reliable"
    })
    
    print(f"Created evidence node: {e_node.id}")
    print(f"Created goal node: {g_node.id}")
    
    # Create relationship
    graph.create_relationship("SUPPORTS", e_node.id, g_node.id)
    
    # Query
    node = graph.get_node(e_node.id)
    print(f"Evidence node: {node.label if node else 'Not found'}")
    
    rels = graph.get_relationships(e_node.id)
    print(f"Number of relationships: {len(rels)}")
    print()

def example_framework():
    """Example: Using the web framework emulator."""
    print("=== Web Framework Example ===")
    
    # Create application
    app = Application()
    
    # Define route handler
    def hello_handler(request: Request) -> Response:
        name = request.query_params.get("name", "World")
        return Response(
            status_code=200,
            body={"message": f"Hello, {name}!"},
            headers={"Content-Type": "application/json"}
        )
    
    # Register route
    app.router.add_route("GET", "/hello", hello_handler)
    
    print("Web application configured")
    print("Routes:")
    for path, methods in app.router.routes.items():
        for method, handler in methods.items():
            print(f"  {method} {path} -> {handler.__name__}")
    print()

if __name__ == "__main__":
    example_cache()
    example_tasks()
    example_graph()
    example_framework()
    
    print("✓ All infrastructure examples completed successfully!")
