# TracAgg - Distributed Tracing Aggregator for Microservices

**Homegrown distributed tracing solution for microservices architectures**

## Overview

TracAgg is a distributed tracing aggregator that collects, analyzes, and visualizes traces across microservice architectures. It emulates and recreates functionality from industry-standard tools like Jaeger and Zipkin, providing comprehensive trace collection, aggregation, and performance analysis capabilities.

## Purpose

In modern microservice architectures, understanding request flows and identifying performance bottlenecks requires distributed tracing. TracAgg provides:

- **Trace Aggregation**: Collect and aggregate spans from multiple services
- **Dependency Analysis**: Identify service-to-service communication patterns
- **Performance Analysis**: Analyze trace performance and identify bottlenecks
- **Critical Path Analysis**: Find the longest path through distributed requests
- **Service Statistics**: Track per-service performance metrics

## Features

### 1. Trace Aggregation (`TraceAggregator`)

Collect and aggregate distributed traces from multiple microservices:

```python
from tracagg import TraceAggregator, create_span, create_trace_id, SpanKind

aggregator = TraceAggregator()

# Create a trace
trace_id = create_trace_id()

# Create spans for different services
api_span = create_span(
    trace_id=trace_id,
    service_name="api-gateway",
    operation_name="GET /users",
    duration_ms=250.0,
    kind=SpanKind.SERVER
)

user_span = create_span(
    trace_id=trace_id,
    service_name="user-service",
    operation_name="get_users",
    duration_ms=150.0,
    parent_span_id=api_span.span_id,
    kind=SpanKind.SERVER
)

# Ingest spans
aggregator.ingest_spans([api_span, user_span])

# Complete the trace
trace = aggregator.complete_trace(trace_id)
print(f"Trace duration: {trace.duration_ms}ms")
print(f"Services involved: {trace.services}")
```

**Key Capabilities:**
- Ingest spans from multiple services
- Aggregate spans into complete traces
- Track service statistics
- Query traces with filters

### 2. Query Traces

Search and filter traces based on various criteria:

```python
# Query traces by service
traces = aggregator.query_traces(
    service_name="user-service",
    min_duration_ms=100.0,
    limit=50
)

# Query traces with errors
error_traces = aggregator.query_traces(
    has_errors=True
)

# Query slow traces
slow_traces = aggregator.query_traces(
    min_duration_ms=1000.0
)
```

**Query Parameters:**
- `service_name`: Filter by service name
- `operation_name`: Filter by operation name
- `min_duration_ms`: Minimum trace duration
- `max_duration_ms`: Maximum trace duration
- `has_errors`: Filter traces with/without errors
- `limit`: Maximum number of traces to return

### 3. Service Statistics

Get performance statistics for services:

```python
# Get statistics for all services
all_stats = aggregator.get_service_statistics()

# Get statistics for a specific service
user_service_stats = aggregator.get_service_statistics("user-service")

print(f"Average duration: {user_service_stats['user-service']['avg_duration_ms']}ms")
print(f"Total spans: {user_service_stats['user-service']['span_count']}")
print(f"Error count: {user_service_stats['user-service']['error_count']}")
```

**Statistics Include:**
- Total span count
- Error count
- Average duration
- Total duration
- Operations performed

### 4. Dependency Analysis (`TraceDependencyAnalyzer`)

Analyze service dependencies and communication patterns:

```python
from tracagg import TraceDependencyAnalyzer

analyzer = TraceDependencyAnalyzer()

# Analyze a trace to extract dependencies
analyzer.analyze_trace(trace)

# Get all service dependencies
dependencies = analyzer.get_dependencies()
# Returns: [{'from_service': 'api-gateway', 'to_service': 'user-service', 'call_count': 5}]

# Get service dependency graph
service_graph = analyzer.get_service_graph()
# Returns: {'api-gateway': ['user-service', 'auth-service'], ...}
```

**Analysis Features:**
- Identify cross-service dependencies
- Count service-to-service calls
- Build service dependency graph
- Find critical paths through traces

### 5. Critical Path Analysis

Find the critical path (longest path) through a distributed trace:

```python
analyzer = TraceDependencyAnalyzer()
critical_path = analyzer.find_critical_path(trace)

for span in critical_path:
    print(f"{span.service_name}:{span.operation_name} - {span.duration_ms}ms")
```

