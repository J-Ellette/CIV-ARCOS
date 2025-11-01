"""
Application Topology Mapper from Actual Traffic (TopoMapper).

Automatically discovers and maps application topology by analyzing actual network
traffic patterns and service interactions. Creates dynamic topology maps showing
services, dependencies, and communication patterns.
"""

import json
import hashlib
import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict


class ServiceType(Enum):
    """Types of services in the topology."""

    WEB_SERVER = "web_server"
    API_GATEWAY = "api_gateway"
    MICROSERVICE = "microservice"
    DATABASE = "database"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"
    LOAD_BALANCER = "load_balancer"
    EXTERNAL_API = "external_api"
    UNKNOWN = "unknown"


class Protocol(Enum):
    """Network protocols."""

    HTTP = "http"
    HTTPS = "https"
    TCP = "tcp"
    UDP = "udp"
    GRPC = "grpc"
    WEBSOCKET = "websocket"
    AMQP = "amqp"
    KAFKA = "kafka"
    REDIS = "redis"
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MONGODB = "mongodb"


class TrafficDirection(Enum):
    """Direction of traffic flow."""

    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BIDIRECTIONAL = "bidirectional"


@dataclass
class NetworkEndpoint:
    """Represents a network endpoint (host:port)."""

    host: str
    port: int
    protocol: Protocol

    def to_string(self) -> str:
        """Convert to string representation."""
        return f"{self.host}:{self.port}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"host": self.host, "port": self.port, "protocol": self.protocol.value}


@dataclass
class TrafficObservation:
    """Represents an observed network traffic event."""

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result["source"] = self.source.to_dict()
        result["destination"] = self.destination.to_dict()
        result["protocol"] = self.protocol.value
        return result


@dataclass
class Service:
    """Represents a service in the topology."""

    service_id: str
    service_name: str
    service_type: ServiceType
    endpoints: List[NetworkEndpoint] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result["service_type"] = self.service_type.value
        result["endpoints"] = [ep.to_dict() for ep in self.endpoints]
        return result


@dataclass
class ServiceDependency:
    """Represents a dependency between two services."""

    source_service: str
    target_service: str
    protocol: Protocol
    direction: TrafficDirection
    request_count: int = 0
    total_bytes: int = 0
    error_count: int = 0
    avg_latency_ms: float = 0.0
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result["protocol"] = self.protocol.value
        result["direction"] = self.direction.value
        return result


