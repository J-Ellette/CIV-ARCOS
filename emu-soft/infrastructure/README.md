# Core Infrastructure

This directory contains emulations of core infrastructure components that form the foundation of CIV-ARCOS.

## Overview

The infrastructure components provide essential services without external dependencies. Each component emulates industry-standard tools while maintaining full control, transparency, and zero external service requirements.

## Components

### 1. cache.py - Redis Emulator

**Emulates:** Redis (in-memory data structure store)  
**Original Location:** `civ_arcos/core/cache.py`

**What it does:**
- In-memory caching with TTL (time-to-live) support
- Pub/sub messaging for real-time updates
- Key-value storage without requiring Redis server
- Thread-safe operations
- Automatic expiration handling

**Key Features:**
- **Operations**: SET, GET, DELETE, EXISTS, EXPIRE, TTL
- **Data Types**: Strings, lists, sets, hashes
- **TTL Support**: Automatic expiration after timeout
- **Pub/Sub**: Publish-subscribe messaging pattern
- **Persistence**: Optional disk persistence
- **Memory Management**: Automatic cleanup of expired keys

**Usage Example:**
```python
from civ_arcos.core.cache import RedisEmulator

cache = RedisEmulator()

# Basic operations
cache.set("key", "value", ttl=3600)  # Expires in 1 hour
value = cache.get("key")
cache.delete("key")

# Pub/Sub
def message_handler(channel, message):
    print(f"Received on {channel}: {message}")

cache.subscribe("updates", message_handler)
cache.publish("updates", {"event": "data_changed"})

# Check expiration
ttl = cache.ttl("key")  # Time remaining in seconds
exists = cache.exists("key")
```

### 2. tasks.py - Celery Emulator

**Emulates:** Celery (distributed task queue)  
**Original Location:** `civ_arcos/core/tasks.py`

**What it does:**
- Background task processing for asynchronous operations
- Task queues without RabbitMQ or Redis
- Worker thread management
- Task scheduling and retry logic
- Result tracking and retrieval

**Key Features:**
- **Task Definition**: Decorator-based task registration
- **Async Execution**: Background task processing
- **Queues**: Multiple named queues
- **Priority**: Task prioritization
- **Retry**: Automatic retry with exponential backoff
- **Results**: Task result storage and retrieval
- **Scheduling**: Delayed and periodic tasks
- **Workers**: Multi-threaded worker pool

**Usage Example:**
```python
from civ_arcos.core.tasks import TaskQueue, task

# Initialize queue
queue = TaskQueue(num_workers=4)
queue.start()

# Define task
@task(queue=queue, retry=3)
def process_evidence(evidence_id):
    """Process evidence in background."""
    # Long-running operation
    return {"processed": evidence_id}

# Submit task
task_id = process_evidence.delay(evidence_id="ev_001")

# Check status
result = queue.get_result(task_id)
status = queue.get_status(task_id)

# Wait for completion
final_result = queue.wait_for_result(task_id, timeout=60)
```

### 3. framework.py - Web Framework

**Emulates:** FastAPI / Flask / Django REST Framework  
**Original Location:** `civ_arcos/web/framework.py`

**What it does:**
- Minimal web framework for HTTP services
- Request/response handling
- URL routing with path parameters
- JSON serialization
- Middleware support
- Built on Python's http.server

**Key Features:**
- **Routing**: Decorator-based route registration
- **Methods**: GET, POST, PUT, DELETE, PATCH
- **Path Parameters**: URL parameter extraction
- **Query Parameters**: Query string parsing
- **JSON**: Automatic JSON request/response handling
- **Middleware**: Request/response processing pipeline
- **CORS**: Cross-origin resource sharing support
- **Static Files**: Static file serving

**Usage Example:**
```python
from civ_arcos.web.framework import create_app, Request, Response

app = create_app()

# Simple route
@app.get("/")
async def index(request: Request) -> Response:
    return Response({"message": "Hello, World!"})

# Path parameters
@app.get("/users/{user_id}")
async def get_user(request: Request, user_id: str) -> Response:
    return Response({"user_id": user_id})

# POST with JSON
@app.post("/api/data")
async def create_data(request: Request) -> Response:
    data = request.json()
    return Response({"created": data}, status_code=201)

# Middleware
@app.middleware
async def auth_middleware(request: Request, call_next):
    # Check authentication
    if not request.headers.get("Authorization"):
        return Response({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

### 4. graph.py - Graph Database

**Emulates:** Neo4j (graph database)  
**Original Location:** `civ_arcos/storage/graph.py`

**What it does:**
- Graph-based storage for evidence relationships
- Node and relationship management
- Property storage on nodes and relationships
- Graph traversal and path finding
- Persistence without Neo4j server

**Key Features:**
- **Nodes**: Create, update, delete, query nodes
- **Relationships**: Directional relationships with properties
- **Labels**: Node classification and indexing
- **Properties**: Flexible key-value properties
- **Queries**: Find nodes by label, traverse relationships
- **Paths**: Find paths between nodes
- **Persistence**: JSON-based disk storage
- **Indexing**: Label-based indexes for fast lookup

**Usage Example:**
```python
from civ_arcos.storage.graph import EvidenceGraph

