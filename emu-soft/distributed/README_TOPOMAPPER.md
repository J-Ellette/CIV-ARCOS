# TopoMapper - Application Topology Mapper from Actual Traffic

**Automatically discover and map application topology by analyzing real network traffic**

## Overview

TopoMapper automatically discovers and maps application topology by analyzing actual network traffic patterns and service interactions. It creates dynamic topology maps showing services, dependencies, communication patterns, and performance characteristics without requiring manual configuration or service registration.

## Purpose

Traditional service discovery requires manual registration or configuration. TopoMapper provides:

- **Automatic Discovery**: Discover services from actual traffic patterns
- **Dynamic Mapping**: Build topology maps without manual configuration
- **Dependency Analysis**: Identify service relationships and communication flows
- **Performance Insights**: Track latency, throughput, and error rates per dependency
- **Visual Representations**: Generate topology visualizations and reports
- **Critical Path Identification**: Find bottlenecks and critical services

## Features

### 1. Topology Mapper (`TopologyMapper`)

Automatically discover and map services from network traffic:

```python
from topomapper import TopologyMapper, create_traffic_observation, Protocol

mapper = TopologyMapper()

# Record traffic observations
obs = create_traffic_observation(
    source_host="client.internal",
    source_port=54321,
    dest_host="api.example.com",
    dest_port=443,
    protocol=Protocol.HTTPS,
    method="GET",
    path="/api/users",
    latency_ms=45.0
)

mapper.observe_traffic(obs)

# Generate topology map
topology_map = mapper.generate_topology_map()
print(f"Discovered {len(topology_map.services)} services")
print(f"Found {len(topology_map.dependencies)} dependencies")
```

**Key Capabilities:**
- Automatic service discovery
- Protocol detection
- Dependency tracking
- Performance metrics collection
- Service classification

### 2. Traffic Observation

Record network traffic between services:

```python
# HTTP/HTTPS traffic
http_obs = create_traffic_observation(
    source_host="web-app", source_port=8080,
    dest_host="api-gateway", dest_port=443,
    protocol=Protocol.HTTPS,
    method="POST",
    path="/api/orders",
    bytes_sent=2048,
    bytes_received=4096,
    latency_ms=125.0,
    status_code=201
)

# Database traffic
db_obs = create_traffic_observation(
    source_host="user-service", source_port=8080,
    dest_host="postgres.db", dest_port=5432,
    protocol=Protocol.POSTGRES,
    bytes_sent=512,
    bytes_received=8192,
    latency_ms=15.0
)

# Cache traffic
cache_obs = create_traffic_observation(
    source_host="user-service", source_port=8080,
    dest_host="redis.cache", dest_port=6379,
    protocol=Protocol.REDIS,
    bytes_sent=256,
    bytes_received=1024,
    latency_ms=3.0
)

# Batch observation
mapper.observe_traffic_batch([http_obs, db_obs, cache_obs])
```

**Supported Protocols:**
- HTTP/HTTPS
- gRPC
- WebSocket
- PostgreSQL, MySQL, MongoDB
- Redis
- Kafka, AMQP
- TCP/UDP

### 3. Service Discovery

Services are automatically discovered and classified:

```python
# Get all discovered services
for service_id, service in topology_map.services.items():
    print(f"{service.service_name}:")
    print(f"  Type: {service.service_type.value}")
    print(f"  Endpoints: {[ep.to_string() for ep in service.endpoints]}")
    print(f"  First seen: {service.first_seen}")
    print(f"  Last seen: {service.last_seen}")
```

**Service Types:**
- Web Server
- API Gateway
- Microservice
- Database
- Cache
- Message Queue
- Load Balancer
- External API

### 4. Service Classification (`ServiceClassifier`)

Automatically classify services based on characteristics:

```python
from topomapper import ServiceClassifier

classifier = ServiceClassifier()

# Classification is automatic but can be accessed directly
service_type = classifier.classify_service(endpoint, observation)
```

**Classification Factors:**
- Port numbers (e.g., 5432 → PostgreSQL)
- Protocol types
- Hostname patterns
- Traffic patterns
- Request paths