@dataclass
class TopologyMap:
    """Represents the complete application topology."""

    services: Dict[str, Service]
    dependencies: List[ServiceDependency]
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "services": {k: v.to_dict() for k, v in self.services.items()},
            "dependencies": [d.to_dict() for d in self.dependencies],
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class TopologyMapper:
    """
    Maps application topology from actual network traffic patterns.

    Analyzes traffic observations to discover services, their relationships,
    and communication patterns automatically.
    """

    def __init__(self):
        """Initialize topology mapper."""
        self.services: Dict[str, Service] = {}
        self.endpoints_to_service: Dict[str, str] = {}
        self.traffic_observations: List[TrafficObservation] = []
        self.dependencies: Dict[Tuple[str, str], ServiceDependency] = {}
        self.service_classifier = ServiceClassifier()

    def observe_traffic(self, observation: TrafficObservation) -> None:
        """
        Record a traffic observation.

        Args:
            observation: Network traffic observation
        """
        self.traffic_observations.append(observation)

        # Discover or update services
        source_service_id = self._discover_service(observation.source, observation)
        dest_service_id = self._discover_service(observation.destination, observation)

        # Record dependency
        if source_service_id and dest_service_id:
            self._record_dependency(source_service_id, dest_service_id, observation)

    def observe_traffic_batch(self, observations: List[TrafficObservation]) -> None:
        """
        Record multiple traffic observations.

        Args:
            observations: List of network traffic observations
        """
        for observation in observations:
            self.observe_traffic(observation)

    def _discover_service(
        self, endpoint: NetworkEndpoint, observation: TrafficObservation
    ) -> Optional[str]:
        """
        Discover or identify a service from an endpoint.

        Args:
            endpoint: Network endpoint
            observation: Traffic observation for context

        Returns:
            Service ID
        """
        endpoint_key = f"{endpoint.host}:{endpoint.port}"

        # Check if endpoint already mapped to a service
        if endpoint_key in self.endpoints_to_service:
            service_id = self.endpoints_to_service[endpoint_key]
            service = self.services[service_id]
            service.last_seen = observation.timestamp
            return service_id

        # Discover new service
        service_name = self._infer_service_name(endpoint, observation)
        service_type = self.service_classifier.classify_service(endpoint, observation)

        service_id = self._generate_service_id(service_name, endpoint)

        service = Service(
            service_id=service_id,
            service_name=service_name,
            service_type=service_type,
            endpoints=[endpoint],
            first_seen=observation.timestamp,
            last_seen=observation.timestamp,
            tags=self._extract_tags(endpoint, observation),
        )

        self.services[service_id] = service
        self.endpoints_to_service[endpoint_key] = service_id

        return service_id

    def _generate_service_id(self, service_name: str, endpoint: NetworkEndpoint) -> str:
        """
        Generate a unique service ID.

        Uses deterministic hashing for consistent IDs across observations,
        which ensures the same service is always identified with the same ID.
        """
        unique_str = f"{service_name}-{endpoint.host}-{endpoint.port}"
        return hashlib.sha256(unique_str.encode()).hexdigest()[:16]

    def _infer_service_name(
        self, endpoint: NetworkEndpoint, observation: TrafficObservation
    ) -> str:
        """
        Infer service name from endpoint and traffic patterns.

        Args:
            endpoint: Network endpoint
            observation: Traffic observation

        Returns:
            Inferred service name
        """
        # Try to infer from hostname
        if "." in endpoint.host:
            parts = endpoint.host.split(".")
            if len(parts) >= 2:
                return parts[0]

        # Try to infer from path patterns
        if observation.path:
            path_parts = observation.path.strip("/").split("/")
            if path_parts and path_parts[0]:
                return path_parts[0]

        # Fallback to endpoint description
        return f"service-{endpoint.host.replace('.', '-')}-{endpoint.port}"

    def _extract_tags(
        self, endpoint: NetworkEndpoint, observation: TrafficObservation
    ) -> Dict[str, str]:
        """Extract tags from endpoint and observation."""
        tags = {
            "host": endpoint.host,
            "port": str(endpoint.port),
            "protocol": endpoint.protocol.value,
        }

        if observation.method:
            tags["method"] = observation.method

        return tags

    def _record_dependency(
        self, source_service_id: str, dest_service_id: str, observation: TrafficObservation
    ) -> None:
        """
        Record or update a service dependency.

        Args:
            source_service_id: Source service ID
            dest_service_id: Destination service ID
            observation: Traffic observation
        """
        dep_key = (source_service_id, dest_service_id)

        if dep_key not in self.dependencies:
            self.dependencies[dep_key] = ServiceDependency(
                source_service=source_service_id,
                target_service=dest_service_id,
                protocol=observation.protocol,
                direction=TrafficDirection.OUTBOUND,
                first_seen=observation.timestamp,
                last_seen=observation.timestamp,
            )

        dep = self.dependencies[dep_key]
        dep.request_count += 1
        dep.total_bytes += observation.bytes_sent + observation.bytes_received
        dep.last_seen = observation.timestamp

        # Update average latency
        dep.avg_latency_ms = (
            dep.avg_latency_ms * (dep.request_count - 1) + observation.latency_ms
        ) / dep.request_count

        # Count errors
        if observation.status_code and observation.status_code >= 400:
            dep.error_count += 1

    def generate_topology_map(self) -> TopologyMap:
        """
        Generate the current topology map.

        Returns:
            Complete topology map
        """
        return TopologyMap(
            services=self.services,
            dependencies=list(self.dependencies.values()),
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            metadata={
                "total_observations": len(self.traffic_observations),
                "service_count": len(self.services),
                "dependency_count": len(self.dependencies),
            },
        )

    def get_service(self, service_id: str) -> Optional[Service]:
        """
        Get a service by ID.

        Args:
            service_id: Service ID

        Returns:
            Service or None if not found
        """
        return self.services.get(service_id)

    def get_service_dependencies(
        self, service_id: str, direction: Optional[TrafficDirection] = None
    ) -> List[ServiceDependency]:
        """
        Get dependencies for a service.

        Args:
            service_id: Service ID
            direction: Filter by direction (INBOUND or OUTBOUND)

        Returns:
            List of dependencies
        """
        dependencies = []

        for dep in self.dependencies.values():
            if direction == TrafficDirection.OUTBOUND:
                if dep.source_service == service_id:
                    dependencies.append(dep)
            elif direction == TrafficDirection.INBOUND:
                if dep.target_service == service_id:
                    dependencies.append(dep)
            else:
                if dep.source_service == service_id or dep.target_service == service_id:
                    dependencies.append(dep)

        return dependencies

    def find_critical_services(self) -> List[Tuple[str, int]]:
        """
        Find critical services based on dependency count.

        Returns:
            List of (service_id, dependency_count) sorted by criticality
        """
        service_dep_counts = defaultdict(int)

        for dep in self.dependencies.values():
            service_dep_counts[dep.source_service] += 1
            service_dep_counts[dep.target_service] += 1

        return sorted(service_dep_counts.items(), key=lambda x: x[1], reverse=True)

    def find_bottlenecks(self, latency_threshold_ms: float = 1000.0) -> List[ServiceDependency]:
        """
        Find bottlenecks based on latency.

        Args:
            latency_threshold_ms: Latency threshold for bottleneck detection

        Returns:
            List of slow dependencies
        """
        bottlenecks = []

        for dep in self.dependencies.values():
            if dep.avg_latency_ms >= latency_threshold_ms:
                bottlenecks.append(dep)

        return sorted(bottlenecks, key=lambda x: x.avg_latency_ms, reverse=True)

    def analyze_traffic_patterns(self) -> Dict[str, Any]:
        """
        Analyze overall traffic patterns.

        Returns:
            Traffic pattern analysis
        """
        # Protocol distribution
        protocol_counts = defaultdict(int)
        for obs in self.traffic_observations:
            protocol_counts[obs.protocol.value] += 1

        # Total traffic
        total_bytes = sum(obs.bytes_sent + obs.bytes_received for obs in self.traffic_observations)

        # Average latency
        avg_latency = (
            sum(obs.latency_ms for obs in self.traffic_observations)
            / len(self.traffic_observations)
            if self.traffic_observations
            else 0.0
        )

        # Error rate
        error_count = sum(
            1 for obs in self.traffic_observations if obs.status_code and obs.status_code >= 400
        )
        error_rate = (
            error_count / len(self.traffic_observations) if self.traffic_observations else 0.0
        )

        return {
            "total_observations": len(self.traffic_observations),
            "total_bytes": total_bytes,
            "avg_latency_ms": avg_latency,
            "error_rate": error_rate,
            "protocol_distribution": dict(protocol_counts),
            "service_count": len(self.services),
            "dependency_count": len(self.dependencies),
        }