The critical path represents the sequence of operations that determines the total trace duration.

### 6. Performance Analysis (`TracePerformanceAnalyzer`)

Analyze trace performance and identify bottlenecks:

```python
from tracagg import TracePerformanceAnalyzer

perf_analyzer = TracePerformanceAnalyzer()

# Analyze multiple traces
results = perf_analyzer.analyze_traces(traces)

print(f"Total traces analyzed: {results['total_traces']}")
print(f"Error rate: {results['error_rate']:.2%}")

# View slowest operations
for op in results['slowest_operations']:
    print(f"{op['operation']}: P95={op['p95_ms']}ms, P99={op['p99_ms']}ms")
```

**Performance Metrics:**
- Min, max, average, median durations
- P95 and P99 percentiles
- Standard deviation
- Error rate
- Slowest operations

### 7. Bottleneck Identification

Identify specific performance bottlenecks in a trace:

```python
# Identify spans that take longer than 100ms
bottlenecks = perf_analyzer.identify_bottlenecks(trace, threshold_ms=100.0)

for bottleneck in bottlenecks:
    print(f"{bottleneck['service']}:{bottleneck['operation']}")
    print(f"  Duration: {bottleneck['duration_ms']}ms")
    print(f"  % of trace: {bottleneck['percentage_of_trace']:.1f}%")
```

## Data Models

### Span

Represents a single operation in a distributed trace:

```python
@dataclass
class Span:
    trace_id: str              # Unique trace identifier
    span_id: str               # Unique span identifier
    parent_span_id: Optional[str]  # Parent span ID
    name: str                  # Span name
    kind: SpanKind            # SERVER, CLIENT, INTERNAL, etc.
    start_time: str           # ISO format timestamp
    end_time: Optional[str]   # ISO format timestamp
    duration_ms: float        # Duration in milliseconds
    status: SpanStatus        # OK, ERROR, UNSET
    service_name: str         # Service that created the span
    operation_name: str       # Operation being performed
    attributes: Dict[str, Any]  # Additional metadata
    events: List[SpanEvent]   # Events during span execution
    tags: Dict[str, str]      # Tags for categorization
```

### Trace

Represents a complete distributed trace:

```python
@dataclass
class Trace:
    trace_id: str             # Unique trace identifier
    spans: List[Span]         # All spans in the trace
    root_span: Optional[Span] # Root span (no parent)
    start_time: str           # Trace start time
    end_time: str             # Trace end time
    duration_ms: float        # Total trace duration
    service_count: int        # Number of services involved
    span_count: int           # Total number of spans
    error_count: int          # Number of spans with errors
    services: List[str]       # List of services in trace
```

## Span Types

TracAgg supports standard span kinds:

- **SERVER**: Server-side span (handles requests)
- **CLIENT**: Client-side span (makes requests)
- **PRODUCER**: Producer span (sends messages)
- **CONSUMER**: Consumer span (receives messages)
- **INTERNAL**: Internal operation

## Example: Complete Distributed Trace