### 5. Dependency Analysis

Analyze dependencies between services:

```python
# Get dependencies for a specific service
service_id = "abc123"
outbound_deps = mapper.get_service_dependencies(
    service_id,
    direction=TrafficDirection.OUTBOUND
)

for dep in outbound_deps:
    target = topology_map.services[dep.target_service]
    print(f"→ {target.service_name}")
    print(f"  Requests: {dep.request_count}")
    print(f"  Avg latency: {dep.avg_latency_ms:.1f}ms")
    print(f"  Errors: {dep.error_count}")
    print(f"  Protocol: {dep.protocol.value}")
```

**Dependency Metrics:**
- Request count
- Total bytes transferred
- Average latency
- Error count
- First/last seen timestamps
- Protocol used

### 6. Critical Service Identification

Find critical services based on dependency count:

```python
# Find services with most dependencies
critical_services = mapper.find_critical_services()

for service_id, dep_count in critical_services[:10]:
    service = mapper.get_service(service_id)
    print(f"{service.service_name}: {dep_count} dependencies")
```

Services with many dependencies are often:
- Central to the architecture
- Single points of failure
- Prime candidates for monitoring

### 7. Bottleneck Detection

Identify performance bottlenecks:

```python
# Find slow dependencies
bottlenecks = mapper.find_bottlenecks(latency_threshold_ms=100.0)

for dep in bottlenecks:
    source = topology_map.services[dep.source_service]
    target = topology_map.services[dep.target_service]
    print(f"{source.service_name} → {target.service_name}")
    print(f"  Avg latency: {dep.avg_latency_ms:.1f}ms")
    print(f"  Requests: {dep.request_count}")
```

### 8. Traffic Pattern Analysis

Analyze overall traffic patterns:

```python
patterns = mapper.analyze_traffic_patterns()

print(f"Total observations: {patterns['total_observations']}")
print(f"Total bytes transferred: {patterns['total_bytes']}")
print(f"Average latency: {patterns['avg_latency_ms']:.1f}ms")
print(f"Error rate: {patterns['error_rate']:.2%}")
print(f"Protocol distribution: {patterns['protocol_distribution']}")
```

**Analysis Includes:**
- Total traffic volume
- Average latency across all traffic
- Error rates
- Protocol distribution
- Service and dependency counts

### 9. Topology Visualization (`TopologyVisualizer`)

Generate visual representations of topology:

```python
from topomapper import TopologyVisualizer

visualizer = TopologyVisualizer(topology_map)

# ASCII text map
ascii_map = visualizer.generate_ascii_map()
print(ascii_map)

# Graphviz DOT format
dot_graph = visualizer.generate_dot_graph()
with open("topology.dot", "w") as f:
    f.write(dot_graph)
```

**Visualization Formats:**
- ASCII text diagrams
- Graphviz DOT format (for rendering with Graphviz)
- JSON export (for custom visualization)

### 10. ASCII Topology Map

Generate human-readable topology maps:

```python
visualizer = TopologyVisualizer(topology_map)
print(visualizer.generate_ascii_map())
```

**Example Output:**
```
================================================================================
APPLICATION TOPOLOGY MAP
================================================================================

Total Services: 5
Total Dependencies: 6

SERVICES:
--------------------------------------------------------------------------------
  • api-gateway (api_gateway)
    - api.example.com:443 [https]
  • user-service (microservice)
    - user-service.internal:8080 [http]
  • postgres (database)
    - db.internal:5432 [postgres]
  • redis (cache)
    - cache.internal:6379 [redis]

DEPENDENCIES:
--------------------------------------------------------------------------------
  api-gateway
    → user-service [150 reqs, 35ms avg]
    → auth-service [150 reqs, 20ms avg]

  user-service
    → postgres [75 reqs, 25ms avg]
    → redis [150 reqs, 5ms avg]
```

### 11. Graphviz DOT Export

Export topology for visualization with Graphviz:

```python
visualizer = TopologyVisualizer(topology_map)
dot_graph = visualizer.generate_dot_graph()

# Save to file
with open("topology.dot", "w") as f:
    f.write(dot_graph)

# Render with Graphviz (if installed)
# $ dot -Tpng topology.dot -o topology.png
```

The DOT format includes:
- Service nodes with types and names
- Dependency edges with request counts and latencies
- Color coding by service type
- Error highlighting

### 12. JSON Export

Export topology data for analysis or custom visualization:

```python
# Export complete topology
topology_json = topology_map.to_json()

# Or as dictionary
topology_dict = topology_map.to_dict()

# Save to file
with open("topology.json", "w") as f:
    f.write(topology_json)
```

## Data Models

### TrafficObservation

Represents observed network traffic:

```python
@dataclass
class TrafficObservation:
    timestamp: str
    source: NetworkEndpoint
    destination: NetworkEndpoint
    protocol: Protocol
    bytes_sent: int
    bytes_received: int
    latency_ms: float
    status_code: Optional[int] = None
    method: Optional[str] = None
    path: Optional[str] = None
```

### Service

Represents a discovered service:

```python
@dataclass
class Service:
    service_id: str
    service_name: str
    service_type: ServiceType
    endpoints: List[NetworkEndpoint]
    tags: Dict[str, str]
    metadata: Dict[str, Any]
    first_seen: Optional[str]
    last_seen: Optional[str]
```

### ServiceDependency

Represents a dependency between services:

```python
@dataclass
class ServiceDependency:
    source_service: str
    target_service: str
    protocol: Protocol
    direction: TrafficDirection
    request_count: int
    total_bytes: int
    error_count: int
    avg_latency_ms: float
    first_seen: Optional[str]
    last_seen: Optional[str]
```

## Complete Example: Microservices Application

```python
from topomapper import (
    TopologyMapper, TopologyVisualizer,
    create_traffic_observation, Protocol
)

# Initialize mapper
mapper = TopologyMapper()

# Simulate traffic from a microservices application

# 1. Client → API Gateway
for i in range(100):
    obs = create_traffic_observation(
        "client.external", 54321 + i,
        "api.example.com", 443,
        Protocol.HTTPS,
        method="GET",
        path="/api/users",
        latency_ms=45.0 + (i % 10)
    )
    mapper.observe_traffic(obs)

# 2. API Gateway → Auth Service
for i in range(100):
    obs = create_traffic_observation(
        "api.example.com", 443,
        "auth-service.internal", 8080,
        Protocol.HTTP,
        method="POST",
        path="/verify",
        latency_ms=20.0
    )
    mapper.observe_traffic(obs)

# 3. API Gateway → User Service
for i in range(100):
    obs = create_traffic_observation(
        "api.example.com", 443,
        "user-service.internal", 8080,
        Protocol.HTTP,
        method="GET",
        path="/users",
        latency_ms=35.0
    )
    mapper.observe_traffic(obs)

# 4. User Service → Database
for i in range(50):
    obs = create_traffic_observation(
        "user-service.internal", 8080,
        "postgres.db.internal", 5432,
        Protocol.POSTGRES,
        bytes_sent=512,
        bytes_received=4096,
        latency_ms=25.0
    )
    mapper.observe_traffic(obs)

# 5. User Service → Cache (cache hits)
for i in range(100):
    obs = create_traffic_observation(
        "user-service.internal", 8080,
        "redis.cache.internal", 6379,
        Protocol.REDIS,
        bytes_sent=256,
        bytes_received=1024,
        latency_ms=5.0
    )
    mapper.observe_traffic(obs)

# 6. Some errors
for i in range(5):
    obs = create_traffic_observation(
        "api.example.com", 443,
        "user-service.internal", 8080,
        Protocol.HTTP,
        method="GET",
        path="/users",
        status_code=500,
        latency_ms=150.0
    )
    mapper.observe_traffic(obs)

# Generate topology map
topology_map = mapper.generate_topology_map()

print(f"Topology Analysis:")
print(f"  Services: {len(topology_map.services)}")
print(f"  Dependencies: {len(topology_map.dependencies)}")

# Analyze traffic patterns
patterns = mapper.analyze_traffic_patterns()
print(f"\nTraffic Patterns:")
print(f"  Total observations: {patterns['total_observations']}")
print(f"  Average latency: {patterns['avg_latency_ms']:.1f}ms")
print(f"  Error rate: {patterns['error_rate']:.2%}")

# Find critical services
critical = mapper.find_critical_services()
print(f"\nCritical Services:")
for service_id, dep_count in critical[:5]:
    service = mapper.get_service(service_id)
    print(f"  {service.service_name}: {dep_count} connections")

# Find bottlenecks
bottlenecks = mapper.find_bottlenecks(latency_threshold_ms=30.0)
print(f"\nBottlenecks (>30ms):")
for dep in bottlenecks:
    source = topology_map.services[dep.source_service]
    target = topology_map.services[dep.target_service]
    print(f"  {source.service_name} → {target.service_name}: {dep.avg_latency_ms:.1f}ms")

# Visualize
visualizer = TopologyVisualizer(topology_map)
print("\n" + visualizer.generate_ascii_map())

# Export
topology_map_json = topology_map.to_json()
with open("topology.json", "w") as f:
    f.write(topology_map_json)

dot_graph = visualizer.generate_dot_graph()
with open("topology.dot", "w") as f:
    f.write(dot_graph)
```