class ServiceClassifier:
    """
    Classifies services based on traffic patterns and characteristics.
    """

    def classify_service(
        self, endpoint: NetworkEndpoint, observation: TrafficObservation
    ) -> ServiceType:
        """
        Classify a service based on its characteristics.

        Args:
            endpoint: Network endpoint
            observation: Traffic observation

        Returns:
            Classified service type
        """
        # Classify by port
        if endpoint.port in [80, 8080, 443, 8443]:
            if observation.path and observation.path.startswith("/api"):
                return ServiceType.API_GATEWAY
            return ServiceType.WEB_SERVER

        if endpoint.port in [5432, 5433]:
            return ServiceType.DATABASE

        if endpoint.port in [3306, 3307]:
            return ServiceType.DATABASE

        if endpoint.port in [27017, 27018]:
            return ServiceType.DATABASE

        if endpoint.port in [6379, 6380]:
            return ServiceType.CACHE

        if endpoint.port in [5672, 5673]:  # RabbitMQ
            return ServiceType.MESSAGE_QUEUE

        if endpoint.port in [9092, 9093]:  # Kafka
            return ServiceType.MESSAGE_QUEUE

        # Classify by protocol
        if observation.protocol in [Protocol.AMQP, Protocol.KAFKA]:
            return ServiceType.MESSAGE_QUEUE

        if observation.protocol in [Protocol.REDIS]:
            return ServiceType.CACHE

        if observation.protocol in [Protocol.POSTGRES, Protocol.MYSQL, Protocol.MONGODB]:
            return ServiceType.DATABASE

        # Classify by hostname patterns
        if "api" in endpoint.host.lower():
            return ServiceType.API_GATEWAY

        if "db" in endpoint.host.lower() or "database" in endpoint.host.lower():
            return ServiceType.DATABASE

        if "cache" in endpoint.host.lower() or "redis" in endpoint.host.lower():
            return ServiceType.CACHE

        if "queue" in endpoint.host.lower() or "mq" in endpoint.host.lower():
            return ServiceType.MESSAGE_QUEUE

        if "lb" in endpoint.host.lower() or "loadbalancer" in endpoint.host.lower():
            return ServiceType.LOAD_BALANCER

        # Default to microservice for internal services, external API for others
        if self._is_internal_ip(endpoint.host):
            return ServiceType.MICROSERVICE

        return ServiceType.EXTERNAL_API

    def _is_internal_ip(self, host: str) -> bool:
        """Check if an IP address is internal."""
        if host.startswith("10.") or host.startswith("192.168.") or host.startswith("172."):
            return True
        if host in ["localhost", "127.0.0.1", "::1"]:
            return True
        return False