```python
from tracagg import (
    TraceAggregator, TraceDependencyAnalyzer, TracePerformanceAnalyzer,
    create_span, create_trace_id, SpanKind, SpanStatus
)

# Initialize components
aggregator = TraceAggregator()
dep_analyzer = TraceDependencyAnalyzer()
perf_analyzer = TracePerformanceAnalyzer()

# Create a distributed trace
trace_id = create_trace_id()

# API Gateway receives request
api_span = create_span(
    trace_id=trace_id,
    service_name="api-gateway",
    operation_name="GET /orders",
    duration_ms=500.0,
    kind=SpanKind.SERVER,
    attributes={"http.method": "GET", "http.url": "/orders", "user_id": "123"}
)

# Auth service verifies token
auth_span = create_span(
    trace_id=trace_id,
    service_name="auth-service",
    operation_name="verify_token",
    duration_ms=50.0,
    parent_span_id=api_span.span_id,
    kind=SpanKind.INTERNAL
)

# Order service fetches orders
order_span = create_span(
    trace_id=trace_id,
    service_name="order-service",
    operation_name="get_orders",
    duration_ms=300.0,
    parent_span_id=api_span.span_id,
    kind=SpanKind.SERVER
)

# Database query
db_span = create_span(
    trace_id=trace_id,
    service_name="order-service",
    operation_name="SELECT orders",
    duration_ms=200.0,
    parent_span_id=order_span.span_id,
    kind=SpanKind.CLIENT,
    attributes={"db.system": "postgresql", "db.statement": "SELECT * FROM orders"}
)

# Payment service check
payment_span = create_span(
    trace_id=trace_id,
    service_name="payment-service",
    operation_name="check_payment_status",
    duration_ms=100.0,
    parent_span_id=order_span.span_id,
    kind=SpanKind.CLIENT
)

# Ingest all spans
aggregator.ingest_spans([api_span, auth_span, order_span, db_span, payment_span])

# Complete and analyze the trace
trace = aggregator.complete_trace(trace_id)

print(f"Trace completed:")
print(f"  Duration: {trace.duration_ms}ms")
print(f"  Services: {', '.join(trace.services)}")
print(f"  Spans: {trace.span_count}")

# Analyze dependencies
dep_analyzer.analyze_trace(trace)
dependencies = dep_analyzer.get_dependencies()
print(f"\nService Dependencies:")
for dep in dependencies:
    print(f"  {dep['from_service']} → {dep['to_service']}")

# Find critical path
critical_path = dep_analyzer.find_critical_path(trace)
print(f"\nCritical Path:")
for span in critical_path:
    print(f"  {span.service_name}:{span.operation_name} ({span.duration_ms}ms)")
```

## Use Cases

### 1. Debugging Distributed Systems

Track requests across services to identify where failures occur:

```python
# Find traces with errors
error_traces = aggregator.query_traces(has_errors=True)

for trace in error_traces:
    error_spans = [s for s in trace.spans if s.status == SpanStatus.ERROR]
    print(f"Trace {trace.trace_id}: {len(error_spans)} errors")
    for span in error_spans:
        print(f"  Error in {span.service_name}:{span.operation_name}")
```

### 2. Performance Optimization

Identify slow operations and bottlenecks:

```python
# Analyze performance across all traces
traces = aggregator.completed_traces
perf_results = perf_analyzer.analyze_traces(traces)

# Find slowest operations
for op in perf_results['slowest_operations'][:5]:
    print(f"{op['operation']}")
    print(f"  P95: {op['p95_ms']}ms")
    print(f"  P99: {op['p99_ms']}ms")
    print(f"  Count: {op['count']}")
```

### 3. Service Dependency Mapping

Understand service relationships and communication patterns:

```python
# Build service dependency graph
for trace in aggregator.completed_traces:
    dep_analyzer.analyze_trace(trace)

service_graph = dep_analyzer.get_service_graph()

print("Service Dependencies:")
for service, dependencies in service_graph.items():
    print(f"{service} depends on: {', '.join(dependencies)}")
```

### 4. Capacity Planning

Analyze service load and performance characteristics:

```python
# Get service statistics
stats = aggregator.get_service_statistics()

for service, service_stats in stats.items():
    print(f"\n{service}:")
    print(f"  Total spans: {service_stats['span_count']}")
    print(f"  Avg duration: {service_stats['avg_duration_ms']:.2f}ms")
    print(f"  Error rate: {service_stats['error_count'] / service_stats['span_count']:.2%}")
    print(f"  Operations: {', '.join(service_stats['operations'])}")
```

## Integration Examples

### Integrating with HTTP Requests

```python
def trace_http_request(method: str, url: str, trace_id: str, parent_span_id: Optional[str] = None):
    """Trace an HTTP request."""
    start_time = datetime.datetime.now(datetime.timezone.utc)
    
    # Make the actual request here
    # response = requests.request(method, url)
    
    end_time = datetime.datetime.now(datetime.timezone.utc)
    duration_ms = (end_time - start_time).total_seconds() * 1000
    
    span = create_span(
        trace_id=trace_id,
        service_name="http-client",
        operation_name=f"{method} {url}",
        duration_ms=duration_ms,
        parent_span_id=parent_span_id,
        kind=SpanKind.CLIENT,
        attributes={"http.method": method, "http.url": url}
    )
    
    aggregator.ingest_span(span)
    return span
```

### Integrating with Database Operations