## Use Cases

### 1. Service Discovery

Automatically discover services without service registries:

```python
mapper = TopologyMapper()

# Observe traffic from various sources
# (e.g., network packet capture, proxy logs, application logs)

# Periodically check discovered services
topology = mapper.generate_topology_map()
for service in topology.services.values():
    print(f"Found: {service.service_name} at {service.endpoints[0].to_string()}")
```

### 2. Architecture Documentation

Generate up-to-date architecture diagrams:

```python
# Collect traffic over time
mapper = TopologyMapper()
# ... observe traffic ...

# Generate visualization
visualizer = TopologyVisualizer(mapper.generate_topology_map())
dot_graph = visualizer.generate_dot_graph()

# Save and render
with open("architecture.dot", "w") as f:
    f.write(dot_graph)
```

### 3. Performance Monitoring

Track performance between services:

```python
# Monitor continuously
mapper = TopologyMapper()

# Analyze periodically
patterns = mapper.analyze_traffic_patterns()
if patterns['avg_latency_ms'] > 100:
    print("WARNING: High average latency detected")

bottlenecks = mapper.find_bottlenecks(50.0)
if bottlenecks:
    print(f"ALERT: {len(bottlenecks)} bottlenecks found")
```

### 4. Dependency Analysis

Understand service dependencies:

```python
# Find what each service depends on
for service_id in topology_map.services:
    deps = mapper.get_service_dependencies(
        service_id,
        direction=TrafficDirection.OUTBOUND
    )
    if deps:
        service = mapper.get_service(service_id)
        print(f"{service.service_name} depends on:")
        for dep in deps:
            target = topology_map.services[dep.target_service]
            print(f"  - {target.service_name}")
```

### 5. Migration Planning

Identify dependencies before migrating services:

```python
# Before migrating a service, check its dependencies
service_to_migrate = "user-service"

# Find all services that depend on it
inbound = mapper.get_service_dependencies(
    service_to_migrate,
    direction=TrafficDirection.INBOUND
)

print(f"Services that will be affected by migrating {service_to_migrate}:")
for dep in inbound:
    source = topology_map.services[dep.source_service]
    print(f"  - {source.service_name} ({dep.request_count} requests)")
```

### 6. Capacity Planning

Analyze traffic patterns for capacity planning:

```python
patterns = mapper.analyze_traffic_patterns()

print(f"Current traffic: {patterns['total_bytes'] / 1_000_000:.2f} MB")
print(f"Request count: {patterns['total_observations']}")

# Analyze per-service load
for service_id, service in topology_map.services.items():
    deps = mapper.get_service_dependencies(service_id)
    total_requests = sum(d.request_count for d in deps)
    print(f"{service.service_name}: {total_requests} total requests")
```