class TopologyVisualizer:
    """
    Generates visual representations of the topology.
    """

    def __init__(self, topology_map: TopologyMap):
        """
        Initialize visualizer.

        Args:
            topology_map: Topology map to visualize
        """
        self.topology_map = topology_map

    def generate_dot_graph(self) -> str:
        """
        Generate Graphviz DOT format graph.

        Returns:
            DOT format string
        """
        lines = []
        lines.append("digraph topology {")
        lines.append("  rankdir=LR;")
        lines.append("  node [shape=box, style=rounded];")
        lines.append("")

        # Add nodes (services)
        for service_id, service in self.topology_map.services.items():
            label = f"{service.service_name}\\n{service.service_type.value}"
            color = self._get_service_color(service.service_type)
            lines.append(f'  "{service_id}" [label="{label}", color="{color}"];')

        lines.append("")

        # Add edges (dependencies)
        for dep in self.topology_map.dependencies:
            label = f"{dep.request_count} reqs\\n{dep.avg_latency_ms:.0f}ms"
            color = "red" if dep.error_count > 0 else "black"
            lines.append(
                f'  "{dep.source_service}" -> "{dep.target_service}" '
                f'[label="{label}", color="{color}"];'
            )

        lines.append("}")
        return "\n".join(lines)

    def generate_ascii_map(self) -> str:
        """
        Generate ASCII text representation of topology.

        Returns:
            ASCII topology map
        """
        lines = []
        lines.append("=" * 80)
        lines.append("APPLICATION TOPOLOGY MAP")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Total Services: {len(self.topology_map.services)}")
        lines.append(f"Total Dependencies: {len(self.topology_map.dependencies)}")
        lines.append("")

        # List services
        lines.append("SERVICES:")
        lines.append("-" * 80)
        for service in self.topology_map.services.values():
            lines.append(f"  • {service.service_name} ({service.service_type.value})")
            for endpoint in service.endpoints:
                lines.append(f"    - {endpoint.to_string()} [{endpoint.protocol.value}]")

        lines.append("")
        lines.append("DEPENDENCIES:")
        lines.append("-" * 80)

        # Group dependencies by source
        deps_by_source = defaultdict(list)
        for dep in self.topology_map.dependencies:
            deps_by_source[dep.source_service].append(dep)

        for source_id, deps in deps_by_source.items():
            source_service = self.topology_map.services[source_id]
            lines.append(f"  {source_service.service_name}")
            for dep in deps:
                target_service = self.topology_map.services[dep.target_service]
                error_info = f" ({dep.error_count} errors)" if dep.error_count > 0 else ""
                lines.append(
                    f"    → {target_service.service_name} "
                    f"[{dep.request_count} reqs, {dep.avg_latency_ms:.0f}ms avg]{error_info}"
                )
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    def _get_service_color(self, service_type: ServiceType) -> str:
        """Get color for service type."""
        colors = {
            ServiceType.WEB_SERVER: "lightblue",
            ServiceType.API_GATEWAY: "lightgreen",
            ServiceType.MICROSERVICE: "lightyellow",
            ServiceType.DATABASE: "lightcoral",
            ServiceType.CACHE: "lightpink",
            ServiceType.MESSAGE_QUEUE: "lightgray",
            ServiceType.LOAD_BALANCER: "lightcyan",
            ServiceType.EXTERNAL_API: "lightsalmon",
            ServiceType.UNKNOWN: "white",
        }
        return colors.get(service_type, "white")