graph = EvidenceGraph(storage_path="./data/evidence")

# Create nodes
goal_node = graph.create_node(
    label="Goal",
    properties={"title": "System is secure", "priority": "high"}
)

evidence_node = graph.create_node(
    label="Evidence",
    properties={"type": "security_scan", "score": 95}
)

# Create relationship
rel = graph.create_relationship(
    source_id=evidence_node.id,
    target_id=goal_node.id,
    rel_type="SUPPORTS",
    properties={"confidence": 0.95}
)

# Query nodes
goals = graph.find_nodes_by_label("Goal")
high_priority = [g for g in goals 
                 if g.properties.get("priority") == "high"]

# Traverse relationships
supported_by = graph.get_relationships(
    target_id=goal_node.id, 
    rel_type="SUPPORTS"
)

# Find paths
path = graph.find_path(evidence_node.id, goal_node.id)

# Save to disk
graph.save()
```

## Integration

These components work together seamlessly:

```python
from civ_arcos.core.cache import RedisEmulator
from civ_arcos.core.tasks import TaskQueue, task
from civ_arcos.web.framework import create_app, Request, Response
from civ_arcos.storage.graph import EvidenceGraph

# Initialize infrastructure
cache = RedisEmulator()
queue = TaskQueue(num_workers=4)
queue.start()
graph = EvidenceGraph(storage_path="./data")
app = create_app()

# Define background task
@task(queue=queue)
def process_evidence(evidence_id):
    # Get from cache
    data = cache.get(f"evidence:{evidence_id}")
    
    # Process and store in graph
    node = graph.create_node("Evidence", properties=data)
    
    # Notify subscribers
    cache.publish("evidence_processed", {"id": evidence_id})
    
    return {"node_id": node.id}

# API endpoint
@app.post("/api/evidence")
async def submit_evidence(request: Request) -> Response:
    data = request.json()
    
    # Cache immediately
    evidence_id = data["id"]
    cache.set(f"evidence:{evidence_id}", data, ttl=3600)
    
    # Process in background
    task_id = process_evidence.delay(evidence_id)
    
    return Response({
        "evidence_id": evidence_id,
        "task_id": task_id,
        "status": "queued"
    }, status_code=202)
```

## Performance Characteristics

| Component | Operation | Speed | Memory |
|-----------|-----------|-------|--------|
| Cache | GET/SET | ~0.1ms | Low |
| Cache | Pub/Sub | ~1ms | Low |
| Tasks | Submit | ~1ms | Medium |
| Tasks | Execute | Varies | Medium |
| Framework | Request | ~5ms | Low |
| Framework | JSON | ~1ms | Low |
| Graph | Create Node | ~1ms | Low |
| Graph | Query | ~5-50ms | Medium |

## Design Philosophy

### No External Services
- All components run in-process
- No Docker containers required
- No external servers needed
- Simple deployment

### Production-Ready
- Thread-safe operations
- Error handling and recovery
- Resource cleanup
- Proper shutdown handling

### Transparent and Simple
- Easy to understand implementation
- No "magic" behind the scenes
- Full control over behavior
- Easy to debug

### Zero Dependencies
- Built on Python standard library
- No pip install requirements (beyond dev tools)
- Self-contained implementation
- Portable across environments

## Related Documentation

- See `../details.md` for comprehensive documentation
- See `build-docs/STEP1_COMPLETE.md` for graph database and framework details
- See API documentation for web framework endpoints

## Testing

All infrastructure components have comprehensive unit tests:
- `tests/unit/test_cache.py`
- `tests/unit/test_tasks.py`
- `tests/unit/test_framework.py`
- `tests/unit/test_graph.py`

Run tests:
```bash
pytest tests/unit/test_cache.py -v
pytest tests/unit/test_tasks.py -v
```

## Performance Tuning

### Cache
```python
# Adjust cleanup interval
cache = RedisEmulator(cleanup_interval=60)  # Check every 60s

# Set max memory
cache = RedisEmulator(max_memory_mb=512)  # Limit to 512MB
```

### Tasks
```python
# Adjust worker count
queue = TaskQueue(num_workers=8)  # More workers for CPU-bound tasks

# Set queue size
queue = TaskQueue(max_queue_size=1000)  # Limit pending tasks
```

### Graph
```python
# Enable in-memory mode for speed
graph = EvidenceGraph(storage_path="./data", in_memory=True)

# Batch operations
with graph.batch_mode():
    for data in large_dataset:
        graph.create_node("Evidence", properties=data)
```

## License

Original implementations for the CIV-ARCOS project. While they emulate the functionality of existing tools, they contain no copied code.