## Integration Patterns

### Integration with Network Packet Capture

```python
# Pseudo-code for packet capture integration
def process_packet(packet):
    obs = create_traffic_observation(
        source_host=packet.src_ip,
        source_port=packet.src_port,
        dest_host=packet.dst_ip,
        dest_port=packet.dst_port,
        protocol=detect_protocol(packet),
        bytes_sent=len(packet.payload),
        bytes_received=0,  # Set when response arrives
        latency_ms=0.0  # Calculate from request/response pair
    )
    mapper.observe_traffic(obs)
```

### Integration with Application Logs

```python
# Parse application logs to create observations
import re

def parse_http_log(log_line):
    # Example: "2024-01-01 12:00:00 GET /api/users 200 45ms"
    match = re.match(r'(\S+) (\S+) (\S+) (\d+) (\d+)ms', log_line)
    if match:
        timestamp, method, path, status, latency = match.groups()
        obs = create_traffic_observation(
            source_host="app-server",
            source_port=8080,
            dest_host="api-gateway",
            dest_port=443,
            protocol=Protocol.HTTP,
            method=method,
            path=path,
            status_code=int(status),
            latency_ms=float(latency)
        )
        mapper.observe_traffic(obs)
```

### Integration with Service Mesh

```python
# Integration with service mesh (e.g., Istio) telemetry
def process_envoy_metric(metric):
    obs = create_traffic_observation(
        source_host=metric.source_workload,
        source_port=metric.source_port,
        dest_host=metric.destination_workload,
        dest_port=metric.destination_port,
        protocol=Protocol[metric.protocol.upper()],
        bytes_sent=metric.request_bytes,
        bytes_received=metric.response_bytes,
        latency_ms=metric.duration_ms,
        status_code=metric.response_code
    )
    mapper.observe_traffic(obs)
```

## Best Practices

1. **Continuous Observation**: Feed traffic observations continuously for accurate maps
2. **Time Windows**: Analyze topology over specific time windows (e.g., peak hours)
3. **Sampling**: Sample high-volume traffic to reduce overhead
4. **Filtering**: Filter out health checks and internal monitoring traffic
5. **Classification Rules**: Customize service classification for your environment
6. **Periodic Export**: Regularly export topology for historical analysis
7. **Alerting**: Set up alerts for topology changes or new dependencies

## Performance Considerations

- **Memory Usage**: Stores all observations and services in memory
- **Processing Overhead**: Minimal overhead per observation (~0.1ms)
- **Sampling**: Consider sampling for high-volume environments (>10k req/s)
- **Batch Processing**: Use `observe_traffic_batch()` for better performance
- **Cleanup**: Implement retention policies for old observations

## Limitations

- **Single Process**: Designed for single-process use; needs distributed architecture for multi-host
- **Memory Based**: All data stored in memory; implement persistence for production
- **No Real-time Packet Capture**: Requires external capture/logging integration
- **Static Classification**: Service classification based on rules, not ML
- **No Historical Trending**: Current state only; add database for historical analysis

## Future Enhancements

Potential improvements:

1. **Machine Learning Classification**: Learn service types from patterns
2. **Anomaly Detection**: Detect unusual traffic patterns
3. **Distributed Architecture**: Multi-host topology mapping
4. **Real-time Streaming**: Stream processing for real-time updates
5. **Time-series Analysis**: Track topology changes over time
6. **Security Analysis**: Detect unauthorized communications
7. **Auto-scaling Recommendations**: Suggest scaling based on traffic

## Related Modules

- **TracAgg**: Distributed tracing aggregator (companion module)
- **PerProVis**: Performance profiling visualizer (companion module)
- **scalability_optimizer.py**: Distributed system optimization in emu-soft/distributed

## License

Part of the CIV-ARCOS project. See LICENSE file for details.

## References

- Service Mesh Observability
- Network Traffic Analysis
- Application Topology Discovery
- Dependency Mapping Techniques
- Microservices Architecture Patterns