```python
def trace_database_query(query: str, trace_id: str, parent_span_id: str):
    """Trace a database query."""
    start_time = datetime.datetime.now(datetime.timezone.utc)
    
    # Execute the query here
    # result = db.execute(query)
    
    end_time = datetime.datetime.now(datetime.timezone.utc)
    duration_ms = (end_time - start_time).total_seconds() * 1000
    
    span = create_span(
        trace_id=trace_id,
        service_name="database",
        operation_name="query",
        duration_ms=duration_ms,
        parent_span_id=parent_span_id,
        kind=SpanKind.CLIENT,
        attributes={"db.system": "postgresql", "db.statement": query}
    )
    
    aggregator.ingest_span(span)
    return span
```

## Best Practices

1. **Always propagate trace context**: Pass trace_id and parent_span_id across service boundaries
2. **Use meaningful operation names**: Make spans easily identifiable (e.g., "GET /users", "query_orders")
3. **Add relevant attributes**: Include useful metadata like user IDs, request IDs, etc.
4. **Complete traces promptly**: Call `complete_trace()` when all spans are collected
5. **Set appropriate span kinds**: Use correct kinds (SERVER, CLIENT, etc.) for better analysis
6. **Mark errors properly**: Set span status to ERROR when operations fail
7. **Keep sampling in mind**: For high-volume systems, consider sampling strategies

## Performance Considerations

- **Memory usage**: Completed traces are kept in memory; implement retention policies for production use
- **Span ingestion**: Batch span ingestion when possible for better performance
- **Query optimization**: Use filters to limit trace query results
- **Analysis caching**: Cache performance analysis results for frequently accessed data

## Comparison with Industry Tools

TracAgg provides similar functionality to:

- **Jaeger**: Distributed tracing system developed by Uber
- **Zipkin**: Distributed tracing system developed by Twitter
- **AWS X-Ray**: Distributed tracing for AWS services
- **Google Cloud Trace**: Distributed tracing for Google Cloud

Key differences:
- **Homegrown**: Built from scratch using standard library
- **Lightweight**: No external dependencies required
- **Customizable**: Easy to extend and modify for specific needs
- **Educational**: Clear implementation for learning distributed tracing concepts

## Technical Details

### Trace ID Generation

Trace IDs are generated using SHA-256 hashing of timestamp and unique data:

```python
def create_trace_id() -> str:
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    random_data = f"{timestamp}-{id({})}"
    return hashlib.sha256(random_data.encode()).hexdigest()[:32]
```

### Critical Path Algorithm

The critical path algorithm uses recursive tree traversal to find the longest path:

1. Start from root span
2. For each span, recursively compute the longest path through its children
3. Select the child with the maximum path duration
4. Return the path as a list of spans

### Performance Analysis

Performance analysis computes standard statistical measures:

- Mean, median, min, max
- Standard deviation
- Percentiles (P95, P99) using linear interpolation
- Error rates

## Limitations

- **In-memory storage**: Traces are stored in memory; not suitable for very large-scale production use without modification
- **No persistence**: Traces are lost on restart; add database integration for persistence
- **No distributed collection**: Designed for single-process aggregation; needs network protocol for distributed deployment
- **Simplified sampling**: Implements basic sampling; advanced sampling strategies not included

## Future Enhancements

Potential enhancements for production use:

1. **Persistent storage**: Integration with databases (PostgreSQL, Cassandra)
2. **Distributed collection**: Network protocol for collecting spans from remote services
3. **Advanced sampling**: Adaptive and tail-based sampling
4. **Real-time analysis**: Stream processing for real-time bottleneck detection
5. **Visualization**: Web UI for exploring traces
6. **Alerting**: Automated alerts for performance anomalies
7. **Export formats**: Support for OpenTelemetry, Jaeger, Zipkin formats

## Related Modules

- **PerProVis**: Performance profiling visualizer (companion module)
- **TopoMapper**: Application topology mapper from traffic (companion module)
- **OpenTelemetry Integration**: civ_arcos/core/runtime_monitoring.py

## License

Part of the CIV-ARCOS project. See LICENSE file for details.

## References

- OpenTelemetry Tracing Specification
- Jaeger Architecture
- Zipkin Design
- Google Dapper Paper
- Distributed Tracing Best Practices