# Helper functions
def create_traffic_observation(
    source_host: str,
    source_port: int,
    dest_host: str,
    dest_port: int,
    protocol: Protocol,
    bytes_sent: int = 1024,
    bytes_received: int = 2048,
    latency_ms: float = 50.0,
    status_code: Optional[int] = 200,
    method: Optional[str] = "GET",
    path: Optional[str] = "/",
) -> TrafficObservation:
    """
    Create a traffic observation.

    Args:
        source_host: Source host
        source_port: Source port
        dest_host: Destination host
        dest_port: Destination port
        protocol: Network protocol
        bytes_sent: Bytes sent
        bytes_received: Bytes received
        latency_ms: Latency in milliseconds
        status_code: HTTP status code
        method: HTTP method
        path: Request path

    Returns:
        Traffic observation
    """
    return TrafficObservation(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=NetworkEndpoint(source_host, source_port, protocol),
        destination=NetworkEndpoint(dest_host, dest_port, protocol),
        protocol=protocol,
        bytes_sent=bytes_sent,
        bytes_received=bytes_received,
        latency_ms=latency_ms,
        status_code=status_code,
        method=method,
        path=path,
    )


# Example usage functions
def example_basic_topology_mapping():
    """Example: Basic topology mapping from traffic."""
    mapper = TopologyMapper()

    # Simulate traffic observations
    # Client -> API Gateway
    obs1 = create_traffic_observation(
        "192.168.1.100",
        54321,
        "api.example.com",
        443,
        Protocol.HTTPS,
        method="GET",
        path="/api/users",
        latency_ms=45.0,
    )

    # API Gateway -> User Service
    obs2 = create_traffic_observation(
        "api.example.com",
        443,
        "user-service.internal",
        8080,
        Protocol.HTTP,
        method="GET",
        path="/users",
        latency_ms=35.0,
    )

    # User Service -> Database
    obs3 = create_traffic_observation(
        "user-service.internal",
        8080,
        "db.internal",
        5432,
        Protocol.POSTGRES,
        bytes_sent=512,
        bytes_received=4096,
        latency_ms=25.0,
    )

    # User Service -> Cache
    obs4 = create_traffic_observation(
        "user-service.internal",
        8080,
        "cache.internal",
        6379,
        Protocol.REDIS,
        bytes_sent=256,
        bytes_received=1024,
        latency_ms=5.0,
    )

    # Observe traffic
    mapper.observe_traffic_batch([obs1, obs2, obs3, obs4])

    # Generate topology map
    topology_map = mapper.generate_topology_map()

    return topology_map, mapper


def example_traffic_analysis():
    """Example: Analyze traffic patterns."""
    topology_map, mapper = example_basic_topology_mapping()

    # Analyze traffic patterns
    patterns = mapper.analyze_traffic_patterns()

    # Find critical services
    critical_services = mapper.find_critical_services()

    return {"patterns": patterns, "critical_services": critical_services}


def example_topology_visualization():
    """Example: Visualize topology."""
    topology_map, mapper = example_basic_topology_mapping()

    visualizer = TopologyVisualizer(topology_map)

    # Generate ASCII map
    ascii_map = visualizer.generate_ascii_map()

    # Generate DOT graph
    dot_graph = visualizer.generate_dot_graph()

    return {"ascii_map": ascii_map, "dot_graph": dot_graph}


if __name__ == "__main__":
    print("=== Basic Topology Mapping Example ===")
    topology_map, mapper = example_basic_topology_mapping()
    print(f"Services discovered: {len(topology_map.services)}")
    print(f"Dependencies discovered: {len(topology_map.dependencies)}")

    print("\n=== Traffic Analysis Example ===")
    analysis = example_traffic_analysis()
    print(f"Traffic patterns: {json.dumps(analysis['patterns'], indent=2)}")

    print("\n=== Topology Visualization Example ===")
    viz = example_topology_visualization()
    print(viz["ascii_map"])
    print("\nDOT Graph (for Graphviz):")
    print(viz["dot_graph"])
